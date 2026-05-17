# Parts List Review

- Generated: 2026-05-17 16:31:08
- Source: `data/manual/expenses.csv` (`bucket=parts`) -> 120 rows
- Review CSV: `data/manual/parts_list_review.csv`
- Overlap CSV: `data/manual/parts_overlap_candidates.csv`

## Action Buckets

- `buy_now`: 39
- `cancelled_or_not_required`: 12
- `completed_or_received`: 32
- `deferred`: 6
- `needs_spec_before_order`: 15
- `ordered_waiting_arrival`: 5
- `spec_ready_release_hold`: 4
- `unclear`: 7

## Workstream Split

- `body_chassis`: 27
- `brake_system`: 24
- `mechanical_baseline`: 23
- `electrical_reset`: 20
- `interior_weatherproofing`: 11
- `steering_brakes_suspension`: 6
- `fabrication_handoff`: 6
- `optional_upgrades`: 2
- `chassis_fixing`: 1

## Price Coverage

- `has_confirmed_amount=yes`: 20
- `has_confirmed_amount=no`: 100

## Buy-Now / Quote-Ready Missing Price

- `part_body_retaining_clips_cotter_pin_pack` [body_chassis] Body retaining clip pack - R-clips hairpins split pins circlips and small cotters
- `part_fastener_kit_c_captive_clip_nuts` [body_chassis] Fastener Kit C remaining: Captive/clip/speed nut and weld-nut assortment - M6/M8
- `part_tub_mount_reinforcement_plate_3mm_20260513` [body_chassis] 3.0 mm mild-steel plate for tub body-mount backing and captive-nut repairs
- `part_tub_repair_steel_sheet_1_2mm_20260513` [body_chassis] 1.2 mm cold-rolled mild-steel sheet for tub skin/floor patch plates
- `part_tub_repair_steel_sheet_1_6mm_20260513` [body_chassis] 1.6 mm cold-rolled mild-steel sheet for heavier tub patch plates
- `part_brake_clutch_475_hard_line_stock_full_vehicle_20260514` [brake_system] Full vehicle brake/clutch hard-line tube stock - 4.75 mm / 3/16 in OD, 12 m preferred
- `part_brake_clutch_line_support_clamps_full_vehicle_20260514` [brake_system] Full vehicle brake/clutch line support pack - P-clips, clamp-on axle supports, edge protection
- `part_brake_flex_hose_retaining_clip_pack_20260514` [brake_system] Brake flex-hose retaining U-clips and bracket hardware pack
- `part_brake_fluid_bleed_consumables` [brake_system] Brake hydraulic opening prep remaining consumables - caps plugs bleed bottle cleaner rags catch tray
- `part_cabin_compact_fuse_boxes` [electrical_reset] Compact cabin fuse protection - reuse 12-way plus buy one compact OEM add-on
- `part_firewall_grommet_set_large_power` [electrical_reset] Additional firewall grommet set IDs 16/20/25 mm
- `part_firewall_grommet_set_small_medium` [electrical_reset] Additional firewall grommet set IDs 6/8/10/12 mm
- `part_hvac_blower_clutch_fan_wiring_20260514` [electrical_reset] Relay, fuse, switch, and wiring pack for blower, compressor clutch, and condenser fan request
- `part_fabrication_raw_aluminium_plate_3mm_20260513` [fabrication_handoff] 3.0 mm 5052-H32 aluminium sheet for MIDI enclosure, Relay Rev D base, and cutoff electrical plates
- `part_fabrication_raw_electrical_plastic_sheet_20260513` [fabrication_handoff] Electrical insulating plastic/G10 sheet - MIDI 5.0 mm board and relay 3.0 mm sheet
- `part_fabrication_raw_epdm_sheet_small_isolators_20260513` [fabrication_handoff] 3-5 mm EPDM/SBR sheet for radiator isolator and small anti-chafe pads
- `part_fabrication_raw_mild_steel_plate_3mm_20260513` [fabrication_handoff] 3.0 mm mild-steel sheet plus 90-degree angle/L-section stock for compact battery tray/access ladder
- `part_fabrication_raw_mild_steel_plate_4mm_20260513` [fabrication_handoff] 4.0 mm mild-steel plate plus structural 90-degree angle/L-section stock for compact battery saddle/upright/offset bars and radiator post
- `part_hvac_control_panel_20260514` [interior_weatherproofing] Compact A/C control panel or integrated controls
- `part_hvac_duct_defrost_hose_kit_20260514` [interior_weatherproofing] 2.5 inch duct hose, vent adapters, and defrost/demist hose kit
- `part_hvac_evaporator_drain_mount_kit_20260514` [interior_weatherproofing] Evaporator drain hose and mounting/sealing kit
- `part_hvac_hidden_evaporator_blower_unit_20260514` [interior_weatherproofing] Hidden compact evaporator/blower/heater/defrost unit for under-dash fitment
- `part_hvac_return_air_grille_filter_20260514` [interior_weatherproofing] Hidden return-air grille and washable filter for evaporator intake
- `part_hvac_slim_louver_outlet_panel_20260514` [interior_weatherproofing] Slim under-dash louver outlet panel and adjustable vents
- `part_hvac_barrier_hose_fittings_20260514` [mechanical_baseline] A/C barrier hose and refrigerant-compatible fittings
- `part_hvac_firewall_bulkhead_fittings_20260514` [mechanical_baseline] A/C firewall bulkhead fittings and sealing grommets
- `part_hvac_parallel_flow_condenser_20260514` [mechanical_baseline] Parallel-flow A/C condenser sized to core support
- `part_hvac_r134a_oil_oring_charge_kit_20260514` [mechanical_baseline] HNBR O-rings, refrigerant oil, vacuum/leak test, and R134a charge setup
- `part_hvac_receiver_drier_20260514` [mechanical_baseline] Receiver-drier matched to R134a A/C layout
- `part_hvac_trinary_switch_20260514` [mechanical_baseline] Trinary pressure switch for A/C compressor and fan control
- `part_mech_accessory_belt_set` [mechanical_baseline] Accessory belt set
- `part_mech_engine_oil_filter_service` [mechanical_baseline] Engine oil + oil filter service pack
- `part_mech_fuel_filter` [mechanical_baseline] Fuel filter
- `part_mech_fuel_hose_and_clamps` [mechanical_baseline] Diesel fuel hose/line package - 8 mm feed, 6 mm return, leak-off hose, new hard lines
- `part_mech_heat_glow_plugs_set` [mechanical_baseline] Toyota OE glow plugs 19850-68030 x6 - diesel 2H
- `part_mech_heater_hose_set` [mechanical_baseline] Heater hose pair - EPDM 400 mm inlet + 280 mm outlet, 16 mm ID
- `part_mech_radiator_cap` [mechanical_baseline] Radiator cap
- `part_mech_radiator_hose_set` [mechanical_baseline] Cooling hose/pipe package - upper/lower radiator hoses, overflow hose, formed coolant pipe
- `part_mech_vacuum_hose_refresh` [mechanical_baseline] Vacuum/breather hose kit - 10-12 mm vacuum + 16-19 mm oil-resistant breather

## Buy-Now / Quote-Ready With Confirmed Price

- None

## Overlap Groups

- `floor_finish_stack` (3 rows): Floor/interior finish stack [action buckets: deferred]
- `grommet_options` (4 rows): Grommet options [action buckets: buy_now|deferred]
- `switch_options` (4 rows): Switch inventory [action buckets: buy_now]
