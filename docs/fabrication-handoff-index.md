# Fabrication Handoff Index

Purpose: one send-out index for the ready-to-run non-rubber fabrication packages in this repository.

All package dimensions are in `mm`. For each package, send the package PDF for human review plus the listed `DXF` files for cutting. Keep the matching `SVG` files with the job if the shop wants a quick visual reference.

Dashboard UI: open the `Fabrication` workstream in `docs/project-control-ui/` for clickable package links, status gates, and first-article steps.

Raw material procurement: use [fabrication-raw-materials-procurement-estimate-20260513.md](fabrication-raw-materials-procurement-estimate-20260513.md), [fabrication-metal-stock-list-20260514.md](fabrication-metal-stock-list-20260514.md), and `data/manual/fabrication_raw_material_estimates.csv`. The matching raw-stock rows have been added to the procurement ledger, including the `3.0 mm` and `4.0 mm` pre-formed `90-degree` angle/L-section asks and separate tub repair sheet/plate stock so battery/radiator fabrication steel is not consumed by body patches.

## Chassis Rubber Boundary

Chassis/body rubber order control is not owned here. Use [chassis-rubbers-workstream.md](chassis-rubbers-workstream.md) and [longman-rubber-order-spec-20260508.md](longman-rubber-order-spec-20260508.md) for body-mount pads, front-support isolators, bump stops, sleeves, shims, cup washers, and related Longman/first-article release holds.

The old rubber package files remain in the repository as supporting reference material, but the active Fabrication workstream should not send or close chassis-rubber orders independently. The current Longman package lives at [data/manual/fabrication/longman_rubber_order_20260508](../data/manual/fabrication/longman_rubber_order_20260508/README.md), with an interactive 3D visualisation and a package zip generated through the dashboard. The current square-pad 3D quote models live in [data/manual/fabrication/rubber_recreation_rev_a/models_3d](../data/manual/fabrication/rubber_recreation_rev_a/models_3d/README.md); use those rather than the older circular body-pad placeholders when discussing the May 8 Longman rubber order.

## Dashboard 9-inch LCD / HVAC Fascia - Rev I (active design hold)

Current specification and packaging gate: [data/manual/fabrication/dashboard_lcd_hvac_fascia_rev_i](../data/manual/fabrication/dashboard_lcd_hvac_fascia_rev_i/README.md)

Current geometric appearance baseline: [dashboard_rev_i_v35_registered_center_cassette_overlay.png](../data/manual/fabrication/dashboard_lcd_hvac_fascia_rev_i/dashboard_rev_i_v35_registered_center_cassette_overlay.png), with the [exact-scale V35 elevation](../data/manual/fabrication/dashboard_lcd_hvac_fascia_rev_i/dashboard_rev_i_v35_provisional_front_elevation.svg), [quotation CNC specification](../data/manual/fabrication/dashboard_lcd_hvac_fascia_rev_i/dashboard_rev_i_v35_quotation_cnc_spec.md) and [provisional coordinates](../data/manual/fabrication/dashboard_lcd_hvac_fascia_rev_i/dashboard_rev_i_v35_provisional_coordinates.csv).

V35 keeps the OEM glovebox, speedometer/cluster, RHD column scallop, full-width lower edge and all formed contours unchanged. Only the ashtray/centre area is replaced with a removable centre cassette. Its default extension/drop is 0 mm; any later extension is centre-only, no larger than the physically measured shortfall, and requires owner approval. The cassette holds the provisional 211.10 × 126.50 mm 9-inch module plus one line of seven bought black long-lever selectors and a separate red HAZARD below the LCD. Exactly two Ø87 mm target outlet faces remain, each centred in a retained measured outer clear land. All component apertures and rear packaging remain HOLD pending physical traces, actual components and a rigid full-depth rear buck.

Portal/CNC handoff: use the [measurement and survey checklist](../data/manual/fabrication/dashboard_lcd_hvac_fascia_rev_i/cnc_measurement_and_survey_checklist.md) and [fillable M1–M10 schedule](../data/manual/fabrication/dashboard_lcd_hvac_fascia_rev_i/cnc_measurement_schedule.csv) for an exact production release. The V35 image, elevation, specification and coordinates above are quotation/prototype inputs only and must not be used to cut the vehicle or production fascia.

## Dashboard 9-inch LCD / HVAC Fascia - Rev G (superseded four-outlet record)

Directory: [data/manual/fabrication/dashboard_lcd_hvac_fascia_rev_g](../data/manual/fabrication/dashboard_lcd_hvac_fascia_rev_g/README.md)

Send-out archive: `deliverables/fabrication_packages/dashboard_lcd_hvac_fascia_rev_g.zip`

Primary files:
- `j40_dashboard_lcd_hvac_fascia_rev_g_shop_spec.pdf`
- `dashboard_lcd_hvac_fascia_rev_g_dimensioned_front.svg`
- `dashboard_lcd_hvac_fascia_rev_g_photo_overlay_bare_shell.png`
- `dashboard_lcd_hvac_fascia_rev_g_photo_overlay_assembled.png`
- `fabricator_cut_and_release_schedule.csv`
- `measurement_and_release_schedule.csv`
- `switch_position_schedule.csv`
- `dimensional_provenance_audit.csv`

DXF files:
- `full_width_fit_template_rev_g.dxf` - nominal `1260 x 280 mm` full-face coordinate/template envelope with three local vent drops; M1 physical trace controls the final perimeter
- `full_width_fascia_master_rev_g.dxf` - same one-piece architecture with every metal/component feature retained on named HOLD layers
- `lcd_rear_support_reference_rev_g.dxf` - nominal rear-support/reference geometry; actual LCD chassis and mount drawing control

Rev G superseded Rev A-F, but is itself superseded by Rev I above. It replaced the complete visible face, deleted the ashtray, transferred the original glovebox and speedometer assemblies, locked a mathematically true 9-inch active-image reference, integrated four same-height vents, and consolidated all controls at the far right. Retain it for design history only; do not send its four-outlet coordinates as the current dashboard job.

Release position:
- Ready for CNC quotation, full-size vehicle trace/scan, 1:1 plot and disposable prototype only.
- Do not cut production vehicle metal or final LCD/selector/hazard/vent apertures until M1-M10 are closed against the actual vehicle and bought parts, rear screen/contact blocks and duct bends clear, and the owner signs the physical 1:1 layout.
- The nominal fascia centreline is `X=630.0`. LCD active image, bezel and aperture share it exactly. Inner vent centres are `X=555.0` and `705.0`, so their midpoint is exactly `X=630.0`; all four vent centres share `Y=50.0`.
- Exactly seven selectors are shown: top Wipers, Lights, Spots, Aux; bottom Blower, A/C, Engine; the separate red Hazard occupies the eighth bank position and is not counted among the seven.
- Functions matched the purchased four 2-position plus three 3-position inventory. The historical `ENGINE` label is now named `FUEL STOP` in Rev I and remains an EEI-003 electrical release HOLD with key OFF authoritative and manual cable retained; A/C remains subject to thermostat/pressure/trinary interlocks. T1/T2 remain low/high beam and the original dip control remains in service.
- Screen mass is carried by rear supports tied into the dashboard structure, not the `1.5 mm` visible fascia alone. Electrical selectors command relays/controller inputs rather than carrying accessory loads directly.

## Battery Stand Power Carrier - Rev A

Directory: [data/manual/fabrication/battery_power_carrier_mount_rev_a](../data/manual/fabrication/battery_power_carrier_mount_rev_a/README.md)

Control spec: [front-engine-bay-mounting-fabrication-plan-20260508.md](front-engine-bay-mounting-fabrication-plan-20260508.md)

Primary files:
- `data/manual/fabrication/battery_power_carrier_mount_rev_a/j40_battery_power_carrier_mount_rev_a_dimension_sheet.pdf`
- `data/manual/fabrication/battery_power_carrier_mount_rev_a/battery_power_carrier_mount_rev_a_assembled_3d_visualisation.html`
- `data/manual/fabrication/battery_power_carrier_mount_rev_a/battery_power_carrier_mount_rev_a_assembled_3d_visualisation.svg`
- `data/manual/fabrication/battery_power_carrier_mount_rev_a/battery_power_carrier_mount_rev_a_3d_visualisation.html`
- `data/manual/fabrication/battery_power_carrier_mount_rev_a/battery_power_carrier_mount_rev_a_3d_visualisation.svg`
- `data/manual/fabrication/battery_power_carrier_mount_rev_a/fabricator_cut_list.csv`
- `data/manual/fabrication/battery_power_carrier_mount_rev_a/inspection_checklist.csv`
- `data/manual/fabrication/battery_power_carrier_mount_rev_a/component_layout.csv`

DXF files:
- `battery_stand_compact_top_tray_rev_b.dxf` - steel compact `340 x 265 mm` battery tray/deck for the installed Daewoo DLS120 datum from the May 17 ruler photos, with the previous `318 x 180 x 230 mm` envelope kept only as comparison, qty `1`
- `battery_stand_compact_single_chassis_pickup_rev_b.dxf` - formed chassis saddle over rail, qty `1`
- `battery_stand_adjustable_offset_bar_rev_b.dxf` - slotted `360 x 60 x 4 mm` body-side offset bar from the formed chassis saddle/upright bridge toward the battery pocket, qty `2 mirrored`
- `battery_stand_compact_single_mount_upright_rev_b.dxf` - upright bridge side plate, qty `2 mirrored`
- `battery_stand_compact_hold_down_crossbar_rev_b.dxf` - service-removable `340 x 38 mm` battery hold-down crossbar, qty `1`
- `battery_power_compact_front_service_rail_rev_b.dxf` - **superseded/hold**; do not fabricate this former `660 x 310 mm` relay/MIDI battery-stand ladder under the 2026-07-31 layout decision
- `battery_power_compact_cutoff_tab_rev_b.dxf` - folded 100A breaker/cutoff base/guard, qty `1`

Release position:
- 2026-07-31 supersession: retain this package only for the battery tray, chassis saddle/support, hold-down, and battery-side cutoff/breaker. Relay Rev D and MIDI Rev D move to a removable plate on the structural radiator/cooling-stack carrier.
- Rev F standard-battery access update is a prototype/mock-up release for the steel chassis-mounted battery stand.
- The stand must mount from the one known formed chassis saddle, upright bridge, and slotted body-side offset bars, not the battery tray skin, radiator support strap, or unsupported inner wing.
- It supports the installed Daewoo DLS120 battery datum captured in the May 17 ruler photos on a removable hold-down tray and retains the 100A breaker/cutoff close to the battery.
- The tray/front ladder starts around `190 mm` wing-side/outboard from the more central chassis pickup, with the offset bars retaining `160-230 mm` adjustment until dry-fit locks the setting.
- Battery positive must enter the battery-side cutoff/breaker first. Its protected output runs to the structural cooling-stack electrical plate, where it feeds MIDI fuse 4 and the relay battery-side entry without changing circuit assignments or fuse sizing.
- Final drilling still needs the battery/cutoff mock-up plus a separate radiator-carrier electrical mock-up proving airflow, fan/shroud, hose, cap, drain, bonnet, grille, heat/splash, relay-cover, MIDI-lid, cable-bend, disconnect, and radiator-removal clearances.

## Front Radiator Two-Side Retention - Rev A

Directory: [data/manual/fabrication/front_radiator_two_side_retention_rev_a](../data/manual/fabrication/front_radiator_two_side_retention_rev_a/README.md)

Control spec: [front-engine-bay-mounting-fabrication-plan-20260508.md](front-engine-bay-mounting-fabrication-plan-20260508.md)

Primary files:
- `data/manual/fabrication/front_radiator_two_side_retention_rev_a/j40_front_radiator_two_side_retention_rev_a_dimension_sheet.pdf`
- `data/manual/fabrication/front_radiator_two_side_retention_rev_a/front_radiator_two_side_retention_rev_a_assembled_3d_visualisation.html`
- `data/manual/fabrication/front_radiator_two_side_retention_rev_a/front_radiator_two_side_retention_rev_a_assembled_3d_visualisation.svg`
- `data/manual/fabrication/front_radiator_two_side_retention_rev_a/front_radiator_two_side_retention_rev_a_3d_visualisation.html`
- `data/manual/fabrication/front_radiator_two_side_retention_rev_a/front_radiator_two_side_retention_rev_a_3d_visualisation.svg`
- `data/manual/fabrication/front_radiator_two_side_retention_rev_a/fabricator_cut_list.csv`
- `data/manual/fabrication/front_radiator_two_side_retention_rev_a/inspection_checklist.csv`

DXF files:
- `front_radiator_saddle_right_angle_post_rev_a.dxf` - 4 mm bolt-through saddle right-angle post, qty `1`

Release position:
- Rev A is a template release for one simple steel post: 90 degree top return with one radiator screw point, plus lower legs that straddle the chassis/front-support section.
- Final bending/drilling remains gated by right-side vehicle dry-fit, transferred left-bracket dimensions, screw size, radiator ear offset, chassis width, through-bolt route, crush-tube/spacer decision, rubber washer/bush stack, and fan clearance.
- The Bracket Analysis Register remains the evidence/action register; this package is the Fabrication handoff for making the bracket templates.

## Integrated Radiator & Front Cooling Pack - Rev C.1 (Current)

**Current controlled handoff — issued 30 July 2026.** Use this package for the radiator shop, A/C installer and fabrication mock-up. **Final core manufacture remains HOLD** until the documented vehicle measurements, full-size dummy fit and written owner approval are complete.

Controlled specification: [J40-integrated-cooling-pack-fabricator-specification-rev-c.docx](J40-integrated-cooling-pack-fabricator-specification-rev-c.docx) and [source Markdown](J40-integrated-cooling-pack-fabricator-specification-rev-c.md)

Dimensioned drawing assets: [data/manual/fabrication/front_cooling_stack_rev_c/work_document_assets](../data/manual/fabrication/front_cooling_stack_rev_c/work_document_assets/)

Release position:
- The Rev C.1 drawing register covers the complete front elevation, radiator orthographic/interface sheet, exploded radiator parts, condenser/intercooler/dual-fan dimensions, mounting/saddles/shroud, side-depth gates, and dual-fan mounting/wiring.
- **Two matching slim 9-inch 12 V pusher fans are mandatory**, mounted side-by-side above the intercooler. Each fan has its own fused and relayed branch; retain the original engine-driven puller and a close removable shroud.
- The Rev A optional single-fan provision is **not current** and must not be substituted for the required dual-fan arrangement.
- Red dimensions are fixed nominal requirements. Purple items and every unlabeled position must be measured on the actual vehicle and released in writing before final core manufacture.

## Front Cooling Stack Frame - Rev A (Legacy / Superseded)

**Superseded by Integrated Radiator & Front Cooling Pack Rev C.1 on 30 July 2026. Do not issue Rev A as the current radiator-shop or fan specification.** It remains only as historical reference for earlier frame work.

Directory: [data/manual/fabrication/front_cooling_stack_rev_a](../data/manual/fabrication/front_cooling_stack_rev_a/README.md)

Control spec: [front-cooling-stack-fabrication-plan-20260530.md](front-cooling-stack-fabrication-plan-20260530.md)

Primary files:
- `data/manual/fabrication/front_cooling_stack_rev_a/README.md`
- `docs/l4tw-front-cooling-stack-delivery-spec-20260531.md`
- `data/manual/fabrication/front_cooling_stack_rev_a/delivery_spec_l4tw_20260531.csv`
- `docs/front-cooling-stack-local-parts-selection-20260530.md`
- `data/manual/fabrication/front_cooling_stack_rev_a/local_parts_selection_pakistan_20260530.csv`
- `data/manual/fabrication/front_cooling_stack_rev_a/known_price_fit_check_pakistan_20260530.csv`
- `data/manual/fabrication/front_cooling_stack_rev_a/front_cooling_stack_rev_a.svg`
- `data/manual/fabrication/front_cooling_stack_rev_a/component_layout.csv`
- `data/manual/fabrication/front_cooling_stack_rev_a/measurement_basis.csv`
- `data/manual/fabrication/front_cooling_stack_rev_a/fabricator_cut_list.csv`
- `data/manual/fabrication/front_cooling_stack_rev_a/inspection_checklist.csv`

DXF files:
- None in Rev A. This is a site-fit mock-up/fabricator spec because upright height, chassis saddle width, radiator tabs, condenser tabs, drier clamp, fan hoop, and hole centres must be transferred from the actual vehicle and selected parts.

Release position:
- Rev A turns the prior one-side radiator support repair into a full front cooling-stack frame when both full-height chassis/front-support uprights are being fabricated.
- It carries the HJ47/2H radiator, R134a parallel-flow condenser, optional slim pusher fan, and receiver-drier as separate rubber-isolated components.
- The L4TW delivery spec is the acceptance contract: corrected radiator, two-side frame, condenser, fan provision, drier, pressure switch, compressor gate, barrier hoses, electrical protection, and final validation evidence.
- The local buy package selects Master Radiators/KorTech for the radiator route, Snow Cool/Arsalan for condenser/drier/evaporator leads, and Sanpak/Arsalan/Cool Sun style A/C hose support, but final purchase remains gated by dimensions and fitting proof.
- The existing Sanden-type compressor is compatible in principle with the condenser/drier layout, but hose crimping and final charge remain blocked until the compressor port style, clutch voltage, belt alignment, oil/refrigerant state, leak test, and pressure-switch protection are confirmed.

## 2H Turbo-Readiness Chassis Provisions - Rev A

Current controlled build process: [2h-turbo-recommended-build-process-20260801.md](2h-turbo-recommended-build-process-20260801.md)

Illustrative build-sequence assets: [docs/images/turbo-2h-controlled-build](images/turbo-2h-controlled-build/README.md)

Current packaging matrix: [data/manual/fabrication/turbo_packaging_rev_a](../data/manual/fabrication/turbo_packaging_rev_a/README.md)

Visual guide archive: `deliverables/fabrication_packages/2h_turbo_controlled_build_visuals_rev_d_20260802.zip`

The current guide uses a four-step sequence for goods-receipt inspection, full-vehicle steering/hot-side mock-up, a paired near-side/opposite-side Rev H packaging study using recognisable real component forms, and monitored static commissioning. The current study removes the unused compact-air-cleaner alternative and provisional side/wing cooler; the archive retains the earlier cardboard-envelope studies as visual history. The relocation matrix makes retain/move/add/decision actions explicit. Every image is non-dimensional and cannot close an identity, clearance, fabrication or test gate.

Directory: [data/manual/fabrication/turbo_readiness_chassis_rev_a](../data/manual/fabrication/turbo_readiness_chassis_rev_a/README.md)

Control spec: [turbo-readiness-chassis-welder-fabrication-spec-20260717.md](turbo-readiness-chassis-welder-fabrication-spec-20260717.md)

Primary files:
- `data/manual/fabrication/turbo_readiness_chassis_rev_a/README.md`
- `data/manual/fabrication/turbo_readiness_chassis_rev_a/fabrication_scope.csv`
- `data/manual/fabrication/turbo_readiness_chassis_rev_a/inspection_checklist.csv`

DXF files:
- None. This is a measured site-fit interface release; turbo-dependent positions and hole centres must be transferred from the assembled vehicle or rigid full-size templates.

Release position:
- **Superseded as a current welder handout on 2026-07-19.** Use [chassis-welder-steering-turbo-component-first-instruction-20260719.md](chassis-welder-steering-turbo-component-first-instruction-20260719.md).
- Released now: clean/inspect/photograph the existing steering-box mount and continue unrelated approved chassis work.
- No J80 steering, battery-carrier lock or turbo conversion-specific welding is released until the actual matched component sets are present for trial fit. Use `docs/chassis-welder-j80-steering-turbo-component-first-instruction-20260802.md`; the older J60 handout is historical.
- Conditional after physical component trial fit: steering mounting/reinforcement, line/loom relocation tabs, exhaust-hanger interfaces, heat-shield interfaces and removable airbox/breather/charge-support interfaces.
- Explicitly excluded: manifold, turbo support, downpipe, complete exhaust, sump/oil-return work and charge-pipe fabrication.

## Suspension Wood Cribbing - Rev A

Directory: [data/manual/fabrication/suspension_wood_cribbing_rev_a](../data/manual/fabrication/suspension_wood_cribbing_rev_a/README.md)

Control spec: [suspension-wood-cribbing-merchant-spec.md](suspension-wood-cribbing-merchant-spec.md)

Primary files:
- `data/manual/fabrication/suspension_wood_cribbing_rev_a/j40_suspension_wood_cribbing_rev_a_dimension_sheet.pdf`
- `data/manual/fabrication/suspension_wood_cribbing_rev_a/suspension_wood_cribbing_rev_a_3d_visualisation.html`
- `data/manual/fabrication/suspension_wood_cribbing_rev_a/suspension_wood_cribbing_rev_a_3d_visualisation.svg`
- `data/manual/fabrication/suspension_wood_cribbing_rev_a/fabricator_cut_list.csv`
- `data/manual/fabrication/suspension_wood_cribbing_rev_a/inspection_checklist.csv`

DXF files:
- `swc_rectangular_cribbing_block_rev_a.dxf` - rectangular hardwood cribbing block, qty `8`
- `swc_wedge_chock_rev_a.dxf` - wedge chock side/top/end profile, qty `4`

Release position:
- Drawing backup for the suspension-owned cribbing buy in [suspension-wood-cribbing-merchant-spec.md](suspension-wood-cribbing-merchant-spec.md).
- Control dimensions are metric: blocks `300 x 150 x 75 mm`; wedges `200 x 100 mm` base with `75 mm` rear height and `25 mm` nose height.
- These are supplemental cribbing/chocks only and must not be treated as substitutes for rated jack stands or axle support.

## Electrical Mounting Packages

### MIDI 5-Way Hinged Enclosure - Rev D

Directory: [data/manual/fabrication/midi5_enclosure_rev_d](../data/manual/fabrication/midi5_enclosure_rev_d/README.md)

Primary files:
- `data/manual/fabrication/midi5_enclosure_rev_d/j40_midi5_enclosure_rev_d_dimension_sheet.pdf`
- `data/manual/fabrication/midi5_enclosure_rev_d/midi5_enclosure_rev_d_3d_visualisation.html`
- `data/manual/fabrication/midi5_enclosure_rev_d/midi5_enclosure_rev_d_3d_visualisation.svg`

DXF files:
- `midi5_enclosure_body_rev_d.dxf` - `3.0 mm` 5052-H32 aluminium folded enclosure body
- `midi5_holder_subplate_rev_d.dxf` - `5.0 mm` HDPE, ABS, G10, or phenolic holder board
- `midi5_enclosure_lid_rev_d.dxf` - `2.0-3.0 mm` aluminium hinged lid

Order definitions:
- Enclosure body: finished floor `210 x 165 mm` with `65 mm` folded side walls, hinge holes on the input/bus side, latch holes on the output side, one `20 mm` input grommet pilot aligned to fuse 4 / the second-from-last holder, and five output-side grommet pilot holes.
- Far-side output hole: enlarged `28 mm` pilot for the output that carries `2` power cables. The other four output holes are `16 mm` pilots. Open every pilot to the final cable/grommet OD after measurement.
- Holder subplate: `140 x 85 mm` non-conductive board with ten `4.5 mm` holder holes on `20.2 mm` pitch / `44 mm` row separation, plus six `5.5 mm` standoff holes.
- Lid: `230 x 185 mm` aluminium cover panel with hinge holes on the input/bus side and latch holes on the output side.

Release position: current recommended MIDI holder route. The external plastic/CNC quote is still only for the holder subplate; the aluminium enclosure body and lid are owner-made or sheet-metal-shop parts. Use `10-12 mm` insulated/sleeved spacers between the holder board and enclosure floor, and fit rubber grommets before wiring.

### Relay Mount - Rev D

Directory: [data/manual/fabrication/relay_mount_rev_d](../data/manual/fabrication/relay_mount_rev_d/README.md)

Primary files:
- `data/manual/fabrication/relay_mount_rev_d/j40_relay_mount_rev_d_dimension_sheet.pdf`
- `data/manual/fabrication/relay_mount_rev_d/relay_mount_rev_d_3d_visualisation.html`
- `data/manual/fabrication/relay_mount_rev_d/relay_mount_rev_d_3d_visualisation.svg`

DXF files:
- `relay_base_plate_rev_d.dxf` - flat `360 x 245 x 3.0 mm` 5052-H32 aluminium base plate with structural-carrier-plate attachment slots
- `relay_insulating_sheet_rev_d.dxf` - exact `300 x 197 x 3.0 mm` relay-box-bottom-footprint insulating sheet

Order definitions:
- Base plate: flat aluminium only. Use exposed margins/slots to attach the relay assembly to a removable plate on the structural radiator/cooling-stack carrier; never to the core, fins, tanks, necks, seams, or through-core rods.
- Insulating sheet: sits directly between the already-covered relay/fuse box and the aluminium base. Transfer relay-box fixing holes from the actual enclosure after orientation is confirmed.

Release position: current recommended relay-box fabrication route. Rev D supersedes the folded Rev C relay carrier because the existing relay box is already a covered enclosure.

## Electrical Underlay / Insulator Requirements

These non-metal electrical underlays/guards are tracked separately from owner-made metal plates and brackets:

| Requirement | Package file | Definition | Status |
| --- | --- | --- | --- |
| MIDI holder insulating underlay / subplate | `midi5_enclosure_rev_d/midi5_holder_subplate_rev_d.dxf` | `140 x 85 x 5.0 mm` HDPE/ABS/G10/phenolic board; ten `4.5 mm` holder holes; six `5.5 mm` standoff holes. | Current external plastic/CNC quote row. |
| Relay insulating sheet | `relay_mount_rev_d/relay_insulating_sheet_rev_d.dxf` | Exact `300 x 197 x 3.0 mm` ABS/HDPE/polypropylene/G10/phenolic sheet between the existing relay box's large uncovered bottom face and the flat aluminium base. | Current relay-box underlay. |

## Superseded Electrical History

The older MIDI module packages remain in the repo as history, but should not be sent as the current fabrication route unless that older design is deliberately reopened:
- `data/manual/fabrication/midi5_module_rev_a`
- `data/manual/fabrication/midi5_module_rev_b`
- `data/manual/fabrication/midi5_plate_mount_rev_c`
- `data/manual/fabrication/relay_mount_rev_c`

## Shop Instructions

- Confirm material and thickness on the purchase order before cutting.
- Do not treat construction, bend, recess, register, insert, or template layers as through-cuts unless the package README says so.
- Wood cribbing DXFs are dimensional saw-cut/profile references for the timber/workshop package, not vehicle mounting parts.
- Deburr all metal parts and apply corrosion protection after forming.
- Trial-fit first articles before batch production or final loom/body closeout.
