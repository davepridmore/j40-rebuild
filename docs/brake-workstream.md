# Brake Workstream

## Scope

- Split brake work out from `steering_brakes_suspension` so hardware identification, hydraulic refresh, and conversion decisions stay explicit.
- Current working read: `front disc / rear drum`.
- Current default direction: refresh the existing system first and treat rear-disc conversion as optional only if inspection or real use shows a clear need.

## Current Configuration Read

| Area | Current read | Why it currently reads that way |
| --- | --- | --- |
| Front axle | Disc | One front underside photo appears to show a disc caliper, and the March 16 chat log says the front-disc conversion was already done. |
| Rear axle | Drum | Rear axle photos show drum/backing-plate style hardware and parking-brake linkage. |

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

## Rear Axle Cable / Line Replacement Track

UI requirements table source: [brake_system_requirements.csv](../data/manual/brake_system_requirements.csv).

The visible "wires" running to the rear brakes should be handled as brake safety hardware:
- parking-brake / handbrake cables and linkage to the rear drum backing plates
- rear axle hydraulic hard brake lines
- rear center frame-to-axle flexible brake hose
- line clips, cable retainers, and protective sleeves/grommets

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
| Rear center flex hose | Yes, with the hard lines | Photograph both fittings, cap the system, record bracket/clip style, and measure slack/full-droop relationship before discard. |
| Corroded line/cable clips | Yes | Photograph/count positions first and keep one sample of each clip style. |
| Rear drums, shoes, wheel cylinders | Only after opening photos | Photograph both drums/backing plates internally before pulling springs, adjusters, shoes, or wheel cylinders. |

### Replacement Order List

| Priority | Replacement |
| --- | --- |
| P0 | Rear parking-brake cable set: left/right rear cables, equalizer/clevis hardware, return springs, clips, and adjuster parts matched to the backing plates. |
| P0 | Rear axle hard brake lines recreated in 3/16 in / 4.75 mm brake tube, with the correct flare and fitting threads. |
| P0 | Rear center flexible brake hose with correct chassis-side and axle-side fittings, retaining clip, and full-droop slack. |
| P0 | Rear wheel cylinders as a pair once bore/port/mounting pattern is confirmed. |
| P1 | Rear shoes, hold-down springs, return springs, adjuster hardware, and retaining clips after drum family and shoe dimensions are confirmed. |
| P1 | Brake-line clips, parking-brake cable retainers, rubber sleeves/grommets, and rubber-lined P-clips where originals are missing or corroded. |

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
- Existing estimate rows in `data/manual/workbook_tabs/parts.csv`:
  - `Brake master cylinder`: PKR `8,000-30,000`
  - `Wheel cylinders / caliper rebuild parts`: PKR `8,000-40,000`
  - `Flexible brake hoses`: PKR `5,000-15,000`
  - `Hard brake lines`: PKR `8,000-25,000`
  - `Brake shoes / pads`: PKR `6,000-25,000`
  - `Handbrake hardware / cables`: PKR `5,000-20,000`
  - `Reservoir hoses / caps / seals`: PKR `2,000-8,000`

## Current Recommended Direction

- Positively identify the front disc hardware already on the truck.
- Rebuild or refresh front discs, rear drums, and hydraulics on condition.
- Keep rear drums unless inspection or actual use shows a measured need for rear discs.
- Confirm master cylinder, flex hoses, hard lines, and brake-balance/proportioning setup before buying conversion parts.

## Open Unknowns To Close

- Exact front caliper and rotor family already fitted
- Master cylinder / booster / proportioning setup currently on the truck
- Condition of hard lines under clips and at bends
- Actual leakage or seizure state of front calipers and rear wheel cylinders
