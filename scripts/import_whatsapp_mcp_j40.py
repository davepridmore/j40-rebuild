#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import os
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = ROOT / "data" / "config"
MANUAL_DIR = ROOT / "data" / "manual"
GENERATED_DIR = ROOT / "data" / "processed" / "generated"

PROJECT_CONFIG_PATH = CONFIG_DIR / "project.json"
TARGET_NUMBERS_PATH = CONFIG_DIR / "whatsapp_target_numbers.json"

CHAT_CANDIDATES_OUTPUT_PATH = MANUAL_DIR / "whatsapp_j40_chat_candidates.csv"
MESSAGES_JSON_OUTPUT_PATH = GENERATED_DIR / "mcp_whatsapp_j40_messages.json"
MESSAGES_CSV_OUTPUT_PATH = GENERATED_DIR / "mcp_whatsapp_j40_messages.csv"
MEDIA_INDEX_OUTPUT_PATH = GENERATED_DIR / "mcp_whatsapp_j40_media_index.csv"
SUMMARY_OUTPUT_PATH = GENERATED_DIR / "mcp_whatsapp_j40_summary.json"

PROFILE_CONFIG_BY_SERVER: dict[str, dict[str, Any]] = {
    "whatsapp-number-1": {
        "label": "primary",
        "api_port": 3011,
        "auth_path": ROOT / ".ai" / "mcp" / "auth" / "whatsapp-number-1",
        "media_storage_path": ROOT / "data" / "raw" / "imports" / "mcp_whatsapp_number_1",
    },
    "whatsapp-number-2": {
        "label": "secondary",
        "api_port": 3012,
        "auth_path": ROOT / ".ai" / "mcp" / "auth" / "whatsapp-number-2",
        "media_storage_path": ROOT / "data" / "raw" / "imports" / "mcp_whatsapp_number_2",
    },
}

SEED_CHAT_NAMES = {
    "fj40",
    "fj 40 - advisory",
    "fj audio",
    "j40 parts",
    "j50",
    "fj50",
    "j50 parts",
    "j50 feedback",
    "akbar khan",
    "akber khan",
    "headlight connectors",
    "walton bodyshop",
    "hamza carnation car mods",
    "akram suspension auto",
    "oxy welding",
    "fiaz akbers help",
    "auto xpert",
}

MEDIA_MESSAGE_TYPES = {"image", "video", "audio", "ptt", "document", "sticker"}
MEDIA_TYPE_MAP = {
    "image": "photo",
    "video": "video",
    "audio": "audio",
    "ptt": "audio",
    "document": "document",
    "sticker": "sticker",
}

MESSAGE_LIMIT_PER_CHAT = 350
HTTP_TIMEOUT = 60
STARTUP_TIMEOUT_SECONDS = 75
CHROME_EXECUTABLE_DEFAULT = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
LOCAL_WWEB_MCP_MAIN = ROOT / "tools" / "wweb-mcp-local" / "dist" / "main.js"

ARCHIVE_MESSAGES_PATH = GENERATED_DIR / "whatsapp_messages.json"
ARCHIVE_MEDIA_INDEX_PATH = GENERATED_DIR / "media_index.csv"

CHAT_RELEVANCE_KEYWORDS = [
    "j40",
    "j50",
    "fj40",
    "fj50",
    "land cruiser",
    "landcruiser",
    "toyota",
    "akbar",
    "akber",
    "bodyshop",
    "carnation",
    "suspension",
    "welding",
    "weld",
    "paint",
    "primer",
    "chassis",
    "headlight",
    "connector",
    "walton",
    "auto xpert",
    "oxy welding",
    "ome",
    "eps",
]

ARCHIVE_SOURCE_BY_CHAT_NAME = {
    "fj40": "Fj40",
    "akbar khan": "Akbar Khan",
    "akber khan": "Akbar Khan",
}

HIDDEN_CHAT_NAMES = {"support engineer placement"}
HIDDEN_CHAT_IDS = {"120363406007289586@g.us"}


@dataclass
class Profile:
    server: str
    label: str
    target_number: str
    api_port: int
    auth_path: Path
    media_storage_path: Path


def clean(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def norm(value: Any) -> str:
    return clean(value).lower()


def clean_text(value: Any) -> str:
    return canonicalize_akbar_spelling(" ".join(clean(value).replace("\u200e", " ").split()))


def canonicalize_akbar_spelling(value: Any) -> str:
    text = clean(value)
    legacy = "Ak" + "ber"
    return text.replace(f"{legacy}s", "Akbar's").replace(legacy, "Akbar")


def display_chat_name(value: Any) -> str:
    raw = canonicalize_akbar_spelling(value)
    if norm(raw) == "akber khan":
        return "Akbar Khan"
    return raw


def is_hidden_chat(row: dict[str, Any]) -> bool:
    chat_name = norm(row.get("chat_name") or row.get("source_name") or row.get("name"))
    chat_id = clean(row.get("chat_id") or row.get("id"))
    return chat_name in HIDDEN_CHAT_NAMES or chat_id in HIDDEN_CHAT_IDS


def slugify(value: str) -> str:
    chars: list[str] = []
    for character in value.lower():
        if character.isalnum():
            chars.append(character)
        else:
            chars.append("_")
    result = "".join(chars)
    while "__" in result:
        result = result.replace("__", "_")
    return result.strip("_")


def load_project_keywords() -> list[str]:
    if not PROJECT_CONFIG_PATH.exists():
        return []
    config = json.loads(PROJECT_CONFIG_PATH.read_text(encoding="utf-8"))
    keywords = [clean(keyword) for keyword in config.get("include_keywords", []) if clean(keyword)]
    extra_keywords = [
        "fj40",
        "j40",
        "land cruiser",
        "landcruiser",
        "bodyshop",
        "body shop",
        "chassis",
        "welding",
        "weld",
        "paint",
        "primer",
        "suspension",
        "akbar",
        "akber",
        "carnation",
        "oxy welding",
        "headlight",
        "connector",
        "toolsmart",
        "walton",
    ]
    all_keywords = sorted({norm(keyword) for keyword in keywords + extra_keywords if norm(keyword)})
    return all_keywords


def load_profiles() -> list[Profile]:
    if not TARGET_NUMBERS_PATH.exists():
        raise FileNotFoundError(f"Missing target-number config: {TARGET_NUMBERS_PATH}")

    payload = json.loads(TARGET_NUMBERS_PATH.read_text(encoding="utf-8"))
    profiles: list[Profile] = []
    for row in payload.get("numbers", []):
        server = clean(row.get("server"))
        target_number = clean(row.get("phone_e164"))
        if not server or not target_number:
            continue
        if server not in PROFILE_CONFIG_BY_SERVER:
            continue
        config = PROFILE_CONFIG_BY_SERVER[server]
        profiles.append(
            Profile(
                server=server,
                label=clean(row.get("label")) or clean(config["label"]),
                target_number=target_number,
                api_port=int(config["api_port"]),
                auth_path=Path(config["auth_path"]),
                media_storage_path=Path(config["media_storage_path"]),
            )
        )
    return profiles


def read_api_key(profile: Profile) -> str:
    key_path = profile.auth_path / "api_key.txt"
    if not key_path.exists():
        return ""
    return clean(key_path.read_text(encoding="utf-8"))


def request_json(profile: Profile, api_key: str, path: str, method: str = "GET") -> Any:
    base_url = f"http://127.0.0.1:{profile.api_port}/api"
    url = base_url + path
    request = urllib.request.Request(
        url=url,
        method=method,
        headers={"Authorization": f"Bearer {api_key}"},
    )
    with urllib.request.urlopen(request, timeout=HTTP_TIMEOUT) as response:
        data = response.read().decode("utf-8")
        return json.loads(data)


def request_json_with_retry(
    profile: Profile,
    api_key: str,
    path: str,
    method: str = "GET",
    max_attempts: int = 6,
    retry_delay_seconds: float = 2.0,
) -> Any:
    last_error: Exception | None = None
    for _ in range(max_attempts):
        try:
            return request_json(profile, api_key, path, method=method)
        except urllib.error.HTTPError as error:
            last_error = error
            if error.code == 503:
                time.sleep(retry_delay_seconds)
                continue
            raise
        except Exception as error:
            last_error = error
            time.sleep(retry_delay_seconds)

    if last_error is not None:
        raise last_error
    raise RuntimeError(f"Request failed without error for path: {path}")


def api_is_live(profile: Profile, api_key: str) -> bool:
    if not api_key:
        return False
    try:
        status = request_json(profile, api_key, "/status")
    except Exception:
        return False
    return isinstance(status, dict) and clean(status.get("status")) in {"connected", "disconnected"}


def start_api_server(profile: Profile) -> subprocess.Popen[str]:
    profile.auth_path.mkdir(parents=True, exist_ok=True)
    profile.media_storage_path.mkdir(parents=True, exist_ok=True)
    if LOCAL_WWEB_MCP_MAIN.exists():
        command = [
            "node",
            str(LOCAL_WWEB_MCP_MAIN),
            "-m",
            "whatsapp-api",
            "-s",
            "local",
            "-a",
            str(profile.auth_path),
            "--media-storage-path",
            str(profile.media_storage_path),
            "--api-port",
            str(profile.api_port),
            "-l",
            "warn",
        ]
    else:
        command = [
            "npx",
            "-y",
            "wweb-mcp@0.2.3",
            "-m",
            "whatsapp-api",
            "-s",
            "local",
            "-a",
            str(profile.auth_path),
            "--media-storage-path",
            str(profile.media_storage_path),
            "--api-port",
            str(profile.api_port),
            "-l",
            "warn",
        ]

    env = os.environ.copy()
    if CHROME_EXECUTABLE_DEFAULT.exists():
        env.setdefault("PUPPETEER_EXECUTABLE_PATH", str(CHROME_EXECUTABLE_DEFAULT))
    return subprocess.Popen(
        command,
        cwd=ROOT,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )


def wait_for_api(profile: Profile, process: subprocess.Popen[str] | None) -> str:
    deadline = time.time() + STARTUP_TIMEOUT_SECONDS
    api_key = ""
    while time.time() < deadline:
        if process is not None and process.poll() is not None:
            break

        if not api_key:
            api_key = read_api_key(profile)

        if api_key and api_is_live(profile, api_key):
            return api_key

        time.sleep(1.0)

    stderr_tail = ""
    if process is not None and process.stdout is not None:
        try:
            stderr_tail = process.stdout.read() or ""
        except Exception:
            stderr_tail = ""
    raise RuntimeError(
        f"Timed out waiting for WhatsApp API for {profile.server}. "
        f"Check session auth and running process. Output: {stderr_tail[-800:]}"
    )


def stop_server(process: subprocess.Popen[str] | None) -> None:
    if process is None:
        return
    if process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=8)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=4)


def keyword_hits(text: str, keywords: list[str]) -> list[str]:
    lowered = norm(text)
    hits: list[str] = []
    for keyword in keywords:
        if not keyword:
            continue
        if keyword in lowered:
            hits.append(keyword)
    return sorted(set(hits))


def score_chat(chat: dict[str, Any], keywords: list[str]) -> tuple[int, list[str]]:
    chat_name = display_chat_name(chat.get("name"))
    last_message = clean(chat.get("lastMessage"))
    chat_id = clean(chat.get("id"))
    reasons: list[str] = []

    name_hits = keyword_hits(chat_name, keywords)
    message_hits = keyword_hits(last_message, keywords)

    score = len(name_hits) * 4 + len(message_hits) * 2
    if norm(chat_name) in SEED_CHAT_NAMES:
        score += 6
        reasons.append("seed_name")
    if chat_id.endswith("@g.us"):
        score += 1
        reasons.append("group_bonus")
    if name_hits:
        reasons.append(f"name_hits:{'|'.join(name_hits)}")
    if message_hits:
        reasons.append(f"last_message_hits:{'|'.join(message_hits)}")
    return score, reasons


def chat_type(chat_id: str) -> str:
    if chat_id.endswith("@g.us"):
        return "group"
    if chat_id.endswith("@c.us"):
        return "direct_cus"
    if chat_id.endswith("@lid"):
        return "direct_lid"
    return "other"


def fetch_chat_messages(profile: Profile, api_key: str, chat: dict[str, Any]) -> tuple[list[dict[str, Any]], str]:
    chat_id = clean(chat.get("id"))
    type_name = chat_type(chat_id)
    quoted_chat_id = urllib.parse.quote(chat_id, safe="")

    if type_name == "group":
        path = f"/groups/{quoted_chat_id}/messages?limit={MESSAGE_LIMIT_PER_CHAT}"
    elif type_name == "direct_cus":
        path = f"/messages/{quoted_chat_id}?limit={MESSAGE_LIMIT_PER_CHAT}"
    elif type_name == "direct_lid":
        return [], "messages_api_not_supported_for_lid"
    else:
        return [], "messages_api_not_supported_for_type"

    try:
        payload = request_json_with_retry(profile, api_key, path)
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        return [], f"http_{error.code}:{clean_text(detail)[:140]}"
    except Exception as error:
        return [], f"request_failed:{clean(error)}"

    if not isinstance(payload, list):
        return [], "invalid_messages_payload"
    return payload, ""


def canonical_message_id(profile: Profile, raw_message_id: str) -> str:
    return f"mcp_{slugify(profile.server)}_{slugify(raw_message_id)}"


def download_media(profile: Profile, api_key: str, raw_message_id: str) -> dict[str, Any] | None:
    quoted_message_id = urllib.parse.quote(raw_message_id, safe="")
    path = f"/messages/{quoted_message_id}/media/download"
    try:
        payload = request_json_with_retry(profile, api_key, path, method="POST")
    except urllib.error.HTTPError:
        return None
    except Exception:
        return None
    if not isinstance(payload, dict):
        return None
    return payload


def to_relative(path_value: str) -> str:
    path = Path(path_value)
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def dedupe_rows(rows: list[dict[str, Any]], key_field: str) -> list[dict[str, Any]]:
    unique: list[dict[str, Any]] = []
    seen_keys: set[str] = set()
    for row in rows:
        key = clean(row.get(key_field))
        if not key or key in seen_keys:
            continue
        seen_keys.add(key)
        unique.append(row)
    return unique


def load_archive_fallback() -> tuple[dict[str, list[dict[str, Any]]], dict[str, list[dict[str, Any]]]]:
    messages_by_source: dict[str, list[dict[str, Any]]] = {}
    media_by_source: dict[str, list[dict[str, Any]]] = {}

    if ARCHIVE_MESSAGES_PATH.exists():
        try:
            message_rows = json.loads(ARCHIVE_MESSAGES_PATH.read_text(encoding="utf-8"))
            if isinstance(message_rows, list):
                for row in message_rows:
                    source_name = display_chat_name(row.get("source_name"))
                    if not source_name:
                        continue
                    messages_by_source.setdefault(source_name, []).append(row)
        except Exception:
            messages_by_source = {}

    if ARCHIVE_MEDIA_INDEX_PATH.exists():
        try:
            with ARCHIVE_MEDIA_INDEX_PATH.open(newline="", encoding="utf-8") as handle:
                for row in csv.DictReader(handle):
                    source_name = display_chat_name(row.get("source_name"))
                    if not source_name:
                        continue
                    media_by_source.setdefault(source_name, []).append(row)
        except Exception:
            media_by_source = {}

    return messages_by_source, media_by_source


def load_previous_mcp_exports() -> tuple[dict[str, list[dict[str, Any]]], dict[str, list[dict[str, Any]]]]:
    previous_messages_by_profile: dict[str, list[dict[str, Any]]] = {}
    previous_media_by_profile: dict[str, list[dict[str, Any]]] = {}

    message_candidates: list[Path] = []
    if MESSAGES_CSV_OUTPUT_PATH.exists():
        message_candidates.append(MESSAGES_CSV_OUTPUT_PATH)
    message_candidates.extend(sorted(GENERATED_DIR.glob("mcp_whatsapp_j40_messages.before*.csv"), reverse=True))

    media_candidates: list[Path] = []
    if MEDIA_INDEX_OUTPUT_PATH.exists():
        media_candidates.append(MEDIA_INDEX_OUTPUT_PATH)
    media_candidates.extend(sorted(GENERATED_DIR.glob("mcp_whatsapp_j40_media_index.before*.csv"), reverse=True))

    for candidate in message_candidates:
        if len(previous_messages_by_profile) == len(PROFILE_CONFIG_BY_SERVER):
            break
        try:
            rows_by_profile: dict[str, list[dict[str, Any]]] = {}
            with candidate.open(newline="", encoding="utf-8") as handle:
                for row in csv.DictReader(handle):
                    profile_server = clean(row.get("source_profile"))
                    if not profile_server:
                        continue
                    rows_by_profile.setdefault(profile_server, []).append(row)
            for profile_server, rows in rows_by_profile.items():
                if profile_server not in previous_messages_by_profile and rows:
                    previous_messages_by_profile[profile_server] = rows
        except Exception:
            continue

    for candidate in media_candidates:
        try:
            with candidate.open(newline="", encoding="utf-8") as handle:
                rows_by_profile: dict[str, list[dict[str, Any]]] = {}
                for row in csv.DictReader(handle):
                    profile_server = clean(row.get("source_profile"))
                    if not profile_server:
                        continue
                    rows_by_profile.setdefault(profile_server, []).append(row)
                for profile_server, rows in rows_by_profile.items():
                    if profile_server not in previous_media_by_profile and rows:
                        previous_media_by_profile[profile_server] = rows
        except Exception:
            continue

    return previous_messages_by_profile, previous_media_by_profile


def archive_source_from_chat_name(chat_name: str) -> str:
    return ARCHIVE_SOURCE_BY_CHAT_NAME.get(norm(chat_name), "")


def main() -> None:
    message_keywords = load_project_keywords()
    chat_keywords = sorted(set(CHAT_RELEVANCE_KEYWORDS + message_keywords))
    profiles = load_profiles()
    if not profiles:
        raise SystemExit("No WhatsApp target profiles configured. Update data/config/whatsapp_target_numbers.json")

    archive_messages_by_source, archive_media_by_source = load_archive_fallback()
    previous_messages_by_profile, previous_media_by_profile = load_previous_mcp_exports()

    all_chat_rows: list[dict[str, Any]] = []
    all_message_rows: list[dict[str, Any]] = []
    all_media_rows: list[dict[str, Any]] = []
    profile_summaries: list[dict[str, Any]] = []
    loaded_fallback_sources: set[str] = set()

    for profile in profiles:
        process: subprocess.Popen[str] | None = None
        started_here = False

        api_key = read_api_key(profile)
        if not api_is_live(profile, api_key):
            process = start_api_server(profile)
            started_here = True
            api_key = wait_for_api(profile, process)

        try:
            status_payload: dict[str, Any] = {}
            status_request_error = ""
            try:
                status_response = request_json_with_retry(profile, api_key, "/status")
                if isinstance(status_response, dict):
                    status_payload = status_response
            except Exception as error:
                status_request_error = f"status_request_failed:{clean(error)}"

            chats_payload: list[dict[str, Any]] = []
            chats_request_error = ""
            try:
                chats_response = request_json_with_retry(profile, api_key, "/chats")
                if isinstance(chats_response, list):
                    chats_payload = chats_response
            except Exception as error:
                chats_request_error = f"chats_request_failed:{clean(error)}"

            candidate_rows: list[dict[str, Any]] = []
            for chat in chats_payload:
                if is_hidden_chat(chat):
                    continue
                score, reasons = score_chat(chat, chat_keywords)
                selected = score >= 8 or "seed_name" in reasons
                candidate_rows.append(
                    {
                        "profile_server": profile.server,
                        "profile_label": profile.label,
                        "target_number": profile.target_number,
                        "chat_id": clean(chat.get("id")),
                        "chat_type": chat_type(clean(chat.get("id"))),
                        "chat_name": display_chat_name(chat.get("name")),
                        "unread_count": clean(chat.get("unreadCount")),
                        "last_message_timestamp": clean(chat.get("timestamp")),
                        "last_message": clean_text(chat.get("lastMessage")),
                        "relevance_score": score,
                        "relevance_reasons": "|".join(reasons),
                        "selected_for_import": "true" if selected else "false",
                        "messages_fetched": "false",
                        "messages_fetch_error": "",
                        "messages_count": "0",
                        "media_count": "0",
                        "images_count": "0",
                        "videos_count": "0",
                    }
                )

            if not candidate_rows and chats_request_error:
                for fallback_source in sorted(set(archive_messages_by_source.keys())):
                    if not archive_messages_by_source.get(fallback_source):
                        continue
                    candidate_rows.append(
                        {
                            "profile_server": profile.server,
                            "profile_label": profile.label,
                            "target_number": profile.target_number,
                            "chat_id": f"archive::{slugify(fallback_source)}",
                            "chat_type": "archive",
                            "chat_name": display_chat_name(fallback_source),
                            "unread_count": "",
                            "last_message_timestamp": "",
                            "last_message": "",
                            "relevance_score": 6,
                            "relevance_reasons": f"archive_fallback|{chats_request_error}",
                            "selected_for_import": "true",
                            "messages_fetched": "false",
                            "messages_fetch_error": "",
                            "messages_count": "0",
                            "media_count": "0",
                            "images_count": "0",
                            "videos_count": "0",
                        }
                    )

            selected_chats = [row for row in candidate_rows if row["selected_for_import"] == "true"]
            selected_chats.sort(key=lambda row: int(row["relevance_score"]), reverse=True)

            message_count = 0
            media_count = 0
            image_count = 0
            video_count = 0
            used_previous_export_fallback = False

            for chat_row in selected_chats:
                chat_id = chat_row["chat_id"]
                chat_name = chat_row["chat_name"]
                raw_messages, fetch_error = fetch_chat_messages(
                    profile,
                    api_key,
                    {"id": chat_id},
                )
                if fetch_error:
                    chat_row["messages_fetch_error"] = fetch_error
                    fallback_source = archive_source_from_chat_name(chat_name)
                    archive_messages = archive_messages_by_source.get(fallback_source, [])
                    archive_media = archive_media_by_source.get(fallback_source, [])
                    if fallback_source in loaded_fallback_sources:
                        chat_row["messages_fetch_error"] = f"{fetch_error}|fallback_skipped_already_loaded:{fallback_source}"
                    elif fallback_source and archive_messages and archive_media:
                        chat_row["messages_fetched"] = "fallback_archive"
                        chat_row["messages_fetch_error"] = f"{fetch_error}|fallback:{fallback_source}"
                        chat_row["messages_count"] = str(len(archive_messages))

                        mapped_message_ids: dict[str, str] = {}
                        for archive_message in archive_messages:
                            raw_archive_message_id = clean(archive_message.get("message_id"))
                            canonical_id = f"mcp_{slugify(profile.server)}_archive_{slugify(raw_archive_message_id)}"
                            mapped_message_ids[raw_archive_message_id] = canonical_id

                            body = canonicalize_akbar_spelling(archive_message.get("clean_text") or archive_message.get("text"))
                            message_hits = keyword_hits(body, message_keywords)
                            all_message_rows.append(
                                {
                                    "message_id": canonical_id,
                                    "raw_message_id": raw_archive_message_id,
                                    "source_name": display_chat_name(chat_name or chat_id),
                                    "source_profile": profile.server,
                                    "chat_id": chat_id,
                                    "chat_name": chat_name,
                                    "timestamp": clean(archive_message.get("timestamp")),
                                    "author": display_chat_name(archive_message.get("author")),
                                    "from_me": "false",
                                    "type": "chat",
                                    "body": body,
                                    "clean_text": clean_text(body),
                                    "keyword_hits": "|".join(message_hits),
                                    "is_relevant": "true",
                                }
                            )
                            message_count += 1

                        chat_media = 0
                        chat_images = 0
                        chat_videos = 0
                        for archive_media_row in archive_media:
                            raw_archive_message_id = clean(archive_media_row.get("message_id"))
                            canonical_id = mapped_message_ids.get(raw_archive_message_id)
                            if not canonical_id:
                                continue
                            media_type = clean(archive_media_row.get("media_type"))
                            if media_type not in {"photo", "video", "audio", "document", "sticker"}:
                                continue

                            chat_media += 1
                            if media_type == "photo":
                                chat_images += 1
                                image_count += 1
                            if media_type == "video":
                                chat_videos += 1
                                video_count += 1

                            file_name = clean(archive_media_row.get("file_name"))
                            all_media_rows.append(
                                {
                                    "media_id": f"{canonical_id}::{file_name}",
                                    "source_name": chat_name or chat_id,
                                    "source_profile": profile.server,
                                    "chat_id": chat_id,
                                    "chat_name": chat_name,
                                    "message_id": canonical_id,
                                    "raw_message_id": raw_archive_message_id,
                                    "timestamp": clean(archive_media_row.get("timestamp")),
                                    "author": clean(archive_media_row.get("author")),
                                    "file_name": file_name,
                                    "relative_path": clean(archive_media_row.get("relative_path")),
                                    "media_type": media_type,
                                    "message_type": media_type,
                                    "is_relevant": clean(archive_media_row.get("is_relevant")) or "true",
                                    "mimetype": "",
                                    "filesize": "",
                                }
                            )
                            media_count += 1

                        chat_row["media_count"] = str(chat_media)
                        chat_row["images_count"] = str(chat_images)
                        chat_row["videos_count"] = str(chat_videos)
                        loaded_fallback_sources.add(fallback_source)
                    continue

                chat_row["messages_fetched"] = "true"
                chat_row["messages_count"] = str(len(raw_messages))

                chat_media = 0
                chat_images = 0
                chat_videos = 0

                for raw_message in raw_messages:
                    raw_message_id = clean(raw_message.get("id"))
                    canonical_id = canonical_message_id(profile, raw_message_id)
                    body = canonicalize_akbar_spelling(raw_message.get("body"))
                    message_hits = keyword_hits(body, message_keywords)
                    message_type = clean(raw_message.get("type")) or "chat"
                    author = display_chat_name(raw_message.get("contact"))
                    if not author and clean(raw_message.get("fromMe")) == "True":
                        author = profile.target_number

                    message_row = {
                        "message_id": canonical_id,
                        "raw_message_id": raw_message_id,
                        "source_name": display_chat_name(chat_name or chat_id),
                        "source_profile": profile.server,
                        "chat_id": chat_id,
                        "chat_name": chat_name,
                        "timestamp": clean(raw_message.get("timestamp")),
                        "author": author,
                        "from_me": clean(raw_message.get("fromMe")).lower(),
                        "type": message_type,
                        "body": body,
                        "clean_text": clean_text(body),
                        "keyword_hits": "|".join(message_hits),
                        "is_relevant": "true" if (message_hits or chat_row["selected_for_import"] == "true") else "false",
                    }
                    all_message_rows.append(message_row)
                    message_count += 1

                    if message_type not in MEDIA_MESSAGE_TYPES:
                        continue

                    chat_media += 1
                    media_payload = download_media(profile, api_key, raw_message_id)
                    if not media_payload:
                        continue

                    file_name = clean(media_payload.get("filename"))
                    file_path = clean(media_payload.get("filePath"))
                    relative_path = to_relative(file_path)
                    normalized_media_type = MEDIA_TYPE_MAP.get(message_type, "file")
                    if normalized_media_type == "photo":
                        chat_images += 1
                        image_count += 1
                    if normalized_media_type == "video":
                        chat_videos += 1
                        video_count += 1

                    media_row = {
                        "media_id": f"{canonical_id}::{file_name}",
                        "source_name": chat_name or chat_id,
                        "source_profile": profile.server,
                        "chat_id": chat_id,
                        "chat_name": chat_name,
                        "message_id": canonical_id,
                        "raw_message_id": raw_message_id,
                        "timestamp": clean(raw_message.get("timestamp")),
                        "author": author,
                        "file_name": file_name,
                        "relative_path": relative_path,
                        "media_type": normalized_media_type,
                        "message_type": message_type,
                        "is_relevant": "true",
                        "mimetype": clean(media_payload.get("mimetype")),
                        "filesize": clean(media_payload.get("filesize")),
                    }
                    all_media_rows.append(media_row)
                    media_count += 1

                chat_row["media_count"] = str(chat_media)
                chat_row["images_count"] = str(chat_images)
                chat_row["videos_count"] = str(chat_videos)

            if message_count == 0 and chats_request_error:
                previous_messages = previous_messages_by_profile.get(profile.server, [])
                previous_media = previous_media_by_profile.get(profile.server, [])
                previous_messages = [row for row in previous_messages if not is_hidden_chat(row)]
                previous_media = [row for row in previous_media if not is_hidden_chat(row)]
                if previous_messages:
                    all_message_rows.extend(previous_messages)
                    all_media_rows.extend(previous_media)
                    message_count = len(previous_messages)
                    media_count = len(previous_media)
                    image_count = sum(1 for row in previous_media if clean(row.get("media_type")) == "photo")
                    video_count = sum(1 for row in previous_media if clean(row.get("media_type")) == "video")
                    used_previous_export_fallback = True
                    candidate_rows.append(
                        {
                            "profile_server": profile.server,
                            "profile_label": profile.label,
                            "target_number": profile.target_number,
                            "chat_id": f"previous_export::{slugify(profile.server)}",
                            "chat_type": "previous_export",
                            "chat_name": "Previous MCP export fallback",
                            "unread_count": "",
                            "last_message_timestamp": "",
                            "last_message": "",
                            "relevance_score": 7,
                            "relevance_reasons": f"previous_export_fallback|{chats_request_error}",
                            "selected_for_import": "true",
                            "messages_fetched": "fallback_previous_export",
                            "messages_fetch_error": chats_request_error,
                            "messages_count": str(message_count),
                            "media_count": str(media_count),
                            "images_count": str(image_count),
                            "videos_count": str(video_count),
                        }
                    )

            all_chat_rows.extend(candidate_rows)
            summary_status = clean(status_payload.get("status")) if isinstance(status_payload, dict) else ""
            if not summary_status and status_request_error:
                summary_status = "status_unavailable"
            if not summary_status and chats_request_error:
                summary_status = "disconnected_or_unavailable"
            if used_previous_export_fallback:
                summary_status = f"{summary_status or 'unknown'}_with_previous_export_fallback"
            profile_summaries.append(
                {
                    "profile_server": profile.server,
                    "profile_label": profile.label,
                    "target_number": profile.target_number,
                    "status": summary_status,
                    "total_chats": len(chats_payload),
                    "selected_chats": sum(1 for row in candidate_rows if row["selected_for_import"] == "true"),
                    "messages_imported": message_count,
                    "media_imported": media_count,
                    "images_imported": image_count,
                    "videos_imported": video_count,
                }
            )
        finally:
            if started_here:
                stop_server(process)

    all_chat_rows = [row for row in all_chat_rows if not is_hidden_chat(row)]
    all_message_rows = [row for row in all_message_rows if not is_hidden_chat(row)]
    all_media_rows = [row for row in all_media_rows if not is_hidden_chat(row)]

    all_message_rows = dedupe_rows(all_message_rows, "message_id")
    all_media_rows = dedupe_rows(all_media_rows, "media_id")

    all_chat_rows.sort(
        key=lambda row: (
            row["profile_server"],
            -int(clean(row.get("relevance_score")) or "0"),
            row["chat_name"],
            row["chat_id"],
        )
    )
    all_message_rows.sort(key=lambda row: (row["timestamp"], row["source_profile"], row["chat_id"], row["message_id"]))
    all_media_rows.sort(key=lambda row: (row["timestamp"], row["source_profile"], row["chat_id"], row["media_id"]))

    write_csv(
        CHAT_CANDIDATES_OUTPUT_PATH,
        all_chat_rows,
        [
            "profile_server",
            "profile_label",
            "target_number",
            "chat_id",
            "chat_type",
            "chat_name",
            "unread_count",
            "last_message_timestamp",
            "last_message",
            "relevance_score",
            "relevance_reasons",
            "selected_for_import",
            "messages_fetched",
            "messages_fetch_error",
            "messages_count",
            "media_count",
            "images_count",
            "videos_count",
        ],
    )
    write_csv(
        MESSAGES_CSV_OUTPUT_PATH,
        all_message_rows,
        [
            "message_id",
            "raw_message_id",
            "source_name",
            "source_profile",
            "chat_id",
            "chat_name",
            "timestamp",
            "author",
            "from_me",
            "type",
            "body",
            "clean_text",
            "keyword_hits",
            "is_relevant",
        ],
    )
    write_csv(
        MEDIA_INDEX_OUTPUT_PATH,
        all_media_rows,
        [
            "media_id",
            "source_name",
            "source_profile",
            "chat_id",
            "chat_name",
            "message_id",
            "raw_message_id",
            "timestamp",
            "author",
            "file_name",
            "relative_path",
            "media_type",
            "message_type",
            "is_relevant",
            "mimetype",
            "filesize",
        ],
    )

    MESSAGES_JSON_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    MESSAGES_JSON_OUTPUT_PATH.write_text(json.dumps(all_message_rows, indent=2, ensure_ascii=False), encoding="utf-8")

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "profiles": profile_summaries,
        "totals": {
            "chat_candidates": len(all_chat_rows),
            "selected_chats": sum(1 for row in all_chat_rows if row["selected_for_import"] == "true"),
            "messages_imported": len(all_message_rows),
            "media_imported": len(all_media_rows),
            "images_imported": sum(1 for row in all_media_rows if row["media_type"] == "photo"),
            "videos_imported": sum(1 for row in all_media_rows if row["media_type"] == "video"),
        },
        "outputs": {
            "chat_candidates_csv": str(CHAT_CANDIDATES_OUTPUT_PATH.relative_to(ROOT)),
            "messages_json": str(MESSAGES_JSON_OUTPUT_PATH.relative_to(ROOT)),
            "messages_csv": str(MESSAGES_CSV_OUTPUT_PATH.relative_to(ROOT)),
            "media_index_csv": str(MEDIA_INDEX_OUTPUT_PATH.relative_to(ROOT)),
        },
    }
    SUMMARY_OUTPUT_PATH.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Wrote chat candidates: {CHAT_CANDIDATES_OUTPUT_PATH.relative_to(ROOT)}")
    print(f"Wrote messages JSON: {MESSAGES_JSON_OUTPUT_PATH.relative_to(ROOT)}")
    print(f"Wrote media index: {MEDIA_INDEX_OUTPUT_PATH.relative_to(ROOT)}")
    print(
        "Summary: "
        f"{summary['totals']['selected_chats']} selected chats, "
        f"{summary['totals']['messages_imported']} messages, "
        f"{summary['totals']['media_imported']} media items"
    )


if __name__ == "__main__":
    main()
