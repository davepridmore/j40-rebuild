# Body Mount Order Release Plan - 2026-05-02

Purpose: make the body-mount rubber, stop/seat, shim, sleeve, and bolt order executable while marking the few items that still need direct physical confirmation.

Order-line sheet: [body_mount_order_release_specs.csv](../data/manual/body_mount_order_release_specs.csv)

Action sheet: [body_mount_release_actions.csv](../data/manual/body_mount_release_actions.csv)

Station closure sheet: [body_mount_station_closure_sheet.csv](../data/manual/body_mount_station_closure_sheet.csv)

Manufacturing requirements sheet: [rubber_recreation_manufacturing_requirements.csv](../data/manual/rubber_recreation_manufacturing_requirements.csv)

## Route Decision

There are two valid routes. Do not buy both.

| Route | Use When | Active Lines |
| --- | --- | --- |
| OE/reproduction purchase | Supplier can confirm the part-number package fits this exact early J40 body and station count | `BM-OE-001` to `BM-OE-014` |
| Local fabrication | Physical samples are being copied and OE kit fit is uncertain, unavailable, or too expensive | `BM-FAB-001` to `BM-FAB-005`, plus hardware/shims |

The route decision is currently blocked by `BMA-001` and `BMA-002`: lay out the old parts by station and choose OE/reproduction or local fabrication.

## Exact OE/Reproduction Quote Candidate

Use this as the quote list only after the station count is confirmed. Source: WhatsApp-derived quote candidate from April 17, 2026, cross-checked against the Toyota/EPC-style station references already captured in the project.

| Item | Part Number | Qty |
| --- | --- | ---: |
| Body mount cushion NO.1 | `52201-90300` | `4` |
| Body mount cushion NO.2 | `52202-90300` | `4` |
| Body mount cushion NO.3 | `52203-90300` | `2` |
| Body mount cushion NO.4 | `52204-90300` | `2` |
| Body mount cushion NO.5 | `52208-90300` | `4` |
| Body mount collar | `90540-17045` | `2` |
| Body mount stopper/seat | `52023-60010` | `4` |
| Washer/seat | `90560-12009` | `6` |
| Washer/seat | `90560-12233` | `4` |
| Body mount spacer | `52228-22010` | `6` |
| Bolt | `90109-10039` | `2` |
| Bolt | `90105-10053` | `2` |
| Bolt | `90119-10123` | `4` |
| Bolt | `90101-10463` | `2` |

Hold before buying:
- Confirm the old parts actually match this `16` cushion/seat-piece package.
- Ask the supplier for the exploded diagram or station map that matches these part numbers.
- Do not substitute bolt lengths locally from these part numbers alone; open catalog listings confirm identities but not lengths.

## Exact Local Fabrication Specs

These are ready for quote/prototype. Production release still needs the marked physical checks.

| Code | Item | Qty | Spec |
| --- | --- | ---: | --- |
| `BM-LG` | Large circular body-mount cushion | `2` | `78 mm` OD, `24 mm` free height, `32 mm` bore/register, `46 mm` centre register OD x `2 mm` depth, outside radius `R2-R3`, Shore A `60 +/-5` |
| `BM-SM` | Small circular body-mount cushion | `10` | `64 mm` OD, working `22 mm` free height if one-piece, `32 mm` bore/register, `46 mm` centre register OD x `2 mm` depth, outside radius `R2-R3`, Shore A `60 +/-5` |
| `FS-OVAL` | Front support oval isolator pad | `2` | `96 mm` length, `64 mm` max width, `15 mm` thickness, two `12 mm` holes, `64 mm` hole centres, `36 x 18 mm` rectangular relief with `R3` corners, `29 mm` top boss/insert OD |
| `FS-STRIP-L` | Front support left strip/liner | `1` | working trace length `165 mm`, width `38-42 mm`, base thickness `8 mm`, raised/load pad height `14 mm`, M10 clearance hole `11 mm` or slot `11 x 16 mm` where shown |
| `FS-STRIP-R` | Front support right strip/liner | `1` | mirror `FS-STRIP-L` unless physical carrier proves asymmetry |

Material for all local rubber pieces: new black automotive mount-grade `EPDM` or `NR/SBR`, Shore A `60 +/-5`, no tyre rubber, crumb rubber, mixed offcuts, used rubber, or old salvage rubber.

Local fabrication also requires the first-article, material, process, inspection, rejection, and packaging controls in [rubber_recreation_manufacturing_requirements.csv](../data/manual/rubber_recreation_manufacturing_requirements.csv). The fabricator must provide a material declaration and a one-page inspection report before the batch is accepted.

Main production hold: `BM-SM` must be confirmed as either one `22 mm` piece or a split bushing plus seat stack.

## Exact Hardware And Shim Order

These are the local order packs unless the OE/reproduction package includes matching parts.

| Line | Item | Qty To Order | Spec |
| --- | --- | ---: | --- |
| `BM-HW-001` | Main body mount sleeves/crush tubes | `8 blanks` | ID `10.8-11.0 mm` for M10 bolt; OD and cut length held until old sleeve/dry-stack measurement |
| `BM-HW-002` | Cup/seat washers | `14` | `10` small at `64 mm` OD, `2` large at `78 mm` OD, plus `2` spare; `11 mm` hole, `2-3 mm` dish/register depth, `2.5-3.0 mm` steel |
| `BM-HW-003` | M10 bolt length trial pack | `16` | M10 x `1.25`, class `8.8` minimum: `70 mm x4`, `80 mm x4`, `90 mm x4`, `100 mm x4` |
| `BM-HW-004` | M10 nuts/washers/repair pack | `1 pack` | all-metal nuts x`12`, nyloc nuts x`12`, flat washers x`40`, spring washers x`20`, M10 x `1.25` weld nuts x`4`, `3 mm` repair tabs x`4` |
| `BM-HW-005` | M12 front-support/repair pack | hold | Buy only if front support proves M12. If verified: bolts x`4`, nuts x`6`, flat washers x`12`, spring washers x`6` in measured pitch/length |
| `BM-SHIM-001` | Thin M10 alignment shims | `1 pack` | slotted flat steel: `1 mm x12`, `2 mm x12`, `3 mm x12`, `5 mm x12`; slot `11-12 mm`; full pedestal footprint |
| `BM-SHIM-002` | Thick OE-style spacer control pack | `1 pack` | `5 mm x4`, `10 mm x4`, `15 mm x4`; record `22.8 mm` and `27.8 mm` OE references but cut/buy only if original station map proves need |

## Things You Need To Do

These are the open actions that still block final release:

1. `BMA-001`: lay out every old body-mount part by station and photograph it.
2. `BMA-002`: choose OE/reproduction package or local fabrication; mark the other route do-not-order.
3. `BMA-003`: measure the current stopper/seat pieces and match them to `52023-60010`, `90560-12009`, or `90560-12233` if using OE route.
4. `BMA-004`: caliper-measure the best large and small circular cushions.
5. `BMA-005`: prove whether the small mount is a one-piece `22 mm` cushion or a split stack.
6. `BMA-006`: measure sleeve ID, OD, and length, or dry-stack and derive sleeve length.
7. `BMA-007`: thread-gauge body-mount bolts and captive nuts; measure usable captive nut depth.
8. `BMA-008`: preserve and measure original shim/spacer packs by station.
9. `BMA-009`: trace front-support left/right strips from physical pieces.
10. `BMA-010`: confirm front-support fastener diameter and pitch before any M12 order.
11. `BMA-011`: dry-stack one large station, one small station, and one front-support station before final sleeve cutting and bolt-length selection.

Record the results in [body_mount_station_closure_sheet.csv](../data/manual/body_mount_station_closure_sheet.csv).

## Source Controls

- Toyota/EPC-style body mounting listing: [ToyotaPartsDeal 1978 Land Cruiser Cab Mounting & Body Mounting](https://www.toyotapartsdeal.com/parts-list/1978-toyota-land_cruiser/body/cab_mounting_body_mounting.html)
- Existing project OE cross-reference: [rubber_recreation_toyota_oe_cross_reference.csv](../data/manual/rubber_recreation_toyota_oe_cross_reference.csv)
- Existing project measurement closure: [rubber_recreation_measurement_closure.csv](../data/manual/rubber_recreation_measurement_closure.csv)
- Candidate WhatsApp quote source: `data/processed/generated/mcp_whatsapp_j40_messages.json.before_20260501T001520`
