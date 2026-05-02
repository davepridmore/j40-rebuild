# Chassis Rubbers Workstream

Date: 2026-04-27

## Purpose

Lock the exact body-mount rubber system for the tub refit while the chassis is still exposed.

This workstream is for:
- the `6` main tub body mounts
- the separate `2` front support / nose-extension isolators
- the sleeves / crush tubes
- the cup washers / seat washers
- the flat shim pack
- the hardware class and repair contingency that control the rubber stack

This workstream is not for:
- door, windscreen, or vent rubbers
- suspension bushes
- engine or gearbox mounts

## Status

- Working basis is locked to the early pre-`1/79` `BJ40/FJ40` tub pattern.
- The exact numeric dimensions of the old samples are still open and must be captured with calipers before any local reproduction order is treated as closed.
- The stored photos below are the best current evidence of the original mount rubbers, but they are context-only and not measurement-grade.
- May 2 Google Photos picker import `20260502T013759` starts a dedicated selection set for rubber recreation: [rubber-recreation-photo-selection-20260502.md](rubber-recreation-photo-selection-20260502.md).
- May 2 fabricator handoff spec is now drafted from the tape-measure photos: [rubber-recreation-fabrication-spec-20260502.md](rubber-recreation-fabrication-spec-20260502.md).
- UI requirements table source: [chassis_rubber_requirements.csv](../data/manual/chassis_rubber_requirements.csv). This is the acquisition/fabrication status tracker for each rubber, sleeve, cup, shim, and hardware requirement.
- Consolidated rubber order source: [rubber_ordering_specs.csv](../data/manual/rubber_ordering_specs.csv) and [rubber-ordering-spec-20260502.md](rubber-ordering-spec-20260502.md). These control the buy-now, inspect-first, and defer gates across all rubber categories so chassis rubbers are not confused with weatherstrip, suspension, hose, or HVAC rubber.
- Body-mount release pack: [body_mount_order_release_specs.csv](../data/manual/body_mount_order_release_specs.csv), [body_mount_release_actions.csv](../data/manual/body_mount_release_actions.csv), [body_mount_station_closure_sheet.csv](../data/manual/body_mount_station_closure_sheet.csv), and [body-mount-order-release-plan-20260502.md](body-mount-order-release-plan-20260502.md). This is the order-line and user-action control for quantities, OE/reproduction candidates, local fabrication specs, shims, sleeves, and bolts.
- Toyota OE/EPC-style control rows are now captured in [rubber_recreation_toyota_oe_cross_reference.csv](../data/manual/rubber_recreation_toyota_oe_cross_reference.csv). They confirm part numbers, station IDs, bolt families, and several shim/spacer thicknesses, but not rubber cushion OD/ID/free-height.
- Aftermarket thickness cross-checks and the final caliper closure sheet are now captured in [rubber_recreation_aftermarket_dimension_crosscheck.csv](../data/manual/rubber_recreation_aftermarket_dimension_crosscheck.csv) and [rubber_recreation_measurement_closure.csv](../data/manual/rubber_recreation_measurement_closure.csv).

## Original Rubber Evidence

![Original tub-side body-mount rubber context](/Users/davidpridmore/IdeaProjects/J40/photos/20260405_234652.jpg)

Caption:
- Best current photo of an original body-mount rubber still in the tub/chassis interface.
- Useful to show the general rubber shape, seating style, and deterioration context.
- Not good enough to read exact OD, sleeve size, or thickness.

![Original underbody mount and rubber context](/Users/davidpridmore/IdeaProjects/J40/photos/20260405_234546.jpg)

Caption:
- Best current underside photo showing the mount stack area and old rubber context from below.
- Useful to explain seat geometry and why the metal landing surfaces matter.
- Not good enough to replace sample-based measurement.

Evidence note:
- These are the best current stored photos of the original body-mount rubbers in this repo.
- If the removed old rubbers are found, add isolated daylight photos of:
  - large main-tub piece
  - small main-tub piece
  - sleeve
  - front support isolator

## Locked System Split

| System | Locked Pattern | Positions | Rule |
| --- | --- | ---: | --- |
| Main tub body mounts | Pre-`1/79` early `BJ40/FJ40` | `6` | One matched set only |
| Main tub large cushion family | Early `BJ40/FJ40` large type | `2` pieces | Do not buy late-pattern pieces |
| Main tub small cushion family | Early `BJ40/FJ40` small type | `10` pieces | Do not mix with random local leftovers |
| Front support isolators | Separate front support / radiator-grille support pattern | `2` positions | Separate from the six main tub mounts |

## Exact Spec Table

| Part | Qty / Positions | Exact Spec Required | Condition / Material Rule | Measurement Gate |
| --- | ---: | --- | --- | --- |
| Main tub large cushions | `2` pieces | Early pre-`1/79` `BJ40/FJ40` large body-mount pattern | `NEW_ONLY`; matched pair; same maker and hardness | Match old large sample OD, thickness, center bore, and installed stack |
| Main tub small cushions | `10` pieces | Early pre-`1/79` `BJ40/FJ40` small body-mount pattern | `NEW_ONLY`; matched set; same maker and hardness | Match old small sample OD, thickness, center bore, and installed stack |
| Main tub sleeves / crush tubes | `6` minimum | Steel sleeves matched to the main tub mount stack | New steel only; no mixed worn sleeves | Sleeve ID must match bolt, sleeve OD must match rubber bore, sleeve length must stop over-crush |
| Main tub cup washers / seat washers | `12` | Heavy upper/lower mount cups or equivalent seat washers | Matched seat style; do not use thin generic washers | Must seat the rubber fully and match the body/pedestal landing area |
| Main tub hardware | `6` installed, buy `8` | `M10 x 1.25`, class `8.8` minimum | Marked structural hardware only | Final bolt length by station still needs physical measurement |
| Main tub shim pack | `1` assorted pack | Flat steel shims `1 mm`, `2 mm`, `3 mm`, `5 mm` | Steel only; no random washer towers | `M10` ID for the tub rows; keep some `M12` option available for front support or prior repair |
| Front support isolators / pads | `2` positions | Separate front support rubber/pad set for the nose side extensions | `NEW_ONLY`; keep left/right as matched pair | Must match the front support sample style and installed height; do not assume tub rubbers fit |
| Front support shims / pads | `2` | Separate shim/pad pieces to suit the front support pair | Flat and stable; not improvised stacks | Must align front clip height without forcing the tub |
| Captive-thread repair pack | `2` nuts + `2` tabs minimum | `M10 x 1.25` weld nuts / repair nuts plus `3 mm` steel repair tabs | New repair material only | Use only if cleaning shows damaged threads or weak pedestal repair metal |
| OE station map | `1` reconciliation sheet | Toyota `NO.1` to `NO.5` body-mount rows against vehicle-side positions | Must agree with physical samples before production | Use the OE cross-reference plus direct vehicle labels; do not infer from catalog alone |
| Exact release measurements | `1` closure sheet | Final OD, height, bore/register, sleeve, cup, and split-stack fields | Caliper-locked before production | Use `rubber_recreation_measurement_closure.csv`; photos are quote/prototype evidence only |

## Exact Measurement Fields To Capture From Sample

Fill this in from the removed old parts before any local fabrication order is treated as final.

| Measurement Field | Large Main Cushion | Small Main Cushion | Front Support Isolator |
| --- | --- | --- | --- |
| Sleeve ID | `___ mm` | `___ mm` | `___ mm` |
| Sleeve OD | `___ mm` | `___ mm` | `___ mm` |
| Sleeve length | `___ mm` | `___ mm` | `___ mm` |
| Rubber OD | `___ mm` | `___ mm` | `___ mm` |
| Rubber thickness | `___ mm` | `___ mm` | `___ mm` |
| Total installed stack height | `___ mm` | `___ mm` | `___ mm` |

## Acceptance Rules

- Keep one old mount sample with sleeve in hand when buying or reproducing locally.
- Rubber hardness must stay consistent across the full set.
- Total stack height must preserve OEM body height; this is not a body lift.
- Reuse original shims only if they remain flat and rust-free.
- New shims go only at the original metal-to-metal shim interface.
- Do not put shims inside the rubber sandwich.
- Do not mix one side rubber and the other side polyurethane.
- Do not use random washer stacks as height spacers.
- Do not mix the separate front-support rubbers into the six main tub stations.

## Immediate Actions

1. Find and lay out any removed old mount rubbers and sleeves by station.
2. Measure one large sample, one small sample, and one front support sample.
3. Confirm actual thread pitch and final bolt length at each main tub station.
4. Preserve original shim packs by `FL`, `FR`, `ML`, `MR`, `RL`, `RR`.
5. Only then close the order with Bilal Ganj or a local rubber fabricator.
6. Use the May 2 fabrication spec as the quote/prototype sheet, then close its hold dimensions with calipers before production.
7. Reconcile the physical vehicle stations against Toyota `NO.1` to `NO.5` rows before changing the rubber count or approving production.
8. Confirm whether the small circular mounts are one-piece `22 mm` stack-equivalent cushions or a split medium-bushing plus seat stack before asking the fabricator to cut final pieces.
9. Use the consolidated rubber ordering matrix to keep body mounts, suspension bushes, hoses, weatherstrip, and HVAC rubber in their correct order gates.
10. Complete the open `BMA-*` actions in `body_mount_release_actions.csv`; anything not blocked there can be quoted or ordered from `body_mount_order_release_specs.csv`.
