#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import shutil
import time
import urllib.error
import urllib.parse
from pathlib import Path
from typing import Any

from import_whatsapp_mcp_j40 import (
    MEDIA_INDEX_OUTPUT_PATH,
    MESSAGES_CSV_OUTPUT_PATH,
    MESSAGES_JSON_OUTPUT_PATH,
    PROFILE_CONFIG_BY_SERVER,
    Profile,
    canonical_message_id,
    clean,
    clean_text,
    display_chat_name,
    keyword_hits,
    load_project_keywords,
    read_api_key,
    request_json,
    request_json_with_retry,
    slugify,
    start_api_server,
    stop_server,
    to_relative,
    wait_for_api,
)


ROOT = Path(__file__).resolve().parent.parent
TARGET_CHAT_NAME = "TLC 40 Series Owners"
PROFILE_SERVER = "whatsapp-number-2"

MEDIA_FIELDNAMES = [
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
]

MESSAGE_FIELDNAMES = [
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
]


def load_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv_rows(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def write_messages_json(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def dedupe_rows(rows: list[dict[str, Any]], key_name: str) -> list[dict[str, Any]]:
    seen: set[str] = set()
    output: list[dict[str, Any]] = []
    for row in rows:
        key = clean(row.get(key_name))
        if not key or key in seen:
            continue
        seen.add(key)
        output.append(row)
    return output


def media_type_for_message(message_type: str) -> str:
    if message_type == "image":
        return "photo"
    if message_type == "video":
        return "video"
    return "file"


def normalize_media_file(profile: Profile, file_path: str, file_name: str) -> str:
    source_path = Path(file_path)
    destination_path = profile.media_storage_path / file_name
    if not source_path.is_absolute():
        source_path = ROOT / source_path
    if source_path == destination_path:
        return str(destination_path)
    if source_path.exists():
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        if destination_path.exists():
            source_path.unlink()
        else:
            shutil.move(str(source_path), str(destination_path))
        return str(destination_path)
    if destination_path.exists():
        return str(destination_path)
    return file_path


def download_media_with_detail(profile: Profile, api_key: str, raw_message_id: str) -> tuple[dict[str, Any] | None, str]:
    quoted_message_id = urllib.parse.quote(raw_message_id, safe="")
    path = f"/messages/{quoted_message_id}/media/download"
    try:
        payload = request_json_with_retry(profile, api_key, path, method="POST")
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        return None, f"http_{error.code}:{clean_text(detail)[:220]}"
    except Exception as error:
        return None, f"request_failed:{clean(error)}"
    if not isinstance(payload, dict):
        return None, "invalid_media_payload"
    return payload, ""


def build_profile() -> Profile:
    config = PROFILE_CONFIG_BY_SERVER[PROFILE_SERVER]
    return Profile(
        server=PROFILE_SERVER,
        label=clean(config["label"]),
        target_number="+923099351940",
        api_port=int(config["api_port"]),
        auth_path=Path(config["auth_path"]),
        media_storage_path=Path(config["media_storage_path"]),
    )


def find_target_chat(profile: Profile, api_key: str) -> dict[str, Any]:
    chats = request_json(profile, api_key, "/chats")
    if not isinstance(chats, list):
        raise RuntimeError("Invalid /chats payload")
    for chat in chats:
        if clean(chat.get("name")) == TARGET_CHAT_NAME:
            return chat
    lowered = TARGET_CHAT_NAME.lower()
    for chat in chats:
        if lowered in clean(chat.get("name")).lower():
            return chat
    raise RuntimeError(f"Chat not found: {TARGET_CHAT_NAME}")


def wait_for_connected_status(profile: Profile, api_key: str, timeout_seconds: int = 120) -> dict[str, Any]:
    deadline = time.time() + timeout_seconds
    last_status: dict[str, Any] = {}
    while time.time() < deadline:
        try:
            status = request_json(profile, api_key, "/status")
        except Exception:
            time.sleep(2)
            continue
        if isinstance(status, dict):
            last_status = status
            if clean(status.get("status")) == "connected":
                return status
        time.sleep(2)
    raise RuntimeError(f"WhatsApp profile did not reach connected status. Last status: {last_status}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=1000)
    parser.add_argument("--include-videos", action="store_true")
    args = parser.parse_args()

    profile = build_profile()
    process = None
    api_key = read_api_key(profile)
    process = start_api_server(profile)
    api_key = wait_for_api(profile, process)

    try:
        status = wait_for_connected_status(profile, api_key)
        chat = find_target_chat(profile, api_key)
        chat_id = clean(chat.get("id"))
        chat_name = display_chat_name(chat.get("name"))
        quoted_chat_id = urllib.parse.quote(chat_id, safe="")
        messages = request_json_with_retry(profile, api_key, f"/groups/{quoted_chat_id}/messages?limit={args.limit}")
        if not isinstance(messages, list):
            raise RuntimeError("Invalid group messages payload")

        allowed_message_types = {"image", "video"} if args.include_videos else {"image"}
        existing_media_rows = load_csv_rows(MEDIA_INDEX_OUTPUT_PATH)
        existing_message_rows = load_csv_rows(MESSAGES_CSV_OUTPUT_PATH)
        existing_media_by_id = {clean(row.get("media_id")): row for row in existing_media_rows}
        existing_media_ids = set(existing_media_by_id)
        existing_message_ids = {clean(row.get("message_id")) for row in existing_message_rows}
        message_keywords = load_project_keywords()

        new_media_rows: list[dict[str, Any]] = []
        new_message_rows: list[dict[str, Any]] = []
        failures: list[str] = []
        media_candidates = [message for message in messages if clean(message.get("type")) in allowed_message_types]

        for raw_message in media_candidates:
            raw_message_id = clean(raw_message.get("id"))
            if not raw_message_id:
                continue
            canonical_id = canonical_message_id(profile, raw_message_id)
            body = clean(raw_message.get("body"))
            message_type = clean(raw_message.get("type"))
            author = display_chat_name(raw_message.get("contact"))
            if not author and clean(raw_message.get("fromMe")).lower() == "true":
                author = profile.target_number

            if canonical_id not in existing_message_ids:
                message_hits = keyword_hits(body, message_keywords)
                new_message_rows.append(
                    {
                        "message_id": canonical_id,
                        "raw_message_id": raw_message_id,
                        "source_name": chat_name,
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
                        "is_relevant": "true",
                    }
                )
                existing_message_ids.add(canonical_id)

            media_payload, error = download_media_with_detail(profile, api_key, raw_message_id)
            if error or not media_payload:
                failures.append(f"{raw_message_id}: {error or 'no_payload'}")
                continue

            file_name = clean(media_payload.get("filename"))
            file_path = clean(media_payload.get("filePath"))
            file_path = normalize_media_file(profile, file_path, file_name)
            media_id = f"{canonical_id}::{file_name}"
            existing_media_row = existing_media_by_id.get(media_id)
            if existing_media_row is not None:
                existing_media_row["relative_path"] = to_relative(file_path)
                existing_media_row["file_name"] = file_name
                existing_media_row["mimetype"] = clean(media_payload.get("mimetype")) or clean(existing_media_row.get("mimetype"))
                existing_media_row["filesize"] = clean(media_payload.get("filesize")) or clean(existing_media_row.get("filesize"))
                continue

            new_media_rows.append(
                {
                    "media_id": media_id,
                    "source_name": chat_name,
                    "source_profile": profile.server,
                    "chat_id": chat_id,
                    "chat_name": chat_name,
                    "message_id": canonical_id,
                    "raw_message_id": raw_message_id,
                    "timestamp": clean(raw_message.get("timestamp")),
                    "author": author,
                    "file_name": file_name,
                    "relative_path": to_relative(file_path),
                    "media_type": media_type_for_message(message_type),
                    "message_type": message_type,
                    "is_relevant": "true",
                    "mimetype": clean(media_payload.get("mimetype")),
                    "filesize": clean(media_payload.get("filesize")),
                }
            )
            existing_media_ids.add(media_id)

        all_message_rows = dedupe_rows(existing_message_rows + new_message_rows, "message_id")
        all_media_rows = dedupe_rows(existing_media_rows + new_media_rows, "media_id")
        all_message_rows.sort(key=lambda row: (clean(row.get("timestamp")), clean(row.get("source_profile")), clean(row.get("chat_id")), clean(row.get("message_id"))))
        all_media_rows.sort(key=lambda row: (clean(row.get("timestamp")), clean(row.get("source_profile")), clean(row.get("chat_id")), clean(row.get("media_id"))))

        write_csv_rows(MESSAGES_CSV_OUTPUT_PATH, all_message_rows, MESSAGE_FIELDNAMES)
        write_messages_json(MESSAGES_JSON_OUTPUT_PATH, all_message_rows)
        write_csv_rows(MEDIA_INDEX_OUTPUT_PATH, all_media_rows, MEDIA_FIELDNAMES)

        print(f"Status: {status}")
        print(f"Chat: {chat_name} ({chat_id})")
        print(f"Fetched messages: {len(messages)}")
        print(f"Media candidates: {len(media_candidates)}")
        print(f"New media rows: {len(new_media_rows)}")
        print(f"New message rows: {len(new_message_rows)}")
        print(f"Failures: {len(failures)}")
        for failure in failures[:20]:
            print(f"Failure: {failure}")
    finally:
        stop_server(process)


if __name__ == "__main__":
    main()
