# J40 Battery Stand Power Carrier Pack - Rev D Raised Service-Ladder Update

This package changes the battery-side plan into a compact steel chassis-bolted stand with a raised front/radiator-side service ladder. It supports the battery first, keeps the inboard engine/LHD side clear, and moves the relay box high enough to be serviceable without removing the battery.

## Design Intent

- Mount the battery stand from the one known chassis pickup location using a compact formed saddle over the chassis rail plus an upright bridge.
- Support the battery on a compact `315 x 265 mm` tray around the current `275 x 230 mm` battery datum.
- Put Relay Rev C in the raised front service field: `320 x 220 mm` finished folded tray, `360 x 255 mm` flat pattern, `20 mm` side/bottom returns, and `15 mm` top return. The flat plastic rear guard/underlay sits between the relay box and folded metal tray.
- Put MIDI Rev C on a separated shallow top-front shelf using the known open `190 x 150 mm` aluminium plate plus `140 x 85 mm` insulating subplate.
- Put the 100A breaker/cutoff on the top/front accessible corner on a folded aluminium base/guard: `210 x 150 mm` flat pattern, `170 x 110 mm` finished face, and `20 mm` lips bent upward toward the breaker/terminal side.
- Route the cutoff output as two direct protected branches: one to the relay feed and one to the MIDI common feed. Do not route the relay feed through the MIDI bank.
- Treat the inboard engine/LHD steering side as a keep-clear/service envelope except for protected cable clips and pass-through routing.
- Default to this raised front service-ladder split layout. Do not make a one-piece side carrier unless the filled cavity map proves it is smaller, clear, serviceable, and not in the engine-side envelope.

## Image-Based Chassis Pickup Estimate

The May 14 no-battery bay photo shows the existing battery pocket sitting well above the chassis rail and slightly wing-side/outboard from the visible chassis pickup line. Use these only as first cardboard/wood mock-up targets:

- Target tray support plane: keep the compact tray in the existing battery pocket plane, about `170-190 mm` above the top of the chassis rail. Use `180 mm` as the first mock-up rise from chassis top to tray underside.
- Vertical adjustment allowance: build the upright bridge with slotted/stepped adjustment from `150-210 mm` chassis-top-to-tray-underside so the tray can be lowered if bonnet/terminal clearance is tight or raised if the relay tray/cable exit needs more space.
- Sideways adjustment allowance: set the tray centre about `120 mm` wing-side/outboard from the chassis pickup centreline, with `90-150 mm` usable side adjustment. This keeps the battery in the original pocket rather than moving it engine-side.
- Chassis saddle allowance: mock the chassis fixing as a 4 mm mild-steel saddle with a top cap over the rail and two down-legs, not a flat plate beside the rail. Use a nominal `220 x 230 mm` flat pattern (`70 mm` near leg, measured rail-top cap nominal `90 mm`, `70 mm` far leg) until the actual rail width is measured.
- Battery/electrical package hold: mock up the full `275 x 230 x 190 mm` battery block plus hold-down, then add the raised front service-ladder cards. Do not final-drill the pickup or upright until the battery top, bonnet, fan/radiator, steering/hose, tool access, and cable-lug sweeps all pass.

## Parts In This Package

1. `battery_stand_compact_top_tray_rev_b` - 3 mm mild-steel compact battery tray/deck with clamp and cable-clip zones.
2. `battery_stand_compact_single_chassis_pickup_rev_b` - 4 mm mild-steel formed chassis saddle for the one chassis pickup location.
3. `battery_stand_compact_single_mount_upright_rev_b` - 4 mm mild-steel upright bridge side plate; make a mirrored pair if the mock-up needs side-to-side stiffness.
4. `battery_stand_compact_hold_down_crossbar_rev_b` - compact battery hold-down crossbar template.
5. `battery_power_compact_front_service_rail_rev_b` - 3 mm mild-steel raised `325 x 245 mm` front/radiator-side service ladder for the relay tray, plastic underlay, wire gutter, and separated top-front MIDI/cutoff shelf tabs.
6. `battery_power_compact_cutoff_tab_rev_b` - folded aluminium 100A breaker/cutoff base/guard with upward lips, top-front placement basis.

## 3D Visualisation

- `battery_power_carrier_mount_rev_a_3d_visualisation.svg` is the static compact fabrication-read view.
- `battery_power_carrier_mount_rev_a_3d_visualisation.html` is the interactive compact fabrication-read view.
- `battery_power_carrier_mount_rev_a_assembled_3d_visualisation.svg` is the static attached compact assembly view.
- `battery_power_carrier_mount_rev_a_assembled_3d_visualisation.html` is the interactive attached compact assembly view showing the formed chassis saddle over the rail, upright bridge, compact tray, full-height battery, hold-down, raised serviceable Relay Rev C tray with plastic rear guard/underlay ahead of the folded metal tray, top-front MIDI Rev C shelf, folded top-front cutoff base/guard with upward lips, keep-clear engine/LHD side envelope, and direct cutoff-to-relay / cutoff-to-MIDI cable paths installed together.

## Package Relationship

- The relay hardware uses the known Relay Rev C folded tray (`320 x 220 mm` finished face; `360 x 255 mm` flat pattern) plus the flat plastic rear guard/underlay (`280 x 185 mm`) in front of the folded metal tray. The relay face must remain reachable from the front/top service direction.
- The MIDI holder hardware uses `midi5_plate_mount_rev_c` (`190 x 150 mm`) and `midi5_holder_subplate_rev_c` (`140 x 85 mm`). This is an open plate/subplate assembly, so the current route is a separated shallow top-front shelf on the same raised service ladder.
- The older `electrical_modules_rev_a` package includes bent/flanged aluminium tray/box concepts, but remains reference/fallback only.
- The cutoff folded base/guard gets only a pilot/opening allowance until the actual 100A breaker body size, mounting-hole centres, reset-lever access, terminal-stud spacing, and cable-lug sweep are measured. The lips fold upward to protect the breaker/lug envelope, not downward as hidden stiffeners.

## Compact Packaging Hold

- The latest battery-bay photos show no obvious full-size electrical mounting face beside the battery. The previous large sideways carrier is rejected for the active package.
- Before cutting final steel, make cardboard cards for the compact tray (`315 x 265 mm`), raised front service ladder (`325 x 245 mm`), Relay Rev C folded tray (`320 x 220 mm` plus return/depth blocks), relay plastic rear guard/underlay (`280 x 185 mm`), MIDI Rev C top shelf (`190 x 150 mm` plus subplate/depth), folded cutoff base/guard (`170 x 110 mm` finished face / `210 x 150 mm` flat pattern / `20 mm` upward lips), cable lugs, and battery case.
- Test the front/radiator-side space first, with the relay tray raised into the upper/front service field and the MIDI/cutoff cards separated on the top-front shelf. Use inboard/lower/outboard space only after steering, hose, heat, splash, bonnet, and battery-service clearances are proven.
- Reject any placement that enters the engine/LHD steering shaft/box/service sweep, hydraulic line path, alternator service space, bonnet clearance, radiator/fan envelope, or safe battery terminal service area.

## Battery-Cavity Mapping Plan

Use the battery as the fixed exclusion block before placing any relays, MIDI fuses, or cutoff breaker. The current package battery block is `275 x 230 x 190 mm`; verify it against the actual installed battery and update the map if the real battery differs.

- Establish datums with the vehicle facing forward: front/radiator side, rear/firewall side, inboard engine/LHD steering side, outboard wing side, and vertical bonnet clearance.
- Put the battery or a full-size battery box in the tray and mark a no-go block around it: battery case, hold-down, terminals, terminal boots, and cable lug bend radius.
- Measure the cavity in slices at tray height, mid-battery height, battery-top height, and bonnet/terminal-service height.
- Record available rectangles to the front, inboard/engine side, outboard/wing side, and below the tray. Do not count space that requires the battery to be removed for fuse or relay service.
- Trial the known templates in cardboard in the active order: raised Relay Rev C folded tray `320 x 220 mm`, relay plastic rear guard/underlay `280 x 185 mm` ahead of the metal tray, MIDI Rev C open plate `190 x 150 mm` on the separated shallow top-front shelf, folded cutoff base/guard `170 x 110 mm` finished face / `210 x 150 mm` flat pattern with `20 mm` upward lips at the top/front accessible corner, plus their real depth and cable lug sweep.
- Treat the front/radiator-side volume as the first candidate because both battery-in and battery-out photos suggest more usable space forward than sideways.
- Treat the inboard/engine-side gap as a keep-clear zone by default. It must stay clear of LHD steering shaft/box/service motion, hydraulic lines, hoses, alternator service, engine movement, and heat.
- Treat the lower void as cable support or shielded junction space only unless dry, serviceable, and protected from splash and heat.
- Split the layout by front elevation: relay raised on the front service face, MIDI on a separated top-front shelf, cutoff at the top/front accessible corner, two direct cutoff output branches to relay and MIDI, and P-clips on the stand/ladder rather than the engine-side gap.

Detailed measurement rows are in `cavity_mapping_plan.csv`.

## Materials

- Stand top tray/deck, raised front service ladder, top-front shelf tabs, and small steel tabs: `3.0 mm` mild steel.
- Tray/service-ladder angle-first stock: `25 x 25 x 3 mm` or `30 x 30 x 3 mm` pre-formed `90-degree` mild-steel angle for tray perimeter/upstands, ladder frame rails, shelf rails, and cable/P-clip tabs.
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
- Compact holder cards: raised serviceable Relay Rev C tray, relay plastic rear guard/underlay, MIDI Rev C top-front shelf, folded cutoff top/front base/guard with upward lips, and direct cutoff-to-relay / cutoff-to-MIDI cable-lug depth must fit the measured front/radiator volume without touching the steering-side service envelope.
- Single chassis saddle: rail top width, leg depth, through-bolt pitch, crush-tube need, stand-off height, upright bridge height, side-jog from saddle centreline to tray centreline, and access for tools. Current image-based target is `180 mm` rise with `90-150 mm` wing-side/outboard adjustment.
- 100A breaker/cutoff: body length/width/height, mounting hole centres, reset lever access, terminal stud size/spacing, and cable-lug sweep.
- Relay Rev C base: final raised-front service orientation, plastic-underlay order, standoff height, seal direction, and loom exit direction.
- MIDI Rev C base/subplate: final top-front shelf feed/output orientation, direct cutoff common-feed bend radius, and branch-output bend radius.
- Cable support: P-clip positions every `150-200 mm` and near every direction change.

## Safety Notes

- No exposed positive stud may be able to touch the stand, bonnet, battery clamp, radiator support, or loose tools.
- Put insulating boots/caps over cutoff, MIDI, and relay feed studs.
- Keep the relay loom opening downward or side-down so water cannot pool.
- Route all heavy positive cables away from fan, belts, exhaust heat, steering movement, and sharp panel edges.
