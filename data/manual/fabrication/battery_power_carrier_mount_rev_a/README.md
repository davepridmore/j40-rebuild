# J40 Battery Stand Power Carrier Pack - Rev F Standard-Battery Access Update

This package defines the battery-side power carrier as a compact steel stand that bolts to a formed chassis saddle, then reaches toward the body/wing side through configurable slotted offset bars. The tray and electrical access ladder can be set around the current `190 mm` outboard target while keeping a `160-230 mm` offset adjustment range for dry-fit.

## Design Intent

- Mount the stand from the known chassis pickup with a formed saddle over the chassis rail, upright bridge plates, and body-side adjustable offset bars rather than a fixed one-piece sideways carrier.
- Support a standard N70/27-class battery envelope up to `318 x 180 x 230 mm` on the `340 x 265 mm` tray with removable hold-down and vertical lift-out clearance.
- Use the simplified Relay Rev D fabrication on the outboard/access edge: the existing covered relay box sits on a flat `360 x 245 x 3 mm` aluminium base and exact `300 x 197 mm` insulating sheet.
- Use the MIDI Rev D hinged aluminium enclosure on the top/front shelf: `210 x 165 x 65 mm` enclosure floor, `230 x 185 mm` lid, `140 x 85 mm` insulating subplate, fuse 4 input grommet, five output grommets, and an enlarged far-side output grommet for two power cables.
- Keep the 100A breaker/cutoff beside the MIDI enclosure, with the far-side cutoff stud fed from the battery and the near-side switched stud splitting to relay and MIDI.
- Keep the inboard engine/LHD steering side as a service and clearance envelope except for protected cable clips or pass-through routing.

## Chassis Offset

- Start the tray support plane about `180 mm` above the chassis-rail top, with vertical adjustment from `150-210 mm` before final steel is drilled.
- Start the tray/electrical ladder centre about `190 mm` wing-side/outboard from the chassis pickup centreline.
- Use the `battery_stand_adjustable_offset_bar_rev_b` slotted bars to tune the body-side offset from `160-230 mm`. Make two mirrored bars unless one central bar plus gussets proves stiffer in dry-fit.
- Lock the selected offset only after the battery, bonnet, fan/radiator, steering/hose, relay cover, MIDI lid, cutoff lever, and cable-sweep checks pass.

## Parts In This Package

1. `battery_stand_compact_top_tray_rev_b` - 3 mm mild-steel compact battery tray/deck with clamp and cable-clip zones.
2. `battery_stand_compact_single_chassis_pickup_rev_b` - 4 mm mild-steel formed chassis saddle for the known chassis pickup.
3. `battery_stand_adjustable_offset_bar_rev_b` - 4 mm mild-steel slotted offset bar from the chassis saddle/upright bridge toward the body/wing-side battery pocket.
4. `battery_stand_compact_single_mount_upright_rev_b` - 4 mm mild-steel upright bridge side plate; make a mirrored pair if the mock-up needs side-to-side stiffness.
5. `battery_stand_compact_hold_down_crossbar_rev_b` - compact battery hold-down crossbar template.
6. `battery_power_compact_front_service_rail_rev_b` - 3 mm mild-steel raised access ladder for Relay Rev D, MIDI Rev D, cutoff, cable gutter, and P-clip pickups.
7. `battery_power_compact_cutoff_tab_rev_b` - folded aluminium 100A breaker/cutoff base/guard with upward lips for side-by-side placement beside the MIDI enclosure.

## Package Relationship

- Relay hardware comes from `relay_mount_rev_d`: flat aluminium base, exact insulating sheet, and transferred relay-box mounting holes from the real covered enclosure.
- MIDI hardware comes from `midi5_enclosure_rev_d`: hinged aluminium enclosure, fuse 4 input grommet, five output-side grommets, and a larger far-side output hole for the double power-cable exit.
- The older Relay Rev C folded carrier and MIDI Rev C open plate are superseded for this battery power carrier and kept only as fallback/reference history.
- The older `electrical_modules_rev_a` package remains reference/fallback only.

## Mock-Up Hold

- Make cardboard cards for the battery envelope, `340 x 265 mm` tray, formed saddle, adjustable offset bars at `160 / 190 / 230 mm`, Relay Rev D base plus relay cover/removal volume, MIDI Rev D hinged enclosure with lid swing, cutoff base/guard, and cable-lug sweep blocks.
- Test the whole tray/access-ladder assembly shifted toward the wing-side edge cavity from the chassis saddle. Reject any placement that enters the engine/LHD steering shaft/box/service sweep, hydraulic line path, alternator service space, bonnet clearance, radiator/fan envelope, or safe battery terminal service area.
- Do not final-drill the chassis saddle, offset bars, relay base, MIDI enclosure, or cutoff tab until the filled cavity map and installed dry-fit photos prove service access with the battery installed.

## 3D Visualisation

- `battery_power_carrier_mount_rev_a_3d_visualisation.svg` and `.html` show the fabrication-read layout.
- `battery_power_carrier_mount_rev_a_assembled_3d_visualisation.svg` and `.html` show the attached assembly with the formed chassis saddle, adjustable offset bars, compact tray, Relay Rev D, MIDI Rev D, cutoff, and cable paths.

## Materials

- Stand tray/deck, raised front access ladder, shelf tabs, and small steel tabs: `3.0 mm` mild steel.
- Tray/access-ladder angle-first stock: `25 x 25 x 3 mm` or `30 x 30 x 3 mm` pre-formed mild-steel angle where it improves stiffness without blocking service access.
- Chassis saddle, upright bridge, and offset bars: `4.0 mm` mild steel.
- Battery hold-down crossbar: `3.0 mm` mild steel or stainless.
- Relay Rev D base: `3.0 mm` 5052-H32 aluminium with insulating sheet between relay box and base.
- MIDI Rev D enclosure and cutoff base/guard: `3.0 mm` 5052-H32 aluminium.

## Safety Notes

- No exposed positive stud may be able to touch the stand, bonnet, battery clamp, radiator support, or loose tools.
- Put insulating boots/caps over cutoff, MIDI, and relay feed studs.
- Keep the relay loom opening downward or side-down so water cannot pool.
- Route all heavy positive cables away from fan, belts, exhaust heat, steering movement, and sharp panel edges, with P-clips every `150-200 mm` and near direction changes.
