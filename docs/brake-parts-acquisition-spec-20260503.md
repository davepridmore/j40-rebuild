# Brake Parts Acquisition Spec - 2026-05-03

Purpose: vendor/workshop handoff for the brake refresh package. Use this with `data/manual/brake_system_requirements.csv` and `docs/brake-parts-pakistan-acquisition-20260503.md`; do not discard old brake parts until replacements fit.

## Vehicle Basis

- Vehicle: 1978 Toyota Land Cruiser J40 project truck.
- Fitted engine basis: Toyota 2H diesel.
- Brake architecture basis: front disc / rear drum.
- May 29 photos show the front disc setup more specifically: visible Sumitomo fixed front calipers, external hard-line/transfer-pipe detail, dust shields, current rotors, and short hard-line/front hose routing. User decision: replace/renew all front disc service parts. Fitted hardware, hoses, pad shape, rotor dimensions, and old samples still control exact front brake part matching.
- Ironman Foamcell geometry is treated as effectively the same as the current setup, so brake flex hoses do not need a separate lift/geometry release action.

## Purchase-Ready Now

| Item | Quantity / scope | Acquisition spec |
| --- | --- | --- |
| DOT 3 brake fluid | 2 L sealed total, e.g. 2 x 1 L or 4 x 500 ml | Sealed fresh DOT 3 brake fluid meeting SAE J1703 / FMVSS No. 116 DOT 3. Do not use DOT 5. Do not use opened/old bottles. Do not mix with unknown old fluid. Workshop can revise quantity upward if using a pressure bleeder or flushing extra contaminated fluid. |
| Brake cleaner | Workshop quantity | Non-residue brake cleaner for drum opening, line cleanup, and leak checks. |
| Clear bleed hose and catch bottle or bleeder kit | 1 set | Clear hose that fits bleeder nipples, plus catch bottle or decent one-person bleeder kit. |
| Brake line caps/plugs | 1 mixed set | Purpose-made hydraulic line caps/plugs for open brake ports and fittings during line removal. Generic rubber dust caps are not pressure seals. |
| Rags, nitrile gloves, catch tray | Workshop quantity | Must be available before brake fluid is exposed. |

## Baseline Brake Parts To Source After Identification

These are approved replacement/renewal scope, but exact part numbers must be matched to fitted hardware, close photos, measurements, and old samples. The May 29 removed booster/servo photos confirm the old brake parts should be treated as samples or rebuild cores, not reuse candidates. The front disc local quote path is assigned to Amir in [amir-montgomery-road-shopping-list-20260527.md](amir-montgomery-road-shopping-list-20260527.md); he may collect prices/photos but cannot approve safety-critical fit or payment without labelled samples, written specs, or explicit mechanic/user approval. Front disc reference numbers added 2026-05-30 are quote/spec anchors only, not blind-buy approvals.

| Component | Required scope | Release gate |
| --- | --- | --- |
| Front disc pads and retaining hardware | Required P0: 1 axle set for visible Sumitomo fixed-caliper setup | Reference pad family: `04491-60010`, `04491-60030`, `04465-35170`, `04465-YZZC0`; catalog Sumitomo pad shape is about `107 x 65.7 x 15.5 mm`. Reference hardware: `BR06158K` / `MT 12342`, with 4 pad pins, 2 anti-rattle springs, and 2 pin clips; Toyota hardware refs include `90240-06158`, `90468-12003`, `47748-60010`. Buy only after removed pad outline, backing ears, pad thickness, retaining hardware, rotor fit, and wheel clearance match the truck. |
| Front Sumitomo fixed calipers | Required P0: renew as a matched pair; professional rebuild with seal kits only if bodies/pistons/bores/bleeders/bridge pipes pass inspection, otherwise matched rebuilt/new Sumitomo-family calipers | Reference caliper family: Toyota `47730-60021` RH and `47750-60021` LH for 9/1975-1/1990 factory front-disc Land Cruiser applications. Catalog design references show a fixed Sumitomo 4-piston caliper using `34/43 mm` piston diameters on a `20 mm` disc family. Clean and record casting marks, piston count/diameter, inlet and hard-line/transfer-pipe fittings, bleed screw, mounting pattern, and side orientation before payment. |
| Front rotors | Required P0: replace as a pair | Reference rotor: Toyota `43512-60011`, quantity 2 for 1975-1980 Land Cruiser front disc applications. Catalog design reference for the matching OE family: vented front disc, `302 mm` OD, `20 mm` nominal thickness, `19 mm` minimum thickness, `100 mm` center bore, `139.7 mm` PCD, `48 mm` height, 6 mounting holes plus 2 service/auxiliary holes. Measure the old rotor diameter, thickness, height, hub/register fit, stud pattern, dust-shield/caliper clearance, and wheel clearance before payment. Do not machine/reuse as the baseline path. |
| Front flexible brake hoses | Required P0: replace every fitted front flex hose; expected count is 2 lower wheel hoses plus 1 front upper/frame hose if present | Lower wheel hose reference: `553-102`, front lower LH/RH, `9 1/4 in`, DOT rubber, FJ40/FJ45/FJ55 7/1970-8/1980. Front upper/frame hose reference if fitted: `553-101`, `10 3/8 in`, DOT rubber, includes retaining clip, FJ40/FJ45 9/1975-10/1984. Confirm actual hose count, chassis end, caliper/short-hard-line end or banjo if fitted, bracket/clip style, free length, steering lock clearance, and droop clearance. Hose assemblies must be DOT/SAE J1401 or OEM-equivalent crimped brake hoses. |
| Rear parking-brake cable set | New left/right rear cable assemblies plus equalizer/clevis/spring/clip hardware as fitted | Remove/label old cables, measure overall length, sheath length, backing-plate end, equalizer end, adjuster thread/travel, and clip positions. Old cables are samples only. |
| Rear axle hard brake lines | Left/right axle lines from center T/union to wheel cylinders | Recreate in brake-rated 4.75 mm / 3/16 in tube. Match flare type, fitting threads/seats, bend templates, route lengths, and clip positions. No bare copper. |
| Rear center flexible brake hose | 1 frame-to-axle hose | Confirm chassis-side and axle-side fitting style/thread, bracket retention, and old-sample/free length. Must be DOT/SAE J1401 or OEM-equivalent crimped brake hose. |
| Rear wheel cylinders | Pair | Open drums and identify bore, port thread, mounting bolt pattern, pushrod style, side, and bleed screw access. |
| Rear brake shoes and spring/adjuster hardware | 1 axle set | Open drums and confirm drum inside diameter, shoe width, adjuster style, spring layout, and backing-plate family. |
| Brake-line and parking-brake cable clips/retainers/grommets | As counted | Count positions, keep samples, confirm tube/cable OD, hole size, bracket thickness, and chafe points. |
| Brake vacuum booster / servo assembly | 1 replacement or professional rebuild | Front discs/rear drums are confirmed. Target a professionally refurbished/remanufactured Land Cruiser tandem/dual-diaphragm booster in the `44610-60050` / `BBN60050` 1975-1987 40/55/60 family, supplier-confirmed against the old unit. Confirm fitted booster markings, mounting studs, master-cylinder seat/depth, pushrod/clevis, check valve/grommet, and vacuum hold before payment. Reject raw used take-offs unless they are only a rebuild core; reject single/drum `44610-60040` and later `44610-60160` unless sample-matched and approved. |
| Master cylinder, reservoir, and proportioning/bias service parts | Replacement/renewal by fitted layout | Match installed master bore, reservoir layout, booster pushrod depth, ports, fitting threads, flare seats, and any proportioning/bias hardware before ordering or fitting. |

## Brake Booster Options

Do not make the brake plan depend on finding another used 1978 booster.

Amir may carry the old booster/servo as a sample for professional refurbishment or a direct-match refurbished exchange unit. Payment is blocked until the required video set in [amir-refurbishment-video-gates-20260529.md](amir-refurbishment-video-gates-20260529.md) is reviewed: old sample identity, sample match, interface close-ups, vacuum hold test, assist movement test, contamination check, and final acceptance video.

| Rank | Path | What to ask for | Why / risk |
| ---: | --- | --- | --- |
| 1 | Refurbished/reman direct-fit Land Cruiser booster | Professionally refurbished/remanufactured tandem/dual-diaphragm `44610-60050` / `BBN60050` family booster for the 1975-1987 Land Cruiser 40/55/60 disc-brake family. Quote `44610-60100` / `44610-60180` only when supplier lists the same 1975-1987 family fitment and the old unit sample-matches. | Best balance: keeps firewall/pedal/master geometry closest to original while avoiding a tired used servo. |
| 2 | Local Land Cruiser 40/55/60 core for rebuild | Complete dual-diaphragm booster with check valve/grommet and pedal clevis hardware where possible. | Use as a rebuild candidate only, or accept installed use only after sample match and bench vacuum hold test. Reject hiss, leakdown, brake-fluid contamination, welded shell, or wrong single/drum booster. |
| 3 | Complete FJ40 booster/master/proportioning retrofit kit | Dual-diaphragm booster + master cylinder + proportioning valve/bracket/lines designed for FJ40 front disc/rear drum. | Viable modernized path, but it changes plumbing and may require new non-metric/standard inverted flare nuts, line work, and proportioning validation. |
| 4 | Random modern donor booster | Quote/photos only. | Not recommended first pass. Firewall pattern, pedal ratio, pushrod depth, master bore, line threads, and brake balance all become custom engineering. |

Measurements before payment or adaptation:

- Booster shell diameter and depth.
- Firewall stud horizontal/vertical spacing, stud thread, and bracket depth.
- Master-cylinder stud spacing, pilot/seat diameter, gasket face, and pushrod depth.
- Pedal clevis thread, clevis width, clevis pin diameter, pushrod length, and free-play adjustment range.
- Check-valve grommet OD, nipple/barb OD, nipple direction, and hose ID.
- Master-cylinder bore, front/rear port threads, flare seat type, residual/proportioning valve layout.

## Vendor Message

Superseded for hydraulic-opening prep as of 2026-05-27: do not quote this as a separate consumables order. DOT 3 fluid, clear bleed hose, and nitrile gloves are received; line caps/plugs, brake cleaner, catch bottle/bleeder, rags, and catch tray are managed from on-hand/workshop supplies and must be verified before any hydraulic line is opened.

For the remaining brake parts and brake booster, prepare sourcing but do not take payment for exact parts until the fitted calipers, rear drums, hoses, hard-line fittings, parking-brake cables, booster/master interface, and old samples are measured and photographed. Final-install brake hoses, hard lines, parking-brake cables, fittings, clips, rubbers, and seals are new-only.

For the brake booster specifically, do not pay Amir/the shop until the video gate in [amir-refurbishment-video-gates-20260529.md](amir-refurbishment-video-gates-20260529.md) is complete and approved.
