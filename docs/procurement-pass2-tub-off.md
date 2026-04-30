# Procurement Pass 2 (Tub-Off, Pakistan Cost Reality)

- Generated: 2026-05-01 01:07:05
- Input matrix: `data/manual/procurement_decision_matrix.csv`
- Pass-2 matrix: `data/manual/procurement_decision_matrix_pass2.csv`
- Basket plan: `data/manual/procurement_local_baskets_pass2.csv`

## Why This Pass

- Objective: shrink the active list before tub-off and avoid overbuying.
- Wiring stock signal from workbook: `50` received/paid wiring rows (`30` connectors/wiring-related).
- Local Pakistan sourcing assumption: common Toyota service parts and hardware are cheaper and faster locally, so treat them as post-inspection bundles.

## Decision Counts

- `bundle_local_toyota_buy_after_inspection`: 11
- `buy_minimum_qty_now`: 2
- `confirm_order_state`: 1
- `confirm_price_then_buy`: 3
- `defer_as_non_baseline`: 14
- `defer_until_baseline_closure`: 1
- `hold_until_post_weld_primer`: 1
- `inspect_then_local_decide`: 2
- `post_rust_map_body_stack_bundle`: 3
- `scope_audit_before_order`: 1
- `stock_audit_then_local_topup`: 4
- `track_in_flight_order`: 4

## Timing Windows

- `in_flight_now`: 4
- `post_baseline_only`: 15
- `post_rust_repair`: 4
- `post_tub_off_inspection`: 13
- `pre_order_audit`: 5
- `review`: 4
- `tub_off_immediate`: 2

## Immediate Actions (Now)

- `part_metal_protection` Metal protection and restoration products -> buy_minimum_qty_now
- `part_primer` Primer -> buy_minimum_qty_now
- `part_nylon_fiber_wool_polishing_disc_sets_2x` Nylon fiber polishing disc and wool buffing polishing disc set (3pcs) plus drill adapter and grinder nut for metals x2 -> track_in_flight_order
- `part_seam_sealer` Seam sealer -> track_in_flight_order
- `part_ironman_front_dampers_separate_shipment` Ironman Foamcell front damper pair - separate shipment (24635FE x2) -> track_in_flight_order
- `part_old_man_emu_shocks` Ironman Foamcell suspension kit - main shipment (front dampers separate) -> track_in_flight_order

## Practical Outcome

- Keep only minimal rust-control buys immediate for tub-off.
- Treat the full body chemistry stack as a post-rust-map bundle, not separate early purchases.
- Move most electrical purchases to stock-audit/top-up mode.
- Move mechanical baseline list into one local Toyota/common supplier bundle after inspection.
- Keep duplicate/optional/upgrade items deferred to avoid scope creep and unnecessary spend.
