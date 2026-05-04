# Parts List Review

- Generated: 2026-05-04 04:07:22
- Source: `data/manual/expenses.csv` (`bucket=parts`) -> 84 rows
- Review CSV: `data/manual/parts_list_review.csv`
- Overlap CSV: `data/manual/parts_overlap_candidates.csv`

## Action Buckets

- `buy_now`: 16
- `cancelled_or_not_required`: 11
- `completed_or_received`: 19
- `deferred`: 6
- `needs_spec_before_order`: 11
- `next_phase`: 1
- `ordered_waiting_arrival`: 12
- `spec_ready_release_hold`: 4
- `unclear`: 4

## Workstream Split

- `body_chassis`: 23
- `electrical_reset`: 18
- `mechanical_baseline`: 17
- `brake_system`: 13
- `steering_brakes_suspension`: 6
- `interior_weatherproofing`: 5
- `optional_upgrades`: 2

## Price Coverage

- `has_confirmed_amount=yes`: 16
- `has_confirmed_amount=no`: 68

## Buy-Now / Quote-Ready Missing Price

- `part_body_retaining_clips_cotter_pin_pack` [body_chassis] Body retaining clip pack - R-clips hairpins split pins circlips and small cotters
- `part_fastener_kit_c_captive_clip_nuts` [body_chassis] Fastener Kit C: Captive/clip/speed nut and weld/rivnut assortment - M6/M8
- `part_brake_fluid_bleed_consumables` [brake_system] Brake hydraulic opening prep remaining consumables - caps plugs bleed hose bottle cleaner rags gloves catch tray
- `part_cabin_compact_fuse_boxes` [electrical_reset] Compact cabin fuse protection - reuse 12-way plus buy one compact OEM add-on
- `part_firewall_grommet_set_large_power` [electrical_reset] Additional firewall grommet set IDs 16/20/25 mm
- `part_firewall_grommet_set_small_medium` [electrical_reset] Additional firewall grommet set IDs 6/8/10/12 mm
- `part_mech_accessory_belt_set` [mechanical_baseline] Accessory belt set
- `part_mech_engine_oil_filter_service` [mechanical_baseline] Engine oil + oil filter service pack
- `part_mech_fuel_filter` [mechanical_baseline] Fuel filter
- `part_mech_fuel_hose_and_clamps` [mechanical_baseline] Diesel fuel hose/line package - 8 mm feed, 6 mm return, leak-off hose, conditional hard lines
- `part_mech_heat_glow_plugs_set` [mechanical_baseline] Toyota OE glow plugs 19850-68030 x6 - diesel 2H
- `part_mech_heater_hose_set` [mechanical_baseline] Heater hose pair - EPDM 400 mm inlet + 280 mm outlet, expected 16 mm ID
- `part_mech_radiator_cap` [mechanical_baseline] Radiator cap
- `part_mech_radiator_hose_set` [mechanical_baseline] Cooling hose/pipe package - upper/lower radiator hoses, overflow hose, formed coolant pipe
- `part_mech_vacuum_hose_refresh` [mechanical_baseline] Vacuum/breather hose kit - 10-12 mm vacuum + 16-19 mm oil-resistant breather
- `part_suspension_wooden_cribbing_blocks` [steering_brakes_suspension] Seasoned hardwood cribbing cut set - 8 blocks + 4 wedge chocks

## Buy-Now / Quote-Ready With Confirmed Price

- None

## Overlap Groups

- `floor_finish_stack` (3 rows): Floor/interior finish stack [action buckets: deferred]
- `grommet_options` (3 rows): Grommet options [action buckets: buy_now|deferred]
- `primer_system_stack` (3 rows): Primer system stack [action buckets: ordered_waiting_arrival]
