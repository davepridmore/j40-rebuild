# Rubber Hose Component Readiness Audit - 2026-05-03

Purpose: check the rubber hoses/components visible in the current image sets and confirm that each has an open replacement item plus fabrication/order dimensions or a controlled measurement hold.

Primary audit table: [rubber_hose_component_audit.csv](../data/manual/rubber_hose_component_audit.csv).

## Readiness Position

The rubber hose set is not ready to send as one direct acquisition package yet. It is ready as a controlled measurement package: every visible family now has an open item, but most hose purchases still require caliper dimensions in `mm` before payment.

The only rubber items with usable fabrication dimensions today are the body/front-support rubber recreation parts:

- Small circular body-mount cushions: `10` pieces, `64 mm` OD, `22 mm` working free height, `32 mm` bore/register, `46 mm x 2 mm` center register, `R2-R3` edge, Shore A `60 +/-5`.
- Large circular body-mount cushions: `2` pieces, `78 mm` OD, `24 mm` free height, `32 mm` bore/register, `46 mm x 2 mm` center register, `R2-R3` edge, Shore A `60 +/-5`.
- Front two-hole oval isolators: `2` pieces, `96 mm x 64 mm x 15 mm`, two `12 mm` holes at `64 mm` centers, `36 x 18 mm` relief with `R3` corners, `29 mm` boss/insert OD.
- Front support strip rubbers: left/right quote basis `165 mm` trace length, `38-42 mm` width, `8 mm` base thickness, `14 mm` raised pad height, M10 `11 mm` holes or `11 x 16 mm` slots. Final cutting still requires physical tracing.

## Gaps Closed

The image review found two items that were visible but not explicit enough in the order controls:

- Formed coolant pipe rubber connector/coupler hoses: now tracked as `RP-COOL-006`, `RPO-COOL-006A`, `RPO-COOL-006B`, and `RUB-028`.
- Engine air-cleaner intake duct/couplers: now tracked as `RUB-027` so it is inspected separately from coolant, fuel, vacuum, and HVAC hose.

## Direct Acquisition Gate

Do not send these for direct purchase until the listed measurements are recorded:

- Coolant/radiator/heater/overflow hoses: neck or nipple OD, hose OD for clamps, route length/free length, and bend clearance in `mm`.
- Formed-pipe connector hoses: each connector ID/OD, free/cut length, pipe-end OD/bead, mating spigot OD, overlap, clamp band width, and kink clearance in `mm`.
- Fuel hoses: each barb/nipple OD, route length, hose OD for clamps, and printed diesel rating.
- Vacuum/breather/oil hoses: barb/spigot OD, route length, oil exposure, collapse resistance, and check-valve direction.
- Brake/clutch flex hoses: complete assembly length, end fitting/thread/seat, bracket retention, and full-droop or drivetrain movement clearance.
- Air-intake duct: air-cleaner outlet OD, intake inlet OD, free length, offset, accordion/compression travel, branch/nipple OD, and clamp OD.

## Open Item Coverage

All visible/current rubber families are now mapped:

- Cooling: `RP-COOL-001` through `RP-COOL-006`, `RUB-013`, `RUB-014`, `RUB-015`, `RUB-028`.
- Fuel: `RP-FUEL-001`, `RUB-011`, `RUB-012`.
- Vacuum/breather/oil mist: `RP-VAC-001`, `RUB-016`.
- Brake/clutch hydraulics: `RP-BRAKE-001`, `RP-CLUTCH-001`, `RUB-009`, `RUB-010`.
- Engine intake: `RUB-027`.
- Body/front support rubber recreation: `CR-MAIN-001` through `CR-FRONT-003`, `RUB-001`, `RUB-002`.
- Grommets/weatherstrip/body sealing: `RUB-003`, `RUB-004`, `RUB-017` through `RUB-021`.
- HVAC/A/C rubber: `RUB-024`, `RUB-025`.
- Suspension/exhaust/interior rubber: `RUB-007`, `RUB-022`, `RUB-023`, `RUB-026`.

## Next Measurement Pass

Use [replacement_pipe_photo_intake.csv](../data/manual/replacement_pipe_photo_intake.csv) for hose/pipe close-ups and [rubber_hose_component_audit.csv](../data/manual/rubber_hose_component_audit.csv) for the cross-category checklist. The key new shots are `RPI-COOL-006-A`, `RPI-COOL-006-B`, and `RPI-COOL-006-C` for the formed-pipe connector hoses.
