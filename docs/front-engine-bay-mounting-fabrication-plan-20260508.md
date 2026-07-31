# Front Engine-Bay Mounting Fabrication Plan - 2026-05-08

This plan splits the vague "missing bracket" concern into concrete front engine-bay fabrication jobs: radiator two-side retention, battery tray support, a battery-side master cutoff/breaker, and a removable radiator-carrier electrical plate for Relay Rev D and MIDI Rev D.

Linked bracket register: [chassis-bracket-analysis-register-20260508.md](chassis-bracket-analysis-register-20260508.md).

## Current Evidence

| Area | Evidence | Read |
| --- | --- | --- |
| Radiator/front support | `20260422_004423_gp_B1N5ThVw`, `20260422_004429_gp_4emWbTrA`, `20260422_004436_gp_yjCPMWTg`, `20260430_215957_gp_2iBbUagw`, `20260430_220004_gp_C9oYiYmA` | Direct evidence. The radiator, front support upright, lower support area, previous wire support, and fan/radiator clearance are visible enough to define the repair function. |
| May 12 radiator/upright context | `20260512_100000_user_front_support_radiator_pickups_context` | Direct structure-scout evidence. The visible upright/top hole, lower/front support hole field, radiator plane, and fan/pulley clearance are enough to start a removable side-strap/upright template. |
| Battery location / stand context | `20260317_235232_gp_3Ojs4Rag`, `20260317_235150`, `20260317_235201`, `20260423_232309_gp_rrFiL8og`, `20260512_100100_user_battery_side_tray_structure_context`, `20260517_194303_gp_5yuaRoaA`, `20260517_194313_gp_HolDWYeQ`, `20260517_194431_gp_4XVycxAg`, `20260517_194439_gp_K63N2nJw`, `20260517_194452_gp_ow8njPsw`, `20260517_194511_gp_QI0Ua2yQ` | May 17 adds actual installed battery ruler views and existing tray/mount opening and height measurements. Tray underside/foot condition, dry-fit pickup templates, cable sweep, and cutoff/MIDI mock-up still need closure before release. |
| Relay / MIDI fuse / cutoff hardware | `20260411_143125`, `20260411_143135`, `20260420_221819_gp_YV69fbvA`, `data/manual/fabrication/battery_power_carrier_mount_rev_a/README.md`, `data/manual/fabrication/relay_mount_rev_d/README.md`, `data/manual/fabrication/midi5_enclosure_rev_d/README.md` | Direct hardware evidence. The 2026-07-31 layout decision moves Relay Rev D and MIDI Rev D from the battery-stand access ladder to a removable plate on the structural radiator/cooling-stack carrier. Battery Power Carrier Rev A remains reference material for the tray, saddle, hold-down, and battery-side cutoff/breaker only; its relay/MIDI ladder is superseded. |
| Cutoff / isolation hardware | `20260420_221819_gp_YV69fbvA`, electrical planning rows | Hardware/context evidence. Treat the battery-side item here as a battery master cutoff/isolator or breaker placement task, separate from the hidden diesel fuel-stop switch unless final wiring deliberately combines functions. |

## May 12 Provisional Structure Read

- Radiator: copy the simple left-side 90 degree top-post idea, but retain it with a bolt-through saddle rather than welding it to the chassis. Use one 4 mm mild-steel right-angle post with lower legs over both sides of the chassis/front-support section, a through-bolt across the legs and chassis, and a top return for the radiator screw.
- Battery stand: use a steel stand with one formed saddle over the chassis rail, an upright bridge, and a top tray/deck that supports the battery directly from real structure. The battery mass should not load the radiator support strap or a flat unsupported inner-wing skin.
- Electrical layout: mount Relay Rev D and MIDI Rev D on a removable electrical plate carried by the radiator/cooling-stack structural uprights or their designed accessory rails. Do not attach electrical hardware to the radiator core, fins, tanks, necks, seams, or through-core rods, and do not make the rubber-isolated radiator carry its mass. Keep the master cutoff/breaker beside the battery so the unprotected positive lead stays short. Heavy positive cables need insulated clips near direction changes and roughly every `150-200 mm`.
- Clearance holds: keep added structure clear of fan/pulley movement, LHD steering shaft path, alternator access, exhaust/front pipe heat, hose movement, bonnet closure, and battery terminal service space.

## Fabrication Jobs

### RAD-RET-001 - Radiator Two-Side Retention

Preferred outcome: a serviceable two-side radiator retention set that replaces the wire-held/one-side condition without moving the radiator into the fan, belt, hose, or bonnet-close envelope.

Current package: [front_radiator_two_side_retention_rev_a](../data/manual/fabrication/front_radiator_two_side_retention_rev_a/README.md)

Prerequisite: fabricate or dry-fit the right-side strap/post before final radiator installation. The metal stock route is controlled by [fabrication-metal-stock-list-20260514.md](fabrication-metal-stock-list-20260514.md): start with `50 x 50 x 4 mm` mild-steel angle/L-section, `1 m`, plus rubber isolation from `3-5 mm` EPDM/SBR sheet. If the angle does not match the measured `48-50 mm` radiator-post face, use the nearest 4 mm angle only after a dry-fit video proves the radiator ear and vehicle support can be joined without pulling the radiator out of plane.

Aluminium radiator contingency: if the bought aluminium radiator does not land on the existing/fabricated retention arms, do not add another random leg to the radiator. First dry-fit the radiator on lower pads with relaxed hoses. If the core, tanks, necks, drain, cap, and fan clearance are acceptable, fabricate only a removable rubber-isolated adapter plate/crossbar/saddle between the vehicle-side support and the radiator mount. If those fundamentals are wrong, reject the radiator for this vehicle rather than building structure around it.

First-pass construction:

- Use one `4.0 mm` mild-steel formed-angle strip: `48 mm` measured main face, `410 mm` upright/post height, and about `618 mm` developed main-face length across the top screw return, upright post, chassis bridge, and outer chassis leg. Prefer pre-formed `90-degree` angle/L-section stock if one leg is close to `48-50 mm`; otherwise form the return from flat stock.
- Straddle the chassis/front-support section with the two lower legs and retain the bracket with a through-bolt through both legs and the chassis.
- Treat the measured left chassis-attached bracket and the supplied photo as first template datums, subject to ruler confirmation and metal-condition check.
- Use rubber washers, bushes, or grommet-style isolation at the top screw if required. Do not hard-clamp the radiator tank/core.
- Use crush-tube/spacer practice if bolting through boxed chassis/front-support metal.
- Do not weld the bracket to the chassis or add a separate rubber-pad fabrication part unless dry-fit proves the bolted saddle route is wrong.
- Preserve the current radiator plane unless dry-fit proves it must move; fan clearance is a release dimension.
- Any adapter used for a bought aluminium radiator must attach to vehicle-side structure and radiator mounting ears/rails only; it must not hard-clamp or load the aluminium tank/core.

Release checks:

- Both sides of the radiator restrained in fore/aft and lateral movement.
- No metal-to-metal rubbing on radiator tank, fins, or side rails.
- Lower and upper hose paths stay relaxed.
- Fan and shroud clearance confirmed after tightening.
- Top screw and through-bolt remain serviceable and the saddle bracket does not block radiator removal.
- If an aluminium-radiator adapter is used, it is removable, rubber-isolated, and proven by shake test without tank/core flex.

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
- Terminals cannot short against clamp, bonnet, MIDI enclosure, cutoff body, or tools during service.
- Tray coating plan is explicit: zinc-rich epoxy/primer, top protection, then removable liner.

### BAT-CARRIER-001 - Chassis-Mounted Battery Stand / Cutoff Carrier

Preferred outcome: a removable steel stand that supports the full battery mass and retains the master cutoff/breaker close to the battery. Relay Rev D and MIDI Rev D are no longer carried on this stand.

Reference package: [battery_power_carrier_mount_rev_a](../data/manual/fabrication/battery_power_carrier_mount_rev_a/README.md). Use only its battery tray, chassis saddle, upright/offset support, hold-down, and battery-side cutoff/breaker details. The `660 x 310 mm` relay/MIDI access ladder and its hole fields are superseded.

- Keep the battery in its measured pocket with a removable hold-down and a load path into real chassis/body structure.
- Keep the master cutoff/breaker beside the battery and ahead of the longer feed to the radiator carrier, minimizing unprotected positive-cable length.
- Measure the cutoff/breaker body, key/knob sweep, stud/lug sweep, terminal boots, and battery lift-out path before drilling.
- Do not fabricate the old relay/MIDI ladder unless the radiator-carrier dry-fit fails and this plan is deliberately revised again.

### ELEC-RAD-001 - Radiator-Carrier Relay And Fuse Layout

Preferred outcome: Relay Rev D and MIDI Rev D travel with the cooling-stack carrier on a removable, protected, serviceable electrical plate, while the radiator itself remains unloaded and independently isolated.

First-pass layout:

- Attach the electrical plate to the structural cooling-stack upright, crossbar, or purpose-designed accessory rail. Never drill, clamp, or tie it to the radiator core, fins, tanks, necks, cap structure, drain, braze/solder seams, or through-core rods.
- The structural carrier carries the electrical mass. The rubber-isolated radiator should remain removable separately where practical; if the fabricator makes the radiator and plate one removable module, provide a deliberate electrical disconnect and prove that no cable loads the radiator.
- Reuse the Relay Rev D `360 x 245 x 3 mm` aluminium base with its exact `300 x 197 x 3 mm` insulating sheet and covered relay box.
- Reuse the MIDI Rev D `210 x 165 x 65 mm` hinged enclosure and `140 x 85 mm` holder subplate. Preserve the agreed fuse positions, input/output grommets, and far-side doubled-cable exit.
- Orient covers, lids, connectors, and cable exits for access with the grille/front panel removed. Prefer downward or side-down exits, a drip shield, and drainage without creating a water trap.
- Keep the plate and hardware outside the core airflow aperture and clear of the fan/shroud, belts, hoses, cap, drain, bonnet, steering, hot surfaces, and radiator removal path.

Electrical route:

- Battery positive -> battery-side breaker/cutoff -> protected main feed to the radiator-carrier plate. Split there to MIDI fuse 4 input and the relay battery-side top entry; the relay output bundle leaves the second top entry.
- The existing relay assignments, fuse sizing, and branch logic remain unchanged. This decision changes physical placement and cable routing only.
- Protect every live stud with a boot/cover. Use grommets at metal pass-throughs and insulated P-clips near direction changes and roughly every `150-200 mm`.
- Add strain relief at the removable-carrier boundary and enough service loop to disconnect the plate without loading studs. Use rated service connectors for control/branch circuits; retain ring-lug/stud connections and a deliberate isolated disconnect procedure for heavy conductors that exceed connector ratings.
- Label both ends of every relocated feed, output, control plug, and earth. Recalculate cable lengths and voltage drop before final crimping.

Release checks:

- Cardboard-template both enclosures, lids/covers, cable bends, terminal boots, drip protection, and disconnect access on the actual cooling-stack carrier.
- Prove bonnet, grille, fan/shroud, hose, cap, drain, steering, belt, radiator-removal, and tool-access clearances with the stack installed.
- Prove the plate does not mask useful radiator/condenser airflow or transfer electrical mass/vibration into a tank, core, or isolated radiator mount.
- Confirm abrasion protection, heat/splash exposure, clip spacing, bend radius, strain relief, and no exposed positive terminal contact risk.
- After relocation, repeat continuity, earth integrity, fuse identification, relay-function, cranking-voltage-drop, and charging checks before energising optional loads.

### PWR-CABLE-001 - Cable And Clip Support

Preferred outcome: cable support points designed at the same time as the carrier, so the heavy battery/MIDI cables are not left hanging after coating.

First-pass construction:

- Add P-clip holes or small bolted tabs to the carrier and nearby support metal.
- Keep cable routes away from fan, belts, exhaust heat, steering movement, and sharp panel edges.
- Use insulated P-clips for heavy positive cables.
- Keep service loops short enough not to rub, but long enough to remove the MIDI enclosure/cutoff without stressing lugs.

## Scouting Required Before Cutting Metal

Capture these with a ruler or tape measure in frame:

1. Radiator left and right side flanges: top/middle/lower holes, broken tabs, wire-tie path, and current bolt sizes.
2. Front support and lower crossmember holes around the radiator, both sides, including the May 12 visible upright top hole and its base attachment.
3. Minimum fan-to-radiator clearance at the closest point, with the radiator sitting where it currently sits.
4. Battery from top: length, width, height, terminal orientation, clamp position, and bonnet clearance.
5. Battery tray from top and side: existing tray edges, clamp holes, corrosion, cracks, and any current support tabs.
6. Battery tray underside: feet, braces, inner wing attachment, chassis/engine clearance, and possible lower support leg path.
7. Battery stand template: cardboard or flat-bar tray perimeter plus proposed lower/inner pickup points and gusset directions.
8. Radiator-carrier electrical mock-up: hold Relay Rev D `360 x 245 mm` and MIDI Rev D `210 x 165 x 65 mm` templates on the structural cooling-stack carrier, including lid/cover sweeps, cable exits, boots, drip shield, P-clips, disconnects, and the unobstructed core-airflow aperture.
9. Cutoff switch or isolator body: panel-hole size, body depth, terminal stud size, and cable exit directions.
10. Protected cable route from battery positive through the battery-side cutoff/breaker to the radiator carrier, then to MIDI fuse 4 and the relay battery-side entry, with branch/control routes and a service-disconnect point marked.
11. Bonnet closed/near-closed clearance over the battery and cutoff plus grille/front-panel, fan/shroud, hose, cap, drain, radiator-removal, and lid/cover access around the electrical plate.

## Coating Gate

Radiator saddle drilling/through-bolt prep, battery tray support leg, battery carrier pickup, line/harness clip tab, or cable-support tab must be finished before final chassis/front-support primer, seam sealer, Raptor, and cavity wax.

The battery stand/cutoff carrier and radiator-carrier electrical plate may be installed after coating, provided every structural pickup, weld, rivnut/through-bolt hole, pass-through, earth point, and cable-support tab has already been dry-fitted, deburred, primed, and protected.
