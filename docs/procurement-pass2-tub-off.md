# Procurement Pass 2 (Tub-Off, Pakistan Cost Reality)

- Generated: 2026-05-02 09:05:53
- Input matrix: `data/manual/procurement_decision_matrix.csv`
- Pass-2 matrix: `data/manual/procurement_decision_matrix_pass2.csv`
- Basket plan: `data/manual/procurement_local_baskets_pass2.csv`

## Why This Pass

- Objective: shrink the active list before tub-off and avoid overbuying.
- Wiring stock signal from workbook: `50` received/paid wiring rows (`32` connectors/wiring-related).
- Local Pakistan sourcing assumption: common Toyota service parts and hardware are cheaper and faster locally, so treat them as post-inspection bundles.

## Decision Counts

- `bundle_local_toyota_buy_after_inspection`: 5
- `buy_before_suspension_work`: 1
- `defer_as_non_baseline`: 6
- `defer_until_baseline_closure`: 1
- `inspect_then_local_decide`: 2
- `review`: 14
- `stock_audit_then_local_topup`: 2
- `track_in_flight_order`: 10

## Timing Windows

- `in_flight_now`: 10
- `post_baseline_only`: 7
- `post_tub_off_inspection`: 7
- `pre_order_audit`: 2
- `pre_suspension_setup`: 1
- `review`: 14

## Immediate Actions (Now)

- `part_cavity_wax` HB Body U900 cavity wax spray 400ml -> track_in_flight_order
- `part_fastener_kit_a_millat` Fastener Kit A: Tub-to-chassis mounts (OEM positions) - M10/M12 class 8.8 bolts, matching nuts, flat+spring washers, sleeves -> track_in_flight_order
- `part_fastener_kit_b_millat` Fastener Kit B: Body panel/bracket hardware - M6/M8 class 8.8 flange bolts, nyloc nuts, washers -> track_in_flight_order
- `part_primer` Hi-Build Zinc Rich Epoxy Primer EC 11 two-pack set -> track_in_flight_order
- `part_seam_sealer` Seam sealer -> track_in_flight_order
- `part_wax_and_grease_remover` 3M Prep Solvent-70 1 gallon / wax and grease remover -> track_in_flight_order
- `part_fastener_kit_d_millat` Fastener Kit D: Grounding hardware - star/serrated washers M6/M8/M10 + cleaned contact points -> track_in_flight_order
- `part_daraz_jubilee_hose_clip_assortment_30pc` Jubilee hose clip assortment - 10 pc fuel line/diesel/petrol/coolant clamp packs x3 -> track_in_flight_order
- `part_ironman_foamcell_suspension_kit` Ironman Foamcell suspension kit - main shipment (front dampers separate) -> track_in_flight_order
- `part_ironman_front_dampers_separate_shipment` Ironman Foamcell front damper pair - separate shipment (24635FE x2) -> track_in_flight_order

## Practical Outcome

- Keep only minimal rust-control buys immediate for tub-off.
- Treat the full body chemistry stack as a post-rust-map bundle, not separate early purchases.
- Move most electrical purchases to stock-audit/top-up mode.
- Move mechanical baseline list into one local Toyota/common supplier bundle after inspection.
- Keep duplicate/optional/upgrade items deferred to avoid scope creep and unnecessary spend.
