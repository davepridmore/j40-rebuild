(function () {
  const data = window.J40_DASHBOARD_DATA;
  const root = document.getElementById("view-root");
  const generatedAtNode = document.getElementById("generated-at");
  const tabButtons = Array.from(document.querySelectorAll("[data-view]"));
  const STORAGE_KEY = "j40.photo_recategorization_overrides.v3";
  const FALLBACK_IMAGE_PATH = "./assets/image-needed.svg";
  const PUBLIC_DASHBOARD_BASE_URL = "https://dbvg4yfpnc4tj.cloudfront.net/docs/project-control-ui/";
  const VEHICLE_MAP_VIEWER_PATH = "../../data/manual/cad/j40_reference_model/04_exports/scaffold_rev_c/j40_full_vehicle_orbit_viewer.html?v=rev-c-classic-rounded-back-windows";
  const VEHICLE_MAP_EXPORT_LINKS = [
    {
      url: "../../data/manual/cad/j40_reference_model/04_exports/scaffold_rev_c/j40_full_vehicle_scaffold_rev_c.gltf",
      label: "glTF",
    },
    {
      url: "../../data/manual/cad/j40_reference_model/04_exports/scaffold_rev_c/j40_full_vehicle_scaffold_rev_c_parts.csv",
      label: "Parts CSV",
    },
    {
      url: "../../data/manual/cad/j40_reference_model/05_reports/j40_full_vehicle_scaffold_rev_c_notes.md",
      label: "Notes",
    },
    {
      url: "../../data/manual/cad/j40_reference_model/05_reports/j40_full_vehicle_scaffold_rev_c_manifest.json",
      label: "Manifest",
    },
    {
      url: "../../data/manual/cad/j40_reference_model/05_reports/j40_full_vehicle_scaffold_rev_c_online_reference_inventory.csv",
      label: "Online References",
    },
  ];
  const AMIR_FRONT_DISC_ENTRY_IDS = new Set([
    "part_front_disc_pad_axle_set_sumitomo_20260530",
    "part_front_disc_pad_pin_hardware_kit_sumitomo_20260530",
    "part_front_brake_hose_pair",
    "part_front_caliper_rebuild_or_replace_pair",
    "part_front_rotor_service_pair",
  ]);
  const AMIR_FRONT_DISC_TASKS = [
    {
      priority: "P0",
      item: "Front disc brake pad axle set",
      action: "Ask Toyota/Land Cruiser parts counters for the Sumitomo fixed-caliper pad family 04491-60010 / 04491-60030 / 04465-35170 / 04465-YZZC0. Use the removed pad/backing plate as the sample when available; otherwise collect box/part-number photos and price only.",
      gate: "Buy only if the removed pad outline, backing ears, thickness, and rotor/caliper clearance match. Reject Prado/J200/Fortuner/V8 pads and seller-led catalog guesses.",
    },
    {
      priority: "P0",
      item: "Front pad retaining hardware kit",
      action: "Ask for BR06158K / MT 12342 style hardware, or local equivalent, containing exactly 4 pad retaining pins, 2 anti-rattle springs, and 2 pin clips.",
      gate: "Buy only if removed pins, springs, and clips match in length, diameter, shape, and installed retention. Receipt must count all three component groups separately.",
    },
    {
      priority: "P0",
      item: "Front flexible brake hoses",
      action: "Take labelled old front hoses or a written hose spec to a brake hydraulic hose shop. Quote two lower wheel hoses plus the front frame/upper hose only if that hose is actually fitted. Collect end-fitting, thread/seat, bracket-groove, hose-marking, and free-length photos.",
      gate: "Buy only complete crimped automotive brake hose assemblies, DOT/SAE J1401 or OEM-equivalent, with matching end fittings, bracket groove, free length, and lock-to-lock/droop clearance. No generic rubber hose or substitute fittings.",
    },
    {
      priority: "P0",
      item: "Front Sumitomo calipers",
      action: "Take both old calipers as cores/samples to a Land Cruiser or brake-caliper specialist. Quote professional rebuild of the originals and quote matched rebuilt/new Sumitomo-family replacements if available. Collect casting marks, side orientation, inlet/bridge-pipe/bleeder photos, and shop test terms.",
      gate: "Pay only after mechanic/user approves side-by-side match or rebuild proof: clean bores, usable/new pistons, new seals and dust boots, free bleed screws, sound bridge pipes, correct mounting ears, and bench leak/function test. Raw used calipers are cores only.",
    },
    {
      priority: "P0",
      item: "Front rotors",
      action: "Ask Land Cruiser/Toyota parts shops for a new rotor pair using old rotor measurements/sample. Collect rotor diameter, nominal thickness, minimum thickness marking, hub/register dimensions, stud pattern, box label, and return terms.",
      gate: "Buy two only after old rotor diameter/thickness, hub/register fit, stud pattern, dust-shield clearance, Sumitomo caliper clearance, and wheel clearance match. Old rotors are measurement samples only, not reuse candidates.",
    },
    {
      priority: "P1",
      item: "Front disc quote packet",
      action: "For every quote, send shop card/location, price, brand/box label, part-number photos, close-ups of the matching feature, and whether return/exchange is allowed after sample comparison.",
      gate: "No payment if any safety-critical match point is uncertain; collect quote/photos and call.",
    },
  ];

  if (!data || !root) {
    if (root) {
      root.innerHTML = '<p class="card">Dashboard data is missing. Run <code>python3 scripts/build_project_control_ui.py</code>.</p>';
    }
    return;
  }

  const state = {
    activeView: "overview",
    activeWorkstreamId: data.workstreams && data.workstreams.length ? data.workstreams[0].id : "",
    pendingSectionId: "",
    pendingItemId: "",
    photoOverrides: loadPhotoOverrides(),
    lightboxImageBase: null,
    lightboxImageKey: "",
    visualViewerKey: "",
    itemDetailRow: null,
    recategorizeOpen: false,
    imageSearch: "",
    imageComponentGroup: "",
    imageStage: "",
    imageVisibleCount: 120,
  };

  const imageRegistry = new Map();
  const imageSequences = new Map();
  const imageSequenceByKey = new Map();
  const visualRegistry = new Map();
  const visualSequences = new Map();
  const visualSequenceByKey = new Map();
  const itemRegistry = new Map();
  const itemRegistryByStableId = new Map();
  let imageKeyCounter = 0;
  let imageSequenceCounter = 0;
  let visualKeyCounter = 0;
  let visualSequenceCounter = 0;
  let itemKeyCounter = 0;
  const lightbox = createLightbox();
  const visualViewer = createVisualViewer();
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
    const copyRouteTrigger = event.target.closest("[data-copy-link-route]");
    if (copyRouteTrigger) {
      const route = copyRouteTrigger.getAttribute("data-copy-link-route");
      if (!route) {
        return;
      }
      event.preventDefault();
      event.stopPropagation();
      copyDirectLink(route, copyRouteTrigger);
      return;
    }

    const visualTrigger = event.target.closest("[data-visual-key]");
    if (visualTrigger) {
      const visualKey = visualTrigger.getAttribute("data-visual-key");
      if (!visualKey) {
        return;
      }
      event.preventDefault();
      openVisualViewer(visualKey);
      return;
    }

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

    const imageShowMoreTrigger = event.target.closest("[data-images-show-more]");
    if (imageShowMoreTrigger) {
      event.preventDefault();
      state.imageVisibleCount += 120;
      renderImagesResults();
      return;
    }

    const itemTrigger = event.target.closest("[data-item-key]");
    if (!itemTrigger) {
      return;
    }
    const itemKey = itemTrigger.getAttribute("data-item-key");
    const itemId = itemTrigger.getAttribute("data-item-id");
    if (itemId) {
      event.preventDefault();
      navigateToRoute(itemRoute(itemId));
      return;
    }
    if (!itemKey) {
      return;
    }
    event.preventDefault();
    openItemDetail(itemKey);
  });

  root.addEventListener("input", (event) => {
    const target = event.target.closest("[data-images-search]");
    if (!target || state.activeView !== "images") {
      return;
    }
    state.imageSearch = cleanString(target.value);
    state.imageVisibleCount = 120;
    renderImagesResults();
  });

  root.addEventListener("change", (event) => {
    const target = event.target.closest("[data-images-filter]");
    if (!target || state.activeView !== "images") {
      return;
    }
    if (target.getAttribute("data-images-filter") === "component-group") {
      state.imageComponentGroup = cleanString(target.value);
    } else if (target.getAttribute("data-images-filter") === "stage") {
      state.imageStage = cleanString(target.value);
    }
    state.imageVisibleCount = 120;
    renderImagesResults();
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
    if (event.key === "Escape" && state.visualViewerKey) {
      closeVisualViewer();
      return;
    }
    if (event.key === "Escape" && state.lightboxImageBase) {
      closeLightbox();
      return;
    }
    if (event.key === "Escape" && state.itemDetailRow) {
      closeItemDetail();
      return;
    }
    if (!state.lightboxImageBase || isFormControl(event.target)) {
      if (state.visualViewerKey && !isFormControl(event.target)) {
        if (event.key === "ArrowLeft") {
          event.preventDefault();
          navigateVisualViewer(-1);
        } else if (event.key === "ArrowRight") {
          event.preventDefault();
          navigateVisualViewer(1);
        }
      }
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
    } else if (event.key === "ArrowLeft") {
      event.preventDefault();
      navigateLightbox(-1);
    } else if (event.key === "ArrowRight") {
      event.preventDefault();
      navigateLightbox(1);
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
    if (state.visualViewerKey) {
      closeVisualViewer();
    }
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
      state.pendingSectionId = "";
      state.pendingItemId = "";
      refreshTabButtons();
      return false;
    }
    const routeParts = rawHash.split("/").map(cleanString).filter(Boolean);
    const [viewPart] = routeParts;
    const requestedView = cleanString(viewPart);
    const validViews = new Set(tabButtons.map((node) => cleanString(node.getAttribute("data-view"))).filter(Boolean));
    let changed = false;
    let routeIndex = 1;
    let nextSectionId = "";
    let nextItemId = "";

    if (validViews.has(requestedView) && requestedView !== state.activeView) {
      state.activeView = requestedView;
      changed = true;
    } else if (!validViews.has(requestedView)) {
      if (state.activeView !== "overview") {
        state.activeView = "overview";
        changed = true;
      }
      routeIndex = routeParts.length;
    }

    if (requestedView === "workstreams" && routeParts[routeIndex] && !["section", "item"].includes(routeParts[routeIndex])) {
      const requestedWorkstream = cleanString(routeParts[routeIndex]);
      const exists = (data.workstreams || []).some((workstream) => workstream.id === requestedWorkstream);
      if (exists && requestedWorkstream !== state.activeWorkstreamId) {
        state.activeWorkstreamId = requestedWorkstream;
        changed = true;
      }
      routeIndex += 1;
    }

    while (routeIndex < routeParts.length) {
      const key = routeParts[routeIndex];
      const value = cleanString(routeParts[routeIndex + 1]);
      if (key === "section" && value) {
        nextSectionId = value;
        routeIndex += 2;
      } else if (key === "item" && value) {
        nextItemId = value;
        routeIndex += 2;
      } else {
        routeIndex += 1;
      }
    }

    if (nextSectionId !== state.pendingSectionId) {
      state.pendingSectionId = nextSectionId;
      changed = true;
    }
    if (nextItemId !== state.pendingItemId) {
      state.pendingItemId = nextItemId;
      changed = true;
    }

    refreshTabButtons();
    return changed;
  }

  function routeBaseForView(view = state.activeView) {
    if (view === "workstreams" && state.activeWorkstreamId) {
      return `#workstreams/${encodeURIComponent(state.activeWorkstreamId)}`;
    }
    return `#${encodeURIComponent(view)}`;
  }

  function updateRouteHash(extraParts = []) {
    const suffix = extraParts
      .map((part) => encodeURIComponent(cleanString(part)))
      .filter(Boolean)
      .join("/");
    const route = `${routeBaseForView()}${suffix ? `/${suffix}` : ""}`;
    if (window.location.hash !== route) {
      history.replaceState(null, "", route);
    }
  }

  function navigateToRoute(route) {
    const normalizedRoute = cleanString(route);
    if (!normalizedRoute) {
      return;
    }
    if (window.location.hash === normalizedRoute) {
      if (applyRouteFromHash()) {
        render();
      } else {
        handlePendingRouteAfterRender();
      }
      return;
    }
    window.location.hash = normalizedRoute;
  }

  function workstreamRoute(workstreamId) {
    return `#workstreams/${encodeURIComponent(cleanString(workstreamId))}`;
  }

  function itemRoute(itemId) {
    return `#parts/item/${encodeURIComponent(cleanString(itemId))}`;
  }

  function sectionRoute(sectionId) {
    const parts = ["section", cleanString(sectionId)];
    return `${routeBaseForView()}/${parts.map(encodeURIComponent).join("/")}`;
  }

  function isLocalDashboardOrigin() {
    const hostname = cleanString(window.location.hostname).toLowerCase();
    return window.location.protocol === "file:" || hostname === "localhost" || hostname === "127.0.0.1" || hostname === "0.0.0.0" || hostname === "::1";
  }

  function dashboardAssetUrl(url) {
    const rawUrl = cleanString(url);
    return rawUrl;
  }

  function vehicleMapViewerUrl() {
    return dashboardAssetUrl(VEHICLE_MAP_VIEWER_PATH);
  }

  function absoluteRoute(route) {
    const basePath = isLocalDashboardOrigin() ? PUBLIC_DASHBOARD_BASE_URL : `${window.location.origin}${window.location.pathname}`;
    return `${basePath}${cleanString(route) || "#overview"}`;
  }

  function copyDirectLink(route, trigger) {
    const link = absoluteRoute(route);
    const applyCopiedState = () => {
      if (!trigger) {
        return;
      }
      const originalLabel = trigger.getAttribute("data-original-label") || trigger.textContent || "#";
      if (!trigger.getAttribute("data-original-label")) {
        trigger.setAttribute("data-original-label", originalLabel);
      }
      trigger.textContent = "Copied";
      trigger.classList.add("is-copied");
      window.setTimeout(() => {
        trigger.textContent = trigger.getAttribute("data-original-label") || "#";
        trigger.classList.remove("is-copied");
      }, 1300);
    };

    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(link).then(applyCopiedState).catch(() => fallbackCopyText(link, applyCopiedState));
      return;
    }
    fallbackCopyText(link, applyCopiedState);
  }

  function fallbackCopyText(text, onDone) {
    const textarea = document.createElement("textarea");
    textarea.value = text;
    textarea.setAttribute("readonly", "readonly");
    textarea.style.position = "fixed";
    textarea.style.left = "-9999px";
    document.body.appendChild(textarea);
    textarea.select();
    try {
      document.execCommand("copy");
    } catch (error) {
      window.prompt("Copy direct link", text);
    }
    textarea.remove();
    if (typeof onDone === "function") {
      onDone();
    }
  }

  function renderCopyLinkButton(route, label = "#", title = "Copy direct link") {
    const safeRoute = cleanString(route);
    if (!safeRoute) {
      return "";
    }
    return `<button type="button" class="copy-link-btn" data-copy-link-route="${escapeHtml(safeRoute)}" title="${escapeHtml(title)}" aria-label="${escapeHtml(title)}">${escapeHtml(label)}</button>`;
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

  function redactPhoneNumber(value) {
    const raw = cleanString(value);
    if (!raw) {
      return "";
    }
    if (raw.toLowerCase() === "[redacted]" || raw.toLowerCase() === "redacted") {
      return "Redacted";
    }
    return "Redacted";
  }

  function slugify(value, fallback = "section") {
    const slug = cleanString(value)
      .toLowerCase()
      .replace(/&/g, " and ")
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-+|-+$/g, "")
      .slice(0, 80);
    return slug || fallback;
  }

  function isFormControl(node) {
    const tagName = node && node.tagName ? node.tagName.toLowerCase() : "";
    return ["input", "select", "textarea"].includes(tagName) || Boolean(node && node.isContentEditable);
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
    const addLink = (candidate, label = "", options = {}) => {
      const url = cleanString(candidate);
      if (!url || seen.has(url)) {
        return;
      }
      seen.add(url);
      links.push({
        url,
        label: cleanString(label) || linkLabel(url, links.length),
        download: Boolean(options.download),
      });
    };

    if (Array.isArray(row && row.links)) {
      row.links.forEach((link) => {
        if (typeof link === "string") {
          addLink(link);
        } else if (link && typeof link === "object") {
          addLink(link.url || link.href, link.label || link.title, {
            download: link.download || link.downloadable,
          });
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

  function renderItemLink(link, index) {
    const label = cleanString(link && link.label) || `Link ${index + 1}`;
    const download = link && link.download;
    const attributes = download ? " download" : ' target="_blank" rel="noopener noreferrer"';
    return `<a class="item-link" href="${escapeHtml(link.url)}"${attributes}>${escapeHtml(label)}</a>`;
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
          .map((link, index) => renderItemLink(link, index))
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
          .map((link, index) => renderItemLink(link, index))
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
    if (workstream && workstream.id === "fabrication_handoff") {
      return [];
    }
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
    imageSequences.clear();
    imageSequenceByKey.clear();
    imageKeyCounter = 0;
    imageSequenceCounter = 0;
  }

  function resetVisualRegistry() {
    visualRegistry.clear();
    visualSequences.clear();
    visualSequenceByKey.clear();
    visualKeyCounter = 0;
    visualSequenceCounter = 0;
  }

  function resetItemRegistry() {
    itemRegistry.clear();
    itemRegistryByStableId.clear();
    itemKeyCounter = 0;
  }

  function stableItemId(row) {
    const candidates = [
      row && row.entry_id,
      row && row.source_ref,
      row && row.procurement_entry_id,
      row && row.part_id,
      row && row.order_id,
      row && row.material_id,
      row && row.package_id,
      row && row.id,
    ];
    const explicit = candidates.map(cleanString).find(Boolean);
    if (explicit) {
      return explicit;
    }
    return slugify([row && row.source, row && row.workstream, row && row.item].filter(Boolean).join(" "), "item");
  }

  function createImageSequence() {
    imageSequenceCounter += 1;
    const sequenceId = `seq_${imageSequenceCounter}`;
    imageSequences.set(sequenceId, []);
    return sequenceId;
  }

  function registerImage(baseMeta, sequenceId = "") {
    imageKeyCounter += 1;
    const imageKey = `img_${imageKeyCounter}`;
    imageRegistry.set(imageKey, baseMeta);
    if (sequenceId && imageSequences.has(sequenceId)) {
      imageSequences.get(sequenceId).push(imageKey);
      imageSequenceByKey.set(imageKey, sequenceId);
    }
    return imageKey;
  }

  function createVisualSequence() {
    visualSequenceCounter += 1;
    const sequenceId = `visual_seq_${visualSequenceCounter}`;
    visualSequences.set(sequenceId, []);
    return sequenceId;
  }

  function registerVisual(item, sequenceId = "") {
    visualKeyCounter += 1;
    const visualKey = `visual_${visualKeyCounter}`;
    visualRegistry.set(visualKey, item);
    if (sequenceId && visualSequences.has(sequenceId)) {
      visualSequences.get(sequenceId).push(visualKey);
      visualSequenceByKey.set(visualKey, sequenceId);
    }
    return visualKey;
  }

  function registerItem(row) {
    itemKeyCounter += 1;
    const itemKey = `item_${itemKeyCounter}`;
    const stableId = stableItemId(row);
    const registeredRow = { ...row, __item_stable_id: stableId };
    itemRegistry.set(itemKey, registeredRow);
    if (stableId && !itemRegistryByStableId.has(stableId)) {
      itemRegistryByStableId.set(stableId, registeredRow);
    }
    return { itemKey, stableId };
  }

  function renderItemButton(row) {
    const registered = registerItem(row);
    const directRoute = itemRoute(registered.stableId);
    return `
      <span class="item-action-cell">
        <button type="button" class="item-detail-btn" data-item-key="${escapeHtml(registered.itemKey)}" data-item-id="${escapeHtml(registered.stableId)}">
          ${escapeHtml(row.item || "-")}
        </button>
        ${renderCopyLinkButton(directRoute, "#", "Copy direct item link")}
      </span>
    `;
  }

  function prepareImage(image, fallbackCaption, options = {}) {
    const base = getBasePhotoMeta(image);
    const effective = withOverride(base);
    const imageKey = registerImage(base, cleanString(options.sequenceId));
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

  function renderImageButton(prepared, buttonClass, imageClass, loading = "eager") {
    return `
      <button type="button" class="${buttonClass}" data-image-key="${escapeHtml(prepared.key)}" title="Open full-size media">
        <img loading="${loading === "lazy" ? "lazy" : "eager"}" decoding="async" class="${imageClass}" src="${escapeHtml(prepared.path)}" alt="${escapeHtml(prepared.caption)}">
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
    const prepared = prepareImage(image, fallbackCaption, { sequenceId: options.sequenceId });
    const showCaption = options.showCaption !== false;
    const visibleCaption = cleanString(options.caption || prepared.caption);
    const figureClass = options.figureClass || "evidence-figure";
    const buttonClass = options.buttonClass || "image-open-btn";
    const imageClass = options.imageClass || "figure-image";
    const captionClass = options.captionClass || "small-muted";
    return `
      <figure class="${figureClass}">
        ${renderPreparedMedia(prepared, buttonClass, imageClass)}
        ${
          showCaption
            ? `<figcaption class="${captionClass}">${escapeHtml(visibleCaption)}</figcaption>`
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
    const sequenceId = createImageSequence();
    return `
      <div class="requirement-evidence-grid">
        ${images
          .map((image) => {
            const prepared = prepareImage(image, fallbackCaption, { sequenceId });
            return `
              <div class="requirement-evidence-item">
                ${renderPreparedMedia(prepared, "table-image-btn", "table-image")}
                <span class="table-image-note">${escapeHtml(prepared.effective.media_id || "")}</span>
              </div>
            `;
          })
          .join("")}
      </div>
    `;
  }

  function renderRequirementEvidenceStrip(requirement, options = {}) {
    const source = requirement || {};
    const images = filterVisibleImages(source.evidence_images);
    const fallbackCaption =
      options.fallbackCaption ||
      source.requirement_name ||
      source.component_or_function ||
      source.pipe_or_line ||
      source.part_name ||
      "Requirement evidence";
    const status = cleanString(source.photo_status || source.evidence_level || "photo_needed");
    const evidenceRefs = cleanString(options.evidenceRefs || source.evidence_refs || source.evidence_ref || "");
    const label = cleanString(options.label || "Evidence Images");
    const sequenceId = images.length ? createImageSequence() : "";
    const imageMarkup = images.length
      ? images
          .map((image) => {
            const prepared = prepareImage(image, fallbackCaption, { sequenceId });
            return `
              <div class="evidence-strip-item">
                ${renderPreparedMedia(prepared, "table-image-btn", "table-image")}
                <span class="table-image-note">${escapeHtml(prepared.effective.media_id || "")}</span>
              </div>
            `;
          })
          .join("")
      : `<span class="small-muted">${escapeHtml(formatToken(status))}</span>`;

    return `
      <div class="row-evidence-panel">
        <div class="row-evidence-heading">${escapeHtml(label)}</div>
        <div class="row-evidence-strip">${imageMarkup}</div>
        ${
          evidenceRefs
            ? `<details class="evidence-ref-details"><summary>Evidence refs</summary><p>${escapeHtml(evidenceRefs)}</p></details>`
            : ""
        }
      </div>
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
          <table class="requirement-table workstream-requirement-table">
            <colgroup>
              <col class="requirement-col-name">
              <col class="requirement-col-status">
              <col class="requirement-col-spec">
              <col class="requirement-col-measurements">
              <col class="requirement-col-install">
            </colgroup>
            <thead>
              <tr>
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
                    <tr class="workstream-data-row">
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
                    <tr class="row-evidence-strip-row">
                      <td colspan="5">${renderRequirementEvidenceStrip(row, {
                        fallbackCaption: requirementName,
                        evidenceRefs: row.evidence_ref,
                      })}</td>
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
      id: "BM-ISO-SM",
      part: "Small square tub-to-chassis body isolator pads",
      qty: "10 + 6 spares",
      location: "Main tub-to-chassis mount stack: middle/rear small stations plus any small front/cowl stations after station layout.",
      image: "../../photos/20260528_193054_gp_UFyTb44w.jpg",
      imageCaption: "Old small body-mount rubber samples with tape",
      spec: "Custom square flat pad 80 x 80 x 22; flat parallel faces; light edge radius/chamfer; 18.0 mm through bore for Toyota 90560-12009 style body-mount spacer/crush tube.",
      route: "Longman consolidated rubber order",
      files: [
        ["DXF", "../../data/manual/fabrication/rubber_recreation_rev_a/bm_iso_sm_square_pad_rev_a.dxf"],
        ["SVG", "../../data/manual/fabrication/rubber_recreation_rev_a/bm_iso_sm_square_pad_rev_a.svg"],
        ["Longman Spec", "../../docs/longman-rubber-order-spec-20260508.md"],
        ["Order CSV", "../../data/manual/longman_rubber_order_specs.csv"],
      ],
      notes: "Preferred shape is the simple 80 x 80 square pad. Extras cover dry-fit stacking/trim only where a station proves it needs two pads.",
    },
    {
      id: "BM-ISO-LG",
      part: "Large square tub-to-chassis body isolator pads",
      qty: "2 + 2 spares",
      location: "Main tub-to-chassis mount stack: larger front or primary load stations, final side/station confirmed during layout.",
      image: "../../photos/20260528_193054_gp_UFyTb44w.jpg",
      imageCaption: "Old body-mount rubber sample stack with tape",
      spec: "Custom square flat pad 80 x 80 x 24; flat parallel faces; light edge radius/chamfer; same compound batch as BM-ISO-SM where possible; 18.0 mm through bore for Toyota 90560-12009 style spacer.",
      route: "Longman consolidated rubber order",
      files: [
        ["DXF", "../../data/manual/fabrication/rubber_recreation_rev_a/bm_iso_lg_square_pad_rev_a.dxf"],
        ["SVG", "../../data/manual/fabrication/rubber_recreation_rev_a/bm_iso_lg_square_pad_rev_a.svg"],
        ["Longman Spec", "../../docs/longman-rubber-order-spec-20260508.md"],
        ["Order CSV", "../../data/manual/longman_rubber_order_specs.csv"],
      ],
      notes: "Large pair remains height-controlled at 24; final station map controls placement and any proven two-pad stack.",
    },
    {
      id: "FS-OVAL",
      part: "Two-hole oval front-support isolator pads",
      qty: "2",
      location: "Separate front support / nose-extension isolator positions, left and right, not the main tub body-mount stack.",
      image: "../../photos/20260502_004345_gp_yK8VYzMQ.jpg",
      imageCaption: "Front-support two-hole oval pad",
      spec: "Origin lower-left of 64 x 96 plan; outer capsule 64 wide x 96 long with R32 ends; thickness 15; through holes 12 at X32 Y16 and X32 Y80; relief pocket 36 x 18 R3 at X14 Y39; insert/boss mark 29 at X32 Y16.",
      route: "Longman consolidated rubber order; waterjet/knife/punch/moulded 2.5D pad",
      files: [
        ["DXF", "../../data/manual/fabrication/rubber_recreation_rev_a/fs_oval_front_support_pad_rev_a.dxf"],
        ["SVG", "../../data/manual/fabrication/rubber_recreation_rev_a/fs_oval_front_support_pad_rev_a.svg"],
      ],
      notes: "INSERT_MARK is not a through cut. Confirm blind pocket vs through relief.",
    },
    {
      id: "FS-STRIP-L",
      part: "Left plain underfloor body-support strip liner",
      qty: "1",
      location: "Left underfloor front-support/body-support landing; anti-squeak or body-support strip beside the front support pickup.",
      image: "../../photos/20260528_193200_gp_HICSdovA.jpg",
      imageCaption: "Old strip rubber section with tape",
      spec: "Flat strip 420 x 38 x 8; plain rubber strip only; smooth edges and flat parallel faces; no stepped section and no through-holes by default.",
      route: "Longman consolidated rubber order; first article then dry-fit",
      files: [
        ["DXF", "../../data/manual/fabrication/rubber_recreation_rev_a/fs_strip_left_template_blank_rev_a.dxf"],
        ["SVG", "../../data/manual/fabrication/rubber_recreation_rev_a/fs_strip_left_template_blank_rev_a.svg"],
      ],
      notes: "May 17 installed-location photos release the first article. Dry-fit controls only local end trim and any separate steel retainer trace.",
    },
    {
      id: "FS-STRIP-R",
      part: "Right plain underfloor body-support strip liner",
      qty: "1",
      location: "Right underfloor front-support/body-support landing; mate to the left plain strip unless dry-fit proves handed trim.",
      image: "../../photos/20260528_193253_gp_f0eQuSFA.jpg",
      imageCaption: "Old strip rubber end/section with tape",
      spec: "Same as left: flat strip 420 x 38 x 8; plain rubber strip only; use the same blank unless the right-side sample proves a handed end trim.",
      route: "Longman consolidated rubber order; first article then dry-fit",
      files: [
        ["DXF", "../../data/manual/fabrication/rubber_recreation_rev_a/fs_strip_right_template_blank_rev_a.dxf"],
        ["SVG", "../../data/manual/fabrication/rubber_recreation_rev_a/fs_strip_right_template_blank_rev_a.svg"],
      ],
      notes: "May 17 installed-location photos release the right-side first article. Dry-fit controls only local handed trim and any separate steel retainer trace.",
    },
    {
      id: "BUMP-60010-LONG",
      part: "Rear/back bump-stop rubbers - same front shape longer",
      qty: "3",
      location: "Rear/back long-family axle-to-chassis bump-stop stations, plus any Toyota-controlled front-left long station if confirmed.",
      image: "../../photos/20260531_171935_gp_BYfhqiWg.jpg",
      imageCaption: "May 31 exact front bump-stop side height/profile",
      spec: "May 31 exact front-stop rubber shape, free height 70 +/-1 for long-family stops; broad rounded/tapered rubber body with two rubber through-holes, central fixture/channel interface, and flat strike area. Rear/back stops use the same front shape made longer. Final BL/BW/P/D/fixture-channel/contact offsets come from calipers, fixture, bracket, and axle strike pad.",
      route: "Longman first article, then sample/fixture and vehicle-measurement release",
      files: [
        ["Bump Spec", "../../docs/bump-stop-fabrication-spec-20260504.md"],
        ["Longman Spec", "../../docs/longman-rubber-order-spec-20260508.md"],
        ["Order CSV", "../../data/manual/longman_rubber_order_specs.csv"],
      ],
      notes: "May 31 front-stop photos are the active shape master. May 29 photos support fixture/interface only; trace or reuse the removed metal fixture separately and let vehicle measurements release final fit.",
    },
    {
      id: "BUMP-60020-SHORT",
      part: "Exact front/right-front axle bump-stop rubber",
      qty: "1",
      location: "Axle-to-chassis bump-stop bracket: right-front station only.",
      image: "../../photos/20260531_171824_gp_HmSS2ChQ.jpg",
      imageCaption: "May 31 exact front bump-stop face/width",
      spec: "Exact May 31 front-stop construction: rubber through-holes, central fixture/channel interface, rounded/tapered body, and flat strike area, but free height 60 +/-1 for the right-front station. Do not make this at 70 unless a deliberate vehicle full-bump test releases trimming.",
      route: "Longman first article, then sample/fixture and vehicle-measurement release",
      files: [
        ["Bump Spec", "../../docs/bump-stop-fabrication-spec-20260504.md"],
        ["Longman Spec", "../../docs/longman-rubber-order-spec-20260508.md"],
        ["Order CSV", "../../data/manual/longman_rubber_order_specs.csv"],
      ],
      notes: "Right-front height is externally controlled by the 48304-60020 family references.",
    },
    {
      id: "BODY-LINER-FULL-WIDTH-HOLD",
      part: "Hold: unidentified long/full-width flat liner strips",
      qty: "Hold",
      location: "Unknown continuous body/panel liner path; possible tub-to-chassis, apron, floor crossmember, sill, or panel joint only after proof.",
      image: "../../data/manual/fabrication/rubber_recreation_rev_a/body_liner_full_width_hold_control.svg",
      imageCaption: "Hold control; no confirmed old liner photo yet",
      spec: "Possible longer flat strips are not yet captured as orderable pieces. They need full-length photos, traces, holes/slots, thickness, quantity, side/orientation, and installed function before Longman quotes them.",
      route: "hold for identification and measurement",
      files: [
        ["Workstream", "../../docs/chassis-rubbers-workstream.md"],
        ["Longman Spec", "../../docs/longman-rubber-order-spec-20260508.md"],
      ],
      notes: "Do not order until the actual pieces are found or a vehicle station proves the requirement.",
    },
    {
      id: "EXH-HGR-90917",
      part: "Hold: exhaust teardrop hanger cushion",
      qty: "Hold",
      location: "Exhaust tailpipe/rear support hanger location; hold until real fitted support geometry or sample proves it belongs in this batch.",
      image: "../../data/manual/fabrication/rubber_recreation_rev_a/exh_hgr_90917_08004_teardrop_rev_a.svg",
      imageCaption: "Teardrop exhaust cushion CAD; Toyota 90917-08004 is a shape reference",
      spec: "Optional later item only. Target outline 48 x 86, top hole 9, hanger slot 16 x 22, thickness target 22 unless a real sample proves otherwise.",
      route: "sample-match or genuine-part trace before moulding",
      files: [
        ["DXF", "../../data/manual/fabrication/rubber_recreation_rev_a/exh_hgr_90917_08004_teardrop_rev_a.dxf"],
        ["SVG", "../../data/manual/fabrication/rubber_recreation_rev_a/exh_hgr_90917_08004_teardrop_rev_a.svg"],
      ],
      notes: "Not part of the first Longman chassis-rubber quote unless an intact sample is available.",
    },
  ];

  const CHASSIS_RUBBER_LOCATION_MAP_PATH = "../../data/manual/fabrication/rubber_recreation_rev_a/chassis_rubber_location_map_rev_a.svg";
  const CHASSIS_RUBBER_CURRENT_ORDER_PREVIEW_PATH = "../../data/manual/fabrication/rubber_recreation_rev_a/chassis_rubber_current_order_preview_rev_a.svg";
  const CHASSIS_RUBBER_COMPLETE_DRAWING_PREVIEW_PATH = "../../data/manual/fabrication/rubber_recreation_rev_a/chassis_rubber_all_drawings_preview_rev_a.svg";

  const CHASSIS_RUBBER_REFERENCE_IMAGES = [
    [CHASSIS_RUBBER_LOCATION_MAP_PATH, "Vehicle location map: main body pads, front support pads/strips, bump stops, and hold-only references"],
    [CHASSIS_RUBBER_CURRENT_ORDER_PREVIEW_PATH, "Current Longman order preview: active quote and first-article rubber lines only"],
    [CHASSIS_RUBBER_COMPLETE_DRAWING_PREVIEW_PATH, "Complete SVG preview sheet for every current and hold chassis-rubber control"],
    ["../../data/manual/fabrication/rubber_recreation_rev_a/bm_iso_sm_square_pad_rev_a.svg", "BM-ISO-SM square pad SVG control"],
    ["../../data/manual/fabrication/rubber_recreation_rev_a/bm_iso_lg_square_pad_rev_a.svg", "BM-ISO-LG square pad SVG control"],
    ["../../data/manual/fabrication/rubber_recreation_rev_a/fs_oval_front_support_pad_rev_a.svg", "FS-OVAL two-hole front-support SVG control"],
    ["../../data/manual/fabrication/rubber_recreation_rev_a/fs_strip_left_template_blank_rev_a.svg", "FS-STRIP-L left plain-strip SVG control"],
    ["../../data/manual/fabrication/rubber_recreation_rev_a/fs_strip_right_template_blank_rev_a.svg", "FS-STRIP-R right plain-strip SVG control"],
    ["../../data/manual/fabrication/rubber_recreation_rev_a/bump_stop_vehicle_measurement_control.svg", "Bump-stop May 31 front-shape and vehicle measurement control"],
    ["../../data/manual/fabrication/rubber_recreation_rev_a/body_liner_full_width_hold_control.svg", "Full-width liner hold measurement control"],
    ["../../data/manual/fabrication/rubber_recreation_rev_a/exh_hgr_90917_08004_teardrop_rev_a.svg", "Exhaust hanger hold reference SVG"],
    ["../../photos/20260422_004323_gp_JD88KuWQ.jpg", "Body-off chassis body-mount pedestal close-up"],
    ["../../photos/20260422_004332_gp_7d5uYWQQ.jpg", "Central frame rail and body-mount/crossmember context"],
    ["../../photos/20260502_004215_gp_evgCLjSw.jpg", "May 2 rubber sample close reference from picker set"],
    ["../../photos/20260502_004231_gp_CfosvPIg.jpg", "May 2 body-mount/front-support rubber sample group"],
    ["../../photos/20260502_004254_gp_Hm9RR5DQ.jpg", "May 2 rubber sample with tape measurement"],
    ["../../photos/20260502_004314_gp_wuzpgNrA.jpg", "May 2 rubber sample profile reference"],
    ["../../photos/20260502_004337_gp_m2OagYpg.jpg", "May 2 rubber sample edge/profile reference"],
    ["../../photos/20260502_004401_gp_otUSjgGA.jpg", "May 2 rubber recreation sample reference"],
    ["../../photos/20260502_004413_gp_Qno8OVRg.jpg", "May 2 rubber stack hardware / seat reference"],
    ["../../photos/20260502_004419_gp_ZPXJRBzg.jpg", "May 2 rubber sample measurement reference"],
    ["../../photos/20260502_004429_gp_KJHxGcCA.jpg", "May 2 rubber body-mount sample reference"],
    ["../../photos/20260502_004437_gp_f1TySzww.jpg", "May 2 rubber body-mount close reference"],
    ["../../photos/20260502_004442_gp_7WcFHjLQ.jpg", "May 2 rubber body-mount hardware close reference"],
    ["../../photos/20260502_004454_gp_4EoNuEVA.jpg", "May 2 picked rubber thickness / tape measurement reference"],
    ["../../photos/20260517_194143_gp_CO7MuMdA.jpg", "Left underfloor strip installed-location proof"],
    ["../../photos/20260517_194633_gp_rAjY3gjg.jpg", "Right underfloor strip installed-location proof"],
    ["../../photos/20260517_194706_gp_twKRWGFA.jpg", "Installed strip/body-support tape measurement"],
    ["../../photos/20260517_193503_gp_N9nHjqXw.jpg", "Loose strip full-length measurement"],
    ["../../photos/20260517_193559_gp_NEpk1hpg.jpg", "Loose strip width close-up"],
    ["../../photos/20260517_193616_gp_1ye19BZA.jpg", "Loose strip curved-end close-up"],
    ["../../photos/20260502_004345_gp_yK8VYzMQ.jpg", "Front-support two-hole oval pad measurement photo"],
    ["../../photos/20260512_100000_user_front_support_radiator_pickups_context.png", "Front support / radiator pickup location context"],
    ["../../photos/20260531_171824_gp_HmSS2ChQ.jpg", "May 31 exact front bump-stop face/width evidence"],
    ["../../photos/20260531_171935_gp_BYfhqiWg.jpg", "May 31 exact front bump-stop side height/profile evidence"],
    ["../../photos/20260529_223605_gp_CklgF0cQ.jpg", "May 29 removed bump-stop fixture face support"],
    ["../../photos/20260529_223701_gp_wYPExcAA.jpg", "May 29 removed bump-stop fixture side support"],
    ["../../photos/20260502_004222_gp_PKRe5HSQ.jpg", "Superseded bump-stop fragment context only"],
    ["../../photos/20260502_004201_gp_zfUSmKJg.jpg", "Superseded bump-stop vertical/scale context only"],
    ["../../photos/20260422_004254_gp_SplHLSYA.jpg", "Rear axle/chassis bump-stop station context"],
    ["../../photos/20260501_193841_gp_ZwpHFiMA.jpg", "Front axle/chassis bump-stop station context"],
  ];

  const CHASSIS_RUBBER_COVERAGE_ROWS = [
    {
      family: "Main tub-to-chassis body pads",
      current: "BM-ISO-SM 10 + 6 spares, BM-ISO-LG 2 + 2 spares",
      basis: "Toyota EPC-style rows list NO.1-NO.5 body-mount cushions, spacers, shims, and hardware; aftermarket kits are split by early/late 40-series year ranges.",
      decision: "Covered in the Longman bundle as simple function-first 80 x 80 square pads because the vehicle photos do not prove shaped rubber sockets. Extra pads are for dry-fit stacking only where a station proves it. Keep OE/reproduction kit rows reference-only unless the route is deliberately changed.",
    },
    {
      family: "Front support / nose extension isolators",
      current: "FS-OVAL x2 plus FS-STRIP-L/R first articles",
      basis: "May 2 and May 17 measured photos identify the two-hole oval pads and the left/right 420 x 38 x 8 plain strip pair.",
      decision: "Covered. Do not substitute the main body pads here; dry-fit only controls end trim, retainer reuse, and caliper confirmation.",
    },
    {
      family: "Axle-to-chassis bump stops",
      current: "BUMP-60010-LONG x3, BUMP-60020-SHORT x1",
      basis: "May 31 exact front-stop photos show the representative construction: broad molded rubber, two rubber through-holes, and a central fixture/channel interface; rear/back stops use the same shape made longer, while Toyota references keep the 70 mm long / 60 mm right-front height split.",
      decision: "Covered as first articles. The preview keeps the rubber through-holes visible and calls out sample, fixture, bracket, and strike-pad measurement release.",
    },
    {
      family: "Full-width flat body/panel liners",
      current: "BODY-LINER-FULL-WIDTH-HOLD",
      basis: "No complete installed path or actual strip trace exists yet.",
      decision: "Not required for the current order until an actual liner/path proves quantity, dimensions, holes/slots, and function.",
    },
    {
      family: "Exhaust hanger cushion",
      current: "EXH-HGR-90917 hold/reference only",
      basis: "Teardrop drawing is a Toyota-style shape reference, not a measured fitted part.",
      decision: "Not part of the chassis/body Longman quote unless sample or installed support geometry is captured.",
    },
  ];

  function chassisRubberAutoReferenceImages() {
    const lookup = data.photo_lookup || {};
    return Object.values(lookup)
      .filter((row) => {
        const component = cleanString(row && row.specific_component).toLowerCase();
        const tags = cleanString(row && row.tags).toLowerCase();
        return component === "rubber_parts_recreation_samples" || (tags.includes("rubber") && tags.includes("body_mount"));
      })
      .sort((left, right) => {
        const leftKey = `${cleanString(left.captured_date)} ${cleanString(left.captured_time)} ${cleanString(left.file_name)}`;
        const rightKey = `${cleanString(right.captured_date)} ${cleanString(right.captured_time)} ${cleanString(right.file_name)}`;
        return leftKey.localeCompare(rightKey);
      })
      .map((row) => [
        cleanString(row.path),
        cleanString(row.notes) || `Rubber recreation sample: ${cleanString(row.file_name)}`,
      ]);
  }

  function chassisRubberReferenceImages() {
    const seenMedia = new Set();
    const seenCaptions = new Set();
    return [...CHASSIS_RUBBER_REFERENCE_IMAGES, ...chassisRubberAutoReferenceImages()].filter(([path, caption]) => {
      const cleanPath = cleanString(path);
      const mediaKey = cleanPath.split(/[?#]/)[0].split("/").pop().toLowerCase();
      const captionKey = cleanString(caption).toLowerCase().replace(/\s+/g, " ");
      if (!mediaKey || seenMedia.has(mediaKey) || (captionKey && seenCaptions.has(captionKey))) {
        return false;
      }
      seenMedia.add(mediaKey);
      if (captionKey) {
        seenCaptions.add(captionKey);
      }
      return true;
    });
  }

  const LONGMAN_RUBBER_3D_VISUAL_PATH = "../../data/manual/fabrication/longman_rubber_order_20260508/longman_rubber_order_20260508_3d_visualisation.html";
  function longmanRubber3dVisual(partId) {
    return `${LONGMAN_RUBBER_3D_VISUAL_PATH}?focus=${encodeURIComponent(partId)}`;
  }

  const CHASSIS_RUBBER_ORIGINAL_MEDIA_IDS = {
    "BM-ISO-SM": ["20260528_193054_gp_UFyTb44w", "20260502_004231_gp_CfosvPIg"],
    "BM-ISO-LG": ["20260528_193054_gp_UFyTb44w", "20260502_004231_gp_CfosvPIg"],
    "FS-OVAL": ["20260502_004345_gp_yK8VYzMQ", "20260502_004231_gp_CfosvPIg"],
    "FS-STRIP-L": ["20260528_193200_gp_HICSdovA", "20260517_194143_gp_CO7MuMdA", "20260517_193503_gp_N9nHjqXw"],
    "FS-STRIP-R": ["20260528_193253_gp_f0eQuSFA", "20260517_194633_gp_rAjY3gjg", "20260517_193612_gp_JmbfR0Tw"],
    "BUMP-60010-LONG": ["20260529_223605_gp_CklgF0cQ", "20260529_223701_gp_wYPExcAA"],
    "BUMP-60020-SHORT": ["20260529_223605_gp_CklgF0cQ", "20260529_223701_gp_wYPExcAA"],
  };

  const CHASSIS_RUBBER_DRAWING_FILE_MAP = {
    "BM-ISO-SM": {
      svg: "../../data/manual/fabrication/rubber_recreation_rev_a/bm_iso_sm_square_pad_rev_a.svg",
      dxf: "../../data/manual/fabrication/rubber_recreation_rev_a/bm_iso_sm_square_pad_rev_a.dxf",
      scad: "../../data/manual/fabrication/rubber_recreation_rev_a/models_3d/bm_iso_sm_square_pad.scad",
      visual: longmanRubber3dVisual("BM-ISO-SM"),
    },
    "BM-ISO-LG": {
      svg: "../../data/manual/fabrication/rubber_recreation_rev_a/bm_iso_lg_square_pad_rev_a.svg",
      dxf: "../../data/manual/fabrication/rubber_recreation_rev_a/bm_iso_lg_square_pad_rev_a.dxf",
      scad: "../../data/manual/fabrication/rubber_recreation_rev_a/models_3d/bm_iso_lg_square_pad.scad",
      visual: longmanRubber3dVisual("BM-ISO-LG"),
    },
    "FS-OVAL": {
      svg: "../../data/manual/fabrication/rubber_recreation_rev_a/fs_oval_front_support_pad_rev_a.svg",
      dxf: "../../data/manual/fabrication/rubber_recreation_rev_a/fs_oval_front_support_pad_rev_a.dxf",
      scad: "../../data/manual/fabrication/rubber_recreation_rev_a/models_3d/fs_oval_front_support_pad.scad",
      visual: longmanRubber3dVisual("FS-OVAL"),
    },
    "FS-STRIP-L": {
      svg: "../../data/manual/fabrication/rubber_recreation_rev_a/fs_strip_left_template_blank_rev_a.svg",
      dxf: "../../data/manual/fabrication/rubber_recreation_rev_a/fs_strip_left_template_blank_rev_a.dxf",
      scad: "../../data/manual/fabrication/rubber_recreation_rev_a/models_3d/fs_strip_l_plain_strip.scad",
      visual: longmanRubber3dVisual("FS-STRIP-L"),
    },
    "FS-STRIP-R": {
      svg: "../../data/manual/fabrication/rubber_recreation_rev_a/fs_strip_right_template_blank_rev_a.svg",
      dxf: "../../data/manual/fabrication/rubber_recreation_rev_a/fs_strip_right_template_blank_rev_a.dxf",
      scad: "../../data/manual/fabrication/rubber_recreation_rev_a/models_3d/fs_strip_r_plain_strip.scad",
      visual: longmanRubber3dVisual("FS-STRIP-R"),
    },
    "BUMP-60010-LONG": {
      svg: "../../data/manual/fabrication/rubber_recreation_rev_a/bump_stop_vehicle_measurement_control.svg",
      dxf: "../../data/manual/fabrication/rubber_recreation_rev_a/bump_stop_vehicle_measurement_control.dxf",
      scad: "../../data/manual/fabrication/rubber_recreation_rev_a/models_3d/b_60010_long_measurement_model.scad",
      visual: longmanRubber3dVisual("BUMP-60010-LONG"),
    },
    "BUMP-60020-SHORT": {
      svg: "../../data/manual/fabrication/rubber_recreation_rev_a/bump_stop_vehicle_measurement_control.svg",
      dxf: "../../data/manual/fabrication/rubber_recreation_rev_a/bump_stop_vehicle_measurement_control.dxf",
      scad: "../../data/manual/fabrication/rubber_recreation_rev_a/models_3d/b_60020_short_measurement_model.scad",
      visual: longmanRubber3dVisual("BUMP-60020-SHORT"),
    },
    "BODY-LINER-FULL-WIDTH-HOLD": {
      svg: "../../data/manual/fabrication/rubber_recreation_rev_a/body_liner_full_width_hold_control.svg",
      dxf: "../../data/manual/fabrication/rubber_recreation_rev_a/body_liner_full_width_hold_control.dxf",
    },
    "EXH-HGR-90917": {
      svg: "../../data/manual/fabrication/rubber_recreation_rev_a/exh_hgr_90917_08004_teardrop_rev_a.svg",
      dxf: "../../data/manual/fabrication/rubber_recreation_rev_a/exh_hgr_90917_08004_teardrop_rev_a.dxf",
      scad: "../../data/manual/fabrication/rubber_recreation_rev_a/models_3d/exh_hgr_90917_teardrop_cushion.scad",
      visual: longmanRubber3dVisual("EXH-HGR-90917"),
    },
  };

  const CHASSIS_RUBBER_SPEC_ROW_BY_ID = Object.fromEntries(CHASSIS_RUBBER_SPEC_ROWS.map((row) => [row.id, row]));

  function chassisRubberStaticSpec(rowOrId) {
    const orderId = cleanString(typeof rowOrId === "string" ? rowOrId : rowOrId && (rowOrId.order_id || rowOrId.id)).toUpperCase();
    return CHASSIS_RUBBER_SPEC_ROW_BY_ID[orderId] || null;
  }

  function chassisRubberVehicleLocation(row) {
    return cleanString(row && (row.vehicle_location || row.location)) || cleanString(chassisRubberStaticSpec(row)?.location);
  }

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

  function chassisRubberDrawingFiles(rowOrId) {
    const orderId = cleanString(typeof rowOrId === "string" ? rowOrId : rowOrId && (rowOrId.order_id || rowOrId.id)).toUpperCase();
    return CHASSIS_RUBBER_DRAWING_FILE_MAP[orderId] || null;
  }

  function preferredChassisRubberOriginalImage(row) {
    const orderId = cleanString(row && row.order_id).toUpperCase();
    const evidenceImages = Array.isArray(row && row.evidence_images) ? row.evidence_images : [];
    const evidenceById = Object.fromEntries(evidenceImages.map((image) => [cleanString(image && image.media_id), image]));
    for (const mediaId of CHASSIS_RUBBER_ORIGINAL_MEDIA_IDS[orderId] || []) {
      if (evidenceById[mediaId]) {
        return evidenceById[mediaId];
      }
    }
    if (row && row.image && cleanString(row.image.path).includes("/photos/")) {
      return row.image;
    }
    return evidenceImages.length ? evidenceImages[0] : null;
  }

  function renderChassisRubberOrderImage(row) {
    const drawingFiles = chassisRubberDrawingFiles(row);
    const originalImage = preferredChassisRubberOriginalImage(row);
    const previewPath = cleanString(drawingFiles && (drawingFiles.preview || drawingFiles.svg));
    const secondaryPreviewLabel = previewPath
      ? cleanString(drawingFiles && drawingFiles.preview)
        ? "3D visual"
        : "drawing preview"
      : "";
    const image = originalImage
      ? originalImage
      : previewPath
        ? {
          path: previewPath,
          caption: `${cleanString(row.order_id) || "Rubber"} ${secondaryPreviewLabel || "reference"}`,
          media_id: `${cleanString(row.order_id).toLowerCase()}_svg`,
          media_type: "photo",
        }
      : row && row.image
        ? row.image
        : {};
    const previewLink = originalImage && previewPath ? previewPath : "";
    const prepared = prepareImage(image, row.part || row.order_id || "Rubber order line");
    const mediaClass = originalImage || previewPath ? "table-image table-image-contain" : "table-image";
    const imageNote = originalImage
      ? "Old/sample rubber photo"
      : secondaryPreviewLabel === "drawing preview"
        ? "Drawing preview"
        : secondaryPreviewLabel
        ? secondaryPreviewLabel
        : "Reference";
    return `
      <td class="table-image-cell">
        ${renderPreparedMedia(prepared, "table-image-btn", mediaClass)}
        <span class="table-image-note">${escapeHtml(imageNote)}</span>
        ${previewLink ? `<div class="small-muted"><a href="${escapeHtml(previewLink)}" target="_blank" rel="noopener noreferrer">${escapeHtml(secondaryPreviewLabel)}</a></div>` : ""}
      </td>
    `;
  }

  function renderChassisRubberDrawingLinks(row) {
    const files = chassisRubberDrawingFiles(row);
    if (!files) {
      return "";
    }
    return `
      <div class="item-links chassis-rubber-drawing-links">
        ${files.visual ? renderItemLink({ url: files.visual, label: "3D Visual" }, 0) : ""}
        ${files.scad ? renderItemLink({ url: files.scad, label: "SCAD", download: true }, 1) : ""}
        ${files.svg ? renderItemLink({ url: files.svg, label: "SVG" }, 2) : ""}
        ${files.dxf ? renderItemLink({ url: files.dxf, label: "DXF", download: true }, 3) : ""}
      </div>
    `;
  }

  function fallbackChassisRubberOrderRows() {
    return CHASSIS_RUBBER_SPEC_ROWS.map((row) => ({
      order_id: row.id,
      part: row.part,
      vehicle_location: row.location,
      required_qty: row.qty,
      optional_spare_qty: "",
      spec: row.spec,
      holes_or_inserts: "",
      material: "New black EPDM or NR/SBR automotive mount rubber, Shore A 60 +/-5",
      release_state: row.route,
      photo_refs: "",
      notes: row.notes,
      image: {
        path: row.image,
        caption: row.imageCaption || row.part,
        media_id: row.id,
        media_type: "photo",
      },
    }));
  }

  function renderChassisRubberCompleteDrawingPreview() {
    const currentImage = {
      path: CHASSIS_RUBBER_CURRENT_ORDER_PREVIEW_PATH,
      caption: "Current Longman order SVG preview",
      media_id: "chassis_rubber_current_order_preview_rev_a",
      media_type: "photo",
    };
    const completeImage = {
      path: CHASSIS_RUBBER_COMPLETE_DRAWING_PREVIEW_PATH,
      caption: "Complete chassis-rubber SVG drawing preview",
      media_id: "chassis_rubber_all_drawings_preview_rev_a",
      media_type: "photo",
    };
    const preparedCurrent = prepareImage(currentImage, currentImage.caption);
    const preparedComplete = prepareImage(completeImage, completeImage.caption);
    return `
      <div class="chassis-rubber-preview-block">
        <div class="chassis-rubber-preview-copy">
          <strong>Current Order Preview</strong>
          <span>Shows only the active Longman quote and first-article lines: square body pads, front-support oval, left/right strips, and long/short bump stops following the May 31 front-stop shape.</span>
        </div>
        ${renderPreparedMedia(preparedCurrent, "table-image-btn chassis-rubber-preview-btn", "table-image table-image-contain chassis-rubber-preview-image")}
      </div>
      <div class="chassis-rubber-preview-block">
        <div class="chassis-rubber-preview-copy">
          <strong>Complete SVG Preview</strong>
          <span>Shows every current order line and hold/reference control together: square body pads, front-support oval, left/right strips, long/short bump stops with rubber through-hole and fixture-channel controls, full-width liner hold, and exhaust hanger hold.</span>
        </div>
        ${renderPreparedMedia(preparedComplete, "table-image-btn chassis-rubber-preview-btn", "table-image table-image-contain chassis-rubber-preview-image")}
      </div>
    `;
  }

  function renderChassisRubberCoverageCheck() {
    return `
      <div class="chassis-rubber-coverage-block">
        <div class="chassis-rubber-coverage-copy">
          <strong>Coverage / Kit Check</strong>
          <span>Toyota current GR Heritage parts list does not expose a complete chassis-rubber kit in this area. EPC-style Toyota listings and aftermarket kits confirm the normal body-mount families exist, but the active route stays as one Longman rubber bundle until a complete matched kit is deliberately selected.</span>
        </div>
        <div class="table-wrap requirement-table-wrap chassis-rubber-coverage-table-wrap">
          <table class="requirement-table chassis-rubber-coverage-table">
            <thead>
              <tr>
                <th>Family</th>
                <th>Current Coverage</th>
                <th>Basis</th>
                <th>Decision</th>
              </tr>
            </thead>
            <tbody>
              ${CHASSIS_RUBBER_COVERAGE_ROWS.map((row) => `
                <tr>
                  <td><strong>${escapeHtml(row.family)}</strong></td>
                  <td>${escapeHtml(row.current)}</td>
                  <td>${escapeHtml(row.basis)}</td>
                  <td>${escapeHtml(row.decision)}</td>
                </tr>
              `).join("")}
            </tbody>
          </table>
        </div>
      </div>
    `;
  }

  function renderChassisRubberConsolidatedSpec(rows) {
    const sourceRows = Array.isArray(rows) && rows.length ? rows : fallbackChassisRubberOrderRows();
    const holdRows = sourceRows.filter((row) => {
      const qty = cleanString(row.required_qty).toLowerCase();
      const state = cleanString(row.release_state).toLowerCase();
      return qty === "hold" || state.includes("hold");
    });
    const currentRows = sourceRows.filter((row) => !holdRows.includes(row));
    const orderedRows = [...currentRows, ...holdRows];
    return `
      <article class="card pipe-requirements-card">
        <div class="detail-header">
          <h3>Consolidated Longman Rubber Order</h3>
          <div class="chip-row">
            ${chip("1 supplier request")}
            ${chip(`${currentRows.length} quote lines`)}
            ${holdRows.length ? chip(`${holdRows.length} holds`) : ""}
            ${chip("3D + 2D + location assets")}
            ${chip("All dimensions mm")}
            ${chip("Shore A 60 +/-5")}
          </div>
        </div>
        <p class="small-muted">Send this as one Longman quote/order bundle. The rows below are line items inside that single supplier request, not separate custom rubber orders. Hold rows stay in the pack only as reference controls and are not current production quantities.</p>
        <p class="small-muted">Body/front-support rubbers: new black solid EPDM or NR/SBR automotive mount rubber, Shore A 60 +/-5. Main body isolators are now function-first custom square pads, not circular/register bushings, because the chassis/tub photos do not prove a shaped rubber socket. Steel cup/seat washers, sleeves, shims, bolts, and captive-thread repairs are separate from the Longman rubber order. Bump stops: public OEM/catalog sources confirm the Toyota part numbers, applications, and 70 mm / 60 mm height split, but not the Toyota mould drawing. Use the May 31 exact front-stop construction: broad rounded/tapered rubber body, two rubber through-holes, central fixture/channel interface, flat strike area, vehicle bracket measurements, and axle contact measurements. Rear/back stops are the same shape made longer. Reject tyre rubber, crumb rubber, sponge, mixed offcuts, salvage rubber, unmarked compound, washer stacks, simple cut blocks, universal bump stops, or replacements that omit the through-hole and fixture/channel layout.</p>
        <p class="small-muted">Current supplier pack: <a href="../../docs/longman-rubber-order-spec-20260508.md">Longman rubber order spec</a>, <a href="../../data/manual/longman_rubber_order_specs.csv">Longman order CSV</a>, <a href="../../docs/chassis-rubbers-workstream.md">chassis rubbers workstream</a>, <a href="${CHASSIS_RUBBER_CURRENT_ORDER_PREVIEW_PATH}">current order preview</a>, <a href="${CHASSIS_RUBBER_LOCATION_MAP_PATH}">vehicle location map</a>, <a href="${CHASSIS_RUBBER_COMPLETE_DRAWING_PREVIEW_PATH}">complete SVG preview</a>, <a href="../../data/manual/fabrication/longman_rubber_order_20260508/longman_rubber_order_20260508_3d_visualisation.html">3D visualisation</a>, and <a href="../../data/manual/fabrication/rubber_recreation_rev_a/models_3d/j40_rubber_models_master.scad">OpenSCAD master model</a>.</p>
        ${renderChassisRubberCoverageCheck()}
        ${renderChassisRubberCompleteDrawingPreview()}
        <div class="table-wrap requirement-table-wrap">
          <table class="requirement-table chassis-rubber-spec-table">
            <thead>
              <tr>
                <th>Preview</th>
                <th>Line</th>
                <th>Qty</th>
                <th>Location</th>
                <th>Rubber Definition</th>
                <th>3D / Edges</th>
                <th>Holes / Inserts</th>
                <th>Material</th>
                <th>Files / Release</th>
              </tr>
            </thead>
            <tbody>
              ${orderedRows
                .map((row) => {
                  const qtyBits = [
                    row.required_qty ? `Required: ${row.required_qty}` : "",
                    row.optional_spare_qty ? `Spare: ${row.optional_spare_qty}` : "",
                  ].filter(Boolean);
                  const isHold = holdRows.includes(row);
                  const geometryCell = [
                    renderScoutField("Envelope", row.envelope_3d_mm),
                    renderScoutField("Edges", row.edge_profile),
                  ].join("") || "-";
                  const location = chassisRubberVehicleLocation(row);
                  return `
                    <tr>
                      ${renderChassisRubberOrderImage(row)}
                      <td class="scout-line-cell">
                        <strong>${escapeHtml(row.part || row.order_id || "-")}</strong>
                        <div class="small-muted">${escapeHtml(row.order_id || "")}</div>
                        ${statusChip(isHold ? "hold/reference only" : "current order line")}
                      </td>
                      <td>${escapeHtml(qtyBits.join(" / ") || "-")}</td>
                      <td>${escapeHtml(location || "-")}</td>
                      <td>${escapeHtml(row.spec)}</td>
                      <td>${geometryCell}</td>
                      <td>${escapeHtml(row.holes_or_inserts || "-")}</td>
                      <td>${escapeHtml(row.material || "-")}</td>
                      <td class="scout-notes-cell">
                        ${renderChassisRubberDrawingLinks(row)}
                        ${statusChip(row.release_state || "open")}
                        ${renderScoutField("Basis", row.photo_refs)}
                        ${renderScoutField("Notes", row.notes)}
                      </td>
                    </tr>
                  `;
                })
                .join("")}
            </tbody>
          </table>
        </div>
        <p class="small-muted">Tolerances: square body pad length/width +/-1.0, height +/-0.5, faces parallel <=0.5; body-pad bore 18.0 +0.5/-0.0 for Toyota 90560-12009 style spacer. Sleeve set is qty 6, 48.1 mm length, M10 clearance ID 10.8-11.0 if locally fabricated, with OD copied from old/OE spacer. FS-OVAL outside +/-1.0, hole position +/-0.5, thickness +/-0.5. FS-STRIP-L/R first articles are 420 x 38 x 8 mm with only dry-fit trim pending. Bump stops: height +/-1, rubber through-hole pitch/diameter and fixture/channel features +/-0.5 after sample/fixture/vehicle release, contact centre +/-5; fixture retention must survive compression.</p>
        <p class="small-muted">Remaining holds: possible full-width flat liners need full-length photos/traces before any quote; EXH-HGR-90917 needs a genuine sample or intact original to confirm side profile, insert depth, exact thickness, and reinforcement before local moulding. FS-STRIP-L/R are current first-article order lines at 420 x 38 x 8 mm; dry-fit controls only local end trim and any separate steel retainer trace. Bump stops need May 31 front-stop sample/photo calipers, removed fixture trace, BL/BW/P/D/fixture-channel/X-Y/G/F values, fabricator side/profile sketch, rubber through-hole layout, material declaration, and first-article compression recovery check before mould release.</p>
      </article>
    `;
  }

  function rubberOrderPriorityRank(row) {
    const priority = cleanString(row && row.priority).toUpperCase();
    const required = cleanString(row && row.required_for_current_build).toUpperCase();
    const route = cleanString(row && row.route).toLowerCase();
    if (priority.includes("P0_NOW")) return 0;
    if (priority.includes("P0_RECEIPT")) return 1;
    if (priority.includes("P1_NOW")) return 2;
    if (required === "YES") return 3;
    if (priority.includes("P1_INSPECT")) return 4;
    if (priority.includes("P2_INSPECT")) return 5;
    if (route.includes("no_active") || priority.includes("P6")) return 7;
    if (priority.includes("P2_DEFER")) return 8;
    return 6;
  }

  function rubberOrderCategoryLabel(value) {
    const raw = cleanString(value);
    const labels = {
      body_sealing: "Body Sealing",
      body_weatherstrip: "Body Weatherstrip",
      brakes: "Brakes",
      chassis_rubbers: "Chassis Rubbers",
      clutch_hydraulics: "Clutch",
      cooling: "Cooling",
      engine_air_intake: "Air Intake",
      engine_controls: "Engine Controls",
      exhaust: "Exhaust",
      fuel_system: "Fuel",
      hvac: "HVAC",
      interior_controls: "Interior Controls",
      powertrain_mounts: "Powertrain Mounts",
      sealing_grommets: "Grommets",
      steering: "Steering",
      suspension_ironman: "Suspension",
    };
    return labels[raw] || formatToken(raw || "rubber");
  }

  function rubberOrderStatusLabel(row) {
    const priority = cleanString(row && row.priority);
    const required = cleanString(row && row.required_for_current_build);
    const route = cleanString(row && row.route);
    const parts = [priority, required ? `Current build: ${required}` : "", route].filter(Boolean);
    return parts.join(" / ");
  }

  function renderRubberOrderLinkedFiles(value) {
    const files = cleanString(value)
      .split(/[;|]/)
      .map((item) => item.trim())
      .filter(Boolean)
      .slice(0, 5);
    if (!files.length) return "";
    return `
      <div class="item-links compact-links">
        ${files
          .map((file) => {
            const href = file.startsWith("http") ? file : `../../${file}`;
            return `<a class="item-link" href="${escapeHtml(href)}">${escapeHtml(file.split("/").pop() || file)}</a>`;
          })
          .join("")}
      </div>
    `;
  }

  function renderCompleteJ40RubberCoverage(rows) {
    const source = Array.isArray(rows) ? rows.filter((row) => row && cleanString(row.rubber_order_id)) : [];
    if (!source.length) return "";
    const orderedRows = [...source].sort((a, b) => {
      const priorityDelta = rubberOrderPriorityRank(a) - rubberOrderPriorityRank(b);
      if (priorityDelta) return priorityDelta;
      return cleanString(a.rubber_order_id).localeCompare(cleanString(b.rubber_order_id));
    });
    const requiredNow = source.filter((row) => cleanString(row.required_for_current_build).toUpperCase() === "YES").length;
    const currentOrConditional = source.filter((row) => {
      const required = cleanString(row.required_for_current_build).toUpperCase();
      return required === "YES" || required === "CONDITIONAL" || required === "LATER_OR_CONDITIONAL";
    }).length;
    const buyNow = source.filter((row) => cleanString(row.priority).toUpperCase().includes("NOW")).length;
    const deferred = source.filter((row) => cleanString(row.priority).toUpperCase().includes("DEFER")).length;
    const categories = new Set(source.map((row) => cleanString(row.workstream_category)).filter(Boolean));
    return `
      <article class="card pipe-requirements-card">
        <div class="detail-header">
          <h3>Complete J40 Rubber Coverage</h3>
          <div class="chip-row">
            ${chip(`${source.length} rubber rows`)}
            ${chip(`${requiredNow} current-build`)}
            ${chip(`${currentOrConditional} current/conditional`)}
            ${chip(`${buyNow} buy/lock now`)}
            ${chip(`${deferred} deferred`)}
            ${chip(`${categories.size} categories`)}
          </div>
        </div>
        <p class="small-muted">This is the all-rubbers control layer behind the chassis mount pack. The Longman table above is only the body/chassis custom-rubber bundle; this matrix keeps every J40 rubber, hose, seal, boot, grommet, bushing, mount, weatherstrip, bump stop, HVAC rubber, and hanger in one buy gate so duplicate or premature purchases are visible.</p>
        <div class="table-wrap requirement-table-wrap">
          <table class="requirement-table all-rubber-coverage-table">
            <thead>
              <tr>
                <th>Order</th>
                <th>Category</th>
                <th>Priority / Gate</th>
                <th>Quantity</th>
                <th>Ordering Spec</th>
                <th>Material / Measurement Control</th>
                <th>Source Files</th>
              </tr>
            </thead>
            <tbody>
              ${orderedRows
                .map((row) => `
                  <tr>
                    <td class="scout-line-cell">
                      <strong>${escapeHtml(row.rubber_order_id)}</strong>
                      <div class="small-muted">${escapeHtml(row.item_group || "")}</div>
                    </td>
                    <td>${escapeHtml(rubberOrderCategoryLabel(row.workstream_category))}</td>
                    <td>
                      ${statusChip(rubberOrderStatusLabel(row))}
                      ${renderScoutField("Pre-order gate", row.pre_order_gate)}
                    </td>
                    <td>${escapeHtml(row.quantity_to_order || "-")}</td>
                    <td>${escapeHtml(row.ordering_spec || "-")}</td>
                    <td>
                      ${renderScoutField("Material", row.material_spec)}
                      ${renderScoutField("Measure", row.measurements_required_before_order)}
                      ${row.notes ? `<div class="small-muted requirement-material">${escapeHtml(row.notes)}</div>` : ""}
                    </td>
                    <td>
                      ${renderScoutField("Rows", row.source_rows)}
                      ${renderRubberOrderLinkedFiles(row.linked_files)}
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

  function renderChassisRubberReferenceImages() {
    const sequenceId = createImageSequence();
    const referenceImages = chassisRubberReferenceImages();
    return `
      <article class="card pipe-requirements-card">
        <div class="detail-header">
          <h3>Curated Context Images</h3>
          <div class="chip-row">${chip(`${referenceImages.length} Images`)}</div>
        </div>
        <p class="small-muted">Trimmed to drawings, location proof, and measurement photos that support the chassis-rubber order. Weak exhaust/frame context photos are kept out unless they directly prove a held part.</p>
        <div class="requirement-evidence-grid chassis-rubber-context-grid">
          ${referenceImages
            .map(([path, caption]) => {
              const image = {
                path,
                caption,
                media_id: path.split("/").pop().replace(/\.[^.]+$/, ""),
                media_type: "photo",
              };
              const prepared = prepareImage(image, caption, { sequenceId });
              const mediaClass = path.endsWith(".svg")
                ? "table-image table-image-contain chassis-rubber-context-image"
                : "table-image chassis-rubber-context-image";
              return `
                <div class="requirement-evidence-item">
                  ${renderPreparedMedia(prepared, "table-image-btn chassis-rubber-context-btn", mediaClass)}
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
                <th>Evidence</th>
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
                    <td class="requirement-evidence-cell">${renderRequirementEvidenceImages({
                      evidence_images: scoutEvidenceImages(row),
                      photo_status: row.order_release_state,
                      requirement_name: row.item,
                    })}</td>
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
                <th>Evidence</th>
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
                    <td class="requirement-evidence-cell">${renderRequirementEvidenceImages({
                      evidence_images: scoutEvidenceImages(row),
                      photo_status: row.status,
                      requirement_name: row.action_id,
                    })}</td>
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
                <th>Evidence</th>
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
                    <td class="requirement-evidence-cell">${renderRequirementEvidenceImages({
                      evidence_images: scoutEvidenceImages(row),
                      photo_status: row.release_status,
                      requirement_name: row.vehicle_position,
                    })}</td>
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
                <th>Evidence</th>
                <th>Line</th>
                <th>Qty</th>
                <th>Status</th>
                <th>Spec / Dimensions</th>
                <th>Release Action</th>
              </tr>
            </thead>
            <tbody>
              ${groupScoutRows(source, "pipes")
                .map((group) => `
                  ${renderScoutGroupRow(group, 6)}
                  ${group.rows
                    .map((row) => `
                      <tr>
                        <td class="requirement-evidence-cell">${renderRequirementEvidenceImages({
                          evidence_images: scoutEvidenceImages(row),
                          photo_status: row.order_release_state,
                          requirement_name: row.item,
                        })}</td>
                        <td>
                          <strong>${escapeHtml(row.order_line_id || "")} · ${escapeHtml(row.item || "")}</strong>
                          ${row.part_number_or_code ? `<div class="small-muted">Reference: ${escapeHtml(row.part_number_or_code || "")}</div>` : ""}
                          <div class="small-muted">${escapeHtml(scoutPipeGroup(row).label || formatToken(row.route || ""))}</div>
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
                          ${renderScoutField("Connectors/fittings", scoutConnectorOrFittingText(row))}
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
                <th>Evidence</th>
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
                    <td class="requirement-evidence-cell">${renderRequirementEvidenceImages({
                      evidence_images: scoutEvidenceImages(row),
                      photo_status: row.status,
                      requirement_name: row.action_id,
                    })}</td>
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
                <th>Evidence</th>
                <th>Circuit</th>
                <th>Order Lines</th>
                <th>Ends / Length</th>
                <th>Tube / Fitting Detail</th>
                <th>Status / Action</th>
              </tr>
            </thead>
            <tbody>
              ${groupScoutRows(source, "pipes")
                .map((group) => `
                  ${renderScoutGroupRow(group, 6)}
                  ${group.rows
                    .map((row) => `
                      <tr>
                        <td class="requirement-evidence-cell">${renderRequirementEvidenceImages({
                          evidence_images: scoutEvidenceImages(row),
                          photo_status: row.photo_status,
                          requirement_name: row.pipe_or_line,
                        })}</td>
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

  function renderEvidenceOriginalStateCell(row) {
    const images = Array.isArray(row && row.evidence_images) ? row.evidence_images : [];
    const states = new Map();
    const seen = new Set();
    images.forEach((image) => {
      const meta = withOverride(getBasePhotoMeta(image));
      const stateValue = cleanString(meta.observed_state || (image && image.observed_state));
      if (!stateValue || seen.has(stateValue)) {
        return;
      }
      seen.add(stateValue);
      states.set(stateValue, originalStateDisplayLabel(stateValue));
    });
    const usefulStates = prioritizeOriginalStates(Array.from(states.entries()));
    const decision = originalDecisionLabel(row);
    const dateRange = evidenceDateRange(images);
    if (!states.size) {
      return `<span class="small-muted">No captured evidence yet</span>`;
    }
    return `
      <div class="original-state-cell">
        <div class="chip-row">
          ${usefulStates.map(([, label]) => `<span class="chip info">${escapeHtml(label)}</span>`).join(" ")}
        </div>
        ${decision ? `<div class="small-muted">Decision: ${escapeHtml(decision)}</div>` : ""}
        <div class="small-muted">Evidence: ${escapeHtml(images.length)} photo${images.length === 1 ? "" : "s"}${dateRange ? ` · ${escapeHtml(dateRange)}` : ""}</div>
      </div>
    `;
  }

  function originalStateDisplayLabel(stateValue) {
    const key = cleanString(stateValue).toLowerCase();
    const labels = {
      fabrication_spec_capture: "Original sample captured",
      large_pipe_sample_measurement_reference: "Large-pipe detail photos",
      inspection_in_progress: "Original route inspection",
      cooling_routing_baseline: "Installed route context",
      engine_front_cooling_overview: "Engine clearance context",
      direct_location_photo: "Original location captured",
      image_route_context_closed: "Route context closed",
      reference_only: "Reference only",
    };
    return labels[key] || formatToken(stateValue);
  }

  function prioritizeOriginalStates(entries) {
    const priority = new Map(
      [
        "large_pipe_sample_measurement_reference",
        "fabrication_spec_capture",
        "direct_location_photo",
        "inspection_in_progress",
        "image_route_context_closed",
        "cooling_routing_baseline",
        "engine_front_cooling_overview",
        "reference_only",
      ].map((value, index) => [value, index])
    );
    const sorted = [...entries].sort(([left], [right]) => {
      const leftKey = cleanString(left).toLowerCase();
      const rightKey = cleanString(right).toLowerCase();
      return (priority.get(leftKey) ?? 100) - (priority.get(rightKey) ?? 100);
    });
    const nonReference = sorted.filter(([stateValue]) => cleanString(stateValue).toLowerCase() !== "reference_only");
    return (nonReference.length ? nonReference : sorted).slice(0, 3);
  }

  function originalDecisionLabel(row) {
    const scope = cleanString(row && row.replace_scope).toLowerCase();
    if (!scope) {
      return "";
    }
    if (scope.includes("recreate") || scope.includes("fabricate")) {
      return "Fabricate new from original pattern";
    }
    if (scope.includes("replace_new_after_identification")) {
      return "Replace new after identification";
    }
    if (scope.includes("replace")) {
      return "Replace with new part";
    }
    return formatToken(scope);
  }

  function evidenceDateRange(images) {
    const dates = Array.from(
      new Set(
        images
          .map((image) => cleanString(withOverride(getBasePhotoMeta(image)).captured_date || image.captured_date))
          .filter(Boolean)
      )
    ).sort();
    if (!dates.length) {
      return "";
    }
    return dates.length === 1 ? dates[0] : `${dates[0]} to ${dates[dates.length - 1]}`;
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
    const photoRowsByPipeId = new Map();
    photoRows.forEach((row) => {
      const pipeId = cleanString(row.pipe_id);
      if (!pipeId) {
        return;
      }
      if (!photoRowsByPipeId.has(pipeId)) {
        photoRowsByPipeId.set(pipeId, []);
      }
      photoRowsByPipeId.get(pipeId).push(row);
    });

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
                <th>Original State</th>
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
                  const relatedPhotoRows = photoRowsByPipeId.get(pipeId) || [];
                  const originalStateImages = dedupeImages([
                    ...(Array.isArray(row.evidence_images) ? row.evidence_images : []),
                    ...relatedPhotoRows.flatMap((photoRow) =>
                      Array.isArray(photoRow.evidence_images) ? photoRow.evidence_images : []
                    ),
                  ]);
                  return `
                    <tr>
                      <td>
                        <strong>${escapeHtml(pipeId)} · ${escapeHtml(row.pipe_or_line || "")}</strong>
                        <div class="small-muted">${escapeHtml(row.vehicle_location || "")}</div>
                        <div class="small-muted">Scope: ${escapeHtml(formatToken(row.replace_scope || ""))}</div>
                      </td>
                      <td>${renderEvidenceOriginalStateCell({ ...row, evidence_images: originalStateImages })}</td>
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
        renderChassisRubberConsolidatedSpec(active.longman_rubber_order_specs),
        renderCompleteJ40RubberCoverage(active.rubber_ordering_specs),
        renderChassisRubberReferenceImages(),
      ].join("");
    }
    if (active.id === "replacement_pipes") {
      return [
        renderReplacementPipeSimpleBoard(active),
        renderLongmanPipeHoseOrderTable(active.longman_pipe_hose_order_specs),
      ].join("");
    }
    if (active.id === "brake_system") {
      return renderRequirementTable(rows, {
        title: "Rear Brake Cable / Line Requirements",
        summary: "Rear axle brake cable, hard-line, hose, drum, and retaining-clip actions with removal guidance and replacement-order gates.",
      });
    }
    return renderRequirementTable(rows);
  }

  function renderChassisBracketAnalysisRegister(workstream) {
    const active = workstream || {};
    if (active.id !== "chassis_fixing") {
      return "";
    }

    const rows = Array.isArray(active.chassis_bracket_analysis_register)
      ? active.chassis_bracket_analysis_register
      : [];
    if (!rows.length) {
      return "";
    }

    const coatingHolds = rows.filter((row) => cleanString(row.coating_gate).toLowerCase().includes("block")).length;
    const scoutingRows = rows.filter((row) => cleanString(row.status).toLowerCase().includes("scout")).length;
    const designRows = rows.filter((row) => cleanString(row.design_release_needed).toLowerCase() === "yes").length;

    return `
      <article class="card pipe-requirements-card">
        <div class="detail-header">
          <h3>Bracket Analysis Register</h3>
          <div class="chip-row">
            ${chip(`${rows.length} Rows`)}
            ${chip(`${coatingHolds} Coating Holds`)}
            ${chip(`${scoutingRows} Need Scouting`)}
            ${chip(`${designRows} Need Design Release`)}
          </div>
        </div>
        <p class="small-muted">Seeded from existing radiator/front-support and battery-side photos. Radiator evidence is direct; battery tray base and support legs still need close-up scouting.</p>
        <div class="item-links">
          <a class="item-link" href="../../docs/chassis-bracket-analysis-register-20260508.md">Register Doc</a>
          <a class="item-link" href="../../data/manual/chassis_bracket_analysis_register_20260508.csv">Source CSV</a>
        </div>
        <div class="table-wrap requirement-table-wrap">
          <table class="requirement-table bracket-analysis-table">
            <colgroup>
              <col class="bracket-col-function">
              <col class="bracket-col-photo-read">
              <col class="bracket-col-decision">
              <col class="bracket-col-next-action">
            </colgroup>
            <thead>
              <tr>
                <th>Bracket / Function</th>
                <th>Photo Read</th>
                <th>Decision / Gate</th>
                <th>Next Action</th>
              </tr>
            </thead>
            <tbody>
              ${rows
                .map(
                  (row) => `
                    <tr class="workstream-data-row">
                      <td>
                        <strong>${escapeHtml(row.register_id || "")} · ${escapeHtml(row.component_or_function || "")}</strong>
                        <div class="small-muted">${escapeHtml(formatToken(row.station || ""))}${row.side ? ` / ${escapeHtml(formatToken(row.side))}` : ""}</div>
                        <div class="status-stack">
                          ${statusChip(row.status || "open")}
                          ${statusChip(row.current_condition || "unknown")}
                          ${
                            row.design_release_needed
                              ? statusChip(cleanString(row.design_release_needed).toLowerCase() === "yes" ? "design_needed" : "design_not_required")
                              : ""
                          }
                        </div>
                      </td>
                      <td class="bracket-photo-read-cell">
                        ${escapeHtml(row.photo_read || "")}
                      </td>
                      <td>
                        <strong>${escapeHtml(row.decision || "")}</strong>
                        <div class="small-muted">${escapeHtml(formatToken(row.coating_gate || ""))}</div>
                      </td>
                      <td>
                        ${escapeHtml(row.next_action || "")}
                        ${row.notes ? `<div class="small-muted">${escapeHtml(row.notes)}</div>` : ""}
                      </td>
                    </tr>
                    <tr class="row-evidence-strip-row">
                      <td colspan="4">${renderRequirementEvidenceStrip(
                        {
                          evidence_images: row.evidence_images,
                          component_or_function: row.component_or_function,
                          evidence_level: row.evidence_level || "photo_needed",
                          evidence_refs: row.evidence_refs,
                        },
                        {
                          label: "Row Evidence Images",
                          fallbackCaption: row.component_or_function,
                        }
                      )}</td>
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

  function renderPackageLinks(title, links) {
    const rows = Array.isArray(links) ? links.filter((link) => cleanString(link && link.url)) : [];
    if (!rows.length) {
      return "";
    }
    const visualGroup = cleanString(title).toLowerCase().includes("visual");
    return `
      <div class="fabrication-link-group">
        <strong>${escapeHtml(title)}</strong>
        <div class="item-links">
          ${rows
            .map((link, index) => {
              const attrs = visualGroup ? ' target="_blank" rel="noopener"' : " download";
              return `<a class="item-link" href="${escapeHtml(link.url)}"${attrs}>${escapeHtml(cleanString(link.label) || `File ${index + 1}`)}</a>`;
            })
            .join("")}
        </div>
      </div>
    `;
  }

  function renderPackageDownload(link) {
    if (!link || !cleanString(link.url)) {
      return "";
    }
    const byteCount = Number(link.bytes);
    const size = Number.isFinite(byteCount) && byteCount > 0 ? ` · ${Math.round(byteCount / 1024)} KB` : "";
    return `
      <div class="fabrication-link-group fabrication-download-group">
        <strong>Package</strong>
        <div class="item-links">
          <a class="item-link package-download-link" href="${escapeHtml(link.url)}" download>${escapeHtml(cleanString(link.label) || "Download package (.zip)")}${escapeHtml(size)}</a>
        </div>
      </div>
    `;
  }

  function fileLeafFromLink(link) {
    const raw = cleanString((link && (link.url || link.label)) || "");
    if (!raw) {
      return "";
    }
    return raw.split("?")[0].split("#")[0].split("/").pop() || raw;
  }

  function drawingTitleFromLink(link, fallbackIndex) {
    const leaf = fileLeafFromLink(link).replace(/\.(svg|dxf)$/i, "");
    if (!leaf) {
      return `Drawing ${fallbackIndex + 1}`;
    }
    return leaf.replace(/[_-]+/g, " ");
  }

  function packageDrawingItems(row) {
    const svgLinks = Array.isArray(row && row.svg_links) ? row.svg_links.filter((link) => cleanString(link && link.url)) : [];
    const dxfLinks = Array.isArray(row && row.dxf_links) ? row.dxf_links.filter((link) => cleanString(link && link.url)) : [];
    const dxfByStem = new Map();
    dxfLinks.forEach((link) => {
      const stem = canonicalMediaStem(link.url || link.label);
      if (stem && !dxfByStem.has(stem)) {
        dxfByStem.set(stem, link);
      }
    });

    return svgLinks.map((svgLink, index) => {
      const stem = canonicalMediaStem(svgLink.url || svgLink.label);
      return {
        title: drawingTitleFromLink(svgLink, index),
        svg: svgLink,
        dxf: stem ? dxfByStem.get(stem) : null,
      };
    });
  }

  function renderPackageDrawingPreviews(row) {
    const drawings = packageDrawingItems(row);
    if (!drawings.length) {
      return "";
    }
    return `
      <div class="fabrication-drawing-section">
        <div class="fabrication-drawing-heading">
          <strong>SVG Drawing Previews</strong>
          <span>${escapeHtml(`${drawings.length} SVG${drawings.length === 1 ? "" : "s"}`)}${row.dxf_links && row.dxf_links.length ? escapeHtml(` / ${row.dxf_links.length} DXF`) : ""}</span>
        </div>
        <div class="fabrication-drawing-grid">
          ${drawings
            .map((drawing, index) => {
              const svgUrl = cleanString(drawing.svg && drawing.svg.url);
              const dxfUrl = cleanString(drawing.dxf && drawing.dxf.url);
              const title = cleanString(drawing.title) || `Drawing ${index + 1}`;
              return `
                <div class="fabrication-drawing-item">
                  <a class="fabrication-drawing-preview-link" href="${escapeHtml(svgUrl)}" target="_blank" rel="noopener noreferrer">
                    <img class="fabrication-drawing-image" loading="lazy" decoding="async" src="${escapeHtml(svgUrl)}" alt="${escapeHtml(title)} SVG drawing">
                  </a>
                  <div class="fabrication-drawing-meta">
                    <strong class="fabrication-drawing-title">${escapeHtml(title)}</strong>
                    <div class="item-links">
                      ${renderItemLink({ url: svgUrl, label: "SVG" }, 0)}
                      ${dxfUrl ? renderItemLink({ url: dxfUrl, label: "DXF", download: true }, 1) : ""}
                    </div>
                  </div>
                </div>
              `;
            })
            .join("")}
        </div>
      </div>
    `;
  }

  function visualUrlWithEmbed(url) {
    const cleaned = cleanString(url);
    if (!cleaned) {
      return "";
    }
    return `${cleaned}${cleaned.includes("?") ? "&" : "?"}embed=1`;
  }

  function visualModeKey(link, hasAssembledPeer = false) {
    const label = cleanString(link && link.label).toLowerCase();
    const url = cleanString(link && link.url).toLowerCase();
    const text = `${label} ${url}`;
    if (text.includes("assembled")) {
      return "assembled";
    }
    if (text.includes("fabrication-read") || (hasAssembledPeer && text.includes("_3d_visualisation"))) {
      return "expanded";
    }
    return "default";
  }

  function visualModeLabel(modeKey, link) {
    if (modeKey === "assembled") {
      return "Attached Assembly";
    }
    if (modeKey === "expanded") {
      return "Expanded Parts";
    }
    return cleanString(link && link.label) || "3D View";
  }

  function packageVisualModes(row) {
    const visualLinks = Array.isArray(row && row.visual_links) ? row.visual_links : [];
    const interactiveLinks = visualLinks.filter((link) => cleanString(link && link.url).toLowerCase().endsWith(".html"));
    const fallbackLinks = visualLinks.filter((link) => cleanString(link && link.url).toLowerCase().endsWith(".svg"));
    const hasAssembledPeer = visualLinks.some((link) => cleanString(link && link.label).toLowerCase().includes("assembled") || cleanString(link && link.url).toLowerCase().includes("assembled"));
    return interactiveLinks.map((interactive) => {
      const modeKey = visualModeKey(interactive, hasAssembledPeer);
      const fallback =
        fallbackLinks.find((link) => visualModeKey(link, hasAssembledPeer) === modeKey) ||
        fallbackLinks.find((link) => cleanString(link && link.label).toLowerCase().includes(cleanString(interactive.label).toLowerCase().replace("3d visualisation", "static 3d visualisation"))) ||
        null;
      return {
        modeKey,
        label: visualModeLabel(modeKey, interactive),
        interactive,
        fallback,
      };
    });
  }

  function renderPackageVisualPreviews(row) {
    const modes = packageVisualModes(row);
    if (!modes.length) {
      return "";
    }
    const sequenceId = createVisualSequence();
    return `
      <div class="fabrication-visual-grid">
        ${modes
          .map((mode) => {
            const title = `${cleanString(row && row.title) || "Fabrication package"} · ${mode.label}`;
            const visualKey = registerVisual(
              {
                title,
                packageTitle: cleanString(row && row.title),
                packageId: cleanString(row && row.package_id),
                label: mode.label,
                modeKey: mode.modeKey,
                url: cleanString(mode.interactive && mode.interactive.url),
                embedUrl: visualUrlWithEmbed(mode.interactive && mode.interactive.url),
                staticUrl: cleanString(mode.fallback && mode.fallback.url),
                notes: cleanString(row && row.release_position),
              },
              sequenceId
            );
            return `
              <div class="fabrication-visual-preview">
                <div class="fabrication-visual-label">
                  <strong>${escapeHtml(mode.label)}</strong>
                  <span>${escapeHtml(mode.modeKey === "assembled" ? "installed together" : mode.modeKey === "expanded" ? "separated for fabrication read" : "interactive 3D view")}</span>
                </div>
                <div class="fabrication-visual-viewport">
                  <iframe class="fabrication-visual-frame" src="${escapeHtml(visualUrlWithEmbed(mode.interactive && mode.interactive.url))}" title="${escapeHtml(title)}" loading="lazy"></iframe>
                  <button type="button" class="fabrication-visual-open" data-visual-key="${escapeHtml(visualKey)}" aria-label="Enlarge ${escapeHtml(title)}">
                    <span>Enlarge</span>
                  </button>
                </div>
              </div>
            `;
          })
          .join("")}
      </div>
    `;
  }

  function renderPackageDefinitionRows(row) {
    const primaryCount = Array.isArray(row.primary_links) ? row.primary_links.length : 0;
    const visualCount = Array.isArray(row.visual_links) ? row.visual_links.length : 0;
    const dxfCount = Array.isArray(row.dxf_links) ? row.dxf_links.length : 0;
    const svgCount = Array.isArray(row.svg_links) ? row.svg_links.length : 0;
    const definitions = [
      ["Requirement", `${cleanString(row.requirement_id) || "-"} · ${cleanString(row.title) || "-"}`],
      ["Package", cleanString(row.package_id) || "-"],
      ["System", formatToken(row.system || "") || "-"],
      ["Drawings", `${svgCount} SVG / ${dxfCount} DXF`],
      ["Other files", `${primaryCount} docs/data${visualCount ? ` / ${visualCount} visual` : ""}`],
    ];
    return `
      <dl class="fabrication-definition-rows">
        ${definitions
          .map(
            ([term, value]) => `
              <div class="fabrication-definition-row">
                <dt>${escapeHtml(term)}</dt>
                <dd>${escapeHtml(value)}</dd>
              </div>
            `
          )
          .join("")}
      </dl>
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
        <p class="small-muted">Use the embedded 3D view for assembly orientation, then download the package archive or individual PDF/DXF/SVG files for fabrication.</p>
        <div class="fabrication-package-list">
          ${rows
            .map((row) => {
              const visualPreviews = renderPackageVisualPreviews(row);
              return `
                <section class="fabrication-package-row ${visualPreviews ? "" : "fabrication-package-row-no-visual"}">
                  ${visualPreviews}
                  <div class="fabrication-package-body">
                    <div class="fabrication-package-heading">
                      <div>
                        <h4>${escapeHtml(row.title || row.package_id || "Fabrication package")}</h4>
                        <p class="small-muted">${escapeHtml(row.package_id || "")}</p>
                      </div>
                      ${statusChip(row.current_status || "unknown")}
                    </div>
                    ${renderPackageDefinitionRows(row)}
                    <div class="fabrication-release-row">
                      <strong>Release</strong>
                      <span>${escapeHtml(row.release_position || "")}</span>
                    </div>
                    ${
                      row.notes
                        ? `<div class="fabrication-release-row"><strong>Notes</strong><span>${escapeHtml(row.notes || "")}</span></div>`
                        : ""
                    }
                    ${renderPackageDrawingPreviews(row)}
                    <div class="fabrication-file-rows">
                      ${renderPackageDownload(row.archive_link)}
                      ${renderPackageLinks("3D Visual", row.visual_links)}
                      ${renderPackageLinks("3D Models", row.model_links)}
                      ${renderPackageLinks("Docs + Data", row.primary_links)}
                      ${renderPackageLinks("Cut DXF", row.dxf_links)}
                      ${renderPackageLinks("SVG Drawings", row.svg_links)}
                    </div>
                  </div>
                </section>
              `;
            })
            .join("")}
        </div>
      </article>
    `;
  }

  function rowMatchesWorkstream(row, workstreamId) {
    const target = cleanString(workstreamId);
    return splitMultiValue(row && row.workstream).includes(target);
  }

  function rawMaterialRowsForWorkstream(workstream) {
    const rows = Array.isArray(data.fabrication_raw_material_estimates) ? data.fabrication_raw_material_estimates : [];
    const workstreamId = cleanString(workstream && workstream.id);
    if (!workstreamId || !rows.length) {
      return [];
    }
    return rows.filter((row) => rowMatchesWorkstream(row, workstreamId));
  }

  function procurementRowByEntryId(entryId, workstream) {
    const targetId = cleanString(entryId);
    if (!targetId) {
      return null;
    }
    const activeRows = Array.isArray(workstream && workstream.involved_parts) ? workstream.involved_parts : [];
    const activeMatch = activeRows.find((row) => cleanString(row.entry_id) === targetId);
    if (activeMatch) {
      return activeMatch;
    }
    const openRows = data.parts && Array.isArray(data.parts.open_rows) ? data.parts.open_rows : [];
    return openRows.find((row) => cleanString(row.entry_id) === targetId) || null;
  }

  function renderFabricationRawMaterials(workstream) {
    const rows = rawMaterialRowsForWorkstream(workstream);
    if (!rows.length) {
      return "";
    }
    const purchaseRows = rows.filter((row) => cleanString(row.release_status).startsWith("purchase_ready"));
    const existingRows = rows.filter((row) => cleanString(row.release_status).startsWith("already_in_procurement"));
    return `
      <article class="card fabrication-raw-materials-card">
        <div class="detail-header">
          <h3>Raw Material Procurement</h3>
          <div class="chip-row">
            ${chip(`${rows.length} Stock Lines`)}
            ${chip(`${purchaseRows.length} Buy/Quote`)}
            ${existingRows.length ? chip(`${existingRows.length} Already Covered`) : ""}
          </div>
        </div>
        <p class="small-muted">Raw-stock estimates are now tied to procurement rows. Tub repair steel is listed separately from battery/radiator fabrication steel.</p>
        <div class="table-wrap">
          <table class="compact raw-material-table">
            <thead>
              <tr>
                <th>Material</th>
                <th>Estimate</th>
                <th>Covers</th>
                <th>Procurement</th>
              </tr>
            </thead>
            <tbody>
              ${rows
                .map((row) => {
                  const entryId = cleanString(row.procurement_entry_id);
                  const procurementRow = entryId.includes("|") ? null : procurementRowByEntryId(entryId, workstream);
                  return `
                    <tr>
                      <td>
                        <strong>${escapeHtml(row.raw_material || "")}</strong>
                        <div class="small-muted">${escapeHtml(row.package_or_scope || "")}</div>
                      </td>
                      <td>${escapeHtml(row.estimate_to_buy || "")}</td>
                      <td>${escapeHtml(row.covered_fabrication || "")}</td>
                      <td>
                        ${
                          procurementRow
                            ? `${renderItemButton(procurementRow)}<div class="small-muted">${escapeHtml(formatToken(procurementRow.procurement_stage || ""))}</div>`
                            : `<span class="small-muted">${escapeHtml(entryId || "No procurement row")}</span><div class="small-muted">${escapeHtml(formatToken(row.release_status || ""))}</div>`
                        }
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
    const sequenceId = createImageSequence();
    return `
      <div class="gallery">
        ${uniqueImages
          .map((image) => {
            const prepared = prepareImage(image, "Evidence media", { sequenceId });
            const visibleCaption = cleanString(image.caption || prepared.caption);
            return `
              <figure>
                ${renderPreparedMedia(prepared, "image-open-btn", "gallery-image")}
                <figcaption>${escapeHtml(visibleCaption)}</figcaption>
              </figure>
            `;
          })
          .join("")}
      </div>
    `;
  }

  function imageLibraryRows() {
    const rows = Array.isArray(data.images) ? data.images : Object.values(data.photo_lookup || {});
    const query = cleanString(state.imageSearch).toLowerCase();
    return rows.filter((image) => {
      if (state.imageComponentGroup && cleanString(image.component_group) !== state.imageComponentGroup) {
        return false;
      }
      if (state.imageStage && cleanString(image.stage) !== state.imageStage) {
        return false;
      }
      if (!query) {
        return true;
      }
      const searchable = [
        image.file_name,
        image.caption,
        image.component_group,
        image.specific_component,
        image.stage,
        image.observed_state,
        image.tags,
        image.notes,
      ]
        .map((value) => cleanString(value).toLowerCase())
        .join(" ");
      return searchable.includes(query);
    });
  }

  function renderImagesResults() {
    const resultRoot = document.getElementById("images-results");
    if (!resultRoot) {
      return;
    }
    resetImageRegistry();
    const matches = imageLibraryRows();
    const visible = matches.slice(0, state.imageVisibleCount);
    const sequenceId = createImageSequence();
    resultRoot.innerHTML = `
      <div class="images-result-summary">
        <p class="small-muted">Showing ${escapeHtml(visible.length)} of ${escapeHtml(matches.length)} images.</p>
      </div>
      ${
        visible.length
          ? `<div class="gallery images-library-grid">
              ${visible
                .map((image) => {
                  const prepared = prepareImage(image, image.file_name || "J40 project image", { sequenceId });
                  const component = formatToken(prepared.effective.specific_component || prepared.effective.component_group || "");
                  const date = cleanString(prepared.effective.captured_date);
                  return `
                    <figure>
                      ${renderImageButton(prepared, "image-open-btn", "gallery-image", "lazy")}
                      <figcaption>
                        <span class="images-caption-row">
                          <strong>${escapeHtml(component || prepared.caption)}</strong>
                          <a class="image-direct-link" href="${escapeHtml(prepared.path)}" target="_blank" rel="noopener">Direct URL</a>
                        </span>
                        ${date ? `<span>${escapeHtml(date)}</span>` : ""}
                      </figcaption>
                    </figure>
                  `;
                })
                .join("")}
            </div>`
          : '<article class="card"><p>No images match those filters.</p></article>'
      }
      ${
        visible.length < matches.length
          ? `<div class="images-show-more-wrap">
              <button type="button" class="images-show-more-btn" data-images-show-more>Show 120 more</button>
            </div>`
          : ""
      }
    `;
  }

  function renderImages() {
    const rows = Array.isArray(data.images) ? data.images : Object.values(data.photo_lookup || {});
    const componentGroups = Array.from(new Set(rows.map((image) => cleanString(image.component_group)).filter(Boolean))).sort();
    const stages = Array.from(new Set(rows.map((image) => cleanString(image.stage)).filter(Boolean))).sort();
    root.innerHTML = `
      <div class="images-view">
        <div class="images-view-heading">
          <div>
            <h2 class="section-title">Images</h2>
            <p class="section-subtitle">The complete J40 project image archive. Select any image to open the full-size viewer.</p>
          </div>
          <span class="header-meta">${escapeHtml(rows.length)} images</span>
        </div>
        <section class="card images-toolbar" aria-label="Image filters">
          <label>
            <span>Search</span>
            <input type="search" value="${escapeHtml(state.imageSearch)}" placeholder="Part, stage, tag, or filename" data-images-search>
          </label>
          <label>
            <span>Component group</span>
            <select data-images-filter="component-group">
              <option value="">All component groups</option>
              ${componentGroups
                .map(
                  (value) =>
                    `<option value="${escapeHtml(value)}"${value === state.imageComponentGroup ? " selected" : ""}>${escapeHtml(formatToken(value))}</option>`
                )
                .join("")}
            </select>
          </label>
          <label>
            <span>Stage</span>
            <select data-images-filter="stage">
              <option value="">All stages</option>
              ${stages
                .map(
                  (value) =>
                    `<option value="${escapeHtml(value)}"${value === state.imageStage ? " selected" : ""}>${escapeHtml(formatToken(value))}</option>`
                )
                .join("")}
            </select>
          </label>
        </section>
        <section id="images-results" aria-live="polite"></section>
      </div>
    `;
    renderImagesResults();
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
        const separateZoneEvidenceRows = cleanString(panel.key) === "chassis_prime_readiness";
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
                    <table class="operation-zone-table">
                      <colgroup>
                        <col class="operation-col-area">
                        <col class="operation-col-remaining">
                        <col class="operation-col-status">
                        <col class="operation-col-work">
                        <col class="operation-col-evidence">
                      </colgroup>
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
                              <tr class="operation-zone-data-row">
                                <td><strong>${escapeHtml(zone.area || "")}</strong></td>
                                <td>${escapeHtml(zone.remaining || "")}</td>
                                <td>${statusChip(zone.status || "pending")}</td>
                                <td>${escapeHtml(zone.work_required || "")}</td>
                                <td>${escapeHtml(zone.evidence_count || "0")} photos</td>
                              </tr>
                              ${
                                separateZoneEvidenceRows
                                  ? `<tr class="row-evidence-strip-row operation-zone-evidence-row">
                                      <td colspan="5">${renderRequirementEvidenceStrip(
                                        {
                                          evidence_images: zone.evidence_images,
                                          evidence_level: zone.status || "photo_needed",
                                          evidence_refs: zone.evidence_refs,
                                        },
                                        {
                                          label: "Zone Evidence Images",
                                          fallbackCaption: zone.area,
                                        }
                                      )}</td>
                                    </tr>`
                                  : ""
                              }
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

  function scoutSpecImages(spec) {
    const images = [];
    const seen = new Set();
    const addImage = (image) => {
      if (!image || typeof image !== "object" || isImageDeleted(image)) {
        return;
      }
      const key = cleanString(image.path || image.image_url || image.media_id);
      if (!key || seen.has(key)) {
        return;
      }
      seen.add(key);
      images.push(image);
    };
    if (Array.isArray(spec && spec.images)) {
      spec.images.forEach(addImage);
    }
    addImage(spec && spec.image);
    return images;
  }

  function renderScoutSpecImageGallery(images, fallbackCaption) {
    const sourceImages = Array.isArray(images) ? images : [];
    if (!sourceImages.length) {
      return "";
    }
    const sequenceId = createImageSequence();
    return `
      <div class="scout-spec-gallery">
        ${sourceImages
          .map((image) =>
            renderFigureImage(image, fallbackCaption || "Scout reference image", {
              figureClass: "scout-spec-figure",
              buttonClass: "image-open-btn scout-spec-gallery-btn",
              imageClass: "scout-spec-gallery-image",
              captionClass: "small-muted",
              caption: image.caption,
              sequenceId,
            })
          )
          .join("")}
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
        const images = scoutSpecImages(spec);
        const image = images.length === 1 ? images[0] : null;
        const priceBits = [
          quantity ? `Quantity: ${quantity}` : "",
          price.unit_price_range ? `Unit price range: ${price.unit_price_range}` : price.target_range ? `Unit price range: ${price.target_range}` : "",
          price.negotiation_midpoint ? `Negotiation midpoint: ${price.negotiation_midpoint}` : "",
          price.total_value_range ? `Total value: ${price.total_value_range}` : "",
          price.rule || "",
        ].filter((item) => cleanString(item));
        return `
          <article class="card market-spec-card scout-spec-card" id="${escapeHtml(spec.id || "")}">
            <div class="scout-spec-layout${images.length > 1 ? " scout-spec-layout-text-only" : ""}">
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
            ${images.length > 1 ? renderScoutSpecImageGallery(images, spec.title || "Scout reference image") : ""}
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

  function scoutEvidenceImages(row) {
    const direct = Array.isArray(row && row.evidenceImages) ? row.evidenceImages : [];
    const generated = Array.isArray(row && row.evidence_images) ? row.evidence_images : [];
    return filterVisibleImages([...direct, ...generated]);
  }

  function scoutImageIdentity(image) {
    return [
      image && image.media_id,
      image && image.path,
      image && image.caption,
    ]
      .map((value) => cleanString(value).toLowerCase())
      .join(" ");
  }

  function isMixedFastenerPileImage(image) {
    const imageText = scoutImageIdentity(image);
    return imageText.includes("20260503_153832_gp_0fjjilhg");
  }

  function shouldReplaceScoutRowImage(row, image) {
    const imageText = scoutImageIdentity(image);
    if (!imageText) {
      return false;
    }
    const text = scoutRowText(row);
    const isLoosePileRow = text.includes("user-selected loose fastener photo") || text.includes("user-selected loose hardware photo");
    if (isLoosePileRow && isMixedFastenerPileImage(image)) {
      return true;
    }
    if (imageText.includes("graded_fasteners") && (
      text.includes("body mount hardware") ||
      text.includes("captive/clip") ||
      text.includes("clip/speed nut") ||
      text.includes("retaining clip") ||
      text.includes("trim screws") ||
      text.includes("shoulder bolts") ||
      text.includes("specialty bracket")
    )) {
      return true;
    }
    if ((imageText.includes("body_mount_kit") || imageText.includes("body_shims")) && (
      text.includes("body mount shim") ||
      text.includes("body-to-chassis mount rubber") ||
      text.includes("body mount rubber kit") ||
      text.includes("body mount hardware")
    )) {
      return true;
    }
    if ((
      imageText.includes("20260502_004106_gp_wlyluaha") ||
      imageText.includes("20260502_004133_gp_zepqmara") ||
      imageText.includes("20260503_153017_gp_dm8bca4w") ||
      imageText.includes("20260503_153031_gp_rffqdubw") ||
      imageText.includes("20260503_153130_gp_gkkofapg")
    ) && (
      text.includes("formed metal coolant") ||
      text.includes("formed coolant pipe") ||
      text.includes("hard-line") ||
      text.includes("hard line")
    )) {
      return true;
    }
    return false;
  }

  function preferredScoutMediaIds(row) {
    const id = cleanString((row && (row.id || row.order_id || row.order_line_id || row.requirement_id)) || "").toUpperCase();
    const text = [
      id,
      row && row.item,
      row && row.requirement_name,
      row && row.partNumber,
      row && row.part_number_or_code,
    ]
      .map((value) => cleanString(value).toLowerCase())
      .join(" ");
    if (id === "CR-MAIN-001" || id === "BM-ISO-SM" || id === "BM-SM" || text.includes("small circular body-mount") || text.includes("main body isolator pad")) {
      return ["20260405_234652", "20260405_234546"];
    }
    if (id === "CR-MAIN-002" || id === "BM-ISO-LG" || id === "BM-LG" || text.includes("large circular body-mount")) {
      return ["20260405_234652", "20260405_234546"];
    }
    if (id === "CR-MAIN-004" || text.includes("cup") || text.includes("seat washer")) {
      return ["20260502_004413_gp_Qno8OVRg", "20260502_004429_gp_KJHxGcCA"];
    }
    if (id === "CR-SHIM-001" || id.includes("BM-SHIM") || text.includes("shim") || text.includes("spacer pack")) {
      return ["20260502_004429_gp_KJHxGcCA", "20260502_004231_gp_CfosvPIg", "20260502_004413_gp_Qno8OVRg"];
    }
    if (id.includes("BUMP") || text.includes("bump stop") || text.includes("rubber bumper")) {
      return ["20260529_223605_gp_CklgF0cQ", "20260529_223701_gp_wYPExcAA"];
    }
    if (id === "CR-FRONT-001" || id === "FS-OVAL" || text.includes("two-hole oval")) {
      return ["20260502_004345_gp_yK8VYzMQ"];
    }
    if (id === "CR-FRONT-002" || id === "FS-STRIP-L" || text.includes("left front-support strip") || text.includes("left underfloor")) {
      return ["20260517_194143_gp_CO7MuMdA", "20260517_194706_gp_twKRWGFA", "20260517_193503_gp_N9nHjqXw"];
    }
    if (id === "CR-FRONT-003" || id === "FS-STRIP-R" || text.includes("right front-support strip") || text.includes("right underfloor")) {
      return ["20260517_194633_gp_rAjY3gjg", "20260517_194706_gp_twKRWGFA", "20260517_193612_gp_JmbfR0Tw"];
    }
    if (id === "RPO-COOL-001" || id === "HLS-01" || id === "RP-COOL-001" || text.includes("upper radiator hose")) {
      return ["20260430_220004_gp_C9oYiYmA", "20260503_160327_gp_sFtQuWNQ", "20260503_153249_gp_Lg6JX6Gg"];
    }
    if (id === "RPO-COOL-002" || id === "HLS-02" || id === "RP-COOL-002" || text.includes("lower radiator hose")) {
      return ["20260430_215957_gp_2iBbUagw", "20260503_160010_gp_9F5ZH8kQ", "20260503_155956_gp_P4xfMJzw"];
    }
    if (id === "RPO-COOL-003" || id === "HLS-03" || id === "RP-COOL-003" || text.includes("overflow hose")) {
      return ["20260503_153639_gp_ZueGlpJw", "20260503_153647_gp_L54euoMQ", "20260503_155956_gp_P4xfMJzw"];
    }
    if (id === "RPO-COOL-004A" || id === "RPO-COOL-004B" || id === "HLS-04" || id === "RP-COOL-004" || text.includes("heater hose")) {
      return ["20260503_155747_gp_s91OxyAA", "20260503_155825_gp_Gvgy4PXA", "20260503_153200_gp_YXNuQgGQ"];
    }
    if (id === "RPO-FUEL-001B" || id === "HLS-07" || text.includes("return/bleed")) {
      return ["20260503_160427_gp_HSrKmfzw", "20260503_152937_gp_HdsO0xMA", "20260503_160207_gp_43b3TblQ"];
    }
    if (id === "RPO-FUEL-001C" || id === "HLS-08" || text.includes("leak-off")) {
      return ["20260503_155314_gp_et0BrVkQ", "20260503_160427_gp_HSrKmfzw", "20260503_160207_gp_43b3TblQ"];
    }
    if (id === "RPO-FUEL-001A" || id === "HLS-06" || id === "RP-FUEL-001" || text.includes("diesel feed")) {
      return ["20260503_152937_gp_HdsO0xMA", "20260503_153042_gp_ZL9JEazw", "20260503_160427_gp_HSrKmfzw", "20260504_090640_user_long_diesel_feed_measurement"];
    }
    if (id === "RPO-FUEL-002A" || id === "RPO-FUEL-002B" || id === "HLS-13" || id === "HLS-14" || id === "RP-FUEL-002" || text.includes("fuel hard line")) {
      return ["20260503_152926_gp_4eOEiLQQ", "20260503_153130_gp_gkKoFapg", "20260501_194026_gp_gjPjhxdA"];
    }
    if (id === "RPO-VAC-001A" || id === "HLS-10" || id === "RP-VAC-001" || text.includes("vacuum hose")) {
      return ["20260503_155132_gp_r4UGNnsQ", "20260503_153200_gp_YXNuQgGQ", "20260503_160427_gp_HSrKmfzw"];
    }
    if (id === "RPO-VAC-001C" || id === "HLS-20" || text.includes("oil outlet")) {
      return ["20260503_155314_gp_et0BrVkQ", "20260503_160207_gp_43b3TblQ", "20260503_160427_gp_HSrKmfzw"];
    }
    if (id === "RPO-VAC-001B" || id === "HLS-11" || text.includes("breather") || text.includes("oil-mist")) {
      return ["20260503_155314_gp_et0BrVkQ", "20260503_160207_gp_43b3TblQ", "20260503_160327_gp_sFtQuWNQ"];
    }
    if (id === "RPO-BRAKE-001A" || id === "HLS-17" || id === "RP-BRAKE-001" || text.includes("brake flex")) {
      return ["20260503_152902_gp_xBbsFRzQ", "20260503_152913_gp_AvVGAlHw", "20260503_160050_gp_3aBjHmzw"];
    }
    if (id === "RPO-BRAKE-001B" || id === "HLS-15" || text.includes("brake hard-line") || text.includes("brake tube")) {
      return ["20260503_153017_gp_dM8BCa4w", "20260503_153031_gp_rFfqDUBw", "20260503_153130_gp_gkKoFapg"];
    }
    if (id === "RPO-CLUTCH-001A" || id === "RPO-CLUTCH-001B" || id === "HLS-18" || id === "HLS-19" || id === "RP-CLUTCH-001" || text.includes("clutch")) {
      return ["20260430_215915_gp_ycQ395Gg", "20260430_215939_gp_EjZ7u1ow", "20260430_233755_gp_DO69MLAA"];
    }
    if (id === "RPO-CLIP-001" || id === "HLS-16" || text.includes("p-clip") || text.includes("edge protection")) {
      return ["20260503_153130_gp_gkKoFapg", "20260503_153017_gp_dM8BCa4w", "20260503_152926_gp_4eOEiLQQ"];
    }
    if (id === "RPO-COOL-005" || id === "HLS-12" || id === "RP-COOL-005" || text.includes("formed metal coolant")) {
      return ["20260502_004106_gp_wlYlUahA", "20260502_004044_gp_Hx4Yo0Qg"];
    }
    if (id === "RPO-COOL-006A" || id === "HLS-05A") {
      return ["20260502_004133_gp_ZEpqmARA", "20260502_004044_gp_Hx4Yo0Qg"];
    }
    if (id === "RPO-COOL-006B" || id === "HLS-05B") {
      return ["20260502_004145_gp_e8soxsyA", "20260502_004139_gp_jt1dGw4A", "20260502_004044_gp_Hx4Yo0Qg"];
    }
    if (id === "RP-COOL-006" || text.includes("connector hose")) {
      return ["20260502_004133_gp_ZEpqmARA", "20260502_004145_gp_e8soxsyA", "20260502_004044_gp_Hx4Yo0Qg"];
    }
    return [];
  }

  function suppressScoutEvidenceImages(row) {
    const id = cleanString((row && (row.id || row.order_id || row.order_line_id || row.requirement_id)) || "").toUpperCase();
    const text = [
      id,
      row && row.item,
      row && row.requirement_name,
      row && row.partNumber,
      row && row.part_number_or_code,
    ]
      .map((value) => cleanString(value).toLowerCase())
      .join(" ");
    return id === "HLS-21" ||
      id.startsWith("HLS-") ||
      /^RPO-(COOL|FUEL|VAC|BRAKE|CLUTCH|CLIP)-/.test(id) ||
      id === "RHA-014" ||
      id === "RUB-027" ||
      text.includes("air-cleaner intake") ||
      text.includes("formed metal coolant") ||
      text.includes("formed coolant pipe") ||
      text.includes("hard-line") ||
      text.includes("hard line") ||
      text.includes("user-selected loose fastener photo") ||
      text.includes("user-selected loose hardware photo");
  }

  function bestScoutOriginalImage(row) {
    const suppressEvidence = suppressScoutEvidenceImages(row);
    const evidence = suppressEvidence ? [] : scoutEvidenceImages(row);
    const preferredIds = preferredScoutMediaIds(row);
    const preferred = evidence.find((image) => preferredIds.includes(cleanString(image && image.media_id)));
    if (preferred) {
      return preferred;
    }
    if (evidence.length) {
      return evidence[0];
    }
    if (suppressEvidence) {
      return null;
    }
    const image = row && row.image && !isImageDeleted(row.image) ? row.image : null;
    if (image && !shouldReplaceScoutRowImage(row, image)) {
      return image;
    }
    return null;
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
      const generatedImage = specRow.image && !suppressScoutEvidenceImages(specRow) && !shouldReplaceScoutRowImage(specRow, specRow.image)
        ? specRow.image
        : null;
      specRow.image = bestScoutOriginalImage(specRow) || generatedImage || scoutComponentImage(specRow);
      return specRow;
    });
  }

  function chassisRubberScoutSpecRows() {
    return CHASSIS_RUBBER_SPEC_ROWS.map((row) => {
      const imagePath = cleanString(row.image);
      const mediaId = imagePath.split("/").pop().replace(/\.[^.]+$/, "") || row.id;
      const isReferenceAsset = imagePath.includes("/reference_catalog/");
      const image = imagePath.toLowerCase().endsWith(".svg") || isReferenceAsset
        ? scoutReferenceImage(imagePath, row.imageCaption || row.part, mediaId)
        : scoutPreviousPartImage(imagePath, `${row.part} · original/sample reference`, mediaId, [row.id.toLowerCase()]);
      const fileNames = Array.isArray(row.files) && row.files.length
        ? row.files.map(([, href]) => cleanString(href).split("/").pop()).filter(Boolean).join(" / ")
        : "machine_definitions.csv / machine_definitions.json";
      const isCup = row.id.startsWith("BM-CUP");
      const isShim = row.id.startsWith("BM-SHIM");
      const isBump = row.id.startsWith("BUMP");
      const isExhaust = row.id.startsWith("EXH-");
      const isHold = cleanString(row.qty).toLowerCase() === "hold" || row.id.includes("HOLD") || cleanString(row.part).toLowerCase().includes("hold");
      return {
        id: row.id,
        item: row.part,
        partNumber: fileNames,
        route: row.route,
        state: isHold ? "hold_measurement_required" : isBump ? "vehicle_measurement_mould_release" : isShim ? "trace_then_cut" : "quote_first_article_ready",
        spec: row.spec,
        dimension: row.location,
        qty: row.qty,
        material: isCup
          ? "New 2.5-3.0 mm steel, zinc plated or epoxy primed after forming."
          : isShim
            ? "New flat steel, deburred and zinc plated or epoxy primed."
            : isBump
            ? "NR/SBR automotive bump-stop rubber Shore A 70 +/-5 using May 31 front-stop rubber through-holes, central fixture/channel interface, and sample-proven fixture/insert retention; no used or universal mismatch."
              : isExhaust
                ? "New heat/vibration-resistant molded exhaust rubber, Shore A 60 +/-5."
                : "New black EPDM or NR/SBR automotive mount rubber, Shore A 60 +/-5.",
        sourceBasis: isBump
          ? "docs/bump-stop-fabrication-spec-20260504.md; docs/longman-rubber-order-spec-20260508.md; data/manual/longman_rubber_order_specs.csv"
          : "docs/longman-rubber-order-spec-20260508.md; data/manual/longman_rubber_order_specs.csv; docs/chassis-rubbers-workstream.md",
        action: isHold
          ? "Do not order production until the physical trace/location measurement hold closes."
          : isShim
          ? "Trace preserved station footprint before CNC/laser cutting final outline."
          : isBump
            ? "Measure May 31 front-stop sample/photos, removed fixture, cleaned vehicle bracket BL/BW, rubber through-hole pitch P, hole/thread D, fixture/channel, strike-pad X/Y, loaded gap G, and full-bump clearance F; make 70 mm long-family and 60 mm right-front first articles before full set."
            : "Send DXF/SVG/PDF package in millimeters; quote one first article before batch.",
        reject: isBump
          ? "Used, cracked, oil-softened, simple cut block, universal height/profile, or wrong bracket/contact fit."
          : "Used/salvage material, wrong scale, wrong thickness, or sample mismatch.",
        notes: row.notes,
        image,
      };
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

  function scoutPreviousFabricatedPartImage(row, text) {
    const rowId = cleanString(row && row.id).toUpperCase();
    const partNumber = cleanString(row && row.partNumber).toLowerCase();
    const route = cleanString(row && row.route).toLowerCase();
    const blob = `${cleanString(text).toLowerCase()} ${rowId.toLowerCase()} ${partNumber}`;
    const subject = cleanString(row && row.item) || cleanString(row && row.id) || "Fabricated part";
    const has = (...tokens) => tokens.every((token) => blob.includes(token));
    const hasAny = (...tokens) => tokens.some((token) => blob.includes(token));
    const previous = (path, label, mediaId, tokens = []) =>
      scoutPreviousPartImage(path, `${subject} · ${label}`, mediaId, tokens);
    const controlledIds = new Set([
      "BM-ISO-SM",
      "BM-ISO-LG",
      "BM-SM",
      "BM-LG",
      "BM-CUP-SM",
      "BM-CUP-LG",
      "BM-SHIM-THIN",
      "BM-SHIM-THICK",
      "FS-OVAL",
      "FS-STRIP-L",
      "FS-STRIP-R",
      "BUMP-60010-LONG",
      "BUMP-60020-SHORT",
      "MIDI5-ENC-BODY-001",
      "MIDI5-LID-001",
      "MIDI5-SUBPLATE-001",
      "PWR-CARRIER-001",
      "BPCC-BACKPLANE-001",
      "BPCC-CH-TAB-001",
      "BPCC-OFFSET-BAR-001",
      "BPCC-GUSSET-001",
      "BPCC-GUARD-001",
      "RELAY-BASE-001",
      "RELAY-INSULATOR-001",
    ]);
    const isFabricationRow =
      controlledIds.has(rowId) ||
      partNumber.endsWith(".dxf") ||
      ["rubber_recreation_rev_a", "midi5_enclosure_rev_d", "midi5_plate_mount_rev_c", "relay_mount_rev_d", "relay_mount_rev_c", "battery_power_carrier_mount_rev_a"].some((token) => route.includes(token));

    if (!isFabricationRow) {
      return null;
    }

    if (rowId === "BM-CUP-SM" || partNumber.includes("bm_cup_small") || (has("cup", "small") && hasAny("body-mount", "body mount"))) {
      return previous("../../photos/20260502_004413_gp_Qno8OVRg.jpg", "previous small body-mount cup/seat sample", "20260502_004413_gp_Qno8OVRg", ["bm-cup-sm", "previous"]);
    }
    if (rowId === "BM-CUP-LG" || partNumber.includes("bm_cup_large") || (has("cup", "large") && hasAny("body-mount", "body mount"))) {
      return previous("../../photos/20260502_004419_gp_ZPXJRBzg.jpg", "previous large body-mount cup/seat sample", "20260502_004419_gp_ZPXJRBzg", ["bm-cup-lg", "previous"]);
    }
    if (hasAny("body-mount cup", "body mount cup", "cup / seat", "cup washer", "seat washer", "bm-cup")) {
      return previous("../../photos/20260502_004413_gp_Qno8OVRg.jpg", "previous body-mount cup/seat sample", "20260502_004413_gp_Qno8OVRg", ["bm-cup", "previous"]);
    }
    if (rowId === "BM-SHIM-THIN" || rowId === "BM-SHIM-THICK" || hasAny("bm-shim", "alignment shim", "shim pack", "spacer control pack")) {
      return scoutReferenceImage("../../deliverables/selling_site_images/images/reference_catalog/body_shims.jpg", "Body-mount shim/spacer reference", "body_shims");
    }
    if (rowId === "BM-ISO-LG" || rowId === "BM-ISO-SM" || hasAny("main body isolator pad", "custom square flat pad", "body isolator pad")) {
      return previous("../../photos/20260528_193054_gp_UFyTb44w.jpg", "old body-mount rubber samples with tape", "20260528_193054_gp_UFyTb44w", ["bm-iso", "old-rubber"]);
    }
    if (rowId === "BM-LG" || partNumber.includes("bm_lg") || hasAny("large circular body-mount", "large circular body mount", "large body-mount cushion", "large body mount cushion")) {
      return previous("../../photos/20260502_004419_gp_ZPXJRBzg.jpg", "previous large circular body-mount cushion sample", "20260502_004419_gp_ZPXJRBzg", ["bm-lg", "previous"]);
    }
    if (rowId === "BM-SM" || partNumber.includes("bm_sm") || hasAny("small circular body-mount", "small circular body mount", "small body-mount cushion", "small body mount cushion")) {
      return previous("../../photos/20260502_004442_gp_7WcFHjLQ.jpg", "previous small circular body-mount cushion sample", "20260502_004442_gp_7WcFHjLQ", ["bm-sm", "previous"]);
    }
    if (rowId === "FS-OVAL" || partNumber.includes("fs_oval") || hasAny("two-hole oval", "two hole oval", "oval front-support", "oval front support", "oval pad")) {
      return previous("../../photos/20260502_004345_gp_yK8VYzMQ.jpg", "previous two-hole oval front-support pad", "20260502_004345_gp_yK8VYzMQ", ["fs-oval", "previous"]);
    }
    if (rowId === "BUMP-60010-LONG" || hasAny("long axle-to-chassis bump stop", "48304-60010", "long bump stop")) {
      return previous("../../photos/20260531_171824_gp_HmSS2ChQ.jpg", "May 31 exact front bump-stop face/width view", "20260531_171824_gp_HmSS2ChQ", ["bump-stop", "may31", "front-stop"]);
    }
    if (rowId === "BUMP-60020-SHORT" || hasAny("short right-front bump stop", "48304-60020", "right-front bump stop")) {
      return previous("../../photos/20260531_171935_gp_BYfhqiWg.jpg", "May 31 exact front bump-stop side height/profile view", "20260531_171935_gp_BYfhqiWg", ["bump-stop", "may31", "front-stop"]);
    }
    if (rowId === "FS-STRIP-L" || partNumber.includes("fs_strip_left") || (hasAny("front-support strip", "front support strip", "strip rubber") && hasAny("left", "left-side", "left side"))) {
      return previous("../../photos/20260528_193200_gp_HICSdovA.jpg", "old left strip rubber section with tape", "20260528_193200_gp_HICSdovA", ["fs-strip-l", "old-rubber"]);
    }
    if (rowId === "FS-STRIP-R" || partNumber.includes("fs_strip_right") || (hasAny("front-support strip", "front support strip", "strip rubber") && hasAny("right", "right-side", "right side"))) {
      return previous("../../photos/20260528_193253_gp_f0eQuSFA.jpg", "old right strip rubber section with tape", "20260528_193253_gp_f0eQuSFA", ["fs-strip-r", "old-rubber"]);
    }
    if (rowId === "MIDI5-ENC-BODY-001" || rowId === "MIDI5-LID-001" || rowId === "MIDI5-SUBPLATE-001" || hasAny("midi5_enclosure", "midi5_mount_plate", "midi5_holder_subplate", "midi 5-way structural", "midi 5-way non-conductive")) {
      return previous("../../photos/20260411_143135.jpg", "received MIDI holder bank to mount", "20260411_143135", ["midi5", "previous"]);
    }
    if (rowId === "RELAY-BASE-001" || rowId === "RELAY-INSULATOR-001" || hasAny("relay_base_plate", "relay_insulating_sheet", "daier prewired", "10-way relay/fuse", "10 way relay/fuse")) {
      return previous("../../photos/20260411_143125.jpg", "received 10-way relay/fuse box to mount", "20260411_143125", ["relay-box", "previous"]);
    }

    return null;
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
      return ref("../../deliverables/selling_site_images/images/manual_overrides/compact_cabin_fuse_box_user_photo_20260504.png", "user-supplied compact old-OEM fuse box photo", "compact_cabin_fuse_box_user_photo_20260504");
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
      return ref("../../deliverables/selling_site_images/images/manual_overrides/formed_coolant_pipe_sample_crop_20260502.jpg", "current car formed coolant pipe sample crop", "formed_coolant_pipe_sample_crop_20260502");
    }
    if (hasAny("p-clips", "p clips", "support clips", "line protection", "edge protection")) {
      return ref("../../deliverables/selling_site_images/images/reference_catalog/clamp.jpg", "line clip/clamp reference image", "clamp");
    }
    if (hasAny("hard-line", "hard line", "hard-line tube", "hard line tube", "brake hard-line", "brake hard line", "fuel hard-line", "fuel hard line", "clutch hard-line", "clutch hard line")) {
      return ref("../../deliverables/selling_site_images/images/manual_overrides/rear_axle_hardline_union_current_car_crop_20260503.jpg", "current car hard-line route and union crop", "rear_axle_hardline_union_current_car_crop_20260503");
    }
    if (hasAny("brake flex hose", "clutch flex hose", "flex hose assemblies", "flexible brake hose", "hydraulic hose assemblies")) {
      return ref("../../deliverables/selling_site_images/images/manual_overrides/front_brake_hose_fitting_current_car_crop_20260503.jpg", "current car hydraulic flex hose fitting crop", "front_brake_hose_fitting_current_car_crop_20260503");
    }
    if (hasAny("connector hose", "connector/coupler", "coupler hoses")) {
      return ref("../../deliverables/selling_site_images/images/manual_overrides/radiator_heater_hose_current_car_crop_20260503.jpg", "current car connector hose crop", "radiator_heater_hose_current_car_crop_20260503");
    }
    if (hasAny("air-cleaner", "air cleaner", "intake duct", "air-intake", "air intake", "duct/coupler")) {
      return ref("../../deliverables/selling_site_images/images/reference_catalog/duct_hose.jpg", "air-cleaner intake duct reference image", "duct_hose");
    }
    if (hasAny("a/c barrier", "ac barrier", "air conditioning", "refrigerant")) {
      return ref("../../deliverables/selling_site_images/images/reference_catalog/ac_barrier_hose.jpg", "A/C barrier hose reference image", "ac_barrier_hose");
    }
    if (has("heater", "hose")) {
      return ref("../../deliverables/selling_site_images/images/manual_overrides/radiator_heater_hose_current_car_crop_20260503.jpg", "current car heater hose crop", "radiator_heater_hose_current_car_crop_20260503");
    }
    if (hasAny("radiator overflow", "overflow hose", "coolant overflow")) {
      return ref("../../deliverables/selling_site_images/images/manual_overrides/radiator_cap_current_car_crop_20260503.jpg", "current car radiator neck and overflow crop", "radiator_cap_current_car_crop_20260503");
    }
    if (has("radiator", "hose") || has("coolant", "hose") || hasAny("upper radiator", "lower radiator")) {
      return ref("../../deliverables/selling_site_images/images/manual_overrides/radiator_heater_hose_current_car_crop_20260503.jpg", "current car radiator/coolant hose crop", "radiator_heater_hose_current_car_crop_20260503");
    }
    if ((has("brake", "booster") || has("brake", "servo")) && !hasAny("hose", "line", "pipe", "tube")) {
      return ref("../../deliverables/selling_site_images/images/reference_catalog/brake_booster.jpg", "brake booster reference image", "brake_booster");
    }
    if (hasAny("fuel clamp", "clamp pack", "hose clamp", "hose clamps")) {
      return ref("../../deliverables/selling_site_images/images/expenses_jubilee_hose_clip_assortment_10_pc_fuel__2a666ef4bae6.jpg", "fuel hose clamp reference image", "fuel_hose_clamp_assortment");
    }
    if (hasAny("fuel", "diesel", "injector leak-off", "leak-off")) {
      return ref("../../deliverables/selling_site_images/images/manual_overrides/fuel_hose_line_fittings_current_car_crop_20260503.jpg", "current car fuel hose and fitting crop", "fuel_hose_line_fittings_current_car_crop_20260503");
    }
    if (hasAny("vacuum", "breather", "oil mist", "oil outlet")) {
      return ref("../../deliverables/selling_site_images/images/manual_overrides/vacuum_breather_hose_current_car_crop_20260503.jpg", "current car vacuum and breather hose crop", "vacuum_breather_hose_current_car_crop_20260503");
    }
    if (has("brake") && hasAny("hose", "line", "hydraulic", "tube")) {
      return ref("../../deliverables/selling_site_images/images/manual_overrides/front_brake_hose_fitting_current_car_crop_20260503.jpg", "current car brake hose fitting crop", "front_brake_hose_fitting_current_car_crop_20260503");
    }
    if (has("clutch") && hasAny("hose", "line", "hydraulic", "tube")) {
      return ref("../../deliverables/selling_site_images/images/manual_overrides/clutch_hydraulic_slave_line_current_car_crop_20260430.jpg", "current car clutch hydraulic line crop", "clutch_hydraulic_slave_line_current_car_crop_20260430");
    }
    if (hasAny("p-clips", "p clips", "support clips", "line protection", "edge protection")) {
      return ref("../../deliverables/selling_site_images/images/reference_catalog/clamp.jpg", "line clip/clamp reference image", "clamp");
    }
    if (hasAny("retaining clip", "r-clips", "r clips", "hairpins", "hairpin", "split pins", "split pin", "cotter pins", "cotter", "circlips", "e-clips", "e clips")) {
      return ref("../../deliverables/selling_site_images/images/manual_overrides/body_retaining_clips_cotter_pack_reference.svg", "retaining clip and cotter reference image", "body_retaining_clips_cotter_pack_reference");
    }
    if (hasAny("captive/clip", "clip/speed nut", "captive nuts", "clip nuts", "speed nut", "speed nuts", "weld/rivnut", "weld nut", "weld nuts", "rivnuts", "rivnut")) {
      return ref("../../deliverables/selling_site_images/images/manual_overrides/body_captive_clip_nuts_reference.svg", "captive clip nut and rivnut reference image", "body_captive_clip_nuts_reference");
    }
    if (hasAny("trim screws", "self-tapping", "self tapping", "countersunk", "cup/finishing", "finishing washers")) {
      return ref("../../deliverables/selling_site_images/images/manual_overrides/body_trim_screws_cup_washers_reference.svg", "trim screws and cup washers reference image", "body_trim_screws_cup_washers_reference");
    }
    if (hasAny("rubber/plastic", "rubber bumpers", "plastic bumpers", "rubber bumper", "isolators", "knobs and small spacers", "pads isolators")) {
      return ref("../../deliverables/selling_site_images/images/manual_overrides/body_rubber_bumpers_isolators_reference.svg", "rubber bumpers and isolators reference image", "body_rubber_bumpers_isolators_reference");
    }
    if (hasAny("shoulder bolts", "shoulder bolt", "pivot pins", "pivot pin", "cylindrical sleeves", "stand-off spacers", "standoff spacers", "stand-offs", "stepped pins")) {
      return ref("../../deliverables/selling_site_images/images/manual_overrides/body_shoulder_pins_sleeves_spacers_reference.svg", "shoulder pins sleeves and spacers reference image", "body_shoulder_pins_sleeves_spacers_reference");
    }
    if (hasAny("specialty brackets", "specialty bracket", "retainer plates", "retainer plate", "captive-nut plates", "captive nut plates", "strap brackets", "bent link/strap")) {
      return ref("../../deliverables/selling_site_images/images/manual_overrides/body_specialty_brackets_retainer_plates_reference.svg", "specialty bracket and retainer plate reference image", "body_specialty_brackets_retainer_plates_reference");
    }
    if (hasAny("body mount hardware", "body mount bolts", "bolts sleeves washers")) {
      return ref("../../deliverables/selling_site_images/images/manual_overrides/body_mount_hardware_sleeves_washers_reference.svg", "body mount hardware sleeves and washers reference image", "body_mount_hardware_sleeves_washers_reference");
    }
    if (hasAny("body mount shim", "body shims", "shim/spacer", "shims/spacers", "shim and spacer")) {
      return ref("../../deliverables/selling_site_images/images/manual_overrides/body_mount_shim_pack_reference.svg", "body mount shim and spacer reference image", "body_mount_shim_pack_reference");
    }
    if (hasAny("body mount rubber kit", "body-to-chassis mount rubber", "body to chassis mount rubber")) {
      return ref("../../deliverables/selling_site_images/images/manual_overrides/body_mount_rubber_kit_reference.svg", "body mount rubber kit reference image", "body_mount_rubber_kit_reference");
    }
    if (has("bump", "stop") || hasAny("rubber bumpers", "rubber bumper")) {
      return ref("../../data/manual/fabrication/rubber_recreation_rev_a/bump_stop_vehicle_measurement_control.svg", "bump-stop measurement control", "bump_stop_vehicle_measurement_control");
    }
    if (hasAny("shim", "spacer pack", "spacer control pack")) {
      return ref("../../deliverables/selling_site_images/images/reference_catalog/body_shims.jpg", "body-mount shim/spacer reference image", "body_shims");
    }
    if (hasAny("cup washer", "cup / seat", "seat washer", "crush sleeve")) {
      return ref("../../photos/20260502_004413_gp_Qno8OVRg.jpg", "body-mount cup/seat sample photo", "body_mount_cup_seat_sample");
    }
    if (has("body", "mount") || hasAny("cushion", "front-support", "front support", "oval pad")) {
      return ref("../../deliverables/selling_site_images/images/reference_catalog/body_mount_kit.jpg", "body mount rubber reference image", "body_mount_kit");
    }
    if (has("exhaust", "hanger")) {
      return ref("../../deliverables/selling_site_images/images/reference_catalog/exhaust_hanger.jpg", "exhaust hanger reference image", "exhaust_hanger");
    }
    if (hasAny("glow plug", "heat plug")) {
      return ref("../../deliverables/selling_site_images/images/reference_catalog/glow_plugs.jpg", "glow plug reference image", "glow_plugs");
    }
    return ref("../../deliverables/selling_site_images/images/reference_catalog/generic_part.jpg", "component reference image", "generic_part");
  }

  function firstScoutImage(rows) {
    const sourceRows = Array.isArray(rows) ? rows : [];
    for (const row of sourceRows) {
      const generatedImage = row && !suppressScoutEvidenceImages(row) && row.image && !isImageDeleted(row.image) ? row.image : null;
      const image = bestScoutOriginalImage(row) || generatedImage;
      if (image) {
        return image;
      }
    }
    return null;
  }

  function scoutSpecImage(rows, fallbackImage) {
    return firstScoutImage(rows) || fallbackImage || null;
  }

  function attachScoutImage(specs, rows, fallbackImage) {
    const image = scoutSpecImage(rows, fallbackImage);
    return (Array.isArray(specs) ? specs : []).map((spec) => ({
      ...spec,
      image: spec.image || (Array.isArray(spec.images) && spec.images.length ? null : image),
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
    const steeringWorkstream = workstreamById("eps_vitz_upgrade");
    const replacementPipesWorkstream = workstreamById("replacement_pipes");
    const chassisRubbersWorkstream = workstreamById("chassis_rubbers");
    const fabricationWorkstream = workstreamById("fabrication_handoff");
    const steeringMarketSpecs = [
      ...((steeringWorkstream && steeringWorkstream.market_specs) || []),
      ...((parts.market_specs || []).filter((spec) => cleanString(spec.id).includes("j60_hydraulic_steering"))),
    ];
    const brakeMarketSpecs = (parts.market_specs || []).filter((spec) => cleanString(spec.id).includes("brake_booster"));
    const steeringParts = filterScoutRows(allPartRows, {
      entryIds: ["part_power_steering_upgrade"],
      workstreams: ["eps_vitz_upgrade"],
      terms: ["j60", "hj60", "hydraulic steering", "steering box", "pitman", "drag link", "power steering pump"],
    });
    const brakeBoosterParts = filterScoutRows(allPartRows, {
      entryIds: ["part_brake_booster_servo_44610_60050"],
      workstreams: ["brake_system"],
      terms: ["brake booster", "brake servo", "44610-60050", "vacuum booster"],
    });
    const brakeBoosterImageRows = filterScoutRows(allPartRows, {
      entryIds: ["part_brake_booster_servo_44610_60050"],
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
    const rubberRequirementSpecRows = scoutOrderSpecRows((chassisRubbersWorkstream && chassisRubbersWorkstream.chassis_rubber_requirements) || []);
    const rubberSupportRequirementRows = rubberRequirementSpecRows.filter((row) =>
      ["CR-MAIN-003", "CR-HARD-001"].includes(cleanString(row.id).toUpperCase())
    );
    const rubberScoutSpecRows = [
      ...chassisRubberScoutSpecRows(),
      ...rubberSupportRequirementRows,
    ];
    const longmanPipeHoseOrderRows =
      (data.longman_order_sheets && data.longman_order_sheets.pipe_hose) ||
      (data.local_market_order_sheets && data.local_market_order_sheets.hose) ||
      [];
    const pipeExactSpecRows = scoutOrderSpecRows((replacementPipesWorkstream && replacementPipesWorkstream.replacement_pipe_order_release_specs) || []);
    const fuseBoxParts = filterScoutRows(allPartRows, {
      entryIds: ["part_cabin_compact_fuse_boxes"],
      workstreams: ["electrical_reset"],
      terms: ["compact cabin fuse", "additional fuse", "fuse box", "fuse carrier"],
    });
    const fuseBoxImageRows = filterScoutRows(allPartRows, {
      entryIds: ["part_cabin_compact_fuse_boxes"],
    });
    const workshopSupportParts = dedupeScoutRows([
      ...filterScoutRows(allSupplyRows, {
        entryIds: ["tool_local_toolbench"],
        workstreams: ["site_setup", "fabrication_handoff"],
        terms: ["workbench", "toolbench"],
      }),
    ]);
    const toolbenchImageRows = filterScoutRows(allSupplyRows, {
      entryIds: ["tool_local_toolbench"],
    });
    const toolbenchImage = firstScoutImage(toolbenchImageRows) ||
      scoutReferenceImage("../../deliverables/selling_site_images/images/reference_catalog/toolbench.jpg", "toolbench/workbench reference image", "toolbench");
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
      id: "pipes_hoses_longman_order",
      title: "Longman Pipe + Hose Order",
      scope: "Exact order sheet",
      quantity: "23 HLS line items plus 21 pipe release-spec lines",
      plain_stall_request:
        "I need Longman Mills to quote new replacement components only for the J40/HJ47 hose, pipe, hard-line, brake/clutch hydraulic, fuel, vacuum, and support-clip lines from the order sheet. Use those IDs and specs; old parts/photos are samples only. Do not quote used parts or generic rubber pipe.",
      buy_target:
        "Use the exact Longman requirement list below and the linked order spec. New EPDM for coolant/heater, new diesel-rated fuel hose, new reinforced vacuum hose, new brake-rated hard line, and new complete crimped DOT/SAE J1401 or OEM-equivalent brake/clutch hose assemblies only if certified hydraulic capability is confirmed.",
      must_include: [
        "Correct inside diameter, length, bends, or end fittings matched to the old sample.",
        "New clamps, clips, or fittings quoted separately when needed.",
        "Every hose, rubber, clamp, clip, fitting, hard line, hydraulic assembly, and cable used for final installation must be new.",
        "Brake and clutch flex hoses supplied as complete crimped assemblies.",
        "Brake hard-line material only in new brake-rated 4.75 mm / 3/16 in tube.",
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
        "Any hose, rubber, hydraulic assembly, cable, wire, line, clip, clamp, or fitting is used, salvage, old stock, cracked, swollen, oily, unmarked where markings are required, or already cut too short.",
      ],
      capture_before_leaving: [
        "Photo of each new hose or line beside the old sample or measurement note.",
        "Photo of all end fittings, clamps, clips, and visible rating marks.",
        "Seller name, phone number, shop location, price by line, and return terms.",
      ],
      price_guidance: {
        rule: "Quote each line separately. Do not pay for any brake, clutch, fuel, or vacuum item until sample match and material type are clear.",
      },
      decision_rule: "Quote every hose, rubber, brake, clutch, fuel, vacuum, line-support, and cable item as a new replacement component; buy only the new items that match the old sample or confirmed measurement and have the correct material rating.",
      links: [
        scoutDocLink("docs/longman-pipe-hose-order-spec-20260512.md", "Longman pipe/hose order spec"),
        scoutDocLink("data/manual/longman_pipe_hose_order_specs.csv", "Longman pipe/hose order CSV"),
        scoutDocLink("docs/engine-hose-tube-replacement-specs.md", "Engineering controls"),
      ],
    };
    const rubberMarketSpec = {
      id: "body_mount_rubbers_market_scout",
      title: "Consolidated Longman Rubber Market Scout",
      scope: "Single quote bundle",
      quantity: "3 supplier-facing rubber order groups plus separate controlled hardware rows and all-rubbers coverage check",
      plain_stall_request:
        "I need one consolidated quote for the exact new-only J40 body/front-support/chassis custom rubber bundle listed in the Longman spec. Quote the rubber lines together; sleeves, cup washers, shims, spacers, bolts, nuts, and washers are separate controlled hardware lines. Toyota/OE part numbers are reference shapes only. Old rubbers/photos are samples only. No used or salvage rubber.",
      buy_target:
        "Ask Longman for 3 things: 1) simple 80 x 80 body pads: one active 80 x 80 x 24 pad size, 30 pieces total; the smaller 22 mm body-rubber line is removed; 2) front support/body-support rubbers: FS-OVAL x2 plus FS-STRIP-L/R x1 each; 3) bump stops: BUMP-60010-LONG x3 and BUMP-60020-SHORT x1. The extra body pads are dry-fit allowance for stations that prove they need two stacked pads, not a release for new ribbed or shaped body-rubber variants. Full-width flat liners and the exhaust hanger remain hold/reference lines only. Before buying any other rubber, check the all-rubbers matrix for hoses, grommets, suspension bushes, powertrain mounts, weatherstrips, HVAC rubber, seals, and hangers so they stay in their own gates. For bump stops, use the May 31 exact front-stop photos as the construction pattern, rear/back stops as the same shape made longer, plus the removed fixture, 70 mm long / 60 mm right-front height controls, and vehicle bracket measurements.",
      must_include: [
        "Upper and lower body mount rubber cushions for the required body stations.",
        "Steel sleeves, cup or seat washers, shims, spacers, bolts, nuts, and washers quoted separately.",
        "Rubber dimensions shown clearly: outside size, thickness, hole/insert status, and any sleeve-controlled final hole.",
        "Fabrication quote basis for every non-stock rubber: drawing/profile, old sample, 3D scan, or vehicle-bracket measurement requirement, material/hardness, first article, and dry-fit check.",
        "New rubber only for every fitted rubber, grommet, pad, cushion, boot, sleeve cover, isolator, bump stop, and hanger.",
      ],
      bench_test: [
        "Compare every rubber and sleeve to the old sample or written dimension sheet before payment or mould release.",
        "Press the rubber by hand: it should feel firm and elastic, not brittle or sponge-soft.",
        "Check sleeves and washers with the actual bolt size before payment.",
        "Keep shim and spacer thicknesses separated and labelled.",
      ],
      reject_if: [
        "Seller offers old used rubber, salvage rubber, unknown mixed rubber, sponge rubber, or cracked stock.",
        "Sleeve hole, rubber height, washer shape, shim thickness, moulded profile, or bracket contact face does not match the measured plan.",
        "Hardware has no grade mark, wrong pitch, damaged threads, or heavy rust.",
        "Seller will not allow measurement photos before payment.",
      ],
      capture_before_leaving: [
        "Full kit photo with all rubber, sleeves, washers, shims, spacers, and bolts laid out.",
        "Close photos with ruler/caliper showing key dimensions.",
        "Seller name, phone number, shop location, material claim, price, and return terms.",
      ],
      price_guidance: {
        rule: "Keep the rubber as one Longman bundle with itemized line prices; keep sleeves, cup/seat washers, shims, and bolts outside that rubber quote.",
      },
      decision_rule: "Buy or fabricate only the consolidated new-rubber bundle after the old samples or measurement sheet prove rubber shape, sleeve size, moulded profile, and hardware stack.",
      links: [
        scoutDocLink("docs/longman-rubber-order-spec-20260508.md", "Longman rubber order spec"),
        scoutDocLink("docs/rubber-ordering-spec-20260502.md", "Rubber ordering spec"),
        scoutDocLink("docs/rubber-recreation-fabrication-spec-20260502.md", "Rubber fabrication spec"),
        scoutDocLink("docs/bump-stop-fabrication-spec-20260504.md", "Bump-stop fabrication spec"),
      ],
    };
    const fuseBoxMarketSpec = {
      id: "additional_fuse_box_market_scout",
      title: "Additional Fuse Box Market Scout",
      scope: "Compact OEM-style add-on",
      quantity: "1 compact add-on carrier to match the reusable block",
      plain_stall_request:
        "I need one compact old-OEM under-dash blade-fuse / junction-block style carrier to match the blade-style block extracted from the existing car. Six positions must be usable, with clean rear terminals or serviceable pigtails. Any final wiring, cable, terminals, insulation, and loom protection must be new.",
      buy_target:
        "Reuse the existing extracted compact blade-style donor block for two 6-fuse groups if it tests clean, then buy one matching compact old-OEM add-on carrier for the third group. Prefer Suzuki Mehran/Maruti 800, Daihatsu Cuore, old Alto, old Corolla, or similar compact cabin carriers. Donor pigtails identify circuits only; final install uses new automotive cable, terminals, sleeving, and protection.",
      must_include: [
        "Fuse box body, cover, terminals, and mounting points intact.",
        "Original plugs or at least 100-150 mm wiring tails if it is a used donor fuse box; those tails are samples/identification leads, not final cable stock.",
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
        "Seller offers an old cut loom, used cable bundle, or used terminals as final wiring material.",
        "Large engine-bay relay box, marine/RV stud block, fuse-cover-only listing, or loose fuse assortment.",
        "Single-bus universal block that cannot be split safely for the planned grouped inputs.",
      ],
      capture_before_leaving: [
        "Top, bottom, side, and cover photos.",
        "Close photos of terminals, plugs, wiring tails, and any rating marks.",
        "Seller name, phone number, shop location, price, and return terms.",
      ],
      price_guidance: {
        rule: "Quote the used OEM-style carrier and any new-quality alternative separately. Final wiring/cable/terminal consumables are new-only.",
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
        image: toolbenchImage,
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
        id: "BM-ISO-SM",
        item: "Small square tub-to-chassis body isolator pads",
        partNumber: "longman_rubber_order_specs.csv",
        route: "longman_custom_rubber_order",
        state: "released_for_quote_and_first_article_station_fit_pending",
        image: scoutPreviousPartImage("../../photos/20260528_193054_gp_UFyTb44w.jpg", "Old small body-mount rubber samples with tape", "20260528_193054_gp_UFyTb44w", ["bm-iso-sm", "old-rubber"]),
        spec: "Longman custom square pad with 18.0 mm through bore for Toyota 90560-12009 style body-mount spacer/crush tube.",
        qty: "10 + 6 spares",
        dimension: "3D envelope 80 L x 80 W x 22 H; 18.0 through bore +0.5/-0.0; plan corners R1.5; top/bottom edge break/chamfer 1.0 max; faces parallel <=0.5",
        material: "Black EPDM or NR/SBR, Shore A 60 +/-5",
        sourceBasis: "docs/longman-rubber-order-spec-20260508.md; data/manual/longman_rubber_order_specs.csv",
        action: "Quote/drill/punch as 18.0 mm bore; dry-fit with Toyota 90560-12009 style sleeve and any proven two-pad stack.",
        notes: "Primary custom shape is the simple 80 x 80 square pad; extras cover dry-fit stacking/trim only where proven.",
      },
      {
        id: "BM-ISO-LG",
        item: "Large square tub-to-chassis body isolator pads",
        partNumber: "longman_rubber_order_specs.csv",
        route: "longman_custom_rubber_order",
        state: "released_for_quote_and_first_article_station_fit_pending",
        image: scoutPreviousPartImage("../../photos/20260528_193054_gp_UFyTb44w.jpg", "Old body-mount rubber sample stack with tape", "20260528_193054_gp_UFyTb44w", ["bm-iso-lg", "old-rubber"]),
        spec: "Longman custom square pad. Same compound batch as the small pads where possible; 18.0 mm through bore for Toyota 90560-12009 style spacer.",
        qty: "2 + 2 spares",
        dimension: "3D envelope 80 L x 80 W x 24 H; 18.0 through bore +0.5/-0.0; plan corners R1.5; top/bottom edge break/chamfer 1.0 max; faces parallel <=0.5",
        material: "Black EPDM or NR/SBR, Shore A 60 +/-5",
        sourceBasis: "docs/longman-rubber-order-spec-20260508.md; data/manual/longman_rubber_order_specs.csv",
        action: "Quote/drill/punch as 18.0 mm bore; dry-fit with Toyota 90560-12009 style sleeve and any proven two-pad stack.",
        notes: "Primary custom shape is the simple 80 x 80 square pad; extras cover dry-fit stacking/height correction only where proven.",
      },
      {
        id: "BM-CUP-SM",
        item: "Small body-mount cup washer blank",
        partNumber: "bm_cup_small_seat_washer_rev_a.dxf",
        route: "rubber_recreation_rev_a",
        state: "quote_first_article_ready",
        image: scoutPreviousPartImage("../../photos/20260502_004413_gp_Qno8OVRg.jpg", "Small body-mount cup/seat · separate previous-part sample", "20260502_004413_gp_Qno8OVRg", ["bm-cup-sm", "rubber"]),
        spec: "Cut/form-ready small cup washer blank; confirm cup reuse, dish depth, and forming method before batch.",
        qty: "10 working basis",
        dimension: "Small cup OD 64; M10 clearance hole 11; dish/register depth 2-3; steel thickness 2.5-3.0",
        material: "2.5-3.0 mm steel, zinc plated or epoxy primed after forming",
        sourceBasis: "data/manual/fabrication/rubber_recreation_rev_a/fabricator_cut_list.csv; docs/rubber-recreation-fabrication-spec-20260502.md",
        action: "Cut blank only after confirming old cup/seat construction; form and coat after deburring.",
      },
      {
        id: "BM-CUP-LG",
        item: "Large body-mount cup washer blank",
        partNumber: "bm_cup_large_seat_washer_rev_a.dxf",
        route: "rubber_recreation_rev_a",
        state: "quote_first_article_ready",
        image: scoutPreviousPartImage("../../photos/20260502_004419_gp_ZPXJRBzg.jpg", "Large body-mount cup/seat · separate previous-part sample", "20260502_004419_gp_ZPXJRBzg", ["bm-cup-lg", "rubber"]),
        spec: "Cut/form-ready large cup washer blank; confirm cup reuse, dish depth, and forming method before batch.",
        qty: "2 working basis",
        dimension: "Large cup OD 78; M10 clearance hole 11; dish/register depth 2-3; steel thickness 2.5-3.0",
        material: "2.5-3.0 mm steel, zinc plated or epoxy primed after forming",
        sourceBasis: "data/manual/fabrication/rubber_recreation_rev_a/fabricator_cut_list.csv; docs/rubber-recreation-fabrication-spec-20260502.md",
        action: "Cut blank only after confirming old cup/seat construction; form and coat after deburring.",
      },
      {
        id: "FS-OVAL",
        item: "Two-hole oval front-support isolator pads",
        partNumber: "fs_oval_front_support_pad_rev_a.dxf",
        route: "rubber_recreation_rev_a",
        state: "quote_first_article_ready",
        image: scoutPreviousPartImage("../../photos/20260502_004345_gp_yK8VYzMQ.jpg", "Two-hole oval front-support pad · separate previous-part sample", "20260502_004345_gp_yK8VYzMQ", ["fs-oval", "rubber"]),
        spec: "CNC-ready first article for two-hole oval front-support pad. Use the FS-OVAL row in machine_definitions.csv/json and the DXF/SVG package.",
        qty: "2 matched pieces",
        dimension: "3D envelope 96 L x 64 W x 15 T; capsule ends R32; edge break 0.5-1.0; holes 12 at X32 Y16 and X32 Y80; relief 36 x 18 R3 at X14 Y39; insert/boss mark 29 at X32 Y16",
        material: "Black EPDM or NR/SBR, Shore A 60 +/-5; reuse/bond steel insert if present",
        sourceBasis: "data/manual/fabrication/rubber_recreation_rev_a/machine_definitions.csv",
        action: "Make matched pair; confirm holes, thickness, and insert/boss before batch. INSERT_MARK is not a through cut.",
      },
      {
        id: "FS-STRIP-L",
        item: "Left plain underfloor body-support strip liner",
        partNumber: "fs_strip_left_template_blank_rev_a.dxf",
        route: "rubber_recreation_rev_a",
        state: "released_for_quote_and_first_article_dry_fit_trim_pending",
        image: scoutPreviousPartImage("../../photos/20260528_193200_gp_HICSdovA.jpg", "Old left strip rubber section with tape", "20260528_193200_gp_HICSdovA", ["fs-strip-l", "old-rubber"]),
        spec: "Released first article as a plain flat underfloor body-support / anti-squeak strip. Do not add holes, slots, bonding, or stepped geometry unless dry-fit proves it.",
        qty: "1",
        dimension: "3D envelope 420 L x 38 W x 8 T mm; plan corners R1.5; top/bottom edge break 0.5-1.0; smooth cut edges; flat parallel faces; local end trim only after dry-fit",
        material: "Black EPDM or NR/SBR strip, Shore A 60 +/-5",
        sourceBasis: "docs/longman-rubber-order-spec-20260508.md; data/manual/longman_rubber_order_specs.csv; data/manual/rubber_recreation_measurement_closure.csv",
        reject: "Slots/holes through the rubber, raised-load pad, bonding, or handed trim without installed-sample proof.",
        notes: "Order inside the single consolidated Longman rubber bundle; trace or reuse the steel retainer separately if needed.",
      },
      {
        id: "FS-STRIP-R",
        item: "Right plain underfloor body-support strip liner",
        partNumber: "fs_strip_right_template_blank_rev_a.dxf",
        route: "rubber_recreation_rev_a",
        state: "released_for_quote_and_first_article_dry_fit_trim_pending",
        image: scoutPreviousPartImage("../../photos/20260528_193253_gp_f0eQuSFA.jpg", "Old right strip rubber section with tape", "20260528_193253_gp_f0eQuSFA", ["fs-strip-r", "old-rubber"]),
        spec: "Released first article as the right-side mate to the left strip. Use the same plain blank unless dry-fit proves a handed end trim.",
        qty: "1",
        dimension: "3D envelope 420 L x 38 W x 8 T mm; plan corners R1.5; top/bottom edge break 0.5-1.0; smooth cut edges; flat parallel faces; local handed trim only after dry-fit",
        material: "Black EPDM or NR/SBR strip, Shore A 60 +/-5; same batch/type as left where possible",
        sourceBasis: "docs/longman-rubber-order-spec-20260508.md; data/manual/longman_rubber_order_specs.csv; data/manual/rubber_recreation_measurement_closure.csv",
        reject: "Slots/holes through the rubber, raised-load pad, bonding, or handed trim without installed-sample proof.",
        notes: "Order inside the single consolidated Longman rubber bundle; trace or reuse the steel retainer separately if needed.",
      },
      {
        id: "MIDI5-ENC-BODY-001",
        item: "MIDI 5-way hinged enclosure body",
        partNumber: "midi5_enclosure_body_rev_d.dxf",
        route: "midi5_enclosure_rev_d",
        state: "current_release",
        spec: "CNC/cut-and-fold aluminium enclosure body for the full five-holder MIDI fuse bank.",
        qty: "1",
        dimension: "340 x 295 mm flat pattern; finished floor 210 x 165 mm with 65 mm folded side walls; input side has one 20 mm fuse 4/bus-bar feed grommet pilot; output side has four 16 mm pilots plus one far-side 28 mm two-cable output pilot.",
        material: "3.0 mm 5052-H32 aluminium",
        sourceBasis: "data/manual/fabrication/midi5_enclosure_rev_d/midi5_enclosure_body_rev_d.dxf; j40_midi5_enclosure_rev_d_dimension_sheet.pdf",
        action: "Cut and fold from the Rev D DXF/PDF in mm, deburr all cable holes, and open pilot holes only to the actual grommet OD after cable sizing.",
      },
      {
        id: "MIDI5-LID-001",
        item: "MIDI 5-way hinged enclosure lid",
        partNumber: "midi5_enclosure_lid_rev_d.dxf",
        route: "midi5_enclosure_rev_d",
        state: "current_release",
        spec: "Flat aluminium lid for the Rev D MIDI enclosure, drilled for input-side hinge and output-side latch/retainer points.",
        qty: "1",
        dimension: "230 x 185 mm lid panel with three hinge holes and two output-side latch holes.",
        material: "2.0-3.0 mm aluminium",
        sourceBasis: "data/manual/fabrication/midi5_enclosure_rev_d/midi5_enclosure_lid_rev_d.dxf; j40_midi5_enclosure_rev_d_dimension_sheet.pdf",
        action: "Fit the hinge on the input/bus side so fuse service does not disturb the five output cables held by the grommets.",
      },
      {
        id: "MIDI5-SUBPLATE-001",
        item: "MIDI 5-way non-conductive holder subplate",
        partNumber: "midi5_holder_subplate_rev_d.dxf",
        route: "midi5_enclosure_rev_d",
        state: "current_release",
        spec: "CNC/router-ready insulated holder board for five linked MIDI holders inside the Rev D aluminium enclosure.",
        qty: "1",
        dimension: "140 x 85 mm board; ten 4.5 mm holder holes on 20.2 mm pitch with 44 mm row separation; six 5.5 mm standoff holes.",
        material: "5.0 mm HDPE, ABS, G10, or phenolic",
        sourceBasis: "data/manual/fabrication/midi5_enclosure_rev_d/midi5_holder_subplate_rev_d.dxf; j40_midi5_enclosure_rev_d_dimension_sheet.pdf",
        action: "Route/print only in non-conductive material; the second-from-last holder is the fuse 4 input/bus feed and the opposite side carries five fused outputs.",
      },
      {
        id: "PWR-CARRIER-001",
        item: "Compact chassis-mounted battery stand / cutoff carrier",
        partNumber: "battery_power_carrier_mount_rev_a",
        route: "battery_power_carrier_mount_rev_a",
        state: "prototype_release_mockup_required",
        image: scoutPreviousPartImage("../../photos/20260317_235232_gp_3Ojs4Rag.jpg", "battery-side engine-bay location", "20260317_235232_gp_3Ojs4Rag", ["battery", "carrier"]),
        spec: "Compact steel chassis-bolted stand that supports the installed Daewoo DLS120 battery and retains the master cutoff/breaker close to it. Relay Rev D and MIDI Rev D remain on two independent local structural accessory brackets under ELEC-RAD-001; neither shares the battery stand.",
        qty: "1",
        dimension: "Compact top tray 340 x 265 mm; installed Daewoo DLS120 battery dimensions from May 17 photos replace the previous 318 x 180 x 230 mm comparison envelope before cutting; formed chassis saddle nominal 220 x 230 mm flat pattern with 70 mm near leg, measured rail-top cap, and 70 mm far leg; upright side plates 110 x 220 mm; adjustable offset bars 360 x 60 mm; estimated tray rise 180 mm above chassis top with 150-210 mm adjustment; estimated tray centre jog 190 mm wing-side/outboard into the edge cavity with 160-230 mm adjustment; side-mounted folded cutoff/kill-switch base/guard 170 x 110 mm finished face / 210 x 150 mm flat pattern / 20 mm upward lips. The former 660 x 310 mm relay/MIDI ladder is superseded and excluded.",
        material: "3.0 mm mild-steel compact tray/rail/tabs; 4.0 mm mild-steel formed chassis saddle, upright bridge, and offset bars.",
        sourceBasis: "data/manual/fabrication/battery_power_carrier_mount_rev_a/README.md; j40_battery_power_carrier_mount_rev_a_dimension_sheet.pdf",
        action: "Mock the compact steel tray/stand with the installed battery and battery-side cutoff/breaker only. Prove chassis attachment, tray offset, battery restraint and lift-out, cutoff access, protected outgoing-feed cable bend, and a service disconnect to ELEC-RAD-001 before cutting final holes.",
        reject: "Do not mount to battery tray skin, radiator support strap, unsupported inner wing, or anywhere live studs can contact carrier/body/bonnet/tools.",
        notes: "Current preferred route for battery support and isolation only. Do not fabricate the former relay/MIDI access ladder; those components now use two independent ELEC-RAD-001 accessory brackets.",
      },
      {
        id: "BPCC-FRONT-RAIL-001",
        item: "Widened front access ladder",
        partNumber: "battery_power_compact_front_service_rail_rev_b.dxf",
        route: "battery_power_carrier_mount_rev_a",
        state: "superseded_hold",
        image: scoutReferenceImage("../../data/manual/fabrication/battery_power_carrier_mount_rev_a/battery_power_compact_front_service_rail_rev_b.svg", "Widened front access ladder Rev B", "battery_power_compact_front_service_rail_rev_b"),
        spec: "Former battery-stand relay/MIDI access ladder, superseded by the 2026-08-01 independent electrical-bracket layout.",
        qty: "1",
        dimension: "HISTORICAL ONLY — DO NOT CUT: the superseded plate was 660 x 310 mm with relay/MIDI and cutoff pickup details. Current manufacture uses the compact battery tray/cutoff carrier plus two separate ELEC-RAD-001 local brackets/hoods.",
        material: "3.0 mm mild steel.",
        sourceBasis: "data/manual/fabrication/battery_power_carrier_mount_rev_a/fabricator_cut_list.csv",
        action: "Do not fabricate or drill from this file unless a documented radiator-carrier dry-fit failure deliberately reopens the fallback.",
      },
      {
        id: "ELEC-RAD-001",
        item: "Independent relay and MIDI electrical brackets",
        partNumber: "two site-fit local brackets with individual hoods",
        route: "front_cooling_stack_rev_a",
        state: "approved_dry_fit_required",
        spec: "One covered Relay Rev D box and one closed, gasketed MIDI Rev D enclosure, each on its own staggered local structural accessory bracket and individual rain hood; neither bracket loads the radiator or shares a transverse plate.",
        qty: "2 independent brackets",
        dimension: "Relay: use the 360 x 245 x 3 mm base and 300 x 197 x 3 mm insulator. MIDI: use the 210 x 165 x 65 mm body, 230 x 185 mm lid and 140 x 85 mm subplate. Final bracket outline follows each real box, its own hood and service sweep; no shared electrical envelope.",
        material: "Two site-fit corrosion-protected local brackets, separate hoods and structural fasteners; retain the existing aluminium relay base and MIDI enclosure.",
        sourceBasis: "docs/J40-integrated-cooling-pack-fabricator-specification-rev-c.md; data/manual/fabrication/front_cooling_stack_rev_c/work_document_assets/rev_g_d09_independent_electrical_mounts.png",
        action: "Template each box separately on non-radiator structure with down/rear cable exits. Prove each hood, lid/cover sweep, cable bend, drip path, P-clips, disconnect, removal, bonnet/grille clearance and no active-fin/sealed-airflow obstruction before drilling. Keep the MIDI lid shut in operation; no formal IP rating is claimed unless purchased-rated or tested.",
        reject: "No common transverse plate; no fixing or load into radiator core, fins, tanks, necks, seams, through-core rods, rubber-isolated radiator mounts or battery stand.",
        notes: "Keep the master cutoff/breaker battery-side. Preserve existing relay assignments and fuse sizing; recalculate cable lengths and repeat continuity, function, and voltage-drop checks after relocation.",
      },
      {
        id: "BPCC-TRAY-001",
        item: "Compact battery stand top tray",
        partNumber: "battery_stand_compact_top_tray_rev_b.dxf",
        route: "battery_power_carrier_mount_rev_a",
        state: "prototype_release",
        image: scoutReferenceImage("../../data/manual/fabrication/battery_power_carrier_mount_rev_a/battery_stand_compact_top_tray_rev_b.svg", "Compact battery stand top tray Rev B", "battery_stand_compact_top_tray_rev_b"),
        spec: "Steel tray/deck carrying the standard battery support field, removable hold-down slots, compact upright bridge mount field, low end stops, lift-out clearance, and P-clip holes.",
        qty: "1",
        dimension: "340 x 265 mm around the installed Daewoo DLS120 battery datum from the May 17 ruler photos; previous 318 x 180 x 230 mm envelope is comparison only.",
        material: "3.0 mm mild steel.",
        sourceBasis: "data/manual/fabrication/battery_power_carrier_mount_rev_a/fabricator_cut_list.csv",
        action: "Use as cardboard template first; final clamp and cable positions follow the installed battery, with the battery removable after the hold-down is removed.",
      },
      {
        id: "BPCC-HOLD-001",
        item: "Compact battery hold-down crossbar",
        partNumber: "battery_stand_compact_hold_down_crossbar_rev_b.dxf",
        route: "battery_power_carrier_mount_rev_a",
        state: "battery_measurement_hold",
        image: scoutReferenceImage("../../data/manual/fabrication/battery_power_carrier_mount_rev_a/battery_stand_compact_hold_down_crossbar_rev_b.svg", "Compact battery hold-down crossbar Rev B", "battery_stand_compact_hold_down_crossbar_rev_b"),
        spec: "Compact service-removable hold-down crossbar template for the battery clamp rods.",
        qty: "1",
        dimension: "340 x 38 mm with slotted ends.",
        material: "3.0 mm mild steel or stainless",
        sourceBasis: "data/manual/fabrication/battery_power_carrier_mount_rev_a/fabricator_cut_list.csv",
        action: "Set final slot spacing from the actual battery case and clamp rod positions; battery must lift out vertically once this crossbar and rods are removed.",
      },
      {
        id: "BPCC-CH-TAB-001",
        item: "Compact battery stand formed chassis saddle",
        partNumber: "battery_stand_compact_single_chassis_pickup_rev_b.dxf",
        route: "battery_power_carrier_mount_rev_a",
        state: "site_fit",
        image: scoutReferenceImage("../../data/manual/fabrication/battery_power_carrier_mount_rev_a/battery_stand_compact_single_chassis_pickup_rev_b.svg", "Compact battery stand formed chassis saddle Rev B", "battery_stand_compact_single_chassis_pickup_rev_b"),
        spec: "Site-fit formed saddle that drops over the chassis rail from the top, with legs down both sides and through-bolts at the one known chassis location.",
        qty: "1",
        dimension: "Nominal 220 x 230 mm flat pattern: 70 mm near leg, measured rail-top cap nominal 90 mm, 70 mm far leg, with top-cap upright/service-rail slots.",
        material: "4.0 mm mild steel",
        sourceBasis: "data/manual/fabrication/battery_power_carrier_mount_rev_a/fabricator_cut_list.csv",
        action: "Measure chassis rail top width, leg depth, through-bolt access, and crush-tube need before final cutting; use the saddle as the single chassis pickup.",
      },
      {
        id: "BPCC-OFFSET-BAR-001",
        item: "Battery stand adjustable body-side offset bar",
        partNumber: "battery_stand_adjustable_offset_bar_rev_b.dxf",
        route: "battery_power_carrier_mount_rev_a",
        state: "site_fit",
        image: scoutReferenceImage("../../data/manual/fabrication/battery_power_carrier_mount_rev_a/battery_stand_adjustable_offset_bar_rev_b.svg", "Battery stand adjustable offset bar Rev B", "battery_stand_adjustable_offset_bar_rev_b"),
        spec: "Slotted bar from the formed chassis saddle/upright bridge toward the body/wing-side battery pocket so the battery stand power carrier offset can be configured.",
        qty: "2 mirrored",
        dimension: "360 x 60 mm, 4.0 mm mild steel, with chassis-saddle end slots and body-side adjustment slots for the 160-230 mm offset range.",
        material: "4.0 mm mild steel",
        sourceBasis: "data/manual/fabrication/battery_power_carrier_mount_rev_a/fabricator_cut_list.csv",
        action: "Start at the 190 mm wing-side/outboard target, trial 160 and 230 mm settings in cardboard/temporary steel, then lock the offset only after battery, relay, MIDI, cutoff, bonnet, steering, hose, and cable-sweep checks pass.",
      },
      {
        id: "BPCC-GUSSET-001",
        item: "Compact battery stand single-mount upright bridge",
        partNumber: "battery_stand_compact_single_mount_upright_rev_b.dxf",
        route: "battery_power_carrier_mount_rev_a",
        state: "trim_to_fit",
        image: scoutReferenceImage("../../data/manual/fabrication/battery_power_carrier_mount_rev_a/battery_stand_compact_single_mount_upright_rev_b.svg", "Compact battery stand single mount upright Rev B", "battery_stand_compact_single_mount_upright_rev_b"),
        spec: "Rectangular upright bridge side plates from the formed chassis saddle to the adjustable body-side offset bars and compact tray/service-rail saddle.",
        qty: "2 mirrored",
        dimension: "110 x 220 mm upright side plate; mock-up target 180 mm chassis-top-to-tray-underside rise with 150-210 mm vertical adjustment and 160-230 mm side-jog tuning around a 190 mm wing-side/outboard tray shift from the more central chassis pickup into the edge cavity.",
        material: "4.0 mm mild steel",
        sourceBasis: "data/manual/fabrication/battery_power_carrier_mount_rev_a/fabricator_cut_list.csv",
        action: "Use as the bridge from the single pickup; this is not a second chassis fixing location.",
      },
      {
        id: "BPCC-CUTOFF-TAB-001",
        item: "Folded master cutoff aluminium base/guard",
        partNumber: "battery_power_compact_cutoff_tab_rev_b.dxf",
        route: "battery_power_carrier_mount_rev_a",
        state: "fit_after_switch_measurement",
        image: scoutReferenceImage("../../data/manual/fabrication/battery_power_carrier_mount_rev_a/battery_power_compact_cutoff_tab_rev_b.svg", "Folded cutoff guard Rev B", "battery_power_compact_cutoff_tab_rev_b"),
        spec: "Compact independent tab/knock guard for the master cutoff switch.",
        qty: "1",
        dimension: "170 x 110 mm with 82 x 46 mm access window.",
        material: "2.0-3.0 mm aluminium or plastic",
        sourceBasis: "data/manual/fabrication/battery_power_carrier_mount_rev_a/fabricator_cut_list.csv",
        action: "Fit only after the actual cutoff switch key/knob sweep and emergency access are proven.",
      },
      {
        id: "RELAY-BASE-001",
        item: "Relay box flat aluminium base",
        partNumber: "relay_base_plate_rev_d.dxf",
        route: "relay_mount_rev_d",
        state: "current_release",
        spec: "Flat aluminium base plate for the existing relay box's large uncovered bottom face, with exposed stand-attachment slots.",
        qty: "1",
        dimension: "360 x 245 mm base plate, 3.0 mm thick, sized to extend beyond the 300 x 197 mm relay-box footprint.",
        material: "3.0 mm 5052-H32 aluminium",
        sourceBasis: "data/manual/fabrication/relay_mount_rev_d/relay_base_plate_rev_d.dxf; j40_relay_mount_rev_d_dimension_sheet.pdf",
        action: "Transfer relay-box fixing holes from the actual enclosure after final orientation. Under controlled cooling release ELEC-RAD-001, mount the covered relay box on its own local structural accessory bracket and individual rain hood; never to the battery stand, radiator, isolated radiator mounts or a shared transverse electrical plate.",
      },
      {
        id: "RELAY-INSULATOR-001",
        item: "Relay exact-footprint insulating sheet",
        partNumber: "relay_insulating_sheet_rev_d.dxf",
        route: "relay_mount_rev_d",
        state: "current_release",
        spec: "Exact-size non-conductive sheet between the already-covered relay box and the flat aluminium base.",
        qty: "1",
        dimension: "300 x 197 mm sheet, 3.0 mm thick, matching the relay-box footprint.",
        material: "3.0 mm ABS, HDPE, polypropylene, G10, or phenolic",
        sourceBasis: "data/manual/fabrication/relay_mount_rev_d/relay_insulating_sheet_rev_d.dxf; j40_relay_mount_rev_d_dimension_sheet.pdf",
        action: "Keep full-size under the relay box, mark through-fixing holes from the actual enclosure, and avoid creating a sealed water trap.",
      },
    ];
    const fabricationElectricalUnderlayRows = [
      {
        id: "ELEC-UNDERLAY-001",
        item: "MIDI holder insulating underlay / subplate",
        route: "midi5_enclosure_rev_d",
        state: "external_plastic_quote",
        partNumber: "midi5_holder_subplate_rev_d.dxf",
        image: scoutPreviousPartImage("../../photos/20260411_143135.jpg", "MIDI holder bank needing non-conductive underlay", "20260411_143135", ["midi5", "underlay"]),
        purpose: "Non-conductive middle board between the five linked MIDI holders and the Rev D aluminium enclosure.",
        definition: "140 x 85 x 5.0 mm board; ten 4.5 mm holder holes on 20.2 mm pitch with 44 mm row separation; six 5.5 mm standoff holes.",
        material: "5.0 mm HDPE, ABS, G10, or phenolic",
        action: "This is the only current external plastic/CNC quote row.",
      },
      {
        id: "ELEC-UNDERLAY-002",
        item: "Relay exact-footprint insulating sheet",
        route: "relay_mount_rev_d",
        state: "current_release",
        partNumber: "relay_insulating_sheet_rev_d.dxf",
        image: scoutPreviousPartImage("../../photos/20260411_143125.jpg", "Relay box needing insulating sheet", "20260411_143125", ["relay-box", "underlay"]),
        purpose: "Non-conductive sheet between the existing relay box's large uncovered bottom face and the Rev D flat aluminium base.",
        definition: "300 x 197 x 3.0 mm sheet matching the relay-box footprint.",
        material: "3.0 mm ABS, HDPE, polypropylene, G10, or phenolic",
        action: "Use as the current relay underlay; transfer fixing holes from the actual relay box after orientation is confirmed.",
      },
    ];
    const fabricationSupportMarketSpec = {
      id: "fabrication_support_market_scout",
      title: "MIDI Holder Plastic Underlay Quote",
      scope: "Plastic underlay only",
      quantity: "1 MIDI holder subplate",
      plain_stall_request:
        "I need a quote for one non-conductive MIDI holder underlay/subplate from the supplied DXF/PDF files in millimeters: 140 x 85 x 5 mm, HDPE/ABS/G10/phenolic.",
      buy_target:
        "Use a CNC router, plastic-sheet workshop, or print service that can quote material, lead time, finish, tolerance, and one-piece price clearly before cutting or printing.",
      must_include: [
        "Material option clearly named: HDPE, ABS, G10, phenolic, or suitable equivalent.",
        "New sheet/print material only; no reused plastic, old rubber, scrap offcut of unknown material, or secondhand insulation.",
        "One-piece price, setup charge if any, and lead time.",
        "Basic tolerance and finish expectation before cutting or printing.",
        "Agreement that this is only the non-conductive underlay; the metal enclosure body/lid are separate aluminium fabrication rows.",
      ],
      bench_test: [
        "Ask the shop to inspect the file and confirm scale before quoting.",
        "Confirm units are millimeters before cutting or printing.",
        "Make only one sample unless the fit is confirmed.",
      ],
      reject_if: [
        "Shop cannot identify material, scale, cut/print orientation, or lead time.",
        "Material is recycled/unknown offcut stock or previously used electrical insulation.",
        "Quote includes metal plate/bracket fabrication under this row.",
        "Price is given without seeing the MIDI holder subplate file or understanding quantity.",
      ],
      capture_before_leaving: [
        "Shop name, phone number, location, material, lead time, and price.",
        "Photo or screenshot of the quoted file name: midi5_holder_subplate_rev_d.",
        "Photo of sample material or sample cut/print quality if available.",
      ],
      price_guidance: {
        rule: "Quote first. Make one underlay only after the file, material, quantity, and first-article need are clear.",
      },
      decision_rule: "This quote row is only for the MIDI holder plastic underlay. Owner-made metal brackets and other electrical underlays are tracked separately.",
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
        id: "j60-hydraulic-steering",
        title: "J60 Hydraulic Steering",
        description: "Source a complete RHD J60/HJ60 box-side set and 2H pump-drive set; inspect/rebuild and physically trial-fit before any chassis fabrication or final hoses.",
        chips: ["RHD complete set", "Trial-fit before fabrication", "Steering before turbo"],
        parts: steeringParts,
        marketSpecs: attachScoutImage(
          dedupeScoutRows(steeringMarketSpecs),
          steeringParts,
          null
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
          brakeBoosterImageRows,
          scoutReferenceImage("../../deliverables/selling_site_images/images/reference_catalog/brake_booster.jpg", "brake booster reference image", "brake_booster")
        ),
      },
      {
        id: "additional-fuse-box",
        title: "Additional Fuse Box",
        description: "Compact OEM-style cabin fuse box with sound terminals and identifiable feeds. Final wiring, cables, terminals, sleeving, and protection are new-only.",
        chips: ["Compact OEM style", "New final wiring", "Three isolated input groups"],
        parts: fuseBoxParts,
        marketSpecs: attachScoutImage(
          [fuseBoxMarketSpec],
          fuseBoxImageRows,
          scoutReferenceImage("../../deliverables/selling_site_images/images/manual_overrides/compact_cabin_fuse_box_user_photo_20260504.png", "user-supplied compact old-OEM fuse box photo", "compact_cabin_fuse_box_user_photo_20260504")
        ),
      },
      {
        id: "workshop-fabrication-support",
        title: "Workshop Support",
        description: "Quote card for the remaining local workshop support item.",
        chips: ["Toolbench", "Workbench", "Mounting-ready top"],
        parts: workshopSupportParts,
        marketSpecs: [
          ...attachScoutImage(
            [toolbenchMarketSpec],
            toolbenchImageRows,
            scoutReferenceImage("../../deliverables/selling_site_images/images/reference_catalog/toolbench.jpg", "Toolbench/workbench reference image", "toolbench")
          ),
        ],
        exactSpecRows: workshopSupportExactRows.filter((row) =>
          cleanString(row && row.sourceBasis).includes("tool_local_toolbench")
        ),
      },
    ];
  }

  function formatScoutBuyLength(value) {
    const text = cleanString(value);
    if (!text) {
      return "";
    }
    if (/^\d+(?:\.\d+)?$/.test(text)) {
      return `${text} mm`;
    }
    if (/^\d+(?:\.\d+)?\s*\/\s*\d+(?:\.\d+)?\s*ft$/i.test(text)) {
      return text.replace(/^(\d+(?:\.\d+)?)/, "$1 mm");
    }
    return text;
  }

  function scoutPipeGroup(row) {
    const id = cleanString((row && (row.order_id || row.id || row.order_line_id)) || "").toUpperCase();
    const lane = cleanString(row && row.shop_lane).toLowerCase();
    const route = cleanString(row && row.route).toLowerCase();
    const text = [
      id,
      lane,
      route,
      row && row.item,
      row && row.order_text,
      row && row.spec,
      row && row.material,
      row && row.sourceBasis,
    ]
      .map((value) => cleanString(value).toLowerCase())
      .join(" ");
    const has = (...tokens) => tokens.every((token) => text.includes(token));
    const hasAny = (...tokens) => tokens.some((token) => text.includes(token));

    if (hasAny("connector hose", "connector/coupler", "coupler hoses") || id.startsWith("HLS-05") || id.startsWith("RPO-COOL-006")) {
      return {
        key: "coolant-connectors",
        label: "Coolant Pipe Connector Hoses",
        note: "Pieces below attach to the formed coolant pipe and must include new clamps/fittings by hose OD.",
      };
    }
    if (hasAny("formed metal coolant", "formed coolant pipe", "radiator pipe assembly") || id === "HLS-12" || id === "RPO-COOL-005") {
      return {
        key: "formed-coolant-pipe",
        label: "Formed Metal Coolant Pipe",
        note: "This pipe needs beaded ends and the separate connector hoses listed immediately below.",
      };
    }
    if (id.includes("COOL") || lane.includes("radiator") || hasAny("radiator", "heater", "coolant overflow")) {
      return {
        key: "coolant-hoses",
        label: "Coolant / Heater Rubber Hoses",
        note: "Pieces below are new molded or cut-to-route coolant/heater hoses with new clamps where required.",
      };
    }
    if (id.includes("FUEL-002") || lane.includes("fuel_hard_line") || has("fuel", "hard line")) {
      return {
        key: "fuel-hard-lines",
        label: "Diesel Fuel Hard Lines",
        note: "Pieces below are new metal tube runs; copy the original unions, bends, clips, and end style.",
      };
    }
    if (id.includes("FUEL") || lane.includes("diesel_fuel") || hasAny("diesel feed", "diesel return", "leak-off", "fuel clamp")) {
      return {
        key: "fuel-rubber-hoses",
        label: "Diesel Rubber Hoses",
        note: "Pieces below are new diesel-rated rubber hoses and fuel clamps, cut to the fitted route.",
      };
    }
    if (id.includes("VAC") || lane.includes("vacuum") || hasAny("vacuum", "breather", "oil mist", "oil outlet")) {
      return {
        key: "vacuum-breather",
        label: "Vacuum / Breather / Oil Hose",
        note: "Pieces below are new reinforced or oil-compatible hoses; the oil outlet hose remains presence-gated.",
      };
    }
    if (id.includes("BRAKE") || lane.includes("brake") || has("brake", "hydraulic")) {
      return {
        key: "brake-hydraulic",
        label: "Brake Hydraulic Lines",
        note: "Pieces below require new crimped flex assemblies, brake-rated tube, and correct fittings.",
      };
    }
    if (id.includes("CLUTCH") || has("clutch", "hydraulic")) {
      return {
        key: "clutch-hydraulic",
        label: "Clutch Hydraulic Lines",
        note: "Pieces below require a new crimped clutch flex assembly and a new brake/clutch-rated hard line if fitted.",
      };
    }
    if (id.includes("CLIP") || lane.includes("support") || hasAny("p-clips", "support clips", "line protection", "edge protection")) {
      return {
        key: "line-support",
        label: "Line Supports / Edge Protection",
        note: "Pieces below attach and protect the new fuel, brake, and clutch hard lines.",
      };
    }
    if (lane.includes("general_rubber") || hasAny("air-cleaner", "intake duct", "couplers")) {
      return {
        key: "air-intake-rubber",
        label: "Air Intake Rubber",
        note: "Pieces below are sample-matched new intake duct or couplers, not coolant/fuel hose.",
      };
    }
    if (lane.includes("ac_hose") || hasAny("a/c barrier", "barrier hose")) {
      return {
        key: "ac-hose",
        label: "A/C Barrier Hose",
        note: "Pieces below stay deferred until compressor, condenser, and evaporator layout is fixed.",
      };
    }
    return {
      key: "other-pipe",
      label: "Other Pipe / Hose Items",
      note: "Pieces below use the listed new-part requirements and sample-match checks.",
    };
  }

  function scoutRubberGroup(row) {
    const id = cleanString((row && (row.id || row.requirement_id || row.order_line_id)) || "").toUpperCase();
    const text = [
      id,
      row && row.item,
      row && row.requirement_name,
      row && row.spec,
      row && row.material,
      row && row.sourceBasis,
    ]
      .map((value) => cleanString(value).toLowerCase())
      .join(" ");
    if (id.includes("FRONT") || text.includes("front-support") || text.includes("front support")) {
      return {
        key: "front-support-rubbers",
        label: "Front-Support Rubbers",
        note: "Pieces below are the oval pads and handed strip rubbers from the removed originals.",
      };
    }
    if (id.includes("BUMP") || text.includes("bump stop")) {
      return {
        key: "rubber-bump-stops",
        label: "Bump Stops",
        note: "Pieces below are vehicle-bracket-controlled mould releases because the old rubber is too decayed to copy.",
      };
    }
    if (id.includes("EXH") || text.includes("exhaust")) {
      return {
        key: "exhaust-rubber",
        label: "Exhaust Rubber Hangers",
        note: "Pieces below use the teardrop exhaust cushion style or a sample-matched new molded copy.",
      };
    }
    if (text.includes("sleeve") || text.includes("cup") || text.includes("seat washer")) {
      return {
        key: "rubber-metal-seats",
        label: "Sleeves / Cup Seats",
        note: "Pieces below are the metal interfaces required by the rubber stack.",
      };
    }
    if (text.includes("shim") || text.includes("bolt") || text.includes("hardware")) {
      return {
        key: "rubber-hardware",
        label: "Shim / Hardware Packs",
        note: "Pieces below are supporting hardware, not rubber substitutes.",
      };
    }
    return {
      key: "body-mount-rubbers",
      label: "Body-Mount Rubber Cushions",
      note: "Pieces below are new body-mount rubber cushions matched to the original samples.",
    };
  }

  function groupScoutRows(rows, mode) {
    const sourceRows = Array.isArray(rows) ? rows : [];
    if (!mode) {
      return [{ key: "all", label: "", note: "", rows: sourceRows }];
    }
    const groupOrder = {
      "coolant-hoses": 10,
      "formed-coolant-pipe": 20,
      "coolant-connectors": 30,
      "fuel-rubber-hoses": 40,
      "fuel-hard-lines": 50,
      "vacuum-breather": 60,
      "brake-hydraulic": 70,
      "clutch-hydraulic": 80,
      "line-support": 90,
      "air-intake-rubber": 100,
      "ac-hose": 110,
      "body-mount-rubbers": 10,
      "rubber-metal-seats": 20,
      "front-support-rubbers": 30,
      "exhaust-rubber": 40,
      "rubber-bump-stops": 50,
      "rubber-hardware": 60,
      "other-pipe": 999,
    };
    const groups = [];
    const byKey = new Map();
    sourceRows.forEach((row) => {
      const group = mode === "rubbers" ? scoutRubberGroup(row) : scoutPipeGroup(row);
      if (!byKey.has(group.key)) {
        byKey.set(group.key, { ...group, rows: [] });
        groups.push(byKey.get(group.key));
      }
      byKey.get(group.key).rows.push(row);
    });
    return groups.sort((left, right) => (groupOrder[left.key] || 500) - (groupOrder[right.key] || 500));
  }

  function renderScoutGroupRow(group, colspan) {
    if (!group || !group.label) {
      return "";
    }
    const ids = group.rows
      .map((row) => cleanString(row.order_id || row.id || row.order_line_id || row.requirement_id))
      .filter(Boolean)
      .join(", ");
    return `
      <tr class="scout-group-row">
        <td colspan="${escapeHtml(colspan)}">
          <strong>${escapeHtml(group.label)}</strong>
          ${ids ? `<span class="small-muted">Pieces underneath: ${escapeHtml(ids)}</span>` : ""}
          ${group.note ? `<div class="small-muted">${escapeHtml(group.note)}</div>` : ""}
        </td>
      </tr>
    `;
  }

  function scoutConnectorOrFittingText(row) {
    const id = cleanString((row && (row.id || row.order_id || row.order_line_id)) || "").toUpperCase();
    const text = [
      id,
      row && row.item,
      row && row.spec,
      row && row.material,
      row && row.notes,
      row && row.action,
    ]
      .map((value) => cleanString(value).toLowerCase())
      .join(" ");
    if (id === "RPO-COOL-005" || id === "HLS-12" || text.includes("formed metal coolant")) {
      return "Needs beaded ends plus connector hoses RPO-COOL-006A/B or HLS-05A/HLS-05B attached.";
    }
    if (id.startsWith("RPO-COOL-006") || id.startsWith("HLS-05") || text.includes("connector hose")) {
      return "Attaches to the formed coolant pipe and mating spigot with new smooth-band or constant-tension clamps.";
    }
    if (id.includes("FUEL-002") || text.includes("fuel hard line")) {
      return "Copy original unions/end style and support with rubber-lined P-clips.";
    }
    if (id.includes("BRAKE-001A") || id === "HLS-17") {
      return "Complete crimped brake flex assemblies only; copy end fittings, brackets, clips, and free length.";
    }
    if (id.includes("BRAKE-001B") || id === "HLS-15") {
      return "Needs new brake-rated fittings after flare/thread/seat identification.";
    }
    if (id.includes("CLUTCH-001A") || id === "HLS-18") {
      return "Complete crimped clutch flex assembly only; copy thread/seat and bracket retention.";
    }
    if (id.includes("CLUTCH-001B") || id === "HLS-19") {
      return "Needs new hydraulic-rated fittings after flare/thread/seat identification.";
    }
    if (id.includes("CLIP") || id === "HLS-16") {
      return "Includes line fasteners, rubber-lined clips, grommets, and edge/pass-through protection.";
    }
    return "";
  }

  function renderScoutField(label, value) {
    const text = cleanString(value);
    if (!text) {
      return "";
    }
    return `<div><strong>${escapeHtml(label)}:</strong> ${escapeHtml(text)}</div>`;
  }

  function fabricationDrawingFileSet(row) {
    const partNumber = cleanString(row && (row.partNumber || row.part_number_or_code));
    const route = cleanString(row && row.route);
    if (!partNumber || !route || !partNumber.toLowerCase().endsWith(".dxf")) {
      return null;
    }
    const svgName = partNumber.replace(/\.dxf$/i, ".svg");
    const basePath = `../../data/manual/fabrication/${route}`;
    return {
      dxfName: partNumber,
      svgName,
      dxfUrl: `${basePath}/${partNumber}`,
      svgUrl: `${basePath}/${svgName}`,
    };
  }

  function fabricationDrawingPreviewImage(row) {
    const files = fabricationDrawingFileSet(row);
    if (!files) {
      return null;
    }
    const subject = cleanString(row && row.item) || cleanString(row && row.id) || files.svgName;
    return scoutReferenceImage(
      files.svgUrl,
      `${subject} drawing`,
      cleanString(row && row.id).toLowerCase().replace(/[^a-z0-9_-]+/g, "_") || files.svgName.replace(/\.[^.]+$/, "")
    );
  }

  function renderScoutFileField(row) {
    const files = fabricationDrawingFileSet(row);
    if (!files) {
      return renderScoutField("File", row && row.partNumber);
    }
    return `
      <div class="scout-file-field">
        <strong>Files:</strong>
        <div class="item-links">
          ${renderItemLink({ url: files.svgUrl, label: "SVG" }, 0)}
          ${renderItemLink({ url: files.dxfUrl, label: "DXF", download: true }, 1)}
        </div>
      </div>
    `;
  }

  function renderLongmanPipeHoseOrderTable(rows) {
    const sourceRows = Array.isArray(rows) ? rows : [];
    if (!sourceRows.length) {
      return "";
    }
    return `
      <article class="card">
        <div class="detail-header">
          <h3>Longman Order Sheet</h3>
          ${chip(`${sourceRows.length} exact lines`)}
        </div>
        <div class="table-wrap">
          <table class="scout-market-order-table">
            <thead>
              <tr>
                <th>Image</th>
                <th>Line</th>
                <th>Pipe / Hose Type</th>
                <th>Exact Order Text</th>
                <th>Qty / Size</th>
                <th>Material / Fittings</th>
                <th>Reject / Install Check</th>
              </tr>
            </thead>
            <tbody>
              ${groupScoutRows(sourceRows, "pipes")
                .map((group) => `
                  ${renderScoutGroupRow(group, 7)}
                  ${group.rows
                    .map(
                      (row) => {
                        const rowImage = bestScoutOriginalImage(row) || scoutComponentImage(row);
                        return `
                          <tr>
                            ${renderInventoryImageCell({ item: row.item, image: rowImage }, row.item || "Order line image")}
                            <td class="scout-line-cell">
                              <strong>${escapeHtml(row.order_id || "-")}</strong>
                              <div class="small-muted">${escapeHtml(row.item || "")}</div>
                              ${statusChip(row.order_state || "open")}
                            </td>
                            <td>${escapeHtml(scoutPipeGroup(row).label || formatToken(row.shop_lane || "-"))}</td>
                            <td class="scout-spec-cell">${escapeHtml(row.order_text || "-")}</td>
                            <td class="scout-meta-cell">
                              ${renderScoutField("Qty", row.qty)}
                              ${renderScoutField("Buy length", formatScoutBuyLength(row.buy_length_mm))}
                              ${renderScoutField("Diameter", row.diameter_spec)}
                            </td>
                            <td class="scout-meta-cell">
                              ${renderScoutField("Material", row.material_spec)}
                              ${renderScoutField("Clamp/fitting", row.clamp_or_fitting_spec || scoutConnectorOrFittingText(row))}
                              ${renderScoutField("Basis", row.source_basis)}
                            </td>
                            <td class="scout-notes-cell">
                              ${renderScoutField("Reject if", row.hard_reject)}
                              ${renderScoutField("Install check", row.final_install_check)}
                            </td>
                          </tr>
                        `;
                      }
                    )
                    .join("")}
                `)
                .join("")}
            </tbody>
          </table>
        </div>
      </article>
    `;
  }

  function renderScoutLocalMarketOrderTable(rows) {
    return renderLongmanPipeHoseOrderTable(rows);
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

  function renderScoutOrderSpecTable(rows, category) {
    const sourceRows = Array.isArray(rows) ? rows : [];
    if (!sourceRows.length) {
      return "";
    }
    const groupMode = category && category.id === "pipes" ? "pipes" : category && category.id === "rubbers" ? "rubbers" : "";
    const groupedRows = groupScoutRows(sourceRows, groupMode);
    return `
      <article class="card">
        <div class="detail-header">
          <h3>Order Table</h3>
          ${chip(`${sourceRows.length} rows`)}
        </div>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Image</th>
                <th>Item</th>
                <th>Qty / Material</th>
                <th>Required Definition</th>
                <th>Files / Checks</th>
              </tr>
            </thead>
            <tbody>
              ${groupedRows
                .map((group) => `
                  ${renderScoutGroupRow(group, 5)}
                  ${group.rows
                    .map(
                      (row) => {
                        const rowImage = fabricationDrawingPreviewImage(row) || bestScoutOriginalImage(row) || scoutComponentImage(row);
                        const connectorText = groupMode === "pipes" ? scoutConnectorOrFittingText(row) : "";
                        return `
                          <tr>
                            ${renderInventoryImageCell({ item: row.item, image: rowImage }, row.item || "Spec row image")}
                            <td>
                              <strong>${escapeHtml(row.item || row.id || "-")}</strong>
                              <div class="small-muted">${escapeHtml(row.id || "")}</div>
                              <div>${statusChip(row.state || "release_hold")}</div>
                            </td>
                            <td class="scout-meta-cell">
                              ${renderScoutField("Qty", row.qty)}
                              ${renderScoutField("Material", row.material)}
                            </td>
                            <td class="scout-spec-cell">
                              ${escapeHtml(row.spec || "-")}
                              ${renderScoutField("Dimensions", row.dimension)}
                              ${renderScoutField("Connectors/fittings", connectorText)}
                            </td>
                            <td class="scout-notes-cell">
                              ${renderScoutFileField(row)}
                              ${renderScoutField("Route", row.route ? formatToken(row.route) : "")}
                              ${renderScoutField("Source", row.sourceBasis)}
                              ${renderScoutField("Check", row.action)}
                              ${renderScoutField("Reject if", row.reject)}
                              ${renderScoutField("Notes", row.notes)}
                            </td>
                          </tr>
                        `;
                      }
                    )
                    .join("")}
                `)
                .join("")}
            </tbody>
          </table>
        </div>
      </article>
    `;
  }

  function renderFabricationUnderlayTable(rows) {
    const sourceRows = Array.isArray(rows) ? rows : [];
    if (!sourceRows.length) {
      return "";
    }
    return `
      <article class="card">
        <div class="detail-header">
          <h3>Electrical Underlays</h3>
          ${chip(`${sourceRows.length} requirements`)}
        </div>
        <p class="small-muted">Non-metal underlays, guards, and insulators that let the electrical components mount safely. Metal support plates and brackets stay owner-made unless explicitly re-routed.</p>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Image</th>
                <th>Requirement</th>
                <th>Use</th>
                <th>Required Definition</th>
                <th>File / Action</th>
              </tr>
            </thead>
            <tbody>
              ${sourceRows
                .map(
                  (row) => `
                    <tr>
                      ${renderInventoryImageCell({ item: row.item, image: fabricationDrawingPreviewImage(row) || row.image || scoutComponentImage(row) }, row.item || "Underlay image")}
                      <td>
                        <strong>${escapeHtml(row.item || row.id || "-")}</strong>
                        <div class="small-muted">${escapeHtml(row.id || "")}</div>
                        <div>${statusChip(row.state || "tracked_requirement")}</div>
                      </td>
                      <td>${escapeHtml(row.purpose || "")}</td>
                      <td class="scout-spec-cell">
                        ${escapeHtml(row.definition || "-")}
                        ${renderScoutField("Material", row.material)}
                      </td>
                      <td class="scout-notes-cell">
                        ${renderScoutFileField(row)}
                        ${renderScoutField("Route", row.route ? formatToken(row.route) : "")}
                        ${renderScoutField("Action", row.action)}
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
        ${renderScoutOrderSpecTable(category.exactSpecRows, category)}
        ${renderFabricationUnderlayTable(category.underlayRows)}
        ${renderFabricationPackages(category.fabricationPackages)}
      </section>
    `;
  }

  function renderScout() {
    const categories = buildScoutCategories();
    root.innerHTML = `
      <h2 class="section-title">Scout</h2>
      <p class="section-subtitle">Simple market-facing cards for the remaining Scout-only shop visits: what to ask for, what must come with it, when to reject, and what photos or details to send back. Hoses/pipes and chassis rubbers now live in their dedicated workstreams and Longman order sheets.</p>
      <div class="chip-row scout-jump-row">
        ${categories.map((category) => `<button class="chip chip-button" data-scroll-reference-section="scout-${escapeHtml(category.id)}" type="button">${escapeHtml(category.title)}</button>`).join("")}
      </div>
      ${categories.map(renderScoutCategory).join("")}
    `;
  }

  function renderElectricalEvidenceCell(row, column) {
    const images = filterVisibleImages((row && row[column.key]) || []);
    if (!images.length) {
      return `<span class="small-muted">${escapeHtml(cleanString(row && row.photo_refs) ? "photo not found" : "photo needed")}</span>`;
    }
    const sequenceId = createImageSequence();
    const fallbackCaption =
      cleanString(row && row.input_name) || cleanString(row && row.hole_id) || cleanString(row && row.visible_area) || "Electrical refit evidence";
    return `
      <div class="requirement-evidence-grid">
        ${images
          .map((image) => {
            const prepared = prepareImage(image, fallbackCaption, { sequenceId });
            return `
              <div class="requirement-evidence-item">
                ${renderPreparedMedia(prepared, "table-image-btn", "table-image")}
                <span class="table-image-note">${escapeHtml(prepared.effective.media_id || "")}</span>
              </div>
            `;
          })
          .join("")}
      </div>
    `;
  }

  function renderElectricalCell(row, column) {
    const value = cleanString(row && row[column.key]);
    if (column.kind === "images") {
      return renderElectricalEvidenceCell(row, column);
    }
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
    const engineInputRows = Array.isArray(spec.engine_input_reconciliation) ? spec.engine_input_reconciliation : [];
    const firewallPassThroughRows = Array.isArray(spec.firewall_pass_through_survey) ? spec.firewall_pass_through_survey : [];
    const diagramRows = Array.isArray(spec.diagram_reconciliation) ? spec.diagram_reconciliation : [];

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
        "Engine + Sender Input Reconciliation",
        [
          { key: "evidence_images", label: "Image", kind: "images" },
          { key: "input_id", label: "ID", kind: "token" },
          { key: "input_name", label: "Input / Location" },
          { key: "identified_function_or_status", label: "Purpose / Status" },
          { key: "next_connected_to", label: "Attach / Terminate To" },
          { key: "confidence", label: "Confidence", kind: "token" },
          { key: "verification_before_connection", label: "How To Prove" },
          { key: "refit_action", label: "Refit Action" },
        ],
        engineInputRows
      )}

      ${renderElectricalTable(
        "Firewall Pass-Through Attachment Plan",
        [
          { key: "evidence_images", label: "Image", kind: "images" },
          { key: "hole_id", label: "ID", kind: "token" },
          { key: "visible_area", label: "Location" },
          { key: "what_it_does", label: "What It Does" },
          { key: "attach_or_route_to", label: "Attach / Route To" },
          { key: "refit_decision", label: "Refit Decision" },
          { key: "verification_required", label: "How To Prove" },
        ],
        firewallPassThroughRows
      )}

      ${renderElectricalTable(
        "Diagram Reconciliation",
        [
          { key: "reconciliation_id", label: "ID", kind: "token" },
          { key: "diagram_scope", label: "Diagram Scope" },
          { key: "reconciliation_status", label: "Status", kind: "status" },
          { key: "workstream_alignment", label: "Workstream Alignment" },
          { key: "action_required", label: "Action Required" },
        ],
        diagramRows
      )}

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

  function renderStatusText(value, maxLength = 150) {
    const text = cleanString(value);
    if (!text) {
      return '<span class="small-muted">-</span>';
    }
    if (text.length <= maxLength) {
      return escapeHtml(text);
    }
    return `
      <div class="status-long-text">${escapeHtml(truncateText(text, maxLength))}</div>
      <details class="status-detail">
        <summary>Full detail</summary>
        <p>${escapeHtml(text)}</p>
      </details>
    `;
  }

  function renderStatusMetric(label, value, detail = "") {
    return `
      <article class="card">
        <p class="metric-value">${escapeHtml(value ?? 0)}</p>
        <p class="metric-label">${escapeHtml(label)}</p>
        ${detail ? `<p class="small-muted">${escapeHtml(detail)}</p>` : ""}
      </article>
    `;
  }

  function renderStatusCountChips(rows) {
    const sourceRows = Array.isArray(rows) ? rows : [];
    if (!sourceRows.length) {
      return '<span class="small-muted">No counts recorded.</span>';
    }
    return sourceRows
      .map((row) => chip(`${formatToken(row.label || "unknown")}: ${row.count ?? 0}`))
      .join("");
  }

  function renderStatusSourceFiles(files) {
    const entries = Object.entries(files || {});
    if (!entries.length) {
      return "";
    }
    return `
      <section class="card status-source-card">
        <div class="detail-header">
          <h3>Source Files</h3>
          ${chip(`${entries.length} files`)}
        </div>
        <div class="status-source-list">
          ${entries
            .map(
              ([key, value]) => `
                <div class="status-source-row">
                  <strong>${escapeHtml(formatToken(key))}</strong>
                  <code>${escapeHtml(value)}</code>
                </div>
              `
            )
            .join("")}
        </div>
      </section>
    `;
  }

  function renderStatusUpdateSnapshot() {
    const update = data.status_update || {};
    const gmailRows = (((update.gmail || {}).rows) || []).length;
    const whatsappNewRows = ((((update.whatsapp || {}).new_rows) || [])).length;
    const manualRows = (update.manual_updates || []).length;
    if (!update.date_tag && !gmailRows && !whatsappNewRows && !manualRows) {
      return "";
    }
    return `
      <section class="card status-update-snapshot">
        <div class="detail-header">
          <h3>Latest Comms Status Update</h3>
          ${chip(update.date_tag || "latest")}
        </div>
        <div class="chip-row">
          ${chip(`Gmail rows: ${gmailRows}`)}
          ${chip(`New WhatsApp rows: ${whatsappNewRows}`)}
          ${chip(`Manual tracker rows: ${manualRows}`)}
        </div>
        <p class="small-muted">Gmail, WhatsApp, manual tracker updates, and the order/receipt delivery watchlist are available in the dedicated update view.</p>
        <a class="item-link" href="#status-update">Open Status Update</a>
      </section>
    `;
  }

  function renderStatusManualRows(rows) {
    const sourceRows = Array.isArray(rows) ? rows : [];
    return `
      <section class="card status-update-table-card">
        <div class="detail-header">
          <h3>Manual Tracker Updates</h3>
          ${chip(`${sourceRows.length} rows`)}
        </div>
        <div class="table-wrap">
          <table class="status-update-table">
            <thead>
              <tr>
                <th>Tracker</th>
                <th>Row / Item</th>
                <th>State</th>
                <th>Commercials</th>
                <th>Evidence</th>
                <th>Notes / Next Action</th>
              </tr>
            </thead>
            <tbody>
              ${sourceRows.length
                ? sourceRows
                    .map(
                      (row) => `
                        <tr>
                          <td>
                            <strong>${escapeHtml(formatToken(row.table || "tracker"))}</strong>
                            <div class="small-muted">${escapeHtml(formatToken(row.workstream || row.phase || "unassigned"))}</div>
                          </td>
                          <td>
                            <code>${escapeHtml(row.row_id || "")}</code>
                            <div>${renderStatusText(row.item || "", 120)}</div>
                          </td>
                          <td>
                            ${statusChip(row.status || row.procurement_stage || "tracked")}
                            ${row.procurement_stage ? `<div class="small-muted">Stage: ${escapeHtml(formatToken(row.procurement_stage))}</div>` : ""}
                            ${row.delivery_status ? `<div class="small-muted">Delivery: ${escapeHtml(formatToken(row.delivery_status))}</div>` : ""}
                            ${row.payment_status ? `<div class="small-muted">Payment: ${escapeHtml(formatToken(row.payment_status))}</div>` : ""}
                          </td>
                          <td>
                            ${row.company ? `<strong>${escapeHtml(row.company)}</strong>` : "-"}
                            ${row.transaction_number ? `<div class="small-muted">Txn: ${escapeHtml(row.transaction_number)}</div>` : ""}
                            ${row.amount ? `<div class="small-muted">${escapeHtml(row.currency || "PKR")} ${escapeHtml(row.amount)}</div>` : ""}
                            ${row.expected_delivery_date ? `<div class="small-muted">ETA: ${escapeHtml(row.expected_delivery_date)}</div>` : ""}
                          </td>
                          <td>${renderStatusText(row.evidence_ref || row.product_link || "", 130)}</td>
                          <td>${renderStatusText(row.next_action || row.notes || "", 180)}</td>
                        </tr>
                      `
                    )
                    .join("")
                : '<tr><td colspan="6">No manual tracker rows matched this status update.</td></tr>'}
            </tbody>
          </table>
        </div>
      </section>
    `;
  }

  function renderStatusGmailRows(rows) {
    const sourceRows = Array.isArray(rows) ? rows : [];
    return `
      <section class="card status-update-table-card">
        <div class="detail-header">
          <h3>Gmail Evidence</h3>
          ${chip(`${sourceRows.length} categorized rows`)}
        </div>
        <div class="table-wrap">
          <table class="status-update-table">
            <thead>
              <tr>
                <th>Date</th>
                <th>Source</th>
                <th>Category</th>
                <th>Subject / Topic</th>
                <th>Refs / Amount</th>
                <th>Action</th>
                <th>Notes</th>
              </tr>
            </thead>
            <tbody>
              ${sourceRows.length
                ? sourceRows
                    .map(
                      (row) => `
                        <tr>
                          <td>
                            ${escapeHtml(formatDateTime(row.date_utc || ""))}
                            <div class="small-muted"><code>${escapeHtml(row.message_id || "")}</code></div>
                          </td>
                          <td>${escapeHtml(row.source || row.channel || "-")}</td>
                          <td>
                            ${statusChip(row.category || "categorized")}
                            ${row.subcategory ? `<div class="small-muted">${escapeHtml(formatToken(row.subcategory))}</div>` : ""}
                          </td>
                          <td>
                            <strong>${renderStatusText(row.subject_or_ref || "", 110)}</strong>
                            ${row.product_or_topic ? `<div>${renderStatusText(row.product_or_topic, 170)}</div>` : ""}
                          </td>
                          <td>
                            ${row.part_number_or_code ? renderStatusText(row.part_number_or_code, 120) : "-"}
                            ${row.amount_pkr ? `<div class="small-muted">PKR ${escapeHtml(row.amount_pkr)}</div>` : ""}
                          </td>
                          <td>
                            ${statusChip(row.status || "signal")}
                            <div class="small-muted">Required: ${escapeHtml(formatToken(row.action_required || "unknown"))}</div>
                          </td>
                          <td>${renderStatusText(row.notes || "", 150)}</td>
                        </tr>
                      `
                    )
                    .join("")
                : '<tr><td colspan="7">No Gmail rows were loaded for the latest status update.</td></tr>'}
            </tbody>
          </table>
        </div>
      </section>
    `;
  }

  function renderStatusWhatsappRows(rows) {
    const sourceRows = Array.isArray(rows) ? rows : [];
    return `
      <section class="card status-update-table-card">
        <div class="detail-header">
          <h3>WhatsApp Project Extract</h3>
          ${chip(`${sourceRows.length} rows`)}
        </div>
        <div class="table-wrap">
          <table class="status-update-table">
            <thead>
              <tr>
                <th>Time</th>
                <th>Chat</th>
                <th>Category</th>
                <th>Message</th>
                <th>Matched Terms</th>
              </tr>
            </thead>
            <tbody>
              ${sourceRows.length
                ? sourceRows
                    .map(
                      (row) => `
                        <tr class="${cleanString(row.is_new).toLowerCase() === "true" ? "is-new-status-row" : ""}">
                          <td>
                            ${escapeHtml(formatDateTime(row.timestamp || ""))}
                            <div class="small-muted"><code>${escapeHtml(row.message_id || "")}</code></div>
                            ${cleanString(row.is_new).toLowerCase() === "true" ? chip("new") : ""}
                          </td>
                          <td>
                            <strong>${escapeHtml(row.chat_name || "-")}</strong>
                            <div class="small-muted">${escapeHtml(row.source_profile || "")}</div>
                            ${row.author ? `<div class="small-muted">By: ${escapeHtml(row.author)}</div>` : ""}
                          </td>
                          <td>
                            ${statusChip(row.category || "project")}
                            ${row.subcategory ? `<div class="small-muted">${escapeHtml(formatToken(row.subcategory))}</div>` : ""}
                          </td>
                          <td>${renderStatusText(row.text || "", 220)}</td>
                          <td>${renderStatusText(row.matched_terms || "", 120)}</td>
                        </tr>
                      `
                    )
                    .join("")
                : '<tr><td colspan="5">No WhatsApp project rows were loaded for the latest status update.</td></tr>'}
            </tbody>
          </table>
        </div>
      </section>
    `;
  }

  function renderStatusDeliveryWatchlist(rows) {
    const sourceRows = Array.isArray(rows) ? rows : [];
    return `
      <section class="card status-update-table-card">
        <div class="detail-header">
          <h3>Ordering / Receipt Watchlist</h3>
          ${chip(`${sourceRows.length} rows`)}
        </div>
        <div class="table-wrap">
          <table class="status-update-table">
            <thead>
              <tr>
                <th>Priority</th>
                <th>Item</th>
                <th>Supplier / Txn</th>
                <th>State</th>
                <th>Evidence</th>
                <th>Search Queries</th>
              </tr>
            </thead>
            <tbody>
              ${sourceRows.length
                ? sourceRows
                    .map(
                      (row) => `
                        <tr class="${row.recent_evidence_match ? "is-new-status-row" : ""}">
                          <td>
                            ${statusChip(row.audit_priority || "audit")}
                            ${row.recent_evidence_match ? `<div class="small-muted">latest evidence</div>` : ""}
                          </td>
                          <td>
                            <code>${escapeHtml(row.entry_id || "")}</code>
                            <div><strong>${renderStatusText(row.item || "", 135)}</strong></div>
                            <div class="small-muted">${escapeHtml(formatToken(row.workstream || row.phase || "unassigned"))}</div>
                          </td>
                          <td>
                            ${row.company ? `<strong>${escapeHtml(row.company)}</strong>` : "-"}
                            ${row.transaction_number ? `<div class="small-muted">Txn: ${escapeHtml(row.transaction_number)}</div>` : ""}
                            ${row.amount_display ? `<div class="small-muted">${escapeHtml(row.amount_display)}</div>` : ""}
                            ${row.expected_delivery_date ? `<div class="small-muted">ETA: ${escapeHtml(row.expected_delivery_date)}</div>` : ""}
                          </td>
                          <td>
                            ${statusChip(row.status || row.procurement_stage || "tracked")}
                            ${row.procurement_stage ? `<div class="small-muted">Stage: ${escapeHtml(formatToken(row.procurement_stage))}</div>` : ""}
                            ${row.delivery_status ? `<div class="small-muted">Delivery: ${escapeHtml(formatToken(row.delivery_status))}</div>` : ""}
                            ${row.audit_status ? `<div class="small-muted">Audit: ${escapeHtml(formatToken(row.audit_status))}</div>` : ""}
                          </td>
                          <td>${renderStatusText(row.evidence_ref || row.product_link || "", 140)}</td>
                          <td>
                            ${renderStatusText([row.order_search_query, row.receipt_search_query].filter(Boolean).join(" | "), 170)}
                          </td>
                        </tr>
                      `
                    )
                    .join("")
                : '<tr><td colspan="6">No ordering or receipt watchlist rows were loaded.</td></tr>'}
            </tbody>
          </table>
        </div>
      </section>
    `;
  }

  function renderStatusUpdate() {
    const update = data.status_update || {};
    const gmail = update.gmail || {};
    const gmailSummary = gmail.summary || {};
    const whatsapp = update.whatsapp || {};
    const whatsappImportSummary = whatsapp.import_summary || {};
    const whatsappProjectSummary = whatsapp.project_summary || {};
    const whatsappTotals = whatsappImportSummary.totals || {};
    const whatsappMessages = (whatsappProjectSummary.messages || {});
    const gmailRows = Array.isArray(gmail.rows) ? gmail.rows : [];
    const whatsappRows = Array.isArray(whatsapp.rows) ? whatsapp.rows : [];
    const whatsappNewRows = Array.isArray(whatsapp.new_rows) ? whatsapp.new_rows : [];
    const manualRows = Array.isArray(update.manual_updates) ? update.manual_updates : [];
    const watchlistRows = Array.isArray(update.delivery_watchlist) ? update.delivery_watchlist : [];

    root.innerHTML = `
      <section class="status-update-view">
        <div class="status-update-head">
          <div>
            <h2 class="section-title">Latest Comms Status Update</h2>
            <p class="section-subtitle">Detailed Gmail import, WhatsApp project extract, manual tracker changes, and order/receipt audit state for ${escapeHtml(update.date_tag || "the latest run")}.</p>
          </div>
          <div class="chip-row">
            ${chip(update.date_tag || "latest")}
            ${chip(`${Object.keys(update.source_files || {}).length} source files`)}
          </div>
        </div>

        <section class="metrics-grid">
          ${renderStatusMetric("Gmail Read", gmailSummary.unique_messages_read ?? gmailRows.length, `${gmailSummary.excluded_non_project_records ?? 0} excluded`)}
          ${renderStatusMetric("Gmail Categorized", gmailSummary.categorized_records_written ?? gmailRows.length, `${gmailSummary.queries_run ?? 0} queries`)}
          ${renderStatusMetric("WhatsApp Project Rows", whatsappMessages.project_rows_total ?? whatsappRows.length, `${whatsappTotals.messages_imported ?? 0} imported messages`)}
          ${renderStatusMetric("New WhatsApp Rows", whatsappMessages.project_rows_new_since_rerun ?? whatsappNewRows.length, `${whatsappTotals.media_imported ?? 0} media items`)}
          ${renderStatusMetric("Manual Tracker Rows", manualRows.length, "Expenses, procurement, workstreams")}
          ${renderStatusMetric("Delivery Watchlist", watchlistRows.length, "Orders and receipt checks")}
        </section>

        ${renderStatusSourceFiles(update.source_files || {})}

        <section class="cards-grid status-update-summary-grid">
          <article class="card">
            <div class="detail-header">
              <h3>Gmail Summary</h3>
              ${chip(`${gmailRows.length} rows`)}
            </div>
            <p class="small-muted">Query after: ${escapeHtml(gmailSummary.new_messages_query_after || "unknown")}</p>
            <div class="chip-row">${renderStatusCountChips(gmail.category_counts)}</div>
            <div class="chip-row">${renderStatusCountChips(gmail.top_sources)}</div>
          </article>
          <article class="card">
            <div class="detail-header">
              <h3>WhatsApp Summary</h3>
              ${chip(`${whatsappRows.length} project rows`)}
            </div>
            <p class="small-muted">Selected chats: ${escapeHtml(whatsappTotals.selected_chats ?? 0)}. Messages imported: ${escapeHtml(whatsappTotals.messages_imported ?? 0)}. Media imported: ${escapeHtml(whatsappTotals.media_imported ?? 0)}.</p>
            <div class="chip-row">${renderStatusCountChips(Object.entries((whatsappMessages.categories || {})).map(([label, count]) => ({ label, count })))}</div>
          </article>
        </section>

        ${renderStatusManualRows(manualRows)}
        ${renderStatusGmailRows(gmailRows)}
        ${renderStatusWhatsappRows(whatsappRows)}
        ${renderStatusDeliveryWatchlist(watchlistRows)}
      </section>
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

  function overviewWorkstreamContext() {
    const workstreams = Array.isArray(data.workstreams) ? data.workstreams : [];
    return {
      workstreams,
      byId: new Map(workstreams.map((workstream) => [cleanString(workstream.id), workstream])),
    };
  }

  function overviewWorkstreamId(value) {
    return cleanString(value) || "unassigned";
  }

  function overviewWorkstreamLabel(workstreamId, context) {
    if (workstreamId === "unassigned") {
      return "Unassigned";
    }
    const workstream = context.byId.get(workstreamId);
    return cleanString(workstream && workstream.title) || formatToken(workstreamId);
  }

  function groupOverviewRowsByWorkstream(rows) {
    return (Array.isArray(rows) ? rows : []).reduce((groups, row) => {
      const workstreamId = overviewWorkstreamId(row && row.workstream);
      if (!groups[workstreamId]) {
        groups[workstreamId] = [];
      }
      groups[workstreamId].push(row);
      return groups;
    }, {});
  }

  function sortedOverviewWorkstreamIds(context, ...groupMaps) {
    const ids = [];
    const seen = new Set();
    const addId = (id) => {
      const normalized = overviewWorkstreamId(id);
      if (!seen.has(normalized)) {
        seen.add(normalized);
        ids.push(normalized);
      }
    };
    context.workstreams.forEach((workstream) => addId(workstream.id));
    const extraIds = new Set();
    groupMaps.forEach((groups) => {
      Object.keys(groups || {}).forEach((id) => {
        if (!seen.has(id)) {
          extraIds.add(id);
        }
      });
    });
    [...extraIds]
      .sort((left, right) => {
        if (left === "unassigned") return 1;
        if (right === "unassigned") return -1;
        return overviewWorkstreamLabel(left, context).localeCompare(overviewWorkstreamLabel(right, context));
      })
      .forEach(addId);
    return ids;
  }

  function overviewTaskPriorityRank(task) {
    const priority = cleanString(task && task.priority).toUpperCase();
    const match = priority.match(/^P(\d+)/);
    return match ? Number(match[1]) : 9;
  }

  function overviewTaskTimingRank(task) {
    return cleanString(task && task.timing).toLowerCase() === "later" ? 1 : 0;
  }

  function compareOverviewTasks(left, right) {
    return (
      overviewTaskTimingRank(left) - overviewTaskTimingRank(right) ||
      overviewTaskPriorityRank(left) - overviewTaskPriorityRank(right) ||
      cleanString(left && left.title).localeCompare(cleanString(right && right.title))
    );
  }

  function renderOverviewTaskRows(tasks, options = {}) {
    const showEvidence = Boolean(options.showEvidence);
    return tasks
      .slice()
      .sort(compareOverviewTasks)
      .map(
        (task) => `
          <tr>
            ${showEvidence ? `<td class="requirement-evidence-cell">${renderCaptureTaskEvidence(task)}</td>` : ""}
            <td>${priorityChip(task.priority)}</td>
            <td>${escapeHtml(formatToken(task.timing || "now"))}</td>
            <td>
              <strong>${escapeHtml(task.title || task.task_id || "Task")}</strong>
              ${task.location ? `<div class="small-muted">${escapeHtml(task.location)}</div>` : ""}
              ${task.notes ? `<div class="small-muted">${escapeHtml(truncateText(task.notes, 140))}</div>` : ""}
            </td>
            <td>${statusChip(task.status || "open")}</td>
            <td>${escapeHtml(formatToken(task.task_type || "data"))}</td>
            <td>
              ${escapeHtml(task.action || "-")}
              ${task.data_needed ? `<div class="small-muted">${escapeHtml(truncateText(task.data_needed, 180))}</div>` : ""}
            </td>
            <td>
              <div class="small-muted">${escapeHtml(task.source_row_id || "")}</div>
              ${renderLinksCell(task)}
            </td>
          </tr>
        `
      )
      .join("");
  }

  function renderTasksByWorkstreamSection(tasks, options = {}) {
    const sourceTasks = Array.isArray(tasks) ? tasks : [];
    const context = overviewWorkstreamContext();
    const groupedTasks = groupOverviewRowsByWorkstream(sourceTasks);
    const workstreamIds = sortedOverviewWorkstreamIds(context, groupedTasks).filter(
      (workstreamId) => groupedTasks[workstreamId] && groupedTasks[workstreamId].length
    );
    const showEvidence = Boolean(options.showEvidence);
    const emptyText = options.emptyText || "No tasks found.";
    const columnCount = showEvidence ? 8 : 7;

    if (!sourceTasks.length) {
      return `<section class="card"><p class="small-muted">${escapeHtml(emptyText)}</p></section>`;
    }

    return `
      <section class="task-workstream-list">
        ${workstreamIds
          .map((workstreamId) => {
            const rows = groupedTasks[workstreamId] || [];
            const workstream = context.byId.get(workstreamId);
            return `
              <article class="card task-workstream-card">
                <div class="detail-header">
                  <h3>${escapeHtml(overviewWorkstreamLabel(workstreamId, context))}</h3>
                  <div class="overview-card-actions">
                    ${workstream ? statusChip(workstream.status) : statusChip("unassigned")}
                    ${chip(`${rows.length} tasks`)}
                    ${workstream ? `<button class="overview-open-btn" data-open-workstream-id="${escapeHtml(workstreamId)}" type="button">Open</button>` : ""}
                  </div>
                </div>
                <div class="table-wrap">
                  <table class="capture-task-table compact">
                    <thead>
                      <tr>
                        ${showEvidence ? "<th>Evidence</th>" : ""}
                        <th>Priority</th>
                        <th>Timing</th>
                        <th>Task</th>
                        <th>Status</th>
                        <th>Type</th>
                        <th>Action / Data Needed</th>
                        <th>Source</th>
                      </tr>
                    </thead>
                    <tbody>
                      ${
                        rows.length
                          ? renderOverviewTaskRows(rows, { showEvidence })
                          : `<tr><td colspan="${columnCount}">${escapeHtml(emptyText)}</td></tr>`
                      }
                    </tbody>
                  </table>
                </div>
              </article>
            `;
          })
          .join("")}
      </section>
    `;
  }

  function overviewRequiredOrders() {
    const supplies = data.supplies || {};
    const allSupplyRows = Array.isArray(supplies.all_rows) ? supplies.all_rows : [];
    return allSupplyRows
      .filter((row) => cleanString(row && row.status_group).toLowerCase() === "still_required")
      .sort(
        (left, right) =>
          overviewWorkstreamId(left && left.workstream).localeCompare(overviewWorkstreamId(right && right.workstream)) ||
          cleanString(left && left.supply_type).localeCompare(cleanString(right && right.supply_type)) ||
          cleanString(left && left.item).localeCompare(cleanString(right && right.item))
      );
  }

  function renderRequiredOrdersAcrossAll(requiredOrders, context) {
    const groupedOrders = groupOverviewRowsByWorkstream(requiredOrders);
    const workstreamIds = sortedOverviewWorkstreamIds(context, groupedOrders).filter(
      (workstreamId) => groupedOrders[workstreamId] && groupedOrders[workstreamId].length
    );
    const countChips = workstreamIds
      .map((workstreamId) => chip(`${overviewWorkstreamLabel(workstreamId, context)}: ${(groupedOrders[workstreamId] || []).length}`))
      .join("");

    return `
      <h2 class="section-title">Required Orders Across All Workstreams</h2>
      <section class="card">
        <div class="detail-header">
          <h3>Still Required / Need To Order</h3>
          ${chip(`${requiredOrders.length} rows`)}
        </div>
        <div class="chip-row overview-count-row">
          ${countChips || chip("No required orders")}
        </div>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Workstream</th>
                <th>Type</th>
                <th>Item</th>
                <th>Stage / Status</th>
                <th>Supplier</th>
                <th>Cost</th>
                <th>Links</th>
              </tr>
            </thead>
            <tbody>
              ${
                requiredOrders.length
                  ? requiredOrders
                      .map(
                        (row) => `
                          <tr>
                            <td>${escapeHtml(overviewWorkstreamLabel(overviewWorkstreamId(row.workstream), context))}</td>
                            <td>${escapeHtml(formatToken(row.supply_type || "-"))}</td>
                            <td>${renderItemButton(row)}</td>
                            <td>
                              ${statusChip(row.procurement_stage || row.status_detail || row.status_group || "still_required")}
                              ${row.status_detail ? `<div class="small-muted">${escapeHtml(formatToken(row.status_detail))}</div>` : ""}
                            </td>
                            <td>${tableSupplierCell(row)}</td>
                            <td>${tableCostCell(row)}</td>
                            <td>${renderLinksCell(row)}</td>
                          </tr>
                        `
                      )
                      .join("")
                  : '<tr><td colspan="7">No still-required order rows found.</td></tr>'
              }
            </tbody>
          </table>
        </div>
      </section>
    `;
  }

  function renderOverview() {
    const summary = data.summary || {};
    const parts = data.parts || {};
    const captureTasks = data.capture_tasks || {};
    const allTasks = Array.isArray(captureTasks.tasks) ? captureTasks.tasks : [];
    const currentTasks = allTasks.filter((task) => cleanString(task.timing).toLowerCase() !== "later");
    const context = overviewWorkstreamContext();
    const requiredOrders = overviewRequiredOrders();
    const groupedOrders = groupOverviewRowsByWorkstream(requiredOrders);
    const groupedTasks = groupOverviewRowsByWorkstream(currentTasks);
    const workstreamIds = sortedOverviewWorkstreamIds(context, groupedOrders, groupedTasks);

    root.innerHTML = `
      <section class="metrics-grid">
        <article class="card">
          <p class="metric-value">${escapeHtml(summary.workstreams_in_scope ?? context.workstreams.length)}</p>
          <p class="metric-label">Workstreams</p>
        </article>
        <article class="card">
          <p class="metric-value">${escapeHtml(summary.workstreams_active ?? 0)}</p>
          <p class="metric-label">Active Workstreams</p>
        </article>
        <article class="card">
          <p class="metric-value">${escapeHtml(requiredOrders.length)}</p>
          <p class="metric-label">Required Orders</p>
        </article>
        <article class="card">
          <p class="metric-value">${escapeHtml(summary.parts_ordered_pending_delivery ?? (parts.ordered_pending_delivery || []).length)}</p>
          <p class="metric-label">Orders Awaiting Delivery</p>
        </article>
        <article class="card">
          <p class="metric-value">${escapeHtml(currentTasks.length)}</p>
          <p class="metric-label">Current Tasks</p>
        </article>
        <article class="card">
          <p class="metric-value">${escapeHtml((allTasks.length || 0) - currentTasks.length)}</p>
          <p class="metric-label">Later / Deferred Tasks</p>
        </article>
      </section>

      ${renderStatusUpdateSnapshot()}

      <h2 class="section-title">Workstreams and Status</h2>
      <section class="card overview-status-card">
        <div class="table-wrap">
          <table class="overview-status-table">
            <thead>
              <tr>
                <th>Workstream</th>
                <th>Status</th>
                <th>Priority / Phase</th>
                <th>Required Orders</th>
                <th>Current Tasks</th>
                <th>Next Action</th>
                <th>Open</th>
              </tr>
            </thead>
            <tbody>
              ${workstreamIds
                .map((workstreamId) => {
                  const workstream = context.byId.get(workstreamId);
                  const orderCount = (groupedOrders[workstreamId] || []).length;
                  const taskCount = (groupedTasks[workstreamId] || []).length;
                  return `
                    <tr>
                      <td><strong>${escapeHtml(overviewWorkstreamLabel(workstreamId, context))}</strong></td>
                      <td>${workstream ? statusChip(workstream.status) : statusChip("unassigned")}</td>
                      <td>
                        ${workstream ? chip(`Priority: ${formatToken(workstream.priority)}`) : ""}
                        ${workstream ? chip(`Phase: ${formatToken(workstream.phase)}`) : ""}
                      </td>
                      <td>${escapeHtml(orderCount)}</td>
                      <td>${escapeHtml(taskCount)}</td>
                      <td>${escapeHtml(workstream ? workstream.next_action || "No action recorded" : "Rows need workstream assignment")}</td>
                      <td>${workstream ? `<button class="overview-open-btn" data-open-workstream-id="${escapeHtml(workstreamId)}" type="button">Open</button>` : ""}</td>
                    </tr>
                  `;
                })
                .join("")}
            </tbody>
          </table>
        </div>
      </section>

      ${renderRequiredOrdersAcrossAll(requiredOrders, context)}

      <h2 class="section-title">Tasks by Workstream</h2>
      ${renderTasksByWorkstreamSection(currentTasks, {
        emptyText: "No current tasks found.",
      })}
    `;
  }

  function renderVehicleMap() {
    const viewerUrl = vehicleMapViewerUrl();
    root.innerHTML = `
      <section class="vehicle-map-view">
        <div class="vehicle-map-head">
          <div>
            <h2 class="section-title">3D Vehicle Map</h2>
            <p class="section-subtitle">Orbitable full-car scaffold with part search, group toggles, part focus, and export links for the generated CAD map.</p>
          </div>
          <div class="vehicle-map-links">
            <a class="item-link" href="${escapeHtml(viewerUrl)}" target="_blank" rel="noopener noreferrer">Open Viewer</a>
            ${VEHICLE_MAP_EXPORT_LINKS.map((link, index) => renderItemLink({ ...link, url: dashboardAssetUrl(link.url) }, index)).join("")}
          </div>
        </div>
        <div class="vehicle-map-frame-shell">
          <iframe class="vehicle-map-frame" src="${escapeHtml(viewerUrl)}" title="J40 full vehicle 3D map"></iframe>
        </div>
      </section>
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
        updateRouteHash();
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
    const hideEvidenceMedia = simpleChassisRubbers || active.id === "fabrication_handoff";
    const showFabricationPackages = active.id !== "chassis_fixing";
    const showOperationPanels =
      !simpleChassisRubbers && (active.id === "chassis_fixing" || !(active.subtask_groups && active.subtask_groups.length));

    detailNode.innerHTML = `
      <article class="card">
        <div class="detail-header">
          <h2>${escapeHtml(active.title)}</h2>
          <div class="overview-card-actions">
            ${renderCopyLinkButton(workstreamRoute(active.id), "#", `Copy ${active.title} workstream link`)}
            ${statusChip(active.status)}
          </div>
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
      ${renderChassisBracketAnalysisRegister(active)}
      ${renderFabricationRawMaterials(active)}
      ${showFabricationPackages ? renderFabricationPackages(active.fabrication_packages) : ""}

      ${hideEvidenceMedia ? "" : `
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
                                  ${renderItemButton(row)}
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
    const statusGroups = ["previously", "in_process", "still_required"];
    const supplyTypes = ["tool", "substance", "part"];
    const shouldHideFromOrderingInventory = (row) => {
      const sourceRef = cleanString(row && row.source_ref).toLowerCase();
      const item = cleanString(row && row.item).toLowerCase();
      const workstream = cleanString(row && row.workstream).toLowerCase();
      const notes = cleanString(row && row.notes).toLowerCase();
      const supplyType = cleanString(row && row.supply_type).toLowerCase();
      const blob = [sourceRef, item, workstream, notes].join(" ");
      const bodyPanelInventoryMarkers = new Set([
        "body_floor",
        "body_sections",
        "doors",
        "hood",
        "interior",
        "roof",
        "window_hardware",
        "windows",
      ]);
      if (
        sourceRef === "part_brake_clutch_475_hard_line_stock_full_vehicle_20260514" ||
        item === "full vehicle brake/clutch hard-line tube stock - 4.75 mm / 3/16 in od, 12 m preferred"
      ) {
        return false;
      }
      if (bodyPanelInventoryMarkers.has(item)) {
        return true;
      }
      if (workstream === "fabrication_handoff" || sourceRef.includes("fabrication")) {
        return true;
      }
      if (
        blob.includes("interior conversion") ||
        sourceRef.startsWith("part_hvac_") ||
        blob.includes("hvac") ||
        blob.includes("a/c")
      ) {
        return true;
      }
      if (
        sourceRef === "tool_large_bore_nitto_air_hose_impact_followup_20260517" ||
        (workstream === "site_setup" && (blob.includes("air hose") || blob.includes("air compressor")))
      ) {
        return true;
      }
      if (supplyType !== "part") {
        return false;
      }
      if (workstream === "replacement_pipes") {
        return true;
      }
      return [
        "hose",
        "hard-line",
        "hard line",
        "brake-line",
        "brake line",
        "fuel line",
        "pipe",
        "tube stock",
        "tubing",
        "line support",
      ].some((token) => blob.includes(token));
    };
    const orderingSupplyRows = allSupplyRows.filter((row) => !shouldHideFromOrderingInventory(row));
    const inventorySupplyRows = orderingSupplyRows.filter(
      (row) => cleanString(row && row.status_group).toLowerCase() !== "still_required"
    );
    const groupedSupplyRows = {};
    inventoryGroupOrder.forEach((group) => {
      groupedSupplyRows[group] = [];
    });
    inventorySupplyRows.forEach((row) => {
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
    const supplySummary = supplyTypes.map((supplyType) => {
      const rows = orderingSupplyRows.filter((row) => cleanString(row && row.supply_type).toLowerCase() === supplyType);
      const counts = { previously: 0, in_process: 0, still_required: 0 };
      rows.forEach((row) => {
        const statusGroup = cleanString(row && row.status_group).toLowerCase();
        if (statusGroups.includes(statusGroup)) {
          counts[statusGroup] += 1;
        }
      });
      return {
        supply_type: supplyType,
        previously: counts.previously,
        in_process: counts.in_process,
        still_required: counts.still_required,
        total: rows.length,
      };
    });
    const supplyRowsByStatus = { previously: [], in_process: [], still_required: [] };
    orderingSupplyRows.forEach((row) => {
      const statusGroup = cleanString(row && row.status_group).toLowerCase();
      if (statusGroups.includes(statusGroup)) {
        supplyRowsByStatus[statusGroup].push(row);
      }
    });
    const suppliesPreviously = supplyRowsByStatus.previously || [];
    const suppliesInProcess = supplyRowsByStatus.in_process || [];
    const suppliesStillRequired = supplyRowsByStatus.still_required || [];
    const needToOrderComponentOrder = [
      "brake_hydraulic",
      "electrical_wiring",
      "body_chassis",
      "mechanical_driveline",
      "interior_weatherproofing",
      "workshop_tools",
      "materials_consumables",
      "other",
    ];
    const needToOrderComponentLabels = {
      brake_hydraulic: "Brake / Hydraulic",
      electrical_wiring: "Electrical / Wiring",
      body_chassis: "Body / Chassis / Rubbers",
      mechanical_driveline: "Mechanical / Driveline",
      interior_weatherproofing: "Interior / Weatherproofing",
      workshop_tools: "Workshop Tools",
      materials_consumables: "Materials / Consumables",
      other: "Other / Unsorted",
    };
    const inferNeedToOrderComponent = (row) => {
      const supplyType = cleanString(row && row.supply_type).toLowerCase();
      const inventoryGroup = cleanString(row && row.inventory_group).toLowerCase();
      const workstream = cleanString(row && row.workstream).toLowerCase();
      const blob = [
        row && row.source_ref,
        row && row.item,
        row && row.workstream,
        row && row.inventory_group,
        row && row.procurement_stage,
        row && row.notes,
      ]
        .map((value) => cleanString(value).toLowerCase())
        .join(" ");

      if (workstream === "brake_system") {
        return "brake_hydraulic";
      }
      if (workstream === "body_chassis" || workstream === "chassis_rubbers") {
        return "body_chassis";
      }
      if (workstream === "interior_weatherproofing") {
        return "interior_weatherproofing";
      }
      if (workstream === "mechanical_baseline") {
        return "mechanical_driveline";
      }
      if (workstream === "electrical_reset") {
        return "electrical_wiring";
      }
      if (workstream === "site_setup") {
        return "workshop_tools";
      }
      if (
        ["brake", "clutch", "caliper", "rotor", "drum", "wheel cylinder", "booster", "hydraulic"].some((token) => blob.includes(token))
      ) {
        return "brake_hydraulic";
      }
      if (
        ["interior", "carpet", "foam", "sound", "damping", "trim", "weatherproof"].some((token) => blob.includes(token))
      ) {
        return "interior_weatherproofing";
      }
      if (
        [
          "body mount",
          "body retaining",
          "body specialty",
          "body shoulder",
          "chassis",
          "tub",
          "rubber/plastic",
          "rubbers",
          "bumper",
          "isolator",
          "floor",
          "retainer plate",
          "clip nut",
          "captive",
          "cotter",
          "r-clip",
          "patch plate",
          "mild-steel sheet",
        ].some((token) => blob.includes(token))
      ) {
        return "body_chassis";
      }
      if (
        ["engine", "gearbox", "fuel", "glow", "belt", "compressor bracket", "vacuum", "breather", "oil filter"].some((token) => blob.includes(token))
      ) {
        return "mechanical_driveline";
      }
      if (
        inventoryGroup === "electrical" ||
        ["electrical", "wire", "wiring", "grommet", "fuse", "relay", "speaker", "android", "ignition lock"].some((token) => blob.includes(token))
      ) {
        return "electrical_wiring";
      }
      if (supplyType === "tool" || inventoryGroup === "tools" || workstream === "site_setup") {
        return "workshop_tools";
      }
      if (supplyType === "substance" || inventoryGroup === "substances") {
        return "materials_consumables";
      }
      return "other";
    };
    const compareSupplyRows = (left, right) =>
      [
        cleanString(left && left.supply_type).localeCompare(cleanString(right && right.supply_type)),
        cleanString(left && left.workstream).localeCompare(cleanString(right && right.workstream)),
        cleanString(left && left.item).localeCompare(cleanString(right && right.item)),
      ].find((value) => value !== 0) || 0;
    const stillRequiredRowsByComponent = suppliesStillRequired.reduce((groups, row) => {
      const component = inferNeedToOrderComponent(row);
      if (!groups[component]) {
        groups[component] = [];
      }
      groups[component].push(row);
      return groups;
    }, {});
    Object.values(stillRequiredRowsByComponent).forEach((rows) => rows.sort(compareSupplyRows));
    const stillRequiredComponentGroups = [
      ...needToOrderComponentOrder.filter((component) => stillRequiredRowsByComponent[component] && stillRequiredRowsByComponent[component].length),
      ...Object.keys(stillRequiredRowsByComponent)
        .filter((component) => !needToOrderComponentOrder.includes(component))
        .sort(),
    ].map((component) => ({
      component,
      label: needToOrderComponentLabels[component] || formatToken(component),
      rows: stillRequiredRowsByComponent[component] || [],
    }));

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
    const stillRequiredComponentChips = stillRequiredComponentGroups
      .map((group) => chip(`${group.label}: ${group.rows.length}`))
      .join("");
    const renderStillRequiredRowsTable = (rows) => `
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
              rows.length
                ? rows
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
    `;
    const renderStillRequiredSuppliesSection = () => `
      <section class="card">
        <div class="detail-header">
          <h3>Still Required / Need To Order</h3>
          ${chip(`${suppliesStillRequired.length} rows`)}
        </div>
        <p class="small-muted">Body panel/window marker rows, interior-conversion rows, fabrication rows, detailed hose/line rows, and workshop air-supply rows stay tracked elsewhere; this view keeps only the combined brake/clutch piping line.</p>
        <div class="chip-row">
          ${stillRequiredComponentChips || chip("No still-required rows")}
        </div>
        ${
          stillRequiredComponentGroups.length
            ? stillRequiredComponentGroups
                .map((group) => {
                  const typeCounts = group.rows.reduce((counts, row) => {
                    const type = cleanString(row && row.supply_type).toLowerCase() || "unknown";
                    counts[type] = (counts[type] || 0) + 1;
                    return counts;
                  }, {});
                  const typeChips = Object.entries(typeCounts)
                    .sort((left, right) => left[0].localeCompare(right[0]))
                    .map(([type, count]) => chip(`${formatToken(type)}: ${count}`))
                    .join("");
                  return `
                    <div class="need-to-order-component-group">
                      <div class="detail-header">
                        <h4>${escapeHtml(group.label)}</h4>
                        ${chip(`${group.rows.length} rows`)}
                      </div>
                      <div class="chip-row">${typeChips}</div>
                      ${renderStillRequiredRowsTable(group.rows)}
                    </div>
                  `;
                })
                .join("")
            : renderStillRequiredRowsTable([])
        }
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

  function amirRowText(row) {
    return [
      row && row.entry_id,
      row && row.source_ref,
      row && row.item,
      row && row.vendor,
      row && row.company,
      row && row.supplier,
      row && row.procurement_stage,
      row && row.status_detail,
      row && row.notes,
      row && row.evidence_ref,
      row && row.source,
      row && row.workstream,
    ]
      .map((value) => cleanString(value).toLowerCase())
      .join(" ");
  }

  function amirRowId(row) {
    return cleanString(row && (row.entry_id || row.source_ref || row.procurement_entry_id || row.id));
  }

  function isAmirRunnerRow(row) {
    const text = amirRowText(row);
    return text.includes("amir") || text.includes("aamir") || text.includes("runner_spec_controlled");
  }

  function isAmirFrontDiscRow(row) {
    return AMIR_FRONT_DISC_ENTRY_IDS.has(amirRowId(row));
  }

  function collectAmirRows() {
    const parts = data.parts || {};
    const supplies = data.supplies || {};
    const sourceRows = [
      ...(parts.urgent_actions || []),
      ...(parts.open_rows || []),
      ...(parts.ordered_pending_delivery || []),
      ...(supplies.all_rows || []),
    ];
    const byId = new Map();
    sourceRows.filter(isAmirRunnerRow).forEach((row) => {
      const id = stableItemId(row);
      if (!id || byId.has(id)) {
        return;
      }
      byId.set(id, row);
    });
    return Array.from(byId.values()).sort((left, right) => {
      const leftFront = isAmirFrontDiscRow(left) ? 0 : 1;
      const rightFront = isAmirFrontDiscRow(right) ? 0 : 1;
      return (
        leftFront - rightFront ||
        cleanString(left.workstream).localeCompare(cleanString(right.workstream)) ||
        cleanString(left.procurement_stage).localeCompare(cleanString(right.procurement_stage)) ||
        cleanString(left.item).localeCompare(cleanString(right.item))
      );
    });
  }

  function renderAmirRowsTable(rows, emptyMessage) {
    return `
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Image</th>
              <th>Item</th>
              <th>Workstream</th>
              <th>Stage</th>
              <th>Supplier / Route</th>
              <th>Cost</th>
              <th>Instruction</th>
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
                          ${renderInventoryImageCell(row, row.item || "Amir runner item")}
                          <td>${renderItemButton(row)}</td>
                          <td>${escapeHtml(formatToken(row.workstream || "-"))}</td>
                          <td>${escapeHtml(formatToken(row.procurement_stage || row.status_detail || row.status || "-"))}</td>
                          <td>${tableSupplierCell(row)}</td>
                          <td>${tableCostCell(row)}</td>
                          <td>${escapeHtml(truncateText(row.notes || "", 220) || "-")}</td>
                          <td>${renderLinksCell(row)}</td>
                        </tr>
                      `
                    )
                    .join("")
                : `<tr><td colspan="8">${escapeHtml(emptyMessage || "No Amir rows found.")}</td></tr>`
            }
          </tbody>
        </table>
      </div>
    `;
  }

  function renderAmirPurchaseCards() {
    const amirData = data.amir || {};
    const cardSheet = amirData.card_sheet && cleanString(amirData.card_sheet.path) ? amirData.card_sheet : null;
    const cards = Array.isArray(amirData.purchase_cards) ? amirData.purchase_cards : [];
    if (!cardSheet && !cards.length) {
      return "";
    }
    const shoppingListPath = cleanString(amirData.shopping_list_path);
    const videoGatesPath = cleanString(amirData.video_gates_path);
    return `
      <section id="amir-purchase-cards" class="card">
        <div class="detail-header">
          <h3>Image-Backed Purchase Cards</h3>
          ${renderCopyLinkButton(sectionRoute("amir-purchase-cards"), "#", "Copy Amir purchase cards link")}
        </div>
        <p class="small-muted">Specific photos and card sheet sent to Amir for recognition, receipt checks, quote/photo-only gates, and sample-controlled purchases.</p>
        <div class="link-row">
          ${shoppingListPath ? `<a class="item-link" href="${escapeHtml(shoppingListPath)}">Shopping list</a>` : ""}
          ${videoGatesPath ? `<a class="item-link" href="${escapeHtml(videoGatesPath)}">Video gates</a>` : ""}
        </div>
        ${cardSheet ? renderFigureImage(cardSheet, "Amir image-backed runner cards", { figureClass: "evidence-figure amir-card-sheet", imageClass: "figure-image" }) : ""}
        ${
          cards.length
            ? `
              <div class="table-wrap">
                <table>
                  <thead>
                    <tr>
                      <th>Image</th>
                      <th>Item</th>
                      <th>Current Action</th>
                      <th>Instruction</th>
                      <th>Row</th>
                    </tr>
                  </thead>
                  <tbody>
                    ${cards
                      .map((card) => {
                        const entryId = cleanString(card.entry_id);
                        return `
                          <tr>
                            ${renderInventoryImageCell({ item: card.item, image: card.image }, card.item || "Amir reference")}
                            <td>${escapeHtml(card.item || "-")}</td>
                            <td>${escapeHtml(card.current_action || "-")}</td>
                            <td>${escapeHtml(card.instruction || "-")}</td>
                            <td>${entryId ? `<a class="item-link" href="${escapeHtml(itemRoute(entryId))}">Open row</a>` : "-"}</td>
                          </tr>
                        `;
                      })
                      .join("")}
                  </tbody>
                </table>
              </div>
            `
            : ""
        }
      </section>
    `;
  }

  function sampleChecklistItems(value) {
    if (Array.isArray(value)) {
      return value.map((item) => cleanString(item)).filter(Boolean);
    }
    return cleanString(value)
      .split(/[;|]/)
      .map((item) => item.trim())
      .filter(Boolean);
  }

  function renderAmirSampleFabricationKits() {
    const amirData = data.amir || {};
    const kits = Array.isArray(amirData.sample_fabrication_kits) ? amirData.sample_fabrication_kits : [];
    const kitDocPath = cleanString(amirData.sample_fabrication_kits_path);
    const kitCsvPath = cleanString(amirData.sample_fabrication_kits_csv_path);
    if (!kits.length && !kitDocPath && !kitCsvPath) {
      return "";
    }
    return `
      <section id="amir-sample-fabrication-kits" class="card">
        <div class="detail-header">
          <h3>Bilal Ganj / Montgomery Road Sample Kits</h3>
          ${renderCopyLinkButton(sectionRoute("amir-sample-fabrication-kits"), "#", "Copy sample kits link")}
        </div>
        <p class="small-muted">Physical handoff bundles for sample-copy work. Keep brake hydraulics, handbrake cables, brake springs, and fuel hoses separated.</p>
        <div class="link-row">
          ${kitDocPath ? `<a class="item-link" href="${escapeHtml(kitDocPath)}">Handoff doc</a>` : ""}
          ${kitCsvPath ? `<a class="item-link" href="${escapeHtml(kitCsvPath)}">Kit CSV</a>` : ""}
        </div>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Kit</th>
                <th>Priority</th>
                <th>Shop Route</th>
                <th>Sample Parts To Take</th>
                <th>Instruction</th>
                <th>Rating / Material</th>
                <th>Reject If</th>
              </tr>
            </thead>
            <tbody>
              ${
                kits.length
                  ? kits
                      .map((kit) => {
                        const sampleParts = sampleChecklistItems(kit.sample_parts_checklist || kit.physical_samples_to_pack);
                        return `
                          <tr>
                            <td><strong>${escapeHtml(kit.kit_id || "-")}</strong><br><span class="small-muted">${escapeHtml(kit.kit_name || "")}</span></td>
                            <td>${escapeHtml(cleanString(kit.priority || "P1").toUpperCase())}</td>
                            <td>${escapeHtml(kit.target_market_or_shop || "-")}</td>
                            <td>${renderPlainList(sampleParts)}</td>
                            <td>${escapeHtml(kit.fabrication_or_buy_instruction || "-")}</td>
                            <td>${escapeHtml(kit.required_rating_or_material || "-")}</td>
                            <td>${escapeHtml(kit.reject_if || "-")}</td>
                          </tr>
                        `;
                      })
                      .join("")
                  : '<tr><td colspan="7">No sample fabrication kits found.</td></tr>'
              }
            </tbody>
          </table>
        </div>
      </section>
    `;
  }

  function renderAmir() {
    const amirRows = collectAmirRows();
    const frontDiscRows = amirRows.filter(isAmirFrontDiscRow);
    const runnerSpecRows = amirRows.filter((row) => cleanString(row.procurement_stage).toLowerCase() === "runner_spec_controlled");
    const paymentHeldRows = amirRows.filter((row) => {
      const text = amirRowText(row);
      return text.includes("payment waits") || text.includes("pay only") || text.includes("buy only") || text.includes("no payment");
    });

    root.innerHTML = `
      <h2 class="section-title">Amir Runner</h2>
      <p class="section-subtitle">Local collection, quote, and sample-match tasks. Amir can collect prices/photos and buy only where the written spec or labelled old sample removes fit judgement from him.</p>

      <section class="metrics-grid">
        <article class="card">
          <p class="metric-value">${escapeHtml(amirRows.length)}</p>
          <p class="metric-label">Open Amir Rows</p>
        </article>
        <article class="card">
          <p class="metric-value">${escapeHtml(frontDiscRows.length)}</p>
          <p class="metric-label">Front Disc Rows</p>
        </article>
        <article class="card">
          <p class="metric-value">${escapeHtml(runnerSpecRows.length)}</p>
          <p class="metric-label">Runner Spec-Controlled</p>
        </article>
        <article class="card">
          <p class="metric-value">${escapeHtml(paymentHeldRows.length)}</p>
          <p class="metric-label">Payment-Gated Rows</p>
        </article>
      </section>

      ${renderAmirPurchaseCards()}

      ${renderAmirSampleFabricationKits()}

      <section class="card">
        <div class="detail-header">
          <h3>Front Disc Collection List</h3>
          ${renderCopyLinkButton(sectionRoute("amir-front-disc"), "#", "Copy Amir front disc list link")}
        </div>
        <p id="amir-front-disc" class="small-muted">Safety-critical quote work only. No payment unless labelled old samples, written mechanic specs, or explicit mechanic/user approval confirm the exact item.</p>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Priority</th>
                <th>Item</th>
                <th>Amir action</th>
                <th>Buy / payment gate</th>
              </tr>
            </thead>
            <tbody>
              ${AMIR_FRONT_DISC_TASKS.map(
                (task) => `
                  <tr>
                    <td>${escapeHtml(task.priority)}</td>
                    <td>${escapeHtml(task.item)}</td>
                    <td>${escapeHtml(task.action)}</td>
                    <td>${escapeHtml(task.gate)}</td>
                  </tr>
                `
              ).join("")}
            </tbody>
          </table>
        </div>
      </section>

      <h3 class="section-title">Front Disc Rows</h3>
      ${renderAmirRowsTable(frontDiscRows, "No front disc Amir rows found in the current dashboard data.")}

      <h3 class="section-title">All Amir Runner Rows</h3>
      ${renderAmirRowsTable(amirRows, "No Amir runner rows found in the current dashboard data.")}
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
    const sequenceId = createImageSequence();
    return `
      <div class="requirement-evidence-grid capture-task-evidence-grid">
        ${images
          .map((image) => {
            const prepared = prepareImage(image, fallbackCaption, { sequenceId });
            return `
              <div class="requirement-evidence-item">
                ${renderPreparedMedia(prepared, "table-image-btn", "table-image")}
                <span class="table-image-note">${escapeHtml(prepared.effective.media_id || "")}</span>
              </div>
            `;
          })
          .join("")}
      </div>
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

      <h3 class="section-title">Current Tasks by Workstream</h3>
      ${renderTasksByWorkstreamSection(nowTasks, {
        showEvidence: true,
        emptyText: "No current photo/data tasks found.",
      })}

      <h3 class="section-title">Later / Deferred by Workstream</h3>
      ${renderTasksByWorkstreamSection(tasks.filter((task) => cleanString(task.timing).toLowerCase() === "later"), {
        emptyText: "No later/deferred tasks found.",
      })}
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
        title: "Akbar Wiring And Floor Samples",
        description: "Akbar's missing before/after examples for engine-bay wiring cleanup and floor rust-through around the accelerator pedal.",
        source: "Akbar Khan WhatsApp",
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

  function contactChannelUrl(contact) {
    const value = cleanString(contact && contact.channel_or_url);
    return /^https?:\/\//i.test(value) ? value : "";
  }

  function renderReferenceProjectIdeas(ideas) {
    const rows = Array.isArray(ideas) ? ideas : [];
    if (!rows.length) {
      return "";
    }
    return `
      <section class="reference-section-list" aria-label="Reference ideas from messages">
        <h3 class="section-title">Reference Ideas</h3>
        <div class="reference-idea-list">
          ${rows
            .map((idea) => {
              const contacts = splitMultiValue(idea.contact_refs);
              return `
                <article class="card reference-focus-card reference-idea-card">
                  <div class="detail-header">
                    <h3>${escapeHtml(idea.title || "Reference Idea")}</h3>
                    ${statusChip(idea.status || "open")}
                  </div>
                  <p class="small-muted">${escapeHtml(idea.summary || "")}</p>
                  <div class="chip-row">
                    ${idea.workstream ? chip(formatToken(idea.workstream)) : ""}
                    ${idea.category ? chip(formatToken(idea.category)) : ""}
                    ${idea.source_chat ? chip(idea.source_chat) : ""}
                    ${idea.source_date ? chip(idea.source_date) : ""}
                  </div>
                  ${contacts.length ? `<div class="chip-row">${contacts.map((contact) => chip(contact)).join("")}</div>` : ""}
                  ${idea.next_action ? `<p class="small-muted"><strong>Next:</strong> ${escapeHtml(idea.next_action)}</p>` : ""}
                  ${idea.evidence_ref ? `<p class="small-muted"><strong>Evidence:</strong> <code>${escapeHtml(idea.evidence_ref)}</code></p>` : ""}
                </article>
              `;
            })
            .join("")}
        </div>
      </section>
    `;
  }

  function renderContactRegister(contacts) {
    const rows = Array.isArray(contacts) ? contacts : [];
    if (!rows.length) {
      return "";
    }
    return `
      <section class="reference-section-list" aria-label="Contact register">
        <h3 class="section-title">Contact Register</h3>
        <div class="reference-idea-list">
          ${rows
            .map((contact) => {
              const url = contactChannelUrl(contact);
              const phoneDisplay = redactPhoneNumber(contact.phone);
              const linkPayload = url ? { ...contact, url } : contact;
              return `
                <article class="card reference-focus-card reference-idea-card">
                  <div class="detail-header">
                    <h3>${escapeHtml(contact.name || "Contact")}</h3>
                    ${statusChip(contact.status || "active")}
                  </div>
                  <p class="small-muted">${escapeHtml(contact.role || "")}</p>
                  <div class="chip-row">
                    ${contact.category ? chip(formatToken(contact.category)) : ""}
                    ${contact.location ? chip(contact.location) : ""}
                    ${contact.confidence ? chip(`Confidence: ${formatToken(contact.confidence)}`) : ""}
                  </div>
                  <dl class="meta-grid">
                    ${phoneDisplay ? `<dt>Phone</dt><dd>${escapeHtml(phoneDisplay)}</dd>` : ""}
                    ${contact.source ? `<dt>Source</dt><dd>${escapeHtml(contact.source)}</dd>` : ""}
                    ${contact.source_date ? `<dt>Date</dt><dd>${escapeHtml(contact.source_date)}</dd>` : ""}
                    ${contact.channel_or_url && !url ? `<dt>Channel</dt><dd>${escapeHtml(contact.channel_or_url)}</dd>` : ""}
                  </dl>
                  ${renderLinksPanel(linkPayload)}
                  ${contact.next_action ? `<p class="small-muted"><strong>Next:</strong> ${escapeHtml(contact.next_action)}</p>` : ""}
                  ${contact.notes ? `<p class="small-muted">${escapeHtml(contact.notes)}</p>` : ""}
                  ${contact.evidence_ref ? `<p class="small-muted"><strong>Evidence:</strong> <code>${escapeHtml(contact.evidence_ref)}</code></p>` : ""}
                </article>
              `;
            })
            .join("")}
        </div>
      </section>
    `;
  }

  function renderCoolingPack() {
    const photorealisticVisuals = [
      {
        path: "../../data/manual/fabrication/front_cooling_stack_rev_c/work_document_assets/rev_g_ph01_complete_wide_exploded_v2.png",
        caption: "PH01 — Complete wide Rev G split-out proposal. The main row separates the installed front-to-rear order: centred twin Toyota/Denso pusher module, short central 500 × 180 × 50 charge cooler, 559 × 356 × 21 condenser, HJ47/2H-pattern radiator, then the full-face rear shroud and large retained mechanical puller. Uprights, rails, direct ears, lower saddles, drier, protected electrical enclosures, seals, connectors and fasteners are included. Exploded positions identify parts only; PH05/D09 control the compact installed electrical placement.",
        specific_component: "Complete wide Rev G three-core / three-fan component split-out",
      },
      {
        path: "../../data/manual/fabrication/front_cooling_stack_rev_c/work_document_assets/rev_g_ph02_toyota_donor_assembled.png",
        caption: "PH02 — Rev G off-vehicle central cooling-module proposal: two equal centred 248 mm Prado/GX Denso donor pushers, the retained rear mechanical puller, direct top ears and lower saddles. Chassis posts and electrical boxes are intentionally omitted; PH03/PH04 control the attachment visual and PH05/D09/E2 control the electrical placement.",
        specific_component: "Rev G off-vehicle Toyota-donor cooling module proposal",
      },
      {
        path: "../../data/manual/fabrication/front_cooling_stack_rev_c/work_document_assets/rev_g_ph03_complete_stack_cutaway_v2.png",
        caption: "PH03 — Complete Rev G installed proposal with a controlled depth cutaway. The normal front portion shows the centred twin pushers and both original top-hole attachments; the cutaway visibly accounts for the short charge cooler, condenser, main radiator, sealed rear shroud and large engine-driven puller. The mechanical fan remains centred behind the radiator and inside the two uprights—it is not a side annex. Each original top hole uses the direct M8/washer, sleeved-isolator and independent 4 mm ear path to its radiator side rail, with the lower saddle carrying weight.",
        specific_component: "Complete three-core / three-fan J40 installation cutaway",
      },
      {
        path: "../../data/manual/fabrication/front_cooling_stack_rev_c/work_document_assets/rev_g_ph04_direct_side_ear_closeup.png",
        caption: "PH04 — Direct-side-ear close-up: original top-return hole, M8 bolt and sleeved EPDM isolator locate one short ear immediately below; the lower saddle under that same radiator side rail carries the weight.",
        specific_component: "Existing-top-hole direct radiator-side-ear close-up",
      },
      {
      path: "../../data/manual/fabrication/front_cooling_stack_rev_c/work_document_assets/rev_g_ph05_independent_electrical_mounts.png",
      caption: "PH05 — Rev G electrical-placement detail only: the covered Relay Rev D box is upper/forward and the sealed MIDI enclosure lower/rear, centred one behind the other above/rear of the radiator top tank. Separate local non-radiator brackets and hoods keep both envelopes inside W0/upright width and clear of the active fin/fan aperture. D09 and E2/E2a control exact mounting.",
      specific_component: "Rev G independent sealed MIDI and covered Relay mounts proposal",
      },
    ];
    const diagrams = [
      {
        path: "../../data/manual/fabrication/front_cooling_stack_rev_c/work_document_assets/rev_c_d01_complete_stack.png",
        caption: "D01 — Rev G controlled layout: all-front elevation and central component order. Nominal dimensions remain subject to the listed release gates.",
        specific_component: "Rev G complete cooling-system elevation",
      },
      {
        path: "../../data/manual/fabrication/front_cooling_stack_rev_c/work_document_assets/rev_c_d02_radiator_assembly.png",
        caption: "D02 — Rev G HJ47-pattern radiator assembly: 530 × 435 × 64 mm is active-core thermal basis only; final complete radiator envelope is field-controlled by R0.",
        specific_component: "Rev G HJ47-pattern radiator assembly orthographic",
      },
      {
        path: "../../data/manual/fabrication/front_cooling_stack_rev_c/work_document_assets/rev_c_d03_radiator_components.png",
        caption: "D03 — Rev G exploded radiator parts: recored/custom HJ47-pattern unit, not a Prado radiator.",
        specific_component: "Rev G exploded HJ47-pattern radiator parts",
      },
      {
        path: "../../data/manual/fabrication/front_cooling_stack_rev_c/work_document_assets/rev_c_d04_component_dimensions.png",
        caption: "D04 — Rev G central charge cooler, condenser and 248 mm twin-fan nominal dimensions.",
        specific_component: "Rev G compact all-front component dimensions",
      },
      {
        path: "../../data/manual/fabrication/front_cooling_stack_rev_c/work_document_assets/rev_c_d05_mounting_shroud.png",
        caption: "D05 — Rev G mounting, saddles and custom full-face shroud details; do not reuse a complete donor shroud.",
        specific_component: "Rev G mounting and custom-shroud details",
      },
      {
        path: "../../data/manual/fabrication/front_cooling_stack_rev_c/work_document_assets/rev_c_d06_side_geometry.png",
        caption: "D06 — Rev G complete front-to-rear depth stack, gaps and M3 fit gate: 215 mm absolute stack basis / 225 mm preferred installed-clearance envelope.",
        specific_component: "Rev G all-front side-section and depth gates",
      },
      {
        path: "../../data/manual/fabrication/front_cooling_stack_rev_c/work_document_assets/rev_c_d07_fan_wiring.png",
        caption: "D07 — Rev G independent twin Prado/GX pusher branches: every fuse, holder and live fuse stud is inside the closed MIDI box; relays remain in the separate covered Relay Rev D box.",
        specific_component: "Rev G complete fan wiring",
      },
      {
        path: "../../data/manual/fabrication/front_cooling_stack_rev_c/work_document_assets/rev_d_d08_existing_top_hole_mount.png",
        caption: "D08 — Rev G direct side-ear mounting: short ear directly under each original top-return hole; lower saddle under the same radiator side rail; B0/H0-L/H0-R/W0/P0/R0/BRKT control release.",
        specific_component: "Rev G direct-side-ear existing-top-hole pickup detail",
      },
      {
        path: "../../data/manual/fabrication/front_cooling_stack_rev_c/work_document_assets/rev_g_d09_independent_electrical_mounts.png",
        caption: "D09 — Rev G electrical width control: Relay and MIDI use separate local brackets and hoods, but are vertically/depth staggered so both complete front-view envelopes remain inside W0/uprights and the combined projected width is no greater than the Relay 360 mm envelope. Never side-by-side across vehicle width.",
        specific_component: "Rev G independent electrical brackets and service detail",
      },
      {
        path: "../../data/manual/fabrication/front_cooling_stack_rev_c/work_document_assets/rev_g_d10_procurement_fit_control.png",
        caption: "D10 — Rev G procurement and fit-control drawing: Toyota donor scope, nominal dimensions, measurement records and purchase-release gates.",
        specific_component: "Rev G procurement and fit-control drawing",
      },
    ];
    const purchasePhases = [
      {
        phase: "1 — Sample / mock-up only",
        status: "Quote and trial-fit; do not release final cores",
        items: "Inspect/recore the existing 2H radiator; obtain two matched Prado 120/GX470 fan motor, blade and connector samples; obtain one 14 × 22 condenser sample and one 500 × 180 × 50 mm / 57 mm-outlet charge-cooler sample; bring the actual Relay Rev D and MIDI Rev D hardware to the mock-up.",
        release: "Record complete physical envelopes, part labels and connector condition. First record B0/H0-L/H0-R/W0/P0/R0, make the rigid two-hole BRKT template, then build the full-size dummy. A Prado/GX radiator or complete donor shroud is not an approved purchase item.",
      },
      {
        phase: "2 — Buy after measured fit release",
        status: "Buy only after B0/H0-L/H0-R/W0/P0/R0/BRKT, M1–M6 and F1/F2 pass",
        items: "Final HJ47-pattern recore/custom radiator; final condenser and charge cooler; matched Prado/GX Denso fan motor/blade/connector pair; new drier/trinary parts, A/C hose/fittings, seals and standard M6/M8 isolation hardware.",
        release: "Use the measured whole-part envelopes, not fin dimensions alone. Custom-build only the central shroud, two short direct side ears/adapters, lower saddles, seals and measured pipe adapters after the real samples clear the body, engine fan and service routes. Do not make a transverse radiator carrier.",
      },
      {
        phase: "3 — Electrical / commissioning",
        status: "Release from measured current and completed installation",
        items: "Two independent fan relay/fuse branches with every fuse, holder and live fuse stud inside the closed MIDI Rev D box; covered Relay Rev D box, cable, glands, connectors, protection, P-clips and service consumables; coolant, pressure-test media, evacuation/charge materials and logging equipment.",
        release: "Size relays, fuses and cable from measured start/run current and voltage drop; pass E1 plus individual relay-box and MIDI-box E2 service/weather checks, then T1–T3 at the required 50°C conditions before claiming no cooling derate or increasing boost.",
      },
    ];
    const fitGates = [
      ["M1", "Clear width", "Measure between upright inner faces at top, centre and bottom. A 559 mm complete condenser needs M1 ≥569 mm after the 5 mm hard clearance each side; every tank, bracket, fan guard, plug and wire bend must also fit."],
      ["M2", "Clear height", "Measure the actual complete module with bonnet latch, grille and lower protection represented. The 435 mm active-core basis and every complete tank, seam, filler, drain, ear and saddle must remain inside the available aperture; no nominal height releases manufacture."],
      ["M3", "Complete stack depth", "Measure grille/guard to the locked radiator plane at several heights. The actual complete pusher module + actual charge cooler + gaps + actual condenser + complete R0 radiator dummy, including tanks, seams, filler, drain, ears, locators, plugs, guards and wire bends, must fit the 215 mm absolute stack basis. The 530 × 435 × 64 mm figure is an active-core thermal/depth basis only, not a radiator dummy or finished envelope. A measured 225 mm installed-clearance envelope is preferred; any smaller measured envelope needs written proof of every body, plug, guard and engine-movement clearance before release."],
      ["M4", "Pipe and service routes", "Prove 57 mm charge pipes turn rearward at the lower corners and A/C fittings/tools remain accessible without extra front width, rubbing or sharp bends. Record complete fitting and tool envelopes, not core dimensions alone."],
      ["M5", "Mechanical fan clearance", "At least 20 mm static axial blade clearance and 15 mm radial clearance through engine movement; 25–30 mm axial is preferred."],
      ["M6", "Full-size vehicle dummy", "Final grille, bonnet and bumper/guard close; the assembly is central and symmetric; every module removes separately."],
      ["B0", "Top-hole datum", "Make one rigid 1:1 two-hole template from the original inward top-return holes. Record centre-to-centre, hole diameter/condition, edge distance, tab thickness and elevation; do not infer this from a photo."],
      ["H0-L / H0-R", "Left/right hole plane to saddle seat", "Measure each original top-hole plane to the lower saddle seat on the same radiator side rail. Saddles carry the weight; the top M8 bolts only locate and retain."],
      ["W0", "Upright aperture", "Record minimum clear width between inner faces of both uprights at top, middle and bottom, including weld beads. Existing bracket basis is 48 mm main face, 410 mm upright and 58 mm inward top return; this does not state the radiator height."],
      ["P0", "Rail fore-aft plane", "Measure original inward return/post plane to the radiator side-rail plane. Both short ears must sit directly below their original holes with at least 5 mm hard clearance; no pulling into alignment."],
      ["R0", "Complete radiator envelope", "Record the donor/recored radiator’s complete W × H × D including tanks, seams, filler, drain, ears and lower locators. 530 × 435 × 64 mm is active-core thermal basis only, not a finished-radiator envelope or fit claim."],
      ["BRKT", "Direct side-ear dummy", "Build a full-size two-rail dummy with one short ear under each original top hole and one lower saddle under each same rail. Both M8 bolts must hand-enter with zero pull; prove removal and ≥5 mm hard rail/post clearance. No chassis modification, slot, ream or transverse radiator carrier."],
      ["F1", "Front-fan envelope and centring", "Two equal 248 mm Prado/GX Toyota/Denso donor motors/blades/connectors only; ≥258 mm rings; 266 mm C-C; same height; equal left/right fin bands; no contact through vibration. A complete donor shroud is not an approved fit assumption."],
      ["F2", "Mechanical fan and shroud", "Full-face sealed shroud, 35–50% blade insertion and movement clearance all pass."],
      ["F3", "Front installed airflow", "Twin pushers deliver ≥3,000 m³/h at 13.5 V through the final grille, stone screen and all three cores."],
      ["F4", "Mechanical installed airflow", "Retained puller delivers ≥9,000 m³/h at 1,500 engine rpm through the complete three-core stack."],
      ["E1", "Electrical proof", "Correct polarity, two independent fused/relayed branches, acceptable voltage drop/current/temperature, and adequate hot-idle alternator output."],
      ["E2", "Independent electrical brackets", "Mock the covered Relay Rev D box and closed MIDI Rev D five-fuse enclosure on two separate local structural brackets. Keep each complete box, hood, bracket, cable bend and service sweep inside W0/the upright front-view silhouette. Stagger vertically and/or in depth so MIDI's projected width lies wholly within the Relay 360 mm base envelope; never side-by-side across vehicle width. Each gets its own hood and down/rear cable exit. Neither may load the radiator or obstruct active fins, sealed airflow or module removal."],
      ["E2a", "Individual weather/service proof", "For each box separately, prove its lid/cover sweep, cable bend, glands, drip path, P-clips, disconnect, removal path and bonnet/grille clearance with the real box installed. Hose-spray/dust-check both final hoods, then open both boxes and record dry, clean interiors. No formal IP claim unless purchased-rated or tested."],
      ["T1", "50°C hot idle", "A/C and cabin blower maximum for 30 minutes; coolant and A/C pressures stable, with no recirculation, leak or electrical heating."],
      ["T2", "50°C loaded operation", "Low-speed climb and sustained load pass; 115 kW equivalent remains stable for 60 minutes and 130 kW equivalent for 10 minutes."],
      ["T3", "Charge-air proof", "Charge cooler meets ≥15 kW target, manifold IAT ≤80°C and complete turbo-to-manifold pressure loss ≤10 kPa with no leak."],
    ];

    root.innerHTML = `
      <div class="cooling-pack-view">
        <section class="cooling-pack-hero" id="cooling-pack-summary">
          <div class="cooling-pack-hero-copy">
            <div class="cooling-pack-kicker-row">
              <p class="eyebrow">Fabricator issue · Rev G · 1 August 2026</p>
              ${renderCopyLinkButton(sectionRoute("cooling-pack-summary"), "#", "Copy cooling-pack summary link")}
            </div>
            <h2>J40 Integrated Radiator &amp; Front Cooling Pack</h2>
            <p class="cooling-pack-lead">A simple, clean-looking, best-effort all-front package for the Toyota 2H, R134a A/C and a conservative future turbo installation. Use Prado 120/GX470 donor parts only for the two matched front fan motors, blades and connectors; the radiator remains an HJ47-pattern recored/custom unit on two direct side rails. The 50°C and no-cooling-derate claims remain conditional until the real three-core assembly passes every bracket-fit, airflow and thermal acceptance gate.</p>
            <div class="cooling-pack-release">
              <span class="cooling-pack-hold">50°C CLAIM / FINAL MANUFACTURE: HOLD</span>
              <span>Released for quotation, sample-part sourcing, measurements and full-size mock-up. Final cores and coating wait for measured vehicle fit; logged thermal and charge-air proof release the performance claim.</span>
            </div>
            <blockquote>
              <strong>Karigar ke liye:</strong> Kul teen fans hain: do barabar, centre mein front electric pushers aur radiator ke peechay aik retained engine-driven puller. Fans, intercooler, condenser aur radiator sab dono uprights ke darmiyan aik seedhi central line mein lagain. Radiator ki har side rail ke neeche lower rubber saddle weight uthaye; usi rail ka aik chhota ear existing top-return hole ke bilkul neeche M8 bolt se locate ho—koi cross-car carrier nahin. Existing post basis 48 mm face, 410 mm upright aur 58 mm inward return hai; pehle B0/H0-L/H0-R/W0/P0/R0 naapain aur BRKT dummy pass karein. Covered Relay Rev D aur band/gasketed MIDI Rev D box alag, staggered local structural brackets aur alag rain hoods par lagain—radiator, battery stand ya shared plate par nahin. Pehle gaari naapain aur poora cardboard/plywood dummy fit karein; phir final cores banayen.
            </blockquote>
            <div class="cooling-pack-downloads">
              <a class="item-link package-download-link cooling-pack-download" href="../../docs/J40-integrated-cooling-pack-fabricator-specification-rev-c.docx" download>Download shop specification (.docx)</a>
              <a class="item-link cooling-pack-download" href="../../docs/j40-rev-g-toyota-donor-cooling-pack-purchase-list-20260801.md" download>Download simple purchase list (.md)</a>
              <a class="item-link cooling-pack-download" href="../../docs/J40-integrated-cooling-pack-fabricator-specification-rev-c.md" download>Download source specification (.md)</a>
            </div>
          </div>
          <dl class="cooling-pack-facts" aria-label="Key cooling-pack dimensions">
            <div><dt>Ambient release</dt><dd>50°C + A/C on</dd><span>52°C soak / hot restart</span></div>
            <div><dt>Radiator duty</dt><dd>≥115 kW continuous</dd><span>≥130 kW for 10 min</span></div>
            <div><dt>Front electric air</dt><dd>≥3,000 m³/h</dd><span>13.5 V through all 3 cores</span></div>
            <div><dt>Charge-air duty</dt><dd>≥15 kW</dd><span>central core; IAT ≤80°C</span></div>
            <div><dt>Condenser basis</dt><dd>559 × 356 × 21 mm</dd><span>14 × 22 in nominal</span></div>
            <div><dt>Charge cooler basis</dt><dd>500 × 180 × 50 mm</dd><span>57 mm beaded outlets</span></div>
            <div><dt>Radiator active-core basis</dt><dd>530 × 435 × 64 mm</dd><span>thermal basis only; complete W × H × D is R0-controlled</span></div>
            <div><dt>Front pusher pair</dt><dd>2 × 248 mm / 266 mm C-C</dd><span>Prado/GX motor, blade, connector only</span></div>
            <div><dt>Depth release</dt><dd>215 mm absolute stack basis</dd><span>225 mm installed clearance preferred</span></div>
          </dl>
        </section>

        <section class="card cooling-pack-section cooling-pack-start-here" id="cooling-pack-start-here">
          <div class="detail-header">
            <div>
              <p class="cooling-pack-section-label">Start here · sourcing instruction</p>
              <h3>What to buy, what to keep, and what the local shop fabricates</h3>
            </div>
            ${renderCopyLinkButton(sectionRoute("cooling-pack-start-here"), "#", "Copy cooling-pack sourcing summary link")}
          </div>
          <div class="cooling-pack-start-rule" role="note">
            <strong>This is not a Prado radiator conversion or a catalogue direct-fit kit.</strong>
            <span>The only Prado 120/GX470 donor items are two matched Toyota/Denso front-fan motor, 248 mm blade and plug/pigtail sets. The radiator follows the HJ47/2H pattern and the brackets and shrouds are measured local fabrication.</span>
          </div>
          <div class="table-wrap cooling-pack-table-wrap">
            <table class="cooling-pack-table cooling-pack-source-table">
              <thead><tr><th>Source class</th><th>Qty / item</th><th>Exact standard item or search reference</th><th>Pakistan sourcing instruction</th></tr></thead>
              <tbody>
                <tr>
                  <td><span class="cooling-pack-source-badge is-used">Buy used Toyota donor</span></td>
                  <td><strong>2 matched front-fan sets</strong></td>
                  <td>Prado 120/GX470-family Toyota/Denso motor + 248 mm blade + plug/pigtail. Assembly search references <strong>88590-60040 / -60050 / -60051 / -60060</strong>; motor <strong>88550-12160</strong>; blade <strong>88453-60010</strong>.</td>
                  <td><strong>Practical breaker/Bilal Ganj route.</strong> Bring two physically matching sets, check rotation/hand/depth and bench-test before payment. Part numbers identify candidates only; they do not approve direct fit. <strong>Do not buy a Prado radiator or complete donor shroud.</strong></td>
                </tr>
                <tr>
                  <td><span class="cooling-pack-source-badge is-retain">Retain / rebuild existing</span></td>
                  <td><strong>1 rear fan/hub + 2 electrical boxes</strong></td>
                  <td>Existing Toyota 2H engine-driven puller/hub; blade candidates <strong>16361-68030 / -68031</strong>. Existing covered Relay Rev D box and closed MIDI Rev D fuse box.</td>
                  <td><strong>Already held on the vehicle/project.</strong> Inspect, rebuild where necessary and trial-fit the actual closed boxes. Do not buy replacements unless inspection rejects the existing part.</td>
                </tr>
                <tr>
                  <td><span class="cooling-pack-source-badge is-sample">Sample, then local recore</span></td>
                  <td><strong>1 radiator</strong></td>
                  <td>HJ47/2H radiator pattern <strong>16400-68030</strong> or sound original tanks. <strong>530 × 435 × 64 mm is the active-core thermal basis only</strong>, not the finished radiator size.</td>
                  <td><strong>Exact HJ47/2H local stock is not confirmed.</strong> Source a physical pattern/tank sample, record complete R0, and use a competent local radiator shop. Release the final core only after the rigid two-hole fixture and full-size dummy pass.</td>
                </tr>
                <tr>
                  <td><span class="cooling-pack-source-badge is-new">Source new standard — verify stock</span></td>
                  <td><strong>1 each + service hardware</strong></td>
                  <td>Condenser <strong>559 × 356 × 21 mm</strong>; charge cooler <strong>500 × 180 × 50 mm</strong> with 57 mm outlets; new drier <strong>88471-34010</strong> only if ports fit, otherwise new #6 O-ring equivalent; hoses, relays/connectors, M6/M8 hardware and EPDM.</td>
                  <td><strong>Use local A/C, turbo and automotive-hardware suppliers.</strong> Exact stock changes; the specified charge-cooler size and every complete condenser/drier envelope and port remain <strong>physical-sample first</strong>.</td>
                </tr>
                <tr>
                  <td><span class="cooling-pack-source-badge is-fabricate">Fabricate locally</span></td>
                  <td><strong>Measured interfaces only</strong></td>
                  <td>Two radiator side rails, two 4 mm direct top ears, two lower saddles, centred twin-pusher shroud, rear shroud if the Toyota item cannot fit, exchanger tabs, seals/stone screen, two separate electrical brackets/hoods and measured adapters.</td>
                  <td><strong>Make only after the real parts, rigid top-hole template and full-size dummy pass.</strong> No transverse radiator carrier, shared electrical tray, new chassis hole, slot or forced bolt alignment.</td>
                </tr>
              </tbody>
            </table>
          </div>
          <p class="cooling-pack-simple-rule"><strong>Buyer rule:</strong> “Toyota part number” means a search/identity reference. “Buy” means obtain a physical sample and pass the stated measurement gate; it never means assumed bolt-in fit.</p>
        </section>

        <section class="card cooling-pack-section cooling-pack-photorealistic" id="cooling-pack-photorealistic-visuals">
          <div class="detail-header">
            <div>
              <p class="cooling-pack-section-label">PH01 · PH02 · PH03 · PH04 · PH05 · Rev G visual proposals</p>
              <h3>Component parts, assembled pack and positive existing-hole vehicle mounting</h3>
            </div>
            ${renderCopyLinkButton(sectionRoute("cooling-pack-photorealistic-visuals"), "#", "Copy photorealistic fabrication visuals link")}
          </div>
          <div class="cooling-pack-photorealistic-note" role="note">
            <strong>AI visual proposals only.</strong> The deterministic Rev G drawings D01–D10, the measured vehicle and the thermal test log control manufacture. Do not scale an AI image or use it to release a core, direct radiator ear, fan position, duct or electrical bracket.
          </div>
          <div class="cooling-pack-no-extra-width" role="note">
            <strong>Positive top pickup — existing holes are the master datums.</strong>
            <span>Use one M8 through-bolt per side through the original inward top-return hole: bolt head and large washer above; sleeved EPDM isolator; one short removable radiator-side ear directly below; washer and locking nut below.</span>
            <span>The lower rubber-lined saddles carry all radiator weight under those same two side rails. The two upper bolts only locate and retain the radiator.</span>
            <span><strong>No new chassis holes, slots, reaming or forced alignment:</strong> transfer both holes from a rigid 1:1 template, drill only the two short ears/adapters, and require both bolts to enter freely by hand. Existing post basis: 48 mm face / 410 mm upright / 58 mm inward return.</span>
          </div>
          <div class="cooling-pack-no-extra-width" role="note">
            <strong>No extra front width.</strong>
            <span>The radiator, condenser, charge cooler and front pusher frame stay entirely between the existing welded uprights / original central aperture and stack only front-to-rear.</span>
            <span>The receiver-drier and A/C ports sit behind/in the shadow of an upright. The covered Relay Rev D box and closed, gasketed MIDI Rev D fuse enclosure use two separate local structural brackets, each with its own shallow rain hood, down/rear cable exit and service sweep. Keep both complete envelopes inside W0/the uprights' existing front-view silhouette; stagger vertically and/or in depth so MIDI's projected width is wholly within the Relay 360 mm envelope—never place them side-by-side across vehicle width. They must not cover active fins, change either fan centre, load the radiator/isolated mounts or occupy the battery stand. Exact locations remain an E2/E2a measured hold. The MIDI lid stays shut in normal operation; no formal IP rating is claimed unless purchased-rated or tested. The master cutoff remains battery-side.</span>
            <span>There is no side cooler, side fan, side service tower or extra visible width. Charge pipes turn rearward/inboard at the measured lower corners.</span>
            <span><strong>Depth remains unproven pending M3/M6:</strong> the complete three-core dummy, with real fan motors, guards, plugs, tanks, pipe bends, gaps and tools, controls manufacture.</span>
          </div>
          <p class="small-muted">Read the five images in order and click any image to inspect it full size: PH01 widely separates the complete inventory and all three heat exchangers / three fans; PH02 is deliberately off-vehicle and shows the assembled central cooling module; PH03 places the complete pack on the later chassis-photo geometry, retains both direct original-top-hole attachments and uses a controlled cutaway to expose the centred rear mechanical fan and every core layer; PH04 shows one ear and lower-saddle load path; PH05 is a tight upper/rear electrical-placement detail with the two boxes on separate brackets. These are visual proposals, not measured fit evidence. Build only to deterministic Rev G drawings D01–D10, B0/H0-L/H0-R/W0/P0/R0/BRKT, M1–M6, F1–F4, E1–E2a, an approved full-size dummy and the passed T1–T3 tests.</p>
          <div class="cooling-pack-photorealistic-grid">
            ${photorealisticVisuals
              .map((visual) =>
                renderFigureImage(visual, visual.caption, {
                  figureClass: "cooling-pack-photorealistic-figure",
                  buttonClass: "image-open-btn",
                  imageClass: "cooling-pack-photorealistic-image",
                  captionClass: "cooling-pack-photorealistic-caption",
                })
              )
              .join("")}
          </div>
        </section>

        <section class="card cooling-pack-section" id="cooling-pack-layout">
          <div class="detail-header">
            <div>
              <p class="cooling-pack-section-label">What the shop builds</p>
              <h3>Stack arrangement and required fans</h3>
            </div>
            ${renderCopyLinkButton(sectionRoute("cooling-pack-layout"), "#", "Copy stack arrangement link")}
          </div>
          <div class="cooling-pack-band-grid">
            <article>
              <span class="cooling-pack-band-tag">One central air path</span>
              <p><strong>Exactly three fans: grille → two centred 248 mm Prado/GX donor electric pushers at 266 mm centres → 500 × 180 × 50 mm charge cooler with 57 mm outlets → ≥10 mm gap → 559 × 356 × 21 mm condenser → 15 mm target gap → HJ47-pattern recored/custom radiator with a 530 × 435 × 64 mm active-core thermal basis → sealed shroud → retained rear engine-driven mechanical puller.</strong></p>
            </article>
            <article>
              <span class="cooling-pack-band-tag">Simple factory-style appearance</span>
              <p><strong>One rectangular module, two equal centred black fan rings and no visible side annex.</strong> Drier remains upper/rear; the covered Relay Rev D box and closed, gasketed MIDI Rev D fuse enclosure use separate staggered local brackets and individual hoods, outside active airflow.</p>
            </article>
          </div>
          <div class="table-wrap cooling-pack-table-wrap">
            <table class="cooling-pack-table">
              <thead><tr><th>Component</th><th>Required baseline</th><th>Fan decision</th></tr></thead>
              <tbody>
                <tr><td><strong>Engine radiator</strong></td><td>HJ47/2H-pattern recored/custom copper/brass or equivalent. <strong>530 × 435 × 64 mm is active-core thermal basis only</strong> (0.231 m² gross face); it is not a complete radiator size or a fit claim. Record complete tank/seam/filler/drain/ear/locator envelope at R0 and use two direct side rails, short ears and lower saddles. It is <strong>not</strong> a Prado radiator. Thermal duty—not a claimed net-fin-area figure—controls acceptance: prove ≥115 kW continuous and ≥130 kW for 10 min with both upstream cores represented.</td><td>Fan 3 of 3: retain/rebuild the rear engine-driven puller with removable sealed full-face shroud; ≥9,000 m³/h installed through the complete stack at 1,500 rpm.</td></tr>
                <tr><td><strong>A/C condenser</strong></td><td>New common 14 × 22 in nominal, 559 × 356 × 21 mm R134a parallel-flow condenser on four independent rubber-isolated mounts; complete envelope must pass M1 ≥569 mm and M2/M3/M4.</td><td>Shares the centred twin-pusher module and rear mechanical puller; no separate condenser-only fan.</td></tr>
                <tr><td><strong>Turbo charge cooler</strong></td><td>One 500 × 180 × 50 mm slim horizontal core with 57 mm beaded outlets. ≥15 kW target; complete charge route ≤10 kPa drop.</td><td>Shares the same three baseline fans: two centred front electric pushers plus retained rear mechanical puller. No fourth/additional fan without a new controlled revision.</td></tr>
                <tr><td><strong>Cabin evaporator</strong></td><td>A/C installer to supply and verify.</td><td>Requires its cabin blower; outside radiator-shop metalwork.</td></tr>
              </tbody>
            </table>
          </div>
          <p class="cooling-pack-simple-rule"><strong>Simple rule:</strong> Har part apni bracket par, rubber ke saath, aur alag se nikal sakay. Core par koi load nahin.</p>
        </section>

        <section class="card cooling-pack-section" id="cooling-pack-standard-components">
          <div class="detail-header">
            <div>
              <p class="cooling-pack-section-label">Standard Toyota parts first</p>
              <h3>Use standard service parts where obtainable; custom-make only the measured interfaces</h3>
            </div>
            ${renderCopyLinkButton(sectionRoute("cooling-pack-standard-components"), "#", "Copy standard components link")}
          </div>
          <p class="small-muted"><strong>Important:</strong> “Toyota candidate” means bring the actual part to the vehicle, measure it and pass the listed gate. A part number is a starting point for sourcing, not permission to cut metal or to claim airflow.</p>
          <div class="table-wrap cooling-pack-table-wrap">
            <table class="cooling-pack-table">
              <thead><tr><th>System</th><th>Preferred standard component</th><th>Custom work and release condition</th></tr></thead>
              <tbody>
                <tr><td><strong>Radiator and hoses</strong></td><td>HJ47 / 2H radiator pattern <strong>16400-68030</strong> as a sample/source route; upper hose <strong>16571-68020</strong>; lower hose <strong>16572-68020</strong>; cap candidate <strong>16401-41021</strong>; Toyota-pattern constant-tension clamps. The 530 × 435 × 64 mm figure is active-core thermal basis only.</td><td>Record R0 before ordering: complete W × H × D including tanks, seams, filler, drain, ears and lower locators. Use a local recore/custom HJ47-pattern assembly or copied neck/hose adapter only if its complete envelope and duty pass B0/H0-L/H0-R/W0/P0/R0/BRKT. Do not substitute a Prado radiator. Verify actual neck centres, angles, cap seat and the 2H system's correct pressure before using the candidate cap; then prove hose fit, pressure drop and 115/130 kW thermal duty.</td></tr>
                <tr><td><strong>Front pusher pair</strong></td><td><strong>Donor scope only:</strong> matched Toyota Prado 120 / Lexus GX470 condenser-fan <strong>motors, blades and connectors</strong>: assembly references <strong>88590-60040 / -60050 / -60051 / -60060</strong>, motor <strong>88550-12160</strong>, blade <strong>88453-60010</strong>. Published-equivalent blade diameter 248 mm.</td><td>Reuse two equal motors, blades and plugs in <strong>one removable, sealed, symmetric custom shroud</strong>. Do not buy or fit a complete Prado/GX donor shroud as a direct replacement. Use ≥258 mm rings, 266 mm motor C-C and centres at W-active/2 ±133 mm at the same height. F3 must prove ≥3,000 m³/h installed through the final three-core stack at 13.5 V.</td></tr>
                <tr><td><strong>A/C condenser</strong></td><td>New common <strong>14 × 22 in nominal</strong> R134a parallel-flow condenser (559 × 356 × 21 mm basis), preferably common #8 inlet / #6 outlet O-ring ports.</td><td>Four isolated tabs and only the short adapters required by the measured hose route. Its actual body, seams, manifolds, ports, ears and service-tool envelope must fit and pass the 50°C A/C test.</td></tr>
                <tr><td><strong>Receiver-drier and A/C service parts</strong></td><td>New Toyota receiver-drier <strong>88471-34010</strong> <em>only if its ports fit</em>; otherwise new common serviceable #6 O-ring R134a drier with trinary-switch provision. Use new R134a barrier hose, HNBR seals, crimps, trinary switch and service ports.</td><td>Use one removable rubber-lined vertical clamp and short barrier-hose links. Never reuse a drier; the A/C technician must confirm ports/threads, switch set-points, evacuation, charge and pressures.</td></tr>
                <tr><td><strong>Electrical fan hardware</strong></td><td>Reuse Relay Rev D on its <strong>360 × 245 × 3 mm</strong> aluminium base with <strong>300 × 197 × 3 mm</strong> insulating sheet as a separate covered box. MIDI Rev D retains its <strong>210 × 165 × 65 mm</strong> enclosure, <strong>230 × 185 mm</strong> lid and 140 × 85 mm mounting plate; every MIDI fuse remains inside the closed, gasketed enclosure and its lid stays shut in normal operation. Keep two independently fused front-fan branches and Toyota/Denso/Sumitomo-compatible connectors.</td><td>Use two independent local structural brackets: one for Relay, one for MIDI, each with its own hood and service sweep. Keep both complete envelopes inside W0/the existing upright front-view silhouette and stagger vertically/depth-wise so MIDI's projected width nests wholly inside the Relay 360 mm envelope—never side-by-side across vehicle width. Route cable exits down/rear. Verify actual-current relay rating, voltage drop and branch isolation at E1; prove exact positions, both cover/lid sweeps, cable bends, drip shields, P-clips, disconnects and removal at E2/E2a before final loom work. No common plate; no formal IP rating is claimed unless purchased-rated or tested. Master cutoff stays battery-side.</td></tr>
                <tr><td><strong>Charge-air cooler and route</strong></td><td>If a Toyota/Denso 500 × 180 × 50 mm / 57 mm-outlet sample is physically in hand, trial it against the stated envelope and duty; otherwise source a commonly serviceable bar-and-plate core to the same envelope and duty. Pakistan stock for this exact size is unconfirmed, so the physical sample controls. Use common 57 mm (2.25 in) beaded tube, silicone couplers and T-bolt clamps.</td><td>Mount the core centrally ahead of the condenser. Turn the two short pipe routes rearward/inboard at measured lower corners. Make only independent tabs, sealing panels and measured bends; no side fan or side tower.</td></tr>
                <tr><td><strong>Fasteners and isolation</strong></td><td>Standard metric M6/M8 class 8.8 fasteners, large washers, locking nuts and EPDM isolators.</td><td>Two direct top ears/adapters, two lower saddles, twin-pusher shroud, rear shroud, two electrical brackets/hoods, simple air seals/stone screen and measured adapters are the custom-only items. No transverse radiator carrier and no heat-exchanger core carries another component.</td></tr>
              </tbody>
            </table>
          </div>
          <p class="cooling-pack-simple-rule"><strong>Karigar rule:</strong> Pehle standard part asli gaari par rakhain aur gate pass karein; phir sirf bracket, shroud, duct aur adapter banayen. Donor shroud ko zabardasti fit na karein.</p>
        </section>

        <section class="card cooling-pack-section" id="cooling-pack-purchase-list">
          <div class="detail-header">
            <div>
              <p class="cooling-pack-section-label">Rev G purchasing release</p>
              <h3>Buy standard Toyota donor parts in phases; release custom work from measurement</h3>
            </div>
            ${renderCopyLinkButton(sectionRoute("cooling-pack-purchase-list"), "#", "Copy cooling-pack purchase list link")}
          </div>
          <p class="small-muted"><strong>Purchasing rule:</strong> Prado 120/GX470 is the source route for two matched fan motors, blades and connectors only. It does not approve a Prado radiator, a complete donor shroud or any unmeasured direct fit. Record the actual donor vehicle, label, complete envelope and condition before payment.</p>
          <div class="table-wrap cooling-pack-table-wrap">
            <table class="cooling-pack-table">
              <thead><tr><th>Phase / status</th><th>Items to source</th><th>Release check before the next purchase</th></tr></thead>
              <tbody>
                ${purchasePhases.map((purchase) => `<tr><td><strong>${escapeHtml(purchase.phase)}</strong><br><span class="small-muted">${escapeHtml(purchase.status)}</span></td><td>${escapeHtml(purchase.items)}</td><td>${escapeHtml(purchase.release)}</td></tr>`).join("")}
              </tbody>
            </table>
          </div>
          <div class="cooling-pack-release-footer">
            <strong>Current purchasing status: sample/mock-up only.</strong>
            <span>Final radiator, final fan purchase, shroud/direct-ear/saddle drilling and coating remain HOLD until actual samples and the full-size dummy pass B0/H0-L/H0-R/W0/P0/R0/BRKT, M1–M6, F1/F2 and E2/E2a. Airflow and 50°C performance remain HOLD until F3/F4 and T1–T3 pass.</span>
          </div>
        </section>

        <section class="card cooling-pack-section" id="cooling-pack-diagrams">
          <div class="detail-header">
            <div>
              <p class="cooling-pack-section-label">Rev G drawing register · 1 Aug 2026</p>
              <h3>Complete dimensioned radiator and cooling-pack drawings</h3>
            </div>
            ${renderCopyLinkButton(sectionRoute("cooling-pack-diagrams"), "#", "Copy cooling-pack diagrams link")}
          </div>
          <div class="cooling-pack-drawing-notes" role="note">
            <span><b class="drawing-key drawing-key-fixed"></b><strong>Red</strong> = fixed nominal requirement.</span>
            <span><b class="drawing-key drawing-key-measure"></b><strong>Purple</strong> = measure on vehicle / written approval.</span>
            <span>All unlabeled positions are field-measured. Dimensions are in millimetres. <strong>Final core manufacture: HOLD.</strong></span>
          </div>
          <p class="small-muted">D10 is the procurement/fit-control drawing. Click any drawing to inspect it full size. Deterministic Rev G drawings, the full-size vehicle mock-up and written approval control final core manufacture; AI visuals do not.</p>
          <div class="cooling-pack-gallery">${renderGallery(diagrams)}</div>
        </section>

        <section class="cooling-pack-spec-grid" id="cooling-pack-specifications">
          <article class="card cooling-pack-spec-card">
            <p class="cooling-pack-section-label">Main-pack airflow</p>
            <h3>Installed airflow—not free-air marketing</h3>
            <ul>
              <li>Mechanical puller + sealed full-face shroud: ≥9,000 m³/h installed through all three cores at 1,500 engine rpm.</li>
              <li>Fans 1 and 2 of 3: a matched 248 mm Prado 120/GX470 Toyota/Denso donor motor, blade and connector pair in one custom sealed shroud with ≥258 mm clear rings. Put both centres at the same height and at W-active/2 ±133 mm (266 mm C-C), giving equal left/right fin bands. The complete donor shroud is not a fit-approved part. Installed duty is ≥3,000 m³/h at 13.5 V through the final grille, screen and all three cores.</li>
              <li>Any visual or physical offset needs a measured obstruction and approved coverage evidence. Wiring convenience is not a reason to move the fans off-centre.</li>
              <li>Record make, model, installed test basis, steady current, start current and loaded voltage for every fan.</li>
              <li>No component may obscure the main core or be supported by another heat exchanger.</li>
            </ul>
          </article>
          <article class="card cooling-pack-spec-card">
            <p class="cooling-pack-section-label">Central charge-cooler layer</p>
            <h3>One slim core; no third electric fan</h3>
            <ul>
              <li>≥15 kW heat rejection at 50°C fresh inlet, 0.20 kg/s charge flow and 130°C nominal compressor outlet.</li>
              <li>Manifold IAT ≤80°C at stabilised rated full load; pressure-test to ≥2× declared boost, minimum 30 psi.</li>
              <li>The central twin pushers and rear mechanical puller serve this core, condenser and radiator together: exactly three fans total. No fourth/additional fan is permitted unless a new controlled revision approves the packaging change.</li>
              <li>Nominal core basis is 500 W × 180 H × 50 D with 57 mm beaded outlets, but the physical sample and complete three-core dummy control.</li>
              <li>Keep both tanks/outlets between the uprights, turn the pipes rearward/inboard at measured lower corners, and seal edge bypass.</li>
            </ul>
          </article>
          <article class="card cooling-pack-spec-card">
            <p class="cooling-pack-section-label">Mechanical fan and shroud</p>
            <h3>Retain the engine-driven puller</h3>
            <ul>
              <li>Reject cracked, welded, loose, distorted or contact-marked blades.</li>
              <li>Full-face rigid removable shroud, sealed around radiator perimeter.</li>
              <li>Blade depth 35–50% inside the shroud opening; perimeter seals must force air through the radiator.</li>
              <li>At least 15 radial clearance through checked engine movement.</li>
              <li>Radiator rear face to nearest blade ≥20 static; 25–30 preferred.</li>
            </ul>
          </article>
          <article class="card cooling-pack-spec-card cooling-pack-never-card">
            <p class="cooling-pack-section-label">Turbo and release boundary</p>
            <h3>No cooling derate—but no blank cheque for boost</h3>
            <ul>
              <li>After T1–T3 pass, the cooling system must not require boost reduction within the 150 bhp crank thermal-design envelope.</li>
              <li>Initial calibration stays at 5–7 psi. Consider 8–10 psi only after logged coolant, IAT, EGT, oil, smoke, boost and driveline evidence.</li>
              <li>This cooling specification does not approve 150 bhp, arbitrary boost, fuelling, turbo speed, exhaust drive pressure, clutch or driveline capacity.</li>
            </ul>
          </article>
          <article class="card cooling-pack-spec-card cooling-pack-never-card">
            <p class="cooling-pack-section-label">Never do this</p>
            <h3>Core and mounting prohibitions</h3>
            <ul>
              <li>No drilling or welding into a tank, header, tube, core or fin.</li>
              <li>No plastic ties through any heat-exchanger core.</li>
              <li>No component or fan carried by another heat exchanger.</li>
              <li>No electrical enclosure or plate on the radiator, its isolated mounts or the battery stand; the covered Relay Rev D box and closed MIDI fuse enclosure use two independent staggered local structural brackets with their own hoods, outside active fin/sealed airflow.</li>
              <li>No guessed neck positions, cap pressure, port threads or fan current.</li>
              <li>No forced bolt alignment; every component must remove separately without cutting.</li>
              <li>No new chassis holes, slots or reaming in the two existing inward top-return holes; drill only the two short removable radiator ears/adapters after template transfer. No transverse radiator carrier.</li>
            </ul>
          </article>
        </section>

        <section class="card cooling-pack-section" id="cooling-pack-gates">
          <div class="detail-header">
            <div>
              <p class="cooling-pack-section-label">Release control</p>
              <h3>Mandatory measurements before final manufacture</h3>
            </div>
            ${renderCopyLinkButton(sectionRoute("cooling-pack-gates"), "#", "Copy mandatory fit gates link")}
          </div>
          <p class="small-muted">Measure with both uprights represented, body settled, grille/front panel and bonnet latch installed or accurately represented, and the engine fan present. Put a tape or ruler in every evidence photo.</p>
          <div class="table-wrap cooling-pack-table-wrap">
            <table class="cooling-pack-table cooling-pack-gate-table">
              <thead><tr><th>ID</th><th>Check</th><th>PASS requirement</th></tr></thead>
              <tbody>
                ${fitGates.map(([id, check, requirement]) => `<tr><td><strong>${escapeHtml(id)}</strong></td><td>${escapeHtml(check)}</td><td>${escapeHtml(requirement)}</td></tr>`).join("")}
              </tbody>
            </table>
          </div>
          <div class="cooling-pack-release-footer">
            <strong>Do not order final cores from these nominal dimensions alone.</strong>
            <span>Pass B0/H0-L/H0-R/W0/P0/R0/BRKT, M1 ≥569 mm, M2–M6, F1–F4 and E1–E2a; build the full-size three-core dummy with its two direct radiator side rails/ears/lower saddles and two independent electrical brackets to the 215 mm stack basis; prove the 225 mm preferred installed-clearance envelope where available; close the bonnet/grille/bumper; prove removal paths, ≥5 mm hard rail/post clearance and both hand-entering top bolts; then pass T1–T3 before claiming 50°C / no-cooling-derate performance.</span>
          </div>
        </section>

        <section class="card cooling-pack-section cooling-pack-files" id="cooling-pack-files">
          <div class="detail-header">
            <div>
              <p class="cooling-pack-section-label">Controlled handoff</p>
              <h3>Download the controlled cooling-pack specification</h3>
            </div>
            ${renderCopyLinkButton(sectionRoute("cooling-pack-files"), "#", "Copy cooling-pack downloads link")}
          </div>
          <p>The Word document is the fabricator handoff: complete construction rules, dimensions, tests, sequence, acceptance checks and a sign-off sheet. Print it or send it directly to the radiator shop.</p>
          <div class="cooling-pack-downloads">
            <a class="item-link package-download-link cooling-pack-download" href="../../docs/J40-integrated-cooling-pack-fabricator-specification-rev-c.docx" download>Download shop specification (.docx)</a>
            <a class="item-link cooling-pack-download" href="../../docs/J40-integrated-cooling-pack-fabricator-specification-rev-c.md" download>Download source specification (.md)</a>
          </div>
        </section>
      </div>
    `;
  }

  function renderTurboBuild() {
    const buildStages = [
      ["01", "Record the as-fitted baseline", "Confirm and photograph the 2H identity, engine number, injection-pump tag, oil-filter housing, sump, manifolds, engine mounts, steering, A/C and bonnet structure. Record a no-boost road baseline for smoke, coolant temperature and oil pressure."],
      ["02", "Pass the engine-health gate", "Warm the engine fully. Record all six compression readings, hot oil pressure at idle and test rpm, measured blow-by, cooling-system pressure/flow, injector pattern and pump condition. Stop for a weak cylinder, low oil pressure, heavy blow-by, overheating, injector dribble or unresolved smoke."],
      ["03", "Freeze the available package", "Reserve the 2H-specific low-mount CT26-flange manifold and the CT26-pattern TD05H 16G with 7 cm² / .49 A/R turbine housing and internal wastegate. Verify the actual supplied flange, wheel specification, actuator pressure, oil ports, coolant ports, clocking range and genuine serial/part markings before payment."],
      ["04", "Establish steering and body datums", "Fit or hard-mock the final J60 hydraulic steering box, shaft, pump and hoses. Fit the engine on final mounts, refit wings and bonnet, and mark the bonnet inner-brace envelope. Turbo packaging follows these fixed datums."],
      ["05", "Mock the complete hot side", "Bolt the low-mount manifold and turbo together using temporary hardware. Add the wastegate actuator, compressor elbow, proposed downpipe first bend and removable air-gap heat shield. Clock the housings without loading the centre housing or actuator linkage."],
      ["06", "Prove clearance before fabrication", "Close the bonnet gently over clay markers. Prove approximately 25 mm minimum static clearance after heat shielding, plus engine-roll allowance. Check wing, steering, A/C, starter, oil filter, wiring, brake/clutch/fuel lines and tool access. Relocate the round air cleaner; do not cut the bonnet until every lower-position alternative has failed."],
      ["07", "Build lubrication and optional coolant routes", "Measure the selected oil-gallery source and follow the turbo supplier's feed/restrictor requirement. Build a large-bore gravity drain with continuous fall into a sump bung above normal oil level; remove and clean the sump for welding. Plumb coolant only if the exact centre housing requires it, without creating an air trap."],
      ["08", "Fabricate exhaust and thermal protection", "Build a supported downpipe with a smooth first bend, serviceable joint and flex provision, then the low-restriction single exhaust. Support the exhaust independently of the turbo. Shield the manifold, turbine and downpipe from hydraulics, fuel, wiring, A/C, intake ducting, bonnet and paint."],
      ["09", "Build clean-air and charge-air systems", "Replace or relocate the round air cleaner with a sealed serviceable unit. Use collapse-resistant compressor-inlet ducting. Route beaded charge pipe through the specified intercooler to the intake, using reinforced couplers, proper clamps, supports and flexible engine-movement joints. Retain a low-restriction crankcase breather/separator."],
      ["10", "Install monitoring before fuelling", "Fit calibrated pre-turbine EGT, low-range boost, engine oil-pressure and coolant-temperature instruments with visible alarms. Use a fused labelled supply, correct thermocouple extension wire, clean grounds and protected sender routing. Retain factory warning functions where practical."],
      ["11", "Prime, leak-test and heat-cycle", "Leave fuel at the baseline setting. Disable starting and crank until turbo oil return is proven, then reconnect and idle. Check oil, coolant, exhaust and charge-air leaks; pressure-test the charge route. Complete several heat cycles, re-torque only where specified, inspect witness marks and confirm the wastegate moves freely."],
      ["12", "Commission at 5–7 psi", "Verify mechanical boost control and progressively load the engine while logging boost, pre-turbine EGT, coolant temperature, hot oil pressure and smoke. Permit diesel-specialist fuelling changes only after stable baseline logs. Stop immediately for unstable boost, smoke, EGT/coolant rise, oil-pressure loss, leaks, contact or clutch slip. Treat 8–10 psi as a later evidence-gated decision, not the initial tune."],
    ];
    const bomRows = [
      ["Core package", "2H low-mount CT26-flange manifold; CT26-pattern TD05H 16G, 7 cm² / .49 A/R, internal wastegate", "Assumed available; inspect exact supplied unit"],
      ["Mounting", "Correct studs, locking hardware, heat-rated gaskets and supported downpipe", "Select after flange inspection and mock-up"],
      ["Lubrication", "Measured oil take-off, supplier-compliant feed/restrictor, large gravity drain, sump bung", "No universal restrictor; no drain below oil level"],
      ["Cooling", "Turbo coolant hoses/fittings only if exact centre housing requires them", "Do not disturb heater or create air traps"],
      ["Air system", "Remote sealed air cleaner, inlet duct, intercooler, 2.0–2.5 in working-basis charge pipe, beaded ends, reinforced couplers", "Final diameter and routing follow mock-up"],
      ["Exhaust/heat", "Downpipe, flex provision, single exhaust, independent hangers, removable air-gap shields", "Keep all safety systems outside the heat envelope"],
      ["Controls", "Wastegate reference hose; calibrated EGT, boost, oil-pressure and coolant-temperature instruments", "Installed and tested before fuel adjustment"],
      ["Commissioning", "Fresh oil/filter, coolant, leak-test plugs, torque paint and written test sheets", "Log every staged loaded run"],
    ];
    const gates = [
      ["G1", "Engine health", "Six-cylinder compression, hot oil pressure, blow-by, cooling, injectors and pump accepted"],
      ["G2", "Goods receipt", "Supplied manifold/turbo identity, CT26 pattern, 16G wheel, 7 cm² housing, actuator and ports verified"],
      ["G3", "Vehicle mock-up", "Steering fitted; drain falls continuously; service access retained; no safety-system conflict"],
      ["G4", "Bonnet clearance", "Bonnet closes over complete shielded assembly with ~25 mm static clearance and engine-roll allowance"],
      ["G5", "Static integrity", "Oil/coolant/charge/exhaust leak tests pass; wastegate, gauges and alarms function"],
      ["G6", "5–7 psi road release", "Stable logged boost, EGT, coolant and oil pressure; acceptable smoke; no leaks, contact or clutch slip"],
    ];

    root.innerHTML = `
      <div class="cooling-pack-view turbo-build-view">
        <section class="cooling-pack-hero turbo-build-hero" id="turbo-build-summary">
          <div class="cooling-pack-hero-copy">
            <div class="cooling-pack-kicker-row">
              <p class="eyebrow">2H low-mount turbo · controlled build release</p>
              ${renderCopyLinkButton(sectionRoute("turbo-build-summary"), "#", "Copy turbo-build summary link")}
            </div>
            <h2>A specific package is now assumed available. Vehicle fit still has to be proved.</h2>
            <p class="cooling-pack-lead">Proceed on the basis of a <strong>2H-specific low-mount CT26-flange manifold</strong> paired with a <strong>CT26-pattern TD05H 16G, 7 cm² / .49 A/R, internally wastegated turbo</strong>. The manifold-to-head and turbo-to-manifold interfaces are the controlled direction; the converted J40 installation remains mock-up first.</p>
            <div class="cooling-pack-release">
              <span class="turbo-build-release">PACKAGE DIRECTION: RELEASED</span>
              <span>Purchase only after exact goods-receipt inspection. Permanent fabrication waits for engine-health and vehicle-clearance gates.</span>
            </div>
            <blockquote>Bonnet cutting is not planned. Use the low mount, relocate the large round air cleaner, and change clocking or pipe routes before considering body alteration.</blockquote>
            <div class="cooling-pack-downloads">
              <a class="item-link package-download-link cooling-pack-download" href="../../docs/2h-turbo-recommended-build-process-20260801.md" download>Download detailed build process (.md)</a>
              <a class="item-link cooling-pack-download" href="../../docs/2h-turbo-suitability-and-options-20260717.md" download>Download engineering basis (.md)</a>
            </div>
          </div>
          <dl class="cooling-pack-facts" aria-label="Turbo package summary">
            <div><dt>Engine</dt><dd>Toyota 2H</dd><span>4.0 L naturally aspirated base engine</span></div>
            <div><dt>Turbo</dt><dd>TD05H 16G</dd><span>CT26 pattern · 7 cm² / .49 A/R</span></div>
            <div><dt>Layout</dt><dd>Low mount</dd><span>Bonnet modification not planned</span></div>
            <div><dt>Initial boost</dt><dd>5–7 psi</dd><span>Baseline fuel until monitored proof</span></div>
          </dl>
        </section>

        <section class="card cooling-pack-section cooling-pack-start-here" id="turbo-build-decision">
          <div class="detail-header"><div><p class="cooling-pack-section-label">What is fixed and what is not</p><h3>Release boundary</h3></div>${renderCopyLinkButton(sectionRoute("turbo-build-decision"), "#", "Copy release-boundary link")}</div>
          <div class="turbo-build-decision-grid">
            <article><span class="turbo-build-status is-fixed">Assumed available</span><h4>Matched physical interfaces</h4><p>2H low-mount head flange, CT26 four-bolt turbo flange, compact internally wastegated TD05H 16G/7 cm² direction.</p></article>
            <article><span class="turbo-build-status is-prove">Must be proved</span><h4>As-fitted vehicle clearance</h4><p>Steering, bonnet brace, wing, air cleaner, A/C, downpipe, oil drain, heat shields, engine movement and service access.</p></article>
            <article><span class="turbo-build-status is-hold">Still held</span><h4>Final tune and higher boost</h4><p>Fuelling, exact alarm limits and any 8–10 psi decision remain conditional on health tests and logged commissioning.</p></article>
          </div>
        </section>

        <section class="card cooling-pack-section" id="turbo-build-bom">
          <div class="detail-header"><div><p class="cooling-pack-section-label">Procurement and fabrication scope</p><h3>Complete working bill of materials</h3></div>${renderCopyLinkButton(sectionRoute("turbo-build-bom"), "#", "Copy turbo BOM link")}</div>
          <div class="table-wrap cooling-pack-table-wrap"><table class="cooling-pack-table"><thead><tr><th>System</th><th>Required scope</th><th>Release note</th></tr></thead><tbody>${bomRows.map((row) => `<tr>${row.map((cell) => `<td>${cell}</td>`).join("")}</tr>`).join("")}</tbody></table></div>
        </section>

        <section class="card cooling-pack-section" id="turbo-build-process">
          <div class="detail-header"><div><p class="cooling-pack-section-label">Workshop sequence · do not reorder gates</p><h3>Detailed build process</h3></div>${renderCopyLinkButton(sectionRoute("turbo-build-process"), "#", "Copy turbo build-process link")}</div>
          <ol class="turbo-build-steps">${buildStages.map(([number, title, detail]) => `<li><span class="turbo-build-step-number">${number}</span><div><h4>${title}</h4><p>${detail}</p></div></li>`).join("")}</ol>
        </section>

        <section class="card cooling-pack-section" id="turbo-build-bonnet">
          <div class="detail-header"><div><p class="cooling-pack-section-label">Body preservation rule</p><h3>Bonnet and engine-bay clearance procedure</h3></div>${renderCopyLinkButton(sectionRoute("turbo-build-bonnet"), "#", "Copy bonnet-clearance link")}</div>
          <div class="cooling-pack-band-grid">
            <article><span class="cooling-pack-band-tag">Expected change</span><p>Remove or relocate the present large round air cleaner and build a sealed remote-filter inlet. Re-clock the compressor and re-route charge pipe as required.</p></article>
            <article><span class="cooling-pack-band-tag">Not expected</span><p>No bonnet scoop, bulge or cut-out is approved. A high-mount manifold is outside this build direction.</p></article>
          </div>
          <div class="cooling-pack-start-rule"><strong>Physical check:</strong><span>Fit the complete turbo, actuator, elbows and final heat-shield thickness. Place clay cones at the highest points, close the bonnet gently, measure the compressed clay, then check engine roll within the mount envelope. Record photographs and the minimum clearance.</span></div>
        </section>

        <section class="card cooling-pack-section" id="turbo-build-gates">
          <div class="detail-header"><div><p class="cooling-pack-section-label">Mandatory sign-off</p><h3>Six release gates</h3></div>${renderCopyLinkButton(sectionRoute("turbo-build-gates"), "#", "Copy turbo release-gates link")}</div>
          <div class="table-wrap cooling-pack-table-wrap"><table class="cooling-pack-table cooling-pack-gate-table"><thead><tr><th>Gate</th><th>Decision</th><th>Pass evidence</th></tr></thead><tbody>${gates.map((row) => `<tr>${row.map((cell) => `<td>${cell}</td>`).join("")}</tr>`).join("")}</tbody></table></div>
          <div class="cooling-pack-release-footer"><strong>No skipped gates.</strong><span>Availability releases the candidate package for inspection; it does not release blind installation, fuelling changes or bonnet modification.</span></div>
        </section>
      </div>`;
  }

  function renderOtherBuilds() {
    const otherBuilds = data.other_builds || {};
    const summary = otherBuilds.summary || {};
    const sections = Array.isArray(otherBuilds.sections) ? otherBuilds.sections : [];
    const referenceIdeas = Array.isArray(data.reference_project_ideas) ? data.reference_project_ideas : [];
    const contacts = Array.isArray(data.contact_register) ? data.contact_register : [];
    const totalMedia = summary.total_media ?? summary.total_images ?? 0;
    const dropZoneMedia = summary.drop_zone_media ?? summary.drop_zone_images ?? 0;
    const manualReferenceMedia = summary.manual_reference_media ?? summary.manual_reference_images ?? 0;
    root.innerHTML = `
      <h2 class="section-title">Other Builds</h2>
      <p class="section-subtitle">Outside-build references, including the Islamabad FJ restorations, Akbar wiring/floor caution examples, archived listings, and curated WhatsApp sample media.</p>

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
        <article class="card">
          <p class="metric-value">${escapeHtml(referenceIdeas.length)}</p>
          <p class="metric-label">Reference Ideas</p>
        </article>
        <article class="card">
          <p class="metric-value">${escapeHtml(contacts.length)}</p>
          <p class="metric-label">Useful Contacts</p>
        </article>
      </section>

      ${renderOtherBuildFocusCards(sections)}

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

      <section class="card reference-drop-card">
        <div class="detail-header">
          <h3>Reference Media Drop Zone</h3>
          ${chip(dropZoneMedia ? `${dropZoneMedia} media` : "Empty")}
        </div>
        <p class="small-muted"><code>${escapeHtml(otherBuilds.drop_zone || "data/reference/other_j40_builds")}</code></p>
      </section>

      ${renderReferenceProjectIdeas(referenceIdeas)}
      ${renderContactRegister(contacts)}
    `;
  }

  function createVisualViewer() {
    const wrapper = document.createElement("div");
    wrapper.className = "lightbox visual-viewer is-hidden";
    wrapper.setAttribute("aria-hidden", "true");
    wrapper.innerHTML = `
      <div class="lightbox-backdrop" data-visual-viewer-close="1"></div>
      <section class="visual-viewer-panel" role="dialog" aria-modal="true" aria-label="3D visualisation viewer">
        <button type="button" class="lightbox-close" data-visual-viewer-close="1" aria-label="Close 3D viewer">×</button>
        <div class="visual-viewer-frame-wrap">
          <button type="button" class="lightbox-nav-btn lightbox-nav-prev" id="visual-viewer-prev" title="Previous 3D view" aria-label="Previous 3D view">&lsaquo;</button>
          <button type="button" class="lightbox-nav-btn lightbox-nav-next" id="visual-viewer-next" title="Next 3D view" aria-label="Next 3D view">&rsaquo;</button>
          <iframe id="visual-viewer-frame" title="3D visualisation"></iframe>
        </div>
        <aside class="visual-viewer-sidebar">
          <h3 id="visual-viewer-title" class="section-title" style="margin-top:0;">3D Visualisation</h3>
          <p id="visual-viewer-subtitle" class="small-muted"></p>
          <dl id="visual-viewer-meta" class="meta-grid"></dl>
          <div class="item-detail-links">
            <a class="item-link" id="visual-viewer-open-original" href="#" target="_blank" rel="noopener noreferrer">Open Full Page</a>
            <a class="item-link" id="visual-viewer-open-static" href="#" target="_blank" rel="noopener noreferrer">Open Static SVG</a>
          </div>
          <p id="visual-viewer-notes" class="small-muted"></p>
        </aside>
      </section>
    `;
    document.body.appendChild(wrapper);
    const refs = {
      root: wrapper,
      frame: wrapper.querySelector("#visual-viewer-frame"),
      prevBtn: wrapper.querySelector("#visual-viewer-prev"),
      nextBtn: wrapper.querySelector("#visual-viewer-next"),
      title: wrapper.querySelector("#visual-viewer-title"),
      subtitle: wrapper.querySelector("#visual-viewer-subtitle"),
      meta: wrapper.querySelector("#visual-viewer-meta"),
      openOriginalLink: wrapper.querySelector("#visual-viewer-open-original"),
      openStaticLink: wrapper.querySelector("#visual-viewer-open-static"),
      notes: wrapper.querySelector("#visual-viewer-notes"),
    };
    wrapper.addEventListener("click", (event) => {
      if (event.target.closest("[data-visual-viewer-close]")) {
        closeVisualViewer();
      }
    });
    refs.prevBtn.addEventListener("click", () => navigateVisualViewer(-1));
    refs.nextBtn.addEventListener("click", () => navigateVisualViewer(1));
    return refs;
  }

  function visualViewerKeys() {
    const sequenceId = visualSequenceByKey.get(state.visualViewerKey);
    const sequenceKeys = sequenceId ? visualSequences.get(sequenceId) || [] : [];
    return sequenceKeys.length ? sequenceKeys : Array.from(visualRegistry.keys());
  }

  function currentVisualViewerIndex() {
    return visualViewerKeys().indexOf(state.visualViewerKey);
  }

  function updateVisualViewerNavigation() {
    const keys = visualViewerKeys();
    const index = currentVisualViewerIndex();
    const hasNavigation = keys.length > 1 && index >= 0;
    if (visualViewer.prevBtn) {
      visualViewer.prevBtn.disabled = !hasNavigation;
    }
    if (visualViewer.nextBtn) {
      visualViewer.nextBtn.disabled = !hasNavigation;
    }
  }

  function navigateVisualViewer(direction) {
    const keys = visualViewerKeys();
    if (!state.visualViewerKey || keys.length < 2) {
      return;
    }
    const index = currentVisualViewerIndex();
    if (index < 0) {
      return;
    }
    const nextIndex = (index + direction + keys.length) % keys.length;
    openVisualViewer(keys[nextIndex]);
  }

  function renderVisualViewer() {
    const item = visualRegistry.get(state.visualViewerKey);
    if (!item) {
      return;
    }
    updateVisualViewerNavigation();
    visualViewer.title.textContent = item.title || "3D Visualisation";
    visualViewer.subtitle.textContent = [item.packageId, item.label].filter(Boolean).join(" · ");
    visualViewer.frame.setAttribute("title", item.title || "3D visualisation");
    visualViewer.frame.setAttribute("src", item.embedUrl || item.url || "about:blank");
    visualViewer.openOriginalLink.setAttribute("href", item.url || "#");
    visualViewer.openStaticLink.setAttribute("href", item.staticUrl || item.url || "#");
    visualViewer.openStaticLink.classList.toggle("is-disabled", !cleanString(item.staticUrl));
    visualViewer.meta.innerHTML = `
      <dt>Package</dt><dd>${escapeHtml(item.packageId || "-")}</dd>
      <dt>View</dt><dd>${escapeHtml(item.label || "-")}</dd>
      <dt>Mode</dt><dd>${escapeHtml(item.modeKey === "assembled" ? "Attached / installed" : item.modeKey === "expanded" ? "Expanded / fabrication read" : "3D view")}</dd>
    `;
    visualViewer.notes.textContent = cleanString(item.notes) ? `Release: ${cleanString(item.notes)}` : "";
  }

  function openVisualViewer(visualKey) {
    if (!visualRegistry.has(visualKey)) {
      return;
    }
    if (state.lightboxImageBase) {
      closeLightbox();
    }
    if (state.itemDetailRow) {
      closeItemDetail();
    }
    state.visualViewerKey = visualKey;
    renderVisualViewer();
    visualViewer.root.classList.remove("is-hidden");
    visualViewer.root.setAttribute("aria-hidden", "false");
    document.body.classList.add("lightbox-open");
  }

  function closeVisualViewer() {
    state.visualViewerKey = "";
    visualViewer.frame.setAttribute("src", "about:blank");
    visualViewer.root.classList.add("is-hidden");
    visualViewer.root.setAttribute("aria-hidden", "true");
    document.body.classList.remove("lightbox-open");
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
    openItemDetailRow(row, { updateRoute: true });
  }

  function closeItemDetail() {
    state.itemDetailRow = null;
    state.pendingItemId = "";
    itemDetail.root.classList.add("is-hidden");
    itemDetail.root.setAttribute("aria-hidden", "true");
    itemDetail.media.innerHTML = "";
    itemDetail.links.innerHTML = "";
    document.body.classList.remove("lightbox-open");
    if (window.location.hash.includes("/item/")) {
      updateRouteHash();
    }
  }

  function openItemDetailRow(row, options = {}) {
    if (!row) {
      return false;
    }
    if (state.visualViewerKey) {
      closeVisualViewer();
    }
    if (state.lightboxImageBase) {
      closeLightbox();
    }
    state.itemDetailRow = row;
    renderItemDetail();
    itemDetail.root.classList.remove("is-hidden");
    itemDetail.root.setAttribute("aria-hidden", "false");
    document.body.classList.add("lightbox-open");
    if (options.updateRoute) {
      const itemId = row.__item_stable_id || stableItemId(row);
      if (itemId) {
        updateRouteHash(["item", itemId]);
      }
    }
    return true;
  }

  function openItemDetailByStableId(itemId) {
    const stableId = cleanString(itemId);
    if (!stableId) {
      return false;
    }
    return openItemDetailRow(itemRegistryByStableId.get(stableId), { updateRoute: false });
  }

  function enhanceDeepLinkTargets() {
    const usedIds = new Set();
    const headings = Array.from(root.querySelectorAll(".section-title, .card > h3, .card > h4, .detail-header > h2, .detail-header > h3, .detail-header > h4"));
    headings.forEach((heading) => {
      if (!heading || heading.closest(".lightbox") || heading.querySelector(".copy-link-btn")) {
        return;
      }
      const target = heading.closest(".card, section, article") || heading;
      let baseId = cleanString(target.id || heading.id);
      if (!baseId) {
        baseId = `section-${slugify(heading.textContent || "section")}`;
      }
      let sectionId = baseId;
      let suffix = 2;
      while (usedIds.has(sectionId)) {
        sectionId = `${baseId}-${suffix}`;
        suffix += 1;
      }
      usedIds.add(sectionId);
      target.id = sectionId;
      target.classList.add("deep-link-target");
      heading.appendChild(document.createTextNode(" "));
      const wrapper = document.createElement("span");
      wrapper.innerHTML = renderCopyLinkButton(sectionRoute(sectionId), "#", "Copy direct section link");
      const button = wrapper.firstElementChild;
      if (button) {
        heading.appendChild(button);
      }
    });
  }

  function focusDeepLinkTarget(node) {
    if (!node) {
      return;
    }
    node.scrollIntoView({ behavior: "smooth", block: "start" });
    node.classList.add("is-deep-linked");
    window.setTimeout(() => {
      node.classList.remove("is-deep-linked");
    }, 1800);
  }

  function handlePendingRouteAfterRender() {
    enhanceDeepLinkTargets();
    window.requestAnimationFrame(() => {
      if (state.pendingSectionId) {
        const target = document.getElementById(state.pendingSectionId);
        if (target) {
          focusDeepLinkTarget(target);
          state.pendingSectionId = "";
        }
      }
      if (state.pendingItemId && openItemDetailByStableId(state.pendingItemId)) {
        state.pendingItemId = "";
      }
    });
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
            <span class="lightbox-nav-status" id="lightbox-nav-status"></span>
          </div>
          <button type="button" class="lightbox-nav-btn lightbox-nav-prev" id="lightbox-prev-image" title="Previous image" aria-label="Previous image">&lsaquo;</button>
          <button type="button" class="lightbox-nav-btn lightbox-nav-next" id="lightbox-next-image" title="Next image" aria-label="Next image">&rsaquo;</button>
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
      navStatus: wrapper.querySelector("#lightbox-nav-status"),
      prevImageBtn: wrapper.querySelector("#lightbox-prev-image"),
      nextImageBtn: wrapper.querySelector("#lightbox-next-image"),
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
    refs.prevImageBtn.addEventListener("click", () => navigateLightbox(-1));
    refs.nextImageBtn.addEventListener("click", () => navigateLightbox(1));

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
        event.target.closest(".lightbox-toolbar, .lightbox-nav-btn")
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

  function lightboxImageKeys() {
    const sequenceId = imageSequenceByKey.get(state.lightboxImageKey);
    const sequenceKeys = sequenceId ? imageSequences.get(sequenceId) || [] : [];
    return sequenceKeys.length ? sequenceKeys : Array.from(imageRegistry.keys());
  }

  function currentLightboxImageIndex() {
    const keys = lightboxImageKeys();
    return keys.indexOf(state.lightboxImageKey);
  }

  function updateLightboxNavigationControls() {
    const keys = lightboxImageKeys();
    const index = currentLightboxImageIndex();
    const count = keys.length;
    const hasNavigation = count > 1 && index >= 0;

    if (lightbox.prevImageBtn) {
      lightbox.prevImageBtn.disabled = !hasNavigation;
    }
    if (lightbox.nextImageBtn) {
      lightbox.nextImageBtn.disabled = !hasNavigation;
    }
    if (lightbox.navStatus) {
      lightbox.navStatus.textContent = hasNavigation ? `${index + 1} / ${count}` : "";
    }
  }

  function navigateLightbox(direction) {
    const keys = lightboxImageKeys();
    if (!state.lightboxImageBase || keys.length < 2) {
      return;
    }

    const index = currentLightboxImageIndex();
    if (index < 0) {
      return;
    }

    const nextIndex = (index + direction + keys.length) % keys.length;
    openLightbox(keys[nextIndex]);
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
    updateLightboxNavigationControls();
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
    updateLightboxNavigationControls();
  }

  function openLightbox(imageKey) {
    const baseMeta = imageRegistry.get(imageKey);
    if (!baseMeta) {
      return;
    }
    if (state.visualViewerKey) {
      closeVisualViewer();
    }
    if (state.itemDetailRow) {
      closeItemDetail();
    }
    state.lightboxImageBase = baseMeta;
    state.lightboxImageKey = imageKey;
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
    state.lightboxImageKey = "";
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
    resetVisualRegistry();
    resetItemRegistry();
    let renderer = renderOverview;
    if (state.activeView === "workstreams") {
      renderer = renderWorkstreams;
    } else if (state.activeView === "status-update") {
      renderer = renderStatusUpdate;
    } else if (state.activeView === "vehicle-map") {
      renderer = renderVehicleMap;
    } else if (state.activeView === "parts") {
      renderer = renderParts;
    } else if (state.activeView === "scout") {
      renderer = renderScout;
    } else if (state.activeView === "tasks") {
      renderer = renderCaptureTasks;
    } else if (state.activeView === "amir") {
      renderer = renderAmir;
    } else if (state.activeView === "images") {
      renderer = renderImages;
    } else if (state.activeView === "photos-needed") {
      renderer = renderPhotosNeeded;
    } else if (state.activeView === "cooling-pack") {
      renderer = renderCoolingPack;
    } else if (state.activeView === "turbo-build") {
      renderer = renderTurboBuild;
    } else if (state.activeView === "other-builds") {
      renderer = renderOtherBuilds;
    }
    renderer();
    handlePendingRouteAfterRender();
  }

  applyRouteFromHash();
  render();
})();
