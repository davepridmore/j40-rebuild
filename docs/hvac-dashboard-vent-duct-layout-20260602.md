# HVAC Dashboard Vent And Duct Layout - 2026-06-02

Purpose: convert the new condenser/cabin airflow direction into a buyable vent and duct plan for the J40 A/C retrofit.

## 2026-08-01 Two-Outlet Supersession

The active owner direction is now exactly two high outer/end occupant outlets and a smaller cabin evaporator package. The four-outlet Rev H material below is retained as a superseded design record; do not use its V1-V4 apertures, inner pods, duct quantities, or production coordinates for fabrication.

Active layout controls:

| Item | Active requirement |
| --- | --- |
| Occupant outlets | Two matched, generously sized directional outlets on one high datum at the fixed outer/end fascia regions, one independently aimable toward the passenger and one toward the driver; no central/lower outlets or pods |
| Evaporator connection | Two genuine duct takeoffs of measured OD, or a sealed two-takeoff plenum designed for the selected compact core/case |
| Ducting | Two supported end branches with the largest practical bend radius; prove useful balanced airflow and service clearance with both complete runs connected; no Y split and no capped four-port case unless bench airflow and freeze-control tests pass |
| Demist | Retain the original heater/demist system or add dedicated small plenum takeoffs; do not count the two face outlets as the only windscreen-clearing provision |
| Fabrication status | Rev I console/fascia geometry HOLD until the in-vehicle available envelope, louver samples, evaporator case, fittings, drain, wiring, and service-removal path are measured |

Before purchasing the replacement, obtain tape-measure photos of overall case width, height and depth; the two outlet neck ODs and rear projection; refrigerant fitting side and thread/type; drain position; mounting tabs; return-air face; blower current; thermostat/freeze control; TXV; and stated airflow/capacity. Cardboard-mock that complete envelope in the J40 with the glovebox, cluster, column, knees and lever sweeps represented.

## Superseded Rev H Dashboard Integration Record

The Rev H integration was [dashboard_lcd_hvac_fascia_rev_h](../data/manual/fabrication/dashboard_lcd_hvac_fascia_rev_h/README.md); it is not the current fabrication package. Rev H removed the complete existing visible dashboard face and replaced it with one shallow, body-colour CNC-formed face while directly transferring the original right-hand-drive Toyota speedometer assembly and asymmetric glovebox lid, knob, hinges/latch and instruction plate. Both OEM assemblies were visual no-touch regions: retain their existing position, outline, finish, colour, patina, markings and controls exactly, and form the new fascia to their transferred edges. The ashtray was deleted. A true 9-inch/16:9 LCD sat centrally in an uninterrupted upper field. Its centre, the usable-fascia centreline and the midpoint of the two inner outlets used the same CNC datum; the inner outlets were mirrored at equal offsets. Exactly four matched circular satin-silver outlets sat in a `1-2-1` arrangement. The two outer outlets remained high at nominal centres `X=50/1210 mm, Y=168.5 mm`, with their `Ø87 mm` bezel tops aligned to the LCD-bezel top at `Y=212.0 mm`. V1 was wholly on fixed fascia outboard of the direct-traced OEM glovebox: retain at least `10 mm` of real fixed-metal land from the bezel to the lid boundary, and keep its aperture, retainer, duct and service land outside the lid, hardware, opening and full sweep. The inner pair was lowered below and to either side of the LCD at nominal centres `X=464/796 mm, Y=20.0 mm`, in matched local pods that descended to `Y=-35.0 mm`; its visible faces stopped a nominal `12.5 mm` below the LCD bezel. The historical cost reference was a common `Ø87 mm` visible face / `Ø75 mm` panel-opening family, but no Rev H vent cut is active.

Exactly seven Schneider selectors plus a separate red hazard are consolidated in one labelled two-row, four-column bank at the extreme right, at `48 mm` nominal horizontal and `58 mm` vertical pitch. The top row is `WIPERS | LIGHTS | SPOTS | AUX`; the bottom row is `BLOWER | A/C | ENGINE | HAZARD`. `WIPERS`, `LIGHTS`, `BLOWER` are 3-position; `SPOTS`, `AUX`, `A/C`, `ENGINE` are 2-position. `ENGINE` uses the former spare selector as a low-current RUN/STOP request only after EEI-003 proves the diesel fuel-stop logic; key OFF remains authoritative and the manual stop cable remains the emergency fallback. The bank does not duplicate OEM indicator/dip/horn controls, keyed ignition, washer input or winch lever. Cabin temperature/blend remains with the measured evaporator thermostat/controller and is not an eighth selector. Gates M6, M8 and M9 must prove that selector heads, lever sweeps and rear contact stacks clear both right-hand duct branches, the retained cluster, steering column and driver controls. Only the disposable full-size template is released before gates M1-M10; production vehicle metal, LCD, selector, hazard and vent apertures remain HOLD until physical tracing, bought-part measurement and rear-envelope mock-up are signed.

## Evidence Position

- Live Gmail MCP is not authenticated in this session. The usable Gmail-derived project extract is `data/processed/generated/gmail_project_messages_2026-06-01.json`.
- Live WhatsApp MCP is not exposed as a callable tool in this session. The usable WhatsApp project extract is `data/processed/generated/whatsapp_project_relevant_2026-06-01.csv`.
- Owner reports a condenser has been bought and is expected to fit in the front compartment/front cooling stack. Exact condenser product, dimensions, fitting side, and order proof still need confirmation before final drier/fan/hose release.
- Existing A/C control position remains: hidden or slimline cabin evaporator, external/owner-selected blowers where practical, and no final dash cuts or hose crimps before physical mock-up.

## Superseded Rev H Layout Record

Rev H used the following four-outlet cabin plan; it is retained for traceability and is not an active purchase or fabrication instruction:

| Outlet group | Quantity | Position | Preferred vent type | Duct rule |
| --- | --- | --- | --- | --- |
| End pair | 2 | High and close to the usable flat-face ends, never in the side returns/A-pillars; nominal centres `X=50/1210 mm, Y=168.5 mm`; V1 and its complete rear package remain on fixed fascia outboard of the M2 glovebox trace with at least `10 mm` real fixed-metal land | Matched circular directional louvers with satin-silver `Ø87 mm` reference faces, flush to +0.5 mm | Balanced supported branches from the evaporator/plenum; route V1 above/outboard of the full glovebox opening sweep and prove both end runs clear the cluster, column, selector/contact stacks and structure |
| Inner pair | 2 | Mirrored below and to either side of the LCD at nominal centres `X=464/796 mm, Y=20.0 mm`; matched local pods descend to `Y=-35.0 mm`; preserve at least `8 mm` visible rim-to-LCD clearance as built | Same make, batch, face, louver and finish as the end pair | Short supported branches from the balanced plenum; preserve LCD/cluster/column/service clearance and do not encroach on the control bank |

Do not buy random dashboard vents by appearance only. The vent neck OD must match the evaporator outlet/plenum standard. Use 2.5 inch duct as the default because the current reference HVAC components and louvers commonly use 2.5 inch hose. Use 2.0 inch only if the purchased unit physically provides 2.0 inch outlets and the airflow test still passes.

## Superseded Rev H Reference Parts

These were Rev H geometry/spec references and import fallbacks. They do not authorise a current purchase; the active Rev I job requires one measured matched pair and two complete end branches.

| Use | Reference | Why it matters |
| --- | --- | --- |
| Full front under-dash outlet panel | Vintage Air `492090` slimline universal under-dash louver panel | Four-louver flat under-dash concept; useful if avoiding visible holes in the original dash. |
| Compact double dash outlet | Vintage Air `63316-VUL` all-black double under-dash louver | 11.375 x 2.5 inch panel with 2.5 inch hose inlets; good model for the front pair. |
| Individual directional outlet | Vintage Air `49050-VUL` / `49350-VUL` style single under-dash louver | Good model for each side outlet if a full panel is too wide. |
| Round directional pod | Vintage Air `492083` or `49054-VUL` style 2.5 inch round under-dash pod | Useful geometry reference for the four integrated dash outlets because the ball/eyeball louver can be aimed at occupants. |
| Duct hose | Vintage Air `06250-VUE`, `318005`, `318010` style 2.5 inch duct hose | Buy after mock-up, with enough total length to cover all four outlet paths plus service slack. |
| Adapters | 2.5 inch oval glue-on adapters and 2.5 inch Y connectors only if needed | Use only after the evaporator outlet count is known; Y-splitting reduces flow and should be airflow-tested. |

## Superseded Rev H Buy Specification

Ask suppliers for:

- Four identical directional automotive A/C vents/louvers from one batch, all circular flush-mount dashboard units. Cost/reference geometry is `Ø87 mm` visible face and `Ø75 mm` panel opening; neither dimension is a production release until the samples are measured.
- All four visible faces: matched satin/brushed silver with black directional cores, hidden rear retention and no exposed front screws. Avoid bright mirror chrome and do not mix end and centre vent families.
- Vent face dimensions, rear neck OD/ID, rear depth, louver movement range, shutoff ability, screw spacing, and photos with a tape measure.
- 2.5 inch flexible automotive HVAC duct hose, matching adapters, clamps, and any Y connectors needed after the evaporator outlet count is proven.
- Defrost/demist takeoff parts only after the evaporator/plenum position is known; do not steal all outlet area for face vents if demist is required.

Reject:

- Non-directional vents that cannot aim air at occupants.
- Vents with no hose neck or unknown hose size.
- Thin decorative plastic that cannot clamp a duct hose securely.
- Long rear runs made with small 2.0 inch hose unless airflow testing proves acceptable.
- Any release of production dashboard metal, LCD, control or vent apertures before the actual dashboard, transferred OEM parts and bought components are measured and the evaporator, plenum, blower, both complete end-duct paths, bend radius and rear clearances are mocked with the Rev I full-size template.

## Shop Call Text

Need one matched pair of large directional A/C outlets for an old Land Cruiser CNC dashboard. Use circular satin-silver faces with black directional cores, hidden rear retention and no exposed front screws. Current reference is approximately 87 mm face / 75 mm panel opening, with a 2.5 inch hose neck preferred, but please do not substitute by appearance. Send tape-measure/caliper photos of face diameter, required panel cutout, rear hose-neck OD, total rear depth, retainer, louver movement, shutoff and pair price. Also quote matching flexible automotive HVAC duct, clamps and any two-outlet plenum adapters. No dashboard holes or hose sizes are final until both samples and the evaporator outlets are measured and mocked up.

## Sources Checked

- Vintage Air `492090` slimline universal under-dash louver panel reference: https://fuelcurve.com/vintage-air-universal-ultra-slim-under-dash-louver-panel-kit/
- Vintage Air `63316-VUL` double under-dash louver reference: https://vintageair.com/double-under-dash-louver-assembly-for-2-5-inch-hose-all-black/
- Vintage Air `492083` round single louver kit reference: https://vintageair.com/slimline-recessed-under-dash-round-universal-single-louver-kit-for-2-5-inch-hose/
- Vintage Air catalog, under-dash louvers, adapters, and duct hose stock: https://vintageair.com/content/2023%20Vintage%20Air%20Catalog.pdf
- Generic cost-reference vent family, published `Ø87 mm` face / `Ø75 mm` opening: https://www.joom.com/en/products/68c8f9fa6dffb3012ca80d30
