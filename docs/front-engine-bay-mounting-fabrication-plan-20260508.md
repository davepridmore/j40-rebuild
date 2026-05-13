# Front Engine-Bay Mounting Fabrication Plan - 2026-05-08

This plan splits the vague "missing bracket" concern into concrete front engine-bay fabrication jobs: radiator two-side retention, battery tray support, and a chassis-mounted integrated power carrier for the known Relay Rev C base, MIDI Rev C base/subplate, and battery master cutoff.

Linked bracket register: [chassis-bracket-analysis-register-20260508.md](chassis-bracket-analysis-register-20260508.md).

## Current Evidence

| Area | Evidence | Read |
| --- | --- | --- |
| Radiator/front support | `20260422_004423_gp_B1N5ThVw`, `20260422_004429_gp_4emWbTrA`, `20260422_004436_gp_yjCPMWTg`, `20260430_215957_gp_2iBbUagw`, `20260430_220004_gp_C9oYiYmA` | Direct evidence. The radiator, front support upright, lower support area, previous wire support, and fan/radiator clearance are visible enough to define the repair function. |
| May 12 radiator/upright context | `20260512_100000_user_front_support_radiator_pickups_context` | Direct structure-scout evidence. The visible upright/top hole, lower/front support hole field, radiator plane, and fan/pulley clearance are enough to start a removable side-strap/upright template. |
| Battery location / stand context | `20260317_235232_gp_3Ojs4Rag`, `20260317_235150`, `20260317_235201`, `20260423_232309_gp_rrFiL8og`, `20260512_100100_user_battery_side_tray_structure_context` | Partial structure evidence. The May 12 image improves the battery-side load-path and clearance read, but tray feet, underside supports, battery dimensions, and exact pickup points are still not clear enough to release a cut pattern. |
| Relay / MIDI fuse / cutoff hardware | `20260411_143125`, `20260411_143135`, `20260420_221819_gp_YV69fbvA`, `data/manual/fabrication/battery_power_carrier_mount_rev_a/README.md`, `data/manual/fabrication/midi5_plate_mount_rev_c/README.md` | Direct hardware evidence. Battery Power Carrier Rev A now defines the chassis-mounted integrated backplane, the one chassis pickup plate/upright bridge, cutoff switch/guard base, known Relay Rev C base field, known MIDI Rev C base field, and cable support holes. |
| Cutoff / isolation hardware | `20260420_221819_gp_YV69fbvA`, electrical planning rows | Hardware/context evidence. Treat the battery-side item here as a battery master cutoff/isolator or breaker placement task, separate from the hidden diesel fuel-stop switch unless final wiring deliberately combines functions. |

## May 12 Provisional Structure Read

- Radiator: copy the simple left-side 90 degree top-post idea, but retain it with a bolt-through saddle rather than welding it to the chassis. Use one 4 mm mild-steel right-angle post with lower legs over both sides of the chassis/front-support section, a through-bolt across the legs and chassis, and a top return for the radiator screw.
- Battery stand: use a steel stand with one chassis-bolted pickup plate, an upright bridge, and a top tray/deck that supports the battery directly from real structure. The battery mass should not load the radiator support strap or a flat unsupported inner-wing skin.
- Power carrier: integrate the known Relay Rev C base, MIDI Rev C base/subplate, and cutoff base/guard into the battery stand/backplane assembly, mounted from the one chassis pickup location. The sideways `520 x 340 mm` backplane is a candidate orientation only until a full-size LHD battery-bay cardboard check proves it fits. Heavy positive cables need insulated clips near direction changes and roughly every `150-200 mm`.
- Clearance holds: keep added structure clear of fan/pulley movement, LHD steering shaft path, alternator access, exhaust/front pipe heat, hose movement, bonnet closure, and battery terminal service space.

## Fabrication Jobs

### RAD-RET-001 - Radiator Two-Side Retention

Preferred outcome: a serviceable two-side radiator retention set that replaces the wire-held/one-side condition without moving the radiator into the fan, belt, hose, or bonnet-close envelope.

Current package: [front_radiator_two_side_retention_rev_a](../data/manual/fabrication/front_radiator_two_side_retention_rev_a/README.md)

First-pass construction:

- Use one `4.0 mm` mild-steel formed-angle strip: `48 mm` measured main face, `410 mm` upright/post height, and about `618 mm` developed main-face length across the top screw return, upright post, chassis bridge, and outer chassis leg.
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

Core Rev A parts:

- Battery stand top tray/deck: `560 x 360 x 3.0 mm` mild steel.
- Electrical backplane: `520 x 340 x 3.0 mm` mild steel.
- Single chassis pickup plate: `260 x 160 x 4.0 mm` mild steel, final slot pitch from the one chassis location.
- Upright bridge side plates: `130 x 260 x 4.0 mm` mild steel, make a mirrored pair around the single pickup bridge if stiffness requires it.
- Battery hold-down crossbar: `3.0 mm` mild steel or stainless, slot after measuring the battery.
- Cutoff guard: optional `2.0-3.0 mm` aluminium or plastic guard after the real switch is measured.

Layout:

- Battery field carries the battery and hold-down crossbar on the same stand.
- Relay field carries the existing Relay Rev C carrier base: `320 x 220 mm` finished face, `360 x 255 mm` flat pattern.
- MIDI field carries the existing `midi5_plate_mount_rev_c` fuse plate (`190 x 150 mm`) and `midi5_holder_subplate_rev_c` (`140 x 85 mm`).
- Cutoff field carries the master cutoff pilot/guard field. The pilot hole is not the final switch hole; open it only after measuring the switch body, panel-hole requirement, key/knob sweep, terminal studs, and cable lug sweep.
- The single chassis pickup plate bolts directly to the known chassis pickup location. The stand must remain removable for service.

Electrical route:

- Battery positive -> master cutoff -> MIDI common feed -> fused branches / relay feeds.
- Relay feed and MIDI feed must have insulating boots or covers over live studs.
- Heavy positive cables use insulated P-clips/saddle clamps near every direction change and roughly every `150-200 mm`.
- Use grommets/bushes through any sheet metal pass-throughs.
- Keep fuse, relay, and cutoff hardware away from battery acid/vent splash, water pooling, fan/belt movement, exhaust heat, steering movement, and sharp panel edges.

Release checks:

- Stand/tray cardboard mock-up with full-height battery, known Relay Rev C base, MIDI Rev C holder bank, cutoff switch, and cable lugs clears the bonnet, radiator, fan/belt, LHD steering shaft/box/service path, alternator service sweep, and cable bend radius.
- Sideways `520 x 340 mm` backplane is rejected or stepped/split if it crowds the LHD steering-side envelope, hydraulic line path, bonnet, radiator/fan envelope, or battery terminal service space.
- Battery and electrical load path is taken by the one chassis pickup plate and upright bridge, not tray skin, radiator strap, or unsupported inner wing.
- Cutoff body depth, knob/key clearance, and cable lug sweep are measured.
- Main cable bend radius is proven without loading cutoff, relay, or fuse studs.
- No exposed positive terminal can contact the carrier, body, bonnet, battery clamp, radiator support, or tools.
- Stand can be removed from chassis/front-support pickup points for service without disturbing radiator support pieces.

Battery-cavity mapping method:

- Use the installed battery as the fixed exclusion block before placing electrical hardware. Current working block in the package is `275 x 230 x 190 mm`; verify the actual battery dimensions and terminal height before relying on the map.
- Map front/radiator-side, inboard engine/LHD-steering-side, lower-under-tray, outboard-wing-side, and bonnet/terminal-height slices with the battery installed.
- Trial cardboard templates for Relay Rev C `320 x 220 mm`, MIDI Rev C `190 x 150 mm`, cutoff `150 x 95 mm`, plus depth blocks for cable lugs and boots.
- Prefer front/radiator-side space if it clears fan/radiator/hose/bonnet service. Treat inboard and lower spaces as cautious cable/support candidates unless the map proves a protected, serviceable rectangle.
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
8. Proposed relay/fuse/cutoff mock-up: cardboard `520 x 340 mm` sideways backplane held in the likely location with battery installed; mark the known Relay Rev C base, MIDI Rev C plate/subplate, cutoff base/guard, cable lug sweep, and the LHD steering-side no-go envelope.
9. Cutoff switch or isolator body: panel-hole size, body depth, terminal stud size, and cable exit directions.
10. Cable exit route from battery positive to cutoff/MIDI plate and from MIDI outputs toward the harness.
11. Bonnet closed/near-closed clearance over the battery, tray clamp, MIDI plate, and cutoff.

## Coating Gate

Radiator saddle drilling/through-bolt prep, battery tray support leg, battery carrier pickup, line/harness clip tab, or cable-support tab must be finished before final chassis/front-support primer, seam sealer, Raptor, and cavity wax.

The removable power-carrier backplane, Relay Rev C base, MIDI plate, non-conductive subplate, cutoff switch, and final cable clips can be installed after coating, provided the single chassis pickup structure is already installed, deburred, primed, and protected.
