# HVAC Dashboard Vent And Duct Layout - 2026-06-02

Purpose: convert the new condenser/cabin airflow direction into a buyable vent and duct plan for the J40 A/C retrofit.

## 2026-08-01 Dashboard Integration Update

The controlled integration is now [dashboard_lcd_hvac_fascia_rev_g](../data/manual/fabrication/dashboard_lcd_hvac_fascia_rev_g/README.md). Rev G removes the complete existing visible dashboard face and replaces it with one shallow, body-colour CNC-formed face while transferring the original right-hand-drive Toyota speedometer assembly and asymmetric glovebox lid, knob, hinges/latch and instruction plate. The ashtray is deleted. A true 9-inch/16:9 LCD sits centrally in an uninterrupted upper field. Its centre, the usable-fascia centreline and the midpoint of the two inner outlets are the same CNC datum; the inner outlets are mirrored at equal offsets. Exactly four matched circular satin-silver outlets sit in the dashboard on one common physical height: one close to each usable flat-face end and two below the LCD. Three integral rounded local drops create outlet depth without extending the full dashboard downward. The current cost reference is a common `Ø87 mm` visible face / `Ø75 mm` panel-opening family, but the real four-piece batch controls all cuts, retainers, spigots and rear depths.

Exactly seven Schneider selectors are consolidated in one labelled 2 x 4 far-right bank with a separate red hazard: 3-position `WIPERS`, `LIGHTS`, `BLOWER`; 2-position `SPOTS`, `A/C`, `AUX`, `ENGINE`. `ENGINE` uses the former spare selector as a low-current RUN/STOP request only after EEI-003 proves the diesel fuel-stop logic; key OFF remains authoritative and the manual stop cable remains the emergency fallback. The bank does not duplicate OEM indicator/dip/horn controls, keyed ignition, washer input or winch lever. Cabin temperature/blend remains with the measured evaporator thermostat/controller and is not an eighth selector. Only the disposable full-size template is released before gates M1-M10; production vehicle metal, LCD, selector, hazard and vent apertures remain HOLD until physical tracing, bought-part measurement and rear-envelope mock-up are signed.

## Evidence Position

- Live Gmail MCP is not authenticated in this session. The usable Gmail-derived project extract is `data/processed/generated/gmail_project_messages_2026-06-01.json`.
- Live WhatsApp MCP is not exposed as a callable tool in this session. The usable WhatsApp project extract is `data/processed/generated/whatsapp_project_relevant_2026-06-01.csv`.
- Owner reports a condenser has been bought and is expected to fit in the front compartment/front cooling stack. Exact condenser product, dimensions, fitting side, and order proof still need confirmation before final drier/fan/hose release.
- Existing A/C control position remains: hidden or slimline cabin evaporator, external/owner-selected blowers where practical, and no final dash cuts or hose crimps before physical mock-up.

## Layout Decision

Use a four-outlet cabin plan unless the purchased evaporator case proves it cannot support it:

| Outlet group | Quantity | Position | Preferred vent type | Duct rule |
| --- | --- | --- | --- | --- |
| End pair | 2 | One in each end-adjacent rounded drop, close to the usable flat-face ends and never in the side returns/A-pillars | Matched circular directional louvers with satin-silver `Ø87 mm` reference faces, flush to +0.5 mm | Balanced supported branches from the evaporator/plenum; prove the end runs clear the glovebox, cluster, column and structure |
| Centre pair | 2 | Side-by-side in the broad rounded drop directly below the LCD | Same make, batch, face, louver and finish as the end pair | Short direct branches from the balanced plenum; preserve LCD connector/service clearance |

Do not buy random dashboard vents by appearance only. The vent neck OD must match the evaporator outlet/plenum standard. Use 2.5 inch duct as the default because the current reference HVAC components and louvers commonly use 2.5 inch hose. Use 2.0 inch only if the purchased unit physically provides 2.0 inch outlets and the airflow test still passes.

## Reference Parts

These are geometry/spec references and import fallbacks. A local Snow Cool/Arsalan/Cool Sun equivalent is acceptable if dimensions and hose necks match.

| Use | Reference | Why it matters |
| --- | --- | --- |
| Full front under-dash outlet panel | Vintage Air `492090` slimline universal under-dash louver panel | Four-louver flat under-dash concept; useful if avoiding visible holes in the original dash. |
| Compact double dash outlet | Vintage Air `63316-VUL` all-black double under-dash louver | 11.375 x 2.5 inch panel with 2.5 inch hose inlets; good model for the front pair. |
| Individual directional outlet | Vintage Air `49050-VUL` / `49350-VUL` style single under-dash louver | Good model for each side outlet if a full panel is too wide. |
| Round directional pod | Vintage Air `492083` or `49054-VUL` style 2.5 inch round under-dash pod | Useful geometry reference for the four integrated dash outlets because the ball/eyeball louver can be aimed at occupants. |
| Duct hose | Vintage Air `06250-VUE`, `318005`, `318010` style 2.5 inch duct hose | Buy after mock-up, with enough total length to cover all four outlet paths plus service slack. |
| Adapters | 2.5 inch oval glue-on adapters and 2.5 inch Y connectors only if needed | Use only after the evaporator outlet count is known; Y-splitting reduces flow and should be airflow-tested. |

## Buy Specification

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
- Any release of production dashboard metal, LCD, control or vent apertures before the actual dashboard, transferred OEM parts and bought components are measured and the evaporator, plenum, blower, four duct paths, bend radius and rear clearances are mocked with the Rev G full-size template.

## Shop Call Text

Need four identical directional A/C outlets from one batch for an old Land Cruiser CNC dashboard. Use circular satin-silver faces with black directional cores, hidden rear retention and no exposed front screws. Current reference is approximately 87 mm face / 75 mm panel opening, with a 2.5 inch hose-neck preferred, but please do not substitute by appearance. Send tape-measure/caliper photos of face diameter, required panel cutout, rear hose-neck OD, total rear depth, retainer, louver movement, shutoff and four-piece price. Also quote matching flexible automotive HVAC duct, clamps and any adapters/Y pieces. No dashboard holes or hose sizes are final until these four samples and the evaporator outlets are measured and mocked up.

## Sources Checked

- Vintage Air `492090` slimline universal under-dash louver panel reference: https://fuelcurve.com/vintage-air-universal-ultra-slim-under-dash-louver-panel-kit/
- Vintage Air `63316-VUL` double under-dash louver reference: https://vintageair.com/double-under-dash-louver-assembly-for-2-5-inch-hose-all-black/
- Vintage Air `492083` round single louver kit reference: https://vintageair.com/slimline-recessed-under-dash-round-universal-single-louver-kit-for-2-5-inch-hose/
- Vintage Air catalog, under-dash louvers, adapters, and duct hose stock: https://vintageair.com/content/2023%20Vintage%20Air%20Catalog.pdf
- Generic cost-reference vent family, published `Ø87 mm` face / `Ø75 mm` opening: https://www.joom.com/en/products/68c8f9fa6dffb3012ca80d30
