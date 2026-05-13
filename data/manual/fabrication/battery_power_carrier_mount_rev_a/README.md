# J40 Battery Stand Power Carrier Pack - Rev B Compact Update

This package changes the battery-side plan into a compact steel chassis-bolted stand that supports the battery first, then uses measured rail/tab pickups for the already-fabricated electrical holders. It deliberately supersedes the earlier large shared backplane.

## Design Intent

- Mount the battery stand from the one known chassis pickup location using a compact single pickup plate and upright bridge.
- Support the battery on a compact `315 x 265 mm` tray around the current `275 x 230 mm` battery datum.
- Treat Relay Rev C as the folded aluminium tray it already is: `320 x 220 mm` finished face, `360 x 255 mm` flat pattern, `20 mm` side/bottom returns, and `15 mm` top return.
- Treat MIDI Rev C as an open `190 x 150 mm` aluminium plate plus `140 x 85 mm` insulating subplate, not a folded tray.
- Put the cutoff switch on its own compact `170 x 110 mm` tab/guard so it can move to the most accessible front/top position.
- Default to split/stepped compact holders. Do not make a one-piece carrier unless the filled cavity map proves it.

## Parts In This Package

1. `battery_stand_compact_top_tray_rev_b` - 3 mm mild-steel compact battery tray/deck with clamp and cable-clip zones.
2. `battery_stand_compact_single_chassis_pickup_rev_b` - 4 mm mild-steel base plate for the one chassis pickup location.
3. `battery_stand_compact_single_mount_upright_rev_b` - 4 mm mild-steel upright bridge side plate; make a mirrored pair if the mock-up needs side-to-side stiffness.
4. `battery_stand_compact_hold_down_crossbar_rev_b` - compact battery hold-down crossbar template.
5. `battery_power_compact_front_service_rail_rev_b` - 3 mm mild-steel compact front service rail for a measured Relay/MIDI/cable pickup.
6. `battery_power_compact_cutoff_tab_rev_b` - compact cutoff switch tab/guard.

## 3D Visualisation

- `battery_power_carrier_mount_rev_a_3d_visualisation.svg` is the static compact fabrication-read view.
- `battery_power_carrier_mount_rev_a_3d_visualisation.html` is the interactive compact fabrication-read view.
- `battery_power_carrier_mount_rev_a_assembled_3d_visualisation.svg` is the static attached compact assembly view.
- `battery_power_carrier_mount_rev_a_assembled_3d_visualisation.html` is the interactive attached compact assembly view showing the single chassis pickup, upright bridge, compact tray, full-height battery, hold-down, folded Relay Rev C tray, MIDI Rev C open plate/subplate, cutoff tab/guard, and cable paths installed together.

## Package Relationship

- The relay hardware uses the known Relay Rev C folded tray (`320 x 220 mm` finished face; `360 x 255 mm` flat pattern). Its bent returns make a shallow tray, so the battery carrier must not duplicate that with a second large tray.
- The MIDI holder hardware uses `midi5_plate_mount_rev_c` (`190 x 150 mm`) and `midi5_holder_subplate_rev_c` (`140 x 85 mm`). This is an open plate/subplate assembly, so mount it on measured tabs/rails.
- The older `electrical_modules_rev_a` package includes bent/flanged aluminium tray/box concepts, but remains reference/fallback only.
- The cutoff pilot hole must be opened only after the actual battery master switch panel-hole size, body depth, terminal-stud spacing, and cable-lug sweep are measured.

## Compact Packaging Hold

- The latest battery-bay photos show no obvious full-size electrical mounting face beside the battery. The previous large sideways carrier is not the active design.
- Before cutting final steel, make cardboard cards for the compact tray (`315 x 265 mm`), Relay Rev C folded tray (`320 x 220 mm` plus return/depth blocks), MIDI Rev C plate (`190 x 150 mm` plus subplate/depth), cutoff tab (`170 x 110 mm`), cable lugs, and battery case.
- Test the front/radiator-side space first. Use inboard/lower/outboard space only after steering, hose, heat, splash, bonnet, and battery-service clearances are proven.
- Reject any placement that enters the steering shaft/box/service sweep, hydraulic line path, alternator service space, bonnet clearance, radiator/fan envelope, or safe battery terminal service area.

## Battery-Cavity Mapping Plan

Use the battery as the fixed exclusion block before placing any relays, MIDI fuses, or cutoff switch. The current package battery block is `275 x 230 x 190 mm`; verify it against the actual installed battery and update the map if the real battery differs.

- Establish datums with the vehicle facing forward: front/radiator side, rear/firewall side, inboard engine/LHD steering side, outboard wing side, and vertical bonnet clearance.
- Put the battery or a full-size battery box in the tray and mark a no-go block around it: battery case, hold-down, terminals, terminal boots, and cable lug bend radius.
- Measure the cavity in slices at tray height, mid-battery height, battery-top height, and bonnet/terminal-service height.
- Record available rectangles to the front, inboard/engine side, outboard/wing side, and below the tray. Do not count space that requires the battery to be removed for fuse or relay service.
- Trial the known templates in cardboard: Relay Rev C folded tray `320 x 220 mm`, MIDI Rev C open plate `190 x 150 mm`, cutoff tab/guard `170 x 110 mm`, plus their real depth and cable lug sweep.
- Treat the front/radiator-side volume as the first candidate because both battery-in and battery-out photos suggest more usable space forward than sideways.
- Treat the inboard/engine-side gap as a cautious candidate only. It must clear LHD steering shaft/box/service motion, hydraulic lines, hoses, alternator service, and heat.
- Treat the lower void as cable support or shielded junction space only unless dry, serviceable, and protected from splash and heat.
- Split the layout by default: cutoff in the most accessible top/front spot, MIDI on the shortest protected high-current path, relays on a separate forward/vertical tray, and P-clips on the stand.

Detailed measurement rows are in `cavity_mapping_plan.csv`.

## Materials

- Stand top tray/deck, compact front rail, and small steel tabs: `3.0 mm` mild steel.
- Single chassis pickup plate and upright bridge: `4.0 mm` mild steel.
- Battery hold-down crossbar: `3.0 mm` mild steel or stainless.
- Cutoff tab/guard: `2.0-3.0 mm` aluminium, plastic, or 3.0 mm mild steel if it becomes a structural steel tab.
- Use stainless or zinc-plated M6/M8/M10 hardware with star washers only where electrical bonding is intended. Otherwise isolate live hardware from the steel stand.

## Chassis Mounting Rules

- Pick up at the one known chassis attachment location. Do not add a second vehicle-side fixing unless the dry-fit proves the single-pickup route cannot carry the assembly safely.
- Do not drill or weld the chassis until the battery, bonnet, fan/belt, radiator, LHD steering-side, alternator-service, and cable-sweep clearances are checked.
- Use crush tubes if any pickup goes through boxed structure.
- The stand must remove from the chassis without cutting wires or removing unrelated radiator support pieces.

## Clearance Holds Before Cutting Final Metal

- Battery installed: length, width, full case height, terminal side, clamp path, and bonnet clearance.
- Compact holder cards: Relay Rev C folded tray, MIDI Rev C open plate/subplate, cutoff tab, and cable-lug depth must fit the measured front/inboard/lower/outboard volume without touching the steering-side service envelope.
- Single chassis pickup: hole pitch, stand-off height, upright bridge height, and access for tools.
- Cutoff switch: panel-hole diameter, body depth, key/knob sweep, terminal stud size, and cable-lug sweep.
- Relay Rev C base: final carrier orientation, standoff height, seal direction, and loom exit direction.
- MIDI Rev C base/subplate: final feed/output orientation and cable bend radius.
- Cable support: P-clip positions every `150-200 mm` and near every direction change.

## Safety Notes

- No exposed positive stud may be able to touch the stand, bonnet, battery clamp, radiator support, or loose tools.
- Put insulating boots/caps over cutoff, MIDI, and relay feed studs.
- Keep the relay loom opening downward or side-down so water cannot pool.
- Route all heavy positive cables away from fan, belts, exhaust heat, steering movement, and sharp panel edges.
