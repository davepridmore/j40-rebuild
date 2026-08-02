# J40 dashboard Rev I V32 — provisional assumption-based CNC specification

Revision: **V32-Q1, quotation and disposable prototype only**
Units: **millimetres**
Production state: **HOLD — not a vehicle-cut or production-metal release**

This specification gives the CNC supplier enough geometry to quote CAD cleanup, material, cutting, forming, a full-size face template, a full-depth buck and outlet coupons while the vehicle and bought parts are measured. It deliberately separates measured/supplied values from assumptions. Any item marked `ASSUMED` or `TRACE-LOCK` must be replaced before a production DXF is released.

## Design intent that may not be changed

- Complete replacement fascia at the original dashboard height; no full-width downward extension.
- Original Toyota speedometer cluster, factory RHD steering-column position/scallop and original asymmetric glovebox are transferred at their exact vehicle-traced positions and shapes.
- Ashtray is removed and its area becomes uninterrupted body-colour fascia.
- True 9-inch LCD active image is centred on the complete fascia in both axes.
- Exactly two matching Ø87-class chrome/silver circular outlets, high and slightly inboard, on one horizontal datum.
- Exactly seven bought black selectors plus one separate red hazard control in the far-right 4 x 2 bank.
- Two-position selectors: `SPOTS`, `AUX`, `A/C`, `FUEL STOP`. Three-position selectors: `WIPERS`, `LIGHTS`, `BLOWER`.

## Geometry classes

| Class | Meaning | May production metal be cut? |
| --- | --- | --- |
| `SUPPLIED` | Owner-supplied nominal component figure; still confirm against the actual part | No, until confirmed |
| `ASSUMED` | Deliberate quote/model placeholder | No |
| `TRACE-LOCK` | Copy directly from the installed vehicle or signed 1:1 trace | Only after signed trace |
| `COUPON` | Candidate geometry that must pass a same-material, final-finish coupon | Coupon only |

## Provisional coordinate frame and face envelope

- Origin `(0,0,0)`: top-left of the nominal finished front face.
- `X`: passenger to driver on this RHD vehicle. `Y`: downward. `Z`: rearward.
- Nominal public-listing face envelope: `W_FACE = 1400`, `H_FACE = 250`, `D_VENDOR_ENVELOPE = 100` — `ASSUMED`, used only for quote scale and collision planning.
- Provisional flat front outline: 1400 x 250 with R18 corners — `ASSUMED`. Replace the entire outline with the signed M1 trace.
- Provisional production material: 1.5 mm CR4 mild steel, deburred, primed and body-colour low-gloss finish.
- Quote a 1450 x 330 minimum blank allowance plus scrap for bend and outlet coupons. Actual developed blank comes from the traced returns and the supplier's proven bend allowance.
- For quote only, allow 20 mm top/end returns and a 15 mm lower return, 90-degree bends, R2 inside. These are placeholders; duplicate the vehicle/body support geometry after M1.

## Provisional new-component coordinates

The coordinate table is also supplied as `dashboard_rev_i_v32_provisional_coordinates.csv`.

| Feature | Provisional centre / geometry | Class | Production action |
| --- | --- | --- | --- |
| LCD active image | centre `(700.0, 125.0)`; 198.91 x 111.89 | `SUPPLIED` size, `ASSUMED` envelope centre | Recalculate centre from signed complete-face trace and confirm active-image offsets |
| LCD module | same provisional centre; 211.10 x 126.50 x 5.0 | `SUPPLIED` | Measure actual unit and connector envelope |
| LCD visible opening | 202.0 x 115.0, R3 | `ASSUMED` | Do not cut production; derive from actual bezel/active area |
| Passenger outlet face | centre `(135.0, 70.0)`; Ø87 | `SUPPLIED` target and `ASSUMED` centre | Preserve ≥10 visible/fixed clearance and glovebox sweep; move outward within signed fixed land if rear package clashes |
| Driver outlet face | centre `(1265.0, 70.0)`; Ø87 | `SUPPLIED` target and `ASSUMED` centre | Preserve switch/contact-stack clearance; move outward within signed fixed land if rear package clashes |
| Outlet trial aperture | Ø75.50 +0.25 / -0.00 | `COUPON` | Valid only if measured boss ≤75.00 and slip-through back retention is proven |
| Selector top row | `(1060,137.5)`, `(1110,137.5)`, `(1160,137.5)`, `(1210,137.5)` | `ASSUMED` | Replace cut/key details with M6 part measurements |
| Selector bottom row | `(1060,190)`, `(1110,190)`, `(1160,190)`, `(1210,190)` | `ASSUMED` | Last position is separate red hazard, not an eighth black selector |
| Selector trial cuts | Ø22.5; 50 horizontal x 52.5 vertical pitch | `ASSUMED` | Confirm all seven controls and hazard individually |
| Glovebox | import exact lid, aperture, mounts and sweep from M2 trace | `TRACE-LOCK` | Do not redraw, centre, resize or symmetrise |
| Speedometer cluster | import exact bezel, aperture and mounts from M3 trace | `TRACE-LOCK` | Do not move vertically or horizontally |
| Column/scallop | import exact shaft axis, U-profile and moving envelope from M3 trace | `TRACE-LOCK` | Immutable steering datum |

The assumed vent centres are symmetric about `X = 700`, are 65 mm inboard of the minimum Ø87-plus-10-mm edge rule, and put their top edges 26.5 mm below the nominal top. The driver outlet face to nearest assumed selector-head envelope retains approximately 28.6 mm visible separation when a provisional Ø30 selector head is used. These checks do not prove rear clearance.

## LCD construction allowance

- Reserve a fixed rear keep-out of at least 221.10 x 136.50 around the provisional module, then add the actual carrier, connector and cable-bend envelopes.
- The active-image centre—not merely the module or decorative bezel centre—must equal the complete traced fascia midpoint.
- Provide a removable rear carrier rather than relying on the decorative face as the only support. Carrier material, holes and fasteners remain M4/M5 holds.
- Maintain at least 10 mm physical clearance to adjacent fixed metal, ducts and retained components after tolerances and finish.

## Outlet construction allowance

- `D_FACE = 87.0` is the visible proportion envelope. `D_MOUNT_MAX = 75.0` and `P_BODY ≈ 22` are owner-supplied target-family values, not proof of the ordered SKU.
- Do not infer hose size from the Ø75 mounting boss. Measure the spigot, retention hardware, clamp and first elbow as separate rear envelopes.
- Quote three 120 x 120 coupons in 1.5 mm CR4 with Ø75.25, Ø75.50 and Ø75.75 apertures. This coupon set is only appropriate if receipt inspection confirms a slip-through/back-retained boss near Ø75.
- Keep at least 10 mm between the complete assembled vent/duct package and fixed hardware. Keep at least 20 mm from every moving column/shroud/stalk envelope.
- Use two supported branches from the selected two-takeoff evaporator and retain a separate demist route. Do not crush a round duct below 90% of its nominal inside diameter.

## Control-bank allowance and allocation

| Position | Label | Bought control | Low-current function |
| --- | --- | --- | --- |
| Top 1 | WIPERS | 3-position | OFF / LOW / HIGH with park logic through relays/controller |
| Top 2 | LIGHTS | 3-position | OFF / PARK / HEAD through relays |
| Top 3 | SPOTS | 2-position | OFF / ON request through relay |
| Top 4 | AUX | 2-position | OFF / ON reserved auxiliary request through relay |
| Bottom 1 | BLOWER | 3-position | OFF / LOW / HIGH controller request |
| Bottom 2 | A/C | 2-position | OFF / ON A/C request; safety and fan interlocks remain authoritative |
| Bottom 3 | FUEL STOP | 2-position | RUN / STOP low-current request; key OFF and original manual stop remain authoritative |
| Bottom 4 | HAZARD | Separate red control | Independent hazard request |

Assume Ø30 visible heads and a 68 mm-class rear contact stack for collision quoting only. M6 measurements control the aperture, anti-rotation, clamped thickness, lever sweep, terminals and wiring service loops. No motor, lamp, compressor-clutch or fuel-solenoid load is carried directly through a fascia selector.

## Quotation tolerances and deliverables

- Quote target: cut-feature position ±0.5, cut-feature size ±0.25 and formed outer silhouette ±2 against a signed checking template, unless an actual component drawing is tighter. Supplier must state achievable tolerances.
- Quote separately: CAD/trace digitisation; full-size 1:1 MDF/card/plastic face template; full-depth rigid buck; outlet coupon set; one unpainted steel first article; final production fascia after written release.
- Provide the model in millimetres at 1:1, with layers `TRACE_LOCK`, `NEW_CUTS`, `FORM_LINES`, `KEEP_OUT`, `ASSUMED_QUOTE_ONLY` and `INSPECTION`.
- Supply DXF plus a dimensioned PDF. The PDF must state the DXF overall extents and revision so scale can be checked independently.
- Do not cut the vehicle, production fascia, retained glovebox or cluster from this V32-Q1 document.

## Conversion to an exact CNC release

1. Complete and sign `cnc_measurement_schedule.csv` using `cnc_measurement_and_survey_checklist.md`.
2. Replace the nominal 1400 x 250 outline, returns and fixings with the signed M1 trace.
3. Import M2/M3 glovebox, cluster and column profiles without repositioning them.
4. Replace LCD, outlet, selector and hazard assumptions with actual M4–M7 drawings/measurements.
5. Add the measured M8 HVAC, duct and demist rear envelopes.
6. Pass the full-size face template, full-depth buck and functional tests at M9/M10.
7. Freeze coordinates, issue a new production revision and obtain owner plus body-shop signatures.

Until all seven steps are complete, this remains a transparent cost-and-layout assumption model, not an exact CNC cutting file.
