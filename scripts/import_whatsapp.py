#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
import shutil
import zipfile
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "data" / "config" / "project.json"
RAW_IMPORTS_DIR = ROOT / "data" / "raw" / "imports"
GENERATED_DIR = ROOT / "data" / "processed" / "generated"

MESSAGE_RE = re.compile(
    r"^\u200e?\[(?P<date>\d{2}/\d{2}/\d{4}), (?P<time>\d{2}:\d{2}:\d{2})\] (?P<author>[^:]+): (?P<text>.*)$"
)
ATTACHMENT_RE = re.compile(r"<attached: ([^>]+)>")
URL_RE = re.compile(r"https?://\S+")
PKR_PREFIX_RE = re.compile(r"\bPKR\s?([\d,]+(?:\.\d+)?)\b", re.IGNORECASE)
PKR_SUFFIX_RE = re.compile(r"\b([\d,]+(?:\.\d+)?)\s?PKR\b", re.IGNORECASE)
K_RE = re.compile(r"\b(\d+(?:\.\d+)?)k\b", re.IGNORECASE)

SYSTEM_MARKERS = (
    "messages and calls are end-to-end encrypted",
    "created group",
    "added you",
    "added ",
    "removed ",
    "changed this group's icon",
    "changed the group description",
    "you deleted this message",
    "this message was deleted",
    "voice call",
    "missed voice call"
)

MEDIA_EXTENSIONS = {
    ".jpg": "photo",
    ".jpeg": "photo",
    ".png": "photo",
    ".webp": "sticker",
    ".mp4": "video",
    ".opus": "audio",
    ".pdf": "document",
    ".vcf": "contact"
}


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")


def load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def ensure_generated_dirs() -> None:
    RAW_IMPORTS_DIR.mkdir(parents=True, exist_ok=True)
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)


def extract_zip(source: dict) -> Path:
    zip_path = Path(source["zip_path"]).expanduser()
    if not zip_path.exists():
        raise FileNotFoundError(f"Missing WhatsApp export: {zip_path}")

    destination = RAW_IMPORTS_DIR / slugify(source["name"])
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path) as archive:
        archive.extractall(destination)

    return destination


def parse_chat(chat_path: Path, source_name: str) -> list[dict]:
    lines = chat_path.read_text(encoding="utf-8-sig", errors="replace").splitlines()
    messages: list[dict] = []
    current: dict | None = None

    def flush() -> None:
        nonlocal current
        if current is None:
            return
        current["text"] = current["text"].rstrip()
        messages.append(current)
        current = None

    for raw_line in lines:
        match = MESSAGE_RE.match(raw_line)
        if match:
            flush()
            dt = datetime.strptime(
                f"{match.group('date')} {match.group('time')}",
                "%d/%m/%Y %H:%M:%S",
            )
            current = {
                "source_name": source_name,
                "timestamp": dt.isoformat(timespec="seconds"),
                "date": dt.date().isoformat(),
                "time": dt.time().isoformat(),
                "author": match.group("author").strip(),
                "text": match.group("text").strip(),
            }
            continue

        if current is None:
            continue

        if current["text"]:
            current["text"] += "\n" + raw_line
        else:
            current["text"] = raw_line

    flush()
    for index, message in enumerate(messages, start=1):
        message["message_id"] = f"{slugify(source_name)}-{index:05d}"
    return messages


def extract_amounts(text: str) -> list[dict]:
    amounts: list[dict] = []
    seen: set[tuple[str, int]] = set()

    for match in PKR_PREFIX_RE.finditer(text):
        value = int(float(match.group(1).replace(",", "")))
        key = ("PKR", value)
        if key not in seen:
            seen.add(key)
            amounts.append({"currency": "PKR", "amount": value, "raw": match.group(0)})

    for match in PKR_SUFFIX_RE.finditer(text):
        value = int(float(match.group(1).replace(",", "")))
        key = ("PKR", value)
        if key not in seen:
            seen.add(key)
            amounts.append({"currency": "PKR", "amount": value, "raw": match.group(0)})

    for match in K_RE.finditer(text):
        value = int(float(match.group(1)) * 1000)
        key = ("PKR", value)
        if key not in seen:
            seen.add(key)
            amounts.append({"currency": "PKR", "amount": value, "raw": match.group(0)})

    return amounts


def classify_cost_hint(text: str) -> str:
    lowered = text.lower()
    if any(token in lowered for token in ("quote", "aliexpress", "wiring harness", "kit", "pkr43,570", "pkr34,249")):
        return "quote"
    if any(token in lowered for token in ("paid", "transfer", "down on", "back on the old one", "new battery", "arrived", "inspection", "challan")):
        return "spend"
    return "mentioned"


def clean_text(text: str) -> str:
    text = ATTACHMENT_RE.sub("", text)
    return re.sub(r"\s+", " ", text).strip()


def keyword_present(text: str, keyword: str) -> bool:
    escaped = re.escape(keyword.lower())
    if any(character.isalnum() for character in keyword):
        pattern = rf"(?<!\w){escaped}(?!\w)"
        return re.search(pattern, text) is not None
    return keyword.lower() in text


def topic_hits(text: str, keywords: Iterable[str]) -> list[str]:
    lowered = text.lower()
    return sorted({keyword for keyword in keywords if keyword_present(lowered, keyword)})


def should_seed_relevance(message: dict, source: dict, config: dict) -> bool:
    lowered = message["text"].lower()
    include_hits = topic_hits(lowered, config["include_keywords"])
    exclude_hits = topic_hits(lowered, config["exclude_keywords"])
    message["keyword_hits"] = include_hits
    message["exclude_hits"] = exclude_hits
    message["attachments"] = ATTACHMENT_RE.findall(message["text"])
    message["clean_text"] = clean_text(message["text"])
    message["urls"] = URL_RE.findall(message["text"])
    message["amounts"] = extract_amounts(message["text"])
    message["has_amounts"] = bool(message["amounts"])
    message["has_attachments"] = bool(message["attachments"])
    message["is_reference_dump"] = len(message["text"]) > 350 or message["text"].count("\n") >= 5
    message["is_system"] = any(marker in lowered for marker in SYSTEM_MARKERS)

    if source.get("include_all_non_system_messages"):
        return not message["is_system"]

    include_after = source.get("include_after")
    if include_after and message["date"] < include_after:
        return False

    if message["is_system"] or exclude_hits:
        return False

    if include_hits or message["has_amounts"]:
        return True

    if message["has_attachments"] and include_hits:
        return True

    return False


def apply_relevance_rules(messages: list[dict], source: dict, config: dict) -> list[dict]:
    if source.get("include_all_non_system_messages"):
        for message in messages:
            message["relevance_reason"] = "group_non_system" if message["is_relevant"] else "system"
        return messages

    window = int(source.get("cluster_window", 2))
    cluster_minutes = int(source.get("cluster_minutes", 120))
    for index, message in enumerate(messages):
        if message["is_relevant"]:
            message["relevance_reason"] = "keyword_or_amount"
            continue

        if message["is_system"] or message["exclude_hits"]:
            message["relevance_reason"] = "excluded"
            continue

        nearby = messages[max(0, index - window): index + window + 1]
        same_day_seed = any(
            neighbor["date"] == message["date"]
            and neighbor.get("seed_relevant", False)
            and abs(
                (
                    datetime.fromisoformat(neighbor["timestamp"])
                    - datetime.fromisoformat(message["timestamp"])
                ).total_seconds()
            )
            <= cluster_minutes * 60
            for neighbor in nearby
            if neighbor is not message
        )
        concise_follow_up = len(message["clean_text"]) <= 180 or message["has_attachments"] or message["urls"]

        if same_day_seed and concise_follow_up:
            message["is_relevant"] = True
            message["relevance_reason"] = "adjacent_cluster"
        else:
            message["relevance_reason"] = "filtered_out"

    return messages


def build_messages(config: dict) -> tuple[list[dict], list[dict]]:
    all_messages: list[dict] = []
    media_rows: list[dict] = []

    for source in config["sources"]:
        extracted_dir = extract_zip(source)
        chat_path = extracted_dir / "_chat.txt"
        source_messages = parse_chat(chat_path, source["name"])

        for message in source_messages:
            message["source_kind"] = source["kind"]
            message["seed_relevant"] = should_seed_relevance(message, source, config)
            message["is_relevant"] = message["seed_relevant"]

        source_messages = apply_relevance_rules(source_messages, source, config)
        all_messages.extend(source_messages)

        for message in source_messages:
            for attachment_name in message["attachments"]:
                attachment_path = extracted_dir / attachment_name
                media_rows.append(
                    {
                        "media_id": f"{message['message_id']}::{attachment_name}",
                        "source_name": source["name"],
                        "message_id": message["message_id"],
                        "timestamp": message["timestamp"],
                        "author": message["author"],
                        "file_name": attachment_name,
                        "relative_path": str(attachment_path.relative_to(ROOT)),
                        "media_type": MEDIA_EXTENSIONS.get(attachment_path.suffix.lower(), "file"),
                        "is_relevant": message["is_relevant"],
                    }
                )

    return all_messages, media_rows


def build_manual_photo_rows(config: dict) -> list[dict]:
    photo_inbox = ROOT / config["photo_inbox"]
    rows: list[dict] = []
    if not photo_inbox.exists():
        return rows

    for path in sorted(photo_inbox.rglob("*")):
        if not path.is_file():
            continue
        rows.append(
            {
                "media_id": f"manual::{path.name}",
                "source_name": "manual_photo_inbox",
                "message_id": "",
                "timestamp": "",
                "author": "",
                "file_name": path.name,
                "relative_path": str(path.relative_to(ROOT)),
                "media_type": MEDIA_EXTENSIONS.get(path.suffix.lower(), "file"),
                "is_relevant": True,
            }
        )

    return rows


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_outputs(messages: list[dict], media_rows: list[dict]) -> None:
    relevant_messages = [message for message in messages if message["is_relevant"]]
    cost_rows: list[dict] = []

    for message in relevant_messages:
        for amount in message["amounts"]:
            cost_rows.append(
                {
                    "source_name": message["source_name"],
                    "message_id": message["message_id"],
                    "date": message["date"],
                    "author": message["author"],
                    "amount": amount["amount"],
                    "currency": amount["currency"],
                    "raw_match": amount["raw"],
                    "hint": classify_cost_hint(message["clean_text"]),
                    "text": message["clean_text"],
                }
            )

    message_summary_rows = []
    for message in relevant_messages:
        message_summary_rows.append(
            {
                "message_id": message["message_id"],
                "source_name": message["source_name"],
                "timestamp": message["timestamp"],
                "author": message["author"],
                "relevance_reason": message["relevance_reason"],
                "keyword_hits": "|".join(message["keyword_hits"]),
                "amount_count": len(message["amounts"]),
                "attachment_count": len(message["attachments"]),
                "text": message["clean_text"],
            }
        )

    write_json(GENERATED_DIR / "whatsapp_messages.json", messages)
    write_csv(
        GENERATED_DIR / "relevant_messages.csv",
        message_summary_rows,
        [
            "message_id",
            "source_name",
            "timestamp",
            "author",
            "relevance_reason",
            "keyword_hits",
            "amount_count",
            "attachment_count",
            "text",
        ],
    )
    write_csv(
        GENERATED_DIR / "media_index.csv",
        media_rows,
        [
            "media_id",
            "source_name",
            "message_id",
            "timestamp",
            "author",
            "file_name",
            "relative_path",
            "media_type",
            "is_relevant",
        ],
    )
    write_csv(
        GENERATED_DIR / "cost_candidates.csv",
        cost_rows,
        [
            "source_name",
            "message_id",
            "date",
            "author",
            "amount",
            "currency",
            "raw_match",
            "hint",
            "text",
        ],
    )

    summary = {
        "messages_total": len(messages),
        "messages_relevant": len(relevant_messages),
        "media_total": len(media_rows),
        "media_relevant": sum(1 for row in media_rows if row["is_relevant"]),
        "cost_candidates": len(cost_rows),
        "sources": Counter(message["source_name"] for message in relevant_messages),
    }
    write_json(GENERATED_DIR / "import_summary.json", summary)


def main() -> None:
    ensure_generated_dirs()
    config = load_config()
    messages, media_rows = build_messages(config)
    media_rows.extend(build_manual_photo_rows(config))
    write_outputs(messages, media_rows)
    print(f"Imported {len(messages)} WhatsApp messages")
    print(f"Relevant messages: {sum(1 for message in messages if message['is_relevant'])}")
    print(f"Indexed media items: {len(media_rows)}")


if __name__ == "__main__":
    main()
