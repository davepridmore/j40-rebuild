from __future__ import annotations

import argparse
import csv
import json
import mimetypes
import re
import time
import webbrowser
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import requests
import google.auth
from google.auth.transport.requests import AuthorizedSession, Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


ROOT = Path(__file__).resolve().parent.parent
PHOTOS_DIR = ROOT / "photos"
RAW_IMPORTS_DIR = ROOT / "data" / "raw" / "imports" / "google_photos"
DEFAULT_TOKEN_PATH = RAW_IMPORTS_DIR / "token_photospicker.json"
DEFAULT_HISTORY_PATH = RAW_IMPORTS_DIR / "import_history.csv"

PHOTO_PICKER_SCOPE = "https://www.googleapis.com/auth/photospicker.mediaitems.readonly"
PHOTO_PICKER_API = "https://photospicker.googleapis.com/v1"


@dataclass(frozen=True)
class PickedItem:
    media_item_id: str
    create_time: str
    mime_type: str
    source_filename: str
    base_url: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Import selected Google Photos media into the J40 archive and write import manifests."
    )
    parser.add_argument(
        "--auth-mode",
        choices=("oauth-client", "adc"),
        default="oauth-client",
        help="Authentication source: oauth-client (client secret + token file) or adc (gcloud application-default credentials).",
    )
    parser.add_argument(
        "--client-secrets",
        default="",
        help="Path to Google OAuth client secret JSON (desktop app).",
    )
    parser.add_argument(
        "--token-file",
        default=str(DEFAULT_TOKEN_PATH),
        help="Path for persisted OAuth token JSON.",
    )
    parser.add_argument(
        "--history-file",
        default=str(DEFAULT_HISTORY_PATH),
        help="CSV file tracking previously imported media IDs.",
    )
    parser.add_argument(
        "--recent-days",
        type=int,
        default=120,
        help="Keep only picked items created in the last N days (0 disables date filtering).",
    )
    parser.add_argument(
        "--include-videos",
        action="store_true",
        help="Include video media items from the picker selection.",
    )
    parser.add_argument(
        "--max-items",
        type=int,
        default=0,
        help="Optional hard cap after filtering (0 means no cap).",
    )
    parser.add_argument(
        "--poll-timeout-seconds",
        type=int,
        default=1800,
        help="Maximum wait for user to complete picker selection.",
    )
    parser.add_argument(
        "--open-browser",
        action="store_true",
        help="Open OAuth and picker URLs in the default browser.",
    )
    parser.add_argument(
        "--existing-session-id",
        default="",
        help="Reuse an existing picker session ID (UUID or sessions/<UUID>) instead of creating a new one.",
    )
    return parser.parse_args()


def parse_rfc3339(value: str) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def parse_duration_seconds(value: str | None, default_seconds: float) -> float:
    if not value:
        return default_seconds

    text = value.strip().lower()
    match = re.fullmatch(r"(\d+(?:\.\d+)?)([smh])", text)
    if not match:
        return default_seconds

    amount = float(match.group(1))
    unit = match.group(2)
    if unit == "s":
        return amount
    if unit == "m":
        return amount * 60.0
    if unit == "h":
        return amount * 3600.0
    return default_seconds


def load_credentials_oauth_client(client_secrets: Path, token_file: Path, open_browser: bool) -> Credentials:
    scopes = [PHOTO_PICKER_SCOPE]
    creds: Credentials | None = None

    if token_file.exists():
        creds = Credentials.from_authorized_user_file(str(token_file), scopes=scopes)

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    if not creds or not creds.valid:
        if not client_secrets.exists():
            raise SystemExit(f"OAuth client secret file not found: {client_secrets}")
        flow = InstalledAppFlow.from_client_secrets_file(str(client_secrets), scopes=scopes)
        creds = flow.run_local_server(port=0, open_browser=open_browser)

    token_file.parent.mkdir(parents=True, exist_ok=True)
    token_file.write_text(creds.to_json(), encoding="utf-8")
    return creds


def load_credentials_adc() -> Credentials:
    creds, _ = google.auth.default(scopes=[PHOTO_PICKER_SCOPE])
    if not creds.valid:
        creds.refresh(Request())
    return creds


def api_request(
    session: AuthorizedSession,
    method: str,
    path: str,
    *,
    params: dict[str, Any] | None = None,
    json_body: dict[str, Any] | None = None,
) -> dict[str, Any]:
    url = f"{PHOTO_PICKER_API}{path}"
    response = session.request(method=method, url=url, params=params, json=json_body, timeout=60)
    if response.status_code >= 400:
        raise RuntimeError(f"Photo Picker API error {response.status_code} on {path}: {response.text}")
    if not response.text.strip():
        return {}
    return response.json()


def normalize_session_id(value: str) -> str:
    if value.startswith("sessions/"):
        return value
    return f"sessions/{value}"


def create_picker_session(session: AuthorizedSession) -> dict[str, Any]:
    # Empty body is accepted; media type filtering is handled after selection.
    created = api_request(session, "POST", "/sessions", json_body={})
    if not created.get("id"):
        raise RuntimeError(f"Unexpected session response (missing id): {json.dumps(created, indent=2)}")
    return created


def wait_for_selection(
    session: AuthorizedSession,
    session_id: str,
    poll_timeout_seconds: int,
    initial_poll_interval: float,
) -> dict[str, Any]:
    started = time.monotonic()
    poll_interval = max(1.0, initial_poll_interval)
    last_state: dict[str, Any] = {}

    while time.monotonic() - started <= poll_timeout_seconds:
        current = api_request(session, "GET", f"/{session_id}")
        last_state = current
        if current.get("mediaItemsSet") is True:
            return current

        suggested = parse_duration_seconds(
            (current.get("pollingConfig") or {}).get("pollInterval"),
            poll_interval,
        )
        poll_interval = max(1.0, suggested)
        time.sleep(poll_interval)

    raise TimeoutError(
        "Timed out waiting for picker selection to complete. "
        f"Last session state: {json.dumps(last_state, indent=2)}"
    )


def list_picked_items(session: AuthorizedSession, session_id: str) -> list[PickedItem]:
    all_items: list[PickedItem] = []
    next_page_token = ""
    session_uuid = session_id.split("/", 1)[1] if session_id.startswith("sessions/") else session_id

    while True:
        params: dict[str, Any] = {"sessionId": session_uuid, "pageSize": 100}
        if next_page_token:
            params["pageToken"] = next_page_token

        payload = api_request(session, "GET", "/mediaItems", params=params)
        raw_items = payload.get("mediaItems", [])

        for raw in raw_items:
            media_item_id = str(raw.get("id", "")).strip()
            media_file = raw.get("mediaFile") or {}
            base_url = str(media_file.get("baseUrl", "")).strip()
            mime_type = str(media_file.get("mimeType", "")).strip()
            source_filename = str(media_file.get("filename", "")).strip()
            create_time = str(raw.get("createTime", "")).strip()

            if not media_item_id or not base_url:
                continue

            all_items.append(
                PickedItem(
                    media_item_id=media_item_id,
                    create_time=create_time,
                    mime_type=mime_type,
                    source_filename=source_filename,
                    base_url=base_url,
                )
            )

        next_page_token = str(payload.get("nextPageToken", "")).strip()
        if not next_page_token:
            break

    return all_items


def load_history(history_file: Path) -> dict[str, str]:
    if not history_file.exists():
        return {}

    existing: dict[str, str] = {}
    with history_file.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            media_id = row.get("media_item_id", "").strip()
            file_name = row.get("target_file", "").strip()
            if media_id:
                existing[media_id] = file_name
    return existing


def append_history(history_file: Path, rows: list[dict[str, str]]) -> None:
    history_file.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "imported_at",
        "run_id",
        "media_item_id",
        "create_time",
        "mime_type",
        "source_filename",
        "target_file",
        "status",
        "notes",
    ]
    write_header = not history_file.exists()
    with history_file.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        writer.writerows(rows)


def infer_extension(source_filename: str, mime_type: str) -> str:
    source_suffix = Path(source_filename).suffix.lower()
    if source_suffix:
        return source_suffix
    guessed = mimetypes.guess_extension(mime_type) or ""
    return guessed.lower()


def build_target_name(item: PickedItem, fallback_counter: int) -> str:
    created = parse_rfc3339(item.create_time)
    if created:
        stamp = created.astimezone().strftime("%Y%m%d_%H%M%S")
    else:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    suffix = re.sub(r"[^a-zA-Z0-9]", "", item.media_item_id)[-8:] or f"{fallback_counter:04d}"
    ext = infer_extension(item.source_filename, item.mime_type)
    if not ext:
        ext = ".jpg" if item.mime_type.startswith("image/") else ".bin"

    return f"{stamp}_gp_{suffix}{ext}"


def ensure_unique_name(base_name: str, output_dir: Path) -> str:
    candidate = output_dir / base_name
    if not candidate.exists():
        return base_name

    stem = candidate.stem
    suffix = candidate.suffix
    index = 2
    while True:
        next_name = f"{stem}_{index}{suffix}"
        if not (output_dir / next_name).exists():
            return next_name
        index += 1


def is_video_mime(mime_type: str) -> bool:
    return mime_type.lower().startswith("video/")


def download_item(
    authed_session: AuthorizedSession,
    item: PickedItem,
    output_file: Path,
    timeout_seconds: int = 120,
) -> None:
    url_suffix = "=dv" if is_video_mime(item.mime_type) else "=d"
    download_url = f"{item.base_url}{url_suffix}"
    response = authed_session.get(download_url, timeout=timeout_seconds)
    if response.status_code >= 400:
        raise RuntimeError(f"Download failed ({response.status_code}) for media item {item.media_item_id}: {response.text}")
    output_file.write_bytes(response.content)


def write_run_manifest(run_dir: Path, rows: list[dict[str, str]]) -> Path:
    run_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = run_dir / "manifest.csv"
    fieldnames = [
        "media_item_id",
        "create_time",
        "mime_type",
        "source_filename",
        "target_file",
        "status",
        "notes",
    ]
    with manifest_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return manifest_path


def main() -> None:
    args = parse_args()

    token_file = Path(args.token_file).expanduser()
    history_file = Path(args.history_file).expanduser()

    PHOTOS_DIR.mkdir(parents=True, exist_ok=True)
    RAW_IMPORTS_DIR.mkdir(parents=True, exist_ok=True)

    if args.auth_mode == "adc":
        credentials = load_credentials_adc()
    else:
        if not args.client_secrets:
            raise SystemExit("--client-secrets is required when --auth-mode=oauth-client")
        client_secrets = Path(args.client_secrets).expanduser()
        credentials = load_credentials_oauth_client(client_secrets, token_file, args.open_browser)
    authed_session = AuthorizedSession(credentials)

    existing_session = args.existing_session_id.strip()
    if existing_session:
        session_id = normalize_session_id(existing_session)
        current = api_request(authed_session, "GET", f"/{session_id}")
        if not current.get("mediaItemsSet"):
            raise SystemExit(
                "Existing picker session has no finalized selection yet (mediaItemsSet=false). "
                "Complete selection first, then rerun."
            )
        print(f"Reusing picker session: {session_id}")
    else:
        created = create_picker_session(authed_session)
        session_id = normalize_session_id(str(created["id"]))
        picker_uri = str(created.get("pickerUri", "")).strip()
        poll_interval = parse_duration_seconds((created.get("pollingConfig") or {}).get("pollInterval"), 2.0)

        print(f"Picker session created: {session_id}")
        if picker_uri:
            print("Open this picker URL, select media, then click Done:")
            print(picker_uri)
            if args.open_browser:
                webbrowser.open(picker_uri)

        wait_for_selection(authed_session, session_id, args.poll_timeout_seconds, poll_interval)
    picked_items = list_picked_items(authed_session, session_id)
    print(f"Picked items returned by API: {len(picked_items)}")

    cutoff: datetime | None = None
    if args.recent_days and args.recent_days > 0:
        cutoff = datetime.now(UTC) - timedelta(days=args.recent_days)

    filtered_items: list[PickedItem] = []
    for item in picked_items:
        if not args.include_videos and is_video_mime(item.mime_type):
            continue

        if cutoff is not None:
            created_at = parse_rfc3339(item.create_time)
            if created_at is None:
                continue
            if created_at.astimezone(UTC) < cutoff:
                continue

        filtered_items.append(item)

    if args.max_items and args.max_items > 0:
        filtered_items = filtered_items[: args.max_items]

    existing_history = load_history(history_file)
    run_id = datetime.now().strftime("%Y%m%dT%H%M%S")
    run_dir = RAW_IMPORTS_DIR / run_id

    manifest_rows: list[dict[str, str]] = []
    history_rows: list[dict[str, str]] = []
    downloaded_count = 0
    skipped_known_count = 0
    failed_count = 0

    for counter, item in enumerate(filtered_items, start=1):
        already_target = existing_history.get(item.media_item_id, "")
        if already_target and (PHOTOS_DIR / already_target).exists():
            skipped_known_count += 1
            manifest_rows.append(
                {
                    "media_item_id": item.media_item_id,
                    "create_time": item.create_time,
                    "mime_type": item.mime_type,
                    "source_filename": item.source_filename,
                    "target_file": already_target,
                    "status": "skipped_already_imported",
                    "notes": "Media item ID already exists in import history and target file exists.",
                }
            )
            continue

        target_name = build_target_name(item, fallback_counter=counter)
        target_name = ensure_unique_name(target_name, PHOTOS_DIR)
        target_path = PHOTOS_DIR / target_name

        try:
            download_item(authed_session, item, target_path)
            downloaded_count += 1
            status = "downloaded"
            notes = ""
        except Exception as exc:  # noqa: BLE001
            failed_count += 1
            status = "download_failed"
            notes = str(exc)

        manifest_rows.append(
            {
                "media_item_id": item.media_item_id,
                "create_time": item.create_time,
                "mime_type": item.mime_type,
                "source_filename": item.source_filename,
                "target_file": target_name,
                "status": status,
                "notes": notes,
            }
        )

        history_rows.append(
            {
                "imported_at": datetime.now().isoformat(timespec="seconds"),
                "run_id": run_id,
                "media_item_id": item.media_item_id,
                "create_time": item.create_time,
                "mime_type": item.mime_type,
                "source_filename": item.source_filename,
                "target_file": target_name,
                "status": status,
                "notes": notes,
            }
        )

    manifest_path = write_run_manifest(run_dir, manifest_rows)
    append_history(history_file, history_rows)

    summary = {
        "run_id": run_id,
        "session_id": session_id,
        "picker_items": len(picked_items),
        "filtered_items": len(filtered_items),
        "downloaded": downloaded_count,
        "skipped_already_imported": skipped_known_count,
        "failed": failed_count,
        "manifest": str(manifest_path.relative_to(ROOT)),
    }
    (run_dir / "run_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    print("Import summary:")
    for key, value in summary.items():
        print(f"- {key}: {value}")


if __name__ == "__main__":
    main()
