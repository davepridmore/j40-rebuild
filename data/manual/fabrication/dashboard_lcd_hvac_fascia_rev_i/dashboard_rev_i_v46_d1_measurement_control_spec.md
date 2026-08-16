# Dashboard centre insert — V46-D1 measurement control

Status: **measurement release only — not a production/CNC release**

Drawing: `dashboard_rev_i_v46_d1_component_package_1to1.svg`

Schedule: `dashboard_rev_i_v46_d1_component_dimension_schedule.csv`

## What D1 establishes

The A1 SVG is physically authored at **841 × 594 mm** with a **1:1** drawing scale. It fixes only the component envelopes that can be traced to a manufacturer source:

- Pioneer DMH-AP6650BT front/nose envelope: **229 × 131 × 13 mm**.
- Pioneer chassis envelope: **188 × 108 × 37 mm**.
- Pioneer effective display area: **196.608 × 114.15 mm**. It is drawn separately because its offset from the nose edges is not published.
- Four Schneider Harmony XB4BD21 selector switches: published overall envelope **30 W × 47 H × 68 D mm** and nominal mounting diameter **22.5 mm**.
- Three Schneider Harmony XB4BJ33 selector switches: published overall envelope **30 W × 48 H × 68 D mm** and nominal mounting diameter **22.5 mm**.

The drawing does **not** turn a catalogue envelope into a fabricated profile. Corner radii, mounting-hole coordinates, anti-rotation details, connector sweeps and received-part tolerances remain direct-measurement items.

## Known purchase with no exact model-controlled geometry

The separate red hazard control is documented only as a generic latching illuminated 12 V pushbutton in the 16 mm class. Its catalogue-style description is not sufficient to release a hole. Measure the received button's:

1. threaded body and required bore;
2. any anti-rotation flat or notch;
3. bezel diameter and front projection;
4. rear body, terminals and wire-bend envelope;
5. usable panel-thickness / retaining-nut range.

## Why an exact panel perimeter is not yet on D1

The available dashboard photographs have no trustworthy paired horizontal and vertical scale datums. They show shape and adjacency, but cannot establish an exact common coordinate system. The new panel perimeter must therefore come from the vehicle, not from pixel scaling.

The retained design constraints remain:

- panel between the retained glovebox and speedometer;
- both top corners rounded consistently with those adjacent openings;
- screen recessed so its front is flush with the finished panel plane;
- lower edge closes against the **existing straight factory dashboard bottom line**;
- **zero downward dashboard extension**;
- visual balance left and right, subject to the real retained-edge geometry.

## Physical measurement gates

| Gate | Measurement | Method / output |
|---|---|---|
| M1 | Fascia and common dashboard X/Y datum | Establish perpendicular baselines; trace the top fold, lower edge, centre opening, surviving attachment structure and free centre field. |
| M2 | Glovebox and full centre-section boundary | Trace the retained glovebox, left seam, both upper tangent radii, unchanged factory bottom line, ashtray/opening removal and usable flange. |
| M3 | Speedometer / cluster / column | Trace the right termination, cluster package, installed column axis, scallop and swept clearances. |
| M4/M5 | Pioneer receiver and installed site | Caliper W/H/D and corner radii; locate rear screws; map site depth, plugs, loom, bend radii, ventilation and removal path. |
| M6 | Received controls | Caliper all seven selectors and hazard; make drilling coupons; confirm anti-rotation, rear stacks and service access. |
| M7 | Outer outlets | If retained in the broader fascia scheme, measure their visible and rear interfaces; they remain outside the centre insert. |
| M8 | HVAC package | Measure the case, fittings, drain, branches and complete service envelope behind the dashboard. |
| M9 | Panel stack and full-depth trial | Fix material, recess, trim gap, fasteners and inserts, then fit a rigid full-depth buck through wiring and service-removal sweeps. |
| M10 | Post-fit commissioning | Complete the electrical and functional tests after installation; this gate does not release fabrication geometry. |

All M1–M9 gates must close before a production perimeter, screen aperture, control centres or mounting holes are released. M10 closes post-fit commissioning.

## Recommended measurement sheet

Use the lower left of the glovebox-adjacent edge as the provisional origin only after it is physically marked on the vehicle. Record at minimum:

- four or more points on the factory straight lower line;
- tangent points and radii at both upper corners;
- minimum clear distance to the glovebox and speedometer edges;
- ashtray/opening polygon and available attachment flange;
- Pioneer nose and chassis positions relative to the panel plane;
- all eight control centres and rear-clearance readings;
- fastener centres, edge distances and tool access.

Do not use the old 1400 × 250 dashboard placeholder, 350 × 210 cassette envelope, 202 × 115 trial aperture or 40 mm control pitch as production dimensions. The 40 mm row on D1 is an arrangement study only.

## Print and verification

1. Export or print the SVG at **100% / Actual size**. Disable “fit to page”.
2. Measure the printed 100 × 100 mm calibration square in X and Y.
3. Reject the print if either axis differs by more than **0.25 mm**.
4. Use the print only for component/package comparison. It is explicitly marked **NOT FOR CUTTING**.

## Manufacturer sources

- [Pioneer DMH-AP6650BT operation manual](https://pioneer-mea.com/wp-content/uploads/2025/07/OPM_DMHAP6650BTGS_EG.pdf)
- [Pioneer DMH-AP6650BT quick-start / installation guide](https://www.pioneer.com.au/wp-content/uploads/2024/12/DMHAP6650BT-Quick-Start-Guide.pdf)
- [Schneider Harmony XB4BD21 official product data](https://eshop.se.com/sg/selector-switch-harmony-xb4-metal-black-22mm-2-positions-stay-put-1no-xb4bd21.html)
- [Schneider Harmony XB4BJ33 official product data](https://eshop.se.com/sg/selector-switch-harmony-xb4-metal-black-22mm-long-handle-3positions-stay-put-2no-xb4bj33.html)
