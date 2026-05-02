# Suspension Workstream - Ironman Foam Cell Kit

- Updated: 2026-05-03
- Workstreams: `steering_brakes_suspension`, `suspension_upgrade`
- Current state: ordered, pending delivery
- Active path: Ironman Foam Cell medium suspension kit for Toyota Land Cruiser 40 Series
- Order evidence: `data/manual/procurement_queue.csv`, `data/manual/orders_receipts_audit_queue.csv`, `data/manual/workstream_status.csv`

## Decision

The suspension path is now the incoming Ironman Foam Cell set. The previous local fabricated leaf-spring path, OME/EMU shock path, Bilstein path, separate generic bush path, separate shackle path, and separate U-bolt path stay out of active buying unless the Ironman receipt check proves a missing, damaged, or incorrect component.

Do not start final installation until both shipments are physically present: the main Ironman kit and the separate front damper pair.

## Incoming Set

| Part | Qty | Role | Receipt check |
| --- | ---: | --- | --- |
| `TOY001B` | 2 | Front leaf springs | Confirm labels, matched pair, spring-eye width, center pin, clamps, and no transit damage. |
| `TOY002B` | 2 | Rear leaf springs | Confirm labels, matched pair, spring-eye width, center pin, clamps, and no transit damage. |
| `24635FE` | 2 | Front Foam Cell dampers, separate shipment per project tracker | Do not road-test without this pair; verify eye/bush hardware and body clearance before fitment. |
| `24636FE` | 2 | Rear Foam Cell dampers | Verify eye/bush hardware and full-droop clearance before fitment. |
| `415UBK` | 4 | U-bolt kits | Use new U-bolts only; reject any bent threads, damaged nuts, or wrong axle-seat width. |
| `713UK` | 1 kit | Polyurethane spring bush kit | Count every bush, sleeve, washer, and greaseable contact part before installation; do not assume the count is complete from the label alone. |
| `343LH` | 1 listed | Greasable shackle, left-hand side | Confirm actual side/axle position against box instructions before fitting. |
| `343RH` | 1 listed | Greasable shackle, right-hand side | Confirm actual side/axle position against box instructions before fitting. |
| `346` | 2 listed | Greasable front spring pins | Confirm thread, sleeve fit, nipple position, and grease passage before fitting. |
| `3523` | 1 | Steering damper | Fit after spring/shock geometry is settled; verify lock-to-lock clearance. |

Official cross-checks:

- Ironman global `TOY001BKF` page currently lists the LC 40 medium Foam Cell kit with `415UBK`, `713UK`, `TOY001B`, `24635FE`, `24636FE`, and `TOY002B`: https://ironman4x4.global/products/foam-cell-suspension-kit-toy001bkf
- Ironman fitting instructions page points to vehicle-specific fitting instructions and templates: https://ironman4x4.global/pages/fitting-instructions
- Ironman USA `343LH` greasable shackle page: https://www.ironman4x4.com/products/front-rear-greasable-shackle-lhs-toyota-land-cruiser-40-series-1960-1980-343lh40lc
- Ironman USA `713UK` bushing page: https://www.ironman4x4.com/products/front-or-rear-polyurethane-spring-bushing-kit-toyota-land-cruiser-40-series-1960-1980-713uk40lc
- Ironman USA `3523` steering damper page: https://www.ironman4x4.com/products/steering-damper-toyota-land-cruiser-40-series-1960-1980-352340lc
- Ironman USA pins/shackles listing includes `346-40LC`: https://www.ironman4x4.com/collections/pins-shackles
- Ironman USA product pages state that manuals may be in the box or downloadable from the Vehicle Fitment/User Guide tab; if missing, contact Ironman support before fitting.

## Installation Control Rule

The boxed Ironman instructions and the Toyota factory service manual control torque values and any vehicle-specific sequence. This document is the project work instruction and gate list; it does not replace the supplier manual, the OEM manual, or professional workshop judgement.

Before touching the truck, the mechanic must write a one-page torque sheet from the Ironman instructions and Toyota manual covering:

- Front and rear spring eye bolts/pins.
- Shackle nuts.
- U-bolt nuts.
- Shock absorber mounts.
- Steering damper mounts.
- Wheel nuts.
- Any brake-line, parking-brake, or line-clip brackets disturbed during the job.

No torque sheet means no installation.

## Pre-Install Gates

1. Photograph every incoming label, part number, batch/date mark, and hardware bag before opening.
2. Count the kit against the incoming-set table and the supplier invoice.
3. Preserve all old springs, shackles, pins, plates, and U-bolts until the Ironman kit is fully installed and validated.
4. Confirm all chassis spring hangers, shackle mounts, steering-box mount area, axle spring pads, and U-bolt plates are clean and crack-free.
5. Stop for repair if any spring hanger is cracked, ovalized, bent, deeply pitted, or has damaged captive hardware.
6. Confirm brake flexible hoses, brake hard lines, parking-brake cables, breather hose, and wiring have slack at expected full droop.
7. Confirm safe support gear is present: 3T trolley jack, four rated jack stands, hardwood cribbing blocks, wheel chocks, and a level working surface.
8. Confirm tools: torque wrench in the required range, breaker bar, metric sockets/spanners, pry bars, hammer/mallet, punch/drift, grease gun, penetrating oil, paint marker, calipers/tape, and camera.
9. Confirm consumables: supplied/suspension-compatible bush grease, chassis grease for nipples, anti-seize only where the supplier permits, thread cleaner/chaser, and new split pins/retainers where used.
10. Confirm the separate `24635FE` front damper shipment has arrived before final assembly or road validation.

## Baseline Measurements

Record these before removing anything:

- Ride height at all four corners, measured from wheel hub center to guard edge or a fixed body datum.
- Bump-stop clearance at all four corners.
- Shackle angle on each corner.
- Wheelbase left and right.
- Axle location relative to spring center pins.
- Front steering lock-to-lock clearance.
- Brake hose and parking-brake cable slack at static height.
- Rear pinion angle and propshaft slip-yoke exposure if tools are available.
- Current tyre size, wheel offset, and any visible tyre-to-body clearance issue.

Use the same measurement points after installation, after first road test, and after the 500 km recheck.

## Front Axle Procedure

1. Work on one axle at a time. Chock the rear wheels, loosen front wheel nuts, lift the chassis, and set the chassis on rated stands. Keep the front axle supported separately with the jack.
2. Remove the front wheels for access.
3. Support the axle so the spring is neutral, not hanging from the brake hoses.
4. Photograph the original spring, shackle, fixed pin, U-bolts, shock, steering damper, brake hose route, and line clips.
5. Remove the front shocks and steering damper if they restrict access. Keep original hardware labelled until the Ironman hardware is confirmed.
6. Free any brake-line or breather brackets that would be stretched during axle droop. Do not open hydraulic brake lines unless brake work is intentionally being done.
7. Remove the old U-bolts and nuts. Treat old U-bolts as scrap; do not reuse them.
8. Lower/support the axle just enough to separate it from the spring center pin.
9. Remove the shackle and fixed-pin fasteners, then remove the old spring pack.
10. Clean hanger bores, shackle brackets, spring pads, and U-bolt plates. Check for cracks, oval holes, and crushed or bent plates.
11. Install Ironman bushes and sleeves into `TOY001B` springs using supplied or polyurethane-compatible grease only.
12. Fit the `TOY001B` spring to the fixed hanger and shackle with the correct side/orientation confirmed from the Ironman sheet. Leave spring-eye and shackle fasteners finger tight.
13. Fit greasable pins/shackles so nipples are reachable and protected. Confirm the grease passages take grease before final road use.
14. Raise the axle onto the spring center pin. The pin must fully seat in the axle pad before U-bolt tightening starts.
15. Install new `415UBK` U-bolts, plates, washers, and nuts. Tighten gradually in a cross pattern to the Ironman/OEM torque sheet.
16. Install the `24635FE` front dampers with supplied bushes/washers/spacers in the correct order. Leave final bushing crush and pivot torque until the vehicle is at ride height unless the Ironman sheet says otherwise.
17. Install the `3523` steering damper after the spring and shock are in place. Turn steering lock-to-lock and confirm no binding, drag-link contact, hose stretch, or damper body contact.

## Rear Axle Procedure

1. Chock the front wheels, loosen rear wheel nuts, lift the chassis, and support the chassis on rated stands. Support the rear axle separately.
2. Remove the rear wheels for access.
3. Photograph the original rear spring, shackle, fixed pin, U-bolts, shock, brake hose, parking-brake cable, breather, and rear axle hard-line routing.
4. Free any brake-line, parking-brake, or breather brackets that would be stretched during droop.
5. Remove rear shocks if they limit droop or access.
6. Remove old U-bolts and nuts. Scrap the old U-bolts.
7. Support the axle, separate it from the spring center pin, and remove the old rear spring pack.
8. Clean rear hanger bores, shackle brackets, spring pads, and U-bolt plates. Stop for repair if any bracket is cracked, ovalized, or visibly distorted.
9. Install Ironman bushes and sleeves into `TOY002B` springs using supplied or polyurethane-compatible grease only.
10. Fit the `TOY002B` spring to the fixed hanger and shackle, leaving spring-eye and shackle fasteners finger tight.
11. Seat the rear axle on the spring center pin and install new `415UBK` U-bolts. Tighten evenly in a cross pattern to the torque sheet.
12. Install the `24636FE` rear dampers with supplied bushes/washers/spacers in the correct order. Leave final bushing crush and pivot torque until the vehicle is at ride height unless the Ironman sheet says otherwise.
13. Check rear brake hose, rear hard lines, parking-brake cable, breather hose, propshaft slip travel, and exhaust clearance at static height and supported droop.

## Final Settle And Torque

1. Refit wheels and lower the vehicle onto its tyres at normal build weight.
2. Bounce/settle each corner and roll the vehicle forward/back to release spring bind.
3. Torque spring-eye fasteners, shackle fasteners, shock mounts, steering damper mounts, and wheel nuts from the torque sheet.
4. Paint-mark every torqued fastener.
5. Grease all greasable shackles and pins until grease has reached the bearing surface; wipe excess grease away from brake parts.
6. Recheck U-bolt torque after the first settle cycle.
7. Recheck steering lock-to-lock, brake hose slack, parking-brake cable slack, breather slack, tyre clearance, shock body clearance, and bump-stop alignment.
8. Measure and record ride height, bump-stop clearance, shackle angle, and wheelbase again.
9. Align steering and suspension through a qualified alignment shop. Headlights must also be aimed again because ride height has changed.

## Road Validation

1. First movement is a low-speed yard test only: braking, steering, reverse, slow turns, and listen for clunks.
2. Stop and inspect every spring eye, shackle, U-bolt plate, shock mount, steering damper mount, brake hose, and parking-brake route.
3. Run a short road test at low speed, then inspect again.
4. If there is steering pull, brake pull, driveline vibration, spring clunk, shock contact, brake hose tension, or axle shift, stop road use and correct before further driving.
5. After 50 km, recheck U-bolt torque, spring/shackle torque marks, shock mounts, steering damper mounts, ride height, shackle angle, and all hose/cable clearances.
6. After 500 km, repeat the full torque and visual inspection, then record final settled ride height.

## No-Go Conditions

- Any missing Ironman instruction sheet and no replacement PDF from supplier/support.
- Any missing or unmatched `24635FE` front damper pair.
- Wrong spring pair, mixed left/right hardware, damaged bush sleeves, or incomplete U-bolt hardware.
- Chassis spring hanger cracks, ovalized holes, broken welds, or distorted shackle brackets.
- Brake hose, breather, parking-brake cable, or wiring tension at droop.
- Shock body contact, steering damper bind, tyre contact, or insufficient bump-stop engagement.
- No torque sheet, no torque wrench, or no post-install torque record.

## Closeout Evidence

Store these before closing the workstream:

- Receipt/invoice and shipment photos for both Ironman deliveries.
- Parts laid out by axle before installation.
- Baseline measurements.
- Hanger/spring-pad inspection photos after cleaning.
- Installed front and rear springs, shocks, U-bolts, shackles, pins, and steering damper.
- Torque sheet with final torque marks noted.
- Alignment record.
- 50 km and 500 km recheck records.
