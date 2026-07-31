# HVAC Dashboard Vent And Duct Layout - 2026-06-02

Purpose: convert the new condenser/cabin airflow direction into a buyable vent and duct plan for the J40 A/C retrofit.

## 2026-07-31 Dashboard Integration Update

The controlled front-pair integration is now [dashboard_lcd_hvac_fascia_rev_c](../data/manual/fabrication/dashboard_lcd_hvac_fascia_rev_c/README.md). The right-hand-drive glovebox and instrument/speedometer pressing remain original. The compact CNC insert covers the deleted ashtray and radio zone, carries a true-scale 9-inch LCD reference and three selectors, while four further selectors reuse the original right-side 2 x 2 holes. Two directional eyeball outlets mount separately below the dash and retain the `63.5 mm / 2.5 inch` hose-neck preference. Production geometry remains HOLD until the actual parts, right-side hole centres and rear envelope are measured and owner-approved at 1:1. The other two outlets in the four-outlet plan remain rear/pillar outlets.

## Evidence Position

- Live Gmail MCP is not authenticated in this session. The usable Gmail-derived project extract is `data/processed/generated/gmail_project_messages_2026-06-01.json`.
- Live WhatsApp MCP is not exposed as a callable tool in this session. The usable WhatsApp project extract is `data/processed/generated/whatsapp_project_relevant_2026-06-01.csv`.
- Owner reports a condenser has been bought and is expected to fit in the front compartment/front cooling stack. Exact condenser product, dimensions, fitting side, and order proof still need confirmation before final drier/fan/hose release.
- Existing A/C control position remains: hidden or slimline cabin evaporator, external/owner-selected blowers where practical, and no final dash cuts or hose crimps before physical mock-up.

## Layout Decision

Use a four-outlet cabin plan unless the purchased evaporator case proves it cannot support it:

| Outlet group | Quantity | Position | Preferred vent type | Duct rule |
| --- | --- | --- | --- | --- |
| Front pair | 2 | Driver/passenger lower dash or very shallow under-dash panel | Low-profile directional louvers, preferably black or paintable | Short, direct 2.5 inch hose runs from evaporator/plenum |
| Rear/pillar pair | 2 | Just behind the front-door pillar / rearward side of front cabin area | Individual directional eyeball/pod vents | Longer 2.5 inch hose runs, supported and swept, not crushed or drooped |

Do not buy random dashboard vents by appearance only. The vent neck OD must match the evaporator outlet/plenum standard. Use 2.5 inch duct as the default because the current reference HVAC components and louvers commonly use 2.5 inch hose. Use 2.0 inch only if the purchased unit physically provides 2.0 inch outlets and the airflow test still passes.

## Reference Parts

These are geometry/spec references and import fallbacks. A local Snow Cool/Arsalan/Cool Sun equivalent is acceptable if dimensions and hose necks match.

| Use | Reference | Why it matters |
| --- | --- | --- |
| Full front under-dash outlet panel | Vintage Air `492090` slimline universal under-dash louver panel | Four-louver flat under-dash concept; useful if avoiding visible holes in the original dash. |
| Compact double dash outlet | Vintage Air `63316-VUL` all-black double under-dash louver | 11.375 x 2.5 inch panel with 2.5 inch hose inlets; good model for the front pair. |
| Individual directional outlet | Vintage Air `49050-VUL` / `49350-VUL` style single under-dash louver | Good model for each side outlet if a full panel is too wide. |
| Round directional pod | Vintage Air `492083` or `49054-VUL` style 2.5 inch round under-dash pod | Better for the rear/pillar pair because the ball/eyeball louver can be aimed at occupants. |
| Duct hose | Vintage Air `06250-VUE`, `318005`, `318010` style 2.5 inch duct hose | Buy after mock-up, with enough total length to cover all four outlet paths plus service slack. |
| Adapters | 2.5 inch oval glue-on adapters and 2.5 inch Y connectors only if needed | Use only after the evaporator outlet count is known; Y-splitting reduces flow and should be airflow-tested. |

## Buy Specification

Ask suppliers for:

- Four directional automotive A/C vents/louvers with 2.5 inch hose necks: two low-profile front dash/under-dash vents and two smaller pod/eyeball vents for rearward/pillar positions.
- Black or paintable finish preferred. Avoid shiny chrome if it looks out of period against the J40 dash.
- Vent face dimensions, rear neck OD/ID, rear depth, louver movement range, shutoff ability, screw spacing, and photos with a tape measure.
- 2.5 inch flexible automotive HVAC duct hose, matching adapters, clamps, and any Y connectors needed after the evaporator outlet count is proven.
- Defrost/demist takeoff parts only after the evaporator/plenum position is known; do not steal all outlet area for face vents if demist is required.

Reject:

- Non-directional vents that cannot aim air at occupants.
- Vents with no hose neck or unknown hose size.
- Thin decorative plastic that cannot clamp a duct hose securely.
- Long rear runs made with small 2.0 inch hose unless airflow testing proves acceptable.
- Any dash cut before the purchased evaporator, plenum, blower, duct bend radius, and vent bezels have been cardboard-mocked in the vehicle.

## Shop Call Text

Need four directional A/C outlet vents for an old Land Cruiser hidden A/C installation. Prefer 2.5 inch hose-neck vents. Two should suit the lower dash or a slim under-dash panel for driver/passenger airflow. Two should be small directional pod/eyeball vents that can mount just behind the front-door pillar area, fed by longer duct hoses. Please send tape-measure photos of the face size, rear hose neck, depth behind the panel, screw holes, louver movement, and price. Also quote matching 2.5 inch flexible HVAC duct hose, clamps, and adapters/Y pieces, but final lengths are not cut until the evaporator and vent positions are mocked in the vehicle.

## Sources Checked

- Vintage Air `492090` slimline universal under-dash louver panel reference: https://fuelcurve.com/vintage-air-universal-ultra-slim-under-dash-louver-panel-kit/
- Vintage Air `63316-VUL` double under-dash louver reference: https://vintageair.com/double-under-dash-louver-assembly-for-2-5-inch-hose-all-black/
- Vintage Air `492083` round single louver kit reference: https://vintageair.com/slimline-recessed-under-dash-round-universal-single-louver-kit-for-2-5-inch-hose/
- Vintage Air catalog, under-dash louvers, adapters, and duct hose stock: https://vintageair.com/content/2023%20Vintage%20Air%20Catalog.pdf
