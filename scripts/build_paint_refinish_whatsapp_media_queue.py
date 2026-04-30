from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
GENERATED_DIR = ROOT / "data" / "processed" / "generated"
MANUAL_DIR = ROOT / "data" / "manual"

MESSAGES_PATH = GENERATED_DIR / "whatsapp_messages.json"
MEDIA_INDEX_PATH = GENERATED_DIR / "media_index.csv"
MCP_MESSAGES_PATH = GENERATED_DIR / "mcp_whatsapp_j40_messages.json"
MCP_MEDIA_INDEX_PATH = GENERATED_DIR / "mcp_whatsapp_j40_media_index.csv"
OUTPUT_PATH = MANUAL_DIR / "paint_refinish_whatsapp_media_queue.csv"

CONTEXT_WINDOW = 6
CLUSTER_DISTANCE = 3

ALLOWED_BUCKETS = {
    "prepared_for_send_out",
    "returned_from_painter",
    "in_progress_video",
}

PAINT_CONTEXT_PATTERNS = (
    re.compile(r"\b(?:paint|painter|paintshop|bodywork|denter|primer|sanding|spray|refinish|rechrom(?:e|ed)?)\b", re.IGNORECASE),
)
PART_CONTEXT_PATTERNS = (
    re.compile(
        r"\b(?:roof|door|doors|panel|panels|bonnet|hood|fender|wing|hatch|tailgate|body|parts?|hinges?|latches?|trim|nuts?\s*bolts?|hardware|chrome)\b",
        re.IGNORECASE,
    ),
)
SEND_PATTERNS = (
    re.compile(
        r"\b(?:send|sending|sent|dispatch(?:ed)?|outbound)\b.{0,120}\b(?:repair|paint|painter|re-?paint|bodywork|denter|vendor|shop)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:roof|doors?|panels?|bonnet|wing|parts?)\b.{0,80}\b(?:send|sending|sent|dispatch(?:ed)?)\b",
        re.IGNORECASE,
    ),
    re.compile(r"\bready\s+for\s+(?:paint|painter|bodywork|send(?:-?out)?)\b", re.IGNORECASE),
)
RETURN_PATTERNS = (
    re.compile(
        r"\b(?:returned?|received|came\s+back|back\s+from|collected)\b.{0,120}\b(?:paint(?:er|shop)?|bodywork|denter|refinish)\b",
        re.IGNORECASE,
    ),
    re.compile(r"\b(?:refinish(?:ed)?|rechrom(?:e|ed)|painted)\b", re.IGNORECASE),
)
PROGRESS_PATTERNS = (
    re.compile(r"\b(?:sanding|sand|primer|spray|filler|putty|prep|preparation|bodywork|denting|painting|paint\s*work|rubbed\s*down)\b", re.IGNORECASE),
    re.compile(r"\brestor(?:e|ing|ation)\b", re.IGNORECASE),
)
STRONG_SEND_PATTERN = re.compile(r"\b(?:sent\s+off|send\s+out|dispatch(?:ed)?\s+to|ready\s+for\s+paint)\b", re.IGNORECASE)
STRONG_RETURN_PATTERN = re.compile(r"\b(?:returned?\s+from|came\s+back|refinish(?:ed)?|rechrom(?:e|ed)|painted\s+parts?)\b", re.IGNORECASE)

KEYWORD_TERMS = (
    "paint",
    "painter",
    "bodywork",
    "primer",
    "sanding",
    "spray",
    "refinish",
    "rechromed",
    "door",
    "panel",
    "roof",
    "wing",
    "bonnet",
    "hood",
    "send",
    "sent",
    "dispatch",
    "returned",
    "received",
    "prep",
)


def load_json_rows(path: Path) -> list[dict]:
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        return []
    return [row for row in payload if isinstance(row, dict)]


def load_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_messages() -> list[dict]:
    combined: list[dict] = []
    seen_ids: set[str] = set()

    for row in load_json_rows(MESSAGES_PATH):
        message_id = clean_text(row.get("message_id"))
        if not message_id or message_id in seen_ids:
            continue
        seen_ids.add(message_id)
        combined.append(row)

    for row in load_json_rows(MCP_MESSAGES_PATH):
        message_id = clean_text(row.get("message_id"))
        if not message_id or message_id in seen_ids:
            continue
        seen_ids.add(message_id)
        combined.append(
            {
                "message_id": message_id,
                "source_name": row.get("source_name", ""),
                "timestamp": row.get("timestamp", ""),
                "author": row.get("author", ""),
                "clean_text": row.get("clean_text") or row.get("body", ""),
                "text": row.get("body", ""),
                "is_relevant": row.get("is_relevant", "true"),
            }
        )
    return combined


def load_media_rows() -> list[dict[str, str]]:
    combined: list[dict[str, str]] = []
    seen_ids: set[str] = set()
    for path in (MEDIA_INDEX_PATH, MCP_MEDIA_INDEX_PATH):
        for row in load_csv_rows(path):
            media_id = clean_text(row.get("media_id"))
            if not media_id or media_id in seen_ids:
                continue
            seen_ids.add(media_id)
            combined.append(row)
    return combined


def parse_message_sequence(message_id: str) -> int:
    match = re.search(r"-(\d+)$", message_id or "")
    return int(match.group(1)) if match else -1


def clean_text(value: str) -> str:
    return " ".join((value or "").replace("\u200e", " ").split())


def text_matches(patterns: tuple[re.Pattern[str], ...], text: str) -> bool:
    return any(pattern.search(text) for pattern in patterns)


def extract_keyword_hits(text: str) -> list[str]:
    lowered = text.lower()
    hits: list[str] = []
    for term in KEYWORD_TERMS:
        pattern = rf"(?<!\w){re.escape(term)}(?!\w)"
        if re.search(pattern, lowered):
            hits.append(term)
    return sorted(set(hits))


def truncate_text(value: str, limit: int = 240) -> str:
    if len(value) <= limit:
        return value
    return value[: limit - 3].rstrip() + "..."


def build_context_lookup(messages: list[dict]) -> tuple[dict[str, list[dict]], dict[str, tuple[str, int]]]:
    by_source: dict[str, list[dict]] = defaultdict(list)
    for message in messages:
        by_source[message["source_name"]].append(message)

    for source_messages in by_source.values():
        source_messages.sort(
            key=lambda message: (
                parse_message_sequence(message.get("message_id", "")),
                message.get("timestamp", ""),
            )
        )

    message_position: dict[str, tuple[str, int]] = {}
    for source_name, source_messages in by_source.items():
        for index, message in enumerate(source_messages):
            message_position[message["message_id"]] = (source_name, index)

    return by_source, message_position


def get_context_text(messages: list[dict], center_index: int) -> str:
    snippets: list[str] = []
    start = max(0, center_index - CONTEXT_WINDOW)
    end = min(len(messages), center_index + CONTEXT_WINDOW + 1)
    for index in range(start, end):
        message = messages[index]
        text = clean_text(message.get("clean_text") or message.get("text") or "")
        if text:
            snippets.append(text)
    return " ".join(snippets)


def classify_media_row(row: dict[str, str], context_text: str) -> tuple[str, str, str]:
    media_type = (row.get("media_type") or "").strip().lower()

    send_hit = text_matches(SEND_PATTERNS, context_text)
    return_hit = text_matches(RETURN_PATTERNS, context_text)
    paint_hit = text_matches(PAINT_CONTEXT_PATTERNS, context_text)
    part_hit = text_matches(PART_CONTEXT_PATTERNS, context_text)
    progress_hit = text_matches(PROGRESS_PATTERNS, context_text)

    if send_hit and part_hit:
        confidence = "high" if STRONG_SEND_PATTERN.search(context_text) else "medium"
        return "prepared_for_send_out", confidence, "send_context"
    if return_hit and (paint_hit or part_hit):
        confidence = "high" if STRONG_RETURN_PATTERN.search(context_text) else "medium"
        return "returned_from_painter", confidence, "return_context"
    if media_type == "video" and (progress_hit or paint_hit):
        confidence = "medium" if progress_hit else "low"
        return "in_progress_video", confidence, "progress_context"
    return "", "", ""


def build_output_rows(media_rows: list[dict[str, str]], messages: list[dict]) -> list[dict[str, str]]:
    message_by_id = {message["message_id"]: message for message in messages}
    by_source, message_position = build_context_lookup(messages)

    draft_rows: list[dict[str, str]] = []

    for media_row in media_rows:
        media_type = (media_row.get("media_type") or "").strip().lower()
        if media_type not in {"photo", "video"}:
            continue

        message_id = media_row.get("message_id", "")
        if not message_id or message_id not in message_position:
            continue

        source_name, message_index = message_position[message_id]
        source_messages = by_source[source_name]
        context_text = get_context_text(source_messages, message_index)
        evidence_bucket, confidence, reason = classify_media_row(media_row, context_text)
        keyword_hits = extract_keyword_hits(context_text)

        message = message_by_id.get(message_id, {})

        draft_rows.append(
            {
                "media_id": media_row.get("media_id", ""),
                "source_name": media_row.get("source_name", ""),
                "message_id": message_id,
                "timestamp": media_row.get("timestamp", ""),
                "author": media_row.get("author", ""),
                "file_name": media_row.get("file_name", ""),
                "relative_path": media_row.get("relative_path", ""),
                "media_type": media_type,
                "is_relevant": media_row.get("is_relevant", ""),
                "evidence_bucket": evidence_bucket,
                "classification_confidence": confidence,
                "classification_reason": reason,
                "keyword_hits": "|".join(keyword_hits),
                "context_excerpt": truncate_text(context_text),
                "_source_name": source_name,
                "_sequence": str(parse_message_sequence(message_id)),
                "_message_relevant": str(bool(message.get("is_relevant", False))).lower(),
            }
        )

    rows_by_source: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in draft_rows:
        rows_by_source[row["_source_name"]].append(row)

    for source_rows in rows_by_source.values():
        source_rows.sort(key=lambda row: int(row["_sequence"]))
        anchors = [row for row in source_rows if row["evidence_bucket"] in {"prepared_for_send_out", "returned_from_painter"}]

        for row in source_rows:
            if row["evidence_bucket"]:
                continue

            sequence = int(row["_sequence"])
            nearby_anchors = [anchor for anchor in anchors if abs(int(anchor["_sequence"]) - sequence) <= CLUSTER_DISTANCE]
            if nearby_anchors:
                nearest = min(nearby_anchors, key=lambda anchor: abs(int(anchor["_sequence"]) - sequence))
                row["evidence_bucket"] = nearest["evidence_bucket"]
                row["classification_confidence"] = "low"
                row["classification_reason"] = "adjacent_media_cluster"

    for row in draft_rows:
        if row["evidence_bucket"]:
            continue
        if row["media_type"] == "video":
            row["evidence_bucket"] = "in_progress_video"
            row["classification_confidence"] = "low"
            row["classification_reason"] = "video_default"

    output_rows = [row for row in draft_rows if row["evidence_bucket"] in ALLOWED_BUCKETS]
    output_rows.sort(key=lambda row: (row["timestamp"], row["source_name"], row["message_id"], row["file_name"]))

    cleaned_rows: list[dict[str, str]] = []
    for row in output_rows:
        cleaned_rows.append(
            {
                "media_id": row["media_id"],
                "source_name": row["source_name"],
                "message_id": row["message_id"],
                "timestamp": row["timestamp"],
                "author": row["author"],
                "file_name": row["file_name"],
                "relative_path": row["relative_path"],
                "media_type": row["media_type"],
                "is_relevant": row["is_relevant"],
                "evidence_bucket": row["evidence_bucket"],
                "classification_confidence": row["classification_confidence"],
                "classification_reason": row["classification_reason"],
                "keyword_hits": row["keyword_hits"],
                "context_excerpt": row["context_excerpt"],
            }
        )
    return cleaned_rows


def write_csv(rows: list[dict[str, str]]) -> None:
    fieldnames = [
        "media_id",
        "source_name",
        "message_id",
        "timestamp",
        "author",
        "file_name",
        "relative_path",
        "media_type",
        "is_relevant",
        "evidence_bucket",
        "classification_confidence",
        "classification_reason",
        "keyword_hits",
        "context_excerpt",
    ]
    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    messages = load_messages()
    media_rows = load_media_rows()
    output_rows = build_output_rows(media_rows, messages)
    write_csv(output_rows)

    bucket_counts = Counter(row["evidence_bucket"] for row in output_rows)
    confidence_counts = Counter(row["classification_confidence"] for row in output_rows)
    print(f"Wrote WhatsApp paint queue: {OUTPUT_PATH.relative_to(ROOT)}")
    print(f"Rows: {len(output_rows)}")
    for bucket in ("prepared_for_send_out", "returned_from_painter", "in_progress_video"):
        print(f"{bucket}: {bucket_counts.get(bucket, 0)}")
    for confidence in ("high", "medium", "low"):
        print(f"{confidence}: {confidence_counts.get(confidence, 0)}")


if __name__ == "__main__":
    main()
