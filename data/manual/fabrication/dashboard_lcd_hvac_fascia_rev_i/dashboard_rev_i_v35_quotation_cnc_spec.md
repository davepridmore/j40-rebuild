# J40 dashboard Rev I V35 — quotation-only centre cassette CNC brief

**Release state: PRODUCTION HOLD.** V35 is a quotation, 1:1 paper-template and full-depth-buck brief only. It is not authority to cut the vehicle, machine production sheet, or order a production aperture programme.

## Locked design intent

- Preserve the OEM glovebox, speedometer/cluster aperture and mounting relationship, RHD steering-column scallop, full-width lower edge, and all existing formed outer/end contours unchanged.
- Preserve the existing perpendicular glovebox-to-local-lower-edge gap (`G1`) and the complete cluster/lower-lip/column-scallop relationship (`C1`) from direct vehicle traces. Photo perspective must not be converted into different left- and right-hand face heights or offsets.
- Replace only the traced ashtray/centre-area opening with one removable centre cassette. It must not become a full-width replacement panel.
- Default cassette downward extension is **0 mm**: its lower edge remains above the existing full-width lower edge. A later extension, if measurements make one necessary, is centre-only, no larger than the measured shortfall, and needs written owner approval after the physical survey. It must never alter the lower edge or either end contour.
- There are exactly two outer vents, one passenger-side and one driver-side. No centre vents and no additional vent holes are included.

The [V35 photorealistic dashboard](dashboard_rev_i_v35_photorealistic_corrected_outer_vents.png) is an appearance preview only. Do not scale, trace or derive any CNC coordinate from the raster image. The photo-registered concept is [dashboard_rev_i_v35_registered_center_cassette_overlay.svg](dashboard_rev_i_v35_registered_center_cassette_overlay.svg); it is a registration aid, not production geometry. The scale-controlled provisional front elevation is [dashboard_rev_i_v35_provisional_front_elevation.svg](dashboard_rev_i_v35_provisional_front_elevation.svg), with the matching [coordinate schedule](dashboard_rev_i_v35_provisional_coordinates.csv). Production geometry authority remains the signed M1–M9 vehicle/component evidence and resulting released DXF/PDF; M10 is the post-fit electrical/functional commissioning gate before vehicle handoff.

## Datum and provisional coordinate model

All V35 coordinates are in millimetres. `X` runs **passenger to driver** (left to right in the RHD front elevation); `Y` runs down; the front-layout model uses `Z` rearward from the finished front face. For component-depth inspection, establish a separate local `Z=0` on the **finished rear fascia surface** at the component and measure perpendicular to that surface. Do not mix these two Z origins. The coordinate model is photo-informed and quotation-only:

| Datum / field | Provisional value | Meaning and restriction |
| --- | ---: | --- |
| Quotation face envelope | 1400 W × 250 H | A plotting envelope only; it is not the vehicle perimeter or a cut profile. |
| Free centre field | X=510…860, Y=5…215 | Candidate field inferred between the retained glovebox and cluster zones. M1 must physically trace and sign this field. |
| Centre-field centre | (685.0, 110.0) | The LCD X centre follows this field, **not** the overall-face midpoint (700.0). |
| Cassette visible envelope | 350 W × 210 H, X=510…860, Y=5…215 | A removable cover/carrier envelope; it is not a 350 × 210 vehicle cut. |
| Downward extension beyond existing lower edge | 0 | Default and only quoted configuration. |

The cassette may bridge the actual old openings with a traced service flange, but the smallest connected centre service opening must be determined from the vehicle and actual rear packages. Retain sound perimeter metal, folds, brackets and attachment points. The factory glovebox, cluster and column must not be moved, resized, flattened or made symmetric to accommodate this cassette.

## Source-photo registration audit

The V35 overlay is registered directly to `dashboard_rev_i_v35_registered_source_20260413.jpg` at 4080 × 1884 px. These pixel checks prove that the illustration did not move retained features; they are **not millimetre dimensions** and must never be scaled into a CNC profile:

| Check | Registered source-photo result | Design consequence |
| --- | ---: | --- |
| Passenger outer clear land | approximate visible end tangent X=286 to glovebox trace X=790; 504 px | vent centre X=538 px, exactly the land midpoint |
| Retained glovebox trace | X≈766…1207; Y≈277…611 | source pixels and complete contour remain unchanged |
| Clear centre interval between retained traces | glovebox rightmost X≈1207 to cluster leftmost X≈2037; about 830 px | centre cassette is confined to this interval subject to M1 flange/fastener proof; neither retained component moves |
| Retained cluster/column trace | X≈2037…2634; Y≈236…774 including scallop | source pixels, cluster position and column axis remain unchanged |
| Driver outer clear land | cluster trace X=2634 to visible lower/end contour X=3264; 630 px | vent centre X=2949 px, exactly the land midpoint |
| Glovebox-to-local-lower-edge marker G1 | 22 px in this perspective view | copy the physical gap from the direct M1/M2 trace; do not infer 22 mm |
| Cluster/lower-lip/column marker C1 | 111 px in this perspective view | preserve the complete physical relationship from M1/M3; it is not comparable with G1 as a face-height number |

The different G1 and C1 pixel readings are expected because the photograph is oblique and the cluster relationship includes the steering-column scallop. The overlay leaves both relationships untouched. Only a perpendicular physical trace can establish their actual millimetre values.

## Components and front layout

| Item | V35 provisional requirement | Release condition |
| --- | --- | --- |
| LCD module | 211.10 W × 126.50 H mm | M4 physical drawing/calipers, bezel, fasteners, connectors and removal path. |
| LCD active image | 198.91 W × 111.89 H mm | Size is supplied; its offset inside the actual module is not assumed for the final aperture. |
| LCD location | module centre (685.0, 75.25); X-centred on the free centre field and raised within it to reserve the Y=177 one-line control bank | M1 field trace and M4 module confirmation. |
| LCD opening | 202 W × 115 H provisional visible opening | Do not cut until M4 confirms the actual bezel/touch-border and carrier. |
| LCD complete installed rear projection | 115 mm maximum for quotation/buck; integral chassis/body including any integral rear heat sink target ≤80 mm | `ASSUMED_UNVERIFIED`, derived conservatively from the 2026-08-02 photo audit. It is not a production maximum; M5/M9 controls. |
| Control line | seven bought Schneider Harmony/XB4-family black maintained selectors (4 × 2-position, 3 × 3-position) plus separate red HAZARD, all in one compact line below LCD | M6 actual part codes, handles, lever sweeps, keys, clamps, contact blocks and rear stack. |
| Selector presentation | Ø30 provisional heads at 40 mm pitch | Appearance and spacing only; check actual anti-rotation and handle sweep at M6. |
| Selector aperture | Ø22.5 provisional, based on the 22 mm family and earlier 22.3 mm nominal schedule | Not a production diameter; M6 controls thread, keyway, clamp and finished-sheet fit. |
| Hazard | separate red 2-position control, eighth position in the line | It is not an eighth black selector. |
| Outer vents | Ø87 face target; Ø75 rear mounting diameter target; each face centred in its available outer land | M1 establishes the actual land boundaries; M7 measures the supplied parts and retention. Complete rear envelope is unverified. |

LCD size audit: the supplied active-area values give a calculated diagonal of **228.22 mm / 8.985 in**, consistent with a nominal 9-inch display. The module outline aspect is **211.10 ÷ 126.50 = 1.66877**; both the registered overlay and scale-controlled elevation use that outline ratio. The 202 × 115 mm visible opening remains provisional and must not be mistaken for either the module outline or active area.

### LCD installed-depth control

The supplied **5.0 mm** value is the generic panel/module thickness only. It is not the installed depth of a usable screen assembly. Define `P_LCD_INSTALLED` as the largest perpendicular rearward projection from the finished rear fascia to any part of the module/chassis, carrier, mounts, fasteners, heat sink and ventilation keep-out, largest fully mated plug/adapter, cable bend radius, retained service loop, or cabin-side removal sweep.

For quotation and construction of the rigid depth buck only:

- `P_LCD_INSTALLED,Q ≤ 115 mm`;
- target `P_LCD_CHASSIS ≤ 80 mm`, where `P_LCD_CHASSIS` includes the integral screen chassis/body and any integral rear heat sink; and
- reserve at least 35 mm inside that 115 mm envelope for the external carrier/mounts, fasteners, largest fully mated connector, cable bend/service loop and removal tolerance.

These are `ASSUMED_UNVERIFIED` limits derived from the smallest apparent 125–130 mm local span in the [2026-08-02 rear-clearance photo audit](rear_clearance_photo_audit_20260802.md), rounded down to 125 mm and reduced by the required 10 mm fixed clearance. The photograph is oblique and unregistered, so it cannot release a production maximum.

For production, map the perpendicular available depth `Z_FIXED(x,y)` over the complete actual LCD installed and service/removal envelope, then require:

`P_LCD_INSTALLED,PROD ≤ min[Z_FIXED(x,y)] − 10 mm`.

Also maintain at least 20 mm to the signed moving column/shroud/stalk envelope. The smaller result controls. Replace the 115 mm quotation cap with the measured M5 limit and actual-part M9 buck proof before production release.

The defined line centres are X=545, 585, 625, 665, 705, 745, 785 and 825 at Y=177. The seven black selectors occupy the first seven centres in the allocation below; the red HAZARD is at X=825. At Ø30 heads this makes a 310 mm visible-control envelope, leaving provisional 20 mm margins on both sides inside the 350 mm cassette. These margins are not a substitute for M6 lever-sweep measurements. No selector rear depth is asserted in V35: the previously sketched 68 mm reserve has been removed because the complete bought handle/body/contact-block stack has not yet been measured.

| X (mm) | Hardware | Label | Positions / front legend | Function boundary |
| ---: | --- | --- | --- | --- |
| 545 | black long-lever selector | WIPERS | 3; OFF / LOW / HIGH | Low-current wiper request with park logic. |
| 585 | black long-lever selector | LIGHTS | 3; OFF / SIDE / HEAD | Low-current lighting request; dip and horn remain on column. |
| 625 | black long-lever selector | SPOTS | 2; OFF / ON | Fused relay request only. |
| 665 | black long-lever selector | AUX | 2; OFF / ON | Fused auxiliary relay request only. |
| 705 | black long-lever selector | BLOWER | 3; OFF / LOW / HIGH | Controller/relay input only; never blower-motor current. |
| 745 | black long-lever selector | A/C | 2; OFF / ON | Request through thermostat, pressure and airflow safeties. |
| 785 | black long-lever selector | FUEL STOP | 2; RUN / STOP | Low-current request; key OFF and manual stop remain authoritative. |
| 825 | separate red hazard control | HAZARD | 2; OFF / ON | Separate fused hazard request. |

Use a 1:1 label and lever-sweep proof with the actual bought controls before machining engraving, labels or cuts.

## Vent and rear-package constraints

Each retained outer land receives only one target Ø87 visible vent face. For the quotation model the passenger-side centre is the midpoint between the assumed left fascia boundary and the assumed left edge of the retained glovebox zone: `X=(0+225)/2=112.5`. The driver-side centre is the midpoint between the assumed right edge of the retained cluster zone and the assumed right fascia boundary: `X=(1045+1400)/2=1222.5`. Both use the same physical face-height datum `Y=70`; the sloping centre line in the registered photograph is perspective only. M1 must replace all four assumed land boundaries and recompute both midpoints before release. The nominal Ø75 rear mounting diameter is an interface target, **not a released aperture**. It must be replaced by the actual vent boss/retainer drawing and a finished-sheet coupon.

The minimum nominal front land for an Ø87 face is Ø107 (10 mm clear all around). If either measured midpoint cannot provide that land without touching the fascia end contour, glovebox zone or cluster/column zone, stop and reposition from the physical trace; do not trim a retained OEM feature.

The complete rear envelope is **NOT VERIFIED**. Two of the photos imported on 2026-08-02 show oblique local rays of about 125–130 mm and 160–170 mm. The third shows a 270–280 mm endpoint reading, not a span, because its tape zero/start is outside the frame. The nominal approximately 22 mm louver body is therefore **provisionally plausible / not contradicted** on the photographed local ray. However, none of those rays is perpendicular to a declared finished-rear-fascia datum or registered to either planned vent centre. They do not prove the retained outer lands.

Define `P_VENT_INSTALLED` as the greatest perpendicular rearward projection of the louver body, retention and anti-rotation hardware, adapter/spigot, clamp, hose OD, first bend, duct support, full aim/shutoff sweep and cabin-side removal path. At each marked actual centre and across the complete rear swept envelope require:

`P_VENT_INSTALLED ≤ min[Z_FIXED(x,y)] − 10 mm`,

with at least 20 mm to the moving column/shroud/stalk envelope. The full [photo audit](rear_clearance_photo_audit_20260802.md), [evidence schedule](rear_clearance_photo_evidence_20260802.csv) and [control diagram](rear_package_clearance_control.svg) are controlled quotation evidence. The rear buck must prove both complete vent branches with the LCD, wiring, controls, glovebox, cluster and steering envelope installed at once.

## Mandatory physical gates

Production remains HOLD until every applicable gate passes; the minimum non-negotiable gates are:

1. **M1 — fascia/free-centre-field trace:** signed 1:1 trace of the complete existing visible face, both end boundaries, lower edge, folds, centre openings and true unobstructed centre field. Record `G1` glovebox-to-lower-edge gap, the `C1` cluster/lower-lip/column relationship, and the four outer-land boundaries used to calculate the two vent midpoints.
2. **M4/M5 — LCD trace and depth:** actual module/bezel/cutout, mounting pattern, connector/wire-bend, heat and cabin-side removal measurements; perpendicular `Z_FIXED` depth map at chassis corners, centre, mounts, connector and cable-turn zone; complete actual `P_LCD_INSTALLED`. Replace the 115 mm quotation cap before production release.
3. **M6 — control trace:** each purchased selector and the hazard: body, thread, key, clamp, head, lever sweep, terminal orientation, rear depth and label proof.
4. **M7/M9 vent-site survey and rear buck:** mark both actual vent centres, map perpendicular available depth over each complete retention/duct swept envelope, measure each assembled `P_VENT_INSTALLED`, then prove the LCD, all eight controls, both complete vent-to-duct assemblies, glovebox operation, cluster package and complete moving steering envelope simultaneously in a rigid full-depth mock-up.

Also complete M2 glovebox/ashtray trace, M3 cluster/column/scallop trace, M7 vent retention and total rear package, and the vehicle-specific duct-route survey before releasing any affected cut.

## Supplier quotation instruction

Quote (a) one removable 1.5 mm CR4 mild-steel centre cassette, template and trial blank, and separately (b) two retained-panel vent operations plus coupons. Use deburred/radiused edges, low-gloss body-colour finish and serviceable concealed fixings/captive nuts. Quote a rigid full-depth buck and 1:1 paper template; do not quote a vehicle cut from this document.

When the physical gates are signed, issue a separate production DXF/PDF with locked layers for `TRACE_LOCK`, `RETAINED_OEM`, `CENTRE_SERVICE_CUT`, `CASSETTE_OUTLINE`, `COMPONENT_CUTS`, `FORM_LINES`, `KEEP_OUT` and `INSPECTION`. Until then all V35 numerical geometry carries `HOLD`.

## V35 verdict

- OEM fascia envelope and features: **LOCKED / UNCHANGED**.
- Centre-only cassette and zero-drop layout: **accepted design direction for quotation**.
- One-line selector/hazard allocation: **provisional, HOLD M6**.
- LCD location and opening: **provisional, HOLD M1/M4**. Complete rear projection: **115 mm quotation/buck cap and ≤80 mm chassis target only; production maximum HOLD M5/M9**.
- Two outer vent faces: **provisional**. Approximately 22 mm body-only fit: **plausible / no contradiction in the imported local-cavity photos**. Complete outlet/retainer/duct fit at both actual centres: **NOT PROVEN, HOLD M7 and rear buck**.
- Production vehicle cut and production CNC: **HOLD pending M1, M4, M6 and rear buck (plus associated M2/M3/M7/duct evidence).**
