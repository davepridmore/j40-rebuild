# Parts List Review

- Generated: 2026-05-02 06:33:11
- Source: `data/manual/expenses.csv` (`bucket=parts`) -> 64 rows
- Review CSV: `data/manual/parts_list_review.csv`
- Overlap CSV: `data/manual/parts_overlap_candidates.csv`

## Action Buckets

- `buy_now`: 12
- `cancelled_or_not_required`: 2
- `completed_or_received`: 18
- `deferred`: 6
- `next_phase`: 7
- `ordered_waiting_arrival`: 4
- `researching`: 1
- `unclear`: 14

## Workstream Split

- `mechanical_baseline`: 17
- `electrical_reset`: 16
- `body_chassis`: 14
- `brake_system`: 6
- `steering_brakes_suspension`: 5
- `interior_weatherproofing`: 4
- `optional_upgrades`: 2

## Price Coverage

- `has_confirmed_amount=yes`: 11
- `has_confirmed_amount=no`: 53

## Buy-Now / Quote-Ready Missing Price

- `part_bedliner_sprays` [body_chassis] Bedliner sprays
- `part_metal_protection` [body_chassis] Metal protection and restoration products
- `part_primer` [body_chassis] Primer
- `part_firewall_grommet_set_large_power` [electrical_reset] Additional firewall grommet set IDs 16/20/25 mm
- `part_firewall_grommet_set_small_medium` [electrical_reset] Additional firewall grommet set IDs 6/8/10/12 mm
- `part_horn_relay` [electrical_reset] Horn relay
- `part_star_washers` [electrical_reset] Star washers (bite into metal)
- `part_mech_accessory_belt_set` [mechanical_baseline] Accessory belt set
- `part_mech_engine_oil_filter_service` [mechanical_baseline] Engine oil + oil filter service pack
- `part_mech_fuel_filter` [mechanical_baseline] Fuel filter
- `part_mech_heat_glow_plugs_set` [mechanical_baseline] Heat/glow plugs set - diesel 2H
- `part_mech_radiator_cap` [mechanical_baseline] Radiator cap

## Buy-Now / Quote-Ready With Confirmed Price

- None

## Overlap Groups

- `floor_finish_stack` (5 rows): Floor/interior finish stack [action buckets: buy_now|deferred|next_phase]
- `grommet_options` (3 rows): Grommet options [action buckets: buy_now|deferred]
- `primer_system_stack` (5 rows): Primer system stack [action buckets: buy_now|next_phase|ordered_waiting_arrival]
- `switch_options` (3 rows): Switch inventory [action buckets: buy_now|deferred|next_phase]
