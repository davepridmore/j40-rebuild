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
