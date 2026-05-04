(function () {
  const data = window.J40_DASHBOARD_DATA;
  const root = document.getElementById("view-root");
  const generatedAtNode = document.getElementById("generated-at");
  const tabButtons = Array.from(document.querySelectorAll("[data-view]"));
  const STORAGE_KEY = "j40.photo_recategorization_overrides.v3";
  const FALLBACK_IMAGE_PATH = "./assets/image-needed.svg";

  if (!data || !root) {
    if (root) {
      root.innerHTML = '<p class="card">Dashboard data is missing. Run <code>python3 scripts/build_project_control_ui.py</code>.</p>';
    }
    return;
  }

  const state = {
    activeView: "overview",
    activeWorkstreamId: data.workstreams && data.workstreams.length ? data.workstreams[0].id : "",
    photoOverrides: loadPhotoOverrides(),
    lightboxImageBase: null,
    itemDetailRow: null,
    recategorizeOpen: false,
  };

  const imageRegistry = new Map();
  const itemRegistry = new Map();
  let imageKeyCounter = 0;
  let itemKeyCounter = 0;
  const lightbox = createLightbox();
  const itemDetail = createItemDetail();
  const lightboxViewport = {
    scale: 1,
    x: 0,
    y: 0,
    drag: null,
  };
  let fitLightboxOnImageLoad = false;

  if (generatedAtNode) {
    generatedAtNode.textContent = `Generated: ${formatDateTime(data.generated_at)}`;
  }

  tabButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const nextView = button.getAttribute("data-view");
      switchView(nextView);
    });
  });

  window.addEventListener("hashchange", () => {
    if (applyRouteFromHash()) {
      render();
    }
  });

  root.addEventListener("click", (event) => {
    const imageTrigger = event.target.closest("[data-image-key]");
    if (imageTrigger) {
      const imageKey = imageTrigger.getAttribute("data-image-key");
      if (!imageKey) {
        return;
      }
      event.preventDefault();
      openLightbox(imageKey);
      return;
    }

    const workstreamTrigger = event.target.closest("[data-open-workstream-id]");
    if (workstreamTrigger) {
      const workstreamId = workstreamTrigger.getAttribute("data-open-workstream-id");
      if (!workstreamId) {
        return;
      }
      event.preventDefault();
      openWorkstream(workstreamId);
      return;
    }

    const referenceSectionTrigger = event.target.closest("[data-scroll-reference-section]");
    if (referenceSectionTrigger) {
      const sectionId = referenceSectionTrigger.getAttribute("data-scroll-reference-section");
      const sectionNode = sectionId ? document.getElementById(sectionId) : null;
      if (sectionNode) {
        event.preventDefault();
        sectionNode.scrollIntoView({ behavior: "smooth", block: "start" });
      }
      return;
    }

    const itemTrigger = event.target.closest("[data-item-key]");
    if (!itemTrigger) {
      return;
    }
    const itemKey = itemTrigger.getAttribute("data-item-key");
    if (!itemKey) {
      return;
    }
    event.preventDefault();
    openItemDetail(itemKey);
  });

  root.addEventListener("pointerover", (event) => {
    handleVideoPreviewEvent(event, true);
  });

  root.addEventListener("pointerout", (event) => {
    handleVideoPreviewEvent(event, false);
  });

  root.addEventListener("focusin", (event) => {
    handleVideoPreviewEvent(event, true);
  });

  root.addEventListener("focusout", (event) => {
    handleVideoPreviewEvent(event, false);
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && state.lightboxImageBase) {
      closeLightbox();
      return;
    }
    if (event.key === "Escape" && state.itemDetailRow) {
      closeItemDetail();
      return;
    }
    if (!state.lightboxImageBase || isFormControl(event.target)) {
      return;
    }
    if (event.key === "+" || event.key === "=") {
      event.preventDefault();
      zoomLightboxAtCenter(1.25);
    } else if (event.key === "-" || event.key === "_") {
      event.preventDefault();
      zoomLightboxAtCenter(0.8);
    } else if (event.key === "0") {
      event.preventDefault();
      setLightboxActualSize();
    } else if (event.key.toLowerCase() === "f") {
      event.preventDefault();
      fitLightboxImage();
    }
  });

  function escapeHtml(value) {
    return String(value ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  function escapeRegExp(value) {
    return String(value).replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  }

  function switchView(nextView) {
    if (!nextView || nextView === state.activeView) {
      return;
    }
    state.activeView = nextView;
    refreshTabButtons();
    if (state.lightboxImageBase) {
      closeLightbox();
    }
    if (state.itemDetailRow) {
      closeItemDetail();
    }
    updateRouteHash();
    render();
  }

  function openWorkstream(workstreamId) {
    const targetId = cleanString(workstreamId);
    if (!targetId) {
      return;
    }
    state.activeWorkstreamId = targetId;
    if (state.activeView === "workstreams") {
      renderWorkstreams();
      updateRouteHash();
      return;
    }
    switchView("workstreams");
  }

  function refreshTabButtons() {
    tabButtons.forEach((node) => {
      node.classList.toggle("is-active", node.getAttribute("data-view") === state.activeView);
    });
  }

  function applyRouteFromHash() {
    const rawHash = cleanString(decodeURIComponent(window.location.hash.replace(/^#/, "")));
    if (!rawHash) {
      refreshTabButtons();
      return false;
    }
    const [viewPart, workstreamPart] = rawHash.split("/");
    const requestedView = cleanString(viewPart);
    const validViews = new Set(tabButtons.map((node) => cleanString(node.getAttribute("data-view"))).filter(Boolean));
    let changed = false;

    if (validViews.has(requestedView) && requestedView !== state.activeView) {
      state.activeView = requestedView;
      changed = true;
    }

    if (requestedView === "workstreams" && workstreamPart) {
      const requestedWorkstream = cleanString(workstreamPart);
      const exists = (data.workstreams || []).some((workstream) => workstream.id === requestedWorkstream);
      if (exists && requestedWorkstream !== state.activeWorkstreamId) {
        state.activeWorkstreamId = requestedWorkstream;
        changed = true;
      }
    }

    refreshTabButtons();
    return changed;
  }

  function updateRouteHash() {
    const route =
      state.activeView === "workstreams" && state.activeWorkstreamId
        ? `#workstreams/${encodeURIComponent(state.activeWorkstreamId)}`
        : `#${encodeURIComponent(state.activeView)}`;
    if (window.location.hash !== route) {
      history.replaceState(null, "", route);
    }
  }

  function formatToken(value) {
    return String(value || "")
      .replace(/\|/g, ", ")
      .replace(/_/g, " ")
      .replace(/\s+/g, " ")
      .trim()
      .replace(/\b\w/g, (char) => char.toUpperCase());
  }

  function cleanString(value) {
    return String(value ?? "").trim();
  }

  function isFormControl(node) {
    const tagName = node && node.tagName ? node.tagName.toLowerCase() : "";
    return ["input", "select", "textarea", "button"].includes(tagName) || Boolean(node && node.isContentEditable);
  }

  function supplierLabel(row) {
    return cleanString(row && (row.supplier || row.vendor || row.company));
  }

  function formatMoneyAmount(value) {
    const raw = cleanString(value);
    const normalized = raw.replace(/,/g, "");
    if (/^-?\d+(?:\.\d+)?$/.test(normalized)) {
      const parsed = Number(normalized);
      if (Number.isFinite(parsed)) {
        return parsed.toLocaleString();
      }
    }
    return raw;
  }

  function costLabel(row) {
    const amount = cleanString(row && (row.cost || row.amount));
    if (!amount) {
      return "";
    }
    const amountText = formatMoneyAmount(amount);
    const currency = cleanString(row && row.currency);
    if (!currency || new RegExp(`\\b${escapeRegExp(currency)}\\b`, "i").test(amountText) || /\bPKR\b|Rs\.?/i.test(amountText)) {
      return amountText;
    }
    return `${currency} ${amountText}`;
  }

  function tableSupplierCell(row) {
    return escapeHtml(supplierLabel(row) || "-");
  }

  function tableCostCell(row) {
    const cost = costLabel(row);
    if (cost) {
      return escapeHtml(cost);
    }
    const amountStatus = cleanString(row && row.amount_status);
    return escapeHtml(amountStatus ? formatToken(amountStatus) : "-");
  }

  function extractLinksFromText(value) {
    const text = cleanString(value);
    if (!text) {
      return [];
    }
    return Array.from(text.matchAll(/https?:\/\/[^\s<>()"']+/g)).map((match) => match[0].replace(/[.,;:)\]}>]+$/g, ""));
  }

  function linkLabel(url, index) {
    try {
      return new URL(url).hostname.replace(/^www\./, "") || `Link ${index + 1}`;
    } catch (error) {
      return `Link ${index + 1}`;
    }
  }

  function normalizeRowLinks(row) {
    const links = [];
    const seen = new Set();
    const addLink = (candidate, label = "") => {
      const url = cleanString(candidate);
      if (!url || seen.has(url)) {
        return;
      }
      seen.add(url);
      links.push({ url, label: cleanString(label) || linkLabel(url, links.length) });
    };

    if (Array.isArray(row && row.links)) {
      row.links.forEach((link) => {
        if (typeof link === "string") {
          addLink(link);
        } else if (link && typeof link === "object") {
          addLink(link.url || link.href, link.label || link.title);
        }
      });
    }

    [
      row && row.link,
      row && row.url,
      row && row.listing_url,
      row && row.image_url,
      row && row.image && row.image.listing_url,
      row && row.image && row.image.image_url,
    ].forEach((value) => addLink(value));

    [
      row && row.notes,
      row && row.evidence_ref,
      row && row.vendor,
      row && row.company,
      row && row.source_ref,
    ].forEach((value) => extractLinksFromText(value).forEach((url) => addLink(url)));

    return links;
  }

  function renderLinksCell(row) {
    const links = normalizeRowLinks(row);
    if (!links.length) {
      return "-";
    }
    const visible = links.slice(0, 2);
    return `
      <div class="item-links">
        ${visible
          .map((link, index) => `<a class="item-link" href="${escapeHtml(link.url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(link.label || `Link ${index + 1}`)}</a>`)
          .join("")}
        ${links.length > visible.length ? `<span class="table-image-note">+${escapeHtml(links.length - visible.length)} more</span>` : ""}
      </div>
    `;
  }

  function renderLinksPanel(row) {
    const links = normalizeRowLinks(row);
    if (!links.length) {
      return "";
    }
    return `
      <div class="item-detail-links">
        ${links
          .map((link, index) => `<a class="item-link" href="${escapeHtml(link.url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(link.label || `Link ${index + 1}`)}</a>`)
          .join("")}
      </div>
    `;
  }

  function mediaTypeFromPath(path) {
    const normalizedPath = cleanString(path).toLowerCase();
    const match = normalizedPath.match(/\.([a-z0-9]+)(?:[?#].*)?$/);
    const extension = match ? match[1] : "";
    if (["mp4", "mov", "m4v", "webm", "mkv", "avi", "3gp"].includes(extension)) {
      return "video";
    }
    if (["jpg", "jpeg", "png", "webp", "heic", "heif", "gif", "bmp", "avif", "svg"].includes(extension)) {
      return "photo";
    }
    return "";
  }

  function resolvedMediaType(value, path) {
    const normalized = cleanString(value).toLowerCase();
    if (normalized === "image") {
      return "photo";
    }
    if (normalized === "photo" || normalized === "video") {
      return normalized;
    }
    return mediaTypeFromPath(path) || "photo";
  }

  function toNumber(value, fallback = 0) {
    const parsed = Number(value);
    return Number.isFinite(parsed) ? parsed : fallback;
  }

  function truncateText(value, maxLength = 120) {
    const normalized = cleanString(value);
    if (!normalized || normalized.length <= maxLength) {
      return normalized;
    }
    return `${normalized.slice(0, maxLength - 1)}…`;
  }

  function formatDateTime(value) {
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) {
      return value || "Unknown";
    }
    return date.toLocaleString();
  }

  function toneForStatus(status) {
    const key = String(status || "").toLowerCase();
    if (["completed", "closed", "received", "installed", "done", "previously", "properly_specced", "spec_ready", "acquired"].includes(key)) {
      return "good";
    }
    if (key.startsWith("spec_ready")) {
      return "info";
    }
    if ([
      "not_acquired",
      "not_installed",
      "needs_measurement",
      "needs_physical_measurement",
      "needs_close_photo",
      "needs_brake_close_photos",
      "needs_template_trace",
      "needs_station_reconciliation",
      "needs_thread_length_confirmation",
      "needs_cable_end_identification",
      "needs_thread_flare_confirmation",
      "needs_fitting_identification",
      "needs_drum_opening",
      "needs_clip_count",
    ].includes(key)) {
      return "warn";
    }
    if (["blocked"].includes(key)) {
      return "bad";
    }
    if (["in_progress", "in_process", "pending_work", "inspection_pending", "sent_to_painter", "ordered", "ordered_pending_delivery"].includes(key)) {
      return "info";
    }
    return "warn";
  }

  function statusChip(status) {
    const tone = toneForStatus(status);
    return `<span class="chip ${tone}">${escapeHtml(formatToken(status || "unknown"))}</span>`;
  }

  function isSpecReadyStatus(status) {
    const key = cleanString(status).toLowerCase();
    return key === "properly_specced" || key === "spec_ready" || key.startsWith("spec_ready");
  }

  function chip(text) {
    return `<span class="chip">${escapeHtml(text)}</span>`;
  }

  function renderInventoryPageLink(label = "Open inventory") {
    return `<a class="item-link inventory-page-link" href="#parts">${escapeHtml(label)}</a>`;
  }

  function loadPhotoOverrides() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) {
        return {};
      }
      const parsed = JSON.parse(raw);
      return parsed && typeof parsed === "object" ? parsed : {};
    } catch (error) {
      return {};
    }
  }

  function persistPhotoOverrides() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state.photoOverrides));
    } catch (error) {
      setLightboxStatus("Override save failed in browser storage.", "bad");
    }
  }

  function photoLookupById(mediaId) {
    if (!mediaId) {
      return null;
    }
    const lookup = data.photo_lookup || {};
    return lookup[mediaId] || null;
  }

  function isDeletedPhotoOverride(override) {
    if (!override || typeof override !== "object") {
      return false;
    }
    return (
      override.deleted === true ||
      Boolean(cleanString(override.deleted_at)) ||
      cleanString(override.action).toLowerCase() === "delete"
    );
  }

  function photoOverrideKeyForMeta(meta) {
    const mediaId = cleanString(meta && meta.media_id);
    if (mediaId) {
      return mediaId;
    }
    const path = cleanString(meta && meta.path);
    if (path && path !== FALLBACK_IMAGE_PATH) {
      return `path:${path}`;
    }
    return "";
  }

  function isPhotoDeletedByKey(key) {
    return Boolean(key && isDeletedPhotoOverride(state.photoOverrides[key]));
  }

  function isPhotoDeletedById(mediaId) {
    return isPhotoDeletedByKey(cleanString(mediaId));
  }

  function getBasePhotoMeta(image) {
    const img = image && typeof image === "object" ? image : {};
    const mediaId = cleanString(img.media_id);
    const lookup = photoLookupById(mediaId) || {};
    const path = cleanString(img.path || lookup.path || FALLBACK_IMAGE_PATH);

    return {
      media_id: mediaId || cleanString(lookup.media_id),
      file_name: cleanString(lookup.file_name),
      path,
      media_type: resolvedMediaType(img.media_type || lookup.media_type, path),
      original_caption: cleanString(img.caption),
      captured_date: cleanString(img.captured_date || lookup.captured_date),
      captured_time: cleanString(img.captured_time || lookup.captured_time),
      component_group: cleanString(img.component_group || lookup.component_group),
      specific_component: cleanString(img.specific_component || lookup.specific_component),
      stage: cleanString(img.stage || lookup.stage),
      observed_state: cleanString(img.observed_state || lookup.observed_state),
      confidence: cleanString(img.confidence || lookup.confidence),
      tags: cleanString(img.tags || lookup.tags),
      notes: cleanString(img.notes || lookup.notes),
      matched_tokens: Array.isArray(img.matched_tokens) ? img.matched_tokens.slice() : [],
      match_basis: cleanString(img.match_basis),
      match_score: cleanString(img.match_score),
    };
  }

  function isImageDeleted(image) {
    const base = getBasePhotoMeta(image);
    return isPhotoDeletedByKey(photoOverrideKeyForMeta(base));
  }

  function filterVisibleImages(images) {
    const source = Array.isArray(images) ? images : [];
    return source.filter((image) => !isImageDeleted(image));
  }

  function withOverride(baseMeta) {
    const mediaId = cleanString(baseMeta.media_id);
    if (!mediaId) {
      return { ...baseMeta };
    }
    const override = state.photoOverrides[mediaId];
    if (!override || typeof override !== "object") {
      return { ...baseMeta };
    }
    return {
      ...baseMeta,
      component_group: cleanString(override.component_group || baseMeta.component_group),
      specific_component: cleanString(override.specific_component || baseMeta.specific_component),
      stage: cleanString(override.stage || baseMeta.stage),
      observed_state: cleanString(override.observed_state || baseMeta.observed_state),
      confidence: cleanString(override.confidence || baseMeta.confidence),
      tags: cleanString(override.tags || baseMeta.tags),
      notes: cleanString(override.notes || baseMeta.notes),
    };
  }

  function buildImageCaption(meta, fallbackCaption) {
    const component = formatToken(meta.specific_component || "");
    const stage = formatToken(meta.stage || "");
    const date = cleanString(meta.captured_date);

    if (component && stage && date) {
      return `${component} · ${stage} · ${date}`;
    }
    if (component && stage) {
      return `${component} · ${stage}`;
    }
    if (component && date) {
      return `${component} · ${date}`;
    }
    if (component) {
      return component;
    }
    if (meta.original_caption) {
      return meta.original_caption;
    }
    if (fallbackCaption) {
      return fallbackCaption;
    }
    if (meta.file_name) {
      return meta.file_name;
    }
    return "Evidence media";
  }

  function workstreamProfile(workstreamId) {
    const profiles = (data.meta && data.meta.workstream_image_profiles) || {};
    const profile = profiles[workstreamId];
    if (!profile) {
      return null;
    }
    const stages = (profile.stages || []).map((value) => cleanString(value).toLowerCase());
    const groups = (profile.component_groups || []).map((value) => cleanString(value).toLowerCase());
    const keywords = (profile.keywords || []).map((value) => cleanString(value).toLowerCase()).filter(Boolean);
    return {
      stages: new Set(stages),
      component_groups: new Set(groups),
      keywords,
    };
  }

  function bestMatchingWorkstreamForMeta(meta) {
    const profiles = (data.meta && data.meta.workstream_image_profiles) || {};
    const stage = cleanString(meta && meta.stage).toLowerCase();
    const componentGroup = cleanString(meta && meta.component_group).toLowerCase();
    const textBlob = [
      cleanString(meta && meta.specific_component),
      cleanString(meta && meta.tags),
      cleanString(meta && meta.notes),
      cleanString(meta && meta.file_name),
      componentGroup,
      stage,
    ]
      .join(" ")
      .toLowerCase();

    let bestWorkstreamId = "";
    let bestScore = -999;

    Object.keys(profiles).forEach((workstreamId) => {
      const profile = workstreamProfile(workstreamId);
      if (!profile) {
        return;
      }

      const stageMatch = Boolean(stage && profile.stages.has(stage));
      const componentMatch = Boolean(componentGroup && profile.component_groups.has(componentGroup));
      let score = 0;

      if (stageMatch) {
        score += 8;
      } else if (stage) {
        score -= 3;
      }

      if (componentMatch) {
        score += 6;
      } else if (componentGroup) {
        score -= 2;
      }

      let keywordHits = 0;
      (profile.keywords || []).forEach((keyword) => {
        if (keyword && textBlob.includes(keyword)) {
          keywordHits += 1;
        }
      });
      score += Math.min(keywordHits, 4) * 2;

      if (stageMatch && componentMatch) {
        score += 5;
      }

      if (score > bestScore) {
        bestScore = score;
        bestWorkstreamId = workstreamId;
      }
    });

    return bestScore >= 9 ? bestWorkstreamId : "";
  }

  function imageBelongsToWorkstream(image, workstreamId) {
    const profile = workstreamProfile(workstreamId);
    if (!profile) {
      return true;
    }
    const effective = withOverride(getBasePhotoMeta(image));
    const stage = cleanString(effective.stage).toLowerCase();
    const componentGroup = cleanString(effective.component_group).toLowerCase();
    const stageMatch = profile.stages.has(stage);
    const componentMatch = profile.component_groups.has(componentGroup);
    if (stageMatch && (!componentGroup || componentMatch)) {
      return true;
    }
    if (!stage && componentMatch) {
      return true;
    }
    return false;
  }

  function buildRecategorizedImagesForWorkstream(workstreamId, existingMediaIds) {
    const results = [];
    const entries = Object.entries(state.photoOverrides || {});
    for (const [mediaId, override] of entries) {
      if (!mediaId || existingMediaIds.has(mediaId) || isDeletedPhotoOverride(override)) {
        continue;
      }
      const targetWorkstream = cleanString(override && override.target_workstream);
      if (targetWorkstream && targetWorkstream !== workstreamId) {
        continue;
      }
      const lookup = photoLookupById(mediaId);
      if (!lookup) {
        continue;
      }
      const candidate = {
        media_id: mediaId,
        file_name: cleanString(lookup.file_name),
        path: cleanString(lookup.path || FALLBACK_IMAGE_PATH),
        captured_date: cleanString(lookup.captured_date),
        captured_time: cleanString(lookup.captured_time),
        component_group: cleanString(lookup.component_group),
        specific_component: cleanString(lookup.specific_component),
        stage: cleanString(lookup.stage),
        observed_state: cleanString(lookup.observed_state),
        confidence: cleanString(lookup.confidence),
        tags: cleanString(lookup.tags),
        notes: cleanString(lookup.notes),
        matched_tokens: [],
        match_basis: "recategorized_override",
      };
      const effective = withOverride(candidate);
      if (!imageBelongsToWorkstream(effective, workstreamId)) {
        continue;
      }

      const inferredWorkstream = targetWorkstream || bestMatchingWorkstreamForMeta(effective);
      if (inferredWorkstream && inferredWorkstream !== workstreamId) {
        continue;
      }

      results.push(candidate);
      existingMediaIds.add(mediaId);
    }
    return results;
  }

  function buildWorkstreamEvidenceSets(workstream) {
    function evidenceSetPriority(set) {
      const key = cleanString(set && set.key).toLowerCase();
      const explicitOrder = {
        sent_to_painter: 10,
        returned_from_painter: 20,
        paint_progress_videos: 50,
        rear_brake_cables_lines: 45,
        may1_chassis_status: 50,
        may1_engine_cleaning: 50,
        primary: 60,
      };
      if (Object.prototype.hasOwnProperty.call(explicitOrder, key)) {
        return explicitOrder[key];
      }
      if (key.startsWith("all_")) {
        return 90;
      }
      return 70;
    }

    const inputSets = workstream.evidence_sets || [];
    const existingMediaIds = new Set();
    const normalizedSets = inputSets
      .map((set) => {
        const sourceImages = filterVisibleImages(set.images);
        const uniqueImages = dedupeImages(sourceImages);
        uniqueImages.forEach((image) => {
          const mediaId = cleanString(image && image.media_id);
          if (mediaId) {
            existingMediaIds.add(mediaId);
          }
        });
        return {
          key: set.key,
          title: set.title,
          description: set.description,
          images: uniqueImages,
        };
      })
      .filter((set) => set.images.length);

    const recategorizedImages = dedupeImages(buildRecategorizedImagesForWorkstream(workstream.id, existingMediaIds));
    if (recategorizedImages.length) {
      if (normalizedSets.length) {
        const firstSet = normalizedSets[0];
        firstSet.images = dedupeImages([...(firstSet.images || []), ...recategorizedImages]);
      } else {
        normalizedSets.push({
          key: "primary",
          title: "Primary Evidence Set",
          description: "Best-matched photos for this workstream.",
          images: recategorizedImages,
        });
      }
    }

    normalizedSets.sort((left, right) => evidenceSetPriority(left) - evidenceSetPriority(right));
    return normalizedSets;
  }

  function chooseWorkstreamLeadImage(workstream) {
    const primary = filterVisibleImages(workstream.images).find(Boolean);
    if (primary) {
      return primary;
    }
    const evidenceSets = Array.isArray(workstream.evidence_sets) ? workstream.evidence_sets : [];
    for (const set of evidenceSets) {
      const image = filterVisibleImages(set && set.images).find(Boolean);
      if (image) {
        return image;
      }
    }
    return null;
  }

  function isProcurementClassification(meta) {
    const stage = cleanString(meta && meta.stage).toLowerCase();
    const group = cleanString(meta && meta.component_group).toLowerCase();
    return stage === "procurement_reconciliation" || group === "procurement_inventory";
  }

  function buildProcurementEvidenceImages(baseImages) {
    const source = filterVisibleImages(baseImages);
    const existingMediaIds = new Set();
    const normalized = [];

    source.forEach((image) => {
      const base = getBasePhotoMeta(image);
      const effective = withOverride(base);
      if (!isProcurementClassification(effective)) {
        return;
      }
      if (effective.media_id) {
        existingMediaIds.add(effective.media_id);
      }
      normalized.push({ ...image });
    });

    Object.entries(state.photoOverrides || {}).forEach(([mediaId, override]) => {
      if (!mediaId || existingMediaIds.has(mediaId) || isDeletedPhotoOverride(override)) {
        return;
      }
      const lookup = photoLookupById(mediaId);
      if (!lookup) {
        return;
      }
      const candidate = {
        media_id: mediaId,
        file_name: cleanString(lookup.file_name),
        path: cleanString(lookup.path || FALLBACK_IMAGE_PATH),
        captured_date: cleanString(lookup.captured_date),
        captured_time: cleanString(lookup.captured_time),
        component_group: cleanString(lookup.component_group),
        specific_component: cleanString(lookup.specific_component),
        stage: cleanString(lookup.stage),
        observed_state: cleanString(lookup.observed_state),
        confidence: cleanString(lookup.confidence),
        tags: cleanString(lookup.tags),
        notes: cleanString(lookup.notes),
        matched_tokens: [],
        match_basis: "recategorized_override",
      };
      if (!isProcurementClassification(withOverride(candidate))) {
        return;
      }
      existingMediaIds.add(mediaId);
      normalized.unshift(candidate);
    });

    return normalized;
  }

  function resetImageRegistry() {
    imageRegistry.clear();
    imageKeyCounter = 0;
  }

  function resetItemRegistry() {
    itemRegistry.clear();
    itemKeyCounter = 0;
  }

  function registerImage(baseMeta) {
    imageKeyCounter += 1;
    const imageKey = `img_${imageKeyCounter}`;
    imageRegistry.set(imageKey, baseMeta);
    return imageKey;
  }

  function registerItem(row) {
    itemKeyCounter += 1;
    const itemKey = `item_${itemKeyCounter}`;
    itemRegistry.set(itemKey, row);
    return itemKey;
  }

  function renderItemButton(row) {
    const itemKey = registerItem(row);
    return `
      <button type="button" class="item-detail-btn" data-item-key="${escapeHtml(itemKey)}">
        ${escapeHtml(row.item || "-")}
      </button>
    `;
  }

  function prepareImage(image, fallbackCaption) {
    const base = getBasePhotoMeta(image);
    const effective = withOverride(base);
    const imageKey = registerImage(base);
    const mediaId = cleanString(base.media_id);
    return {
      key: imageKey,
      path: cleanString(effective.path || FALLBACK_IMAGE_PATH),
      caption: buildImageCaption(effective, fallbackCaption),
      overrideActive: Boolean(mediaId && state.photoOverrides[mediaId]),
      mediaType: resolvedMediaType(effective.media_type, effective.path),
      effective,
    };
  }

  function renderImageButton(prepared, buttonClass, imageClass) {
    return `
      <button type="button" class="${buttonClass}" data-image-key="${escapeHtml(prepared.key)}" title="Open full-size media">
        <img loading="eager" decoding="async" class="${imageClass}" src="${escapeHtml(prepared.path)}" alt="${escapeHtml(prepared.caption)}">
      </button>
    `;
  }

  function renderVideoButton(prepared, buttonClass, videoClass) {
    return `
      <button type="button" class="${buttonClass} video-open-btn" data-image-key="${escapeHtml(prepared.key)}" data-video-preview="1" title="Open video" aria-label="Open video: ${escapeHtml(prepared.caption)}">
        <video class="${videoClass} video-preview" muted loop preload="metadata" playsinline src="${escapeHtml(prepared.path)}"></video>
        <span class="video-preview-icon" aria-hidden="true"></span>
        <span class="video-preview-badge" aria-hidden="true">Video</span>
      </button>
    `;
  }

  function renderPreparedMedia(prepared, buttonClass, mediaClass) {
    if (prepared.mediaType === "video") {
      return renderVideoButton(prepared, buttonClass, mediaClass);
    }
    return renderImageButton(prepared, buttonClass, mediaClass);
  }

  function handleVideoPreviewEvent(event, shouldPlay) {
    const trigger = event.target.closest("[data-video-preview]");
    if (!trigger || trigger.contains(event.relatedTarget)) {
      return;
    }
    const video = trigger.querySelector("video");
    if (!video) {
      return;
    }
    if (shouldPlay) {
      video.muted = true;
      video.play().catch(() => {});
      return;
    }
    video.pause();
  }

  function renderFigureImage(image, fallbackCaption, options = {}) {
    const prepared = prepareImage(image, fallbackCaption);
    const showCaption = options.showCaption !== false;
    const figureClass = options.figureClass || "evidence-figure";
    const buttonClass = options.buttonClass || "image-open-btn";
    const imageClass = options.imageClass || "figure-image";
    const captionClass = options.captionClass || "small-muted";
    return `
      <figure class="${figureClass}">
        ${renderPreparedMedia(prepared, buttonClass, imageClass)}
        ${
          showCaption
            ? `<figcaption class="${captionClass}">${escapeHtml(prepared.caption)}</figcaption>`
            : ""
        }
      </figure>
    `;
  }

  function inventoryImageMatchLabel(matchBasis) {
    const basis = cleanString(matchBasis);
    const labels = {
      exact_order_evidence: "Order evidence",
      local_inventory_evidence: "Local photo",
      manual_override: "Pinned image",
      manual_image_disputed: "Image disputed",
      previous_part_photo: "Previous part",
      selling_site_match: "Listing image",
      inventory_match: "Matched photo",
      whatsapp_evidence_match: "WhatsApp",
      workstream_fallback: "Workstream fallback",
      inventory_fallback: "Fallback",
      placeholder: "Image required",
    };
    return labels[basis] || formatToken(basis);
  }

  function renderInventoryImageCell(row, fallbackCaption) {
    const sourceImage = row && row.image && !isImageDeleted(row.image) ? row.image : {};
    const prepared = prepareImage(sourceImage, fallbackCaption);
    const label = inventoryImageMatchLabel(prepared.effective.match_basis);
    const mediaClass = cleanString(prepared.path).toLowerCase().endsWith(".svg")
      ? "table-image table-image-contain"
      : "table-image";
    return `
      <td class="table-image-cell">
        ${renderPreparedMedia(prepared, "table-image-btn", mediaClass)}
        ${label ? `<span class="table-image-note">${escapeHtml(label)}</span>` : ""}
      </td>
    `;
  }

  function renderRequirementEvidenceImages(requirement) {
    const images = filterVisibleImages(requirement.evidence_images);
    if (!images.length) {
      return `<span class="small-muted">${escapeHtml(formatToken(requirement.photo_status || "photo_needed"))}</span>`;
    }
    const fallbackCaption = requirement.requirement_name || requirement.pipe_or_line || requirement.part_name || "Requirement evidence";
    return `
      <div class="requirement-evidence-grid">
        ${images
          .slice(0, 4)
          .map((image) => {
            const prepared = prepareImage(image, fallbackCaption);
            return `
              <div class="requirement-evidence-item">
                ${renderPreparedMedia(prepared, "table-image-btn", "table-image")}
                <span class="table-image-note">${escapeHtml(prepared.effective.media_id || "")}</span>
              </div>
            `;
          })
          .join("")}
      </div>
      ${images.length > 4 ? `<span class="table-image-note">+${escapeHtml(images.length - 4)} more</span>` : ""}
    `;
  }

  function renderRequirementTable(requirements, options = {}) {
    const rows = Array.isArray(requirements) ? requirements : [];
    if (!rows.length) {
      return "";
    }
    const properlySpecced = rows.filter((row) => isSpecReadyStatus(row.spec_status)).length;
    const acquired = rows.filter((row) => cleanString(row.acquisition_status) === "acquired").length;
    const installed = rows.filter((row) => cleanString(row.installation_status) === "installed").length;
    const title = options.title || "Requirements";
    const summary = options.summary || "Exact make/buy/fabrication requirements with status gates for specification, acquisition, and installation.";
    return `
      <article class="card pipe-requirements-card">
        <div class="detail-header">
          <h3>${escapeHtml(title)}</h3>
          <div class="chip-row">
            ${chip(`${properlySpecced}/${rows.length} Spec'd`)}
            ${chip(`${acquired}/${rows.length} Acquired`)}
            ${chip(`${installed}/${rows.length} Installed`)}
          </div>
        </div>
        <p class="small-muted">${escapeHtml(summary)}</p>
        <div class="table-wrap requirement-table-wrap">
          <table class="requirement-table">
            <thead>
              <tr>
                <th>Evidence</th>
                <th>Requirement</th>
                <th>Status Gates</th>
                <th>Make / Buy Spec</th>
                <th>Measurements Required</th>
                <th>Install Gate</th>
              </tr>
            </thead>
            <tbody>
              ${rows
                .map((row) => {
                  const requirementId = row.requirement_id || row.pipe_id || row.part_id || "";
                  const requirementName = row.requirement_name || row.pipe_or_line || row.part_name || "";
                  const quantity = cleanString(row.quantity || row.qty);
                  return `
                    <tr>
                      <td class="requirement-evidence-cell">${renderRequirementEvidenceImages(row)}</td>
                      <td>
                        <strong>${escapeHtml(requirementId)} · ${escapeHtml(requirementName)}</strong>
                        <div class="small-muted">${escapeHtml(row.vehicle_location || "")}</div>
                        ${quantity ? `<div class="small-muted">Qty: ${escapeHtml(quantity)}</div>` : ""}
                        <div class="small-muted">Scope: ${escapeHtml(formatToken(row.replace_scope || ""))}</div>
                        ${row.current_action ? `<div class="requirement-action"><strong>Now:</strong> ${escapeHtml(row.current_action)}</div>` : ""}
                      </td>
                      <td>
                        <div class="status-stack">
                          ${statusChip(row.spec_status || "needs_measurement")}
                          ${statusChip(row.acquisition_status || "not_acquired")}
                          ${statusChip(row.installation_status || "not_installed")}
                        </div>
                      </td>
                      <td>
                        ${escapeHtml(row.exact_recreation_spec || "")}
                        ${row.material_spec ? `<div class="small-muted requirement-material">${escapeHtml(row.material_spec)}</div>` : ""}
                      </td>
                      <td>${escapeHtml(row.critical_measurements || "")}</td>
                      <td>
                        ${escapeHtml(row.fit_and_test || "")}
                        ${row.notes ? `<div class="small-muted requirement-material">${escapeHtml(row.notes)}</div>` : ""}
                      </td>
                    </tr>
                  `;
                })
                .join("")}
            </tbody>
          </table>
        </div>
      </article>
    `;
  }

  const CHASSIS_RUBBER_SPEC_ROWS = [
    {
      id: "BM-LG",
      part: "Large circular body-mount cushion",
      qty: "2",
      image: "../../photos/20260502_004231_gp_CfosvPIg.jpg",
      imageCaption: "Large circular body-mount cushion",
      spec: "Origin lower-left of 78 x 78 top profile; centre X39 Y39; OD 78; height 24; through bore 32; face A register/recess 46 x 2; face B flat; outside load edge R2-R3; faces parallel <=0.5; concentricity <=1.0.",
      route: "rubber lathe/CNC mill/mould; DXF is top profile",
      files: [
        ["DXF", "../../data/manual/fabrication/rubber_recreation_rev_a/bm_lg_body_mount_cushion_rev_a.dxf"],
        ["SVG", "../../data/manual/fabrication/rubber_recreation_rev_a/bm_lg_body_mount_cushion_rev_a.svg"],
      ],
      notes: "Make matched pair from one setup.",
    },
    {
      id: "BM-SM",
      part: "Small circular body-mount cushion",
      qty: "10",
      image: "../../photos/20260502_004437_gp_f1TySzww.jpg",
      imageCaption: "Small circular body-mount cushion",
      spec: "Origin lower-left of 64 x 64 top profile; centre X32 Y32; OD 64; height 22; through bore 32; face A register/recess 46 x 2; face B flat; outside load edge R2-R3; faces parallel <=0.5; concentricity <=1.0.",
      route: "rubber lathe/CNC mill/mould; DXF is top profile",
      files: [
        ["DXF", "../../data/manual/fabrication/rubber_recreation_rev_a/bm_sm_body_mount_cushion_rev_a.dxf"],
        ["SVG", "../../data/manual/fabrication/rubber_recreation_rev_a/bm_sm_body_mount_cushion_rev_a.svg"],
      ],
      notes: "One-piece definition unless old sample proves split stack.",
    },
    {
      id: "FS-OVAL",
      part: "Front-support two-hole oval pad",
      qty: "2",
      image: "../../photos/20260502_004345_gp_yK8VYzMQ.jpg",
      imageCaption: "Front-support two-hole oval pad",
      spec: "Origin lower-left of 64 x 96 plan; outer capsule 64 wide x 96 long with R32 ends; thickness 15; through holes 12 at X32 Y16 and X32 Y80; relief pocket 36 x 18 R3 at X14 Y39; insert/boss mark 29 at X32 Y16.",
      route: "waterjet/knife/punch/moulded 2.5D rubber pad",
      files: [
        ["DXF", "../../data/manual/fabrication/rubber_recreation_rev_a/fs_oval_front_support_pad_rev_a.dxf"],
        ["SVG", "../../data/manual/fabrication/rubber_recreation_rev_a/fs_oval_front_support_pad_rev_a.svg"],
      ],
      notes: "INSERT_MARK is not a through cut. Confirm blind pocket vs through relief.",
    },
    {
      id: "FS-STRIP-L",
      part: "Front-support left strip / liner",
      qty: "1",
      image: "../../photos/20260502_004201_gp_zfUSmKJg.jpg",
      imageCaption: "Front-support left strip / liner",
      spec: "Stock envelope 165 x 40 with R4 ends; base thickness 8; raised/load pad height 14; provisional slots 16 x 11 at centres X20 Y20 and X145 Y20 only if carrier confirms.",
      route: "template trace, then waterjet/knife/punch; supplied DXF is stock blank only",
      files: [
        ["DXF", "../../data/manual/fabrication/rubber_recreation_rev_a/fs_strip_left_template_blank_rev_a.dxf"],
        ["SVG", "../../data/manual/fabrication/rubber_recreation_rev_a/fs_strip_left_template_blank_rev_a.svg"],
      ],
      notes: "Final CNC cut requires physical left carrier trace.",
    },
    {
      id: "FS-STRIP-R",
      part: "Front-support right strip / liner",
      qty: "1",
      image: "../../photos/20260502_004222_gp_PKRe5HSQ.jpg",
      imageCaption: "Front-support right strip / liner",
      spec: "Stock envelope 165 x 40 with R4 ends; base thickness 8; raised/load pad height 14; provisional slots 16 x 11 at centres X20 Y20 and X145 Y20 only if carrier confirms.",
      route: "template trace, then waterjet/knife/punch; supplied DXF is stock blank only",
      files: [
        ["DXF", "../../data/manual/fabrication/rubber_recreation_rev_a/fs_strip_right_template_blank_rev_a.dxf"],
        ["SVG", "../../data/manual/fabrication/rubber_recreation_rev_a/fs_strip_right_template_blank_rev_a.svg"],
      ],
      notes: "Final CNC cut requires physical right carrier trace.",
    },
    {
      id: "EXH-HGR-90917",
      part: "Exhaust pipe teardrop cushion",
      qty: "As fitted",
      image: "../../data/manual/fabrication/rubber_recreation_rev_a/exh_hgr_90917_08004_teardrop_rev_a.svg",
      imageCaption: "Toyota 90917-08004 style exhaust cushion CAD",
      spec: "Origin lower-left of 48 x 86 top profile; centreline X24; teardrop/paddle outline 48 wide x 86 high; lower bulb R24 centred X24 Y24; mounting hole 9 at X24 Y73; hanger slot 16 x 22 capsule centred X24 Y29; raised boss/recess mark 36 x 42 at X6 Y8; rubber body thickness target 22 unless genuine sample proves otherwise.",
      route: "buy Toyota 90917-08004 / 17572-92000 or mould sample-matched teardrop exhaust cushion",
      files: [
        ["DXF", "../../data/manual/fabrication/rubber_recreation_rev_a/exh_hgr_90917_08004_teardrop_rev_a.dxf"],
        ["SVG", "../../data/manual/fabrication/rubber_recreation_rev_a/exh_hgr_90917_08004_teardrop_rev_a.svg"],
      ],
      notes: "Do not use the previous round ring or generic two-hole strap. Local molding needs a genuine sample or intact original for side profile and metal insert.",
    },
    {
      id: "BUMP-F-L",
      part: "Front left spring bump stop",
      qty: "1",
      image: "../../deliverables/selling_site_images/images/reference_catalog/bump_stop.jpg",
      imageCaption: "Bump stop shape reference",
      spec: "Not a CNC part. Buy Toyota/manufacturer-style 48304-60010 direct replacement. Local reproduction requires physical sample or 3D scan and a mould matching base footprint, bolt pattern/thread, free height, compressed height, progressive profile, and contact face.",
      route: "buy manufacturer molded part preferred",
      files: [],
      notes: "Verify left-front bracket and axle contact point.",
    },
    {
      id: "BUMP-F-R",
      part: "Front right spring bump stop",
      qty: "1",
      image: "../../deliverables/selling_site_images/images/reference_catalog/bump_stop.jpg",
      imageCaption: "Bump stop shape reference",
      spec: "Not a CNC part. Buy Toyota/manufacturer-style 48304-60020 direct replacement. This is the separate shorter/right-side front stop. Local reproduction requires physical sample or 3D scan and a mould.",
      route: "buy manufacturer molded part preferred",
      files: [],
      notes: "Do not install left stop or universal stop here.",
    },
    {
      id: "BUMP-R",
      part: "Rear spring bump stops",
      qty: "2",
      image: "../../deliverables/selling_site_images/images/reference_catalog/bump_stop.jpg",
      imageCaption: "Bump stop shape reference",
      spec: "Not a CNC part. Buy Toyota/manufacturer-style 48304-60010 direct replacement for rear pair. Local reproduction requires physical sample or 3D scan and a mould matching rear bracket/base, bolt pattern/thread, height, progressive profile, and contact face.",
      route: "buy manufacturer molded part preferred",
      files: [],
      notes: "Replace as matched rear pair after suspension ride height is known.",
    },
  ];

  const CHASSIS_RUBBER_REFERENCE_IMAGES = [
    ["../../photos/20260502_004413_gp_Qno8OVRg.jpg", "Circular cushion top reference"],
    ["../../photos/20260502_004442_gp_7WcFHjLQ.jpg", "Circular annular cushion reference 2"],
    ["../../photos/20260502_004254_gp_Hm9RR5DQ.jpg", "Long strip height reference"],
    ["../../photos/20260502_004314_gp_wuzpgNrA.jpg", "Long strip side reference"],
    ["../../photos/20260501_193755_gp_cuaY6sgg.jpg", "Rear exhaust and bracket context"],
    ["../../photos/20260501_193805_gp_VgTc8wYQ.jpg", "Exhaust bracket close reference"],
    ["../../photos/20260501_193811_gp_uv8kwbxw.jpg", "Tailpipe bracket and holder location reference"],
    ["../../photos/20260405_234652.jpg", "Original tub-side body-mount context"],
    ["../../photos/20260405_234546.jpg", "Original underbody mount context"],
  ];

  function renderChassisRubberSpecImage(row) {
    const image = {
      path: row.image,
      caption: row.imageCaption || row.part,
      media_id: row.id,
      media_type: "photo",
    };
    const prepared = prepareImage(image, row.imageCaption || row.part);
    return `
      <td class="table-image-cell">
        ${renderPreparedMedia(prepared, "table-image-btn", "table-image")}
        <span class="table-image-note">${escapeHtml(row.imageCaption || "")}</span>
      </td>
    `;
  }

  function renderChassisRubberCadRoute(row) {
    const links = Array.isArray(row.files)
      ? row.files
          .map(([label, href]) => `<a href="${escapeHtml(href)}">${escapeHtml(label)}</a>`)
          .join(" ")
      : "";
    return `
      <div>${escapeHtml(row.route || "")}</div>
      ${links ? `<div class="small-muted chassis-rubber-file-links">${links}</div>` : ""}
    `;
  }

  function renderChassisRubberSimpleSpec() {
    return `
      <article class="card pipe-requirements-card">
        <div class="detail-header">
          <h3>Rubber Spec</h3>
          <div class="chip-row">
            ${chip("All dimensions mm")}
            ${chip("Shore A 60 +/-5")}
          </div>
        </div>
        <p class="small-muted">Body/front-support rubbers: new black solid EPDM or NR/SBR automotive mount rubber, Shore A 60 +/-5. Exhaust holder: Toyota 90917-08004 / 17572-92000 teardrop exhaust cushion style or sample-matched molded copy. Bump stops: OEM/manufacturer-style molded stops where available; fabricate only by exact sample and bracket match. Reject tyre rubber, crumb rubber, sponge, mixed offcuts, salvage rubber, unmarked compound, or universal bump stops that do not match the axle contact point.</p>
        <p class="small-muted">Machine package: <a href="../../data/manual/fabrication/rubber_recreation_rev_a/machine_definitions.csv">machine_definitions.csv</a>, <a href="../../data/manual/fabrication/rubber_recreation_rev_a/machine_definitions.json">machine_definitions.json</a>, <a href="../../data/manual/fabrication/rubber_recreation_rev_a/j40_rubber_recreation_rev_a_dimension_sheet.pdf">dimension sheet PDF</a>.</p>
        <div class="table-wrap requirement-table-wrap">
          <table class="requirement-table chassis-rubber-spec-table">
            <thead>
              <tr>
                <th>Image</th>
                <th>ID</th>
                <th>Part</th>
                <th>Qty</th>
                <th>Machine / Purchase Definition</th>
                <th>CAD / Route</th>
                <th>Notes</th>
              </tr>
            </thead>
            <tbody>
              ${CHASSIS_RUBBER_SPEC_ROWS
                .map(
                  (row) => `
                    <tr>
                      ${renderChassisRubberSpecImage(row)}
                      <td><strong>${escapeHtml(row.id)}</strong></td>
                      <td>${escapeHtml(row.part)}</td>
                      <td>${escapeHtml(row.qty)}</td>
                      <td>${escapeHtml(row.spec)}</td>
                      <td>${renderChassisRubberCadRoute(row)}</td>
                      <td>${escapeHtml(row.notes)}</td>
                    </tr>
                  `
                )
                .join("")}
            </tbody>
          </table>
        </div>
        <p class="small-muted">Tolerances: circular cushion OD/ID +/-1.0, height +/-0.5, bore/register concentricity <=1.0; FS-OVAL outside +/-1.0, hole position +/-0.5, thickness +/-0.5; strip outline +/-1.0, holes +/-0.5, thickness +/-0.5. Bump stops are not simple cut rubber; OEM/manufacturer part or exact molded sample controls.</p>
        <p class="small-muted">Lower holds: BM-SM split-stack check if the old sample separates; FS-STRIP-L/R require physical carrier trace before final CNC cut; EXH-HGR-90917 should be bought as Toyota 90917-08004 / 17572-92000 where available, or molded only after a genuine sample confirms side profile, insert depth, and exact thickness; bump stops need bracket/contact verification before purchase.</p>
      </article>
    `;
  }

  function renderChassisRubberReferenceImages() {
    return `
      <article class="card pipe-requirements-card">
        <div class="detail-header">
          <h3>Extra Context Images</h3>
          <div class="chip-row">${chip(`${CHASSIS_RUBBER_REFERENCE_IMAGES.length} Images`)}</div>
        </div>
        <div class="requirement-evidence-grid">
          ${CHASSIS_RUBBER_REFERENCE_IMAGES
            .map(([path, caption]) => {
              const image = {
                path,
                caption,
                media_id: path.split("/").pop().replace(/\.[^.]+$/, ""),
                media_type: "photo",
              };
              const prepared = prepareImage(image, caption);
              return `
                <div class="requirement-evidence-item">
                  ${renderPreparedMedia(prepared, "table-image-btn", "table-image")}
                  <span class="table-image-note">${escapeHtml(caption)}</span>
                </div>
              `;
            })
            .join("")}
        </div>
      </article>
    `;
  }

  function renderBodyMountOrderReleaseTable(rows) {
    const source = Array.isArray(rows) ? rows : [];
    if (!source.length) {
      return "";
    }
    const specReady = source.filter((row) => isSpecReadyStatus(row.spec_status || row.order_release_state)).length;
    return `
      <article class="card pipe-requirements-card">
        <div class="detail-header">
          <h3>Body Mount Order Release</h3>
          <div class="chip-row">
            ${chip(`${specReady}/${source.length} Spec Ready`)}
            ${chip(`${source.length} Order Lines`)}
          </div>
        </div>
        <p class="small-muted">Exact order lines, quantities, route controls, and release holds for body-mount rubbers, stops/seats, sleeves, cups, shims, bolts, engine mounts, and gearbox mount.</p>
        <div class="table-wrap requirement-table-wrap">
          <table class="requirement-table body-mount-order-table">
            <thead>
              <tr>
                <th>Line</th>
                <th>Qty</th>
                <th>Status</th>
                <th>Exact Spec</th>
                <th>Release Action</th>
              </tr>
            </thead>
            <tbody>
              ${source
                .map((row) => `
                  <tr>
                    <td>
                      <strong>${escapeHtml(row.order_line_id || "")} · ${escapeHtml(row.item || "")}</strong>
                      <div class="small-muted">${escapeHtml(row.part_number_or_code || "")}</div>
                      <div class="small-muted">${escapeHtml(formatToken(row.route || ""))}</div>
                    </td>
                    <td>
                      <div>Required: ${escapeHtml(row.qty_required || "-")}</div>
                      <div class="small-muted">Order: ${escapeHtml(row.qty_to_order || "-")}</div>
                    </td>
                    <td>
                      <div class="status-stack">
                        ${statusChip(row.spec_status || "spec_ready")}
                        ${statusChip(row.order_release_state || "spec_ready")}
                      </div>
                    </td>
                    <td>
                      ${escapeHtml(row.exact_order_spec || "")}
                      ${row.material_spec ? `<div class="small-muted requirement-material">${escapeHtml(row.material_spec)}</div>` : ""}
                      ${row.source_basis ? `<div class="small-muted requirement-material">Source: ${escapeHtml(row.source_basis)}</div>` : ""}
                    </td>
                    <td>
                      ${escapeHtml(row.user_action_required || "")}
                      ${row.do_not_order_if ? `<div class="requirement-action"><strong>Do not order if:</strong> ${escapeHtml(row.do_not_order_if)}</div>` : ""}
                      ${row.notes ? `<div class="small-muted requirement-material">${escapeHtml(row.notes)}</div>` : ""}
                    </td>
                  </tr>
                `)
                .join("")}
            </tbody>
          </table>
        </div>
      </article>
    `;
  }

  function renderBodyMountReleaseActions(rows) {
    const source = Array.isArray(rows) ? rows : [];
    if (!source.length) {
      return "";
    }
    const open = source.filter((row) => cleanString(row.status).toLowerCase() !== "closed").length;
    return `
      <article class="card pipe-requirements-card">
        <div class="detail-header">
          <h3>Body Mount Release Actions</h3>
          <div class="chip-row">
            ${chip(`${open}/${source.length} Open`)}
          </div>
        </div>
        <p class="small-muted">These are the remaining physical checks before held body-mount order lines move from spec-ready to released.</p>
        <div class="table-wrap requirement-table-wrap">
          <table class="requirement-table body-mount-actions-table">
            <thead>
              <tr>
                <th>Action</th>
                <th>Status</th>
                <th>Blocks</th>
                <th>Record In</th>
                <th>Reason</th>
              </tr>
            </thead>
            <tbody>
              ${source
                .map((row) => `
                  <tr>
                    <td>
                      <strong>${escapeHtml(row.action_id || "")}</strong>
                      <div>${escapeHtml(row.action || "")}</div>
                      <div class="small-muted">${escapeHtml(formatToken(row.priority || ""))} · ${escapeHtml(formatToken(row.owner || ""))}</div>
                    </td>
                    <td>${statusChip(row.status || "open")}</td>
                    <td>${escapeHtml(row.blocks_order_lines || "")}</td>
                    <td>${escapeHtml(row.record_result_in || "")}</td>
                    <td>${escapeHtml(row.why_it_matters || "")}</td>
                  </tr>
                `)
                .join("")}
            </tbody>
          </table>
        </div>
      </article>
    `;
  }

  function renderBodyMountStationClosure(rows) {
    const source = Array.isArray(rows) ? rows : [];
    if (!source.length) {
      return "";
    }
    const released = source.filter((row) => cleanString(row.release_status).toLowerCase() === "released").length;
    return `
      <article class="card pipe-requirements-card">
        <div class="detail-header">
          <h3>Body Mount Station Closure</h3>
          <div class="chip-row">
            ${chip(`${released}/${source.length} Released`)}
            ${chip(`${source.length} Stations`)}
          </div>
        </div>
        <p class="small-muted">Station-by-station measurement sheet for final rubber, sleeve, shim, and bolt release.</p>
        <div class="table-wrap requirement-table-wrap">
          <table class="requirement-table body-mount-station-table">
            <thead>
              <tr>
                <th>Station</th>
                <th>Expected Parts</th>
                <th>Measurements</th>
                <th>Bolt</th>
                <th>Status / Action</th>
              </tr>
            </thead>
            <tbody>
              ${source
                .map((row) => `
                  <tr>
                    <td>
                      <strong>${escapeHtml(row.station_id || "")}</strong>
                      <div class="small-muted">${escapeHtml(formatToken(row.vehicle_position || ""))}</div>
                      <div class="small-muted">${escapeHtml(row.candidate_toyota_station || "")}</div>
                    </td>
                    <td>
                      <div>${escapeHtml(row.expected_rubber_family || "")}</div>
                      <div class="small-muted">${escapeHtml(row.expected_rubber_qty_at_position || "")}</div>
                      <div class="small-muted">Old parts: ${escapeHtml(row.old_parts_present || "")}</div>
                    </td>
                    <td>
                      <div>Shim: ${escapeHtml(row.shim_or_spacer_thickness_mm || "-")}</div>
                      <div class="small-muted">Sleeve ID/OD/L: ${escapeHtml(row.sleeve_id_mm || "-")} / ${escapeHtml(row.sleeve_od_mm || "-")} / ${escapeHtml(row.sleeve_length_mm || "-")}</div>
                    </td>
                    <td>
                      <div>Pitch: ${escapeHtml(row.bolt_pitch || "-")}</div>
                      <div class="small-muted">Old/final length: ${escapeHtml(row.bolt_under_head_length_mm || "-")} / ${escapeHtml(row.final_bolt_length_mm || "-")}</div>
                      <div class="small-muted">Nut depth: ${escapeHtml(row.captive_nut_depth_mm || "-")}</div>
                    </td>
                    <td>
                      ${statusChip(row.release_status || "open")}
                      <div class="small-muted">${escapeHtml(row.action_required || "")}</div>
                      ${row.notes ? `<div class="small-muted requirement-material">${escapeHtml(row.notes)}</div>` : ""}
                    </td>
                  </tr>
                `)
                .join("")}
            </tbody>
          </table>
        </div>
      </article>
    `;
  }

  function renderReplacementPipeOrderReleaseTable(rows) {
    const source = Array.isArray(rows) ? rows : [];
    if (!source.length) {
      return "";
    }
    const specReady = source.filter((row) => isSpecReadyStatus(row.spec_status || row.order_release_state)).length;
    return `
      <article class="card pipe-requirements-card">
        <div class="detail-header">
          <h3>Replacement Pipe Order Release</h3>
          <div class="chip-row">
            ${chip(`${specReady}/${source.length} Spec Ready`)}
            ${chip(`${source.length} Order Lines`)}
          </div>
        </div>
        <p class="small-muted">Exact order and fabrication lines for coolant, fuel, vacuum, breather, brake, clutch, and support-clip pipe work.</p>
        <div class="table-wrap requirement-table-wrap">
          <table class="requirement-table replacement-pipe-order-table">
            <thead>
              <tr>
                <th>Line</th>
                <th>Qty</th>
                <th>Status</th>
                <th>Spec / Dimensions</th>
                <th>Release Action</th>
              </tr>
            </thead>
            <tbody>
              ${source
                .map((row) => `
                  <tr>
                    <td>
                      <strong>${escapeHtml(row.order_line_id || "")} · ${escapeHtml(row.item || "")}</strong>
                      ${row.part_number_or_code ? `<div class="small-muted">Reference: ${escapeHtml(row.part_number_or_code || "")}</div>` : ""}
                      <div class="small-muted">${escapeHtml(formatToken(row.route || ""))}</div>
                    </td>
                    <td>
                      <div>Required: ${escapeHtml(row.qty_required || "-")}</div>
                      <div class="small-muted">Order: ${escapeHtml(row.qty_to_order || "-")}</div>
                    </td>
                    <td>
                      <div class="status-stack">
                        ${statusChip(row.spec_status || "spec_ready")}
                        ${statusChip(row.order_release_state || "spec_ready")}
                      </div>
                    </td>
                    <td>
                      ${row.dimension_spec_mm ? `<div><strong>Dimensions:</strong> ${escapeHtml(row.dimension_spec_mm)}</div>` : ""}
                      ${escapeHtml(row.exact_order_spec || "")}
                      ${row.material_spec ? `<div class="small-muted requirement-material">${escapeHtml(row.material_spec)}</div>` : ""}
                      ${row.source_basis ? `<div class="small-muted requirement-material">Source: ${escapeHtml(row.source_basis)}</div>` : ""}
                    </td>
                    <td>
                      ${escapeHtml(row.user_action_required || "")}
                      ${row.do_not_order_if ? `<div class="requirement-action"><strong>Do not order if:</strong> ${escapeHtml(row.do_not_order_if)}</div>` : ""}
                      ${row.notes ? `<div class="small-muted requirement-material">${escapeHtml(row.notes)}</div>` : ""}
                    </td>
                  </tr>
                `)
                .join("")}
            </tbody>
          </table>
        </div>
      </article>
    `;
  }

  function renderReplacementPipeReleaseActions(rows) {
    const source = Array.isArray(rows) ? rows : [];
    if (!source.length) {
      return "";
    }
    const open = source.filter((row) => cleanString(row.status).toLowerCase() !== "closed").length;
    return `
      <article class="card pipe-requirements-card">
        <div class="detail-header">
          <h3>Replacement Pipe Release Actions</h3>
          <div class="chip-row">
            ${chip(`${open}/${source.length} Open`)}
          </div>
        </div>
        <p class="small-muted">Physical checks that must close before held pipe, hose, hydraulic, and fabricated-line orders are released.</p>
        <div class="table-wrap requirement-table-wrap">
          <table class="requirement-table replacement-pipe-actions-table">
            <thead>
              <tr>
                <th>Action</th>
                <th>Status</th>
                <th>Blocks</th>
                <th>Record In</th>
                <th>Reason</th>
              </tr>
            </thead>
            <tbody>
              ${source
                .map((row) => `
                  <tr>
                    <td>
                      <strong>${escapeHtml(row.action_id || "")}</strong>
                      <div>${escapeHtml(row.action || "")}</div>
                      <div class="small-muted">${escapeHtml(formatToken(row.priority || ""))} · ${escapeHtml(formatToken(row.owner || ""))}</div>
                    </td>
                    <td>${statusChip(row.status || "open")}</td>
                    <td>${escapeHtml(row.blocks_order_lines || "")}</td>
                    <td>${escapeHtml(row.record_result_in || "")}</td>
                    <td>${escapeHtml(row.why_it_matters || "")}</td>
                  </tr>
                `)
                .join("")}
            </tbody>
          </table>
        </div>
      </article>
    `;
  }

  function renderReplacementPipeCircuitClosure(rows) {
    const source = Array.isArray(rows) ? rows : [];
    if (!source.length) {
      return "";
    }
    const released = source.filter((row) => cleanString(row.release_status).toLowerCase() === "released").length;
    return `
      <article class="card pipe-requirements-card">
        <div class="detail-header">
          <h3>Replacement Pipe Circuit Closure</h3>
          <div class="chip-row">
            ${chip(`${released}/${source.length} Released`)}
            ${chip(`${source.length} Circuits`)}
          </div>
        </div>
        <p class="small-muted">Circuit-by-circuit closure sheet for final hose IDs, tube dimensions, threads/flares, templates, supports, and release status.</p>
        <div class="table-wrap requirement-table-wrap">
          <table class="requirement-table replacement-pipe-circuit-table">
            <thead>
              <tr>
                <th>Circuit</th>
                <th>Order Lines</th>
                <th>Ends / Length</th>
                <th>Tube / Fitting Detail</th>
                <th>Status / Action</th>
              </tr>
            </thead>
            <tbody>
              ${source
                .map((row) => `
                  <tr>
                    <td>
                      <strong>${escapeHtml(row.circuit_id || "")} · ${escapeHtml(row.pipe_or_line || "")}</strong>
                      <div class="small-muted">${escapeHtml(row.vehicle_location || "")}</div>
                      <div class="small-muted">${escapeHtml(formatToken(row.photo_status || ""))}</div>
                    </td>
                    <td>${escapeHtml(row.order_lines || "")}</td>
                    <td>
                      <div>A: ${escapeHtml(row.barb_or_fitting_a || "-")}</div>
                      <div class="small-muted">B: ${escapeHtml(row.barb_or_fitting_b || "-")}</div>
                      <div class="small-muted">Length: ${escapeHtml(row.route_length_mm || "-")}</div>
                    </td>
                    <td>
                      <div>${escapeHtml(row.tube_or_hose_od_id || "")}</div>
                      <div class="small-muted">Thread/flare: ${escapeHtml(row.thread_or_flare || "-")}</div>
                      <div class="small-muted">Template: ${escapeHtml(row.bend_template_status || "-")}</div>
                      <div class="small-muted">Support: ${escapeHtml(row.clip_support_status || "-")}</div>
                    </td>
                    <td>
                      ${statusChip(row.release_status || "open")}
                      <div class="small-muted">${escapeHtml(row.action_required || "")}</div>
                      ${row.notes ? `<div class="small-muted requirement-material">${escapeHtml(row.notes)}</div>` : ""}
                    </td>
                  </tr>
                `)
                .join("")}
            </tbody>
          </table>
        </div>
      </article>
    `;
  }

  function renderReplacementPipePhotoIntake(rows) {
    const source = Array.isArray(rows) ? rows : [];
    if (!source.length) {
      return "";
    }
    const captured = source.filter((row) => Array.isArray(row.media_ids) && row.media_ids.length).length;
    return `
      <article class="card pipe-requirements-card">
        <div class="detail-header">
          <h3>Replacement Pipe Photo Intake</h3>
          <div class="chip-row">
            ${chip(`${captured}/${source.length} Captured`)}
            ${chip(`${source.length} Required Shots`)}
          </div>
        </div>
        <p class="small-muted">Shot-by-shot intake list for naming each pipe or hose, recording its placement, and linking the imported media IDs that release exact measurements.</p>
        <div class="table-wrap requirement-table-wrap">
          <table class="requirement-table replacement-pipe-intake-table">
            <thead>
              <tr>
                <th>Evidence</th>
                <th>Shot</th>
                <th>Placement</th>
                <th>Measurements</th>
                <th>Release Use</th>
              </tr>
            </thead>
            <tbody>
              ${source
                .map((row) => `
                  <tr>
                    <td class="requirement-evidence-cell">${renderRequirementEvidenceImages({
                      evidence_images: row.evidence_images,
                      photo_status: row.photo_status,
                      requirement_name: row.exact_name,
                    })}</td>
                    <td>
                      <strong>${escapeHtml(row.shot_id || "")} · ${escapeHtml(row.exact_name || "")}</strong>
                      <div class="small-muted">${escapeHtml(row.pipe_id || "")}${row.order_lines ? ` / ${escapeHtml(row.order_lines)}` : ""}</div>
                      <div class="requirement-action"><strong>Take:</strong> ${escapeHtml(row.shot_required || "")}</div>
                      ${statusChip(row.photo_status || "capture_pending")}
                    </td>
                    <td>
                      ${escapeHtml(row.vehicle_placement || "")}
                      ${row.placement_notes ? `<div class="small-muted">${escapeHtml(row.placement_notes)}</div>` : ""}
                    </td>
                    <td>
                      <div class="item-links">
                        ${(Array.isArray(row.measurement_targets_mm) ? row.measurement_targets_mm : [])
                          .map((target) => `<span class="item-link">${escapeHtml(formatToken(target))}</span>`)
                          .join("")}
                      </div>
                    </td>
                    <td>${escapeHtml(row.release_use || "")}</td>
                  </tr>
                `)
                .join("")}
            </tbody>
          </table>
        </div>
      </article>
    `;
  }

  function splitMultiValue(value) {
    return cleanString(value)
      .split(/[|,]/)
      .map((item) => cleanString(item))
      .filter(Boolean);
  }

  function findReplacementPipeOrderLines(pipeId, closureRow, orderRows) {
    const source = Array.isArray(orderRows) ? orderRows : [];
    const idsFromClosure = splitMultiValue(closureRow && closureRow.order_lines);
    if (idsFromClosure.length) {
      const byId = new Map(source.map((row) => [cleanString(row.order_line_id), row]));
      return idsFromClosure.map((id) => byId.get(id)).filter(Boolean);
    }
    return source.filter((row) => splitMultiValue(row.source_basis).includes(pipeId));
  }

  function renderReplacementPipeBuyLines(lines) {
    const rows = Array.isArray(lines) ? lines : [];
    if (!rows.length) {
      return `<span class="small-muted">No order lines mapped.</span>`;
    }
    return `
      <div class="pipe-buy-lines">
        ${rows
          .map((row) => {
            const qty = cleanString(row.qty_to_order || row.qty_required);
            return `
              <div class="pipe-buy-line">
                <strong>${escapeHtml(row.order_line_id || "")}</strong>
                <span>${escapeHtml(row.item || "")}</span>
                ${qty ? `<span class="small-muted">Order: ${escapeHtml(qty)}</span>` : ""}
              </div>
            `;
          })
          .join("")}
      </div>
    `;
  }

  function renderReplacementPipeSimpleBoard(active) {
    const requirements =
      Array.isArray(active.pipe_requirements) && active.pipe_requirements.length
        ? active.pipe_requirements
        : Array.isArray(active.requirements)
          ? active.requirements
          : [];
    const orderRows = Array.isArray(active.replacement_pipe_order_release_specs)
      ? active.replacement_pipe_order_release_specs
      : [];
    const actionRows = Array.isArray(active.replacement_pipe_release_actions)
      ? active.replacement_pipe_release_actions
      : [];
    const closureRows = Array.isArray(active.replacement_pipe_circuit_closure)
      ? active.replacement_pipe_circuit_closure
      : [];
    const photoRows = Array.isArray(active.replacement_pipe_photo_intake)
      ? active.replacement_pipe_photo_intake
      : [];
    const closureByCircuit = new Map(closureRows.map((row) => [cleanString(row.circuit_id), row]));
    const specReady = orderRows.filter((row) => isSpecReadyStatus(row.spec_status || row.order_release_state)).length;
    const openActions = actionRows.filter((row) => cleanString(row.status).toLowerCase() !== "closed");
    const missingPhotos = photoRows.filter((row) => !(Array.isArray(row.media_ids) && row.media_ids.length));
    const released = closureRows.filter((row) => cleanString(row.release_status).toLowerCase() === "released").length;

    return `
      <article class="card replacement-pipe-simple-card">
        <div class="detail-header">
          <h3>Replacement Pipes Board</h3>
          <div class="chip-row">
            ${chip(`${requirements.length} Circuits`)}
            ${chip(`${specReady}/${orderRows.length} Quote Lines Ready`)}
            ${chip(`${openActions.length} Holds Open`)}
            ${chip(`${released}/${closureRows.length} Released`)}
          </div>
        </div>
        <p class="small-muted">Simplified view: one row per circuit. The shop-facing buy quantity is exact enough to quote; final measurement holds stay visible only where cutting, flaring, bending, or dry-fit controls the release.</p>
        <div class="table-wrap requirement-table-wrap">
          <table class="requirement-table replacement-pipe-simple-table">
            <thead>
              <tr>
                <th>Circuit</th>
                <th>Local Quote / Buy</th>
                <th>Final Release Check</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              ${requirements
                .map((row) => {
                  const pipeId = cleanString(row.pipe_id);
                  const closure = closureByCircuit.get(pipeId) || {};
                  const mappedOrderLines = findReplacementPipeOrderLines(pipeId, closure, orderRows);
                  return `
                    <tr>
                      <td>
                        <strong>${escapeHtml(pipeId)} · ${escapeHtml(row.pipe_or_line || "")}</strong>
                        <div class="small-muted">${escapeHtml(row.vehicle_location || "")}</div>
                        <div class="small-muted">Scope: ${escapeHtml(formatToken(row.replace_scope || ""))}</div>
                      </td>
                      <td>
                        ${renderReplacementPipeBuyLines(mappedOrderLines)}
                        ${row.quantity ? `<div class="small-muted requirement-material">Circuit basis: ${escapeHtml(row.quantity)}</div>` : ""}
                      </td>
                      <td>
                        <div>${escapeHtml(closure.action_required || row.critical_measurements || "")}</div>
                        ${closure.route_length_mm ? `<div class="small-muted requirement-material">Length/stock: ${escapeHtml(closure.route_length_mm)}</div>` : ""}
                        ${closure.tube_or_hose_od_id ? `<div class="small-muted">ID/OD basis: ${escapeHtml(closure.tube_or_hose_od_id)}</div>` : ""}
                      </td>
                      <td>
                        <div class="status-stack">
                          ${statusChip(row.spec_status || "spec_ready")}
                          ${statusChip(row.acquisition_status || "not_acquired")}
                          ${statusChip(row.installation_status || "not_installed")}
                          ${statusChip(closure.release_status || "release_hold")}
                        </div>
                      </td>
                    </tr>
                  `;
                })
                .join("")}
            </tbody>
          </table>
        </div>
      </article>
      <article class="card replacement-pipe-holds-card">
        <div class="detail-header">
          <h3>Remaining Holds</h3>
          <div class="chip-row">
            ${chip(`${openActions.length} Open Actions`)}
            ${chip(`${missingPhotos.length} Photo Closeups Missing`)}
          </div>
        </div>
        <div class="pipe-hold-grid">
          <div>
            <h4>Measure Before Release</h4>
            <ul class="pipe-hold-list">
              ${openActions
                .map(
                  (row) => `
                    <li>
                      <strong>${escapeHtml(row.action_id || "")} · ${escapeHtml(formatToken(row.priority || ""))}</strong>
                      <span>${escapeHtml(row.action || "")}</span>
                      ${row.blocks_order_lines ? `<span class="small-muted">Blocks: ${escapeHtml(row.blocks_order_lines)}</span>` : ""}
                    </li>
                  `
                )
                .join("") || `<li><span>No open release actions.</span></li>`}
            </ul>
          </div>
          <div>
            <h4>Photo Closeups Still Useful</h4>
            <ul class="pipe-hold-list">
              ${missingPhotos
                .map(
                  (row) => `
                    <li>
                      <strong>${escapeHtml(row.shot_id || "")}</strong>
                      <span>${escapeHtml(row.exact_name || row.shot_required || "")}</span>
                      ${row.pipe_id ? `<span class="small-muted">${escapeHtml(row.pipe_id)} / ${escapeHtml(row.order_lines || "")}</span>` : ""}
                    </li>
                  `
                )
                .join("") || `<li><span>All planned pipe intake shots have media attached.</span></li>`}
            </ul>
          </div>
        </div>
      </article>
    `;
  }

  function renderWorkstreamRequirements(workstream) {
    const active = workstream || {};
    const rows = Array.isArray(active.requirements) && active.requirements.length
      ? active.requirements
      : active.pipe_requirements;
    if (active.id === "chassis_rubbers") {
      return [
        renderChassisRubberSimpleSpec(),
        renderChassisRubberReferenceImages(),
      ].join("");
    }
    if (active.id === "replacement_pipes") {
      return renderReplacementPipeSimpleBoard(active);
    }
    if (active.id === "brake_system") {
      return renderRequirementTable(rows, {
        title: "Rear Brake Cable / Line Requirements",
        summary: "Rear axle brake cable, hard-line, hose, drum, and retaining-clip actions with removal guidance and replacement-order gates.",
      });
    }
    return renderRequirementTable(rows);
  }

  function renderPackageLinks(title, links) {
    const rows = Array.isArray(links) ? links.filter((link) => cleanString(link && link.url)) : [];
    if (!rows.length) {
      return "";
    }
    return `
      <div class="fabrication-link-group">
        <strong>${escapeHtml(title)}</strong>
        <div class="item-links">
          ${rows
            .map(
              (link, index) =>
                `<a class="item-link" href="${escapeHtml(link.url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(cleanString(link.label) || `File ${index + 1}`)}</a>`
            )
            .join("")}
        </div>
      </div>
    `;
  }

  function renderFabricationPackages(packages) {
    const rows = Array.isArray(packages) ? packages : [];
    if (!rows.length) {
      return "";
    }
    const currentRows = rows.filter((row) => cleanString(row.current_status) === "current_release").length;
    const quoteRows = rows.filter((row) => cleanString(row.current_status) === "quote_first_article_ready").length;
    return `
      <article class="card fabrication-packages-card">
        <div class="detail-header">
          <h3>Fabrication Packages</h3>
          <div class="chip-row">
            ${chip(`${rows.length} Packages`)}
            ${chip(`${currentRows} Current`)}
            ${chip(`${quoteRows} Quote/First Article`)}
          </div>
        </div>
        <p class="small-muted">Clickable shop package links for PDF review, DXF cutting files, SVG visual checks, cut lists, and inspection sheets.</p>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Requirement</th>
                <th>Status</th>
                <th>Release Position</th>
                <th>Files</th>
                <th>Notes</th>
              </tr>
            </thead>
            <tbody>
              ${rows
                .map(
                  (row) => `
                    <tr>
                      <td>
                        <strong>${escapeHtml(row.requirement_id || "")} · ${escapeHtml(row.title || "")}</strong>
                        <div class="small-muted">${escapeHtml(formatToken(row.system || ""))} / ${escapeHtml(row.package_id || "")}</div>
                      </td>
                      <td>${statusChip(row.current_status || "unknown")}</td>
                      <td>${escapeHtml(row.release_position || "")}</td>
                      <td>
                        ${renderPackageLinks("Primary", row.primary_links)}
                        ${renderPackageLinks("DXF", row.dxf_links)}
                        ${renderPackageLinks("SVG", row.svg_links)}
                      </td>
                      <td>
                        ${escapeHtml(row.notes || "")}
                        <div class="small-muted">${escapeHtml(row.file_count || 0)} linked files</div>
                      </td>
                    </tr>
                  `
                )
                .join("")}
            </tbody>
          </table>
        </div>
      </article>
    `;
  }

  function canonicalMediaStem(value) {
    const raw = cleanString(value).toLowerCase();
    if (!raw) {
      return "";
    }
    const withoutQuery = raw.split("?")[0].split("#")[0];
    const leaf = withoutQuery.split("/").pop() || withoutQuery;
    const dotIndex = leaf.lastIndexOf(".");
    const stem = dotIndex > 0 ? leaf.slice(0, dotIndex) : leaf;
    return stem.replace(/_gp_[a-z0-9]+$/i, "").replace(/_exported_\d+$/i, "");
  }

  function imageDedupeKey(image) {
    const effective = withOverride(getBasePhotoMeta(image));
    const mediaId = cleanString(effective.media_id);
    const path = cleanString(effective.path);
    const fileName = cleanString(effective.file_name);
    for (const candidate of [mediaId, path, fileName]) {
      const canonical = canonicalMediaStem(candidate);
      if (canonical) {
        return `canon:${canonical}`;
      }
    }
    if (path) {
      return `path:${path.toLowerCase()}`;
    }
    if (mediaId) {
      return `media:${mediaId.toLowerCase()}`;
    }
    if (fileName) {
      return `file:${fileName.toLowerCase()}`;
    }
    return "";
  }

  function dedupeImages(images, sharedSeenKeys) {
    const source = filterVisibleImages(images);
    const seen = sharedSeenKeys || new Set();
    const output = [];
    source.forEach((image) => {
      const key = imageDedupeKey(image);
      if (key && seen.has(key)) {
        return;
      }
      if (key) {
        seen.add(key);
      }
      output.push(image);
    });
    return output;
  }

  function renderGallery(images) {
    const uniqueImages = dedupeImages(images);
    if (!uniqueImages.length) {
      return '<p class="small-muted">No media evidence mapped yet.</p>';
    }
    return `
      <div class="gallery">
        ${uniqueImages
          .map((image) => {
            const prepared = prepareImage(image, "Evidence media");
            return `
              <figure>
                ${renderPreparedMedia(prepared, "image-open-btn", "gallery-image")}
                <figcaption>${escapeHtml(prepared.caption)}</figcaption>
              </figure>
            `;
          })
          .join("")}
      </div>
    `;
  }

  function renderEvidenceSets(evidenceSets) {
    if (!evidenceSets || !evidenceSets.length) {
      return '<p class="small-muted">No evidence sets available.</p>';
    }
    const sharedSeen = new Set();
    return evidenceSets
      .map((set) => {
        const media = dedupeImages(set.images || [], sharedSeen);
        if (!media.length) {
          return "";
        }
        const videoCount = media.reduce((count, image) => {
          const mediaType = withOverride(getBasePhotoMeta(image)).media_type;
          return mediaType === "video" ? count + 1 : count;
        }, 0);
        const countLabel = videoCount
          ? `${media.length} media (${videoCount} videos)`
          : `${media.length} media`;
        return `
          <section class="card" style="padding:0.65rem;">
            <div class="detail-header">
              <h4 style="margin:0;">${escapeHtml(set.title || "Evidence")}</h4>
              ${chip(countLabel)}
            </div>
            <p class="small-muted">${escapeHtml(set.description || "")}</p>
            ${renderGallery(media)}
          </section>
        `;
      })
      .join("");
  }

  function renderStepsList(steps) {
    if (!steps || !steps.length) {
      return '<p class="small-muted">No steps available.</p>';
    }
    return `
      <ol class="steps-list">
        ${steps
          .map(
            (step) => `
              <li class="step-item">
                <div class="step-row">
                  <span class="step-label">${escapeHtml(step.label)}</span>
                  ${statusChip(step.status)}
                </div>
                <p class="step-detail">${escapeHtml(step.detail || "")}</p>
              </li>
            `
          )
          .join("")}
      </ol>
    `;
  }

  function renderOperationPanels(panels) {
    const sourcePanels = Array.isArray(panels) ? panels : [];
    if (!sourcePanels.length) {
      return "";
    }
    return sourcePanels
      .map((panel) => {
        const metrics = Array.isArray(panel.metrics) ? panel.metrics : [];
        const zones = Array.isArray(panel.zones) ? panel.zones : [];
        const steps = Array.isArray(panel.steps) ? panel.steps : [];
        const materials = panel.materials || {};
        const available = Array.isArray(materials.available) ? materials.available : [];
        const pendingDelivery = Array.isArray(materials.pending_delivery) ? materials.pending_delivery : [];
        const missing = Array.isArray(materials.missing) ? materials.missing : [];
        return `
          <article class="card">
            <div class="detail-header">
              <h3>${escapeHtml(panel.title || "Operations")}</h3>
              ${chip(panel.key || "operation")}
            </div>
            <p>${escapeHtml(panel.summary || "")}</p>
            ${
              metrics.length
                ? `<div class="chip-row">${metrics.map((metric) => chip(`${metric.label}: ${metric.value}`)).join("")}</div>`
                : ""
            }
            ${
              zones.length
                ? `
                  <h4>Still Needs Work</h4>
                  <div class="table-wrap">
                    <table>
                      <thead>
                        <tr>
                          <th>Area</th>
                          <th>Remaining</th>
                          <th>Status</th>
                          <th>Work Required</th>
                          <th>Evidence</th>
                        </tr>
                      </thead>
                      <tbody>
                        ${zones
                          .map(
                            (zone) => `
                              <tr>
                                <td><strong>${escapeHtml(zone.area || "")}</strong></td>
                                <td>${escapeHtml(zone.remaining || "")}</td>
                                <td>${statusChip(zone.status || "pending")}</td>
                                <td>${escapeHtml(zone.work_required || "")}</td>
                                <td>${escapeHtml(zone.evidence_count || "0")}</td>
                              </tr>
                            `
                          )
                          .join("")}
                      </tbody>
                    </table>
                  </div>
                `
                : ""
            }
            ${
              steps.length
                ? `
                  <h4>Steps Before Primer</h4>
                  ${renderStepsList(steps)}
                `
                : ""
            }
            ${
              available.length || pendingDelivery.length || missing.length
                ? `
                  <div class="operation-materials">
                    <div>
                      <h4>Available</h4>
                      ${renderPlainList(available)}
                    </div>
                    <div>
                      <h4>Pending Delivery</h4>
                      ${renderPlainList(pendingDelivery)}
                    </div>
                    <div>
                      <h4>Still Missing / Lock</h4>
                      ${renderPlainList(missing)}
                    </div>
                  </div>
                `
                : ""
            }
          </article>
        `;
      })
      .join("");
  }

  function renderSubtaskGroups(groups) {
    const sourceGroups = Array.isArray(groups) ? groups : [];
    if (!sourceGroups.length) {
      return "";
    }
    return sourceGroups
      .map((group) => {
        const subtasks = Array.isArray(group.subtasks) ? group.subtasks : [];
        return `
          <article class="card">
            <div class="detail-header">
              <h3>${escapeHtml(group.title || "Sub-Tasks")}</h3>
              ${chip(`${subtasks.length} sub-tasks`)}
            </div>
            <p>${escapeHtml(group.summary || "")}</p>
            ${
              subtasks.length
                ? `
                  <div class="subtask-grid">
                    ${subtasks.map((subtask) => renderSubtaskCard(subtask)).join("")}
                  </div>
                `
                : '<p class="small-muted">No sub-tasks mapped yet.</p>'
            }
          </article>
        `;
      })
      .join("");
  }

  function renderSubtaskListSection(title, items) {
    const sourceItems = Array.isArray(items) ? items.filter((item) => cleanString(item)) : [];
    if (!sourceItems.length) {
      return "";
    }
    const shouldLinkInventory = ["Parts", "Registered Items"].includes(cleanString(title));
    return `
      <div class="subtask-section">
        <div class="subtask-section-header">
          <h5>${escapeHtml(title)}</h5>
          ${shouldLinkInventory ? renderInventoryPageLink("Inventory") : ""}
        </div>
        ${renderPlainList(sourceItems)}
      </div>
    `;
  }

  function renderSubtaskCard(subtask) {
    const images = dedupeImages(Array.isArray(subtask.images) ? subtask.images : []);
    const processSteps = Array.isArray(subtask.process_steps) ? subtask.process_steps.filter((item) => cleanString(item)) : [];
    const tools = Array.isArray(subtask.tools) ? subtask.tools.filter((item) => cleanString(item)) : [];
    const supplies = Array.isArray(subtask.supplies) ? subtask.supplies.filter((item) => cleanString(item)) : [];
    const parts = Array.isArray(subtask.parts) ? subtask.parts.filter((item) => cleanString(item)) : [];
    const registeredItems = Array.isArray(subtask.registered_items)
      ? subtask.registered_items.filter((item) => cleanString(item))
      : [];
    const safety = Array.isArray(subtask.safety) ? subtask.safety.filter((item) => cleanString(item)) : [];
    return `
      <section class="subtask-card">
        <div class="detail-header">
          <h4>${escapeHtml(subtask.title || "Sub-task")}</h4>
          ${statusChip(subtask.status || "pending")}
        </div>
        <div class="chip-row">
          ${subtask.priority ? chip(`Priority: ${subtask.priority}`) : ""}
          ${subtask.remaining ? chip(`Remaining: ${subtask.remaining}`) : ""}
          ${chip(`${images.length} images`)}
        </div>
        ${subtask.instruction ? `<p><strong>Instruction:</strong> ${escapeHtml(subtask.instruction || "")}</p>` : ""}
        ${
          processSteps.length
            ? `
              <div class="subtask-process">
                <h5>Process</h5>
                <ol>
                  ${processSteps.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}
                </ol>
              </div>
            `
            : ""
        }
        <div class="subtask-sections">
          ${renderSubtaskListSection("Tools", tools)}
          ${renderSubtaskListSection("Supplies", supplies)}
          ${renderSubtaskListSection("Parts", parts)}
          ${renderSubtaskListSection("Registered Items", registeredItems)}
          ${renderSubtaskListSection("Safety", safety)}
        </div>
        ${subtask.hold_point ? `<p class="small-muted"><strong>Hold:</strong> ${escapeHtml(subtask.hold_point || "")}</p>` : ""}
        ${images.length ? renderGallery(images) : '<p class="small-muted">No images linked to this sub-task.</p>'}
      </section>
    `;
  }

  function renderPlainList(items) {
    const sourceItems = Array.isArray(items) ? items : [];
    if (!sourceItems.length) {
      return '<p class="small-muted">None recorded.</p>';
    }
    return `
      <ul class="plain-list">
        ${sourceItems.map((item) => `<li class="plain-item">${escapeHtml(item || "")}</li>`).join("")}
      </ul>
    `;
  }

  function renderMarketSpecList(title, items) {
    const sourceItems = Array.isArray(items) ? items.filter((item) => cleanString(item)) : [];
    if (!sourceItems.length) {
      return "";
    }
    return `
      <div class="market-spec-block">
        <h4>${escapeHtml(title)}</h4>
        ${renderPlainList(sourceItems)}
      </div>
    `;
  }

  function renderMarketSpecCards(specs) {
    const sourceSpecs = Array.isArray(specs) ? specs.filter((spec) => spec && cleanString(spec.title)) : [];
    if (!sourceSpecs.length) {
      return "";
    }
    return sourceSpecs
      .map((spec) => {
        const price = spec.price_guidance || {};
        const quantity = cleanString(spec.quantity || price.quantity);
        const image = spec.image && !isImageDeleted(spec.image) ? spec.image : null;
        const priceBits = [
          quantity ? `Quantity: ${quantity}` : "",
          price.unit_price_range ? `Unit price range: ${price.unit_price_range}` : price.target_range ? `Unit price range: ${price.target_range}` : "",
          price.negotiation_midpoint ? `Negotiation midpoint: ${price.negotiation_midpoint}` : "",
          price.total_value_range ? `Total value: ${price.total_value_range}` : "",
          price.rule || "",
        ].filter((item) => cleanString(item));
        return `
          <article class="card market-spec-card scout-spec-card" id="${escapeHtml(spec.id || "")}">
            <div class="scout-spec-layout">
              ${
                image
                  ? renderFigureImage(image, spec.title || "Scout reference image", {
                      figureClass: "scout-spec-figure",
                      buttonClass: "image-open-btn scout-spec-image-btn",
                      imageClass: "scout-spec-image",
                      captionClass: "small-muted",
                      showCaption: false,
                    })
                  : ""
              }
              <div class="scout-spec-copy">
                <div class="detail-header">
                  <h3>${escapeHtml(spec.title || "Market Spec")}</h3>
                  ${chip(spec.scope || "Market scout")}
                </div>
                ${spec.plain_stall_request ? `<p class="market-spec-callout"><strong>Ask for:</strong> ${escapeHtml(spec.plain_stall_request)}</p>` : ""}
                ${spec.buy_target ? `<p><strong>Buy target:</strong> ${escapeHtml(spec.buy_target)}</p>` : ""}
                ${quantity ? `<p><strong>Quantity:</strong> ${escapeHtml(quantity)}</p>` : ""}
              </div>
            </div>
            <div class="market-spec-grid">
              ${renderMarketSpecList("Must Include", spec.must_include)}
              ${renderMarketSpecList("Test Before Payment", spec.bench_test)}
              ${renderMarketSpecList("Reject If", spec.reject_if)}
              ${renderMarketSpecList("Photos + Details To Send", spec.capture_before_leaving)}
            </div>
            ${priceBits.length ? `<p class="market-spec-price"><strong>Price Guidance:</strong> ${escapeHtml(priceBits.join(" | "))}</p>` : ""}
            ${spec.decision_rule ? `<p><strong>Buy rule:</strong> ${escapeHtml(spec.decision_rule)}</p>` : ""}
            ${renderLinksPanel(spec)}
          </article>
        `;
      })
      .join("");
  }

  function workstreamById(workstreamId) {
    const targetId = cleanString(workstreamId);
    return (data.workstreams || []).find((workstream) => workstream.id === targetId) || null;
  }

  function scoutDocLink(path, label) {
    return {
      url: `../../${path}`,
      label,
    };
  }

  function scoutRowText(row) {
    return [
      row.entry_id,
      row.source_ref,
      row.workstream,
      row.source,
      row.supply_type,
      row.inventory_group,
      row.item,
      row.procurement_stage,
      row.status,
      row.status_group,
      row.status_detail,
      row.notes,
      row.vendor,
      row.evidence_ref,
      row.source_sheet,
      row.system,
      row.decision,
      row.stage,
    ]
      .map((value) => cleanString(value).toLowerCase())
      .join(" ");
  }

  function dedupeScoutRows(rows) {
    const seen = new Set();
    return (Array.isArray(rows) ? rows : []).filter((row) => {
      if (!row) {
        return false;
      }
      const key = [row.entry_id, row.source_ref, row.id, row.title, row.item].map(cleanString).join("|");
      if (seen.has(key)) {
        return false;
      }
      seen.add(key);
      return true;
    });
  }

  function filterScoutRows(rows, config) {
    const entryIds = new Set(config.entryIds || []);
    const workstreams = new Set(config.workstreams || []);
    const terms = (config.terms || []).map((term) => cleanString(term).toLowerCase()).filter(Boolean);
    return dedupeScoutRows(rows).filter((row) => {
      const entryId = cleanString(row.entry_id || row.source_ref);
      if (entryId && entryIds.has(entryId)) {
        return true;
      }
      const workstream = cleanString(row.workstream);
      if (workstream && workstreams.has(workstream)) {
        return true;
      }
      const text = scoutRowText(row);
      return terms.some((term) => text.includes(term));
    });
  }

  function scoutSourceLinks(sourceLinks, terms) {
    const sourceTerms = (terms || []).map((term) => cleanString(term).toLowerCase()).filter(Boolean);
    if (!sourceTerms.length) {
      return [];
    }
    return dedupeScoutRows(sourceLinks).filter((row) => {
      const text = scoutRowText(row);
      return sourceTerms.some((term) => text.includes(term));
    });
  }

  function scoutOrderSpecRows(rows, limit) {
    const sourceRows = Array.isArray(rows) ? rows : [];
    const maxRows = Number.isFinite(limit) ? limit : sourceRows.length;
    return sourceRows.slice(0, maxRows).map((row) => {
      const specRow = {
        id: row.order_line_id || row.rubber_order_id || row.requirement_id || row.action_id || "",
        item: row.item || row.item_group || row.requirement_name || row.action || "",
        partNumber: row.part_number_or_code || "",
        route: row.route || row.workstream_category || row.priority || row.release_status || "",
        state: row.order_release_state || row.pre_order_gate || row.status || row.release_status || "",
        spec: row.exact_order_spec || row.exact_recreation_spec || row.ordering_spec || row.material_spec || row.user_action_required || row.notes || "",
        action: row.user_action_required || row.measurements_required_before_order || row.action_required || row.do_not_order_if || "",
        qty: row.qty_to_order || row.qty_required || row.quantity || "",
        dimension: row.dimension_spec_mm || row.dimension_spec || row.critical_measurements || "",
        material: row.material_spec || "",
        sourceBasis: row.source_basis || row.source_ref || "",
        reject: row.do_not_order_if || row.reject_if || "",
        notes: row.notes || "",
        image: row.image || null,
        evidenceImages: Array.isArray(row.evidence_images) ? row.evidence_images : [],
      };
      specRow.image = specRow.image || scoutComponentImage(specRow);
      return specRow;
    });
  }

  function scoutReferenceImage(path, caption, mediaId) {
    return {
      path,
      caption,
      media_type: "photo",
      component_group: "procurement_inventory",
      specific_component: "",
      stage: "",
      media_id: mediaId || "",
      match_basis: "semantic_reference_image",
    };
  }

  function scoutPreviousPartImage(path, caption, mediaId, matchedTokens = []) {
    return {
      path,
      caption,
      media_type: "photo",
      component_group: "procurement_inventory",
      specific_component: "previous_part_photo",
      stage: "fabrication_reference",
      media_id: mediaId || "",
      matched_tokens: matchedTokens,
      match_basis: "previous_part_photo",
      match_score: "900",
    };
  }

  function firstEvidencePreviousPartImage(row) {
    const evidenceImages = Array.isArray(row && row.evidenceImages) ? row.evidenceImages : [];
    const image = evidenceImages.find((candidate) => candidate && !isImageDeleted(candidate));
    if (!image) {
      return null;
    }
    return {
      ...image,
      caption: cleanString(image.caption) || `${cleanString(row && row.item) || "Component"} · previous part evidence`,
      match_basis: cleanString(image.match_basis) || "previous_part_photo",
      specific_component: cleanString(image.specific_component) || "previous_part_photo",
    };
  }

  function scoutPreviousFabricatedPartImage(row, text) {
    const rowId = cleanString(row && row.id).toUpperCase();
    const partNumber = cleanString(row && row.partNumber).toLowerCase();
    const blob = `${cleanString(text).toLowerCase()} ${rowId.toLowerCase()} ${partNumber}`;
    const subject = cleanString(row && row.item) || cleanString(row && row.id) || "Fabricated part";
    const has = (...tokens) => tokens.every((token) => blob.includes(token));
    const hasAny = (...tokens) => tokens.some((token) => blob.includes(token));
    const previous = (path, label, mediaId, tokens = []) =>
      scoutPreviousPartImage(path, `${subject} · ${label}`, mediaId, tokens);

    if (rowId === "BM-CUP-SM" || partNumber.includes("bm_cup_small") || (has("cup", "small") && hasAny("body-mount", "body mount"))) {
      return previous("../../photos/20260502_004413_gp_Qno8OVRg.jpg", "previous small body-mount cup/seat sample", "20260502_004413_gp_Qno8OVRg", ["bm-cup-sm", "previous"]);
    }
    if (rowId === "BM-CUP-LG" || partNumber.includes("bm_cup_large") || (has("cup", "large") && hasAny("body-mount", "body mount"))) {
      return previous("../../photos/20260502_004231_gp_CfosvPIg.jpg", "previous large body-mount cup/seat scale sample", "20260502_004231_gp_CfosvPIg", ["bm-cup-lg", "previous"]);
    }
    if (hasAny("body-mount cup", "body mount cup", "cup / seat", "cup washer", "seat washer", "bm-cup")) {
      return previous("../../photos/20260502_004413_gp_Qno8OVRg.jpg", "previous body-mount cup/seat sample", "20260502_004413_gp_Qno8OVRg", ["bm-cup", "previous"]);
    }
    if (rowId === "BM-LG" || partNumber.includes("bm_lg") || hasAny("large circular body-mount", "large circular body mount", "large body-mount cushion", "large body mount cushion")) {
      return previous("../../photos/20260502_004231_gp_CfosvPIg.jpg", "previous large circular body-mount cushion sample", "20260502_004231_gp_CfosvPIg", ["bm-lg", "previous"]);
    }
    if (rowId === "BM-SM" || partNumber.includes("bm_sm") || hasAny("small circular body-mount", "small circular body mount", "small body-mount cushion", "small body mount cushion")) {
      return previous("../../photos/20260502_004437_gp_f1TySzww.jpg", "previous small circular body-mount cushion sample", "20260502_004437_gp_f1TySzww", ["bm-sm", "previous"]);
    }
    if (rowId === "FS-OVAL" || partNumber.includes("fs_oval") || hasAny("two-hole oval", "two hole oval", "oval front-support", "oval front support", "oval pad")) {
      return previous("../../photos/20260502_004345_gp_yK8VYzMQ.jpg", "previous two-hole oval front-support pad", "20260502_004345_gp_yK8VYzMQ", ["fs-oval", "previous"]);
    }
    if (rowId === "FS-STRIP-L" || partNumber.includes("fs_strip_left") || (hasAny("front-support strip", "front support strip", "strip rubber") && hasAny("left", "left-side", "left side"))) {
      return previous("../../photos/20260502_004201_gp_zfUSmKJg.jpg", "previous left front-support strip sample", "20260502_004201_gp_zfUSmKJg", ["fs-strip-l", "previous"]);
    }
    if (rowId === "FS-STRIP-R" || partNumber.includes("fs_strip_right") || (hasAny("front-support strip", "front support strip", "strip rubber") && hasAny("right", "right-side", "right side"))) {
      return previous("../../photos/20260502_004222_gp_PKRe5HSQ.jpg", "previous right front-support strip sample", "20260502_004222_gp_PKRe5HSQ", ["fs-strip-r", "previous"]);
    }
    if (hasAny("crush sleeve", "body-mount sleeve", "body mount sleeve", "shim and spacer", "shim pack")) {
      return firstEvidencePreviousPartImage(row);
    }
    if (rowId === "MIDI5-PLATE-001" || rowId === "MIDI5-SUBPLATE-001" || hasAny("midi5_mount_plate", "midi5_holder_subplate", "midi 5-way structural", "midi 5-way non-conductive")) {
      return previous("../../photos/20260411_143135.jpg", "received MIDI holder bank to mount", "20260411_143135", ["midi5", "previous"]);
    }
    if (rowId === "RELAY-CARRIER-001" || rowId === "RELAY-GUARD-001" || hasAny("relay_carrier", "relay_rear_guard", "daier prewired", "10-way relay/fuse", "10 way relay/fuse")) {
      return previous("../../photos/20260411_143125.jpg", "received 10-way relay/fuse box to mount", "20260411_143125", ["relay-box", "previous"]);
    }

    return firstEvidencePreviousPartImage(row);
  }

  function scoutComponentImage(row) {
    const text = [
      row && row.id,
      row && row.item,
      row && row.partNumber,
      row && row.route,
      row && row.spec,
      row && row.order_text,
      row && row.material,
      row && row.material_spec,
      row && row.sourceBasis,
      row && row.source_basis,
      row && row.notes,
    ]
      .map((value) => cleanString(value).toLowerCase())
      .join(" ");
    const has = (...tokens) => tokens.every((token) => text.includes(token));
    const hasAny = (...tokens) => tokens.some((token) => text.includes(token));
    const ref = (path, label, mediaId) => scoutReferenceImage(path, `${cleanString(row && row.item) || "Component"} · ${label}`, mediaId);
    const previousPartImage = scoutPreviousFabricatedPartImage(row, text);
    if (previousPartImage) {
      return previousPartImage;
    }

    if (hasAny("fuse carrier", "cabin fuse", "compact fuse", "under-dash fuse", "under dash fuse")) {
      return ref("../../deliverables/selling_site_images/images/manual_overrides/compact_cabin_fuse_box_user_photo_20260504.png", "user-supplied compact fuse box reference image", "compact_cabin_fuse_box_user_photo_20260504");
    }
    if (hasAny("bench vice", "workshop vice", "vise") || has("vice", "bench")) {
      return ref("../../deliverables/selling_site_images/images/reference_catalog/bench_vice.jpg", "bolt-down bench vice reference image", "bench_vice");
    }
    if (hasAny("toolbench", "workbench", "work bench")) {
      return ref("../../deliverables/selling_site_images/images/reference_catalog/toolbench.jpg", "toolbench/workbench reference image", "toolbench");
    }
    if (hasAny("pillar drill", "bench drill", "drill press")) {
      return ref("../../deliverables/selling_site_images/images/reference_catalog/bench_drill.jpg", "pillar drill / bench drill reference image", "bench_drill");
    }
    if (hasAny("swc-block-001", "rectangular hardwood cribbing block")) {
      return ref("../../data/manual/fabrication/suspension_wood_cribbing_rev_a/swc_rectangular_cribbing_block_rev_a.svg", "rectangular block drawing", "swc_block_001");
    }
    if (hasAny("swc-chock-001", "hardwood wedge chock")) {
      return ref("../../data/manual/fabrication/suspension_wood_cribbing_rev_a/swc_wedge_chock_rev_a.svg", "wedge chock drawing", "swc_chock_001");
    }
    if (cleanString(row && row.partNumber).toLowerCase().endsWith(".dxf") && cleanString(row && row.route)) {
      const svgName = cleanString(row.partNumber).replace(/\.dxf$/i, ".svg");
      const mediaId = cleanString(row.id || svgName).toLowerCase().replace(/[^a-z0-9_-]+/g, "_");
      return ref(`../../data/manual/fabrication/${cleanString(row.route)}/${svgName}`, "part drawing", mediaId);
    }
    if (hasAny("cribbing", "wedge chock", "hardwood")) {
      return ref("../../deliverables/selling_site_images/images/manual_overrides/suspension_hardwood_cribbing_cut_set_flat_lay.jpg", "hardwood cribbing cut-set reference image", "hardwood_cribbing");
    }
    if (hasAny("formed metal coolant", "formed coolant pipe", "metal coolant", "radiator pipe assembly")) {
      return ref("../../photos/20260502_004106_gp_wlYlUahA.jpg", "formed coolant pipe sample photo", "formed_coolant_pipe_sample");
    }
    if (hasAny("connector hose", "connector/coupler", "coupler hoses")) {
      return ref("../../photos/20260502_004133_gp_ZEpqmARA.jpg", "formed-pipe connector hose sample photo", "formed_pipe_connector_hose_sample");
    }
    if (has("heater", "hose")) {
      return ref("../../deliverables/selling_site_images/images/reference_catalog/heater_hose.jpg", "heater hose reference image", "heater_hose");
    }
    if (hasAny("radiator overflow", "overflow hose", "coolant overflow")) {
      return ref("../../deliverables/selling_site_images/images/reference_catalog/coolant_overflow.jpg", "coolant overflow reference image", "coolant_overflow");
    }
    if (has("radiator", "hose") || has("coolant", "hose") || hasAny("upper radiator", "lower radiator")) {
      return ref("../../deliverables/selling_site_images/images/reference_catalog/radiator_hose.jpg", "radiator/coolant hose reference image", "radiator_hose");
    }
    if ((has("brake", "booster") || has("brake", "servo")) && !hasAny("hose", "line", "pipe", "tube")) {
      return ref("../../deliverables/selling_site_images/images/reference_catalog/brake_booster.jpg", "brake booster reference image", "brake_booster");
    }
    if (hasAny("fuel", "diesel", "injector leak-off", "leak-off")) {
      return ref("../../deliverables/selling_site_images/images/reference_catalog/fuel_hose.jpg", "diesel fuel hose reference image", "fuel_hose");
    }
    if (hasAny("vacuum", "breather", "oil mist", "oil outlet")) {
      return ref("../../deliverables/selling_site_images/images/reference_catalog/fuel_hose.jpg", "vacuum/breather hose reference image", "vacuum_hose");
    }
    if ((has("brake") || has("clutch")) && hasAny("hose", "line", "hydraulic", "tube")) {
      return ref("../../deliverables/selling_site_images/images/reference_catalog/brake_hose_line.jpg", "hydraulic hose/line reference image", "brake_hose_line");
    }
    if (hasAny("p-clips", "p clips", "support clips", "line protection", "edge protection")) {
      return ref("../../deliverables/selling_site_images/images/reference_catalog/clamp.jpg", "line clip/clamp reference image", "clamp");
    }
    if (hasAny("cup washer", "crush sleeve", "shim")) {
      return ref("../../deliverables/selling_site_images/images/reference_catalog/body_shims.jpg", "body shim/washer reference image", "body_shims");
    }
    if (has("body", "mount") || hasAny("cushion", "front-support", "front support", "oval pad")) {
      return ref("../../deliverables/selling_site_images/images/reference_catalog/body_mount_kit.jpg", "body mount rubber reference image", "body_mount_kit");
    }
    if (has("exhaust", "hanger")) {
      return ref("../../deliverables/selling_site_images/images/reference_catalog/exhaust_hanger.jpg", "exhaust hanger reference image", "exhaust_hanger");
    }
    if (has("bump", "stop")) {
      return ref("../../deliverables/selling_site_images/images/reference_catalog/bump_stop.jpg", "bump stop reference image", "bump_stop");
    }
    if (hasAny("glow plug", "heat plug")) {
      return ref("../../deliverables/selling_site_images/images/reference_catalog/glow_plugs.jpg", "glow plug reference image", "glow_plugs");
    }
    return ref("../../deliverables/selling_site_images/images/reference_catalog/generic_part.jpg", "component reference image", "generic_part");
  }

  function firstScoutImage(rows) {
    const sourceRows = Array.isArray(rows) ? rows : [];
    const row = sourceRows.find((item) => item && item.image && !isImageDeleted(item.image));
    return row ? row.image : null;
  }

  function scoutSpecImage(rows, fallbackImage) {
    return firstScoutImage(rows) || fallbackImage || null;
  }

  function attachScoutImage(specs, rows, fallbackImage) {
    const image = fallbackImage || scoutSpecImage(rows, null);
    return (Array.isArray(specs) ? specs : []).map((spec) => ({
      ...spec,
      image: spec.image || image,
    }));
  }

  function fallbackMarketSpec(sourceSpecs, fallbackSpec) {
    const specs = Array.isArray(sourceSpecs) ? sourceSpecs.filter((spec) => spec && cleanString(spec.title)) : [];
    return specs.length ? specs : [fallbackSpec];
  }

  function buildScoutCategories() {
    const parts = data.parts || {};
    const allPartRows = dedupeScoutRows([
      ...(parts.open_rows || []),
      ...(parts.ordered_pending_delivery || []),
      ...(parts.urgent_actions || []),
    ]);
    const allSupplyRows = dedupeScoutRows((data.supplies && data.supplies.all_rows) || []);
    const epsWorkstream = workstreamById("eps_vitz_upgrade");
    const replacementPipesWorkstream = workstreamById("replacement_pipes");
    const chassisRubbersWorkstream = workstreamById("chassis_rubbers");
    const fabricationWorkstream = workstreamById("fabrication_handoff");
    const epsMarketSpecs = [
      ...((epsWorkstream && epsWorkstream.market_specs) || []),
      ...((parts.market_specs || []).filter((spec) => cleanString(spec.id).includes("eps"))),
    ];
    const brakeMarketSpecs = (parts.market_specs || []).filter((spec) => cleanString(spec.id).includes("brake_booster"));
    const epsParts = filterScoutRows(allPartRows, {
      entryIds: ["part_power_steering_upgrade"],
      workstreams: ["eps_vitz_upgrade"],
      terms: ["eps", "vitz", "yaris", "scp90", "ncp90"],
    });
    const brakeBoosterParts = filterScoutRows(allPartRows, {
      entryIds: ["part_brake_booster_servo_44610_60050"],
      workstreams: ["brake_system"],
      terms: ["brake booster", "brake servo", "44610-60050", "vacuum booster"],
    });
    const pipeParts = filterScoutRows(allPartRows, {
      entryIds: [
        "part_mech_radiator_hose_set",
        "part_mech_fuel_hose_and_clamps",
        "part_mech_heater_hose_set",
        "part_mech_vacuum_hose_refresh",
        "part_mech_brake_flex_hose_set",
        "part_rear_axle_hard_brake_lines",
        "part_rear_center_brake_flex_hose",
        "part_front_brake_hose_pair",
      ],
      workstreams: ["replacement_pipes", "brake_system"],
      terms: ["replacement pipe", "hose", "hard-line", "brake flex", "fuel hose", "heater hose", "vacuum"],
    });
    const rubberParts = filterScoutRows(allPartRows, {
      entryIds: [
        "part_body_mount_rubber_kit",
        "part_body_mount_hardware_kit",
        "part_body_mount_shim_pack",
        "part_body_rubber_plastic_bumpers_isolators",
        "part_body_shoulder_pins_sleeves_spacers",
      ],
      workstreams: ["chassis_rubbers"],
      terms: ["body mount", "rubber kit", "shim", "sleeve", "isolator"],
    });
    const fuseBoxParts = filterScoutRows(allPartRows, {
      entryIds: ["part_cabin_compact_fuse_boxes"],
      workstreams: ["electrical_reset"],
      terms: ["compact cabin fuse", "additional fuse", "fuse box", "fuse carrier"],
    });
    const workshopSupportParts = dedupeScoutRows([
      ...filterScoutRows(allPartRows, {
        entryIds: ["part_suspension_wooden_cribbing_blocks"],
        workstreams: ["suspension_upgrade"],
        terms: ["wooden cribbing", "hardwood", "wedge chocks"],
      }),
      ...filterScoutRows(allSupplyRows, {
        entryIds: [
          "tool_local_toolbench",
          "tool_local_bench_drill",
          "tool_local_bench_vice",
        ],
        workstreams: ["site_setup", "fabrication_handoff"],
        terms: ["workbench", "toolbench", "pillar drill", "bench drill", "drill press", "bench vice", "workshop vice", "vise"],
      }),
    ]);
    const fabricationParts = dedupeScoutRows([
      ...filterScoutRows(allPartRows, {
        entryIds: ["service_local_3d_printing_fabrication_prototypes"],
        workstreams: ["fabrication_handoff"],
        terms: ["3d printing", "fabrication", "prototype", "guard", "template", "spacer"],
      }),
      ...filterScoutRows(allSupplyRows, {
        entryIds: ["service_local_3d_printing_fabrication_prototypes"],
        workstreams: ["fabrication_handoff"],
        terms: ["3d printing", "fabrication", "prototype", "guard", "template", "spacer"],
      }),
    ]);
    const hoseMarketSpec = {
      id: "pipes_hoses_market_scout",
      title: "Pipes + Hoses Market Scout",
      scope: "Exact order sheet",
      quantity: "23 HLS line items plus 21 pipe release-spec lines",
      plain_stall_request:
        "I need the exact J40/HJ47 hose, pipe, hard-line, brake/clutch hydraulic, fuel, vacuum, and support-clip lines listed in the order sheet. Use those IDs and specs; do not quote generic rubber pipe.",
      buy_target:
        "Use the exact requirement list below and the linked handoff pages. EPDM for coolant/heater, diesel-rated fuel hose, reinforced vacuum hose, brake-rated hard line, and complete crimped DOT/SAE J1401 or OEM-equivalent brake/clutch hose assemblies only.",
      must_include: [
        "Correct inside diameter, length, bends, or end fittings matched to the old sample.",
        "New clamps, clips, or fittings quoted separately when needed.",
        "Brake and clutch flex hoses supplied as complete crimped assemblies.",
        "Brake hard-line material only in brake-rated 4.75 mm / 3/16 in tube where hard lines are being replaced.",
        "Visible rating or brand markings where the hose type normally has markings.",
      ],
      bench_test: [
        "Hold each hose or line against the old sample before payment.",
        "Confirm brake and clutch thread, flare, banjo, seat, bracket, and clip style before payment.",
        "Ask the seller to point out hose rating markings.",
        "For radiator and heater hose, check that the bend will not kink when installed.",
      ],
      reject_if: [
        "Seller gives generic hydraulic or air hose for fuel, coolant, vacuum, brake, or clutch use.",
        "Brake or clutch hose is loose rubber hose instead of a crimped hydraulic assembly.",
        "End fittings, bend, diameter, length, or clip style do not match the sample or measurement.",
        "Hose is old, cracked, swollen, oily, unmarked where markings are required, or already cut too short.",
      ],
      capture_before_leaving: [
        "Photo of each new hose or line beside the old sample or measurement note.",
        "Photo of all end fittings, clamps, clips, and visible rating marks.",
        "Seller name, phone number, shop location, price by line, and return terms.",
      ],
      price_guidance: {
        rule: "Quote each line separately. Do not pay for any brake, clutch, fuel, or vacuum item until sample match and material type are clear.",
      },
      decision_rule: "Buy only the lines that match the old sample or confirmed measurement and have the correct material rating.",
      links: [
        scoutDocLink("docs/hose-local-scout-handoff.md", "Hose local scout handoff"),
        scoutDocLink("docs/local-market-component-order-spec-20260504.md", "Exact local-market order spec"),
        scoutDocLink("docs/engine-hose-tube-replacement-specs.md", "Engineering controls"),
      ],
    };
    const rubberMarketSpec = {
      id: "body_mount_rubbers_market_scout",
      title: "Body Mount Rubbers Market Scout",
      scope: "Exact requirement sheet",
      quantity: "9 rubber requirements plus controlled hardware/order-release lines",
      plain_stall_request:
        "I need the exact J40 body/front-support rubber requirements listed in the spec sheet, plus sleeves, cup washers, shims, spacers, bolts, nuts, and washers as separate controlled lines. No used rubber.",
      buy_target:
        "Use the exact requirement list below and the linked rubber-ordering pages. Buy a complete matched OE/reproduction kit only if it matches the actual station layout, or fabricate from the measured BM-LG, BM-SM, FS-OVAL, FS-STRIP-L, and FS-STRIP-R specs.",
      must_include: [
        "Upper and lower body mount rubber cushions for the required body stations.",
        "Steel sleeves, cup or seat washers, shims, spacers, bolts, nuts, and washers quoted separately.",
        "Rubber dimensions shown clearly: outside diameter, inside hole, thickness, and sleeve length.",
        "New rubber only, with no cracks, hard spots, or old compression damage.",
      ],
      bench_test: [
        "Compare every rubber and sleeve to the old sample or written dimension sheet.",
        "Press the rubber by hand: it should feel firm and elastic, not brittle or sponge-soft.",
        "Check sleeves and washers with the actual bolt size before payment.",
        "Keep shim and spacer thicknesses separated and labelled.",
      ],
      reject_if: [
        "Seller offers old used rubber, unknown mixed rubber, sponge rubber, or cracked stock.",
        "Sleeve hole, rubber height, washer shape, or shim thickness does not match the measured plan.",
        "Hardware has no grade mark, wrong pitch, damaged threads, or heavy rust.",
        "Seller will not allow measurement photos before payment.",
      ],
      capture_before_leaving: [
        "Full kit photo with all rubber, sleeves, washers, shims, spacers, and bolts laid out.",
        "Close photos with ruler/caliper showing key dimensions.",
        "Seller name, phone number, shop location, material claim, price, and return terms.",
      ],
      price_guidance: {
        rule: "Keep rubber, sleeves, shims, and bolts as separate quote lines so a wrong line can be rejected without losing the whole package.",
      },
      decision_rule: "Buy only after the old mount samples or measurement sheet prove the rubber shape, sleeve size, and hardware stack.",
      links: [
        scoutDocLink("docs/rubber-ordering-spec-20260502.md", "Rubber ordering spec"),
        scoutDocLink("docs/local-market-component-order-spec-20260504.md", "Exact local-market order spec"),
        scoutDocLink("docs/rubber-recreation-fabrication-spec-20260502.md", "Rubber fabrication spec"),
      ],
    };
    const fuseBoxMarketSpec = {
      id: "additional_fuse_box_market_scout",
      title: "Additional Fuse Box Market Scout",
      scope: "Compact OEM-style add-on",
      quantity: "1 compact add-on carrier to match the reusable block",
      plain_stall_request:
        "I need one compact old-OEM under-dash blade-fuse / junction-block style carrier to match the blade-style block extracted from the existing car. Six positions must be usable, with clean rear terminals or serviceable pigtails.",
      buy_target:
        "Reuse the existing extracted compact blade-style donor block for two 6-fuse groups if it tests clean, then buy one matching compact old-OEM add-on carrier for the third group. Prefer Suzuki Mehran/Maruti 800, Daihatsu Cuore, old Alto, old Corolla, or similar compact cabin carriers.",
      must_include: [
        "Fuse box body, cover, terminals, and mounting points intact.",
        "Original plugs or at least 100-150 mm wiring tails if it is a used donor fuse box.",
        "Six usable fuse positions with clean rear terminals or pigtails.",
        "Fuse rating markings readable on cover or body where present.",
      ],
      bench_test: [
        "Insert and remove sample fuses to confirm tight terminal grip.",
        "Check continuity across each fuse position with a meter if possible.",
        "Confirm no terminal is loose, burned, corroded, or pushed back.",
        "Confirm the compact box fits the planned under-dash space, roughly no larger than 130 x 70 x 45 mm unless the electrician approves.",
      ],
      reject_if: [
        "Melted plastic, cracked body, missing cover, broken mounting tabs, or loose terminals.",
        "Cut-flush wires or missing plugs that make the feeds impossible to identify.",
        "Large engine-bay relay box, marine/RV stud block, fuse-cover-only listing, or loose fuse assortment.",
        "Single-bus universal block that cannot be split safely for the planned grouped inputs.",
      ],
      capture_before_leaving: [
        "Top, bottom, side, and cover photos.",
        "Close photos of terminals, plugs, wiring tails, and any rating marks.",
        "Seller name, phone number, shop location, price, and return terms.",
      ],
      price_guidance: {
        rule: "Quote the used OEM-style box and any new-quality alternative separately. Do not buy a damaged donor box just because it is cheap.",
      },
      decision_rule: "Buy only if the box is physically sound, terminals are tight, and the input/feed layout can be identified.",
      links: [
        scoutDocLink("docs/cabin-fuse-box-acquisition-20260503.md", "Cabin fuse-box acquisition"),
        scoutDocLink("docs/local-market-component-order-spec-20260504.md", "Exact local-market order spec"),
        scoutDocLink("deliverables/selling_site_images/images/junction_block.png", "Extracted blade-style junction block reference"),
        scoutDocLink("deliverables/selling_site_images/images/junction_block_cover.png", "Matching junction-block cover reference"),
      ],
    };
    const woodCribbingMarketSpec = {
      id: "hardwood_cribbing_market_scout",
      title: "Hardwood Cribbing Market Scout",
      scope: "Cut-list quote",
      quantity: "8 blocks plus 4 wedge chocks",
      plain_stall_request:
        "I need 8 dry hardwood blocks at 300 x 150 x 75 mm, plus 4 dry hardwood wedge chocks at 200 x 100 mm with 75 mm rear height and 25 mm blunt nose.",
      buy_target:
        "Dry dense solid hardwood only. Use sheesham/shisham, kikar/acacia, oak, ash, or similar. Leave it raw/unfinished.",
      must_include: [
        "8 straight blocks: 300 x 150 x 75 mm.",
        "4 blunt wedges: 200 x 100 mm, 75 mm rear, 25 mm nose.",
      ],
      bench_test: [
        "Put each piece on a flat floor; it must sit without rocking.",
        "Confirm dry solid hardwood and check the two sizes before loading.",
      ],
      reject_if: [
        "Wet/soft wood, plywood/MDF/chipboard, laminated board, cracks, oil, paint, or rocking faces.",
        "Wedge has a feather-edge nose instead of a blunt 25 mm nose.",
      ],
      capture_before_leaving: [
        "Photo of all 12 pieces together and one close size check.",
        "Merchant name, wood type, price, and pickup/delivery time.",
      ],
      price_guidance: {
        rule: "Quote as one cut set. Do not accept substitute board material.",
      },
      decision_rule: "Buy only dense dry solid hardwood pieces with flat bearing faces and stable square cuts.",
      links: [
        scoutDocLink("docs/suspension-wood-cribbing-merchant-spec.md", "Wood cribbing merchant spec"),
        scoutDocLink("data/manual/fabrication/suspension_wood_cribbing_rev_a/README.md", "Wood cribbing Rev A pack"),
        scoutDocLink("data/manual/fabrication/suspension_wood_cribbing_rev_a/j40_suspension_wood_cribbing_rev_a_dimension_sheet.pdf", "Wood cribbing dimension PDF"),
      ],
    };
    const toolbenchMarketSpec = {
      id: "toolbench_market_scout",
      title: "Toolbench / Workbench Scout",
      scope: "Local workshop support",
      quantity: "1 stable bench",
      plain_stall_request:
        "I need one stable workshop bench/toolbench for vehicle parts layout, pillar-drill work, and a bolt-down bench vice.",
      buy_target:
        "Steel-frame or heavy hardwood workbench with a flat top, minimum 1200 x 600 mm working surface, 850-950 mm working height, and enough structure to bolt down a vice and drill base.",
      must_include: [
        "Flat top with no rocking or twist.",
        "Rigid frame that does not sway when pushed from the side.",
        "Top thick enough, or reinforced enough, for a bolt-down vice and small pillar drill.",
        "Clear usable working surface; avoid decorative or light domestic furniture.",
      ],
      bench_test: [
        "Push the bench from each side and check for sway.",
        "Place it on a flat floor and confirm all feet sit stable.",
        "Confirm the top can accept drilled mounting holes for the vice and pillar drill.",
      ],
      reject_if: [
        "Thin folding table, domestic desk, loose particle-board top, or unstable legs.",
        "Top is badly warped, oily, cracked, or too weak to mount a vice.",
      ],
      capture_before_leaving: [
        "Photo of full bench, top thickness, frame, feet, and any mounting holes.",
        "Seller name, price, dimensions, and delivery option.",
      ],
      price_guidance: {
        rule: "Quote the bench separately from the vice and pillar drill.",
      },
      decision_rule: "Buy only if it is stable enough for drilling and vice work.",
    };
    const pillarDrillMarketSpec = {
      id: "pillar_drill_market_scout",
      title: "Pillar Drill / Bench Drill Scout",
      scope: "Local workshop support",
      quantity: "1 drill press",
      plain_stall_request:
        "I need one pillar drill or solid bench drill press for controlled workshop drilling, not a loose hand drill.",
      buy_target:
        "Floor pillar drill or solid bench drill press with 13 mm chuck minimum, locking table, depth stop, straight spindle with no visible wobble, and 220-240 V single-phase power if powered.",
      must_include: [
        "Chuck key or keyless chuck in working condition.",
        "Table height and angle lock working.",
        "Depth stop working.",
        "Belt cover and switch working where fitted.",
      ],
      bench_test: [
        "Run the drill before payment and watch the chuck/spindle for wobble.",
        "Lock the table and press down to confirm it does not slip.",
        "Open and close the chuck through its range.",
        "Check motor noise, belt condition, and available drill bits separately.",
      ],
      reject_if: [
        "Visible spindle runout, bent column, loose table lock, cracked casting, missing chuck key, or unsafe wiring.",
        "Seller will not test-run the drill.",
      ],
      capture_before_leaving: [
        "Photo/video of test run, chuck, spindle, table lock, motor plate, and switch.",
        "Seller name, price, voltage, chuck size, and whether bits are included.",
      ],
      price_guidance: {
        rule: "Quote drill and drill-bit set separately.",
      },
      decision_rule: "Buy only after a clean test-run and table/chuck checks.",
    };
    const benchViceMarketSpec = {
      id: "bench_vice_market_scout",
      title: "Bench Vice Scout",
      scope: "Local workshop support",
      quantity: "1 bolt-down vice",
      plain_stall_request:
        "I need one bolt-down bench vice for holding parts on the toolbench. This line is a vice, not a clamp.",
      buy_target:
        "Cast-iron or steel bench vice with 100-150 mm jaws, smooth screw action, intact mounting holes, clean or replaceable jaws, and no cracked casting.",
      must_include: [
        "Bolt-down base with at least two mounting holes.",
        "Jaws close squarely and grip evenly.",
        "Screw opens and closes smoothly through usable travel.",
        "Swivel base is acceptable only if the lock is firm.",
      ],
      bench_test: [
        "Open and close fully; check for binding and excessive jaw lift.",
        "Tighten on scrap metal or wood and check grip.",
        "Inspect casting, jaw screws, base lugs, and mounting holes.",
      ],
      reject_if: [
        "Cracked casting, broken base lug, stripped screw, badly chipped jaws, or missing mounting holes.",
        "Seller offers a C-clamp, spring clamp, or hand clamp instead of a bench vice.",
      ],
      capture_before_leaving: [
        "Photo of front, side, jaws, screw, base holes, and any brand/size marking.",
        "Seller name, price, jaw width, and mounting-bolt recommendation.",
      ],
      price_guidance: {
        rule: "Quote separately from the bench. Include mounting bolts if the seller has a matched set.",
      },
      decision_rule: "Buy only a solid bolt-down vice with sound jaws and body.",
    };
    const workshopSupportExactRows = [
      {
        id: "TOOL-BENCH-001",
        item: "Toolbench / workbench",
        route: "site_setup",
        state: "purchase_ready",
        spec: "Stable workbench for parts layout, pillar drill work, and bolt-down vice mounting.",
        qty: "1",
        dimension: "Minimum top 1200 x 600 mm; working height 850-950 mm",
        material: "Steel frame or heavy hardwood/reinforced top",
        sourceBasis: "data/manual/expenses.csv:tool_local_toolbench",
        action: "Scout local hardware/tools market and send dimension/frame photos before purchase.",
        reject: "Thin folding table, domestic desk, loose particle-board top, warped top, or unstable legs.",
      },
      {
        id: "TOOL-DRILL-001",
        item: "Pillar drill / bench drill press",
        route: "site_setup",
        state: "purchase_ready",
        spec: "Floor pillar drill or solid bench drill press; 13 mm chuck minimum; locking table; depth stop; straight spindle with no visible wobble.",
        qty: "1",
        dimension: "13 mm chuck minimum; 220-240 V single-phase if powered",
        material: "Cast/steel drill press with sound motor and table",
        sourceBasis: "data/manual/expenses.csv:tool_local_bench_drill",
        action: "Test-run before payment and photograph chuck, spindle, table lock, motor plate, and switch.",
        reject: "Visible runout, bent column, unsafe wiring, loose table lock, cracked casting, or no test-run.",
      },
      {
        id: "TOOL-VICE-001",
        item: "Bench vice / workshop vice",
        route: "site_setup",
        state: "purchase_ready",
        spec: "Bolt-down bench vice with smooth screw action, square-closing jaws, intact base lugs, and no cracked casting.",
        qty: "1",
        dimension: "100-150 mm jaw width",
        material: "Cast iron or steel vice body",
        sourceBasis: "data/manual/expenses.csv:tool_local_bench_vice",
        action: "Open/close fully, grip-test on scrap, and photograph jaws, screw, and mounting holes.",
        reject: "C-clamp, spring clamp, cracked vice body, stripped screw, broken base lug, or badly chipped jaws.",
      },
      {
        id: "SWC-BLOCK-001",
        item: "Rectangular hardwood cribbing block",
        route: "suspension_wood_cribbing_rev_a",
        state: "purchase_and_fabrication_ready",
        spec: "Dry hardwood block for the cribbing set.",
        qty: "8",
        dimension: "300 x 150 x 75 mm",
        material: "Dry dense hardwood",
        sourceBasis: "Wood cribbing merchant spec",
        action: "Ask timber merchant for the full 8 block + 4 wedge set.",
        reject: "Wet/soft/board material, cracks, rocking, or bad knots.",
      },
      {
        id: "SWC-CHOCK-001",
        item: "Hardwood wedge chock",
        route: "suspension_wood_cribbing_rev_a",
        state: "purchase_and_fabrication_ready",
        spec: "Dry hardwood blunt wedge chock.",
        qty: "4",
        dimension: "200 x 100 mm; 75 rear H; 25 nose H",
        material: "Same dry hardwood as the blocks",
        sourceBasis: "Wood cribbing merchant spec",
        action: "Ask for finished wedges, or buy 200 x 100 x 75 mm blanks for workshop tapering.",
        reject: "Feather nose, split taper, rocking base, or wet/soft wood.",
      },
    ];
    const fabricationExactSpecRows = [
      {
        id: "BM-SM",
        item: "Small circular body-mount cushion",
        partNumber: "bm_sm_body_mount_cushion_rev_a.dxf",
        route: "rubber_recreation_rev_a",
        state: "quote_first_article_ready",
        spec: "DXF quote/first article for small body-mount cushion; through cuts only on CUT/CUT_BORE/DRILL layers.",
        qty: "10",
        material: "Black EPDM or NR/SBR, Shore A 60 +/-5",
        sourceBasis: "data/manual/fabrication/rubber_recreation_rev_a/fabricator_cut_list.csv",
        action: "Quote/prototype first; production waits for one-piece vs split-stack decision.",
      },
      {
        id: "BM-LG",
        item: "Large circular body-mount cushion",
        partNumber: "bm_lg_body_mount_cushion_rev_a.dxf",
        route: "rubber_recreation_rev_a",
        state: "quote_first_article_ready",
        spec: "DXF quote/first article for large body-mount cushion; caliper-confirm station and final stack before batch.",
        qty: "2",
        material: "Black EPDM or NR/SBR, Shore A 60 +/-5",
        sourceBasis: "data/manual/fabrication/rubber_recreation_rev_a/fabricator_cut_list.csv",
      },
      {
        id: "BM-CUP-SM",
        item: "Small body-mount cup washer blank",
        partNumber: "bm_cup_small_seat_washer_rev_a.dxf",
        route: "rubber_recreation_rev_a",
        state: "quote_first_article_ready",
        spec: "Small cup washer blank; confirm cup reuse, dish depth, and forming method before batch.",
        qty: "10 working basis",
        material: "2.5-3.0 mm steel, zinc plated or epoxy primed after forming",
        sourceBasis: "data/manual/fabrication/rubber_recreation_rev_a/fabricator_cut_list.csv",
      },
      {
        id: "BM-CUP-LG",
        item: "Large body-mount cup washer blank",
        partNumber: "bm_cup_large_seat_washer_rev_a.dxf",
        route: "rubber_recreation_rev_a",
        state: "quote_first_article_ready",
        spec: "Large cup washer blank; confirm cup reuse, dish depth, and forming method before batch.",
        qty: "2 working basis",
        material: "2.5-3.0 mm steel, zinc plated or epoxy primed after forming",
        sourceBasis: "data/manual/fabrication/rubber_recreation_rev_a/fabricator_cut_list.csv",
      },
      {
        id: "FS-OVAL",
        item: "Two-hole oval front-support isolator pad",
        partNumber: "fs_oval_front_support_pad_rev_a.dxf",
        route: "rubber_recreation_rev_a",
        state: "quote_first_article_ready",
        spec: "Oval front-support pad; caliper-confirm holes and insert before batch.",
        qty: "2 matched pieces",
        material: "Black EPDM or NR/SBR, Shore A 60 +/-5; reuse/bond steel insert if present",
        sourceBasis: "data/manual/fabrication/rubber_recreation_rev_a/fabricator_cut_list.csv",
      },
      {
        id: "FS-STRIP-L",
        item: "Left front-support strip template blank",
        partNumber: "fs_strip_left_template_blank_rev_a.dxf",
        route: "rubber_recreation_rev_a",
        state: "template_required",
        spec: "Quote/template blank only; trace physical left strip rubber and carrier before production cutting.",
        qty: "1",
        material: "8 mm base / 14 mm raised-load EPDM or NR/SBR strip, Shore A 60 +/-5",
        sourceBasis: "data/manual/fabrication/rubber_recreation_rev_a/fabricator_cut_list.csv",
        reject: "Do not cut final production from this blank without the physical trace.",
      },
      {
        id: "FS-STRIP-R",
        item: "Right front-support strip template blank",
        partNumber: "fs_strip_right_template_blank_rev_a.dxf",
        route: "rubber_recreation_rev_a",
        state: "template_required",
        spec: "Quote/template blank only; trace physical right strip rubber and carrier before production cutting.",
        qty: "1",
        material: "8 mm base / 14 mm raised-load EPDM or NR/SBR strip, Shore A 60 +/-5",
        sourceBasis: "data/manual/fabrication/rubber_recreation_rev_a/fabricator_cut_list.csv",
        reject: "Do not cut final production from this blank without the physical trace.",
      },
      {
        id: "MIDI5-PLATE-001",
        item: "MIDI 5-way structural mount plate",
        partNumber: "midi5_mount_plate_rev_c.dxf",
        route: "midi5_plate_mount_rev_c",
        state: "current_release",
        spec: "Open plate-mount arrangement for five linked MIDI fuse holders.",
        qty: "1",
        material: "3.0 mm 5052-H32 aluminium",
        sourceBasis: "data/manual/fabrication/midi5_plate_mount_rev_c/README.md",
        action: "Use 10-12 mm spacers and add cable P-clips after final routing.",
      },
      {
        id: "MIDI5-SUBPLATE-001",
        item: "MIDI 5-way non-conductive holder subplate",
        partNumber: "midi5_holder_subplate_rev_c.dxf",
        route: "midi5_plate_mount_rev_c",
        state: "current_release",
        spec: "Non-conductive board that carries the five linked MIDI holders.",
        qty: "1",
        material: "5.0 mm HDPE, ABS, G10, or phenolic",
        sourceBasis: "data/manual/fabrication/midi5_plate_mount_rev_c/README.md",
      },
      {
        id: "RELAY-CARRIER-001",
        item: "Relay box carrier",
        partNumber: "relay_carrier_rev_c.dxf",
        route: "relay_mount_rev_c",
        state: "current_release",
        spec: "Structural carrier for DAIER prewired 10-way relay/fuse box.",
        qty: "1",
        material: "3.0 mm 5052-H32 aluminium",
        sourceBasis: "data/manual/fabrication/relay_mount_rev_c/README.md",
      },
      {
        id: "RELAY-GUARD-001",
        item: "Relay rear guard",
        partNumber: "relay_rear_guard_rev_c.dxf",
        route: "relay_mount_rev_c",
        state: "current_release",
        spec: "Rear guard behind the relay box on spacers; keep bottom loom opening downward.",
        qty: "1",
        material: "3.0 mm ABS, HDPE, or polypropylene",
        sourceBasis: "data/manual/fabrication/relay_mount_rev_c/README.md",
        reject: "Do not fully seal the relay-box rear.",
      },
    ];
    const fabricationSupportMarketSpec = {
      id: "fabrication_support_market_scout",
      title: "3D Print + Workshop Support Scout",
      scope: "Quote only",
      quantity: "Quote per item or per print file",
      plain_stall_request:
        "I need local quotes for non-metal 3D printed check-fit pieces, guards, templates, spacers, or prototypes from supplied CAD/STL/DXF files. Metal brackets and plate fabrication are not part of this quote.",
      buy_target:
        "Use a print service or workshop that can quote material, lead time, finish, tolerance, and per-piece price clearly before printing.",
      must_include: [
        "Material options such as PETG, ABS, nylon, or PLA clearly named.",
        "Per-piece price, setup charge if any, and lead time.",
        "Basic tolerance and finish expectation before printing.",
        "Agreement that these are check-fit/prototype pieces, not final load-bearing metal parts.",
      ],
      bench_test: [
        "Ask the shop to inspect the file and confirm scale before quoting.",
        "Confirm units are millimeters before printing.",
        "For a first article, print one sample before ordering multiples.",
      ],
      reject_if: [
        "Shop cannot identify material, scale, print orientation, or lead time.",
        "Quote treats prototype plastic as a final structural metal replacement.",
        "Price is given without seeing the file or understanding quantity.",
      ],
      capture_before_leaving: [
        "Shop name, phone number, location, material, lead time, and price.",
        "Photo or screenshot of the file name quoted.",
        "Photo of sample material or sample print quality if available.",
      ],
      price_guidance: {
        rule: "Quote first. Print only after the file, material, quantity, and first-article need are clear.",
      },
      decision_rule: "Use the service only for non-metal check-fit or prototype parts unless a separate approved final-part spec exists.",
      links: [
        scoutDocLink("docs/fabrication-handoff-index.md", "Fabrication handoff index"),
        scoutDocLink("docs/rubber-recreation-fabrication-spec-20260502.md", "Rubber fabrication spec"),
      ],
    };
    const brakeFallbackSpec = {
      id: "brake_booster_servo_44610_60050_market_scout",
      title: "Brake Booster / Servo Market Scout",
      scope: "Quote and sample-match only",
      quantity: "1 booster assembly",
      plain_stall_request:
        "Need a brake servo or brake booster for a 1978 Toyota Land Cruiser J40 with front disc brakes and rear drum brakes. Primary target part number is Toyota 44610-60050. Quote only until the old booster is sample-matched and vacuum-tested.",
      buy_target:
        "Primary target is the J40/FJ40/BJ40 dual-diaphragm booster family, Toyota 44610-60050. Quote 44610-60100 or 44610-60180 only if the shop proves all mounting, pushrod, clevis, master-cylinder seat, check valve, and depth dimensions match the old unit.",
      must_include: [
        "Booster shell with intact mounting studs and no welded shell repair.",
        "Correct pedal pushrod and clevis, or confirmed reuse of the old clevis.",
        "Correct master-cylinder mounting face and pushrod depth.",
        "Vacuum check valve and grommet included or quoted separately.",
      ],
      bench_test: [
        "Vacuum-test before payment; it must hold vacuum without hiss or leakdown.",
        "Check pushrod movement and return.",
        "Inspect for brake-fluid contamination inside the master-cylinder side.",
        "Compare old and replacement booster side by side if the old sample is available.",
      ],
      reject_if: [
        "Single/drum booster such as 44610-60040 is offered as a direct replacement.",
        "Used unit cannot be vacuum-tested before payment.",
        "Firewall studs, master studs, pushrod, clevis, check valve, or shell depth do not match.",
        "Universal booster requires cutting, welding, or unproven brake-line changes.",
      ],
      capture_before_leaving: [
        "Photos of front, rear, side depth, studs, master face, pushrod, clevis, and check valve.",
        "Part number, brand label, donor claim, or remanufacturer label.",
        "Seller name, phone number, shop location, price, and return/test terms.",
      ],
      price_guidance: {
        rule: "Record local PKR quotes first. Do not buy used or reman stock unless sample-match and vacuum tests pass.",
      },
      decision_rule: "Buy locally only after sample match and vacuum test pass.",
    };

    return [
      {
        id: "eps",
        title: "EPS",
        description: "Only the 2005-2011 Vitz/Yaris SCP90/NCP90 complete EPS kit is a buy candidate.",
        chips: ["SCP90/NCP90 only", "Bench-test before payment", "Complete matched kit"],
        parts: epsParts,
        marketSpecs: attachScoutImage(
          dedupeScoutRows(epsMarketSpecs),
          epsParts,
          scoutReferenceImage("../../deliverables/selling_site_images/images/reference_catalog/eps_column.jpg", "Vitz/Yaris XP90 EPS column set reference image", "eps_column")
        ),
      },
      {
        id: "brake-booster",
        title: "Brake Booster",
        description: "Quote the correct J40 brake servo only; sample-match and vacuum-test before payment.",
        chips: ["44610-60050 target", "Vacuum-test", "Quote first"],
        parts: brakeBoosterParts,
        marketSpecs: attachScoutImage(
          fallbackMarketSpec(brakeMarketSpecs, brakeFallbackSpec),
          brakeBoosterParts,
          scoutReferenceImage("../../deliverables/selling_site_images/images/reference_catalog/brake_booster.jpg", "44610-60050 dual-diaphragm brake booster reference image", "brake_booster")
        ),
      },
      {
        id: "pipes",
        title: "Pipes + Hoses",
        description: "Use the exact order sheet for every hose, pipe, hard line, clip, and hydraulic assembly.",
        chips: ["23 HLS lines", "21 release specs", "No generic hydraulic hose"],
        parts: pipeParts,
        marketSpecs: attachScoutImage(
          [hoseMarketSpec],
          pipeParts,
          scoutReferenceImage("../../deliverables/selling_site_images/images/reference_catalog/radiator_hose.jpg", "Automotive hose reference image", "radiator_hose")
        ),
        docLinks: [
          scoutDocLink("docs/hose-local-scout-handoff.md", "Hose local scout handoff"),
          scoutDocLink("docs/local-market-component-order-spec-20260504.md", "Exact local-market component order spec"),
          scoutDocLink("docs/replacement-pipes-workstream.md", "Replacement pipes workstream"),
        ],
        localMarketOrderRows: (data.local_market_order_sheets && data.local_market_order_sheets.hose) || [],
        exactSpecRows: scoutOrderSpecRows((replacementPipesWorkstream && replacementPipesWorkstream.replacement_pipe_order_release_specs) || []),
      },
      {
        id: "rubbers",
        title: "Rubbers",
        description: "Use the exact rubber requirement list and controlled body-mount release gates.",
        chips: ["9 rubber requirements", "Fabricate or exact-kit only", "No salvage rubber"],
        parts: rubberParts,
        marketSpecs: attachScoutImage(
          [rubberMarketSpec],
          rubberParts,
          scoutReferenceImage("../../deliverables/selling_site_images/images/reference_catalog/body_mount_kit.jpg", "Body mount rubber reference image", "body_mount_kit")
        ),
        docLinks: [
          scoutDocLink("docs/rubber-ordering-spec-20260502.md", "Rubber ordering spec"),
          scoutDocLink("docs/local-market-component-order-spec-20260504.md", "Exact local-market component order spec"),
          scoutDocLink("docs/body-mount-order-release-plan-20260502.md", "Body-mount order release plan"),
        ],
        exactSpecRows: scoutOrderSpecRows((chassisRubbersWorkstream && chassisRubbersWorkstream.chassis_rubber_requirements) || []),
      },
      {
        id: "additional-fuse-box",
        title: "Additional Fuse Box",
        description: "Compact OEM-style cabin fuse box with sound terminals and identifiable feeds.",
        chips: ["Compact OEM style", "One add-on box", "Three isolated input groups"],
        parts: fuseBoxParts,
        marketSpecs: attachScoutImage(
          [fuseBoxMarketSpec],
          fuseBoxParts,
          scoutReferenceImage("../../deliverables/selling_site_images/images/manual_overrides/compact_cabin_fuse_box_user_photo_20260504.png", "User-supplied compact old-OEM fuse box reference", "compact_cabin_fuse_box_user_photo_20260504")
        ),
      },
      {
        id: "workshop-fabrication-support",
        title: "Workshop Support",
        description: "Simple quote cards for support items the market scout can source locally.",
        chips: ["Hardwood cribbing", "Bench/pillar drill", "Support tools"],
        parts: workshopSupportParts,
        marketSpecs: [
          ...attachScoutImage(
            [woodCribbingMarketSpec],
            filterScoutRows(workshopSupportParts, { terms: ["cribbing", "hardwood", "wedge"] }),
            scoutReferenceImage("../../deliverables/selling_site_images/images/manual_overrides/suspension_hardwood_cribbing_cut_set_flat_lay.jpg", "Hardwood cribbing cut-set reference image", "hardwood_cribbing")
          ),
          ...attachScoutImage(
            [toolbenchMarketSpec],
            filterScoutRows(workshopSupportParts, { entryIds: ["tool_local_toolbench"], terms: ["toolbench", "workbench"] }),
            scoutReferenceImage("../../deliverables/selling_site_images/images/reference_catalog/toolbench.jpg", "Toolbench/workbench reference image", "toolbench")
          ),
          ...attachScoutImage(
            [pillarDrillMarketSpec],
            filterScoutRows(workshopSupportParts, { entryIds: ["tool_local_bench_drill"], terms: ["pillar drill", "bench drill", "drill press"] }),
            scoutReferenceImage("../../deliverables/selling_site_images/images/reference_catalog/bench_drill.jpg", "Pillar drill / bench drill reference image", "bench_drill")
          ),
          ...attachScoutImage(
            [benchViceMarketSpec],
            filterScoutRows(workshopSupportParts, { entryIds: ["tool_local_bench_vice"], terms: ["bench vice", "workshop vice", "vise"] }),
            scoutReferenceImage("../../deliverables/selling_site_images/images/reference_catalog/bench_vice.jpg", "Bolt-down bench vice reference image", "bench_vice")
          ),
        ],
        docLinks: [
          scoutDocLink("docs/local-market-procurement-workstream.md", "Local market procurement workstream"),
          scoutDocLink("docs/suspension-wood-cribbing-merchant-spec.md", "Wood cribbing merchant spec"),
          scoutDocLink("data/manual/fabrication/suspension_wood_cribbing_rev_a/fabricator_cut_list.csv", "Wood cribbing cut list"),
        ],
        exactSpecRows: workshopSupportExactRows,
      },
      {
        id: "fabrication",
        title: "Fabrication",
        description: "Controlled shop send-out packages with itemized files, release position, and exact fabrication specs.",
        chips: ["DXF/SVG/PDF packages", "Quote first article", "Do not send superseded files"],
        parts: fabricationParts,
        marketSpecs: [
          ...attachScoutImage(
            [fabricationSupportMarketSpec],
            fabricationParts,
            scoutReferenceImage("../../deliverables/selling_site_images/images/reference_catalog/generic_part.jpg", "Prototype part reference image", "generic_part")
          ),
        ],
        docLinks: [
          scoutDocLink("docs/fabrication-handoff-index.md", "Fabrication handoff index"),
          scoutDocLink("docs/rubber-recreation-fabrication-spec-20260502.md", "Rubber recreation fabrication spec"),
        ],
        exactSpecRows: fabricationExactSpecRows,
        fabricationPackages: (fabricationWorkstream && fabricationWorkstream.fabrication_packages) || [],
      },
    ];
  }

  function renderScoutField(label, value) {
    const text = cleanString(value);
    if (!text) {
      return "";
    }
    return `<div><strong>${escapeHtml(label)}:</strong> ${escapeHtml(text)}</div>`;
  }

  function renderScoutLocalMarketOrderTable(rows) {
    const sourceRows = Array.isArray(rows) ? rows : [];
    if (!sourceRows.length) {
      return "";
    }
    return `
      <article class="card">
        <div class="detail-header">
          <h3>Local Market Order Sheet</h3>
          ${chip(`${sourceRows.length} exact lines`)}
        </div>
        <div class="table-wrap">
          <table class="scout-market-order-table">
            <thead>
              <tr>
                <th>Image</th>
                <th>Line</th>
                <th>Shop Lane</th>
                <th>Exact Order Text</th>
                <th>Qty / Size</th>
                <th>Material / Fittings</th>
                <th>Reject / Install Check</th>
              </tr>
            </thead>
            <tbody>
              ${sourceRows
                .map(
                  (row) => `
                    <tr>
                      ${renderInventoryImageCell({ item: row.item, image: row.image || scoutComponentImage(row) }, row.item || "Order line image")}
                      <td class="scout-line-cell">
                        <strong>${escapeHtml(row.order_id || "-")}</strong>
                        <div class="small-muted">${escapeHtml(row.item || "")}</div>
                        ${statusChip(row.order_state || "open")}
                      </td>
                      <td>${escapeHtml(formatToken(row.shop_lane || "-"))}</td>
                      <td class="scout-spec-cell">${escapeHtml(row.order_text || "-")}</td>
                      <td class="scout-meta-cell">
                        ${renderScoutField("Qty", row.qty)}
                        ${renderScoutField("Buy length", row.buy_length_mm)}
                        ${renderScoutField("Diameter", row.diameter_spec)}
                      </td>
                      <td class="scout-meta-cell">
                        ${renderScoutField("Material", row.material_spec)}
                        ${renderScoutField("Clamp/fitting", row.clamp_or_fitting_spec)}
                        ${renderScoutField("Basis", row.source_basis)}
                      </td>
                      <td class="scout-notes-cell">
                        ${renderScoutField("Reject if", row.hard_reject)}
                        ${renderScoutField("Install check", row.final_install_check)}
                      </td>
                    </tr>
                  `
                )
                .join("")}
            </tbody>
          </table>
        </div>
      </article>
    `;
  }

  function renderScoutPartsTable(rows) {
    const sourceRows = Array.isArray(rows) ? rows : [];
    return `
      <article class="card">
        <div class="detail-header">
          <h3>Scout Part Rows</h3>
          ${chip(`${sourceRows.length} rows`)}
        </div>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Image</th>
                <th>Item</th>
                <th>Workstream</th>
                <th>Status</th>
                <th>Supplier</th>
                <th>Cost</th>
                <th>Notes</th>
              </tr>
            </thead>
            <tbody>
              ${
                sourceRows.length
                  ? sourceRows
                      .map(
                        (row) => `
                          <tr>
                            ${renderInventoryImageCell(row, row.item || "Scout row image")}
                            <td>${renderItemButton(row)}</td>
                            <td>${escapeHtml(formatToken(row.workstream || "-"))}</td>
                            <td>
                              ${statusChip(row.procurement_stage || row.status || "open")}
                              <div class="small-muted">${escapeHtml(formatToken(row.payment_status || ""))}${row.delivery_status ? ` / ${escapeHtml(formatToken(row.delivery_status))}` : ""}</div>
                            </td>
                            <td>${tableSupplierCell(row)}</td>
                            <td>${tableCostCell(row)}</td>
                            <td class="scout-notes-cell">${escapeHtml(row.notes || "-")}</td>
                          </tr>
                        `
                      )
                      .join("")
                  : '<tr><td colspan="7">No scout part rows matched this category.</td></tr>'
              }
            </tbody>
          </table>
        </div>
      </article>
    `;
  }

  function renderScoutOrderSpecTable(rows) {
    const sourceRows = Array.isArray(rows) ? rows : [];
    if (!sourceRows.length) {
      return "";
    }
    return `
      <article class="card">
        <div class="detail-header">
          <h3>Exact Release Specs</h3>
          ${chip(`${sourceRows.length} rows`)}
        </div>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Image</th>
                <th>Line</th>
                <th>Route / State</th>
                <th>Shop Ask</th>
                <th>Qty / Size</th>
                <th>Check / Reject</th>
              </tr>
            </thead>
            <tbody>
              ${sourceRows
                .map(
                  (row) => `
                    <tr>
                      ${renderInventoryImageCell({ item: row.item, image: row.image || scoutComponentImage(row) }, row.item || "Spec row image")}
                      <td>
                        <strong>${escapeHtml(row.id || "-")}</strong>
                        <div class="small-muted">${escapeHtml(row.item || "")}</div>
                        ${row.partNumber ? `<div class="small-muted">${escapeHtml(row.partNumber)}</div>` : ""}
                      </td>
                      <td>
                        ${escapeHtml(formatToken(row.route || "-"))}
                        <div>${statusChip(row.state || "release_hold")}</div>
                      </td>
                      <td class="scout-spec-cell">${escapeHtml(row.spec || "-")}</td>
                      <td class="scout-meta-cell">
                        ${renderScoutField("Qty", row.qty)}
                        ${renderScoutField("Dimensions", row.dimension)}
                        ${renderScoutField("Material", row.material)}
                        ${renderScoutField("Source", row.sourceBasis)}
                      </td>
                      <td class="scout-notes-cell">
                        ${renderScoutField("Check", row.action)}
                        ${renderScoutField("Reject if", row.reject)}
                        ${renderScoutField("Notes", row.notes)}
                      </td>
                    </tr>
                  `
                )
                .join("")}
            </tbody>
          </table>
        </div>
      </article>
    `;
  }

  function renderScoutSourceLinksTable(rows) {
    const sourceRows = Array.isArray(rows) ? rows : [];
    if (!sourceRows.length) {
      return "";
    }
    return `
      <article class="card">
        <div class="detail-header">
          <h3>Source Links</h3>
          ${chip(`${sourceRows.length} rows`)}
        </div>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>System</th>
                <th>Item</th>
                <th>Source</th>
                <th>Stage / Decision</th>
                <th>Cost</th>
                <th>Links</th>
                <th>Notes</th>
              </tr>
            </thead>
            <tbody>
              ${sourceRows
                .map(
                  (row) => `
                    <tr>
                      <td>${escapeHtml(formatToken(row.system || "-"))}</td>
                      <td>${escapeHtml(row.item || "-")}</td>
                      <td>${escapeHtml(formatToken(row.source_sheet || "-"))}</td>
                      <td>${escapeHtml(formatToken(row.stage || row.decision || "-"))}</td>
                      <td>${escapeHtml(row.cost || "-")}</td>
                      <td>${renderLinksCell(row)}</td>
                      <td class="scout-notes-cell">${escapeHtml(row.notes || "-")}</td>
                    </tr>
                  `
                )
                .join("")}
            </tbody>
          </table>
        </div>
      </article>
    `;
  }

  function renderScoutDocLinks(links) {
    const sourceLinks = Array.isArray(links) ? links : [];
    if (!sourceLinks.length) {
      return "";
    }
    return `
      <article class="card scout-doc-card">
        <h3>Reference Files</h3>
        ${renderLinksCell({ links: sourceLinks })}
      </article>
    `;
  }

  function renderScoutCategory(category) {
    const chips = Array.isArray(category.chips) ? category.chips : [];
    return `
      <section class="scout-category" id="scout-${escapeHtml(category.id || "")}">
        <article class="card scout-category-header">
          <div class="detail-header">
            <h2>${escapeHtml(category.title || "Scout")}</h2>
            <div class="chip-row">
              ${chip(`${(category.marketSpecs || []).length} scout cards`)}
            </div>
          </div>
          <p>${escapeHtml(category.description || "")}</p>
          <div class="chip-row">
            ${chips.map((item) => chip(item)).join("")}
          </div>
        </article>
        ${renderMarketSpecCards(category.marketSpecs)}
        ${renderScoutDocLinks(category.docLinks)}
        ${renderScoutLocalMarketOrderTable(category.localMarketOrderRows)}
        ${renderScoutOrderSpecTable(category.exactSpecRows)}
        ${renderFabricationPackages(category.fabricationPackages)}
      </section>
    `;
  }

  function renderScout() {
    const categories = buildScoutCategories();
    root.innerHTML = `
      <h2 class="section-title">Scout</h2>
      <p class="section-subtitle">Simple market-facing cards for the person visiting shops: what to ask for, what must come with it, when to reject, and what photos or details to send back.</p>
      <div class="chip-row scout-jump-row">
        ${categories.map((category) => `<button class="chip chip-button" data-scroll-reference-section="scout-${escapeHtml(category.id)}" type="button">${escapeHtml(category.title)}</button>`).join("")}
      </div>
      ${categories.map(renderScoutCategory).join("")}
    `;
  }

  function renderElectricalCell(row, column) {
    const value = cleanString(row && row[column.key]);
    if (column.kind === "status") {
      return statusChip(value || "unknown");
    }
    if (column.kind === "token") {
      return escapeHtml(formatToken(value || "-"));
    }
    return escapeHtml(value || "-");
  }

  function renderElectricalTable(sectionTitle, columns, rows) {
    const sourceRows = Array.isArray(rows) ? rows : [];
    return `
      <article class="card">
        <h4>${escapeHtml(sectionTitle)}</h4>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                ${columns.map((column) => `<th>${escapeHtml(column.label)}</th>`).join("")}
              </tr>
            </thead>
            <tbody>
              ${
                sourceRows.length
                  ? sourceRows
                      .map(
                        (row) => `
                          <tr>
                            ${columns.map((column) => `<td>${renderElectricalCell(row, column)}</td>`).join("")}
                          </tr>
                        `
                      )
                      .join("")
                  : `<tr><td colspan="${columns.length}">No rows mapped.</td></tr>`
              }
            </tbody>
          </table>
        </div>
      </article>
    `;
  }

  function renderElectricalSpecLayout(spec) {
    if (!spec || typeof spec !== "object") {
      return "";
    }

    const layoutTemplates = Array.isArray(spec.layout_templates) ? spec.layout_templates : [];
    const sourceRefs = Array.isArray(spec.source_refs) ? spec.source_refs : [];
    const wiringRows = Array.isArray(spec.wiring_progress_tracker) ? spec.wiring_progress_tracker : [];
    const gateRows = Array.isArray(spec.minimum_electrical_gate) ? spec.minimum_electrical_gate : [];
    const lockedRows = Array.isArray(spec.locked_as_built_standards) ? spec.locked_as_built_standards : [];
    const relayRows = Array.isArray(spec.relay_quick_lookup) ? spec.relay_quick_lookup : [];
    const connectorRows = Array.isArray(spec.connector_quick_lookup) ? spec.connector_quick_lookup : [];
    const loomRows = Array.isArray(spec.loom_quick_lookup) ? spec.loom_quick_lookup : [];

    return `
      <article class="card">
        <div class="detail-header">
          <h3>Electrical Specs and Layout</h3>
          ${spec.scope ? chip(`Scope: ${formatToken(spec.scope)}`) : ""}
        </div>
        <p><strong>Reference:</strong> ${escapeHtml(spec.title || "Electrical master tracker")}</p>
        <p><strong>Last Updated:</strong> ${escapeHtml(spec.last_updated || "Unknown")}</p>
        <p><strong>Purpose:</strong> ${escapeHtml(spec.purpose || "Electrical build progress and lookup references.")}</p>
        ${
          sourceRefs.length
            ? `<p class="small-muted"><strong>Source Files:</strong> ${escapeHtml(sourceRefs.join(", "))}</p>`
            : ""
        }
        ${
          layoutTemplates.length
            ? `<p><strong>Layout Templates:</strong> ${escapeHtml(layoutTemplates.map((row) => cleanString(row && row.label)).filter(Boolean).join(", "))}</p>`
            : '<p class="small-muted">No layout template labels found.</p>'
        }
      </article>

      ${renderElectricalTable(
        "Wiring Progress Tracker",
        [
          { key: "priority", label: "Priority", kind: "token" },
          { key: "area", label: "Area" },
          { key: "task", label: "Task" },
          { key: "status", label: "Status", kind: "status" },
          { key: "next_action", label: "Next Action" },
        ],
        wiringRows
      )}

      ${renderElectricalTable(
        "Minimum Electrical Gate",
        [
          { key: "step", label: "Step", kind: "token" },
          { key: "action", label: "Action" },
          { key: "target_stage", label: "Target Stage" },
          { key: "status", label: "Status", kind: "status" },
        ],
        gateRows
      )}

      <div class="split">
        ${renderElectricalTable(
          "Locked As-Built Standards",
          [
            { key: "standard", label: "Standard" },
            { key: "decision", label: "Decision" },
            { key: "revisit_trigger", label: "Revisit Trigger" },
          ],
          lockedRows
        )}
        ${renderElectricalTable(
          "Loom Quick Lookup",
          [
            { key: "loom_id", label: "Loom" },
            { key: "loom_name", label: "Name" },
            { key: "build_makeup", label: "Build Makeup" },
            { key: "status", label: "Status", kind: "token" },
          ],
          loomRows
        )}
      </div>

      <div class="split">
        ${renderElectricalTable(
          "Relay Quick Lookup",
          [
            { key: "relay_pos", label: "Relay" },
            { key: "function", label: "Function" },
            { key: "relay_colour", label: "Color" },
            { key: "power_code", label: "Power Code" },
            { key: "implementation_status", label: "Implementation", kind: "token" },
          ],
          relayRows
        )}
        ${renderElectricalTable(
          "Connector Quick Lookup",
          [
            { key: "connector", label: "Connector" },
            { key: "type", label: "Type" },
            { key: "loom_or_branch", label: "Loom / Branch" },
            { key: "terminated_circuits", label: "Circuits" },
            { key: "status", label: "Status", kind: "token" },
          ],
          connectorRows
        )}
      </div>
    `;
  }

  function renderWhatsappOverviewSection(summary) {
    const selectedChatsSummary = toNumber(summary.whatsapp_j40_selected_chats);
    const mediaItemsSummary = toNumber(summary.whatsapp_j40_media_items);
    const whatsapp = data.whatsapp_j40 || {};
    const selectedChats = Array.isArray(whatsapp.selected_chats) ? whatsapp.selected_chats : [];
    const recentMedia = (Array.isArray(whatsapp.recent_media) ? whatsapp.recent_media : []).filter(
      (row) => !isPhotoDeletedById(row && row.media_id)
    );
    const mediaCountsByType = Array.isArray(whatsapp.media_counts_by_type) ? whatsapp.media_counts_by_type : [];
    const mediaCountsByProfile = Array.isArray(whatsapp.media_counts_by_profile) ? whatsapp.media_counts_by_profile : [];

    if (!selectedChatsSummary && !mediaItemsSummary && !selectedChats.length && !recentMedia.length) {
      return "";
    }

    const sortedTypeCounts = mediaCountsByType
      .slice()
      .sort((left, right) => toNumber(right.count) - toNumber(left.count));
    const sortedProfileCounts = mediaCountsByProfile
      .slice()
      .sort((left, right) => toNumber(right.count) - toNumber(left.count));

    return `
      <h2 class="section-title">WhatsApp J40 Intake</h2>
      <p class="section-subtitle">Selected J40 chat candidates, import status, and latest imported attachments.</p>
      <section class="cards-grid">
        <article class="card">
          <div class="detail-header">
            <h3>Selected Chats</h3>
            ${chip(`${selectedChatsSummary || selectedChats.length} chats`)}
          </div>
          ${
            sortedTypeCounts.length
              ? `<p class="small-muted"><strong>Media by Type:</strong> ${sortedTypeCounts
                  .map((row) => `${formatToken(row.media_type)} ${toNumber(row.count)}`)
                  .join(" · ")}</p>`
              : '<p class="small-muted">No media type counts available.</p>'
          }
          ${
            sortedProfileCounts.length
              ? `<p class="small-muted"><strong>Media by Profile:</strong> ${sortedProfileCounts
                  .map((row) => `${cleanString(row.source_profile)} ${toNumber(row.count)}`)
                  .join(" · ")}</p>`
              : ""
          }
          <div class="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Chat</th>
                  <th>Profile</th>
                  <th>Score</th>
                  <th>Messages</th>
                  <th>Media</th>
                  <th>Fetch Status</th>
                </tr>
              </thead>
              <tbody>
                ${
                  selectedChats.length
                    ? selectedChats
                        .slice(0, 20)
                        .map((row) => {
                          const fetchStatus = cleanString(row.messages_fetched || "unknown");
                          const statusLabel =
                            fetchStatus === "fallback_archive"
                              ? "archive_fallback"
                              : fetchStatus === "true"
                                ? "fetched"
                                : fetchStatus === "false"
                                  ? "blocked"
                                  : fetchStatus;
                          const fetchError = truncateText(row.messages_fetch_error || "", 95);
                          return `
                            <tr>
                              <td>${escapeHtml(cleanString(row.chat_name) || cleanString(row.chat_id) || "Unknown chat")}</td>
                              <td>${escapeHtml(cleanString(row.profile_server) || "-")}</td>
                              <td>${escapeHtml(cleanString(row.relevance_score) || "0")}</td>
                              <td>${escapeHtml(cleanString(row.messages_count) || "0")}</td>
                              <td>${escapeHtml(cleanString(row.media_count) || "0")}</td>
                              <td>
                                ${statusChip(statusLabel)}
                                ${fetchError ? `<p class="small-muted">${escapeHtml(fetchError)}</p>` : ""}
                              </td>
                            </tr>
                          `;
                        })
                        .join("")
                    : '<tr><td colspan="6">No selected WhatsApp chats mapped.</td></tr>'
                }
              </tbody>
            </table>
          </div>
        </article>

        <article class="card">
          <div class="detail-header">
            <h3>Recent Imported Media</h3>
            ${chip(`${mediaItemsSummary || recentMedia.length} items`)}
          </div>
          <div class="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Timestamp</th>
                  <th>Type</th>
                  <th>Chat</th>
                  <th>File</th>
                  <th>Source</th>
                </tr>
              </thead>
              <tbody>
                ${
                  recentMedia.length
                    ? recentMedia
                        .slice(0, 24)
                        .map((row) => `
                          <tr>
                            <td>${escapeHtml(formatDateTime(row.timestamp || ""))}</td>
                            <td>${escapeHtml(formatToken(row.media_type || ""))}</td>
                            <td>${escapeHtml(cleanString(row.chat_name) || "-")}</td>
                            <td>${escapeHtml(cleanString(row.file_name) || "-")}</td>
                            <td>${escapeHtml(cleanString(row.source_profile) || "-")}</td>
                          </tr>
                        `)
                        .join("")
                    : '<tr><td colspan="5">No WhatsApp media has been imported yet.</td></tr>'
                }
              </tbody>
            </table>
          </div>
        </article>
      </section>
    `;
  }

  function renderOverview() {
    const summary = data.summary || {};
    const workstreams = data.workstreams || [];
    const parts = data.parts || {};
    const projectSteps = data.project_steps || [];
    const urgentActions = parts.urgent_actions || [];

    root.innerHTML = `
      <section class="metrics-grid">
        <article class="card">
          <p class="metric-value">${escapeHtml(summary.workstreams_in_scope ?? 0)}</p>
          <p class="metric-label">Workstreams in Scope</p>
        </article>
        <article class="card">
          <p class="metric-value">${escapeHtml(summary.workstreams_active ?? 0)}</p>
          <p class="metric-label">Active Workstreams</p>
        </article>
        <article class="card">
          <p class="metric-value">${escapeHtml(summary.parts_open_rows ?? 0)}</p>
          <p class="metric-label">Open Parts Rows</p>
        </article>
        <article class="card">
          <p class="metric-value">${escapeHtml(summary.parts_ordered_pending_delivery ?? 0)}</p>
          <p class="metric-label">Orders Awaiting Delivery</p>
        </article>
        <article class="card">
          <p class="metric-value">${escapeHtml(summary.capture_data_tasks_now ?? 0)}</p>
          <p class="metric-label">Photo / Data Tasks Now</p>
        </article>
        <article class="card">
          <p class="metric-value">${escapeHtml(summary.workstream_evidence_images ?? 0)}</p>
          <p class="metric-label">Mapped Workstream Evidence Media</p>
        </article>
        <article class="card">
          <p class="metric-value">${escapeHtml(summary.supply_rows_tracked ?? 0)}</p>
          <p class="metric-label">Tracked Tool/Substance/Part Rows</p>
        </article>
        <article class="card">
          <p class="metric-value">${escapeHtml(summary.whatsapp_j40_selected_chats ?? 0)}</p>
          <p class="metric-label">J40 Chats Selected</p>
        </article>
        <article class="card">
          <p class="metric-value">${escapeHtml(summary.whatsapp_j40_media_items ?? 0)}</p>
          <p class="metric-label">WhatsApp Media Imported</p>
        </article>
        <article class="card">
          <p class="metric-value">${escapeHtml(summary.whatsapp_j40_media_images ?? 0)}</p>
          <p class="metric-label">WhatsApp Images</p>
        </article>
        <article class="card">
          <p class="metric-value">${escapeHtml(summary.whatsapp_j40_media_videos ?? 0)}</p>
          <p class="metric-label">WhatsApp Videos</p>
        </article>
        <article class="card">
          <p class="metric-value">${escapeHtml(summary.other_build_reference_media ?? summary.other_build_reference_images ?? 0)}</p>
          <p class="metric-label">Other-Build Reference Media</p>
        </article>
      </section>

      <h2 class="section-title">Core Workstreams</h2>
      <p class="section-subtitle">Current status, immediate next action, and direct media evidence.</p>
      <section class="cards-grid">
        ${workstreams
          .map((ws) => {
            const leadImage = chooseWorkstreamLeadImage(ws);
            return `
              <article class="card overview-workstream-card" data-open-workstream-id="${escapeHtml(ws.id)}">
                <div class="detail-header">
                  <h3>${escapeHtml(ws.title)}</h3>
                  <div class="overview-card-actions">
                    ${statusChip(ws.status)}
                    <button class="overview-open-btn" data-open-workstream-id="${escapeHtml(ws.id)}" type="button" aria-label="Open ${escapeHtml(ws.title)} workstream">Open</button>
                  </div>
                </div>
                <p class="small-muted">${chip(`Priority: ${formatToken(ws.priority)}`)} ${chip(`Phase: ${formatToken(ws.phase)}`)}</p>
                <p><strong>Next:</strong> ${escapeHtml(ws.next_action || "No action recorded")}</p>
                <p class="small-muted"><strong>Evidence:</strong> ${escapeHtml(ws.image_count ?? 0)} mapped media items</p>
                ${
                  leadImage
                    ? renderFigureImage(leadImage, ws.title, {
                        figureClass: "evidence-figure",
                        buttonClass: "image-open-btn",
                        imageClass: "lead-image",
                      })
                    : '<p class="small-muted">No media mapped.</p>'
                }
              </article>
            `;
          })
          .join("")}
      </section>

      ${renderWhatsappOverviewSection(summary)}

      <h2 class="section-title">Project Steps</h2>
      <div class="cards-grid">
        ${projectSteps
          .map(
            (step) => `
              <article class="card">
                <div class="detail-header">
                  <h3>${escapeHtml(step.work_package_id)} · ${escapeHtml(step.title)}</h3>
                  ${statusChip(step.current_state)}
                </div>
                <p>${escapeHtml(step.objective || "")}</p>
                <p class="small-muted"><strong>Gate:</strong> ${escapeHtml(step.gate_to_close || "")}</p>
              </article>
            `
          )
          .join("")}
      </div>

      <h2 class="section-title">Immediate Part Actions</h2>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Image</th>
              <th>Priority</th>
              <th>Workstream</th>
              <th>Item</th>
              <th>Next Action</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            ${
              urgentActions.length
                ? urgentActions
                    .slice(0, 14)
                    .map(
                      (row) => `
                        <tr>
                          ${renderInventoryImageCell(row, row.item || "Part image")}
                          <td>${escapeHtml(row.priority)}</td>
                          <td>${escapeHtml(formatToken(row.workstream))}</td>
                          <td>${renderItemButton(row)}</td>
                          <td>${escapeHtml(formatToken(row.next_action))}</td>
                          <td>${statusChip(row.status)}</td>
                        </tr>
                      `
                    )
                    .join("")
                : '<tr><td colspan="6">No urgent actions found.</td></tr>'
            }
          </tbody>
        </table>
      </div>
    `;
  }

  function renderWorkstreams() {
    const workstreams = data.workstreams || [];
    const active = workstreams.find((ws) => ws.id === state.activeWorkstreamId) || workstreams[0];
    if (!active) {
      root.innerHTML = '<p class="card">No workstream data available.</p>';
      return;
    }

    root.innerHTML = `
      <div class="workstream-layout">
        <aside class="workstream-list" id="workstream-list"></aside>
        <section class="workstream-detail" id="workstream-detail"></section>
      </div>
    `;

    const listNode = document.getElementById("workstream-list");
    const detailNode = document.getElementById("workstream-detail");
    if (!listNode || !detailNode) {
      return;
    }

    listNode.innerHTML = workstreams
      .map(
        (ws) => `
          <button class="ws-btn ${ws.id === active.id ? "is-active" : ""}" data-workstream-id="${escapeHtml(ws.id)}" type="button">
            <span>${escapeHtml(ws.title)}</span>
            ${statusChip(ws.status)}
          </button>
        `
      )
      .join("");

    listNode.querySelectorAll("[data-workstream-id]").forEach((button) => {
      button.addEventListener("click", () => {
        const nextId = button.getAttribute("data-workstream-id");
        if (!nextId || nextId === state.activeWorkstreamId) {
          return;
        }
        state.activeWorkstreamId = nextId;
        renderWorkstreams();
      });
    });

    const filteredEvidenceSets = buildWorkstreamEvidenceSets(active);
    const uniqueEvidenceMedia = dedupeImages(
      filteredEvidenceSets.flatMap((set) => (Array.isArray(set.images) ? set.images : []))
    );
    const involvedParts = Array.isArray(active.involved_parts) ? active.involved_parts : [];
    const filteredEvidenceCount = uniqueEvidenceMedia.length;
    const filteredVideoCount = uniqueEvidenceMedia.reduce((count, image) => {
      const mediaType = withOverride(getBasePhotoMeta(image)).media_type;
      return mediaType === "video" ? count + 1 : count;
    }, 0);
    const simpleChassisRubbers = active.id === "chassis_rubbers";
    const showOperationPanels =
      !simpleChassisRubbers && (active.id === "chassis_fixing" || !(active.subtask_groups && active.subtask_groups.length));

    detailNode.innerHTML = `
      <article class="card">
        <div class="detail-header">
          <h2>${escapeHtml(active.title)}</h2>
          ${statusChip(active.status)}
        </div>
        <div class="chip-row">
          ${chip(`Priority: ${formatToken(active.priority)}`)}
          ${chip(`Phase: ${formatToken(active.phase)}`)}
          ${chip(`Location: ${formatToken(active.primary_location)}`)}
          ${chip(`Owner Mode: ${formatToken(active.owner_mode)}`)}
        </div>
        <p><strong>Depends On:</strong> ${escapeHtml(active.depends_on && active.depends_on.length ? active.depends_on.map(formatToken).join(", ") : "None")}</p>
        <p><strong>Next Action:</strong> ${escapeHtml(active.next_action || "No action recorded.")}</p>
        <p><strong>Exit Gate:</strong> ${escapeHtml(active.exit_gate || "No gate recorded.")}</p>
        <p class="small-muted">${escapeHtml(active.notes || "")}</p>
      </article>

      ${renderWorkstreamRequirements(active)}
      ${simpleChassisRubbers ? "" : renderFabricationPackages(active.fabrication_packages)}

      ${simpleChassisRubbers ? "" : `
        <article class="card">
          <h3>Evidence Media</h3>
          <p class="small-muted">${escapeHtml(filteredEvidenceCount || 0)} unique media items across evidence sets${filteredVideoCount ? ` (${escapeHtml(filteredVideoCount)} videos)` : ""}.</p>
          ${renderEvidenceSets(filteredEvidenceSets)}
        </article>
      `}

      ${simpleChassisRubbers ? "" : renderSubtaskGroups(active.subtask_groups)}
      ${showOperationPanels ? renderOperationPanels(active.operation_panels) : ""}

      ${simpleChassisRubbers ? "" : `
        <article class="card">
          <h3>Guided Steps</h3>
          ${renderStepsList(active.steps)}
        </article>
      `}

      ${simpleChassisRubbers ? "" : `
        <article class="card">
          <h3>Involved Parts</h3>
          <p class="small-muted">${escapeHtml(involvedParts.length || 0)} mapped part rows for this workstream. ${renderInventoryPageLink("Open Ordering + Inventory")}</p>
          ${
            involvedParts.length
              ? `
                  <div class="table-wrap">
                    <table>
                      <thead>
                        <tr>
                          <th>Image</th>
                          <th>Item</th>
                          <th>Status</th>
                          <th>Procurement</th>
                          <th>Payment / Delivery</th>
                          <th>Inventory</th>
                        </tr>
                      </thead>
                      <tbody>
                        ${involvedParts
                          .map(
                            (row) => `
                              <tr>
                                ${renderInventoryImageCell(row, row.item || "Part image")}
                                <td>
                                  <strong>${escapeHtml(row.item || "")}</strong>
                                  <div class="small-muted">${escapeHtml(row.entry_id || "")}</div>
                                </td>
                                <td>${statusChip(row.status)}</td>
                                <td>${escapeHtml(formatToken(row.procurement_stage || "unknown"))}</td>
                                <td>${escapeHtml(formatToken(row.payment_status || "unknown"))} / ${escapeHtml(formatToken(row.delivery_status || "unknown"))}</td>
                                <td>${renderInventoryPageLink("Open")}</td>
                              </tr>
                            `
                          )
                          .join("")}
                      </tbody>
                    </table>
                  </div>
                `
              : '<p class="small-muted">No part rows are mapped to this workstream yet.</p>'
          }
        </article>
      `}

      ${renderElectricalSpecLayout(active.electrical_spec_layout)}

      ${simpleChassisRubbers ? "" : `
        <article class="card">
          <h3>Linked Project Packages</h3>
          ${
            active.linked_packages && active.linked_packages.length
              ? `
                  <div class="table-wrap">
                    <table>
                      <thead>
                        <tr>
                          <th>Package</th>
                          <th>Status</th>
                          <th>Objective</th>
                          <th>Gate</th>
                        </tr>
                      </thead>
                      <tbody>
                        ${active.linked_packages
                          .map(
                            (row) => `
                              <tr>
                                <td>${escapeHtml(row.work_package_id)} · ${escapeHtml(row.title)}</td>
                                <td>${statusChip(row.current_state)}</td>
                                <td>${escapeHtml(row.objective)}</td>
                                <td>${escapeHtml(row.gate_to_close)}</td>
                              </tr>
                            `
                          )
                          .join("")}
                      </tbody>
                    </table>
                  </div>
                `
              : '<p class="small-muted">No linked package rows found.</p>'
          }
        </article>
      `}

      ${simpleChassisRubbers ? "" : `
        <div class="split">
          <article class="card">
            <h3>Component Jobs</h3>
            ${
              active.component_jobs && active.component_jobs.length
                ? `<ul class="plain-list">
                    ${active.component_jobs
                      .slice(0, 14)
                      .map(
                        (job) => `
                          <li class="plain-item">
                            <div class="step-row">
                              <span class="step-label">${escapeHtml(formatToken(job.component_job_id))}</span>
                              ${statusChip(job.current_status)}
                            </div>
                            <p class="step-detail">${escapeHtml(job.planned_action || "")}</p>
                          </li>
                        `
                      )
                      .join("")}
                  </ul>`
                : '<p class="small-muted">No component jobs linked.</p>'
            }
          </article>

          <article class="card">
            <h3>Issue Checks</h3>
            ${
              active.issue_jobs && active.issue_jobs.length
                ? `<ul class="plain-list">
                    ${active.issue_jobs
                      .map(
                        (issue) => `
                          <li class="plain-item">
                            <div class="step-row">
                              <span class="step-label">${escapeHtml(formatToken(issue.component_job_id))}</span>
                              ${statusChip(issue.current_status)}
                            </div>
                            <p class="step-detail">${escapeHtml(issue.planned_action || "")}</p>
                          </li>
                        `
                      )
                      .join("")}
                  </ul>`
                : '<p class="small-muted">No issue-specific rows for this workstream.</p>'
            }
          </article>
        </div>
      `}
    `;
  }

  function renderParts() {
    const parts = data.parts || {};
    const supplies = data.supplies || {};
    const stageCounts = parts.counts_by_procurement_stage || [];
    const nextActionCounts = parts.counts_by_next_action || [];
    const urgentRows = parts.urgent_actions || [];
    const orderedRows = parts.ordered_pending_delivery || [];
    const openRows = parts.open_rows || [];
    const workstreamCards = parts.open_counts_by_workstream || [];
    const procurementEvidence = buildProcurementEvidenceImages(parts.procurement_evidence_images || []);
    const workbookSourceLinks = parts.workbook_source_links || [];
    const supplySummary = supplies.summary_by_type || [];
    const supplyRowsByStatus = supplies.rows_by_status || {};
    const allSupplyRows = supplies.all_rows || [];
    const inventoryGroupOrder = Array.isArray(supplies.inventory_groups) && supplies.inventory_groups.length
      ? supplies.inventory_groups
      : ["electrical", "mechanical", "tools", "parts", "substances"];
    const inventoryGroupLabels = {
      electrical: "Electrical Inventory",
      mechanical: "Mechanical Inventory",
      tools: "Tools Inventory",
      parts: "Parts Inventory",
      substances: "Substances Inventory",
    };
    const groupedSupplyRows = {};
    inventoryGroupOrder.forEach((group) => {
      groupedSupplyRows[group] = [];
    });
    allSupplyRows.forEach((row) => {
      const explicitGroup = cleanString(row && row.inventory_group).toLowerCase();
      const supplyType = cleanString(row && row.supply_type).toLowerCase();
      let group = explicitGroup;
      if (!group) {
        if (supplyType === "tool") {
          group = "tools";
        } else if (supplyType === "substance") {
          group = "substances";
        } else {
          group = "parts";
        }
      }
      if (!groupedSupplyRows[group]) {
        groupedSupplyRows[group] = [];
      }
      groupedSupplyRows[group].push(row);
    });
    const suppliesPreviously = supplyRowsByStatus.previously || [];
    const suppliesInProcess = supplyRowsByStatus.in_process || [];
    const suppliesStillRequired = supplyRowsByStatus.still_required || [];

    const renderEstimateTypeCell = (row) => {
      const value = cleanString(row.estimated_hardware_type || "");
      return value ? escapeHtml(truncateText(value, 140)) : "-";
    };
    const renderEstimateCountCell = (row) => {
      const count = cleanString(row.estimated_visible_count || "");
      const confidence = cleanString(row.estimate_confidence || "");
      if (!count) {
        return "-";
      }
      return `
        <div>${escapeHtml(count)}</div>
        ${confidence ? `<div class="small-muted">Confidence: ${escapeHtml(formatToken(confidence))}</div>` : ""}
      `;
    };
    const stillRequiredTypeChips = supplySummary
      .filter((row) => toNumber(row.still_required) > 0)
      .map((row) => chip(`${formatToken(row.supply_type)}: ${row.still_required}`))
      .join("");
    const renderStillRequiredSuppliesSection = () => `
      <section class="card">
        <div class="detail-header">
          <h3>Still Required / Need To Order</h3>
          ${chip(`${suppliesStillRequired.length} rows`)}
        </div>
        <div class="chip-row">
          ${stillRequiredTypeChips || chip("No still-required rows")}
        </div>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Image</th>
                <th>Type</th>
                <th>Item</th>
                <th>Anticipated Type</th>
                <th>Est. Count</th>
                <th>Source</th>
                <th>Workstream</th>
                <th>Procurement Stage</th>
                <th>Supplier</th>
                <th>Cost</th>
                <th>Links</th>
              </tr>
            </thead>
            <tbody>
              ${
                suppliesStillRequired.length
                  ? suppliesStillRequired
                      .map(
                        (row) => `
                          <tr>
                            ${renderInventoryImageCell(row, row.item || "Inventory image")}
                            <td>${escapeHtml(formatToken(row.supply_type))}</td>
                            <td>${renderItemButton(row)}</td>
                            <td>${renderEstimateTypeCell(row)}</td>
                            <td>${renderEstimateCountCell(row)}</td>
                            <td>${escapeHtml(formatToken(row.source))}</td>
                            <td>${escapeHtml(formatToken(row.workstream || "-"))}</td>
                            <td>${escapeHtml(formatToken(row.procurement_stage || row.status_detail || "-"))}</td>
                            <td>${tableSupplierCell(row)}</td>
                            <td>${tableCostCell(row)}</td>
                            <td>${renderLinksCell(row)}</td>
                          </tr>
                        `
                      )
                      .join("")
                  : '<tr><td colspan="11">No still-required supply rows.</td></tr>'
              }
            </tbody>
          </table>
        </div>
      </section>
    `;

    root.innerHTML = `
      <h2 class="section-title">Ordering and Inventory Guidance</h2>
      <p class="section-subtitle">Parts ordering plus lifecycle tracking for tools, substances, and parts.</p>

      ${renderStillRequiredSuppliesSection()}

      <section class="card">
        <h3>Tools + Substances + Parts Lifecycle</h3>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Type</th>
                <th>Previously</th>
                <th>In Process</th>
                <th>Still Required</th>
                <th>Total</th>
              </tr>
            </thead>
            <tbody>
              ${
                supplySummary.length
                  ? supplySummary
                      .map(
                        (row) => `
                          <tr>
                            <td>${escapeHtml(formatToken(row.supply_type))}</td>
                            <td>${escapeHtml(row.previously)}</td>
                            <td>${escapeHtml(row.in_process)}</td>
                            <td>${escapeHtml(row.still_required)}</td>
                            <td>${escapeHtml(row.total)}</td>
                          </tr>
                        `
                      )
                      .join("")
                  : '<tr><td colspan="5">No supply rows found.</td></tr>'
              }
            </tbody>
          </table>
        </div>
      </section>

      ${
        inventoryGroupOrder
          .map((groupKey) => {
            const rows = groupedSupplyRows[groupKey] || [];
            return `
              <h3 class="section-title">${escapeHtml(inventoryGroupLabels[groupKey] || `${formatToken(groupKey)} Inventory`)}</h3>
              <div class="table-wrap">
                <table>
                  <thead>
                    <tr>
                      <th>Image</th>
                      <th>Item</th>
                      <th>Anticipated Type</th>
                      <th>Est. Count</th>
                      <th>Status Group</th>
                      <th>Source</th>
                      <th>Workstream</th>
                      <th>Supplier</th>
                      <th>Cost</th>
                      <th>Links</th>
                    </tr>
                  </thead>
                  <tbody>
                    ${
                      rows.length
                        ? rows
                            .map(
                              (row) => `
                                <tr>
                                  ${renderInventoryImageCell(row, row.item || "Inventory image")}
                                  <td>${renderItemButton(row)}</td>
                                  <td>${renderEstimateTypeCell(row)}</td>
                                  <td>${renderEstimateCountCell(row)}</td>
                                  <td>${statusChip(row.status_group || "-")}</td>
                                  <td>${escapeHtml(formatToken(row.source || "-"))}</td>
                                  <td>${escapeHtml(formatToken(row.workstream || "-"))}</td>
                                  <td>${tableSupplierCell(row)}</td>
                                  <td>${tableCostCell(row)}</td>
                                  <td>${renderLinksCell(row)}</td>
                                </tr>
                              `
                            )
                            .join("")
                        : `<tr><td colspan="10">No ${escapeHtml(groupKey)} inventory rows found.</td></tr>`
                    }
                  </tbody>
                </table>
              </div>
            `;
          })
          .join("")
      }

      <section class="card">
        <h3>Part Ordering Steps</h3>
        ${renderStepsList(parts.steps || [])}
      </section>

      <section class="card">
        <h3>Procurement Package Evidence</h3>
        <p class="small-muted">${escapeHtml(procurementEvidence.length)} images currently tagged for package/part-number reconciliation.</p>
        ${renderGallery(procurementEvidence)}
      </section>

      <h3 class="section-title">Workbook Source Links</h3>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>System</th>
              <th>Item</th>
              <th>Source</th>
              <th>Stage / Decision</th>
              <th>Cost</th>
              <th>Qty</th>
              <th>Total Value</th>
              <th>Links</th>
              <th>Notes</th>
            </tr>
          </thead>
          <tbody>
            ${
              workbookSourceLinks.length
                ? workbookSourceLinks
                    .map(
                      (row) => `
                        <tr>
                          <td>${escapeHtml(formatToken(row.system || "-"))}</td>
                          <td>${escapeHtml(row.item || "-")}</td>
                          <td>${escapeHtml(row.source_sheet || "-")}</td>
                          <td>${escapeHtml([formatToken(row.stage || ""), formatToken(row.decision || "")].filter(Boolean).join(" / ") || "-")}</td>
                          <td>${escapeHtml(row.cost || "-")}</td>
                          <td>${escapeHtml(row.quantity || "-")}</td>
                          <td>${escapeHtml(row.total_value || "-")}</td>
                          <td>${renderLinksCell(row)}</td>
                          <td>${escapeHtml(truncateText(row.notes || "", 140) || "-")}</td>
                        </tr>
                      `
                    )
                    .join("")
                : '<tr><td colspan="9">No workbook source links found.</td></tr>'
            }
          </tbody>
        </table>
      </div>

      <section class="split">
        <article class="card">
          <h3>Counts by Procurement Stage</h3>
          <div class="chip-row">
            ${stageCounts.map((row) => chip(`${formatToken(row.stage)}: ${row.count}`)).join("") || chip("No rows")}
          </div>
        </article>
        <article class="card">
          <h3>Counts by Next Action</h3>
          <div class="chip-row">
            ${nextActionCounts.map((row) => chip(`${formatToken(row.next_action)}: ${row.count}`)).join("") || chip("No rows")}
          </div>
        </article>
      </section>

      <h3 class="section-title">Urgent Actions</h3>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Image</th>
              <th>Priority</th>
              <th>Item</th>
              <th>Anticipated Type</th>
              <th>Est. Count</th>
              <th>Supplier</th>
              <th>Cost</th>
              <th>Links</th>
              <th>Workstream</th>
              <th>Next Action</th>
              <th>Stage</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            ${
              urgentRows.length
                ? urgentRows
                    .map(
                      (row) => `
                        <tr>
                          ${renderInventoryImageCell(row, row.item || "Part image")}
                          <td>${escapeHtml(row.priority)}</td>
                          <td>${renderItemButton(row)}</td>
                          <td>${renderEstimateTypeCell(row)}</td>
                          <td>${renderEstimateCountCell(row)}</td>
                          <td>${tableSupplierCell(row)}</td>
                          <td>${tableCostCell(row)}</td>
                          <td>${renderLinksCell(row)}</td>
                          <td>${escapeHtml(formatToken(row.workstream))}</td>
                          <td>${escapeHtml(formatToken(row.next_action))}</td>
                          <td>${escapeHtml(formatToken(row.procurement_stage))}</td>
                          <td>${statusChip(row.status)}</td>
                        </tr>
                      `
                    )
                    .join("")
                : '<tr><td colspan="12">No urgent action rows.</td></tr>'
            }
          </tbody>
        </table>
      </div>

      <h3 class="section-title">Ordered / Pending Delivery</h3>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Image</th>
              <th>Item</th>
              <th>Anticipated Type</th>
              <th>Est. Count</th>
              <th>Supplier</th>
              <th>Cost</th>
              <th>Links</th>
              <th>Workstream</th>
              <th>Payment</th>
              <th>Delivery</th>
              <th>Stage</th>
              <th>Expected Date</th>
            </tr>
          </thead>
          <tbody>
            ${
              orderedRows.length
                ? orderedRows
                    .map(
                      (row) => `
                        <tr>
                          ${renderInventoryImageCell(row, row.item || "Part image")}
                          <td>${renderItemButton(row)}</td>
                          <td>${renderEstimateTypeCell(row)}</td>
                          <td>${renderEstimateCountCell(row)}</td>
                          <td>${tableSupplierCell(row)}</td>
                          <td>${tableCostCell(row)}</td>
                          <td>${renderLinksCell(row)}</td>
                          <td>${escapeHtml(formatToken(row.workstream))}</td>
                          <td>${statusChip(row.payment_status)}</td>
                          <td>${statusChip(row.delivery_status)}</td>
                          <td>${escapeHtml(formatToken(row.procurement_stage))}</td>
                          <td>${escapeHtml(row.expected_delivery_date || "-")}</td>
                        </tr>
                      `
                    )
                    .join("")
                : '<tr><td colspan="12">No in-flight delivery rows.</td></tr>'
            }
          </tbody>
        </table>
      </div>

      <h3 class="section-title">Open Part Load by Workstream</h3>
      <section class="parts-workstream-grid">
        ${
          workstreamCards.length
            ? workstreamCards
                .map(
                  (card) => `
                    <article class="card">
                      <div class="detail-header">
                        <h4>${escapeHtml(formatToken(card.workstream))}</h4>
                        ${chip(`${card.open_count} open`)}
                      </div>
                      ${
                        card.image && !isImageDeleted(card.image)
                          ? renderFigureImage(card.image, card.workstream || "Workstream image", {
                              figureClass: "evidence-figure",
                              imageClass: "lead-image",
                            })
                          : '<p class="small-muted">No media mapped for this workstream.</p>'
                      }
                    </article>
                  `
                )
                .join("")
            : '<article class="card">No open part rows.</article>'
        }
      </section>

      <h3 class="section-title">Open Parts (All)</h3>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Image</th>
              <th>Item</th>
              <th>Anticipated Type</th>
              <th>Est. Count</th>
              <th>Supplier</th>
              <th>Cost</th>
              <th>Links</th>
              <th>Workstream</th>
              <th>Status</th>
              <th>Stage</th>
              <th>Payment</th>
              <th>Delivery</th>
            </tr>
          </thead>
          <tbody>
            ${
              openRows.length
                ? openRows
                    .map(
                      (row) => `
                        <tr>
                          ${renderInventoryImageCell(row, row.item || "Part image")}
                          <td>${renderItemButton(row)}</td>
                          <td>${renderEstimateTypeCell(row)}</td>
                          <td>${renderEstimateCountCell(row)}</td>
                          <td>${tableSupplierCell(row)}</td>
                          <td>${tableCostCell(row)}</td>
                          <td>${renderLinksCell(row)}</td>
                          <td>${escapeHtml(formatToken(row.workstream))}</td>
                          <td>${statusChip(row.status)}</td>
                          <td>${escapeHtml(formatToken(row.procurement_stage))}</td>
                          <td>${statusChip(row.payment_status)}</td>
                          <td>${statusChip(row.delivery_status)}</td>
                        </tr>
                      `
                    )
                    .join("")
                : '<tr><td colspan="12">No open parts.</td></tr>'
            }
          </tbody>
        </table>
      </div>

      <h3 class="section-title">Supplies In Process</h3>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Image</th>
              <th>Type</th>
              <th>Item</th>
              <th>Anticipated Type</th>
              <th>Est. Count</th>
              <th>Supplier</th>
              <th>Cost</th>
              <th>Links</th>
              <th>Source</th>
              <th>Workstream</th>
              <th>Status Detail</th>
              <th>Payment</th>
              <th>Delivery</th>
            </tr>
          </thead>
          <tbody>
            ${
              suppliesInProcess.length
                ? suppliesInProcess
                    .map(
                      (row) => `
                        <tr>
                          ${renderInventoryImageCell(row, row.item || "Inventory image")}
                          <td>${escapeHtml(formatToken(row.supply_type))}</td>
                          <td>${renderItemButton(row)}</td>
                          <td>${renderEstimateTypeCell(row)}</td>
                          <td>${renderEstimateCountCell(row)}</td>
                          <td>${tableSupplierCell(row)}</td>
                          <td>${tableCostCell(row)}</td>
                          <td>${renderLinksCell(row)}</td>
                          <td>${escapeHtml(formatToken(row.source))}</td>
                          <td>${escapeHtml(formatToken(row.workstream || "-"))}</td>
                          <td>${escapeHtml(formatToken(row.status_detail || row.procurement_stage || "-"))}</td>
                          <td>${statusChip(row.payment_status || "-")}</td>
                          <td>${statusChip(row.delivery_status || "-")}</td>
                        </tr>
                      `
                    )
                    .join("")
                : '<tr><td colspan="13">No in-process supply rows.</td></tr>'
            }
          </tbody>
        </table>
      </div>

      <h3 class="section-title">Previously Procured Supplies</h3>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Image</th>
              <th>Type</th>
              <th>Item</th>
              <th>Anticipated Type</th>
              <th>Est. Count</th>
              <th>Supplier</th>
              <th>Cost</th>
              <th>Links</th>
              <th>Source</th>
              <th>Workstream</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            ${
              suppliesPreviously.length
                ? suppliesPreviously
                    .map(
                      (row) => `
                        <tr>
                          ${renderInventoryImageCell(row, row.item || "Inventory image")}
                          <td>${escapeHtml(formatToken(row.supply_type))}</td>
                          <td>${renderItemButton(row)}</td>
                          <td>${renderEstimateTypeCell(row)}</td>
                          <td>${renderEstimateCountCell(row)}</td>
                          <td>${tableSupplierCell(row)}</td>
                          <td>${tableCostCell(row)}</td>
                          <td>${renderLinksCell(row)}</td>
                          <td>${escapeHtml(formatToken(row.source))}</td>
                          <td>${escapeHtml(formatToken(row.workstream || "-"))}</td>
                          <td>${escapeHtml(formatToken(row.status_detail || "received"))}</td>
                        </tr>
                      `
                    )
                    .join("")
                : '<tr><td colspan="11">No previously-procured supply rows.</td></tr>'
            }
          </tbody>
        </table>
      </div>
    `;
  }

  function priorityChip(priority) {
    const normalized = cleanString(priority || "P1").toUpperCase();
    let tone = "info";
    if (normalized === "P0") {
      tone = "bad";
    } else if (normalized === "P1") {
      tone = "warn";
    }
    return `<span class="chip ${tone}">${escapeHtml(normalized)}</span>`;
  }

  function renderCaptureTaskEvidence(task) {
    const images = Array.isArray(task.evidence_images) ? task.evidence_images : [];
    if (!images.length) {
      const ref = cleanString(task.evidence_ref);
      return ref ? `<span class="small-muted">${escapeHtml(truncateText(ref, 90))}</span>` : "-";
    }
    const fallbackCaption = task.title || "Task evidence";
    return `
      <div class="requirement-evidence-grid capture-task-evidence-grid">
        ${images
          .slice(0, 4)
          .map((image) => {
            const prepared = prepareImage(image, fallbackCaption);
            return `
              <div class="requirement-evidence-item">
                ${renderPreparedMedia(prepared, "table-image-btn", "table-image")}
                <span class="table-image-note">${escapeHtml(prepared.effective.media_id || "")}</span>
              </div>
            `;
          })
          .join("")}
      </div>
      ${images.length > 4 ? `<span class="table-image-note">+${escapeHtml(images.length - 4)} more</span>` : ""}
    `;
  }

  function renderTaskCountChips(rows, keyName, formatter) {
    const source = Array.isArray(rows) ? rows : [];
    return source.length
      ? source.map((row) => chip(`${formatter(row[keyName])}: ${row.count}`)).join("")
      : chip("No rows");
  }

  function isPhotoNeededTask(task) {
    return cleanString(task && task.task_type).includes("photo");
  }

  function countRowsBy(rows, keyName) {
    const counts = new Map();
    (Array.isArray(rows) ? rows : []).forEach((row) => {
      const key = cleanString(row && row[keyName]) || "unassigned";
      counts.set(key, (counts.get(key) || 0) + 1);
    });
    return Array.from(counts.entries())
      .map(([key, count]) => ({ key, count }))
      .sort((left, right) => right.count - left.count || left.key.localeCompare(right.key));
  }

  function renderPhotoNeededCountChips(rows, keyName, formatter) {
    const counts = countRowsBy(rows, keyName);
    return counts.length
      ? counts.map((row) => chip(`${formatter(row.key)}: ${row.count}`)).join("")
      : chip("No rows");
  }

  function renderPhotoNeededRows(rows, emptyMessage) {
    const source = Array.isArray(rows) ? rows : [];
    if (!source.length) {
      return `<tr><td colspan="7">${escapeHtml(emptyMessage)}</td></tr>`;
    }
    return source
      .map(
        (task) => `
          <tr>
            <td>
              <div class="task-title-row">
                ${priorityChip(task.priority)}
                ${statusChip(task.status || "open")}
              </div>
              <strong>${escapeHtml(task.title || task.task_id || "Photo")}</strong>
              ${task.location ? `<div class="small-muted">${escapeHtml(task.location)}</div>` : ""}
            </td>
            <td>${escapeHtml(formatToken(task.workstream || "-"))}</td>
            <td>${escapeHtml(formatToken(task.timing || "now"))}</td>
            <td>
              ${escapeHtml(task.action || "-")}
              ${task.notes ? `<div class="small-muted">${escapeHtml(truncateText(task.notes, 150))}</div>` : ""}
            </td>
            <td>${escapeHtml(task.data_needed || "-")}</td>
            <td class="requirement-evidence-cell">${renderCaptureTaskEvidence(task)}</td>
            <td>
              ${task.blocks ? `<div>${escapeHtml(task.blocks)}</div>` : ""}
              ${task.record_result_in ? `<div class="small-muted">${escapeHtml(task.record_result_in)}</div>` : ""}
              <div class="small-muted">${escapeHtml(task.source_row_id || "")}</div>
              ${renderLinksCell(task)}
            </td>
          </tr>
        `
      )
      .join("");
  }

  function renderPhotosNeeded() {
    const captureTasks = data.capture_tasks || {};
    const tasks = Array.isArray(captureTasks.tasks) ? captureTasks.tasks : [];
    const photoTasks = tasks.filter(isPhotoNeededTask);
    const nowPhotoTasks = photoTasks.filter((task) => cleanString(task.timing) !== "later");
    const laterPhotoTasks = photoTasks.filter((task) => cleanString(task.timing) === "later");
    const p0PhotoTasks = photoTasks.filter((task) => cleanString(task.priority).toUpperCase() === "P0");
    const photoMeasurementTasks = photoTasks.filter((task) => cleanString(task.task_type) === "photo_measurement");

    root.innerHTML = `
      <h2 class="section-title">Photos Needed</h2>
      <p class="section-subtitle">Open capture rows where the next closeout evidence includes a photo or photo-backed measurement.</p>

      <section class="metrics-grid">
        <article class="card">
          <p class="metric-value">${escapeHtml(photoTasks.length)}</p>
          <p class="metric-label">Photos Needed</p>
        </article>
        <article class="card">
          <p class="metric-value">${escapeHtml(nowPhotoTasks.length)}</p>
          <p class="metric-label">Current Photo Rows</p>
        </article>
        <article class="card">
          <p class="metric-value">${escapeHtml(p0PhotoTasks.length)}</p>
          <p class="metric-label">P0 Photo Rows</p>
        </article>
        <article class="card">
          <p class="metric-value">${escapeHtml(photoMeasurementTasks.length)}</p>
          <p class="metric-label">Photo + Measurement Rows</p>
        </article>
        <article class="card">
          <p class="metric-value">${escapeHtml(laterPhotoTasks.length)}</p>
          <p class="metric-label">Deferred Photo Rows</p>
        </article>
      </section>

      <section class="split capture-task-counts">
        <article class="card">
          <h3>By Workstream</h3>
          <div class="chip-row">
            ${renderPhotoNeededCountChips(photoTasks, "workstream", formatToken)}
          </div>
        </article>
        <article class="card">
          <h3>By Priority</h3>
          <div class="chip-row">
            ${renderPhotoNeededCountChips(photoTasks, "priority", (value) => cleanString(value).toUpperCase() || "P1")}
          </div>
        </article>
      </section>

      <h3 class="section-title">Take These Photos Now</h3>
      <div class="table-wrap">
        <table class="capture-task-table photos-needed-table">
          <thead>
            <tr>
              <th>Photo</th>
              <th>Workstream</th>
              <th>When</th>
              <th>What To Capture</th>
              <th>Labels / Measurements</th>
              <th>Context Evidence</th>
              <th>Blocks / Source</th>
            </tr>
          </thead>
          <tbody>
            ${renderPhotoNeededRows(nowPhotoTasks, "No current photo rows found.")}
          </tbody>
        </table>
      </div>

      <h3 class="section-title">Later / Deferred Photos</h3>
      <div class="table-wrap">
        <table class="capture-task-table photos-needed-table compact">
          <thead>
            <tr>
              <th>Photo</th>
              <th>Workstream</th>
              <th>When</th>
              <th>What To Capture</th>
              <th>Labels / Measurements</th>
              <th>Context Evidence</th>
              <th>Blocks / Source</th>
            </tr>
          </thead>
          <tbody>
            ${renderPhotoNeededRows(laterPhotoTasks, "No deferred photo rows found.")}
          </tbody>
        </table>
      </div>
    `;
  }

  function renderCaptureTasks() {
    const captureTasks = data.capture_tasks || {};
    const summary = captureTasks.summary || {};
    const tasks = Array.isArray(captureTasks.tasks) ? captureTasks.tasks : [];
    const nowTasks = tasks.filter((task) => cleanString(task.timing) !== "later");

    root.innerHTML = `
      <h2 class="section-title">Photo and Data Tasks</h2>
      <p class="section-subtitle">Open rows that need a photograph, measurement, identification, inspection result, or release decision before the related work can close.</p>

      <section class="metrics-grid">
        <article class="card">
          <p class="metric-value">${escapeHtml(summary.total_tasks ?? 0)}</p>
          <p class="metric-label">Total Open Tasks</p>
        </article>
        <article class="card">
          <p class="metric-value">${escapeHtml(summary.now_tasks ?? 0)}</p>
          <p class="metric-label">Current Tasks</p>
        </article>
        <article class="card">
          <p class="metric-value">${escapeHtml(summary.p0_tasks ?? 0)}</p>
          <p class="metric-label">P0 Tasks</p>
        </article>
        <article class="card">
          <p class="metric-value">${escapeHtml(summary.photo_tasks ?? 0)}</p>
          <p class="metric-label">Photo Tasks</p>
        </article>
        <article class="card">
          <p class="metric-value">${escapeHtml(summary.measurement_tasks ?? 0)}</p>
          <p class="metric-label">Measurement / Template Tasks</p>
        </article>
        <article class="card">
          <p class="metric-value">${escapeHtml(summary.later_tasks ?? 0)}</p>
          <p class="metric-label">Later / Deferred</p>
        </article>
      </section>

      <section class="split capture-task-counts">
        <article class="card">
          <h3>By Workstream</h3>
          <div class="chip-row">
            ${renderTaskCountChips(captureTasks.counts_by_workstream, "workstream", formatToken)}
          </div>
        </article>
        <article class="card">
          <h3>By Task Type</h3>
          <div class="chip-row">
            ${renderTaskCountChips(captureTasks.counts_by_task_type, "task_type", formatToken)}
          </div>
        </article>
      </section>

      <h3 class="section-title">Current Task List</h3>
      <div class="table-wrap">
        <table class="capture-task-table">
          <thead>
            <tr>
              <th>Evidence</th>
              <th>Task</th>
              <th>Workstream</th>
              <th>Type</th>
              <th>Action</th>
              <th>Data Needed</th>
              <th>Blocks / Source</th>
            </tr>
          </thead>
          <tbody>
            ${
              nowTasks.length
                ? nowTasks
                    .map(
                      (task) => `
                        <tr>
                          <td class="requirement-evidence-cell">${renderCaptureTaskEvidence(task)}</td>
                          <td>
                            <div class="task-title-row">
                              ${priorityChip(task.priority)}
                              ${statusChip(task.status || "open")}
                            </div>
                            <strong>${escapeHtml(task.title || task.task_id || "Task")}</strong>
                            ${task.location ? `<div class="small-muted">${escapeHtml(task.location)}</div>` : ""}
                            ${task.notes ? `<div class="small-muted">${escapeHtml(truncateText(task.notes, 180))}</div>` : ""}
                          </td>
                          <td>${escapeHtml(formatToken(task.workstream || "-"))}</td>
                          <td>${escapeHtml(formatToken(task.task_type || "data"))}</td>
                          <td>${escapeHtml(task.action || "-")}</td>
                          <td>${escapeHtml(task.data_needed || "-")}</td>
                          <td>
                            ${task.blocks ? `<div>${escapeHtml(task.blocks)}</div>` : ""}
                            ${task.record_result_in ? `<div class="small-muted">${escapeHtml(task.record_result_in)}</div>` : ""}
                            <div class="small-muted">${escapeHtml(task.source_row_id || "")}</div>
                            ${renderLinksCell(task)}
                          </td>
                        </tr>
                      `
                    )
                    .join("")
                : '<tr><td colspan="7">No current photo/data tasks found.</td></tr>'
            }
          </tbody>
        </table>
      </div>

      <h3 class="section-title">Later / Deferred</h3>
      <div class="table-wrap">
        <table class="capture-task-table compact">
          <thead>
            <tr>
              <th>Priority</th>
              <th>Task</th>
              <th>Workstream</th>
              <th>Status</th>
              <th>Action / Data Needed</th>
              <th>Source</th>
            </tr>
          </thead>
          <tbody>
            ${
              tasks.filter((task) => cleanString(task.timing) === "later").length
                ? tasks
                    .filter((task) => cleanString(task.timing) === "later")
                    .map(
                      (task) => `
                        <tr>
                          <td>${priorityChip(task.priority)}</td>
                          <td>
                            <strong>${escapeHtml(task.title || task.task_id || "Task")}</strong>
                            ${task.location ? `<div class="small-muted">${escapeHtml(task.location)}</div>` : ""}
                          </td>
                          <td>${escapeHtml(formatToken(task.workstream || "-"))}</td>
                          <td>${statusChip(task.status || "open")}</td>
                          <td>
                            ${escapeHtml(task.action || "-")}
                            ${task.data_needed ? `<div class="small-muted">${escapeHtml(task.data_needed)}</div>` : ""}
                          </td>
                          <td>
                            <div class="small-muted">${escapeHtml(task.source_row_id || "")}</div>
                            ${renderLinksCell(task)}
                          </td>
                        </tr>
                      `
                    )
                    .join("")
                : '<tr><td colspan="6">No later/deferred tasks found.</td></tr>'
            }
          </tbody>
        </table>
      </div>
    `;
  }

  function renderProjectSteps() {
    const projectSteps = data.project_steps || [];
    root.innerHTML = `
      <h2 class="section-title">Project Steps and Status</h2>
      <p class="section-subtitle">These are the controlling work packages for the current build phase.</p>
      <section class="cards-grid">
        ${projectSteps
          .map(
            (step) => `
              <article class="card">
                <div class="detail-header">
                  <h3>${escapeHtml(step.work_package_id)} · ${escapeHtml(step.title)}</h3>
                  ${statusChip(step.current_state)}
                </div>
                <p><strong>Objective:</strong> ${escapeHtml(step.objective || "")}</p>
                <p><strong>Depends On:</strong> ${escapeHtml((step.depends_on || []).map(formatToken).join(", ") || "None")}</p>
                <p><strong>Linked Streams:</strong> ${escapeHtml((step.linked_workstreams || []).map(formatToken).join(", ") || "None")}</p>
                <p><strong>Blockers:</strong> ${escapeHtml(step.blocker_summary || "None recorded")}</p>
                <p><strong>Gate To Close:</strong> ${escapeHtml(step.gate_to_close || "")}</p>
                <p><strong>Procurement Guidance:</strong> ${escapeHtml(step.key_procurement_actions || "")}</p>
                ${
                  step.image && !isImageDeleted(step.image)
                    ? renderFigureImage(step.image, step.title || "Project step image", {
                        figureClass: "evidence-figure",
                        imageClass: "lead-image",
                      })
                    : ""
                }
              </article>
            `
          )
          .join("")}
      </section>
    `;
  }

  function renderSectionLinks(links) {
    const rows = Array.isArray(links) ? links : [];
    if (!rows.length) {
      return "";
    }
    return `
      <div class="item-links reference-links">
        ${rows
          .map((link, index) => {
            const url = cleanString(link && (link.url || link.href));
            if (!url) {
              return "";
            }
            return `<a class="item-link" href="${escapeHtml(url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(cleanString(link.label || link.title) || `Link ${index + 1}`)}</a>`;
          })
          .join("")}
      </div>
    `;
  }

  function otherBuildSectionId(section) {
    const raw = cleanString(section && (section.key || section.title)) || "reference";
    const slug = raw
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-+|-+$/g, "");
    return `other-build-${slug || "reference"}`;
  }

  function findOtherBuildSection(sections, key) {
    return sections.find((section) => cleanString(section && section.key) === key) || null;
  }

  function otherBuildMediaCount(section) {
    return Array.isArray(section && section.images) ? section.images.length : 0;
  }

  function otherBuildVideoCount(section) {
    const media = Array.isArray(section && section.images) ? section.images : [];
    return media.reduce((count, image) => {
      const type = resolvedMediaType(image && image.media_type, image && image.path);
      return type === "video" ? count + 1 : count;
    }, 0);
  }

  function otherBuildMediaLabel(section) {
    const mediaCount = otherBuildMediaCount(section);
    const videoCount = otherBuildVideoCount(section);
    return videoCount ? `${mediaCount} media (${videoCount} videos)` : `${mediaCount} media`;
  }

  function renderOtherBuildFocusCards(sections) {
    const focusCards = [
      {
        key: "whatsapp_islamabad_fj_restorations",
        title: "Islamabad FJ Restorations",
        description: "Original-spec 1965 and 1973 FJ references from the Fj40 group: stripped tub/chassis, chrome, cadmium hardware, panel finish, and engine component refinishing.",
        source: "Fj40 WhatsApp",
      },
      {
        key: "whatsapp_workshop_wiring_floor_samples",
        title: "Akber Wiring And Floor Samples",
        description: "Akber's missing before/after examples for engine-bay wiring cleanup and floor rust-through around the accelerator pedal.",
        source: "Akber Khan WhatsApp",
      },
    ]
      .map((card) => {
        const section = findOtherBuildSection(sections, card.key);
        if (!section) {
          return "";
        }
        const sectionId = otherBuildSectionId(section);
        return `
          <article class="card reference-focus-card">
            <div class="detail-header">
              <h3>${escapeHtml(card.title)}</h3>
              ${chip(otherBuildMediaLabel(section))}
            </div>
            <p class="small-muted">${escapeHtml(card.description)}</p>
            <div class="chip-row">
              ${chip(card.source)}
              <button class="item-link reference-jump-btn" type="button" data-scroll-reference-section="${escapeHtml(sectionId)}">View group</button>
            </div>
          </article>
        `;
      })
      .filter(Boolean);

    if (!focusCards.length) {
      return "";
    }

    return `
      <section class="reference-focus-grid" aria-label="New other-build reference groups">
        ${focusCards.join("")}
      </section>
    `;
  }

  function renderOtherBuilds() {
    const otherBuilds = data.other_builds || {};
    const summary = otherBuilds.summary || {};
    const sections = Array.isArray(otherBuilds.sections) ? otherBuilds.sections : [];
    const totalMedia = summary.total_media ?? summary.total_images ?? 0;
    const dropZoneMedia = summary.drop_zone_media ?? summary.drop_zone_images ?? 0;
    const manualReferenceMedia = summary.manual_reference_media ?? summary.manual_reference_images ?? 0;
    root.innerHTML = `
      <h2 class="section-title">Other Builds</h2>
      <p class="section-subtitle">Outside-build references, including the Islamabad FJ restorations, Akber wiring/floor caution examples, archived listings, and curated WhatsApp sample media.</p>

      <section class="metrics-grid">
        <article class="card">
          <p class="metric-value">${escapeHtml(totalMedia)}</p>
          <p class="metric-label">Reference Media</p>
        </article>
        <article class="card">
          <p class="metric-value">${escapeHtml(summary.total_videos ?? 0)}</p>
          <p class="metric-label">Reference Videos</p>
        </article>
        <article class="card">
          <p class="metric-value">${escapeHtml(dropZoneMedia)}</p>
          <p class="metric-label">Drop-Zone Media</p>
        </article>
        <article class="card">
          <p class="metric-value">${escapeHtml(manualReferenceMedia)}</p>
          <p class="metric-label">Curated WhatsApp Media</p>
        </article>
      </section>

      ${renderOtherBuildFocusCards(sections)}

      <section class="card reference-drop-card">
        <div class="detail-header">
          <h3>Reference Media Drop Zone</h3>
          ${chip(dropZoneMedia ? `${dropZoneMedia} media` : "Empty")}
        </div>
        <p class="small-muted"><code>${escapeHtml(otherBuilds.drop_zone || "data/reference/other_j40_builds")}</code></p>
      </section>

      <section class="reference-section-list">
        ${
          sections.length
            ? sections
                .map((section) => {
                  const images = Array.isArray(section.images) ? section.images : [];
                  const sectionId = otherBuildSectionId(section);
                  return `
                    <article class="card reference-section-card" id="${escapeHtml(sectionId)}">
                      <div class="detail-header">
                        <h3>${escapeHtml(section.title || "Reference Media")}</h3>
                        ${chip(otherBuildMediaLabel(section))}
                      </div>
                      <p class="small-muted">${escapeHtml(section.description || "")}</p>
                      ${section.source_path ? `<p class="small-muted"><strong>Source:</strong> <code>${escapeHtml(section.source_path)}</code></p>` : ""}
                      ${renderSectionLinks(section.links)}
                      ${renderGallery(images)}
                    </article>
                  `;
                })
                .join("")
            : '<article class="card">No other-build reference sections found.</article>'
        }
      </section>
    `;
  }

  function createItemDetail() {
    const wrapper = document.createElement("div");
    wrapper.className = "lightbox item-detail is-hidden";
    wrapper.setAttribute("aria-hidden", "true");
    wrapper.innerHTML = `
      <div class="lightbox-backdrop" data-item-detail-close="1"></div>
      <section class="item-detail-panel" role="dialog" aria-modal="true" aria-label="Item detail">
        <button type="button" class="lightbox-close" data-item-detail-close="1" aria-label="Close item detail">×</button>
        <div id="item-detail-media" class="item-detail-media"></div>
        <aside class="item-detail-sidebar">
          <h3 id="item-detail-title" class="section-title" style="margin-top:0;">Item Detail</h3>
          <p id="item-detail-subtitle" class="small-muted"></p>
          <dl id="item-detail-meta" class="meta-grid"></dl>
          <div id="item-detail-links"></div>
          <p id="item-detail-notes" class="small-muted"></p>
        </aside>
      </section>
    `;
    document.body.appendChild(wrapper);
    wrapper.addEventListener("click", (event) => {
      if (event.target.closest("[data-item-detail-close]")) {
        closeItemDetail();
      }
    });
    return {
      root: wrapper,
      media: wrapper.querySelector("#item-detail-media"),
      title: wrapper.querySelector("#item-detail-title"),
      subtitle: wrapper.querySelector("#item-detail-subtitle"),
      meta: wrapper.querySelector("#item-detail-meta"),
      links: wrapper.querySelector("#item-detail-links"),
      notes: wrapper.querySelector("#item-detail-notes"),
    };
  }

  function itemAmountLabel(row) {
    return costLabel(row);
  }

  function renderItemMetaRow(label, value, options = {}) {
    const normalized = cleanString(value);
    if (!normalized && !options.keepEmpty) {
      return "";
    }
    const displayValue = normalized || "-";
    return `<dt>${escapeHtml(label)}</dt><dd>${escapeHtml(displayValue)}</dd>`;
  }

  function renderItemDetail() {
    const row = state.itemDetailRow;
    if (!row) {
      return;
    }
    const sourceImage = row && row.image && !isImageDeleted(row.image) ? row.image : {};
    const prepared = prepareImage(sourceImage, row.item || "Item image");
    itemDetail.title.textContent = cleanString(row.item) || "Item Detail";
    itemDetail.subtitle.textContent = [
      formatToken(row.supply_type || row.inventory_group || "part"),
      formatToken(row.workstream || row.source || ""),
    ].filter(Boolean).join(" · ");
    itemDetail.media.innerHTML =
      prepared.mediaType === "video"
        ? `<video class="item-detail-image" controls preload="metadata" playsinline src="${escapeHtml(prepared.path)}"></video>`
        : `<img class="item-detail-image" src="${escapeHtml(prepared.path)}" alt="${escapeHtml(prepared.caption)}">`;
    itemDetail.meta.innerHTML = [
      renderItemMetaRow("Status Group", formatToken(row.status_group || ""), { keepEmpty: true }),
      renderItemMetaRow("Status", formatToken(row.status || row.status_detail || "")),
      renderItemMetaRow("Procurement Stage", formatToken(row.procurement_stage || "")),
      renderItemMetaRow("Payment", formatToken(row.payment_status || "")),
      renderItemMetaRow("Delivery", formatToken(row.delivery_status || "")),
      renderItemMetaRow("Expected", row.expected_delivery_date || ""),
      renderItemMetaRow("Priority", row.priority || ""),
      renderItemMetaRow("Next Action", formatToken(row.next_action || "")),
      renderItemMetaRow("Source", [formatToken(row.source || ""), row.source_ref || row.entry_id || ""].filter(Boolean).join(" · ")),
      renderItemMetaRow("Supplier", supplierLabel(row)),
      renderItemMetaRow("Cost", itemAmountLabel(row)),
      renderItemMetaRow("Anticipated Type", row.estimated_hardware_type || ""),
      renderItemMetaRow("Estimated Count", row.estimated_visible_count || ""),
      renderItemMetaRow("Estimate Confidence", formatToken(row.estimate_confidence || "")),
      renderItemMetaRow("Estimate Basis", row.estimated_purchase_basis || ""),
      renderItemMetaRow("Evidence", row.evidence_ref || ""),
      renderItemMetaRow("Image Match", formatToken(prepared.effective.match_basis || "")),
    ].join("");
    itemDetail.links.innerHTML = renderLinksPanel(row);
    itemDetail.notes.textContent = cleanString(row.notes) ? `Notes: ${cleanString(row.notes)}` : "";
  }

  function openItemDetail(itemKey) {
    const row = itemRegistry.get(itemKey);
    if (!row) {
      return;
    }
    if (state.lightboxImageBase) {
      closeLightbox();
    }
    state.itemDetailRow = row;
    renderItemDetail();
    itemDetail.root.classList.remove("is-hidden");
    itemDetail.root.setAttribute("aria-hidden", "false");
    document.body.classList.add("lightbox-open");
  }

  function closeItemDetail() {
    state.itemDetailRow = null;
    itemDetail.root.classList.add("is-hidden");
    itemDetail.root.setAttribute("aria-hidden", "true");
    itemDetail.media.innerHTML = "";
    itemDetail.links.innerHTML = "";
    document.body.classList.remove("lightbox-open");
  }

  function createLightbox() {
    const wrapper = document.createElement("div");
    wrapper.className = "lightbox is-hidden";
    wrapper.setAttribute("aria-hidden", "true");
    wrapper.innerHTML = `
      <div class="lightbox-backdrop" data-lightbox-close="1"></div>
      <section class="lightbox-panel" role="dialog" aria-modal="true" aria-label="Media viewer">
        <button type="button" class="lightbox-close" data-lightbox-close="1" aria-label="Close media">×</button>
        <div class="lightbox-media" id="lightbox-media">
          <div class="lightbox-toolbar" id="lightbox-image-controls">
            <button type="button" class="lightbox-zoom-btn" id="lightbox-fit-image" title="Fit image">Fit</button>
            <button type="button" class="lightbox-zoom-btn" id="lightbox-actual-size" title="Show image at full size">100%</button>
            <button type="button" class="lightbox-zoom-btn icon" id="lightbox-zoom-out" title="Zoom out">-</button>
            <button type="button" class="lightbox-zoom-btn icon" id="lightbox-zoom-in" title="Zoom in">+</button>
            <a class="lightbox-zoom-btn" id="lightbox-open-original" href="#" target="_blank" rel="noopener noreferrer">Open Original</a>
            <span class="lightbox-zoom-level" id="lightbox-zoom-level">100%</span>
          </div>
          <img id="lightbox-image" alt="Selected media">
          <video id="lightbox-video" controls preload="metadata" playsinline class="is-hidden"></video>
        </div>
        <aside class="lightbox-sidebar">
          <h3 id="lightbox-title" class="section-title" style="margin-top:0;">Media Detail</h3>
          <p id="lightbox-subtitle" class="small-muted"></p>
          <dl id="lightbox-meta" class="meta-grid"></dl>
          <p id="lightbox-notes" class="small-muted"></p>
          <div class="lightbox-actions">
            <button type="button" class="lightbox-btn" id="lightbox-toggle-recategorize">Re-categorize</button>
            <button type="button" class="lightbox-btn danger" id="lightbox-delete-photo">Delete From Project</button>
            <button type="button" class="lightbox-btn" id="lightbox-clear-override">Clear Override</button>
            <button type="button" class="lightbox-btn" id="lightbox-clear-all-overrides">Reset All Overrides</button>
            <button type="button" class="lightbox-btn" id="lightbox-export-overrides">Export Overrides CSV</button>
          </div>
          <form id="lightbox-recategorize-form" class="recat-form is-hidden">
            <div class="form-row">
              <label for="recat-component-group">Component Group</label>
              <select id="recat-component-group" name="component_group"></select>
            </div>
            <div class="form-row">
              <label for="recat-specific-component">Specific Component</label>
              <select id="recat-specific-component" name="specific_component"></select>
            </div>
            <div class="form-row">
              <label for="recat-stage">Stage</label>
              <select id="recat-stage" name="stage"></select>
            </div>
            <div class="form-row">
              <label for="recat-observed-state">Observed State</label>
              <select id="recat-observed-state" name="observed_state"></select>
            </div>
            <div class="form-row">
              <label for="recat-confidence">Confidence</label>
              <select id="recat-confidence" name="confidence"></select>
            </div>
            <div class="form-row">
              <label for="recat-tags">Tags</label>
              <input id="recat-tags" name="tags" type="text" placeholder="tag1|tag2">
            </div>
            <div class="form-row">
              <label for="recat-notes">Notes</label>
              <textarea id="recat-notes" name="notes" rows="3"></textarea>
            </div>
            <div class="lightbox-actions">
              <button type="submit" class="lightbox-btn primary">Save Override</button>
            </div>
          </form>
          <p id="lightbox-status" class="small-muted"></p>
        </aside>
      </section>
    `;
    document.body.appendChild(wrapper);

    const refs = {
      root: wrapper,
      media: wrapper.querySelector("#lightbox-media"),
      imageControls: wrapper.querySelector("#lightbox-image-controls"),
      image: wrapper.querySelector("#lightbox-image"),
      video: wrapper.querySelector("#lightbox-video"),
      fitImageBtn: wrapper.querySelector("#lightbox-fit-image"),
      actualSizeBtn: wrapper.querySelector("#lightbox-actual-size"),
      zoomOutBtn: wrapper.querySelector("#lightbox-zoom-out"),
      zoomInBtn: wrapper.querySelector("#lightbox-zoom-in"),
      openOriginalLink: wrapper.querySelector("#lightbox-open-original"),
      zoomLevel: wrapper.querySelector("#lightbox-zoom-level"),
      title: wrapper.querySelector("#lightbox-title"),
      subtitle: wrapper.querySelector("#lightbox-subtitle"),
      meta: wrapper.querySelector("#lightbox-meta"),
      notes: wrapper.querySelector("#lightbox-notes"),
      status: wrapper.querySelector("#lightbox-status"),
      toggleRecategorizeBtn: wrapper.querySelector("#lightbox-toggle-recategorize"),
      deletePhotoBtn: wrapper.querySelector("#lightbox-delete-photo"),
      clearOverrideBtn: wrapper.querySelector("#lightbox-clear-override"),
      clearAllOverridesBtn: wrapper.querySelector("#lightbox-clear-all-overrides"),
      exportOverridesBtn: wrapper.querySelector("#lightbox-export-overrides"),
      form: wrapper.querySelector("#lightbox-recategorize-form"),
      fieldComponentGroup: wrapper.querySelector("#recat-component-group"),
      fieldSpecificComponent: wrapper.querySelector("#recat-specific-component"),
      fieldStage: wrapper.querySelector("#recat-stage"),
      fieldObservedState: wrapper.querySelector("#recat-observed-state"),
      fieldConfidence: wrapper.querySelector("#recat-confidence"),
      fieldTags: wrapper.querySelector("#recat-tags"),
      fieldNotes: wrapper.querySelector("#recat-notes"),
    };

    wrapper.addEventListener("click", (event) => {
      if (event.target.closest("[data-lightbox-close]")) {
        closeLightbox();
      }
    });

    refs.image.addEventListener("load", () => {
      if (!fitLightboxOnImageLoad || lightbox.image.classList.contains("is-hidden")) {
        return;
      }
      fitLightboxOnImageLoad = false;
      fitLightboxImage();
    });

    refs.fitImageBtn.addEventListener("click", fitLightboxImage);
    refs.actualSizeBtn.addEventListener("click", setLightboxActualSize);
    refs.zoomOutBtn.addEventListener("click", () => zoomLightboxAtCenter(0.8));
    refs.zoomInBtn.addEventListener("click", () => zoomLightboxAtCenter(1.25));

    refs.media.addEventListener(
      "wheel",
      (event) => {
        if (!state.lightboxImageBase || lightbox.image.classList.contains("is-hidden")) {
          return;
        }
        event.preventDefault();
        zoomLightboxAt(event.clientX, event.clientY, event.deltaY < 0 ? 1.15 : 1 / 1.15);
      },
      { passive: false }
    );

    refs.media.addEventListener("pointerdown", (event) => {
      if (
        !state.lightboxImageBase ||
        lightbox.image.classList.contains("is-hidden") ||
        event.target.closest(".lightbox-toolbar")
      ) {
        return;
      }
      refs.media.setPointerCapture(event.pointerId);
      refs.media.classList.add("is-dragging");
      lightboxViewport.drag = {
        pointerId: event.pointerId,
        startX: event.clientX,
        startY: event.clientY,
        imageX: lightboxViewport.x,
        imageY: lightboxViewport.y,
      };
    });

    refs.media.addEventListener("pointermove", (event) => {
      const drag = lightboxViewport.drag;
      if (!drag || drag.pointerId !== event.pointerId) {
        return;
      }
      lightboxViewport.x = drag.imageX + event.clientX - drag.startX;
      lightboxViewport.y = drag.imageY + event.clientY - drag.startY;
      applyLightboxTransform();
    });

    const endLightboxDrag = (event) => {
      const drag = lightboxViewport.drag;
      if (!drag || drag.pointerId !== event.pointerId) {
        return;
      }
      lightboxViewport.drag = null;
      refs.media.classList.remove("is-dragging");
    };

    refs.media.addEventListener("pointerup", endLightboxDrag);
    refs.media.addEventListener("pointercancel", endLightboxDrag);

    refs.toggleRecategorizeBtn.addEventListener("click", () => {
      if (!state.lightboxImageBase || !cleanString(state.lightboxImageBase.media_id)) {
        return;
      }
      state.recategorizeOpen = !state.recategorizeOpen;
      renderLightbox();
    });

    refs.clearOverrideBtn.addEventListener("click", () => {
      clearCurrentPhotoOverride();
    });

    refs.deletePhotoBtn.addEventListener("click", () => {
      toggleCurrentPhotoDeletion();
    });

    refs.clearAllOverridesBtn.addEventListener("click", () => {
      clearAllPhotoOverrides();
    });

    refs.exportOverridesBtn.addEventListener("click", () => {
      exportPhotoOverridesCsv();
    });

    refs.form.addEventListener("submit", (event) => {
      event.preventDefault();
      saveCurrentPhotoOverride();
    });

    return refs;
  }

  function isLightboxPhotoVisible() {
    return (
      Boolean(state.lightboxImageBase) &&
      lightbox.image &&
      !lightbox.image.classList.contains("is-hidden") &&
      Boolean(lightbox.image.naturalWidth)
    );
  }

  function applyLightboxTransform() {
    if (!lightbox.image) {
      return;
    }
    lightbox.image.style.transform = `translate(${lightboxViewport.x}px, ${lightboxViewport.y}px) scale(${lightboxViewport.scale})`;
    if (lightbox.zoomLevel) {
      lightbox.zoomLevel.textContent = `${Math.round(lightboxViewport.scale * 100)}%`;
    }
  }

  function resetLightboxTransform() {
    lightboxViewport.scale = 1;
    lightboxViewport.x = 0;
    lightboxViewport.y = 0;
    lightboxViewport.drag = null;
    if (lightbox.image) {
      lightbox.image.style.transform = "";
    }
    if (lightbox.zoomLevel) {
      lightbox.zoomLevel.textContent = "100%";
    }
  }

  function fitLightboxImage() {
    if (!isLightboxPhotoVisible()) {
      return;
    }
    const rect = lightbox.media.getBoundingClientRect();
    const padding = 28;
    const maxWidth = Math.max(rect.width - padding * 2, 1);
    const maxHeight = Math.max(rect.height - padding * 2, 1);
    const imageWidth = lightbox.image.naturalWidth;
    const imageHeight = lightbox.image.naturalHeight;
    lightboxViewport.scale = Math.min(maxWidth / imageWidth, maxHeight / imageHeight, 1);
    lightboxViewport.x = Math.round((rect.width - imageWidth * lightboxViewport.scale) / 2);
    lightboxViewport.y = Math.round((rect.height - imageHeight * lightboxViewport.scale) / 2);
    applyLightboxTransform();
  }

  function setLightboxActualSize() {
    if (!isLightboxPhotoVisible()) {
      return;
    }
    const rect = lightbox.media.getBoundingClientRect();
    lightboxViewport.scale = 1;
    lightboxViewport.x = Math.round((rect.width - lightbox.image.naturalWidth) / 2);
    lightboxViewport.y = Math.round((rect.height - lightbox.image.naturalHeight) / 2);
    applyLightboxTransform();
  }

  function zoomLightboxAt(clientX, clientY, factor) {
    if (!isLightboxPhotoVisible()) {
      return;
    }
    const rect = lightbox.media.getBoundingClientRect();
    const pointerX = clientX - rect.left;
    const pointerY = clientY - rect.top;
    const imageX = (pointerX - lightboxViewport.x) / lightboxViewport.scale;
    const imageY = (pointerY - lightboxViewport.y) / lightboxViewport.scale;
    const nextScale = Math.min(16, Math.max(0.05, lightboxViewport.scale * factor));
    lightboxViewport.scale = nextScale;
    lightboxViewport.x = pointerX - imageX * lightboxViewport.scale;
    lightboxViewport.y = pointerY - imageY * lightboxViewport.scale;
    applyLightboxTransform();
  }

  function zoomLightboxAtCenter(factor) {
    if (!lightbox.media) {
      return;
    }
    const rect = lightbox.media.getBoundingClientRect();
    zoomLightboxAt(rect.left + rect.width / 2, rect.top + rect.height / 2, factor);
  }

  function setLightboxPhotoControlsEnabled(isEnabled) {
    [lightbox.fitImageBtn, lightbox.actualSizeBtn, lightbox.zoomOutBtn, lightbox.zoomInBtn].forEach((button) => {
      if (button) {
        button.disabled = !isEnabled;
      }
    });
    if (lightbox.media) {
      lightbox.media.classList.toggle("is-zoomable", isEnabled);
      lightbox.media.classList.remove("is-dragging");
    }
    if (!isEnabled) {
      resetLightboxTransform();
    }
  }

  function setLightboxImageSource(path, altText) {
    const src = cleanString(path || FALLBACK_IMAGE_PATH);
    if (lightbox.openOriginalLink) {
      lightbox.openOriginalLink.setAttribute("href", src);
    }
    lightbox.image.setAttribute("alt", altText || "Selected media");
    if (cleanString(lightbox.image.getAttribute("src")) === src) {
      if (!cleanString(lightbox.image.style.transform) && lightbox.image.complete) {
        requestAnimationFrame(fitLightboxImage);
      }
      return;
    }
    fitLightboxOnImageLoad = true;
    resetLightboxTransform();
    lightbox.image.setAttribute("src", src);
    if (lightbox.image.complete && lightbox.image.naturalWidth) {
      requestAnimationFrame(() => {
        if (!fitLightboxOnImageLoad) {
          return;
        }
        fitLightboxOnImageLoad = false;
        fitLightboxImage();
      });
    }
  }

  function taxonomyValues(key, fallbackValues = []) {
    const taxonomy = data.photo_taxonomy || {};
    const values = Array.isArray(taxonomy[key]) ? taxonomy[key] : [];
    const cleaned = values.map((value) => cleanString(value)).filter(Boolean);
    if (cleaned.length) {
      return cleaned;
    }
    return fallbackValues;
  }

  function fillSelectOptions(selectNode, values, selected) {
    const selectedValue = cleanString(selected);
    const options = values.slice();
    if (selectedValue && !options.includes(selectedValue)) {
      options.unshift(selectedValue);
    }
    const html = ['<option value="">-</option>']
      .concat(
        options.map((value) => {
          const isSelected = value === selectedValue;
          return `<option value="${escapeHtml(value)}"${isSelected ? " selected" : ""}>${escapeHtml(formatToken(value))}</option>`;
        })
      )
      .join("");
    selectNode.innerHTML = html;
  }

  function populateRecategorizeForm(meta) {
    fillSelectOptions(lightbox.fieldComponentGroup, taxonomyValues("component_groups"), meta.component_group);
    fillSelectOptions(lightbox.fieldSpecificComponent, taxonomyValues("specific_components"), meta.specific_component);
    fillSelectOptions(lightbox.fieldStage, taxonomyValues("stages"), meta.stage);
    fillSelectOptions(lightbox.fieldObservedState, taxonomyValues("observed_states"), meta.observed_state);
    fillSelectOptions(lightbox.fieldConfidence, taxonomyValues("confidence_values", ["low", "medium", "high"]), meta.confidence);
    lightbox.fieldTags.value = cleanString(meta.tags);
    lightbox.fieldNotes.value = cleanString(meta.notes);
  }

  function setLightboxStatus(message, tone = "info") {
    if (!lightbox.status) {
      return;
    }
    lightbox.status.textContent = message || "";
    lightbox.status.classList.remove("good", "warn", "bad", "info");
    if (message) {
      lightbox.status.classList.add(tone);
    }
  }

  function startLightboxVideoPlayback() {
    if (!state.lightboxImageBase || !lightbox.video || lightbox.video.classList.contains("is-hidden")) {
      return;
    }
    if (!cleanString(lightbox.video.getAttribute("src"))) {
      return;
    }

    const playPromise = lightbox.video.play();
    if (playPromise && typeof playPromise.catch === "function") {
      playPromise.catch(() => {
        setLightboxStatus("The browser blocked automatic playback. Press Play in the video controls.", "warn");
      });
    }
  }

  function renderLightbox() {
    const baseMeta = state.lightboxImageBase;
    if (!baseMeta) {
      return;
    }
    const effective = withOverride(baseMeta);
    const mediaId = cleanString(effective.media_id);
    const overrideKey = photoOverrideKeyForMeta(effective);
    const mediaType = resolvedMediaType(effective.media_type, effective.path);
    const currentOverride = overrideKey ? state.photoOverrides[overrideKey] || {} : {};
    const hasOverride = Boolean(overrideKey && state.photoOverrides[overrideKey]);
    const isDeleted = isDeletedPhotoOverride(currentOverride);
    const overrideTarget = cleanString(currentOverride.target_workstream);
    const deletedAt = cleanString(currentOverride.deleted_at);
    lightbox.title.textContent = buildImageCaption(effective, "Media detail");

    if (mediaType === "video") {
      lightbox.video.setAttribute("src", effective.path || FALLBACK_IMAGE_PATH);
      lightbox.video.load();
      lightbox.video.classList.remove("is-hidden");
      lightbox.image.classList.add("is-hidden");
      lightbox.image.removeAttribute("src");
      if (lightbox.openOriginalLink) {
        lightbox.openOriginalLink.setAttribute("href", cleanString(effective.path || FALLBACK_IMAGE_PATH));
      }
      if (lightbox.zoomLevel) {
        lightbox.zoomLevel.textContent = "Video";
      }
      setLightboxPhotoControlsEnabled(false);
    } else {
      if (cleanString(lightbox.video.getAttribute("src"))) {
        lightbox.video.pause();
      }
      lightbox.video.removeAttribute("src");
      lightbox.video.load();
      lightbox.video.classList.add("is-hidden");
      lightbox.image.classList.remove("is-hidden");
      setLightboxPhotoControlsEnabled(true);
      setLightboxImageSource(effective.path || FALLBACK_IMAGE_PATH, buildImageCaption(effective, "Media detail"));
    }

    const capture = [effective.captured_date, effective.captured_time].filter(Boolean).join(" ");
    lightbox.subtitle.textContent = capture ? `Captured: ${capture}` : "Capture date not set.";
    lightbox.notes.textContent = effective.notes ? `Notes: ${effective.notes}` : "";

    lightbox.meta.innerHTML = `
      <dt>Media ID</dt><dd>${escapeHtml(mediaId || "-")}</dd>
      <dt>Media Type</dt><dd>${escapeHtml(formatToken(mediaType || "-"))}</dd>
      <dt>Component Group</dt><dd>${escapeHtml(formatToken(effective.component_group || "-"))}</dd>
      <dt>Specific Component</dt><dd>${escapeHtml(formatToken(effective.specific_component || "-"))}</dd>
      <dt>Stage</dt><dd>${escapeHtml(formatToken(effective.stage || "-"))}</dd>
      <dt>Observed State</dt><dd>${escapeHtml(formatToken(effective.observed_state || "-"))}</dd>
      <dt>Confidence</dt><dd>${escapeHtml(formatToken(effective.confidence || "-"))}</dd>
      <dt>Tags</dt><dd>${escapeHtml(effective.tags || "-")}</dd>
      <dt>Override Target</dt><dd>${escapeHtml(formatToken(overrideTarget || "-"))}</dd>
      <dt>Project Status</dt><dd>${escapeHtml(isDeleted ? `Deleted${deletedAt ? ` ${formatDateTime(deletedAt)}` : ""}` : "Active")}</dd>
    `;

    lightbox.toggleRecategorizeBtn.disabled = !mediaId;
    lightbox.deletePhotoBtn.disabled = !overrideKey;
    lightbox.deletePhotoBtn.textContent = isDeleted ? "Restore Deleted" : "Delete From Project";
    lightbox.deletePhotoBtn.classList.toggle("danger", !isDeleted);
    lightbox.clearOverrideBtn.disabled = !hasOverride;
    lightbox.clearAllOverridesBtn.disabled = !Object.keys(state.photoOverrides).length;
    lightbox.exportOverridesBtn.disabled = !Object.keys(state.photoOverrides).length;

    if (!mediaId) {
      state.recategorizeOpen = false;
      lightbox.form.classList.add("is-hidden");
      lightbox.toggleRecategorizeBtn.textContent = "Re-categorize";
      lightbox.deletePhotoBtn.textContent = isDeleted ? "Restore Deleted" : "Delete From Project";
      if (!lightbox.status.textContent) {
        setLightboxStatus(
          overrideKey
            ? "This media item has no media_id, so recategorization is disabled; delete/restore is still available."
            : "This media item has no media_id or file path, so recategorization and deletion are disabled.",
          "warn"
        );
      }
      return;
    }

    lightbox.toggleRecategorizeBtn.textContent = state.recategorizeOpen ? "Hide Re-categorize" : "Re-categorize";
    lightbox.form.classList.toggle("is-hidden", !state.recategorizeOpen);
    if (state.recategorizeOpen) {
      populateRecategorizeForm(effective);
    }
    if (!lightbox.status.textContent) {
      setLightboxStatus("", "info");
    }
  }

  function openLightbox(imageKey) {
    const baseMeta = imageRegistry.get(imageKey);
    if (!baseMeta) {
      return;
    }
    if (state.itemDetailRow) {
      closeItemDetail();
    }
    state.lightboxImageBase = baseMeta;
    state.recategorizeOpen = false;
    setLightboxStatus("", "info");
    renderLightbox();
    lightbox.root.classList.remove("is-hidden");
    lightbox.root.setAttribute("aria-hidden", "false");
    document.body.classList.add("lightbox-open");
    startLightboxVideoPlayback();
  }

  function closeLightbox() {
    if (cleanString(lightbox.video.getAttribute("src"))) {
      lightbox.video.pause();
      lightbox.video.removeAttribute("src");
      lightbox.video.load();
      lightbox.video.classList.add("is-hidden");
    }
    state.lightboxImageBase = null;
    state.recategorizeOpen = false;
    fitLightboxOnImageLoad = false;
    resetLightboxTransform();
    lightbox.root.classList.add("is-hidden");
    lightbox.root.setAttribute("aria-hidden", "true");
    document.body.classList.remove("lightbox-open");
  }

  function hasSavedPhotoOverrideFields(override) {
    const systemFields = new Set(["media_id", "path", "file_name", "updated_at", "deleted", "deleted_at", "delete_reason", "action"]);
    return Object.entries(override || {}).some(([key, value]) => !systemFields.has(key) && cleanString(value));
  }

  function saveCurrentPhotoOverride() {
    const baseMeta = state.lightboxImageBase;
    if (!baseMeta) {
      return;
    }
    const mediaId = cleanString(baseMeta.media_id);
    if (!mediaId) {
      setLightboxStatus("Cannot save override: media item has no media_id.", "bad");
      return;
    }
    const existingOverride = state.photoOverrides[mediaId] || {};
    const targetWorkstream =
      state.activeView === "workstreams"
        ? cleanString(state.activeWorkstreamId)
        : cleanString(existingOverride.target_workstream);

    const override = {
      component_group: cleanString(lightbox.fieldComponentGroup.value),
      specific_component: cleanString(lightbox.fieldSpecificComponent.value),
      stage: cleanString(lightbox.fieldStage.value),
      observed_state: cleanString(lightbox.fieldObservedState.value),
      confidence: cleanString(lightbox.fieldConfidence.value),
      tags: cleanString(lightbox.fieldTags.value),
      notes: cleanString(lightbox.fieldNotes.value),
      target_workstream: targetWorkstream,
      updated_at: new Date().toISOString(),
    };

    if (!hasSavedPhotoOverrideFields(override)) {
      delete state.photoOverrides[mediaId];
      setLightboxStatus("Override cleared (no override fields set).", "warn");
    } else {
      state.photoOverrides[mediaId] = override;
      setLightboxStatus("Override saved locally. Evidence allocation refreshed for this session. Use Export Overrides CSV to persist externally.", "good");
    }
    persistPhotoOverrides();
    render();
    renderLightbox();
  }

  function toggleCurrentPhotoDeletion() {
    const baseMeta = state.lightboxImageBase;
    if (!baseMeta) {
      return;
    }
    const overrideKey = photoOverrideKeyForMeta(baseMeta);
    if (!overrideKey) {
      setLightboxStatus("Cannot delete: media item has no media_id or file path.", "bad");
      return;
    }

    const existingOverride = state.photoOverrides[overrideKey] || {};
    if (isDeletedPhotoOverride(existingOverride)) {
      const restoredOverride = { ...existingOverride, updated_at: new Date().toISOString() };
      delete restoredOverride.deleted;
      delete restoredOverride.deleted_at;
      delete restoredOverride.delete_reason;
      if (cleanString(restoredOverride.action).toLowerCase() === "delete") {
        delete restoredOverride.action;
      }

      if (hasSavedPhotoOverrideFields(restoredOverride)) {
        state.photoOverrides[overrideKey] = restoredOverride;
      } else {
        delete state.photoOverrides[overrideKey];
      }
      persistPhotoOverrides();
      state.recategorizeOpen = false;
      setLightboxStatus("Media restored to the project view.", "good");
      render();
      renderLightbox();
      return;
    }

    const caption = buildImageCaption(withOverride(baseMeta), "this media item");
    const proceed = window.confirm(
      `Delete "${caption}" from project evidence? It will be hidden from this dashboard and included in the override export for permanent cleanup.`
    );
    if (!proceed) {
      return;
    }

    const now = new Date().toISOString();
    state.photoOverrides[overrideKey] = {
      ...existingOverride,
      media_id: cleanString(baseMeta.media_id),
      path: cleanString(baseMeta.path),
      file_name: cleanString(baseMeta.file_name),
      deleted: true,
      delete_reason: "not_project_relevant",
      deleted_at: now,
      updated_at: now,
    };
    persistPhotoOverrides();
    state.recategorizeOpen = false;
    setLightboxStatus("Media deleted from the project view. Export overrides to persist this cleanup.", "good");
    render();
    renderLightbox();
  }

  function clearCurrentPhotoOverride() {
    const baseMeta = state.lightboxImageBase;
    if (!baseMeta) {
      return;
    }
    const overrideKey = photoOverrideKeyForMeta(baseMeta);
    if (!overrideKey) {
      setLightboxStatus("No media_id or file path on this media item, so there is no override to clear.", "warn");
      return;
    }
    if (!state.photoOverrides[overrideKey]) {
      setLightboxStatus("No override set for this media item.", "warn");
      return;
    }

    delete state.photoOverrides[overrideKey];
    persistPhotoOverrides();
    state.recategorizeOpen = false;
    setLightboxStatus("Override cleared.", "good");
    render();
    renderLightbox();
  }

  function clearAllPhotoOverrides() {
    const keys = Object.keys(state.photoOverrides || {});
    if (!keys.length) {
      setLightboxStatus("No overrides set.", "warn");
      return;
    }
    const proceed = window.confirm(`Clear all ${keys.length} local photo overrides?`);
    if (!proceed) {
      return;
    }
    state.photoOverrides = {};
    persistPhotoOverrides();
    state.recategorizeOpen = false;
    setLightboxStatus("All local overrides cleared.", "good");
    render();
    renderLightbox();
  }

  function csvEscape(value) {
    const text = String(value ?? "");
    if (!/[,"\n]/.test(text)) {
      return text;
    }
    return `"${text.replace(/"/g, '""')}"`;
  }

  function exportPhotoOverridesCsv() {
    const entries = Object.entries(state.photoOverrides || {});
    if (!entries.length) {
      setLightboxStatus("No overrides to export.", "warn");
      return;
    }

    const headers = [
      "media_id",
      "override_key",
      "file_name",
      "path",
      "component_group",
      "specific_component",
      "stage",
      "observed_state",
      "confidence",
      "tags",
      "notes",
      "target_workstream",
      "updated_at",
      "deleted",
      "deleted_at",
      "delete_reason",
    ];
    const lines = [headers.join(",")];

    entries
      .sort((a, b) => a[0].localeCompare(b[0]))
      .forEach(([overrideKey, override]) => {
        const overrideRow = override && typeof override === "object" ? override : {};
        const isPathKey = overrideKey.startsWith("path:");
        const mediaId = isPathKey ? cleanString(overrideRow.media_id) : overrideKey;
        const lookup = photoLookupById(mediaId) || {};
        const path = cleanString(lookup.path || overrideRow.path || (isPathKey ? overrideKey.slice(5) : ""));
        const fileName = cleanString(lookup.file_name || overrideRow.file_name || (path.split("/").pop() || ""));
        const row = [
          mediaId,
          overrideKey,
          fileName,
          path,
          cleanString(overrideRow.component_group),
          cleanString(overrideRow.specific_component),
          cleanString(overrideRow.stage),
          cleanString(overrideRow.observed_state),
          cleanString(overrideRow.confidence),
          cleanString(overrideRow.tags),
          cleanString(overrideRow.notes),
          cleanString(overrideRow.target_workstream),
          cleanString(overrideRow.updated_at),
          isDeletedPhotoOverride(overrideRow) ? "true" : "",
          cleanString(overrideRow.deleted_at),
          cleanString(overrideRow.delete_reason),
        ];
        lines.push(row.map(csvEscape).join(","));
      });

    const blob = new Blob([lines.join("\n") + "\n"], { type: "text/csv;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = `photo_recategorization_overrides_${new Date().toISOString().slice(0, 10)}.csv`;
    document.body.appendChild(anchor);
    anchor.click();
    anchor.remove();
    URL.revokeObjectURL(url);
    setLightboxStatus("Overrides CSV exported with recategorization and deletion fields.", "good");
  }

  function render() {
    resetImageRegistry();
    resetItemRegistry();
    if (state.activeView === "workstreams") {
      renderWorkstreams();
      return;
    }
    if (state.activeView === "parts") {
      renderParts();
      return;
    }
    if (state.activeView === "scout") {
      renderScout();
      return;
    }
    if (state.activeView === "tasks") {
      renderCaptureTasks();
      return;
    }
    if (state.activeView === "photos-needed") {
      renderPhotosNeeded();
      return;
    }
    if (state.activeView === "steps") {
      renderProjectSteps();
      return;
    }
    if (state.activeView === "other-builds") {
      renderOtherBuilds();
      return;
    }
    renderOverview();
  }

  applyRouteFromHash();
  render();
})();
