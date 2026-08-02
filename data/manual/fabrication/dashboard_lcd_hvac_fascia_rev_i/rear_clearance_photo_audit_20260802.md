# Rev I V35 rear-of-dashboard clearance audit — 2026-08-02

**Status: quotation input only; production vehicle cuts and component apertures remain HOLD.**

This audit records the three photographs imported through the Google Photos Picker run `20260802T153617`. They show useful local structure behind the dashboard, but they do not show the finished rear-fascia datum, either proposed outer vent centre, or a complete LCD/vent/duct assembly. They therefore support a conservative quotation buck; they do **not** prove production fit.

Use this audit with the [rear-package clearance control diagram](rear_package_clearance_control.svg), [V35 quotation CNC specification](dashboard_rev_i_v35_quotation_cnc_spec.md), and [fillable measurement schedule](cnc_measurement_schedule.csv).

## Decision

| Question | Decision | Reason |
| --- | --- | --- |
| Does the nominal vent louver body fit the photographed local cavity? | **Provisionally plausible / no contradiction** | The supplied approximately 22 mm louver-body projection is well below the smallest apparent tape span of about 125–130 mm. This comparison applies to the body alone and only to the photographed ray. |
| Does either complete outer vent installation fit? | **Not proven — HOLD M7/M9** | Neither planned outlet centre is identified. Retainer, spigot, clamp, hose, first bend, aim/shutoff sweep and removal path are absent. |
| What LCD depth may be used for quotation? | **115 mm maximum total installed projection behind the finished rear-fascia plane, ASSUMED/UNVERIFIED** | Conservative quotation cap derived from a 125 mm rounded-down apparent local span less the required 10 mm fixed clearance. It is not a production measurement. |
| What LCD chassis should be procured within that quotation envelope? | **Target integral chassis/body projection, including any integral rear heat sink, no more than 80 mm** | Leaves at least 35 mm within the 115 mm quote envelope for the external carrier/mounts, fasteners, largest fully mated connector, cable bend/service loop and removal tolerance. Verify the actual product drawing. |
| What is the production LCD maximum? | **Not released** | It must be calculated from a perpendicular depth map at the actual LCD envelope and nearest obstruction, then proven with the actual assembly in the full-depth buck. |

## Imported photographic evidence

| Photograph | What can be read | Confidence and limitation |
| --- | --- | --- |
| [20260802_145250_gp_4wxWxPmA.jpg](../../../../photos/20260802_145250_gp_4wxWxPmA.jpg) | An oblique tape ray crosses a local lower ledge at approximately 125–130 mm from the hook end | **Low.** The hook/zero is not tied to the finished rear-fascia plane, the endpoint is not named, and the ray is not shown at either vent or the LCD service envelope. |
| [20260802_145305_gp_bepTxJOA.jpg](../../../../photos/20260802_145305_gp_bepTxJOA.jpg) | A visible endpoint reading of roughly 270–280 mm near the right upright; this is not a measured span | **Low.** The zero/start is out of frame—the visible tape begins around the 4-inch region—so no available distance can be calculated, and the component location is not registered to the front face. |
| [20260802_145316_gp_tJASS8hQ.jpg](../../../../photos/20260802_145316_gp_tJASS8hQ.jpg) | An oblique local lower-ledged-to-upper-structure span of approximately 160–170 mm | **Low.** The endpoints and front-fascia datum are not declared, and the measurement is not at a planned outlet centre. |

Machine-readable evidence and restrictions are in [rear_clearance_photo_evidence_20260802.csv](rear_clearance_photo_evidence_20260802.csv).

## Controlled Z-datum and installed-depth definitions

Set `Z=0` on the **finished rear surface of the fascia or centre cassette**, local to the component being checked. `+Z` runs rearward. All depths must be measured perpendicular to that local surface; a diagonal tape reading is not `Z` clearance.

### LCD

`P_LCD_INSTALLED` is the greatest rearward `Z` reached by **any** part of the installed and serviceable LCD package:

- module and rear chassis;
- carrier, mounts and all fasteners;
- heat sink and required ventilation keep-out;
- largest fully mated plug/adapter;
- cable bend radius and retained service loop; and
- cabin-side release/removal sweep where that sweep moves rearward.

The owner-supplied **5.0 mm** figure is the generic LCD module/panel thickness only. It is **not** the installed-depth specification.

Quotation-only constraint:

`P_LCD_INSTALLED,Q ≤ 115 mm`, with `P_LCD_CHASSIS target ≤ 80 mm`; `P_LCD_CHASSIS` includes the integral screen chassis/body and any integral rear heat sink.

Production constraint:

`P_LCD_INSTALLED,PROD ≤ min[Z_FIXED(x,y) over the complete installed and removal envelope] − 10 mm`.

Any steering column, shroud, stalk or other moving envelope requires at least **20 mm** clearance instead of 10 mm. The final production maximum is the smaller result after both fixed and moving-envelope checks. If the purchased screen's connector exits rearward, its plug and minimum permitted bend radius are included in the depth—not routed into the clearance reserve after the fact.

### A/C outlets

`P_VENT_INSTALLED` is the greatest rearward `Z` reached by the louver body, retention hardware, anti-rotation feature, adapter/spigot, clamp, hose outside diameter, first bend, duct support, full aim/shutoff sweep and cabin-side removal path.

At each actual vent centre and over its complete rear swept envelope:

`P_VENT_INSTALLED ≤ min[Z_FIXED(x,y)] − 10 mm`.

Maintain at least **20 mm** to the signed moving column/shroud/stalk envelope. The nominal Ø87 face still needs a minimum Ø107 unobstructed front land (10 mm visible/structural clearance all around), while the Ø75 rear target remains an unreleased mounting interface—not a hose size and not a production cut diameter.

## Measurements required to close the fit decision

1. Mark the final V1 passenger and V2 driver centre points on the front face from the signed M1 trace. Photograph each mark from the front and rear.
2. At each centre, hold a rigid square or depth bridge on the finished rear-fascia datum and measure perpendicular `Z` to the nearest obstruction across the full Ø75 mounting boss, retention hardware, adapter, clamp and first-bend swept envelope.
3. Repeat with the actual selected outlet, retainer, adapter, hose and clamp assembled. Record `P_VENT_INSTALLED`, closest fixed clearance and closest moving-envelope clearance.
4. For the LCD, record perpendicular `Z_FIXED` at the four chassis corners, centre, mounting points, connector exit and planned cable-turn zone. Photograph the zero datum and obstruction in the same frame.
5. Install the actual LCD, carrier, largest mated connector, cable loop, all eight controls, both complete vent branches, glovebox and cluster in the rigid buck. Exercise glovebox, vents and complete steering/stalk movement and prove cabin-side removal.

Until those measurements are entered in M5, M7 and M9, the correct release statement is: **front-face packaging plausible; complete rear fit not yet ensured; production CNC HOLD.**
