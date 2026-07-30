# Parts List Review

- Generated: 2026-07-29 06:18:23
- Source: `data/manual/expenses.csv` (`bucket=parts`) -> 174 rows
- Review CSV: `data/manual/parts_list_review.csv`
- Overlap CSV: `data/manual/parts_overlap_candidates.csv`

## Action Buckets

- `buy_now`: 21
- `cancelled_or_not_required`: 25
- `completed_or_received`: 45
- `deferred`: 5
- `needs_confirmation`: 8
- `needs_spec_before_order`: 6
- `ordered_waiting_arrival`: 7
- `runner_spec_controlled`: 9
- `spec_ready_release_hold`: 2
- `unclear`: 46

## Workstream Split

- `turbocharger_powertrain`: 36
- `brake_system`: 31
- `body_chassis`: 26
- `electrical_reset`: 20
- `mechanical_baseline`: 17
- `ac_hvac_retrofit`: 14
- `fabrication_handoff`: 6
- `steering_brakes_suspension`: 5
- `interior_weatherproofing`: 5
- `chassis_fixing`: 4
- `chassis_rubbers`: 3
- `optional_upgrades`: 2
- `radiator`: 2
- `eps_vitz_upgrade`: 1
- `gearbox_oil_service`: 1
- `site_setup`: 1

## Price Coverage

- `has_confirmed_amount=yes`: 35
- `has_confirmed_amount=no`: 139

## Buy-Now / Quote-Ready Missing Price

- `part_hvac_barrier_hose_fittings_20260514` [ac_hvac_retrofit] A/C barrier hose and refrigerant-compatible fittings
- `part_hvac_blower_clutch_fan_wiring_20260514` [ac_hvac_retrofit] Relay, fuse, switch, and wiring pack for blower, compressor clutch, and condenser fan request
- `part_hvac_control_panel_20260514` [ac_hvac_retrofit] Compact A/C control panel or integrated controls
- `part_hvac_duct_defrost_hose_kit_20260514` [ac_hvac_retrofit] 2.5 inch duct hose, vent adapters, and defrost/demist hose kit
- `part_hvac_evaporator_drain_mount_kit_20260514` [ac_hvac_retrofit] Evaporator drain hose and mounting/sealing kit
- `part_hvac_firewall_bulkhead_fittings_20260514` [ac_hvac_retrofit] A/C firewall bulkhead fittings and sealing grommets
- `part_hvac_parallel_flow_condenser_20260514` [ac_hvac_retrofit] Parallel-flow A/C condenser sized to core support
- `part_hvac_r134a_oil_oring_charge_kit_20260514` [ac_hvac_retrofit] HNBR O-rings, refrigerant oil, vacuum/leak test, and R134a charge setup
- `part_hvac_receiver_drier_20260514` [ac_hvac_retrofit] Receiver-drier matched to R134a A/C layout
- `part_hvac_return_air_grille_filter_20260514` [ac_hvac_retrofit] Hidden return-air grille and washable filter for evaporator intake
- `part_hvac_slim_louver_outlet_panel_20260514` [ac_hvac_retrofit] Slim under-dash louver outlet panel / matched air-directing vent pieces
- `part_hvac_trinary_switch_20260514` [ac_hvac_retrofit] Trinary pressure switch for A/C compressor and fan control
- `part_body_retaining_clips_cotter_pin_pack` [body_chassis] Body retaining clip pack - R-clips hairpins split pins circlips and small cotters
- `part_fastener_kit_c_captive_clip_nuts` [body_chassis] Fastener Kit C remaining: Captive/clip/speed nut and weld-nut assortment - M6/M8
- `part_rear_brake_shoes_correct_k2221_20260722` [brake_system] Correct rear brake shoe axle set - MK Yellow K-2221-N/Y / Toyota 04494-60010 or 04494-60011
- `part_rear_center_brake_flex_hose` [brake_system] Rear center frame-to-axle brake flex hose - local/catalog first using 553-103 reference
- `part_fuel_filler_neck_hose_vent_20260619` [mechanical_baseline] Fuel filler rubber parts - main fuel fill hose vent hose and smooth-band clamps
- `part_mech_fuel_hose_and_clamps` [mechanical_baseline] Diesel fuel hose/line package - 8 mm feed, 6 mm return, leak-off hose, new hard lines
- `part_mech_heat_glow_plugs_set` [mechanical_baseline] Toyota OE glow plugs 19850-68030 x6 - diesel 2H
- `part_mech_oil_filter_guard_gdo135_20260529` [mechanical_baseline] Engine oil filter - Guard GDO-135 candidate for 2H
- `part_mech_vacuum_hose_refresh` [mechanical_baseline] Vacuum/breather hose kit - 10-12 mm vacuum + 16-19 mm oil-resistant breather

## Buy-Now / Quote-Ready With Confirmed Price

- None

## Overlap Groups

- `floor_finish_stack` (3 rows): Floor/interior finish stack [action buckets: deferred]
- `grommet_options` (2 rows): Grommet options [action buckets: buy_now|unclear]
- `switch_options` (2 rows): Switch inventory [action buckets: buy_now]
