# Parts List Review

- Generated: 2026-05-03 23:02:53
- Source: `data/manual/expenses.csv` (`bucket=parts`) -> 76 rows
- Review CSV: `data/manual/parts_list_review.csv`
- Overlap CSV: `data/manual/parts_overlap_candidates.csv`

## Action Buckets

- `buy_now`: 10
- `cancelled_or_not_required`: 10
- `completed_or_received`: 19
- `deferred`: 6
- `next_phase`: 1
- `ordered_waiting_arrival`: 10
- `unclear`: 20

## Workstream Split

- `electrical_reset`: 18
- `mechanical_baseline`: 17
- `body_chassis`: 17
- `brake_system`: 12
- `steering_brakes_suspension`: 6
- `interior_weatherproofing`: 4
- `optional_upgrades`: 2

## Price Coverage

- `has_confirmed_amount=yes`: 11
- `has_confirmed_amount=no`: 65

## Buy-Now / Quote-Ready Missing Price

- `part_brake_fluid_bleed_consumables` [brake_system] Brake hydraulic opening prep - DOT 3 brake fluid caps plugs bleed hose bottle cleaner rags gloves
- `part_cabin_compact_fuse_boxes` [electrical_reset] Compact covered cabin blade fuse boxes - likely 3 identical units
- `part_firewall_grommet_set_large_power` [electrical_reset] Additional firewall grommet set IDs 16/20/25 mm
- `part_firewall_grommet_set_small_medium` [electrical_reset] Additional firewall grommet set IDs 6/8/10/12 mm
- `part_mech_accessory_belt_set` [mechanical_baseline] Accessory belt set
- `part_mech_engine_oil_filter_service` [mechanical_baseline] Engine oil + oil filter service pack
- `part_mech_fuel_filter` [mechanical_baseline] Fuel filter
- `part_mech_heat_glow_plugs_set` [mechanical_baseline] Heat/glow plugs set - diesel 2H
- `part_mech_radiator_cap` [mechanical_baseline] Radiator cap
- `part_suspension_wooden_cribbing_blocks` [steering_brakes_suspension] Seasoned hardwood cribbing cut set - 8 blocks + 4 wedge chocks

## Buy-Now / Quote-Ready With Confirmed Price

- None

## Overlap Groups

- `floor_finish_stack` (3 rows): Floor/interior finish stack [action buckets: deferred]
- `grommet_options` (3 rows): Grommet options [action buckets: buy_now|deferred]
- `primer_system_stack` (3 rows): Primer system stack [action buckets: ordered_waiting_arrival]
- `wire_sleeving_options` (2 rows): Wire sleeving options [action buckets: ordered_waiting_arrival|unclear]
