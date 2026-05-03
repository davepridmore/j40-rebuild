# Procurement Pass 2 (Tub-Off, Pakistan Cost Reality)

- Generated: 2026-05-04 02:08:55
- Input matrix: `data/manual/procurement_decision_matrix.csv`
- Pass-2 matrix: `data/manual/procurement_decision_matrix_pass2.csv`
- Basket plan: `data/manual/procurement_local_baskets_pass2.csv`

## Why This Pass

- Objective: shrink the active list before tub-off and avoid overbuying.
- Wiring stock signal from workbook: `49` received/paid wiring rows (`31` connectors/wiring-related).
- Local Pakistan sourcing assumption: common Toyota service parts and hardware are cheaper and faster locally, so treat them as post-inspection bundles.

## Decision Counts

- `bundle_local_toyota_buy_after_inspection`: 5
- `buy_before_suspension_work`: 1
- `buy_body_fastener_hardware_from_samples`: 2
- `buy_compact_cabin_fuse_boxes`: 1
- `buy_remaining_brake_bleed_consumables`: 1
- `capture_body_hardware_samples_then_order`: 6
- `capture_brake_specs_then_order`: 8
- `defer_as_non_baseline`: 5
- `defer_until_baseline_closure`: 1
- `defer_until_mount_failure_or_engine_lift_scope`: 1
- `hold_until_body_closed`: 1
- `inspect_then_local_decide`: 1
- `open_inspect_then_order_standard_brake_parts`: 3
- `review`: 5
- `stock_audit_then_local_topup`: 2
- `track_in_flight_order`: 12

## Timing Windows

- `body_fastener_topup`: 2
- `body_hardware_sample_sort`: 6
- `body_sealed`: 1
- `electrical_closeout`: 1
- `in_flight_now`: 12
- `merged_suspension_brake_window`: 11
- `no_engine_lift_baseline`: 1
- `post_baseline_only`: 6
- `post_tub_off_inspection`: 6
- `pre_brake_hydraulic_opening`: 1
- `pre_order_audit`: 2
- `pre_suspension_setup`: 1
- `review`: 5

## Immediate Actions (Now)

- `part_cavity_wax` HB Body U900 cavity wax spray 400ml -> track_in_flight_order
- `part_fastener_kit_a_millat` Fastener Kit A: Tub-to-chassis mounts (OEM positions) - M10/M12 class 8.8 bolts, matching nuts, flat+spring washers, sleeves -> track_in_flight_order
- `part_fastener_kit_b_millat` Fastener Kit B: Body panel/bracket hardware - M6/M8 class 8.8 flange bolts, nyloc nuts, washers -> track_in_flight_order
- `part_fastener_kit_e_millat` Millat order #38902 metric screw pack - M10x20 x20, M6x16 x60, M6x12 x120, M8x16 x60 -> track_in_flight_order
- `part_primer` Hi-Build Zinc Rich Epoxy Primer EC 11 two-pack set -> track_in_flight_order
- `part_seam_sealer` Seam sealer -> track_in_flight_order
- `part_wax_and_grease_remover` 3M Prep Solvent-70 1 gallon / wax and grease remover -> track_in_flight_order
- `part_brake_fluid_bleed_consumables` Brake hydraulic opening prep remaining consumables - caps plugs bleed hose bottle cleaner rags gloves catch tray -> buy_remaining_brake_bleed_consumables
- `part_dot3_brake_fluid_autohub_6x354ml` Lion Brake Fluid DOT-3 12oz/354ml x6 -> track_in_flight_order
- `part_fastener_kit_d_millat` Fastener Kit D: Grounding hardware - star/serrated washers M6/M8/M10 + cleaned contact points -> track_in_flight_order
- `part_daraz_jubilee_hose_clip_assortment_30pc` Jubilee hose clip assortment - 10 pc fuel line/diesel/petrol/coolant clamp packs x3 -> track_in_flight_order
- `part_ironman_foamcell_suspension_kit` Ironman Foamcell suspension kit - main shipment (front dampers separate) -> track_in_flight_order
- `part_ironman_front_dampers_separate_shipment` Ironman Foamcell front damper pair - separate shipment (24635FE x2) -> track_in_flight_order

## Practical Outcome

- Keep only minimal rust-control buys immediate for tub-off.
- Treat the full body chemistry stack as a post-rust-map bundle, not separate early purchases.
- Move most electrical purchases to stock-audit/top-up mode.
- Move mechanical baseline list into one local Toyota/common supplier bundle after inspection.
- Keep DOT 3 brake-fluid opening prep purchase-ready before hydraulic lines are opened.
- Move brake rows into the merged suspension/brake window: capture measurements and samples first, then order exact parts.
- Keep duplicate/optional/upgrade items deferred to avoid scope creep and unnecessary spend.
