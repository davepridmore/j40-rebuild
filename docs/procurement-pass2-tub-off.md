# Procurement Pass 2 (Tub-Off, Pakistan Cost Reality)

- Generated: 2026-05-08 17:29:19
- Input matrix: `data/manual/procurement_decision_matrix.csv`
- Pass-2 matrix: `data/manual/procurement_decision_matrix_pass2.csv`
- Basket plan: `data/manual/procurement_local_baskets_pass2.csv`

## Why This Pass

- Objective: shrink the active list before tub-off and avoid overbuying.
- Wiring stock signal from workbook: `49` received/paid wiring rows (`31` connectors/wiring-related).
- Local Pakistan sourcing assumption: common Toyota service parts and hardware are cheaper and faster locally, so treat them as post-inspection bundles.

## Decision Counts

- `bundle_local_toyota_buy_after_inspection`: 4
- `buy_body_fastener_hardware_from_samples`: 2
- `buy_compact_cabin_fuse_boxes`: 1
- `buy_remaining_brake_bleed_consumables`: 1
- `capture_body_hardware_samples_then_order`: 6
- `capture_brake_specs_then_order`: 9
- `clutch_hydraulic_inspect_then_exact_order`: 1
- `defer_as_non_baseline`: 5
- `defer_until_baseline_closure`: 1
- `hold_until_body_closed`: 1
- `hose_local_market_order_ready`: 4
- `open_inspect_then_order_standard_brake_parts`: 3
- `review`: 2
- `source_toyota_oe_glow_plugs_by_part_number`: 1
- `stock_audit_then_local_topup`: 2
- `track_in_flight_order`: 8

## Timing Windows

- `body_fastener_topup`: 2
- `body_hardware_sample_sort`: 6
- `body_sealed`: 1
- `clutch_hydraulic_inspection`: 1
- `electrical_closeout`: 1
- `hose_local_market_order`: 4
- `in_flight_now`: 8
- `merged_suspension_brake_window`: 12
- `post_baseline_only`: 6
- `post_tub_off_inspection`: 5
- `pre_brake_hydraulic_opening`: 1
- `pre_order_audit`: 2
- `review`: 2

## Immediate Actions (Now)

- `part_fastener_kit_a_millat` Fastener Kit A: Tub-to-chassis mounts (OEM positions) - M10/M12 class 8.8 bolts, matching nuts, flat+spring washers, sleeves -> track_in_flight_order
- `part_fastener_kit_b_millat` Fastener Kit B: Body panel/bracket hardware - M6/M8 class 8.8 flange bolts, nyloc nuts, washers -> track_in_flight_order
- `part_fastener_kit_e_millat` Millat order #38902 metric screw pack - M10x20 x20, M6x16 x60, M6x12 x120, M8x16 x60 -> track_in_flight_order
- `part_brake_fluid_bleed_consumables` Brake hydraulic opening prep remaining consumables - caps plugs bleed hose bottle cleaner rags gloves catch tray -> buy_remaining_brake_bleed_consumables
- `part_daraz_nitrile_gloves_black_l_100pc_20260504` Safety Black Disposable Nitrile gloves 100 PCs Box - black large -> track_in_flight_order
- `part_chassis_masking_plugs_tape_solvent_wipes` Chassis coating masking pack - solvent-safe wipes, masking tape, thread/hole plugs -> track_in_flight_order
- `part_fastener_kit_d_millat` Fastener Kit D: Grounding hardware - star/serrated washers M6/M8/M10 + cleaned contact points -> track_in_flight_order
- `part_ironman_front_dampers_separate_shipment` Ironman Foamcell front damper pair - separate shipment (24635FE x2) -> track_in_flight_order
- `part_suspension_wooden_cribbing_blocks` Seasoned hardwood cribbing cut set - 8 blocks + 4 wedge chocks -> track_in_flight_order

## Practical Outcome

- Keep only minimal rust-control buys immediate for tub-off.
- Use the received body-chemistry stock after receipt/condition checks; do not rebuy solvent, seam sealer, cavity wax, or primer unless a received item fails inspection.
- Move most electrical purchases to stock-audit/top-up mode.
- Move mechanical baseline list into one local Toyota/common supplier bundle after inspection.
- Keep DOT 3 brake-fluid opening prep purchase-ready before hydraulic lines are opened.
- Track chassis masking tape and solvent-safe wipe delivery before primer/sealer/Raptor work; use on-hand grommets as temporary open-hole masking only after fit and solvent checks.
- Move brake rows into the merged suspension/brake window: capture measurements and samples first, then order exact parts.
- Move fuel/coolant/heater/vacuum hose rows to the local-market order sheet with explicit buy lengths, while keeping final trim, clamp, chafe, and leak checks at install.
- Keep clutch hydraulics inspect-first, then buy exact master/slave/flex/hard-line parts only if failed.
- Keep duplicate/optional/upgrade items deferred to avoid scope creep and unnecessary spend.
