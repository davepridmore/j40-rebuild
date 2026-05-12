# Front Engine-Bay Mounting Fabrication Plan - 2026-05-08

This plan splits the vague "missing bracket" concern into concrete front engine-bay fabrication jobs: radiator two-side retention, battery tray support, and a battery-adjacent power carrier for the MIDI fuse plate and battery master cutoff.

Linked bracket register: [chassis-bracket-analysis-register-20260508.md](chassis-bracket-analysis-register-20260508.md).

## Current Evidence

| Area | Evidence | Read |
| --- | --- | --- |
| Radiator/front support | `20260422_004423_gp_B1N5ThVw`, `20260422_004429_gp_4emWbTrA`, `20260422_004436_gp_yjCPMWTg`, `20260430_215957_gp_2iBbUagw`, `20260430_220004_gp_C9oYiYmA` | Direct evidence. The radiator, front support upright, lower support area, previous wire support, and fan/radiator clearance are visible enough to define the repair function. |
| May 12 radiator/upright context | `20260512_100000_user_front_support_radiator_pickups_context` | Direct structure-scout evidence. The visible upright/top hole, lower/front support hole field, radiator plane, and fan/pulley clearance are enough to start a removable side-strap/upright template. |
| Battery location / stand context | `20260317_235232_gp_3Ojs4Rag`, `20260317_235150`, `20260317_235201`, `20260423_232309_gp_rrFiL8og`, `20260512_100100_user_battery_side_tray_structure_context` | Partial structure evidence. The May 12 image improves the battery-side load-path and clearance read, but tray feet, underside supports, battery dimensions, and exact pickup points are still not clear enough to release a cut pattern. |
| MIDI fuse hardware | `20260411_143125`, `20260411_143135`, `data/manual/fabrication/midi5_plate_mount_rev_c/README.md` | Direct hardware evidence. Rev C remains the current MIDI holder plate/subplate package; it still needs a vehicle-side carrier/pickup design. |
| Cutoff / isolation hardware | `20260420_221819_gp_YV69fbvA`, electrical planning rows | Hardware/context evidence. Treat the battery-side item here as a battery master cutoff/isolator or breaker placement task, separate from the hidden diesel fuel-stop switch unless final wiring deliberately combines functions. |

## May 12 Provisional Structure Read

- Radiator: start with a removable side strap/upright template that uses the visible vertical upright/top hole, lower/front support hole field, and radiator side flange holes. Keep rubber isolation at the radiator and do not use the bracket to pull the radiator closer to the fan.
- Battery stand: build a separate tray/stand load path with a perimeter tray, lower/inner pickup points, and gussets. The battery mass should not load the radiator support strap or a flat unsupported inner-wing skin.
- Power carrier: mount the MIDI/cutoff carrier from the reinforced battery stand or adjacent structural support, with heavy positive cables clipped close to direction changes.
- Clearance holds: keep added structure clear of fan/pulley movement, LHD steering shaft path, alternator access, exhaust/front pipe heat, hose movement, bonnet closure, and battery terminal service space.

## Fabrication Jobs

### RAD-RET-001 - Radiator Two-Side Retention

Preferred outcome: a serviceable two-side radiator retention set that replaces the wire-held/one-side condition without moving the radiator into the fan, belt, hose, or bonnet-close envelope.

First-pass construction:

- Use existing radiator side flange holes and sound front-support holes where possible.
- Add or repair chassis/front-support tabs only where the existing support is missing, cracked, too thin, or badly placed.
- Treat the May 12 visible vertical upright/top hole and lower/front support hole field as the first template datum, subject to ruler confirmation and metal-condition check.
- Prefer a bolted removable bracket after any required welded tab is installed and coated.
- Use `3.0 mm` mild steel for welded tabs and removable support brackets unless aluminium is deliberately chosen for a fully bolted non-welded piece.
- Use rubber washers, bushes, or grommet-style isolation at the radiator contact faces. Do not hard-clamp the radiator tank/core.
- Use slotted holes only for alignment, then washer properly so the slot cannot tear or creep.
- Preserve the current radiator plane unless dry-fit proves it must move; fan clearance is a release dimension.

Release checks:

- Both sides of the radiator restrained in fore/aft and lateral movement.
- No metal-to-metal rubbing on radiator tank, fins, or side rails.
- Lower and upper hose paths stay relaxed.
- Fan and shroud clearance confirmed after tightening.
- Brackets removable enough for future radiator service.

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

### PWR-CARRIER-001 - Battery-Side MIDI / Cutoff Carrier

Preferred outcome: a battery-adjacent removable carrier that accepts the existing MIDI 5-way Rev C plate and a battery master cutoff/isolator without loading the battery tray skin or crowding the battery terminals.

The existing `midi5_plate_mount_rev_c` package remains valid for the MIDI holder itself:

- Mount plate: `190 x 150 x 3.0 mm` aluminium.
- Holder subplate: `140 x 85 x 5.0 mm` non-conductive board.
- Stand-offs: `10-12 mm`.

The new work is the vehicle-side carrier/interface:

- Use a `3.0 mm` steel or aluminium upright/bridge bracket, depending on whether the final pickup points are welded or bolted.
- Pick up from battery tray support/upright or adjacent structural support, not unsupported thin sheet.
- Prefer a removable vertical carrier on the reinforced battery-stand side rather than a plate fixed directly to tray skin.
- Keep MIDI covers serviceable from above/front.
- Keep the cutoff reachable but protected from accidental knocks and water pooling.
- Route battery positive as: battery positive -> master cutoff/breaker -> MIDI common feed -> fused branches.
- Support heavy cables with P-clips/saddle clamps near direction changes and at roughly `150-200 mm` intervals.
- Use grommets/bushes through any sheet metal pass-throughs.
- Keep fuse and cutoff hardware out of the battery acid/venting splash zone as far as packaging allows.

Release checks:

- Cutoff body depth, knob/key clearance, and cable lug sweep measured.
- MIDI plate template placed next to the real battery and bonnet shut line.
- Main cable bend radius proven without loading fuse studs.
- No exposed positive terminal can contact the carrier, body, bonnet, or clamp.
- Carrier can be removed without removing the battery tray from the vehicle.

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
8. Proposed MIDI/cutoff mock-up: cardboard `190 x 150 mm` plate held in the likely location with battery installed.
9. Cutoff switch or isolator body: panel-hole size, body depth, terminal stud size, and cable exit directions.
10. Cable exit route from battery positive to cutoff/MIDI plate and from MIDI outputs toward the harness.
11. Bonnet closed/near-closed clearance over the battery, tray clamp, MIDI plate, and cutoff.

## Coating Gate

Any welded radiator tab, battery tray support leg, battery carrier pickup, line/harness clip tab, or cable-support tab must be finished before final chassis/front-support primer, seam sealer, Raptor, and cavity wax.

The removable MIDI plate, non-conductive subplate, cutoff switch, and final cable clips can be installed after coating, provided their welded or structural pickup points are already installed, deburred, primed, and protected.
