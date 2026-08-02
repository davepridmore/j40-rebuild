# Rev I V35 — Ø87 outlet CNC quotation and fit-coupon addendum

Issue date: 2026-08-02
Release state: **quotation, measurement drawing and fit coupon only; production fascia and vehicle cutting HOLD**

## Scope

This addendum updates the selected original-height J40 dashboard arrangement for exactly two matching circular A/C outlets. It does not change the retained original glovebox, original speedometer/cluster, factory RHD steering-column axis or scallop, central LCD location, seven-selector-plus-hazard allocation, fascia top edge or normal lower edge.

Use the [V35 registered overlay](dashboard_rev_i_v35_registered_center_cassette_overlay.png) and [scale-controlled front elevation](dashboard_rev_i_v35_provisional_front_elevation.svg) only as front-view appearance and quotation references. Use the signed 1:1 vehicle trace, the received components and successful fit coupons as the CAD masters; never scale production coordinates from the raster image.

## Controlled design inputs

| Part/interface | Design input | Status |
| --- | ---: | --- |
| LCD diagonal | 228.6 mm / 9.000 in | Nominal |
| LCD module outline | 211.10 W × 126.50 H × 5.0 D mm | Provisional; verify bought part |
| LCD active image | 198.91 W × 111.89 H mm | Provisional; verify bought part |
| LCD complete installed rear projection | 115 mm maximum for quotation/buck; chassis/body target ≤80 mm | `ASSUMED_UNVERIFIED`; not a production maximum |
| Outlet visible face | Ø87.0 mm target | Controls V35 front-face proportion |
| Outlet rear mounting boss/barrel | Ø75.0 mm target maximum | Verify every received part; not a released hole size |
| Outlet louver-body depth | ≤ approximately 22 mm | Datum is finished rear fascia plane to rear of louver body |
| Outlet retainer/spigot/clamp/first bend | To be measured separately | Not included in the 22 mm body figure |
| Fascia material | 1.5 mm CR4 mild steel | Production intent; coupon must match |
| Finish | Deburred, primed and body-colour low gloss | Coupon must include representative finish build |

`Ø75 mm rear mounting` is not a duct or hose diameter. Record the separate spigot OD, spigot ID, projection, retaining bead and usable hose engagement before specifying an adapter or hose.

## Layout rules for CAD

1. Establish `X0/Y0` and the complete outer profile from the signed perpendicular 1:1 vehicle trace. Preserve the factory top edge, both ends and normal lower edge.
2. Preserve the directly traced OEM glovebox aperture and complete opening sweep. Preserve the complete cluster aperture and the factory steering-column scallop on the installed steering axis.
3. Centre the bought LCD's measured **active image** in the signed unobstructed centre field between the retained glovebox and cluster/column zones. Do not centre the complete fascia or centre the chassis/bezel in place of the active image.
4. Use two outlet centres, `V1` passenger-side and `V2` driver-side, on exactly one common horizontal datum: `Y_V1 = Y_V2`.
5. Place the two Ø87 faces at the measured midpoints of their available retained outer lands, on the common high datum shown in V35. Determine both physical centres only after the signed face trace and full-depth mock-up; do not derive them from the image. Keep each face wholly on fixed fascia and outside the glovebox lid, cluster, LCD, switch bank, ashtray closure and steering-column relief. If the complete rear package conflicts, reposition within approved fixed land rather than moving an OEM assembly, lowering the fascia or crushing a duct.
6. Where the visible Ø87 face and a 10 mm visible gap control, maintain centre-to-boundary distance ≥53.5 mm. Where only a conditional Ø75.5 coupon aperture and 10 mm structural land control, maintain centre-to-boundary distance ≥47.75 mm. Apply the stricter rule wherever both apply.
7. Maintain ≥10 mm verified three-dimensional service clearance from the complete outlet retainer/spigot/clamp/first-bend package to the LCD, glovebox hardware and sweep, cluster, switch contact stacks, terminals, loom and retained structure.
8. Maintain ≥20 mm from all new fixed parts, ducts and wiring to the signed moving column/shroud/stalk envelope through full movement.
9. Do not lower the dashboard or add a vent pod, dip, lower extension, central vent or third visible outlet to obtain clearance.

## 2026-08-02 rear-clearance photo result

The picker import provides useful cavity context, but it does not release either vent or the LCD for production. Two oblique, unregistered tape rays read approximately 125–130 mm and 160–170 mm. The third shows a 270–280 mm endpoint reading, not a span, because its tape zero/start is outside the frame. None identifies the planned V1 or V2 centre or measures perpendicular from the finished rear fascia.

- The approximately 22 mm louver body is **provisionally plausible / not contradicted** by the photographed local cavity.
- The complete outlet package—retainer, anti-rotation hardware, spigot, clamp, hose, first bend, support, moving louver envelope and removal path—is **NOT PROVEN**.
- The LCD quotation buck may use `P_LCD_INSTALLED,Q ≤ 115 mm`, with a chassis/body target `≤80 mm`. These are `ASSUMED_UNVERIFIED`; the supplied 5.0 mm module thickness is not installed depth.

At each marked actual vent centre, establish local `Z=0` on the finished rear fascia, map the closest fixed obstruction across the full rear swept envelope, measure the complete actual assembly, and require:

`P_VENT_INSTALLED ≤ min[Z_FIXED(x,y)] − 10 mm`.

For the LCD, apply the same rule to the complete chassis/carrier/cooling/fastener/plug/cable/service/removal envelope:

`P_LCD_INSTALLED,PROD ≤ min[Z_FIXED(x,y)] − 10 mm`.

Both installations must also remain at least 20 mm from the signed moving steering-column/shroud/stalk envelope. See the [photo audit](rear_clearance_photo_audit_20260802.md), [evidence schedule](rear_clearance_photo_evidence_20260802.csv) and [rear-package control diagram](rear_package_clearance_control.svg).

## Fit-coupon instruction

Do not infer the production aperture directly from Ø75.0 mm. First photograph, label and measure all four ordered outlets at multiple clock and axial positions. Record maximum/minimum boss diameter and ovality, retention method, anti-rotation feature and representative paint build.

If and only if the measured maximum boss is ≤75.00 mm and the part is a slip-through design with a separate rear retainer, quote the first trial coupon as:

- `D_CUT = Ø75.50 mm +0.25 / −0.00`
- coupon material: 1.5 mm CR4 mild steel
- coupon finish: production-equivalent deburr, edge preparation, primer and paint
- surrounding flat land: sufficient to reproduce the tighter installed boundary; minimum 20 mm from aperture edge unless the signed vehicle geometry is tighter

Snap, interference, threaded or clip-retained parts use the component maker's requirement or a physically proven coupon size instead. The accepted coupon must prove insertion, positive retention, anti-rotation, aiming/shutoff operation, no finish damage, cabin-side removal and no rattle before `D_CUT` is released.

## Drawing layers and dimensions requested from CNC supplier

- `CUT_OUTER`: signed fascia outer profile and factory column scallop
- `CUT_OEM`: directly traced cluster and glovebox apertures
- `CUT_LCD`: bought-LCD cutout and mounting features after M4/M5
- `CUT_VENT`: accepted coupon-derived apertures `V1` and `V2` after M7
- `CUT_CONTROL`: seven measured selector apertures plus separate hazard
- `ETCH_LABEL`: WIPERS, LIGHTS, SPOTS, AUX, BLOWER, A/C, FUEL STOP, HAZARD in one line
- `BEND`: signed folds/returns and bend direction
- `DATUM`: fascia centre, installed steering axis and common outlet centreline
- `NO_CUT`: retained structure, glovebox sweep, column swept envelope and service exclusions

Quote targets unless the component drawing requires tighter control: cut-feature position ±0.50 mm, accepted cut-feature size ±0.25 mm, and formed outer silhouette ±2.0 mm against the signed checking template. Supplier must state achievable tolerances and bend allowance before acceptance.

## Release evidence

Production `CUT_VENT` remains HOLD until the owner/body shop signs:

- received-part M7 inspection and selected matched pair;
- successful final-finish outlet coupon;
- perpendicular available-depth maps at the two actual vent centres and over the complete LCD installed/service envelope;
- measured complete installed projection of both selected vent assemblies and the actual LCD assembly;
- full-depth mock-up including retainer, spigot, clamp, first bend and supported hose;
- full glovebox opening/closing sweep;
- switch terminal and loom clearance;
- balanced airflow test with both complete duct branches attached; and
- preserved original or dedicated windscreen-demist path.
