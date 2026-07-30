# Procurement Pass 2 (Tub-Off, Pakistan Cost Reality)

- Generated: 2026-07-29 06:20:53
- Input matrix: `data/manual/procurement_decision_matrix.csv`
- Pass-2 matrix: `data/manual/procurement_decision_matrix_pass2.csv`
- Basket plan: `data/manual/procurement_local_baskets_pass2.csv`

## Why This Pass

- Objective: shrink the active list before tub-off and avoid overbuying.
- Wiring stock signal from workbook: `49` received/paid wiring rows (`31` connectors/wiring-related).
- Local Pakistan sourcing assumption: common Toyota service parts and hardware are cheaper and faster locally, so treat them as post-inspection bundles.

## Decision Counts

- `bundle_local_toyota_buy_after_inspection`: 2
- `buy_body_fastener_hardware_from_samples`: 2
- `buy_compact_cabin_fuse_boxes`: 1
- `buy_now`: 2
- `capture_body_hardware_samples_then_order`: 5
- `capture_brake_specs_then_order`: 3
- `confirm_price_then_buy`: 12
- `confirm_procured_receipt`: 8
- `defer_as_non_baseline`: 4
- `defer_until_baseline_closure`: 1
- `gearbox_oil_spec_then_buy`: 1
- `hold_until_body_closed`: 1
- `longman_hose_pipe_order_ready`: 4
- `review`: 42
- `runner_spec_controlled`: 9
- `source_toyota_oe_glow_plugs_by_part_number`: 1
- `track_in_flight_order`: 6

## Timing Windows

- `body_fastener_topup`: 2
- `body_hardware_sample_sort`: 5
- `body_sealed`: 1
- `electrical_closeout`: 1
- `gearbox_oil_service_gate`: 1
- `in_flight_now`: 14
- `longman_mills_quote_pack`: 4
- `merged_suspension_brake_window`: 3
- `post_baseline_only`: 5
- `post_tub_off_inspection`: 3
- `review`: 56
- `runner_spec_controlled`: 9

## Immediate Actions (Now)

- `part_hvac_hidden_evaporator_blower_unit_20260514` Hidden compact evaporator core/case and outlet plenum for custom blower fitment -> track_in_flight_order
- `part_brake_master_reservoir_refresh` Brake master cylinder candidate order - ULTIMA UFM-1041 x1; reservoir/proportioning still inspect -> track_in_flight_order
- `part_toolsmart_vmd_brake_clutch_cleaner_400ml_tm26231_20260704` VMD Brake and Clutch Cleaner 400ML - qty 1 -> track_in_flight_order
- `part_brighto_extreme_paint_remover_3l_second_order_20260618` Brighto Extreme Paint Remover - 3 L second order -> track_in_flight_order
- `part_mech_engine_oil_filter_service` Engine oil - Liqui Moly Touring High Tech SHPD 15W-40 5L; oil filter tracked separately -> track_in_flight_order
- `part_ironman_front_dampers_separate_shipment` Ironman Foamcell front damper pair - separate shipment (24635FE x2) -> track_in_flight_order

## Practical Outcome

- Keep only minimal rust-control buys immediate for tub-off.
- Use the received body-chemistry stock after receipt/condition checks; do not rebuy solvent, seam sealer, cavity wax, or primer unless a received item fails inspection.
- Move most electrical purchases to stock-audit/top-up mode.
- Move mechanical baseline list into one local Toyota/common supplier bundle after inspection.
- Keep DOT 3 brake-fluid opening prep purchase-ready before hydraulic lines are opened.
- Chassis masking tape and Ultra-cloth solvent-safe wipes are received; use on-hand grommets as temporary open-hole masking only after fit and solvent checks.
- Move brake rows into the merged suspension/brake window: capture measurements and samples first, then order exact parts.
- Move fuel/coolant/heater/vacuum hose rows to the Longman pipe/hose order spec with explicit quote/order lengths, while keeping final trim, clamp, chafe, and leak checks at install.
- Keep clutch hydraulics inspect-first, then buy exact master/slave/flex/hard-line parts only if failed.
- Keep duplicate/optional/upgrade items deferred to avoid scope creep and unnecessary spend.
