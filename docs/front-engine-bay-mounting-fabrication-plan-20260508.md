# Front Engine-Bay Mounting Fabrication Plan - 2026-05-08

This plan splits the vague "missing bracket" concern into concrete front engine-bay fabrication jobs: radiator two-side retention, battery tray support, and a chassis-mounted integrated power carrier for the known Relay Rev C base, MIDI Rev C base/subplate, and battery master cutoff.

Linked bracket register: [chassis-bracket-analysis-register-20260508.md](chassis-bracket-analysis-register-20260508.md).

## Current Evidence

| Area | Evidence | Read |
| --- | --- | --- |
| Radiator/front support | `20260422_004423_gp_B1N5ThVw`, `20260422_004429_gp_4emWbTrA`, `20260422_004436_gp_yjCPMWTg`, `20260430_215957_gp_2iBbUagw`, `20260430_220004_gp_C9oYiYmA` | Direct evidence. The radiator, front support upright, lower support area, previous wire support, and fan/radiator clearance are visible enough to define the repair function. |
| May 12 radiator/upright context | `20260512_100000_user_front_support_radiator_pickups_context` | Direct structure-scout evidence. The visible upright/top hole, lower/front support hole field, radiator plane, and fan/pulley clearance are enough to start a removable side-strap/upright template. |
| Battery location / stand context | `20260317_235232_gp_3Ojs4Rag`, `20260317_235150`, `20260317_235201`, `20260423_232309_gp_rrFiL8og`, `20260512_100100_user_battery_side_tray_structure_context` | Partial structure evidence. The May 12 image improves the battery-side load-path and clearance read, but tray feet, underside supports, battery dimensions, and exact pickup points are still not clear enough to release a cut pattern. |
| Relay / MIDI fuse / cutoff hardware | `20260411_143125`, `20260411_143135`, `20260420_221819_gp_YV69fbvA`, `data/manual/fabrication/battery_power_carrier_mount_rev_a/README.md`, `data/manual/fabrication/midi5_plate_mount_rev_c/README.md` | Direct hardware evidence. Battery Power Carrier Rev A now defines the chassis-mounted integrated backplane, the formed chassis saddle/upright bridge, folded aluminium cutoff base/guard with upward lips, known Relay Rev C base field, known MIDI Rev C base field, and cable support holes. |
| Cutoff / isolation hardware | `20260420_221819_gp_YV69fbvA`, electrical planning rows | Hardware/context evidence. Treat the battery-side item here as a battery master cutoff/isolator or breaker placement task, separate from the hidden diesel fuel-stop switch unless final wiring deliberately combines functions. |

## May 12 Provisional Structure Read

- Radiator: copy the simple left-side 90 degree top-post idea, but retain it with a bolt-through saddle rather than welding it to the chassis. Use one 4 mm mild-steel right-angle post with lower legs over both sides of the chassis/front-support section, a through-bolt across the legs and chassis, and a top return for the radiator screw.
- Battery stand: use a steel stand with one formed saddle over the chassis rail, an upright bridge, and a top tray/deck that supports the battery directly from real structure. The battery mass should not load the radiator support strap or a flat unsupported inner-wing skin.
- Power carrier: integrate the known Relay Rev C base, MIDI Rev C base/subplate, and folded aluminium cutoff base/guard into a compact front/radiator-side cassette on the battery stand, mounted from the one chassis pickup location. The cutoff lips bend upward around the switch/terminal side, not downward as hidden stiffeners. The sideways `520 x 340 mm` backplane is rejected for the active route because it fights the engine/LHD-side clearance. Heavy positive cables need insulated clips near direction changes and roughly every `150-200 mm`.
- Clearance holds: keep added structure clear of fan/pulley movement, LHD steering shaft path, alternator access, exhaust/front pipe heat, hose movement, bonnet closure, and battery terminal service space.

## Fabrication Jobs

### RAD-RET-001 - Radiator Two-Side Retention

Preferred outcome: a serviceable two-side radiator retention set that replaces the wire-held/one-side condition without moving the radiator into the fan, belt, hose, or bonnet-close envelope.

Current package: [front_radiator_two_side_retention_rev_a](../data/manual/fabrication/front_radiator_two_side_retention_rev_a/README.md)

First-pass construction:

- Use one `4.0 mm` mild-steel formed-angle strip: `48 mm` measured main face, `410 mm` upright/post height, and about `618 mm` developed main-face length across the top screw return, upright post, chassis bridge, and outer chassis leg. Prefer pre-formed `90-degree` angle/L-section stock if one leg is close to `48-50 mm`; otherwise form the return from flat stock.
- Straddle the chassis/front-support section with the two lower legs and retain the bracket with a through-bolt through both legs and the chassis.
- Treat the measured left chassis-attached bracket and the supplied photo as first template datums, subject to ruler confirmation and metal-condition check.
- Use rubber washers, bushes, or grommet-style isolation at the top screw if required. Do not hard-clamp the radiator tank/core.
- Use crush-tube/spacer practice if bolting through boxed chassis/front-support metal.
- Do not weld the bracket to the chassis or add a separate rubber-pad fabrication part unless dry-fit proves the bolted saddle route is wrong.
- Preserve the current radiator plane unless dry-fit proves it must move; fan clearance is a release dimension.

Release checks:

- Both sides of the radiator restrained in fore/aft and lateral movement.
- No metal-to-metal rubbing on radiator tank, fins, or side rails.
- Lower and upper hose paths stay relaxed.
- Fan and shroud clearance confirmed after tightening.
- Top screw and through-bolt remain serviceable and the saddle bracket does not block radiator removal.

### BAT-TRAY-001 - Battery Tray Support Upgrade

Preferred outcome: a tray and clamp system that supports the full battery mass from real structure, not a single weak side tab or thin unsupported sheet.

First-pass construction:

- Build or reinforce a tray base from `3.0 mm` mild steel with `20-25 mm` angle or formed upstands on at least two edges.
- Use a separate tray/stand load path: tray perimeter plus lower/inner support pickups with gussets. Do not hang the battery mass from the radiator support strap or a flat inner-wing skin alone.
- Add drain holes and leave access for cleaning/neutralising acid residue.
- Use a top clamp, crossbar, or J-bolt arrangement that cannot touch terminals.
- Tie the tray into at least two structural pickup points: inner wing/support bracket and lower brace/leg where available.
- Avoid relying only on the flat inner wing skin.
- Keep the tray stand and support legs clear of the LHD steering shaft zone, alternator swing/service access, exhaust/front pipe heat, hoses, and cable movement visible in the May 12 engine-side view.
- Isolate the battery base with an acid-resistant rubber or plastic mat after paint.

Release checks:

- Battery dimensions, terminal orientation, and bonnet clearance measured.
- Tray cannot rock or peel under battery mass and vibration.
- Terminals cannot short against clamp, bonnet, MIDI plate, cutoff body, or tools during service.
- Tray coating plan is explicit: zinc-rich epoxy/primer, top protection, then removable liner.

### PWR-CARRIER-001 - Chassis-Mounted Battery Stand / Relay / Fuse / Cutoff Carrier

Preferred outcome: a removable steel chassis-mounted stand that supports a full-height battery and carries the known Relay Rev C carrier base, MIDI Rev C fuse-holder base/subplate, and battery master cutoff/isolator base as one serviceable assembly.

Current package: [battery_power_carrier_mount_rev_a](../data/manual/fabrication/battery_power_carrier_mount_rev_a/README.md)

Core compact access-ladder parts:

- Battery stand top tray/deck: `340 x 265 x 3.0 mm` mild steel around a standard N70/27-class `318 x 180 x 230 mm` battery envelope.
- Front/radiator-side widened access-ladder spine: `660 x 310 x 3.0 mm` mild steel.
- Tray/access-ladder angle stock: `25 x 25 x 3 mm` or `30 x 30 x 3 mm` pre-formed `90-degree` mild-steel angle, about `3 m` total, for tray perimeter/upstands, access-ladder frame rails, shelf rails, and cable/P-clip tabs.
- Single chassis saddle: nominal `220 x 230 x 4.0 mm` mild-steel flat pattern, formed to a `70 mm` near leg, measured chassis-top cap width, and `70 mm` far leg. Final cap width, bend allowance, and through-bolt pitch come from the one chassis location.
- Upright bridge stock: keep `110 x 220 x 4.0 mm` mild-steel flat side plates as the fallback/flat-interface route, but prefer `40 x 40 x 4 mm` pre-formed `90-degree` mild-steel angle for straight stand bridge members if dry-fit keeps bolt access clear.
- Radiator post stock: prefer `50 x 50 x 4 mm` pre-formed `90-degree` mild-steel angle, `1 m`, if one leg matches the measured `48-50 mm` radiator-post face.
- Battery hold-down crossbar: `340 x 38 x 3.0 mm` mild steel or stainless, slot after measuring the battery; it must be removable so the battery can lift out vertically.
- Cutoff folded aluminium base/guard: `210 x 150 mm` flat pattern, `170 x 110 mm` finished face, `20 mm` lips bent upward toward the switch/terminal side; open final switch hole only after the real switch is measured.
- Chassis pickup geometry estimate from the May 14 no-battery photo: keep the tray in the existing battery pocket plane, start with `180 mm` chassis-top-to-tray-underside rise, build `150-210 mm` vertical adjustment into the upright bridge, and allow `90-150 mm` wing-side/outboard side-jog from the chassis pickup centreline to the tray centreline. First mock-up target is `120 mm` outboard jog.

Layout:

- Battery field carries the battery and removable hold-down crossbar on the same stand, with low stops that retain the case without blocking lift-out.
- Relay field carries the existing Relay Rev C carrier base outside the battery footprint on the outboard/access edge of the front/radiator-side service face: `320 x 220 mm` finished face, `360 x 255 mm` flat pattern, with the `280 x 185 mm` flat plastic rear guard/underlay placed before the folded metal tray, the covered relay box facing a removable-cover service path, left-hand power in/out exits, and top control-cable relief left clear.
- MIDI field carries the existing `midi5_plate_mount_rev_c` fuse plate (`190 x 150 mm`) and `midi5_holder_subplate_rev_c` (`140 x 85 mm`) on a separated shallow top-front shelf started from the battery leading-edge datum, with one direct battery common-feed side, a seated output comb/backplate/gland strip tied into a side gutter, one enlarged double-wire output access hole, and five heavy output cables from the opposite side.
- Cutoff field carries the folded master cutoff/kill-switch base/guard beside the MIDI shelf, not after the MIDI outputs. The pilot hole is not the final switch hole; open it only after measuring the switch body, panel-hole requirement, key/knob sweep, terminal studs, cable lug sweep, and whether the upward lips need local relief/drain notches.
- The formed chassis saddle drops over the known chassis pickup location from the top, with legs down both rail sides and through-bolts through both legs/chassis. The stand must remain removable for service.
- Use angle stock for rails and bridge members only where it simplifies the build; keep flat plate/sheet for the battery deck, chassis saddle, and electrical mounting faces.
- The inboard engine/LHD steering side is a keep-clear/service envelope by default; use it only for protected cable clips/pass-throughs after steering, hose, alternator, heat, and tool sweeps are proven.

Electrical route:

- Battery positive -> two direct protected branches: one to the MIDI common feed and one to the covered relay left-hand power input. Keep the cutoff/kill switch side-mounted beside the MIDI shelf until its final circuit role is confirmed.
- Relay feed and MIDI feed must have insulating boots or covers over live studs.
- Heavy positive cables use insulated P-clips/saddle clamps near every direction change and roughly every `150-200 mm`.
- Use grommets/bushes through any sheet metal pass-throughs.
- Keep fuse, relay, and cutoff hardware away from battery acid/vent splash, water pooling, fan/belt movement, exhaust heat, steering movement, and sharp panel edges.

Release checks:

- Stand/tray cardboard mock-up with standard `318 x 180 x 230 mm` battery envelope, removable hold-down, battery lift-out path, known Relay Rev C base outside the battery footprint on the outboard/front access edge, plastic guard/underlay before the folded metal tray, relay left-side power in/out exits, relay top control-cable exit, MIDI Rev C holder bank on its separated top-front shelf with seated output comb/backplate and enlarged double-wire output hole, folded cutoff/kill-switch base/guard beside the MIDI shelf, direct battery-to-relay and battery-to-MIDI cable branches, five MIDI output cables, and cable lugs clears the bonnet, radiator, fan/belt, LHD steering shaft/box/service path, alternator service sweep, and cable bend radius.
- Sideways `520 x 340 mm` backplane is rejected. Reopen side/lower placement only if the widened access-ladder mock-up fails and the measured alternative is smaller, serviceable, and clear of the engine/LHD side envelope.
- Battery and electrical load path is taken by the one formed chassis saddle and upright bridge, not tray skin, radiator strap, or unsupported inner wing.
- The bridge must be adjustable in height and side-jog during mock-up. If the `180 mm` rise or `120 mm` outboard jog moves the battery out of the original pocket, blocks bonnet/terminal clearance, or enters steering/hose service space, reset from the measured battery pocket rather than forcing the estimate.
- Cutoff body depth, knob/key clearance, and cable lug sweep are measured.
- Main cable bend radius is proven without loading cutoff, relay, or fuse studs.
- No exposed positive terminal can contact the carrier, body, bonnet, battery clamp, radiator support, or tools.
- Stand can be removed from chassis/front-support pickup points for service without disturbing radiator support pieces.

Battery-cavity mapping method:

- Use the installed battery as the fixed exclusion block before placing electrical hardware. Current working block in the package is a standard `318 x 180 x 230 mm` envelope; verify the actual battery dimensions and terminal height before relying on the map.
- Map front/radiator-side, inboard engine/LHD-steering-side, lower-under-tray, outboard-wing-side, and bonnet/terminal-height slices with the battery installed.
- Trial cardboard templates as a stack: widened front access-ladder spine `660 x 310 mm`, `340 x 265 mm` battery tray with `318 x 180 x 230 mm` battery envelope, Relay Rev C outboard/front `320 x 220 mm`, relay plastic rear guard/underlay `280 x 185 mm`, left-side relay power in/out cards, top relay control-cable card, MIDI Rev C top-front `190 x 150 mm` with seated output comb/backplate and enlarged double-wire output access hole started from the battery leading-edge datum, folded cutoff/kill-switch base/guard `170 x 110 mm` finished face / `210 x 150 mm` flat pattern / `20 mm` upward lips beside the MIDI shelf, plus depth blocks for direct battery branches, relay cover removal, cable lugs, MIDI five-output fanout, and boots.
- Add chassis-pickup mock-up marks: tray plane at `150`, `180`, and `210 mm` above the chassis rail top; tray centreline side-jog at `90`, `120`, and `150 mm` wing-side/outboard from the chassis pickup centreline; saddle card over both rail sides with `70 mm` leg depth each side until the actual rail height dictates otherwise.
- Prefer front/radiator-side space if it clears fan/radiator/hose/bonnet service. Treat inboard and lower spaces as cautious cable/support candidates only; do not put relay/MIDI/cutoff faces there unless the widened access-ladder route fails by measurement.
- Record the filled plan in `data/manual/fabrication/battery_power_carrier_mount_rev_a/cavity_mapping_plan.csv`.

### PWR-CABLE-001 - Cable And Clip Support

Preferred outcome: cable support points designed at the same time as the carrier, so the heavy battery/MIDI cables are not left hanging after coating.

First-pass construction:

- Add P-clip holes or small bolted tabs to the carrier and nearby support metal.
- Keep cable routes away from fan, belts, exhaust heat, steering movement, and sharp panel edges.
- Use insulated P-clips for heavy positive cables.
- Keep service loops short enough not to rub, but long enough to remove the MIDI plate/cutoff without stressing lugs.

## Scouting Required Before Cutting Metal

Capture these with a ruler or tape measure in frame:

1. Radiator left and right side flanges: top/middle/lower holes, broken tabs, wire-tie path, and current bolt sizes.
2. Front support and lower crossmember holes around the radiator, both sides, including the May 12 visible upright top hole and its base attachment.
3. Minimum fan-to-radiator clearance at the closest point, with the radiator sitting where it currently sits.
4. Battery from top: length, width, height, terminal orientation, clamp position, and bonnet clearance.
5. Battery tray from top and side: existing tray edges, clamp holes, corrosion, cracks, and any current support tabs.
6. Battery tray underside: feet, braces, inner wing attachment, chassis/engine clearance, and possible lower support leg path.
7. Battery stand template: cardboard or flat-bar tray perimeter plus proposed lower/inner pickup points and gusset directions.
8. Proposed relay/fuse/cutoff mock-up: widened access-ladder cards held with battery installed: `660 x 310 mm` service spine, `340 x 265 mm` tray and `318 x 180 x 230 mm` battery envelope, Relay Rev C `320 x 220 mm` outboard/front face outside the battery footprint, `280 x 185 mm` relay plastic rear guard/underlay before the folded metal tray, relay left-side power in/out exits, relay top control-cable exit, MIDI Rev C `190 x 150 mm` top-front shelf with one direct battery common-feed side, seated output comb/backplate, one enlarged double-wire output access hole, and five output cables, folded cutoff/kill-switch base/guard `170 x 110 mm` finished face / `210 x 150 mm` flat pattern / `20 mm` upward lips beside the MIDI shelf, direct battery-to-relay and battery-to-MIDI cable lug sweeps, and the LHD steering-side no-go envelope.
9. Cutoff switch or isolator body: panel-hole size, body depth, terminal stud size, and cable exit directions.
10. Cable exit route from battery positive to relay and MIDI plate, plus MIDI outputs toward the harness.
11. Bonnet closed/near-closed clearance over the battery, tray clamp, MIDI plate, and cutoff.

## Coating Gate

Radiator saddle drilling/through-bolt prep, battery tray support leg, battery carrier pickup, line/harness clip tab, or cable-support tab must be finished before final chassis/front-support primer, seam sealer, Raptor, and cavity wax.

The removable power-carrier backplane, Relay Rev C base, MIDI plate, non-conductive subplate, cutoff switch, and final cable clips can be installed after coating, provided the formed chassis saddle/upright structure is already installed, deburred, primed, and protected.
