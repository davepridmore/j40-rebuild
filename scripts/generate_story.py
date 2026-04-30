#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "data" / "config" / "project.json"
MESSAGES_PATH = ROOT / "data" / "processed" / "generated" / "whatsapp_messages.json"
MEDIA_PATH = ROOT / "data" / "processed" / "generated" / "media_index.csv"
EXPENSES_PATH = ROOT / "data" / "manual" / "expenses.csv"
OUTPUT_PATH = ROOT / "docs" / "restoration-story.md"

TOPIC_MAP = {
    "Electrical reset": [
        "wiring",
        "wire",
        "loom",
        "harness",
        "electrical",
        "heat shrink",
        "connector",
        "grommet",
        "battery",
        "speaker",
        "amp",
        "led"
    ],
    "Body and rust": [
        "rust",
        "body",
        "roof",
        "door",
        "hood",
        "floor",
        "panel",
        "primer",
        "epoxy",
        "seam sealer",
        "bedliner",
        "weld",
        "paint"
    ],
    "Steering and suspension": [
        "power steering",
        "steering",
        "shock",
        "bilstein",
        "old man emu",
        "nitrocharger",
        "ome",
        "suspension"
    ],
    "Mechanical baseline": [
        "engine",
        "oil",
        "filter",
        "ac",
        "wiper",
        "brake"
    ],
    "Workshop setup": [
        "tool",
        "grease gun",
        "torque wrench",
        "breaker bar",
        "bench grinder",
        "tap set",
        "cover",
        "dremel",
        "sander"
    ],
}

STORY_KEYWORDS = {
    "bought": 3,
    "bought the jeep": 4,
    "inspection": 3,
    "taking for an oil change": 3,
    "strip": 3,
    "replace the wiring": 4,
    "power steering": 3,
    "battery": 4,
    "buy a car cover": 3,
    "stripped tomorrow": 4,
    "primer": 3,
    "bedliner": 3,
    "arrived": 3,
    "quote": 2,
    "need": 1,
    "plan": 1,
    "new plates": 2,
    "body work": 3,
    "wiring harness": 3
}


def load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def load_messages() -> list[dict]:
    return json.loads(MESSAGES_PATH.read_text(encoding="utf-8"))


def load_media_rows() -> list[dict]:
    with MEDIA_PATH.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_expenses() -> list[dict]:
    with EXPENSES_PATH.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_amount(value: str) -> int | None:
    if not value:
        return None
    try:
        return int(float(value))
    except ValueError:
        return None


def topic_counts(messages: list[dict]) -> list[tuple[str, int]]:
    counts: Counter[str] = Counter()
    for message in messages:
        text = message["clean_text"].lower()
        for label, tokens in TOPIC_MAP.items():
            if any(token in text for token in tokens):
                counts[label] += 1
    return counts.most_common()


def story_score(message: dict) -> int:
    if not message["is_relevant"] or message["is_system"]:
        return -10

    text = message["clean_text"].lower()
    if not text:
        return -5

    score = 0
    for token, weight in STORY_KEYWORDS.items():
        if token in text:
            score += weight

    if message["amounts"]:
        score += 4
    if message["attachments"]:
        score += 1
    if message["is_reference_dump"]:
        score -= 8
    if len(text) > 220:
        score -= 1

    return score


def clip_text(text: str, width: int = 180) -> str:
    text = text.strip()
    if len(text) <= width:
        return text
    return text[: width - 1].rstrip() + "…"


def select_timeline(messages: list[dict]) -> dict[str, list[dict]]:
    by_date: defaultdict[str, list[dict]] = defaultdict(list)
    for message in messages:
        score = story_score(message)
        if score >= 2 and message["clean_text"].strip():
            candidate = dict(message)
            candidate["story_score"] = score
            by_date[message["date"]].append(candidate)

    curated: dict[str, list[dict]] = {}
    for date_key, items in sorted(by_date.items()):
        items.sort(key=lambda item: (item["is_reference_dump"], -item["story_score"], item["timestamp"]))
        chosen: list[dict] = []
        seen_texts: set[str] = set()
        for item in items:
            if item["clean_text"] in seen_texts:
                continue
            chosen.append(item)
            seen_texts.add(item["clean_text"])
            if len(chosen) == 4:
                break
        if chosen:
            curated[date_key] = chosen
    return curated


def spend_summary(expenses: list[dict]) -> tuple[dict[str, int], list[dict], list[dict], list[dict]]:
    confirmed_totals: Counter[str] = Counter()
    confirmed_rows: list[dict] = []
    quote_rows: list[dict] = []
    unpriced_rows: list[dict] = []

    for row in expenses:
        amount = parse_amount(row["amount"])
        amount_status = row["amount_status"]
        status = row["status"]
        bucket = row["bucket"]

        if amount_status == "confirmed" and amount is not None:
            if status == "quote":
                quote_rows.append(row)
            else:
                confirmed_totals[bucket] += amount
                confirmed_rows.append(row)
        elif amount_status == "missing" and status in {"received", "planned", "researching", "installed"}:
            unpriced_rows.append(row)

    return dict(confirmed_totals), confirmed_rows, quote_rows, unpriced_rows


def render_story(config: dict, messages: list[dict], media_rows: list[dict], expenses: list[dict]) -> str:
    relevant_messages = [message for message in messages if message["is_relevant"]]
    relevant_media = [row for row in media_rows if row.get("is_relevant") in (True, "True", "true", "1")]
    topic_summary = topic_counts(relevant_messages)
    timeline = select_timeline(relevant_messages)
    confirmed_totals, confirmed_rows, quote_rows, unpriced_rows = spend_summary(expenses)

    restoration_total = sum(
        amount for bucket, amount in confirmed_totals.items() if bucket in {"tools", "parts", "labour"}
    )
    admin_total = confirmed_totals.get("admin", 0)
    source_counts = Counter(message["source_name"] for message in relevant_messages)

    lines: list[str] = []
    lines.append(f"# {config['project_name']}")
    lines.append("")
    lines.append("## Snapshot")
    lines.append("")
    lines.append(f"- Vehicle: {config['vehicle']}")
    lines.append(f"- Relevant chat messages indexed: {len(relevant_messages)}")
    lines.append(f"- Relevant media items indexed: {len(relevant_media)}")
    lines.append(f"- Evidence sources in use: {', '.join(f'{name} ({count})' for name, count in sorted(source_counts.items()))}")
    lines.append(f"- Confirmed restoration spend so far: PKR {restoration_total:,}")
    lines.append(f"- Confirmed admin spend tracked separately: PKR {admin_total:,}")
    lines.append(f"- Quoted but not confirmed as purchased: PKR {sum(parse_amount(row['amount']) or 0 for row in quote_rows):,}")
    lines.append(f"- Purchased / planned items still missing prices: {len(unpriced_rows)}")
    lines.append("")
    lines.append("## Main Workstreams")
    lines.append("")
    for label, count in topic_summary[:5]:
        lines.append(f"- {label}: mentioned across {count} relevant messages")
    lines.append("")
    lines.append("## Timeline")
    lines.append("")
    for date_key, items in timeline.items():
        lines.append(f"### {date_key}")
        lines.append("")
        for item in items:
            lines.append(
                f"- {item['time'][:5]} `{item['source_name']}` {item['author']}: {clip_text(item['clean_text'])}"
            )
        lines.append("")
    lines.append("## Confirmed Spend")
    lines.append("")
    if confirmed_rows:
        for row in confirmed_rows:
            amount = parse_amount(row["amount"]) or 0
            lines.append(f"- {row['date'] or 'Unknown date'} `{row['bucket']}` {row['item']}: PKR {amount:,}")
    else:
        lines.append("- No confirmed spend rows yet.")
    lines.append("")
    lines.append("## Quote Watchlist")
    lines.append("")
    if quote_rows:
        for row in quote_rows:
            amount = parse_amount(row["amount"]) or 0
            lines.append(f"- {row['date'] or 'Unknown date'} {row['item']}: PKR {amount:,}")
    else:
        lines.append("- No quotes captured yet.")
    lines.append("")
    lines.append("## Unpriced Items To Backfill")
    lines.append("")
    for row in unpriced_rows[:20]:
        lines.append(f"- `{row['status']}` {row['item']}")
    if len(unpriced_rows) > 20:
        lines.append(f"- Plus {len(unpriced_rows) - 20} more items in `data/manual/expenses.csv`")
    lines.append("")
    lines.append("## Notes")
    lines.append("")
    lines.append("- This draft only includes build-relevant messages from the supplied WhatsApp exports.")
    lines.append("- The direct Akber chat was filtered to the March 2026 restoration discussion and adjacent build context.")
    lines.append("- Gmail / order-status evidence is not ingested yet. Add exported order emails later to tighten delivery tracking.")
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    config = load_config()
    messages = load_messages()
    media_rows = load_media_rows()
    expenses = load_expenses()
    OUTPUT_PATH.write_text(render_story(config, messages, media_rows, expenses), encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
