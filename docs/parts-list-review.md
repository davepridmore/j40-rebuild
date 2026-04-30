# Parts List Review

- Generated: 2026-04-26 03:48:27
- Source: `data/manual/expenses.csv` (`bucket=parts`) -> 66 rows
- Review CSV: `data/manual/parts_list_review.csv`
- Overlap CSV: `data/manual/parts_overlap_candidates.csv`

## Action Buckets

- `buy_now`: 29
- `completed_or_received`: 13
- `deferred`: 8
- `next_phase`: 7
- `ordered_waiting_arrival`: 3
- `quote_decision_ready`: 1
- `researching`: 3
- `unclear`: 2

## Workstream Split

- `electrical_reset`: 21
- `mechanical_baseline`: 16
- `body_chassis`: 12
- `steering_brakes_suspension`: 11
- `interior_weatherproofing`: 4
- `optional_upgrades`: 2

## Price Coverage

- `has_confirmed_amount=yes`: 12
- `has_confirmed_amount=no`: 54

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
- `part_split_conduit_braided_sleeve_large` [electrical_reset] Split conduit / braided sleeve - Large
- `part_split_conduit_braided_sleeve_medium` [electrical_reset] Split conduit / braided sleeve - Medium
- `part_split_conduit_braided_sleeve_small` [electrical_reset] Split conduit / braided sleeve - Small
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
- `part_local_leaf_springs_front` [steering_brakes_suspension] Local front leaf spring pack x2
- `part_local_leaf_springs_rear` [steering_brakes_suspension] Local rear leaf spring pack x2
- `part_mech_brake_flex_hose_set` [steering_brakes_suspension] Brake flexible hose set front and rear
- `part_old_man_emu_shocks` [steering_brakes_suspension] Ironman foam cell suspension - medium kit
- `part_omesb30_bushing_kit` [steering_brakes_suspension] OMESB30 suspension bushing kit
- `part_suspension_u_bolt_nut_plate_kit` [steering_brakes_suspension] Leaf spring U-bolt and nut plate kit front+rear

## Buy-Now / Quote-Ready With Confirmed Price

- `quote_pet_braided_sleeving` [electrical_reset] PET expandable braided sleeving (100ft 1/4 inch) (7414)

## Overlap Groups

- `floor_finish_stack` (6 rows): Floor/interior finish stack [action buckets: buy_now|deferred|next_phase]
- `grommet_options` (4 rows): Grommet options [action buckets: buy_now|completed_or_received|deferred]
- `primer_system_stack` (5 rows): Primer system stack [action buckets: buy_now|next_phase|ordered_waiting_arrival]
- `switch_options` (5 rows): Switch inventory [action buckets: buy_now|completed_or_received|deferred|next_phase|ordered_waiting_arrival]
- `wire_sleeving_options` (6 rows): Wire sleeving options [action buckets: buy_now|completed_or_received|quote_decision_ready]
- `wiring_kit_options` (4 rows): Wiring kit options [action buckets: completed_or_received|deferred|researching]
