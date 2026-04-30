# Procurement Pass 2 (Tub-Off, Pakistan Cost Reality)

- Generated: 2026-04-26 03:50:30
- Input matrix: `data/manual/procurement_decision_matrix.csv`
- Pass-2 matrix: `data/manual/procurement_decision_matrix_pass2.csv`
- Basket plan: `data/manual/procurement_local_baskets_pass2.csv`

## Why This Pass

- Objective: shrink the active list before tub-off and avoid overbuying.
- Wiring stock signal from workbook: `50` received/paid wiring rows (`30` connectors/wiring-related).
- Local Pakistan sourcing assumption: common Toyota service parts and hardware are cheaper and faster locally, so treat them as post-inspection bundles.

## Decision Counts

- `bundle_local_toyota_buy_after_inspection`: 16
- `buy_minimum_qty_now`: 2
- `confirm_order_state`: 1
- `confirm_price_then_buy`: 3
- `defer_as_non_baseline`: 15
- `defer_until_baseline_closure`: 1
- `do_not_buy_separately`: 2
- `hold_until_post_weld_primer`: 1
- `inspect_then_local_decide`: 2
- `post_rust_map_body_stack_bundle`: 4
- `scope_audit_before_order`: 1
- `stock_audit_then_local_topup`: 5

## Timing Windows

- `post_baseline_only`: 16
- `post_rust_repair`: 5
- `post_tub_off_inspection`: 18
- `pre_order_audit`: 6
- `review`: 6
- `tub_off_immediate`: 2

## Immediate Actions (Now)

- `part_metal_protection` Metal protection and restoration products -> buy_minimum_qty_now
- `part_primer` Primer -> buy_minimum_qty_now

## Practical Outcome

- Keep only minimal rust-control buys immediate for tub-off.
- Treat the full body chemistry stack as a post-rust-map bundle, not separate early purchases.
- Move most electrical purchases to stock-audit/top-up mode.
- Move mechanical baseline list into one local Toyota/common supplier bundle after inspection.
- Keep duplicate/optional/upgrade items deferred to avoid scope creep and unnecessary spend.
