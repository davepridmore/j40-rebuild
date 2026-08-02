# J40 dashboard Rev I V34 — centre cassette / single-row controls

Status: **approved design direction for quotation, a 1:1 face template and a full-depth packaging buck only. Production dashboard cuts and production component apertures remain HOLD.**

## Design decision

V34 corrects the packaging error in the former full-width replacement concept:

- retain the original dashboard shell, height, non-flat end contours, glovebox, speedometer aperture, steering-column scallop and their mountings;
- remove the ashtray and obsolete centre HVAC/radio metal only where the signed centre cut trace permits;
- install one removable CNC-made centre cassette carrying the 9-inch LCD and every new electrical control;
- place the seven bought black selectors plus the separate red hazard in **one horizontal row directly below the LCD**;
- make only two separate circular outlet holes in the retained outer dashboard lands; do not replace or flatten those lands;
- do not move the speedometer, glovebox or steering column to make room.

The current visual is [dashboard_rev_i_v34_center_cassette_single_row_straight_on.png](dashboard_rev_i_v34_center_cassette_single_row_straight_on.png). It is an appearance and packaging study, not a scale source. The dimensioned [front elevation](dashboard_rev_i_v34_center_cassette_front_elevation.svg) and [coordinate schedule](dashboard_rev_i_v34_center_cassette_coordinates.csv) state the provisional quotation geometry.

## Speedometer and steering-column verdict

The V34 visual places the original cluster in the correct **relationship**: low on the driver/right side, immediately above the original column/shroud, and centred on the factory column axis. That is the correct design rule. Its absolute X/Y cannot be certified from a rendered image.

For production, copy the installed vehicle's complete cluster aperture, mounting points, narrow lower seam, column centre and factory U/scallop as one immutable M3 trace. The intact reference `photos/20260317_165113.jpg` controls the cluster-to-column relationship; `photos/20260413_040719.jpg` controls the original aperture, scallop and lower-edge shape. No V34 dimension moves or resizes those OEM features.

## Assumption-based quotation geometry

Coordinate convention: provisional overall-face origin `(0,0)` is the upper-left of a **1400 × 250 mm assumed visible-face envelope**, X rightwards and Y downwards. That envelope is not a measured J40 production profile and must be replaced by the signed M1 trace.

| Feature | V34 quotation value | Basis / release status |
| --- | ---: | --- |
| Assumed visible face | 1400 W × 250 H mm | Public-envelope assumption; HOLD M1 |
| Centre cassette visible outer envelope | 350 W × 210 H mm, nominal `X=525…875`, `Y=5…215`, R18 corners | Quotation/template only; actual perimeter must bridge the measured centre field without touching OEM apertures |
| Minimum measured straight centre-field width | **370 mm** | 350 mm cassette plus 10 mm verified fixed clearance each side; production blocker |
| LCD module | 211.10 W × 126.50 H × 5.0 D mm | Owner-supplied nominal; confirm actual M4/M5 |
| LCD active image | 198.91 W × 111.89 H mm; 228.6 mm diagonal | Owner-supplied nominal; confirm offsets M4 |
| Provisional LCD module centre | `(700.0, 75.25)` mm | Horizontally centred on assumed complete face; vertically raised to make the control row possible |
| Provisional visible opening | 202 W × 115 H mm, R3 | Do not cut until actual bezel/touch border is measured |
| Control row centres | `X=553, 595, 637, 679, 721, 763, 805, 847`; `Y=177` mm | 42 mm pitch; quotation/template only |
| Visible control-row envelope | 324 W mm using Ø30 heads | Derived: 7 × 42 + 30; confirm actual lever sweeps and labels M6 |
| Selector apertures | Ø22.5 mm provisional | Actual bought-part thread/key/clamp range controls M6 |
| Selector visible head | Ø30 mm provisional; long black lever, pale inset and chrome bezel | Owner's bought-switch photograph controls appearance |
| Selector rear stack | 68 mm provisional from rear finished face | Include contacts, terminals, boots, wire bends and service loop in buck |
| Outlet visible face | Ø87 mm target | Owner-supplied target; measure all four M7 |
| Outlet rear mount | Ø75 mm target maximum | Not a released cut size |
| Outlet louver-body depth | approximately ≤22 mm target | Does **not** include retainer, spigot, clamp, elbow or duct |

The one-row arrangement uses the centre width efficiently and reduces the required cassette height. On the 250 mm quotation envelope it fits without lowering the normal dashboard edge. If the signed vehicle trace provides less than 215 mm of clear centre height, quote a shallow rounded local drop of only the measured deficit, capped provisionally at 25 mm and subject to owner approval. Do not extend the complete dashboard downward.

## Centre cut and attachment rule

The 350 × 210 mm cassette outline is a **visible removable cover/carrier**, not permission to cut a 350 × 210 rectangle from the vehicle.

1. Direct-trace the glovebox lid/aperture/sweep, centre openings and ashtray structure, cluster aperture, steering scallop, mounts, folds and behind-face braces.
2. Define the smallest connected centre service opening that clears the actual LCD rear body/connectors and actual control bodies while retaining sound perimeter metal and all structural attachments.
3. Use the cassette's 15–20 mm nominal stepped flange to bridge the old centre apertures and conceal the ashtray deletion.
4. Attach the cassette to retained centre metal with concealed serviceable fasteners or captive nuts; prove cabin-side removal with the LCD and wired selectors installed.
5. Keep at least 10 mm measured fixed clearance from the complete cassette/rear package to the glovebox box and cluster package, and at least 20 mm to the steering moving envelope.

If the signed unobstructed centre field is narrower than 370 mm, do not move an OEM assembly. Re-measure the actual selector head/lever sweep and contact-body width, then reduce pitch only to the bought manufacturer's permitted minimum or use a locally stepped/asymmetric cassette flange. A full-width flat replacement is not the fallback.

## Single-row switch allocation

Left to right beneath the LCD:

| Position | Hardware | Label | States | Electrical function |
| ---: | --- | --- | --- | --- |
| 1 | bought 3-position black/chrome long-handle selector | WIPERS | OFF / LOW / HIGH | low-current wiper request with park logic |
| 2 | bought 3-position black/chrome long-handle selector | LIGHTS | OFF / SIDE / HEAD | low-current lighting relay request; dip/horn remain on column |
| 3 | bought 2-position black/chrome long-handle selector | SPOTS | OFF / ON | fused spot-lamp relay request |
| 4 | bought 2-position black/chrome long-handle selector | AUX | OFF / ON | fused auxiliary relay request |
| 5 | bought 3-position black/chrome long-handle selector | BLOWER | OFF / LOW / HIGH | controller/relay input; no motor current through selector |
| 6 | bought 2-position black/chrome long-handle selector | A/C | OFF / ON | request through thermostat, pressure and airflow safeties |
| 7 | bought 2-position black/chrome long-handle selector | FUEL STOP | RUN / STOP | low-current request; key OFF and manual cable retained |
| 8 | separate red maintained hazard control | HAZARD | OFF / ON | independent fused hazard request |

Inventory is exact: three 3-position selectors, four 2-position selectors, and one separate red hazard. There is no spare black selector and no variable-input control. Use a two-line `FUEL / STOP` legend if required to prevent label overlap. Make a 1:1 printed engraving proof with the actual handles fitted before machining labels.

## A/C outlet available-space check

### Front-face result

The two outer positions are visually credible and benefit from moving the switch/contact stack away from the driver outlet. A Ø87 face with 10 mm visible clearance needs a clear fixed-land circle of **Ø107 mm**, or its centre at least **53.5 mm** from a lid edge, panel boundary or adjacent visible component. A conditional Ø75.5 trial aperture with 10 mm structural land needs at least **Ø95.5 mm** clear fixed metal. These requirements must be demonstrated on the signed M1/M2/M3 trace; the image alone does not prove them.

- Passenger outlet: must be wholly outboard of the complete glovebox lid, aperture, hinges, latch, box and opening/removal sweep.
- Driver outlet: must be wholly outboard of the complete cluster package and at least 20 mm from the moving column/shroud/stalk envelope.
- Keep both faces on one measured upper datum. Move an outlet farther outward within proven fixed land if its rear package clashes; do not move the glovebox, cluster or column.

### Rear-package result

**Not yet proven.** The approximately 22 mm value covers only the louver body. Installation also needs the retainer, any anti-rotation feature, hose spigot, clamp land, clamp, first elbow/flexible-hose bend, duct support and service-removal path. `photos/20260323_190005.jpg` confirms wiring and HVAC obstructions behind the dashboard but supplies no perpendicular depth grid.

For a provisional 2.5-inch (63.5 mm) duct study, reserve a 65–70 mm installed hose/clamp outside diameter and use the hose maker's minimum bend radius; where no controlled value exists, mock a centreline radius of at least 1.5D (about 95 mm). This is a buck envelope, not a production dimension.

Measure each candidate outlet centre at rear-depth stations `Z=0, 25, 50, 75, 100, 125 and 150 mm`. At every station record the nearest body return, brace, glovebox/cluster envelope, loom and moving steering envelope. Pass only when the complete actual outlet-to-duct assembly maintains:

- at least 10 mm to every fixed item;
- at least 20 mm to every moving steering item;
- uncrushed duct, supported throughout, with cabin-side outlet removal;
- full glovebox and steering operation.

## Mandatory pre-CNC evidence

1. M1 signed 1:1 original-fascia and centre-field trace, including the minimum clear width and height.
2. M2 unchanged glovebox profiles, box depth and complete opening/removal sweep; separate ashtray deletion boundary.
3. M3 unchanged cluster/column/scallop profiles, rear package and all moving envelopes.
4. M4/M5 actual LCD drawing/calipers, bezel, carrier, connectors, heat and removal path.
5. M6 every actual selector/hazard front sweep, cut/key/clamp details, rear stack, terminal and label proof.
6. M7 all four actual vents, retention, total rear projection, spigot, hose/clamp and finished-sheet coupon.
7. M8 actual evaporator ports/case/drain plus two complete supported duct routes.
8. M9 1:1 face template and rigid full-depth buck with all actual components installed simultaneously.

## CNC supplier instruction

Quote the centre cassette separately from the two retained-panel vent operations. Proposed cassette material is 1.5 mm CR4 mild steel, body-colour low-gloss finish, deburred/radiused edges and concealed serviceable attachment. Supply 1:1 millimetre DXF and dimensioned PDF only after the signed traces are imported. Layers: `TRACE_LOCK`, `RETAINED_OEM`, `CENTRE_SERVICE_CUT`, `CASSETTE_OUTLINE`, `COMPONENT_CUTS`, `FORM_LINES`, `KEEP_OUT`, `ASSUMED_QUOTE_ONLY`, `INSPECTION`.

Unless an actual part requires tighter limits, quote cut position ±0.5 mm, cut size ±0.25 mm, and formed silhouette ±2 mm against the signed checking template. Do not cut the vehicle or production sheet from the V34 PNG, SVG or provisional CSV.

## Release verdict

- Speedometer/column design rule: **PASS; retain exact OEM trace and low factory relationship.**
- One-row control allocation and front packaging: **PASS for 1:1 template/quotation.**
- Centre-only replacement strategy: **PASS for design direction.**
- Ø87 outlet front-land feasibility: **CONDITIONAL pending trace.**
- Outlet and duct rear fit: **HOLD pending actual-parts full-depth buck.**
- Production vehicle cut / production CNC: **HOLD M1–M9.**
