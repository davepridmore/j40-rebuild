# Parts List Review

- Generated: 2026-05-01 01:41:29
- Source: `data/manual/expenses.csv` (`bucket=parts`) -> 57 rows
- Review CSV: `data/manual/parts_list_review.csv`
- Overlap CSV: `data/manual/parts_overlap_candidates.csv`

## Action Buckets

- `buy_now`: 21
- `completed_or_received`: 18
- `deferred`: 6
- `next_phase`: 7
- `ordered_waiting_arrival`: 4
- `researching`: 1

## Workstream Split

- `mechanical_baseline`: 16
- `electrical_reset`: 16
- `body_chassis`: 14
- `steering_brakes_suspension`: 5
- `interior_weatherproofing`: 4
- `optional_upgrades`: 2

## Price Coverage

- `has_confirmed_amount=yes`: 11
- `has_confirmed_amount=no`: 46

## Buy-Now / Quote-Ready Missing Price

- `part_bedliner_sprays` [body_chassis] Bedliner sprays
- `part_body_mount_hardware_kit` [body_chassis] Body mount hardware kit bolts sleeves washers
- `part_body_mount_rubber_kit` [body_chassis] Body-to-chassis mount rubber kit
- `part_body_mount_shim_pack` [body_chassis] Body mount shim and spacer pack
- `part_metal_protection` [body_chassis] Metal protection and restoration products
- `part_primer` [body_chassis] Primer
- `part_firewall_grommet_set_large_power` [electrical_reset] Additional firewall grommet set IDs 16/20/25 mm
- `part_firewall_grommet_set_small_medium` [electrical_reset] Additional firewall grommet set IDs 6/8/10/12 mm
- `part_horn_relay` [electrical_reset] Horn relay
- `part_star_washers` [electrical_reset] Star washers (bite into metal)
- `part_mech_accessory_belt_set` [mechanical_baseline] Accessory belt set
- `part_mech_distributor_cap_rotor_tuneup` [mechanical_baseline] Distributor cap rotor and ignition tune-up consumables
- `part_mech_engine_oil_filter_service` [mechanical_baseline] Engine oil + oil filter service pack
- `part_mech_fuel_filter` [mechanical_baseline] Fuel filter
- `part_mech_fuel_hose_and_clamps` [mechanical_baseline] Fuel-rated rubber hose and clamp kit
- `part_mech_heater_hose_set` [mechanical_baseline] Heater hose set with clamps
- `part_mech_radiator_cap` [mechanical_baseline] Radiator cap
- `part_mech_radiator_hose_set` [mechanical_baseline] Radiator hose set upper plus lower with clamps
- `part_mech_spark_plugs_set` [mechanical_baseline] Spark plugs set
- `part_mech_vacuum_hose_refresh` [mechanical_baseline] Vacuum hose refresh kit
- `part_mech_brake_flex_hose_set` [steering_brakes_suspension] Brake flexible hose set front and rear

## Buy-Now / Quote-Ready With Confirmed Price

- None

## Overlap Groups

- `floor_finish_stack` (5 rows): Floor/interior finish stack [action buckets: buy_now|deferred|next_phase]
- `grommet_options` (3 rows): Grommet options [action buckets: buy_now|deferred]
- `primer_system_stack` (5 rows): Primer system stack [action buckets: buy_now|next_phase|ordered_waiting_arrival]
- `switch_options` (3 rows): Switch inventory [action buckets: buy_now|deferred|next_phase]
