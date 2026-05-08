# Chassis Bracket Audit - 2026-05-08

Evidence: refreshed WhatsApp MCP import generated `2026-05-08T15:22:35Z`, Akbar direct chat through `2026-05-08T15:04:01Z`.

## Why This Is A Hold

Akbar flagged that some brackets that should be welded on were previously wire-tied, with the radiator bracket named directly. David added the battery holder as another likely example. Akbar also estimated roughly `10-15` auxiliary additions before the chassis is final-coated.

This means Raptor is still the selected exposed chassis finish after primer/sealer, but final primer/Raptor should wait until the bracket survey is closed. Temporary flash-rust protection is acceptable if needed, but do not bury missing or poorly attached brackets under the final coating stack.

## Tasks Added

| Task | Workstream | Required closeout |
| --- | --- | --- |
| `chassis_missing_welded_bracket_survey_20260508` | `chassis_fixing` | Full station-by-station bracket map with keep/remove/repair/fabricate decisions. |
| `chassis_bracket_analysis_register_20260508` | `chassis_fixing` | Analysis register covering station, function, evidence, status, and primer/Raptor block state. |
| `chassis_bracket_design_release_20260508` | `chassis_fixing` | Released sketches/templates for every repair or fabricated bracket before metalwork starts. |
| `chassis_bracket_fabrication_install_20260508` | `chassis_fixing` | Fabricate, weld, bolt, grind, deburr, and trial-fit released baseline brackets only. |
| `chassis_bracket_validation_release_20260508` | `chassis_fixing` | Dry-fit and photo signoff proving no required bracket remains missing, loose, wire-tied, or unprotected. |
| `front_radiator_bracket_repair_20260508` | `chassis_fixing` | Radiator/support bracket location, fix method, rubber support, fan clearance, and labelled photos. |
| `front_radiator_two_side_retention_fabrication_20260508` | `chassis_fixing` | Released two-side radiator retention bracket set replacing the one-side/wire-held condition. |
| `battery_tray_holder_bracket_repair_20260508` | `chassis_fixing` | Battery tray/holder position, clamp path, drain/corrosion isolation, cable clearance, and final weld/bolt choice. |
| `battery_power_carrier_mount_fabrication_20260508` | `chassis_fixing` | Battery-side support/carrier for the MIDI Rev C plate and battery master cutoff/isolator, tied into real structure. |
| `engine_bay_mounting_scouting_pass_20260508` | `chassis_fixing` | Ruler photos and mock-up checks for radiator holes, battery tray feet, MIDI/cutoff envelope, cable exits, and bonnet clearance. |
| `auxiliary_chassis_tabs_and_clip_brackets_20260508` | `chassis_fixing` | Required baseline tabs only: line clips, harness clips, earth straps, exhaust hangers, washer/overflow/ancillary supports. |
| `exhaust_mockup_brackets_before_coating_20260508` | `chassis_fixing` | Exhaust fabricator gets current chassis photos; any hanger/clearance tabs needed on the chassis are mocked up before Raptor. |

## Work Plan

### 1. Analysis

Build a bracket register before more coating prep:

- Station and side.
- Current condition: intact, missing, bent, cracked, loose, wire-tied, non-baseline, or unknown.
- Function: radiator/support, battery holder, brake/fuel line clip, harness clip, earth strap, exhaust hanger, washer/overflow/ancillary support, or unknown.
- Evidence: current close-up photo, existing inventory photo, loose part sample, or WhatsApp note.
- Decision: keep, repair, fabricate, remove non-baseline, or hold for more evidence.
- Coating effect: blocks primer/Raptor, can be done after coating, or no action.

Close `chassis_bracket_analysis_register_20260508` only when the register covers the front support, radiator retention, battery tray, battery-side MIDI/cutoff carrier, both chassis rails, crossmembers, hard-line runs, rear rail, and exhaust route.

### 2. Design

Release each bracket before cutting or welding:

- Card or paper template where shape matters.
- Material and thickness.
- Hole diameter, slot size, stud size, or clip type.
- Bend direction, offset, and datum from a fixed chassis feature.
- Weld versus bolt decision.
- Clearance envelope to fan, radiator, belts, steering, suspension, brake/fuel lines, battery cables, bonnet, body, and exhaust.
- Coating plan: faces to prime before assembly, weld areas to clean after welding, bare-metal ground contact points to reopen later.

Unknown brackets stay hold/no-weld until their function is proven. Do not add generic auxiliary tabs just because access is good.

### 3. Implementation

Fabricate or repair only released baseline brackets:

1. Remove non-baseline wire ties and temporary straps only after photos record what they were holding.
2. Clean weld zones to bare metal.
3. Fit templates and tack brackets with the supported component or mock-up in place.
4. Trial-fit radiator/support rubbers, battery tray/clamp, line clips, harness clips, ground straps, and exhaust hanger/mock-up points.
5. Finish weld or bolt as released.
6. Grind only enough to remove sharp edges or bad weld profile; do not thin chassis bracket roots.
7. Clean heat-affected areas and prepare them for primer.

### 4. Validation

Before final primer/Raptor:

- Photograph each completed bracket with a label and ruler.
- Confirm radiator/fan/bonnet clearance.
- Confirm battery clamp security, cable route, and corrosion isolation.
- Confirm brake/fuel lines and harness clips are supported without rubbing.
- Confirm earth strap mounting faces have a planned bare-metal contact/re-protection step.
- Confirm exhaust hanger or route mock-up does not conflict with suspension, brake lines, tub, or service access.
- Confirm there are no remaining wire-tied required supports.

Only then can the bracket hold release the zinc-rich epoxy primer, seam sealer, Raptor, and cavity wax sequence.

## Survey Method

1. Walk the chassis front to rear and photograph every bracket, tab, clip point, hanger, and wire-tied attachment with a ruler or hand reference.
2. Use current body-off photos and loose removed parts to identify where a bracket clearly belongs.
3. Label each point as `keep`, `repair`, `fabricate`, `remove non-baseline`, or `unknown`.
4. For `unknown`, do not weld yet. Capture location photos and ask before adding optional brackets.
5. Finish welding/grinding before zinc-rich epoxy primer, seam sealer, and Raptor.

## Known First Checks

- Radiator support bracket(s): explicitly called out in WhatsApp. Current photo review makes this a two-side retention repair that replaces the wire-held/one-side condition.
- Battery tray/holder bracket(s): likely required, raised in the same exchange. Current photos show the battery-side engine-bay location but not enough tray-foot detail, so close-up scouting is required before cutting metal.
- Battery-side MIDI/cutoff carrier: use the existing MIDI Rev C plate as the fuse-holder component, but add a vehicle-side carrier/pickup design tied into the battery tray support or nearby structure.
- Exhaust hanger/mock-up points: coordinate now if the exhaust fabricator can mock up downpipes/routing while the tub is off.
- Brake/fuel line clips and harness P-clips: keep safety/serviceability ahead of appearance.
- Ground strap tabs: keep bare-metal contact strategy separate from final coating.

## Linked Fabrication Plan

The front engine-bay mounting tasks are detailed in [front-engine-bay-mounting-fabrication-plan-20260508.md](front-engine-bay-mounting-fabrication-plan-20260508.md). That plan is the working checklist for:

- `RAD-RET-001` radiator two-side retention.
- `BAT-TRAY-001` battery tray support upgrade.
- `PWR-CARRIER-001` battery-side MIDI/cutoff carrier.
- `PWR-CABLE-001` heavy cable and P-clip support.

Any welded pickup point from that plan is a pre-primer/Raptor item. The removable MIDI plate, insulating subplate, cutoff switch, and final cable clips can be fitted after coating only if their structural pickup points are already complete.

## Evidence Refs

- `mcp_whatsapp_akber_20260508_142600`: brackets should be welded; previous guy wire-tied some; radiator bracket named.
- `mcp_whatsapp_akber_20260508_142752`: radiator and battery holder acknowledged.
- `mcp_whatsapp_akber_20260508_142816`: exhaust mock-up opportunity while access is open.
- `mcp_whatsapp_akber_20260508_142840`: estimated `10-15` additions.
