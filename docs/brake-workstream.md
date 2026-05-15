# Brake Workstream

## Scope

- Split brake work out from `steering_brakes_suspension` so hardware identification, hydraulic refresh, and conversion decisions stay explicit.
- Current working read: `front disc / rear drum`.
- Current default direction: replace normal front and rear brake service parts as baseline work, keep the existing `front disc / rear drum` architecture, and treat rear-disc conversion as optional only if inspection or real use shows a clear measured need.
- Merged execution sheet: [suspension-brake-merged-work-plan.md](suspension-brake-merged-work-plan.md).
- Current hard-line tooling and parts selection: [brake-hard-line-tool-parts-selection-20260514.md](brake-hard-line-tool-parts-selection-20260514.md).

## Current Configuration Read

| Area | Current read | Why it currently reads that way |
| --- | --- | --- |
| Front axle | Disc | One front underside photo appears to show a disc caliper, and the March 16 chat log says the front-disc conversion was already done. |
| Rear axle | Drum | Rear axle photos show drum/backing-plate style hardware and parking-brake linkage. |

## Derived Ordering Constraints

- Vehicle basis for brake ordering is the active project vehicle: `1978 Toyota Land Cruiser J40`.
- Treat the current brake architecture as `front disc / rear drum` until direct inspection proves otherwise.
- Assume standard brake service parts will be replaced during the baseline refresh: front pads/hardware, front flex hoses, rear shoes/hardware, rear wheel cylinders, rear parking-brake cables, rear axle hard lines, rear center flex hose, clips/retainers, brake fluid, and bleed consumables.
- Braking consumables and safety parts are new-only for final installation: flex hoses, hard lines, rear parking-brake cables, cable clips/retainers, hydraulic fittings, rubber sleeves/grommets, seals, and springs/hardware. Old parts are samples for length, end style, routing, and fit.
- Do not order front pads, caliper kits, rotors, or front flex hoses from year/catalog alone because the front disc setup appears to be a previous conversion.
- Do not order rear shoes, wheel cylinders, rear cables, or rear center hose from catalog logic alone. The rear drum family and cable/hose end styles still need direct confirmation from the fitted truck and old samples.
- Use the fitted hardware and old samples to order brake parts: backing plates, cable ends, calipers, wheel cylinders, master/proportioning fittings, and hose ends control the final spec.
- The Ironman Foamcell suspension kit is already ordered and its geometry is treated as effectively the same as the current setup, so brake flex hoses do not need a separate Ironman/lift release action.
- The rear parking-brake cable route and rear axle hard-line route should be renewed in the same workshop window as the rear suspension work, because the axle, U-bolts, spring pads, clips, and routes are exposed then.
- Keep rear drums as the default path; rear-disc conversion stays out of baseline scope unless inspection or road validation gives a measured reason.
- Brake flex hoses must be complete crimped hydraulic assemblies rated to `DOT/SAE J1401` or OEM-equivalent. Do not fabricate flex hoses from generic rubber hose.
- Brake hard-line stock order is `3/16 in / 4.75 mm` brake tube. May 14 installed-fitting photos plus the user flare side-view point to Toyota-style `double / inverted` flares, not ISO bubble flares, but final fabrication still requires a removed old line or opened seat to confirm the straight-on sealing face, fitting thread, and seat at each connection.
- The ordered PARD flaring kit is accepted only after receipt check proves a true `4.75 mm / 3/16 in` double/inverted flare die. If it is only a generic `4-16 mm` set without `4.75 mm / 3/16 in`, it does not release brake-line fabrication.

## Brake Configuration Evidence Photos

### Direct evidence

| File | Inventory classification | Current interpretation |
| --- | --- | --- |
| [20260324_004852.jpg](../photos/20260324_004852.jpg) | `rear_axle_and_leaf_springs` | Rear drum/backing-plate hardware is visible. |
| [20260324_004906.jpg](../photos/20260324_004906.jpg) | `rear_axle_and_leaf_springs` | Second rear drum view that supports the same reading. |
| [20260423_232202_gp_ryYH6xZg.jpg](../photos/20260423_232202_gp_ryYH6xZg.jpg) | `frame_and_mount_points` | Appears to show a front disc caliper at the axle end. |

### Supporting context

| File | Inventory classification | Why it matters |
| --- | --- | --- |
| [20260423_232220_gp_ezwEcH2g.jpg](../photos/20260423_232220_gp_ezwEcH2g.jpg) | `steering_and_suspension_linkages` | Same front-axle/steering area and useful context around the front brake zone. |
| [20260423_232236_gp_caYB252g.jpg](../photos/20260423_232236_gp_caYB252g.jpg) | `steering_and_suspension_linkages` | Same-session support shot for the front axle-end area. |
| [20260406_031010.jpg](../photos/20260406_031010.jpg) | `steering_and_suspension_linkages` | Earlier underside view around the front steering/brake zone. |
| [20260411_220207.jpg](../photos/20260411_220207.jpg) | `suspension_or_linkage_mount` | Supporting underside mount context; not a decisive brake-hardware photo on its own. |
| [20260411_220214.jpg](../photos/20260411_220214.jpg) | `suspension_or_linkage_mount` | Supporting underside mount context; not a decisive brake-hardware photo on its own. |

## Hydraulic And Hard-Line Evidence Photos

These photos already back the existing `chassis_hard_lines_and_brackets` and `issue_brake_fuel_line_clip_corrosion` rows and should be treated as the current direct evidence set for hose, hard-line, clip, and bracket condition:

- [20260331_030439_gp_Hm0ga9nQ.jpg](../photos/20260331_030439_gp_Hm0ga9nQ.jpg)
- [20260331_224409.jpg](../photos/20260331_224409.jpg)
- [20260331_224411_gp_xotdHr5w.jpg](../photos/20260331_224411_gp_xotdHr5w.jpg)
- [20260331_224415.jpg](../photos/20260331_224415.jpg)
- [20260331_224416_gp_HZ3sjkkA.jpg](../photos/20260331_224416_gp_HZ3sjkkA.jpg)
- [20260331_224423.jpg](../photos/20260331_224423.jpg)
- [20260331_224424_gp_whE84rpw.jpg](../photos/20260331_224424_gp_whE84rpw.jpg)
- [20260331_224428.jpg](../photos/20260331_224428.jpg)

### May 14 Brake Pipe / Fitting Close-Ups

The May 14 import is now assigned to the braking workstream and to `RPI-BRAKE-001-B/C` in [replacement_pipe_photo_intake.csv](../data/manual/replacement_pipe_photo_intake.csv). The photos improve the fitting/route evidence. The added user flare side-view is stronger than the installed fitting photos because it shows the raised folded flare lip, but it still does not fully release fabrication because the straight-on sealing face and the matching port seat/thread are not confirmed.

| File | Use |
| --- | --- |
| [20260514_095907_gp_Ni1EUf4A.jpg](../photos/20260514_095907_gp_Ni1EUf4A.jpg) | Master/proportioning-area hard-line and flare-nut context. |
| [20260514_095926_gp_YBNOqh9A.jpg](../photos/20260514_095926_gp_YBNOqh9A.jpg) | Master reservoir/port and installed line fitting context. |
| [20260514_100647_gp_foDr3ymA.jpg](../photos/20260514_100647_gp_foDr3ymA.jpg) | Best close-up of an installed hard-line flare nut into a hydraulic fitting. |
| [20260514_111300_user_brake_flare_side_view.png](../photos/20260514_111300_user_brake_flare_side_view.png) | User-provided side view of an actual brake hard-line flare; raised folded lip supports the `double / inverted` read. |
| [20260514_095856_gp_vjZG4NtQ.jpg](../photos/20260514_095856_gp_vjZG4NtQ.jpg) | Rear axle brake line / flex-hose fitting and route context. |
| [20260514_095846_gp_a9olRp5g.jpg](../photos/20260514_095846_gp_a9olRp5g.jpg) | Rear axle hard-line route and hose/bracket context. |
| [20260514_095836_gp_tmRy9fqg.jpg](../photos/20260514_095836_gp_tmRy9fqg.jpg) | Rear hard-line and parking-brake linkage context at the axle. |
| [20260514_095826_gp_fg74oFMQ.jpg](../photos/20260514_095826_gp_fg74oFMQ.jpg) | Rear drum/backing-plate with wheel-cylinder hard-line entry. |
| [20260514_095820_gp_nuP5s76A.jpg](../photos/20260514_095820_gp_nuP5s76A.jpg) | Rear hard-line route, clip/support context, and parking-brake linkage. |
| [20260514_095812_gp_5kblggGA.jpg](../photos/20260514_095812_gp_5kblggGA.jpg) | Rear wheel-cylinder hard-line entry close-up. |
| [20260514_095953_gp_BXoQkXnw.jpg](../photos/20260514_095953_gp_BXoQkXnw.jpg) | Rear parking-brake cable and backing-plate context. |
| [20260514_100003_gp_Vr2QI7ig.jpg](../photos/20260514_100003_gp_Vr2QI7ig.jpg) | Rear parking-brake cable/bracket route context. |
| [20260514_100008_gp_bq1VQUXQ.jpg](../photos/20260514_100008_gp_bq1VQUXQ.jpg) | Rear drum/wheel-cylinder hard-line and parking-brake close-up. |

Working flare read: treat the brake hard lines as `double / inverted flare` on `4.75 mm / 3/16 in` brake tube. The side-view flare photo makes this a stronger working call, but final fabrication still needs a straight-on view of a removed flare and the matching seat/thread at the hose, wheel cylinder, master/proportioning, and union ports. Do not order or fabricate ISO bubble, single flare, or plumbing flare ends for these brake lines unless a removed original line proves that standard at a specific port.

## Rear Axle Cable / Line Replacement Track

UI requirements table source: [brake_system_requirements.csv](../data/manual/brake_system_requirements.csv).

The visible "wires" running to the rear brakes should be handled as brake safety hardware:
- parking-brake / handbrake cables and linkage to the rear drum backing plates
- rear axle hydraulic hard brake lines
- rear center frame-to-axle flexible brake hose
- line clips, cable retainers, and protective sleeves/grommets

### Required New Photo Capture Task

Existing photos are enough for architecture and broad routing, but not enough for final order release. Add this as a P0 task before brake part payment or sample discard:

| Task | Capture required | Releases |
| --- | --- | --- |
| `BR-CAPTURE-001` brake order-release photo pack | Wide route photo first, then close-ups with label/ruler of front calipers, pad shape, rotor face, front hose ends/brackets, rear cable ends, equalizer, rear center hose ends, T/union, wheel-cylinder ports, hard-line flare nuts, clip positions, master/proportioning ports, and rear drum internals after opening. Lay removed cables and hard lines beside a tape measure and keep them as samples. | Front pads/hardware, front hoses, caliper kits/replacements, rear cables, rear hard-line fittings/flares, rear center hose, rear wheel cylinders, rear shoes/hardware, master/reservoir/proportioning parts. |

Do not discard old parking-brake cables, hard lines, flex hoses, or representative clips until the replacement parts have been checked against them.

### Most Relevant Rear-Axle Photos

| File | Use |
| --- | --- |
| [20260501_194305_gp_EllBGvXA.jpg](../photos/20260501_194305_gp_EllBGvXA.jpg) | Best rear axle route view for hard lines, cable/linkage routing, and drum area. |
| [20260501_194313_gp_lfUqLibA.jpg](../photos/20260501_194313_gp_lfUqLibA.jpg) | Best center/differential view for axle hard-line routing and center hose/T-union area. |
| [20260501_194322_gp_XuRtjN4w.jpg](../photos/20260501_194322_gp_XuRtjN4w.jpg) | Close rear drum/backing-plate view with cable/linkage context. |
| [20260324_004852.jpg](../photos/20260324_004852.jpg) | Earlier wide rear axle view showing axle lines and drum layout. |
| [20260324_004906.jpg](../photos/20260324_004906.jpg) | Earlier wide rear axle view confirming the same rear drum arrangement. |
| [20260324_004918.jpg](../photos/20260324_004918.jpg) | Wider rear axle/drum context before body-off cleaning. |
| [20260324_004921_gp_bHLJcrEw.jpg](../photos/20260324_004921_gp_bHLJcrEw.jpg) | Alternate wide rear axle/drum context. |
| [20260422_004254_gp_SplHLSYA.jpg](../photos/20260422_004254_gp_SplHLSYA.jpg) | Body-off rear axle/spring-hanger context. |
| [20260422_004257_gp_cxEZbZoQ.jpg](../photos/20260422_004257_gp_cxEZbZoQ.jpg) | Body-off rear axle and line-routing context. |
| [20260422_004301_gp_SU89hisw.jpg](../photos/20260422_004301_gp_SU89hisw.jpg) | Body-off rear axle/crossmember context. |

### What Can Be Removed Now

| Item | Remove now? | Conditions |
| --- | --- | --- |
| Rear parking-brake cables | Yes | Photograph both ends, label left/right, disconnect at equalizer and backing plates, keep old cables as length/end samples. |
| Rear axle hard brake lines | Yes, if the truck will not need brakes before rebuild | Photograph full route, label left/right, cap every open hydraulic port immediately, keep old tubes as bend templates. |
| Rear center flex hose | Yes, with the hard lines | Photograph both fittings, cap the system, and record bracket/clip style, free length, and fitted route before discard. |
| Corroded line/cable clips | Yes | Photograph/count positions first and keep one sample of each clip style. |
| Rear drums, shoes, wheel cylinders | Only after opening photos | Photograph both drums/backing plates internally before pulling springs, adjusters, shoes, or wheel cylinders. |

### Replacement Order List

| Priority | Replacement |
| --- | --- |
| P0 | Front disc pad and retaining hardware set after the fitted caliper/pad family is identified. |
| P0 | Front flex hoses after caliper-end, chassis-bracket, free length, and lock-to-lock clearance are confirmed. |
| P0 | Front caliper rebuild kits or replacement calipers if inspection finds leaks, seizure, torn boots, damaged pistons, or unknown unsafe condition. |
| P0 | Full brake/clutch hard-line stock: buy `4.75 mm / 3/16 in` brake/clutch-rated tube, `10000 mm` minimum if combining brake and clutch, `12000 mm` preferred for scrap flares and route correction. Existing controlled basis is `7600 mm / 25 ft` brake line plus `1500 mm` clutch blank. |
| P0 | New brake/clutch flare nuts and fittings after old fittings identify flare type, threads, and seats at master/proportioning, front hose brackets, rear hose/T-union, wheel cylinders, and clutch master/slave or clutch hose ends. Brake-line working basis after the May 14 installed-fitting and flare side-view photos is Toyota-style `double / inverted` flare; final release still comes from a straight-on removed sample and opened seat. |
| P0 | Rear axle brake T-union/splitter and any disturbed inline unions/splitters if corroded, seized, damaged, or mismatched; match thread, flare seat, port orientation, and mounting style from old samples. |
| P0 | New rear parking-brake cable set: left/right rear cables, equalizer/clevis hardware, return springs, clips, and adjuster parts matched to the backing plates. |
| P0 | Rear axle hard brake lines recreated in 3/16 in / 4.75 mm brake tube, with the correct flare and fitting threads. |
| P0 | Rear center flexible brake hose with correct chassis-side and axle-side fittings, retaining clip, and old-sample/free length. |
| P0 | Rear wheel cylinders as a pair once bore/port/mounting pattern is confirmed. |
| P0 | Full brake flex hose set: front left, front right, and rear center after front caliper fitting style, rear center fittings, bracket retention, and free length are captured. |
| P0 | Brake flex-hose retaining U-clips and bracket hardware for front left, front right, and rear center hose brackets. |
| P0 | Full line-support pack: rubber-lined P-clips for `4.75 mm` hard line, clamp-on rubber-lined axle supports, pass-through grommets/edge trim, M5/M6 fasteners, and larger cable saddles where parking-brake cables rub. |
| P0 | Clutch hydraulic flex hose assembly, clutch hard-line fittings, and clutch hard-line route release using the shared `4.75 mm / 3/16 in` hydraulic tube stock. |
| P0 | Clutch master/slave cylinders or rebuild kits if inspection finds leakage, pitting, seizure, bypassing, missing boots, or unknown unsafe condition. |
| P1 | Rear shoes, hold-down springs, return springs, adjuster hardware, and retaining clips after drum family and shoe dimensions are confirmed. |
| P1 | Brake-line clips, parking-brake cable retainers, rubber sleeves/grommets, and rubber-lined P-clips where originals are missing or corroded. |
| P1 | Front rotors: machine or replace after measured rotor thickness, scoring, runout, and service limit check. |
| P1 | Brake master cylinder, reservoir hoses/caps/seals, and proportioning/bias hardware only after the installed master/booster/proportioning layout is photographed and inspected. |
| P1 | Brake fluid, bleed hose/bottle, line caps/plugs, and brake cleaner/consumables for the full hydraulic closeout. |

### Parts Not To Blind-Order

| Item | Why held |
| --- | --- |
| Rear brake shoes and spring kit | Baseline replace, but exact set is held until drum family, shoe width/diameter, adjuster style, and spring layout are known. |
| Rear wheel cylinders | Baseline replace as a pair, but exact part is held until bore, port thread, mounting pattern, pushrod style, and bleed screw access are confirmed. |
| Front pads/caliper kits/rotors | Baseline service is approved, but the front disc conversion hardware family is not yet positively identified. |
| Rear parking-brake cables | Baseline replace with new cable assemblies, but cable length, sheath length, end fittings, equalizer hardware, and clip positions must come from the old samples. |
| Brake master cylinder | Master bore, booster/proportioning layout, reservoir condition, and fitting threads are not yet confirmed. |
| Brake conversion parts | Baseline plan is refresh first; no rear-disc conversion unless inspection or use shows a measured need. |

## Capture Requirements Before Ordering

Use this as the workshop handoff. The output should be photos plus measurements in `mm`, with old parts retained as samples until replacements are fitted.

| Area | Required capture | Blocks |
| --- | --- | --- |
| Rear parking-brake cables | Label left/right; photograph both ends before removal; measure overall cable length, sheath length, backing-plate end type, equalizer/intermediate end type, bracket/clip positions, adjuster thread size, and adjuster travel. Keep both old cables intact if possible. | Rear parking-brake cable set, equalizer hardware, clevises, clips, return springs. |
| Equalizer / intermediate linkage | Photograph the handle-to-equalizer/intermediate layout, clevis pins, return springs, adjuster, and cable attachment points. Record missing or seized parts. | Cable kit completeness and handbrake adjustment hardware. |
| Rear axle hard lines | Photograph full route before removal; label left/right; cap open ports; keep old tubes as bend templates; record tube OD, line length by side, flare standard, union thread, fitting seat, bend pattern, clip locations, and clearances to axle, U-bolts, shocks, springs, and tyres. | Rear axle hard-line fabrication and fittings. |
| Rear center flex hose | Photograph chassis-side and axle-side fittings, bracket slot, retaining clip, T/union, and route; measure hose free length, fitting/thread or banjo style, bracket retention, and fitted route clearance. | Rear center hose and full flex-hose set. |
| Rear drums open | Photograph each side before removing springs; record drum inside diameter, shoe width, lining condition, adjuster style, spring layout, backing-plate condition, parking-brake lever condition, and drum scoring/step. | Rear shoes, hardware kit, adjusters, drum machine/replace decision. |
| Rear wheel cylinders | Photograph installed cylinder and ports; after drum-open capture, record bore, mounting bolt spacing, port thread, pushrod/slot style, bleed screw size/access, and leak/seizure condition. | Wheel cylinder pair and bleed hardware. |
| Front disc hardware | Photograph both front calipers, rotors, hose ends, brackets, bleed screws, and any visible casting/part numbers; record pad shape, rotor thickness/diameter if accessible, caliper fitting type, hose free length, and steering lock clearance. | Front pads, caliper rebuild kits, front hoses, rotor decision. |
| Master/booster/proportioning | Photograph master cylinder, reservoir, booster/vacuum line, proportioning/bias valve if fitted, all ports, and hard-line routing; record fitting threads/flare seats and any leaks or seized fittings. | Master cylinder, reservoir seals/caps/hoses, brake balance decision. |
| Clips and retainers | Count every brake-line clip, parking-brake cable retainer, rubber sleeve/grommet, and P-clip by position; keep one sample of each style; record hole size, bracket thickness, and line/cable OD. | Clip order, P-clip pack, permanent line/cable support. |

## Release Gates

- Brake cables may be removed now after photos/labels, but old cables must remain the ordering samples.
- Hydraulic lines may be removed only if the truck does not need working brakes before rebuild; cap every open port immediately.
- Exact rear shoe and wheel-cylinder orders wait until internal drum photos and measurements are captured.
- Exact front pad, front hose, and caliper rebuild/replacement orders wait until the fitted front disc conversion hardware is identified.
- Brake flex hose order waits for fitting style, old-sample/free length, bracket retention, and fitted route confirmation.
- Final brake closeout requires pressure bleed, leak test, route/lock clearance check, even rear adjustment, parking brake hold/release test, and a short reinspection after bedding.

## Repo Information Already Pointing At Brake Work

- Chat note: `Brake master cylinder rebuild`
- Chat note: `front-disc conversion was already done I think?`
- Chat note: `Replace all fuel + brake lines`
- Master project plan: resolve the brake baseline before upgrades and treat the brake flexible hose set as a baseline must-replace item.
- Vehicle design spec: front disc brakes fit the `usable classic` direction.
- Existing chassis jobs already overlap brake scope:
  - `chassis_hard_lines_and_brackets`
  - `issue_brake_fuel_line_clip_corrosion`

## Parts And Procurement Signals Already In Repo

- `part_copper_grease`: already received
- `part_mech_brake_flex_hose_set`: purchase-ready and should stay in the baseline safety bucket
- `part_dot3_brake_fluid_autohub_6x354ml`: received from Autohub as 6 x 354 ml sealed DOT 3 brake fluid, 2124 ml total, order `62228`; reject opened/damaged bottles before use.
- `part_brake_fluid_bleed_consumables`: still purchase-ready for the remaining non-fitment hydraulic-opening consumables: line caps/plugs, catch bottle or bleeder kit, brake cleaner, rags, and catch tray. Clear bleed hose and nitrile gloves are received. Do not use DOT 5 or mix unknown old fluid.
- Existing estimate rows in `data/manual/workbook_tabs/parts.csv`:
  - `Brake master cylinder`: PKR `8,000-30,000`
  - `Wheel cylinders / caliper rebuild parts`: PKR `8,000-40,000`
  - `Flexible brake hoses`: PKR `5,000-15,000`
  - `Hard brake lines`: PKR `8,000-25,000`
  - `Brake shoes / pads`: PKR `6,000-25,000`
  - `Handbrake hardware / cables`: PKR `5,000-20,000`
  - `Reservoir hoses / caps / seals`: PKR `2,000-8,000`

## Current Recommended Direction

- Positively identify the front disc hardware already on the truck, then replace the normal front service items rather than trusting old unknown parts.
- Replace rear drum service parts, rear wheel cylinders, rear parking-brake cables, rear axle hard lines, and rear flex hose as part of the baseline rear axle package.
- Keep rear drums unless inspection or actual use shows a measured need for rear discs.
- Confirm master cylinder, flex hoses, hard lines, and brake-balance/proportioning setup before buying conversion parts.
- Replace the rear parking-brake cables and routine rear brake wear/hydraulic items while the rear axle area is stripped, but release exact parts only from the capture requirements above.
- Execute this during the Ironman suspension window using [suspension-brake-merged-work-plan.md](suspension-brake-merged-work-plan.md) as the combined parts/tools checklist.

## Open Unknowns To Close

- Exact front caliper and rotor family already fitted
- Master cylinder / booster / proportioning setup currently on the truck
- Condition of hard lines under clips and at bends
- Actual leakage or seizure state of front calipers and rear wheel cylinders
- Rear drum internal dimensions, shoe width, adjuster style, and spring layout
- Parking-brake cable end types, sheath lengths, equalizer hardware, and clip positions
- Brake flex hose fitting styles, free lengths, and fitted-route clearance
