# J40 Battery Stand Power Carrier Pack - Rev F Standard-Battery Access Update

This package changes the battery-side plan into a compact steel chassis-bolted stand with a standard battery envelope, removable hold-down, and widened raised front/radiator-side access ladder. It supports and removes the battery first, keeps the inboard engine/LHD side clear, moves the covered relay box fully outside the battery footprint, places the cutoff/kill switch beside the MIDI shelf instead of after the MIDI outputs, rotates the relay box 90 degrees so heavy power in/out exits from the top and control cables exit toward the front/radiator side, and reserves enough room for the battery-to-cutoff feed, cutoff-switched relay/MIDI feeds, one MIDI common feed, and five heavy MIDI output cables.

## Design Intent

- Mount the battery stand from the one known chassis pickup location using a compact formed saddle over the chassis rail plus an upright bridge.
- Support the battery on a compact `340 x 265 mm` tray around a standard N70/27-class envelope up to `318 x 180 x 230 mm`.
- Retain the battery with a removable top crossbar and J-rods/vertical rods outside the terminal path. The battery must lift vertically out once the hold-down is removed, without removing the relay box or MIDI shelf.
- Put Relay Rev C on the outboard/access edge of the raised front ladder, rotated 90 degrees from the previous view: `220 x 320 mm` rotated finished face using the same `320 x 220 mm` tray basis, with the flat plastic rear guard/underlay between the relay box and folded metal tray.
- Reserve relay wire exits with explicit visual cluster sizes and offsets relative to the rotated relay-box centre: top power input `54 x 46 x 42 mm` at `X-42 / Y+164 / Z-52`, top power output `54 x 46 x 42 mm` at `X+42 / Y+164 / Z-52`, front-facing control cable cluster `170 x 34 x 24 mm` at `X-18 / Y-120 / Z-112`, and a top heavy-cable service-loop volume.
- Put MIDI Rev C on a separated shallow top-front shelf using the known open `190 x 150 mm` aluminium plate plus `140 x 85 mm` insulating subplate. Its leading edge starts at the battery leading-edge datum; keep one common feed entering one side and five heavy protected output cables leaving the opposite side through a seated comb/gland strip tied back to the shelf.
- Provide one enlarged double-wire MIDI output access hole for the output that leaves with two wires. The output guide backplate, comb, saddles, and support tabs are modelled as attached pieces, not floating cable guides.
- Put the 100A breaker/cutoff on a side-by-side tray beside the MIDI shelf, not behind the MIDI output side, using a folded aluminium base/guard: `210 x 150 mm` flat pattern, `170 x 110 mm` finished face, and `20 mm` lips bent upward toward the breaker/terminal side.
- Route the battery positive into the side-mounted cutoff first. The cutoff output then splits into two protected branches: one to the rotated relay top power input and one to the MIDI common feed. Do not route the relay feed through the MIDI bank.
- Treat the inboard engine/LHD steering side as a keep-clear/service envelope except for protected cable clips and pass-through routing.
- Default to this widened raised front access-ladder split layout. Do not make a one-piece side carrier unless the filled cavity map proves it is smaller, clear, serviceable, and not in the engine-side envelope.

## Image-Based Chassis Pickup Estimate

The May 14 no-battery bay photo shows the existing battery pocket sitting well above the chassis rail and slightly wing-side/outboard from the visible chassis pickup line. Use these only as first cardboard/wood mock-up targets:

- Target tray support plane: keep the compact tray in the existing battery pocket plane, about `170-190 mm` above the top of the chassis rail. Use `180 mm` as the first mock-up rise from chassis top to tray underside.
- Vertical adjustment allowance: build the upright bridge with slotted/stepped adjustment from `150-210 mm` chassis-top-to-tray-underside so the tray can be lowered if bonnet/terminal clearance is tight or raised if the relay tray/cable exit needs more space.
- Sideways adjustment allowance: set the tray centre about `120 mm` wing-side/outboard from the chassis pickup centreline, with `90-150 mm` usable side adjustment. This keeps the battery in the original pocket rather than moving it engine-side.
- Chassis saddle allowance: mock the chassis fixing as a 4 mm mild-steel saddle with a top cap over the rail and two down-legs, not a flat plate beside the rail. Use a nominal `220 x 230 mm` flat pattern (`70 mm` near leg, measured rail-top cap nominal `90 mm`, `70 mm` far leg) until the actual rail width is measured.
- Battery/electrical package hold: mock up the full `318 x 180 x 230 mm` standard battery envelope plus removable hold-down, then add the widened front access-ladder cards. Do not final-drill the pickup or upright until the battery lift-out path, battery top, bonnet, fan/radiator, steering/hose, tool access, relay cover removal, rotated relay top/front cable exits, battery-to-cutoff sweep, cutoff-switched relay/MIDI cable sweeps, and MIDI five-output cable fanout all pass.

## Parts In This Package

1. `battery_stand_compact_top_tray_rev_b` - 3 mm mild-steel compact battery tray/deck with clamp and cable-clip zones.
2. `battery_stand_compact_single_chassis_pickup_rev_b` - 4 mm mild-steel formed chassis saddle for the one chassis pickup location.
3. `battery_stand_compact_single_mount_upright_rev_b` - 4 mm mild-steel upright bridge side plate; make a mirrored pair if the mock-up needs side-to-side stiffness.
4. `battery_stand_compact_hold_down_crossbar_rev_b` - compact battery hold-down crossbar template.
5. `battery_power_compact_front_service_rail_rev_b` - 3 mm mild-steel widened `660 x 310 mm` front/radiator-side access ladder for the outboard rotated relay tray, plastic underlay, relay top power in/out and front control-cable clearances, 80 mm wire gutter, seated MIDI output comb/backplate, enlarged double-wire MIDI access hole, and side-by-side MIDI/cutoff shelf tabs.
6. `battery_power_compact_cutoff_tab_rev_b` - folded aluminium 100A breaker/cutoff base/guard with upward lips for side-by-side placement beside the MIDI shelf.

## 3D Visualisation

- `battery_power_carrier_mount_rev_a_3d_visualisation.svg` is the static compact fabrication-read view.
- `battery_power_carrier_mount_rev_a_3d_visualisation.html` is the interactive compact fabrication-read view.
- `battery_power_carrier_mount_rev_a_assembled_3d_visualisation.svg` is the static attached compact assembly view.
- `battery_power_carrier_mount_rev_a_assembled_3d_visualisation.html` is the interactive attached compact assembly view showing the formed chassis saddle over the rail, upright bridge, `340 x 265 mm` tray, standard battery envelope, removable hold-down, vertical battery lift-out clearance, outboard-access covered Relay Rev C tray rotated with top power in/out plus front control-cable exits and plastic rear guard/underlay ahead of the folded metal tray, top-front MIDI Rev C shelf with seated output comb/backplate and enlarged double-wire access hole, side-by-side cutoff/kill-switch base/guard with upward lips, keep-clear engine/LHD side envelope, and battery-to-cutoff / cutoff-to-relay / cutoff-to-MIDI cable paths installed together.

## Package Relationship

- The relay hardware uses the known Relay Rev C folded tray basis (`320 x 220 mm` face rotated to `220 x 320 mm` in this carrier view) plus the flat plastic rear guard/underlay (`280 x 185 mm`, rotated with the box) in front of the folded metal tray. The latest layout rotates the covered black relay enclosure so the heavy power input/output leave from the top and the control cables face the front/radiator-side service direction.
- The MIDI holder hardware uses `midi5_plate_mount_rev_c` (`190 x 150 mm`) and `midi5_holder_subplate_rev_c` (`140 x 85 mm`). This is an open plate/subplate assembly with one common feed side and five heavy output cables on the opposite side, so the current route is a separated shallow top-front shelf whose leading edge aligns to the battery leading-edge datum, with a seated output comb/backplate and an 80 mm cable fanout/gutter on the same raised access ladder. One output is marked with an enlarged pass-through for two wires.
- The older `electrical_modules_rev_a` package includes bent/flanged aluminium tray/box concepts, but remains reference/fallback only.
- The cutoff folded base/guard gets only a pilot/opening allowance until the actual 100A breaker body size, mounting-hole centres, reset-lever access, terminal-stud spacing, and cable-lug sweep are measured. The lips fold upward to protect the breaker/lug envelope, not downward as hidden stiffeners.

## Compact Packaging Hold

- The latest battery-bay photos show no obvious full-size electrical mounting face beside the battery. The previous large sideways carrier is rejected for the active package.
- Before cutting final steel, make cardboard cards for the compact tray (`340 x 265 mm`), standard battery envelope (`318 x 180 x 230 mm`), widened front access ladder (`660 x 310 mm`), Relay Rev C folded tray rotated to `220 x 320 mm` plus return/depth blocks, covered relay box face/removal space, relay plastic rear guard/underlay rotated with the box, relay top power in/out and front control-cable cards with the sizes above, MIDI Rev C top shelf (`190 x 150 mm` plus subplate/depth), attached side-gutter MIDI output comb/backplate/gland strip, enlarged double-wire MIDI output access hole, folded cutoff base/guard (`170 x 110 mm` finished face / `210 x 150 mm` flat pattern / `20 mm` upward lips) beside the MIDI shelf, one MIDI common feed lug, five MIDI output cable lugs, and battery case.
- Test the front/radiator-side space first, with the relay tray shifted to the outboard/access edge, the MIDI shelf started from the battery leading-edge datum, and the cutoff/kill-switch card placed beside the MIDI shelf instead of after its outputs. Use inboard/lower/outboard space only after steering, hose, heat, splash, bonnet, and battery-service clearances are proven.
- Reject any placement that enters the engine/LHD steering shaft/box/service sweep, hydraulic line path, alternator service space, bonnet clearance, radiator/fan envelope, or safe battery terminal service area.

## Battery-Cavity Mapping Plan

Use the battery as the fixed exclusion block before placing any relays, MIDI fuses, or cutoff breaker. The current package uses a standard N70/27-class envelope up to `318 x 180 x 230 mm`; verify it against the actual installed battery and update the map if the real battery differs.

- Establish datums with the vehicle facing forward: front/radiator side, rear/firewall side, inboard engine/LHD steering side, outboard wing side, and vertical bonnet clearance.
- Put the battery or a full-size battery box in the tray and mark a no-go block around it: battery case, hold-down, terminals, terminal boots, and cable lug bend radius.
- Measure the cavity in slices at tray height, mid-battery height, battery-top height, and bonnet/terminal-service height.
- Record available rectangles to the front, inboard/engine side, outboard/wing side, and below the tray. Do not count space that requires the battery to be removed for fuse or relay service.
- Trial the known templates in cardboard in the active order: outboard/access Relay Rev C folded tray rotated to `220 x 320 mm`, covered relay box face/removal clearance, relay plastic rear guard/underlay rotated with the box, relay top power in/out cards and front control-cable card with relative offsets/sizes, MIDI Rev C open plate `190 x 150 mm` on the separated shallow top-front shelf started from the battery leading-edge datum, attached MIDI output side-gutter comb/gland strip with one enlarged double-wire access hole, folded cutoff base/guard `170 x 110 mm` finished face / `210 x 150 mm` flat pattern with `20 mm` upward lips placed beside the MIDI shelf, battery-to-cutoff input lug, cutoff output splitter, one MIDI common feed lug, five MIDI output lugs, plus their real depth and cable lug sweep.
- Treat the front/radiator-side volume as the first candidate because both battery-in and battery-out photos suggest more usable space forward than sideways.
- Treat the inboard/engine-side gap as a keep-clear zone by default. It must stay clear of LHD steering shaft/box/service motion, hydraulic lines, hoses, alternator service, engine movement, and heat.
- Treat the lower void as cable support or shielded junction space only unless dry, serviceable, and protected from splash and heat.
- Split the layout by front elevation: rotated relay outboard on the front access edge with top power and front control exits, MIDI on a separated top-front shelf started from the battery leading-edge datum, cutoff/kill switch beside the MIDI shelf, battery positive into cutoff first, cutoff output split into relay and MIDI feeds, five MIDI branch outputs guided sideways through the attached comb into a supported side gutter, one enlarged double-wire output pass-through, and P-clips on the stand/ladder rather than the engine-side gap.

Detailed measurement rows are in `cavity_mapping_plan.csv`.

## Materials

- Stand top tray/deck, widened raised front access ladder, top-front shelf tabs, and small steel tabs: `3.0 mm` mild steel.
- Tray/access-ladder angle-first stock: `25 x 25 x 3 mm` or `30 x 30 x 3 mm` pre-formed `90-degree` mild-steel angle for tray perimeter/upstands, ladder frame rails, shelf rails, and cable/P-clip tabs.
- Single chassis saddle and upright bridge flat interfaces: `4.0 mm` mild steel. Saddle flat-pattern allowance is nominal `220 x 230 mm` before rail-width measurement and bend allowance correction.
- Upright bridge angle-first stock: `40 x 40 x 4 mm` pre-formed `90-degree` mild-steel angle may replace straight bridge members if dry-fit keeps bolt access, service clearance, and battery/electrical layout clear.
- Battery hold-down crossbar: `3.0 mm` mild steel or stainless.
- Cutoff base/guard: `3.0 mm` 5052-H32 aluminium folded to a `170 x 110 mm` finished face with `20 mm` upstand lips around the 100A breaker/terminal side; use steel only if dry-fit proves the cutoff base must become a structural tab.
- Do not delete flat sheet/plate stock just because angle stock is available; the battery deck, chassis saddle, and electrical mounting faces still need controlled flat geometry.
- Use stainless or zinc-plated M6/M8/M10 hardware with star washers only where electrical bonding is intended. Otherwise isolate live hardware from the steel stand.

## Chassis Mounting Rules

- Pick up at the one known chassis attachment location with a formed saddle over the top of the chassis rail. The saddle must have legs down both rail sides and through-bolts through both legs/chassis; do not treat a flat side plate as the final fixing.
- Confirm rail top width, side height, bolt access, and crush-tube need before final saddle cutting. The nominal flat pattern is `70 mm` leg + measured rail-top cap + `70 mm` leg, shown as `220 x 230 mm` until measured.
- Do not add a second vehicle-side fixing unless the dry-fit proves the single-saddle route cannot carry the assembly safely.
- Do not drill or weld the chassis until the battery, bonnet, fan/belt, radiator, LHD steering-side, alternator-service, and cable-sweep clearances are checked.
- Use crush tubes if any pickup goes through boxed structure.
- The stand must remove from the chassis without cutting wires or removing unrelated radiator support pieces.

## Clearance Holds Before Cutting Final Metal

- Battery installed: length, width, full case height, terminal side, clamp path, and bonnet clearance.
- Compact holder cards: outboard-access covered Relay Rev C tray rotated to put power in/out at the top and controls toward the front, relay plastic rear guard/underlay, top relay power in/out cards, front relay control-cable card, MIDI Rev C top-front shelf, folded cutoff/kill-switch base/guard with upward lips beside the MIDI shelf, battery-leading-edge datum line for the MIDI start, battery-to-cutoff and cutoff-to-relay/MIDI cable-lug depth, seated MIDI output comb/backplate, and five MIDI output cable bends must fit the measured front/radiator volume without touching the steering-side service envelope.
- Single chassis saddle: rail top width, leg depth, through-bolt pitch, crush-tube need, stand-off height, upright bridge height, side-jog from saddle centreline to tray centreline, and access for tools. Current image-based target is `180 mm` rise with `90-150 mm` wing-side/outboard adjustment.
- 100A breaker/cutoff: body length/width/height, mounting hole centres, reset lever access, terminal stud size/spacing, and cable-lug sweep.
- Relay Rev C base: final outboard/front service orientation, cover removal space, plastic-underlay order, standoff height, seal direction, and loom exit direction.
- MIDI Rev C base/subplate: final top-front shelf feed/output orientation, cutoff-switched common-feed bend radius, attached side-gutter output guide, and all five branch-output bend radii.
- Cable support: P-clip positions every `150-200 mm` and near every direction change.

## Safety Notes

- No exposed positive stud may be able to touch the stand, bonnet, battery clamp, radiator support, or loose tools.
- Put insulating boots/caps over cutoff, MIDI, and relay feed studs.
- Keep the relay loom opening downward or side-down so water cannot pool.
- Route all heavy positive cables away from fan, belts, exhaust heat, steering movement, and sharp panel edges.
