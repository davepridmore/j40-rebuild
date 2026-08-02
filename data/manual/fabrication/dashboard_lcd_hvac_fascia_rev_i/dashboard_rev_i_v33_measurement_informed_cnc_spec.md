# J40 dashboard Rev I V33 — measurement-informed CNC quotation specification

Revision: **V33-Q1**
Units: **millimetres**
Production state: **HOLD — quotation, 1:1 disposable template, depth buck and coupons only**

V33 applies the 2026-08-02 measurement-photo batch without converting perspective estimates into false CNC dimensions. It retains the selected V32 layout, applies the supplied new-component sizes, and makes every unresolved vehicle feature a mandatory 1:1 trace. This document is suitable for supplier quotation and prototype planning. It is not permission to cut the vehicle or production metal.

## What the new photographs changed

- The visible `1400 × 250` front-face envelope remains a quotation assumption. The photos make a roughly `250–260` mm visible front region plausible, but do not show two named, perpendicular, in-frame datums. The deeper outer/end shell can appear near `390` mm and must not be substituted for dashboard face height.
- The original asymmetric glovebox, side/end returns, mount structure, and steering/cluster relationship are reinforced as direct-trace features.
- Rear brackets, linkage, wiring and irregular cavity depth are now explicit collision evidence. No behind-dash package is considered clear until the full-depth mock-up passes.
- No LCD, outlet, selector, glovebox, cluster or column coordinate changed from V32 because the photographs do not support such a change.

The photo-by-photo audit is `dashboard_rev_i_v33_measurement_evidence.csv`.

## Design intent — locked

- Replace the complete visible fascia while retaining the factory-height top and normal lower edge from a signed vehicle trace. No full-width downward extension.
- Preserve the original Toyota speedometer, its low position immediately above the factory RHD column, the steering-axis position and the complete U/scallop profile.
- Preserve the original asymmetric Toyota glovebox exactly, including its position, outline, hardware, plate, knob, aperture and opening sweep.
- Delete the separate ashtray and close its recorded aperture with uninterrupted body-colour fascia.
- Centre the **active image**, not merely the bezel, of one true 9-inch LCD on the complete traced fascia midpoint.
- Use exactly two matching chrome/silver circular outlets, one at each outer fixed region, on a common high horizontal datum.
- Use exactly seven black industrial selectors and one separate red hazard control in the compact far-right `4 × 2` bank.

## Geometry authority

| Class | Authority | Production use |
| --- | --- | --- |
| `VEHICLE_TRACE_LOCK` | Signed 1:1 trace/scan of the actual vehicle | May be released only after M1–M3 signoff |
| `OWNER_SUPPLIED_COMPONENT` | Supplied nominal component figure | Confirm actual bought unit before cutting |
| `ASSUMED_QUOTATION` | Costing/layout placeholder | Never use for production cutting |
| `COUPON_CANDIDATE` | Trial geometry in final sheet/finish | Coupon only until fit and retention pass |
| `PHOTO_EVIDENCE_ONLY` | Visual shape, obstruction or plausibility evidence | Never a CNC coordinate |

## Coordinate frame and quotation envelope

- Origin `(0,0,0)`: top-left of the provisional finished visible face.
- `X`: passenger to driver on this RHD vehicle. `Y`: downward. `Z`: rearward.
- `W_FACE = 1400`, `H_FACE = 250`, vendor depth envelope `100`: **ASSUMED_QUOTATION**.
- `H_FACE = 250` means only the visible front-fascia envelope. It is not the complete dashboard/end-shell height.
- Replace the 1400 × 250 R18 placeholder, top/lower/end returns, mounting holes and vehicle-cut boundary with M1 data before a production revision.
- Quotation material: 1.5 mm CR4 mild steel, deburred, primed and body-colour low-gloss finish. Actual sheet, bend allowance and returns require the traced vehicle and supplier process.

## Purchased-component geometry and selected quotation coordinates

The machine-readable schedule is `dashboard_rev_i_v33_measurement_informed_coordinates.csv` and the exact-scale front sheet is `dashboard_rev_i_v33_scale_front_elevation.svg`.

| Feature | Size | Provisional centre | Status |
| --- | ---: | ---: | --- |
| LCD module | `211.10 × 126.50 × 5.0` | `(700.0, 125.0)` | supplied nominal; M4/M5 HOLD |
| LCD active image | `198.91 × 111.89`; diagonal `228.6` | `(700.0, 125.0)` | supplied nominal; M4 HOLD |
| LCD visible opening | `202.0 × 115.0`, R3 | `(700.0, 125.0)` | assumed; do not production-cut |
| Passenger outlet face | `Ø87.0` | `(135.0, 70.0)` | supplied target + assumed centre; M1/M7/M9 HOLD |
| Driver outlet face | `Ø87.0` | `(1265.0, 70.0)` | supplied target + assumed centre; M1/M7/M9 HOLD |
| Candidate outlet coupon | `Ø75.50 +0.25 / −0.00` | same centres | coupon only if boss `≤Ø75.00` and back retention is proven |
| Selector cut placeholder | `Ø22.5`; head `Ø30` assumed | X `1060/1110/1160/1210`; Y `137.5/190.0` | M6 HOLD |

Exact scale relationships under the quotation envelope:

- LCD module width = `15.079%` of face width.
- LCD module height = `50.600%` of face height.
- Each outlet face diameter = `6.214%` of face width and `34.800%` of face height.
- LCD module width / outlet diameter = `2.4264`.
- Provisional selector-head diameter = `2.143%` of face width.

These percentages govern the exact-scale SVG, not the photorealistic PNG. Generative imagery is presentation evidence only.

## OEM trace locks

The CNC supplier must import, without repositioning, redrawing or symmetrising:

1. complete visible fascia perimeter, top and lower edges, both end returns, form lines and every mount;
2. glovebox lid, aperture, hinges, latch, knob, plate, rear box and full opening/removal sweep;
3. speedometer bezel/aperture, mounts, rear case, connectors and service path;
4. steering shaft centre and angle, complete factory U/scallop, shroud, boss, wheel and stalk swept envelope;
5. ashtray aperture and supports before closing it flush.

The V33 PNG and SVG do not define these OEM profiles. The signed M1–M3 trace does.

## Outlet and duct release rules

- Inspect all four ordered vents and choose the closest-matched pair; bag the other two as service spares.
- Measure visible OD, boss/barrel OD at multiple clocks and depths, ovality, retainer, anti-rotation, rear body, spigot, hose engagement, clamp land, first elbow and complete rear projection.
- `Ø87 / Ø75 / approximately 22` are target-family figures, not proof of the ordered SKU.
- Quote three `120 × 120` coupons in final 1.5 mm sheet/finish at `Ø75.25`, `Ø75.50` and `Ø75.75`, but only if receipt inspection confirms a slip-through boss near Ø75.
- Maintain at least 10 mm between each complete fixed vent/duct package and glovebox, LCD, cluster, selectors, loom, brackets and returns; maintain at least 20 mm to the moving column/shroud/stalk envelope.
- Keep both outlets wholly on fixed fascia. If a rear clash occurs, move the affected outlet outward only within signed fixed land; do not move an OEM assembly, lower the normal dashboard edge or crush a duct.
- Support both branches and retain a separate demist route. No round duct may be crushed below 90% of its nominal inside diameter.

## Control allocation and electrical boundary

| Position | Control | Positions | Function |
| --- | --- | --- | --- |
| Top 1 | WIPERS | 3 | OFF / LOW / HIGH request with park logic |
| Top 2 | LIGHTS | 3 | OFF / SIDE / HEAD request |
| Top 3 | SPOTS | 2 | OFF / ON fused relay request |
| Top 4 | AUX | 2 | OFF / ON fused auxiliary request |
| Bottom 1 | BLOWER | 3 | OFF / LOW / HIGH controller request |
| Bottom 2 | A/C | 2 | OFF / ON request through thermostat, pressure and airflow safeties |
| Bottom 3 | FUEL STOP | 2 | RUN / STOP low-current request; key OFF and manual cable retained |
| Bottom 4 | HAZARD | separate red control | Independent hazard request |

The inventory is exact: four 2-position selectors plus three 3-position selectors. All seven are allocated. No motor, lamp, compressor-clutch or fuel-solenoid load passes directly through a fascia selector.

## Mandatory rear-package proof

Before production release, build a rigid full-depth buck containing the actual LCD/carrier/connectors, both complete vent-retainer-spigot-elbow-duct assemblies, glovebox box/sweep, cluster rear body, all selector contact stacks/terminals/loom, actual evaporator/takeoffs/drain/demist, and the complete steering moving envelope. Test cabin-side removal and service access.

The 2026-08-02 photos show rear obstructions but provide no perpendicular depth dimension. They therefore strengthen this hold rather than close it.

## Required field measurements for the production revision

1. **M1 fascia:** perpendicular 1:1 trace/scan of perimeter, height at at least five X stations, form/return geometry, mounts, no-cut structure and signed vehicle-cut boundary.
2. **M2 glovebox/ashtray:** exact glovebox lid and aperture profiles, hardware coordinates, depth and sweep; separately trace the ashtray removal/closure.
3. **M3 cluster/column:** cluster profiles and rear package; installed shaft X/Y/Z and angles; U/scallop; shroud/stalk/boss/wheel sweep.
4. **M4/M5 LCD:** part number, controlled drawing or actual calipers, active-image offsets, aperture/bezel, carrier, connector/cable bend, heat and removal path.
5. **M6 controls:** each actual control/hazard cut, key, clamped range, head/lever sweep, contact stack, terminals, labels and continuity truth table.
6. **M7 outlets:** all-four-part inspection, retention proof, spigot/duct interface and final-finish coupon.
7. **M8 HVAC:** actual case, fittings, takeoffs, drain, intake, demist and both complete duct routes.
8. **M9/M10:** full-size face template, full-depth buck, clearance/operation checks, airflow/drain/electrical tests and owner/body-shop signatures.

Every measurement photograph must show a named datum with tape zero hooked to it, the second endpoint in the same frame, a planar/perpendicular tape, and an identifying wide shot.

## Quotation deliverables and tolerances

- Quote separately: trace digitisation; 1:1 MDF/card/plastic face template; full-depth rigid buck; outlet coupons; one unpainted first article; production panel after written release.
- Supply 1:1 millimetre DXF plus dimensioned PDF with overall extents and revision. Layers: `TRACE_LOCK`, `NEW_CUTS`, `FORM_LINES`, `KEEP_OUT`, `ASSUMED_QUOTE_ONLY`, `INSPECTION`.
- Quotation targets, unless an actual part requires tighter: cut position ±0.5, cut size ±0.25 and formed silhouette ±2 against the signed checking template. Supplier must state capability.
- The production revision must replace every `ASSUMED_QUOTATION`, confirm every bought part, and import every `VEHICLE_TRACE_LOCK` item before release.

## Verdict

- **Layout and component-ratio design:** PASS for quotation and owner review.
- **Measurement-photo incorporation:** PASS; evidence recorded without false coordinates.
- **Exact vehicle geometry and rear fit:** HOLD at M1–M9.
- **Production CNC / vehicle cutting:** HOLD.
