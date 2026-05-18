#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import html as html_lib
import json
import os
import re
import select
import subprocess
import sys
import time
from collections import Counter
from datetime import date, datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
GENERATED_DIR = ROOT / "data" / "processed" / "generated"
MANUAL_DIR = ROOT / "data" / "manual"
AUDIT_QUEUE_PATH = MANUAL_DIR / "orders_receipts_audit_queue.csv"
DEFAULT_CREDENTIALS_PATH = ROOT / "client_secret_969930271813-7128p3h5nduj101tvbapconlnif7mm0a.apps.googleusercontent.com.json"

MCP_PACKAGE = "@dguido/google-workspace-mcp@3.4.4"
MCP_PROFILE = "j40-orders-receipts"
MCP_SERVICES = "gmail,drive"
PROTOCOL_VERSION = "2024-11-05"

PROJECT_TERMS = {
    "j40",
    "fj40",
    "j50",
    "fj50",
    "land cruiser",
    "landcruiser",
    "toyota",
    "chassis",
    "bodyshop",
    "body shop",
    "suspension",
    "brake",
    "clutch",
    "wiring",
    "loom",
    "harness",
    "connector",
    "headlight",
    "fuse",
    "relay",
    "battery",
    "alternator",
    "radiator",
    "hose",
    "rubber",
    "grommet",
    "fastener",
    "primer",
    "epoxy",
    "paint",
    "weld",
    "welding",
    "evaporator",
    "blower",
    "hvac",
    "ac",
}

SUPPLIER_TERMS = {
    "aliexpress",
    "autohub",
    "daraz",
    "tools mart",
    "toolsmart",
    "toolsmart.pk",
    "toolsmartpk",
    "mtl parts",
    "millat",
    "powerhouse",
    "postex",
    "leopard",
    "blue-ex",
    "blueex",
    "coolsun",
    "longman",
    "happilac",
    "arsalan",
    "snow cool",
    "mm paint",
    "adenwalla",
}

ORDER_TERMS = {
    "order",
    "confirmation",
    "confirmed",
    "shipped",
    "dispatch",
    "tracking",
    "delivered",
    "delivery",
    "receipt",
    "invoice",
    "payment",
    "paid",
    "out for delivery",
    "feedback",
    "review",
}

EXCLUDE_TERMS = {
    "foodpanda",
    "restaurant",
    "kfc",
    "spotify",
    "netflix",
    "linkedin",
    "british airways",
    "ba.com",
    "medium newsletter",
    "medium.com",
    "reading books",
    "facebook",
    "instagram",
    "google security",
    "verification code",
    "otp",
    "one-time password",
    "hsbc",
    "hmrc",
    "companies house",
    "tax return",
    "corporation tax",
    "payroll",
}

CURRENCY_RE = re.compile(r"\bPKR\s*([\d,]+(?:\.\d+)?)\b|\bRs\.?\s*([\d,]+(?:\.\d+)?)\b", re.IGNORECASE)
PART_CODE_PATTERNS = [
    re.compile(r"\bTM\d{4,}\b", re.IGNORECASE),
    re.compile(r"\b24\d{10,15}\b"),
    re.compile(r"\b30\d{10,16}\b"),
    re.compile(r"\b17\d{4,}\b"),
    re.compile(r"\b[A-Z]{2,}[A-Z0-9-]*\d[A-Z0-9-]{2,}\b", re.IGNORECASE),
    re.compile(r"\b(?:PostEx|Leopard|Blue-?ex)\s*[A-Z0-9-]+\b", re.IGNORECASE),
]

CSV_FIELDS = [
    "channel",
    "message_id",
    "date_utc",
    "category",
    "subcategory",
    "source",
    "subject_or_ref",
    "product_or_topic",
    "part_number_or_code",
    "amount_pkr",
    "status",
    "action_required",
    "notes",
]


def clean(value: Any) -> str:
    if value is None:
        return ""
    return " ".join(str(value).replace("\u200e", " ").split())


def html_to_text(value: Any) -> str:
    raw = str(value or "")
    if not raw:
        return ""
    raw = re.sub(r"(?is)<(script|style).*?>.*?</\1>", " ", raw)
    raw = re.sub(r"(?i)<br\s*/?>", " ", raw)
    raw = re.sub(r"(?i)</(p|div|tr|td|th|li|h[1-6])>", " ", raw)
    raw = re.sub(r"<[^>]+>", " ", raw)
    return html_lib.unescape(clean(raw))


def redact_private_details(value: str) -> str:
    redacted = re.sub(r"\bAddress:\s+.*?\s+\bPhone:", "Address: [redacted] Phone:", value, flags=re.IGNORECASE)
    redacted = re.sub(r"\bPhone:\s*\+?\d[\d\s().-]{6,}", "Phone: [redacted]", redacted, flags=re.IGNORECASE)
    redacted = re.sub(
        r"\bEmail:\s*[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}",
        "Email: [redacted]",
        redacted,
        flags=re.IGNORECASE,
    )
    redacted = redacted.replace("[redacted]Email:", "[redacted] Email:")
    return redacted


def norm(value: Any) -> str:
    return clean(value).lower()


def has_term(text: str, term: str) -> bool:
    if not term:
        return False
    if " " in term or "-" in term or "." in term:
        return term in text
    return bool(re.search(rf"(?<![a-z0-9]){re.escape(term)}(?![a-z0-9])", text))


def term_hits(text: str, terms: set[str]) -> list[str]:
    return sorted(term for term in terms if has_term(text, term))


def load_credentials_env() -> dict[str, str]:
    env = os.environ.copy()
    if env.get("GOOGLE_CLIENT_ID") and env.get("GOOGLE_CLIENT_SECRET"):
        return env

    credentials_path = Path(env.get("GOOGLE_WORKSPACE_CREDENTIALS_PATH") or DEFAULT_CREDENTIALS_PATH)
    if not credentials_path.exists():
        raise FileNotFoundError(f"Missing Google credentials file: {credentials_path}")

    payload = json.loads(credentials_path.read_text(encoding="utf-8"))
    installed = payload.get("installed") or payload
    client_id = clean(installed.get("client_id"))
    client_secret = clean(installed.get("client_secret"))
    if not client_id or not client_secret:
        raise RuntimeError(f"Could not load Google client credentials from {credentials_path}")

    env["GOOGLE_CLIENT_ID"] = client_id
    env["GOOGLE_CLIENT_SECRET"] = client_secret
    return env


class McpClient:
    def __init__(self) -> None:
        env = load_credentials_env()
        env["GOOGLE_WORKSPACE_MCP_PROFILE"] = env.get("GOOGLE_WORKSPACE_MCP_PROFILE") or MCP_PROFILE
        env["GOOGLE_WORKSPACE_SERVICES"] = env.get("GOOGLE_WORKSPACE_SERVICES") or MCP_SERVICES
        self.process = subprocess.Popen(
            ["npx", "-y", MCP_PACKAGE, "start"],
            cwd=ROOT,
            env=env,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        self.next_id = 0

    def close(self) -> None:
        if self.process.poll() is not None:
            return
        self.process.terminate()
        try:
            self.process.wait(timeout=4)
        except subprocess.TimeoutExpired:
            self.process.kill()
            self.process.wait(timeout=4)

    def request(self, method: str, params: dict[str, Any] | None = None, timeout: int = 60) -> dict[str, Any]:
        if self.process.stdin is None or self.process.stdout is None or self.process.stderr is None:
            raise RuntimeError("MCP process pipes are unavailable")

        self.next_id += 1
        request_id = self.next_id
        message: dict[str, Any] = {"jsonrpc": "2.0", "id": request_id, "method": method}
        if params is not None:
            message["params"] = params
        self.process.stdin.write(json.dumps(message) + "\n")
        self.process.stdin.flush()

        stderr_tail: list[str] = []
        deadline = time.time() + timeout
        while time.time() < deadline:
            readable, _, _ = select.select([self.process.stdout, self.process.stderr], [], [], 0.5)
            for stream in readable:
                line = stream.readline()
                if not line:
                    continue
                if stream is self.process.stderr:
                    stderr_tail.append(line.strip())
                    stderr_tail = stderr_tail[-8:]
                    continue
                try:
                    response = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if response.get("id") == request_id:
                    if response.get("error"):
                        raise RuntimeError(json.dumps(response["error"], ensure_ascii=False))
                    return response

        raise TimeoutError(f"Timed out waiting for MCP response to {method}: {' | '.join(stderr_tail)}")

    def initialize(self) -> None:
        self.request(
            "initialize",
            {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {},
                "clientInfo": {"name": "j40-google-email-import", "version": "1.0"},
            },
            timeout=30,
        )
        if self.process.stdin is None:
            raise RuntimeError("MCP process stdin is unavailable")
        self.process.stdin.write(json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}) + "\n")
        self.process.stdin.flush()

    def call_tool(self, name: str, arguments: dict[str, Any], timeout: int = 90) -> dict[str, Any]:
        response = self.request("tools/call", {"name": name, "arguments": arguments}, timeout=timeout)
        result = response.get("result") or {}
        if result.get("isError"):
            raise RuntimeError(json.dumps(result, ensure_ascii=False)[:2000])
        return result.get("structuredContent") or {}


def latest_previous_run_date() -> date | None:
    dates: list[date] = []
    for path in GENERATED_DIR.glob("comms_ingest_*_status.json"):
        match = re.match(r"comms_ingest_(\d{4}-\d{2}-\d{2})_status\.json$", path.name)
        if not match:
            continue
        try:
            dates.append(date.fromisoformat(match.group(1)))
        except ValueError:
            continue
    return max(dates) if dates else None


def normalize_after(value: str | None) -> str:
    if value:
        return value.replace("-", "/")
    previous = latest_previous_run_date()
    if previous:
        return previous.isoformat().replace("-", "/")
    return "2026/04/24"


def audit_reference_queries(after: str, limit: int) -> list[str]:
    if limit <= 0 or not AUDIT_QUEUE_PATH.exists():
        return []
    refs: list[str] = []
    seen: set[str] = set()
    with AUDIT_QUEUE_PATH.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            priority = norm(row.get("audit_priority"))
            if priority not in {"high", "medium"}:
                continue
            for token in re.split(r"[|,/ ]+", clean(row.get("transaction_number"))):
                token = token.strip().strip('"')
                if len(token) < 4 or token.lower() in {"local", "supplier"}:
                    continue
                if token in seen:
                    continue
                seen.add(token)
                refs.append(f'after:{after} "{token}"')
                if len(refs) >= limit:
                    return refs
    return refs


def base_queries(after: str) -> list[str]:
    negative = "-from:foodpanda -subject:foodpanda -from:linkedin -from:facebook"
    return [
        f"after:{after} {negative} (j40 OR fj40 OR j50 OR fj50 OR landcruiser OR \"land cruiser\" OR toyota)",
        f"after:{after} {negative} (daraz OR autohub OR aliexpress OR toolsmart OR \"tools mart\" OR \"mtl parts\" OR millat OR powerhouse OR postex OR leopard OR blueex OR \"blue-ex\" OR coolsun OR longman OR happilac)",
        f"after:{after} {negative} (chassis OR brake OR suspension OR primer OR epoxy OR paint OR welding OR hose OR rubber OR fastener OR grommet OR radiator OR evaporator OR blower OR relay OR fuse)",
        f"after:{after} {negative} (shipped OR dispatch OR tracking OR delivered OR invoice OR receipt OR payment)",
    ]


def search_messages(client: McpClient, queries: list[str], per_query: int, max_messages: int) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    messages: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    query_stats: dict[str, Any] = {}

    for query in queries:
        if len(messages) >= max_messages:
            break
        payload = client.call_tool(
            "search_emails",
            {"query": query, "maxResults": min(per_query, max_messages - len(messages))},
            timeout=90,
        )
        found = payload.get("messages") or []
        query_stats[query] = {
            "returned": len(found),
            "result_size_estimate": payload.get("resultSizeEstimate", 0),
            "has_next_page": bool(payload.get("nextPageToken")),
        }
        for message in found:
            message_id = clean(message.get("id"))
            if not message_id or message_id in seen_ids:
                continue
            seen_ids.add(message_id)
            messages.append(message)
            if len(messages) >= max_messages:
                break
    return messages, query_stats


def email_date_utc(headers: dict[str, Any], fallback: str = "") -> str:
    raw = clean(headers.get("date")) or clean(fallback)
    if not raw:
        return ""
    try:
        parsed = parsedate_to_datetime(raw)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    except Exception:
        return raw


def extract_amount(text: str) -> str:
    amounts: list[int] = []
    for match in CURRENCY_RE.finditer(text):
        raw = match.group(1) or match.group(2)
        if not raw:
            continue
        try:
            amounts.append(int(float(raw.replace(",", ""))))
        except ValueError:
            continue
    return str(max(amounts)) if amounts else "0"


def extract_codes(text: str) -> list[str]:
    codes: list[str] = []
    seen: set[str] = set()
    for pattern in PART_CODE_PATTERNS:
        for match in pattern.finditer(text):
            value = clean(match.group(0)).upper()
            if value and value not in seen and value not in {"PKR"}:
                seen.add(value)
                codes.append(value)
    return codes[:12]


def source_name(headers: dict[str, Any], text: str) -> str:
    from_header = clean(headers.get("from"))
    lowered = norm(f"{from_header} {text[:500]}")
    for supplier in sorted(SUPPLIER_TERMS, key=len, reverse=True):
        if supplier in lowered:
            return supplier.title()
    if from_header:
        return from_header.split("<")[0].strip().strip('"') or from_header
    return "Gmail"


def classify_email(message: dict[str, Any], full_email: dict[str, Any]) -> tuple[dict[str, str] | None, dict[str, Any]]:
    headers = full_email.get("headers") or {}
    body = full_email.get("body") or {}
    text = clean(body.get("text") or html_to_text(body.get("html") or ""))
    subject = clean(headers.get("subject") or message.get("subject"))
    snippet = clean(full_email.get("snippet") or message.get("snippet"))
    haystack_raw = f"{headers.get('from', '')} {subject} {snippet} {text}"
    haystack = norm(haystack_raw)

    project_hits = term_hits(haystack, PROJECT_TERMS)
    supplier_hits = term_hits(haystack, SUPPLIER_TERMS)
    order_hits = term_hits(haystack, ORDER_TERMS)
    exclude_hits = term_hits(haystack, EXCLUDE_TERMS)
    codes = extract_codes(haystack_raw)
    amount = extract_amount(haystack_raw)

    is_relevant = False
    reason = ""
    if supplier_hits and (order_hits or codes or amount != "0"):
        is_relevant = True
        reason = "supplier_order_signal"
    if project_hits and (order_hits or supplier_hits or codes or amount != "0"):
        is_relevant = True
        reason = reason or "project_order_signal"
    if codes and (supplier_hits or project_hits):
        is_relevant = True
        reason = reason or "reference_code_signal"
    if exclude_hits and not (project_hits or supplier_hits):
        is_relevant = False
        reason = "excluded_non_project"

    if not is_relevant:
        return None, {
            "message_id": clean(message.get("id")),
            "subject": subject,
            "exclude_hits": exclude_hits,
            "project_hits": project_hits,
            "supplier_hits": supplier_hits,
            "order_hits": order_hits,
            "reason": reason or "no_project_signal",
        }

    delivered_signal = bool(
        re.search(
            r"\b(has been delivered|was delivered|delivered to|delivery confirmation|order delivered|parcel delivered)\b",
            haystack,
        )
    )
    delivery_window_signal = bool(re.search(r"\bdelivered on:\s*\d{1,2}\s+\w+\s*-\s*\d{1,2}\s+\w+\s+\d{4}", haystack))

    if delivered_signal and not delivery_window_signal:
        status = "delivered_or_received_signal"
        subcategory = "delivery_update"
    elif any(term in haystack for term in ("shipped", "dispatch", "tracking", "out for delivery")):
        status = "shipment_tracking_signal"
        subcategory = "shipment_update"
    elif any(term in haystack for term in ("receipt", "invoice", "paid", "payment")):
        status = "payment_or_receipt_signal"
        subcategory = "receipt_payment"
    elif "feedback" in haystack or "review" in haystack:
        status = "feedback_requested"
        subcategory = "post_purchase_feedback"
    else:
        status = "order_or_project_signal"
        subcategory = "order_quote_tracking"

    if supplier_hits and order_hits:
        category = "supplier_communication"
    elif project_hits:
        category = "project_update"
    else:
        category = "product"

    excerpt = text or snippet
    excerpt_for_output = redact_private_details(excerpt)
    row = {
        "channel": "email",
        "message_id": clean(message.get("id")),
        "date_utc": email_date_utc(headers, clean(message.get("date"))),
        "category": category,
        "subcategory": subcategory,
        "source": source_name(headers, haystack_raw),
        "subject_or_ref": subject,
        "product_or_topic": excerpt_for_output[:260],
        "part_number_or_code": "|".join(codes),
        "amount_pkr": amount,
        "status": status,
        "action_required": "yes" if status != "feedback_requested" else "no",
        "notes": f"Imported by Gmail MCP; reason={reason}; hits={','.join((project_hits + supplier_hits + order_hits)[:20])}",
    }
    return row, {
        "message_id": row["message_id"],
        "thread_id": clean(full_email.get("threadId") or message.get("threadId")),
        "date_utc": row["date_utc"],
        "from": clean(headers.get("from") or message.get("from")),
        "to": clean(headers.get("to")),
        "subject": subject,
        "snippet": snippet,
        "body_excerpt": excerpt_for_output[:4000],
        "classification": {
            "category": category,
            "subcategory": subcategory,
            "status": status,
            "project_hits": project_hits,
            "supplier_hits": supplier_hits,
            "order_hits": order_hits,
            "exclude_hits": exclude_hits,
            "amount_pkr": amount,
            "codes": codes,
            "reason": reason,
        },
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Import project-relevant Gmail messages through Google Workspace MCP.")
    parser.add_argument("--after", default="", help="Gmail after date, YYYY/MM/DD or YYYY-MM-DD. Defaults to latest comms_ingest run date.")
    parser.add_argument("--date-tag", default=date.today().isoformat(), help="Output date tag YYYY-MM-DD.")
    parser.add_argument("--per-query", type=int, default=75, help="Maximum search results per query.")
    parser.add_argument("--max-messages", type=int, default=250, help="Maximum unique messages to read.")
    parser.add_argument("--audit-query-limit", type=int, default=60, help="Exact order/reference searches from audit queue.")
    args = parser.parse_args()

    after = normalize_after(args.after)
    queries = base_queries(after) + audit_reference_queries(after, args.audit_query_limit)

    client = McpClient()
    try:
        client.initialize()
        search_results, query_stats = search_messages(client, queries, args.per_query, args.max_messages)

        categorized_rows: list[dict[str, str]] = []
        project_messages: list[dict[str, Any]] = []
        excluded: list[dict[str, Any]] = []

        for message in search_results:
            message_id = clean(message.get("id"))
            if not message_id:
                continue
            try:
                full_email = client.call_tool(
                    "read_email",
                    {"id": message_id, "contentFormat": "full"},
                    timeout=90,
                )
            except Exception as error:
                excluded.append({"message_id": message_id, "reason": f"read_failed:{clean(error)}"})
                continue

            row, project_payload = classify_email(message, full_email)
            if row is None:
                excluded.append(project_payload)
                continue
            categorized_rows.append(row)
            project_messages.append(project_payload)
    finally:
        client.close()

    categorized_rows.sort(key=lambda row: (row["date_utc"], row["source"], row["message_id"]))
    output_csv = GENERATED_DIR / f"comms_ingest_{args.date_tag}_categorized.csv"
    output_json = GENERATED_DIR / f"gmail_project_messages_{args.date_tag}.json"
    status_path = GENERATED_DIR / f"comms_ingest_{args.date_tag}_status.json"

    write_csv(output_csv, categorized_rows)
    output_json.write_text(json.dumps(project_messages, indent=2, ensure_ascii=False), encoding="utf-8")

    category_counts = Counter(row["category"] for row in categorized_rows)
    source_counts = Counter(row["source"] for row in categorized_rows)
    status = {
        "run_date_utc": datetime.now(timezone.utc).date().isoformat(),
        "date_tag": args.date_tag,
        "email": {
            "new_messages_query_after": after,
            "queries_run": queries,
            "query_stats": query_stats,
            "unique_messages_read": len(search_results),
            "categorized_records_written": len(categorized_rows),
            "excluded_non_project_records": len(excluded),
            "category_counts": dict(category_counts),
            "top_sources": dict(source_counts.most_common(12)),
            "output_csv": str(output_csv.relative_to(ROOT)),
            "output_json": str(output_json.relative_to(ROOT)),
            "high_signal_procurement_refs": [
                row["subject_or_ref"] for row in categorized_rows[:20]
            ],
        },
    }
    status_path.write_text(json.dumps(status, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Wrote Gmail categorized records: {output_csv.relative_to(ROOT)}")
    print(f"Wrote Gmail project messages: {output_json.relative_to(ROOT)}")
    print(f"Wrote Gmail status: {status_path.relative_to(ROOT)}")
    print(f"Counts: {len(categorized_rows)} categorized, {len(excluded)} excluded, {len(search_results)} read")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit(130)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
