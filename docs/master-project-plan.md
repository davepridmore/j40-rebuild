# Master Project Plan

## Planning Baseline

- Project: 1978 Toyota Land Cruiser J40 rebuild
- Planning date: 2026-03-19
- This plan is built from the evidence already stored in this repo plus current Punjab Excise reference pages.
- Legal/admin items here are a control tracker, not a substitute for confirming the latest filing requirements before submission.

## Primary Objectives

- Close the ownership and vehicle-admin loop cleanly enough that the project can always prove legal status.
- Rebuild the truck in a sequence that favors structural integrity, weatherproofing, electrical reliability, and mechanical reliability before optional upgrades.
- Keep all removable parts, decisions, and vendor work traceable back to evidence.
- Capture every direct project cost, including admin fees, tools, shipping, consumables, labour, refunds, rework, and optional-upgrade spend.

## Current State From Evidence

- Admin spend has started: excise challan and vehicle inspection costs are already in the ledger.
- Ownership transfer is not yet evidenced as complete; seller biometric and transfer completion still need explicit tracking.
- Strip-down is underway or imminent: roof, doors, hood, back cabin, and interior components are being discussed as removable work packages.
- The current operating split is body and electrical at home, with heavier mechanical work expected through workshop contacts.
- Electrical reset is a live workstream. Multiple harness options, grommets, sleeving, fuse hardware, and audio-related line items have already appeared in chat evidence.
- Body and rust work is also live. Primer, seam sealer, bed lining, sound deadening, and floor repair materials are already on the shopping list.
- New photo evidence through `2026-04-20` shows wing removal/body-lift prep and underside access are mature enough to run body-off welding as an active track, with dedicated chassis and stripped-engine tracks in parallel.
- Steering feel is a known problem, but major steering or suspension upgrades should stay behind a decision gate until the mechanical baseline is inspected.

## Operating Rules

- No optional upgrade is approved until the baseline legal, structural, electrical, and mechanical gates are closed.
- Every removed part gets a photo, a label, and a storage location before it leaves the vehicle.
- Every spend event goes into the ledger the same day it happens.
- Every legal/admin step gets a row in the legal tracker with status, dependency, and evidence.
- Every vendor promise stays open until there is proof of order, delivery, completion, or payment.

## Phase Plan

| Phase | Status | Purpose | Exit Gate |
| --- | --- | --- | --- |
| `00_site_setup` | `in_progress` | Covered working area, storage bins, labels, and a repeatable intake process for removed parts and new purchases. | J40 can stay stripped without losing weather protection or part traceability. |
| `01_legal_admin` | `in_progress` | Track challan, inspection, biometric, transfer filing, plate position, and final document pack. | Ownership/admin file is complete enough for later proof, resale, insurance, and road-use questions. |
| `02_stripdown_cataloguing` | `in_progress` | Strip the truck in a controlled way and produce a visible map of what is removable, damaged, missing, or outsourced. | Shell, loose parts, and outbound panels are catalogued with photos and labels. |
| `03_body_chassis` | `in_progress` | Body-off and welding track: weld-zone mapping, structural rust cuts, patch fabrication, and corrosion stack sequencing. | Body is off and weld scope is signed off by zone with materials staged. |
| `03b_chassis_fixing` | `in_progress` | Chassis track (active after tub separation): clean and inspect rails/crossmembers/mounts, then execute frame repairs and protection closeout. | Chassis structural repairs are closed or explicitly approved with no unknowns remaining. |
| `04_electrical_reset` | `in_progress` | Remove junk wiring, define final architecture, buy only the core electrical materials, and install a documented harness. | Starting, charging, lights, horn, wipers, gauges, and required accessories work from a clean, documented loom. |
| `05_mechanical_baseline` | `in_progress` | Engine-while-stripped track: run service/inspection tasks while access is open (leaks, cooling, hoses, fluids, tune consumables). | Engine baseline maintenance is complete and post-service defects are logged. |
| `06_steering_brakes_suspension` | `queued` | Resolve steering slack, brakes, shocks, axle-side wear, and only then decide on power steering and other upgrades. | Steering and braking are safe, and any upgrade path is chosen with the baseline data in hand. |
| `07_interior_weatherproofing` | `queued` | Floor sealing, bed lining, sound deadening, foam, carpet, and interior refit only after leaks and rust are handled. | Cabin is sealed, quieter, and ready for final trim without trapping moisture. |
| `08_final_assembly_validation` | `queued` | Reassemble, close punch-list items, validate drivability, and tie all evidence back to the project archive. | Reassembled truck passes road and function checks with open defects logged or closed. |
| `09_optional_upgrades` | `backlog` | Android unit, audio, premium shocks, and other non-essential extras that should not distort the baseline budget. | Optional work is approved only after baseline completion and explicit budget sign-off. |

## Scope By Workstream

### Legal/Admin

- Capture challan, inspection, seller biometric, transfer submission, transfer completion, number plate status, and final document pack.
- Keep legal/admin spend separate from restoration spend so the build economics remain readable.

### Strip-Down and Cataloguing

- Remove only as fast as the tagging and storage process can keep up.
- Treat roof, doors, hood, windows, trim, and interior components as separate sub-packages with outbound and return states.

### Body-Off Welding Track

- Do not buy the full stack of finishing materials until the rust map and repair method are confirmed.
- Run in three layers: structural repair, corrosion protection, then finish/sealing materials.
- Keep this track focused on shell/body steel; feed chassis-specific items into the dedicated chassis track below.

### Chassis Fixing Track

- This track is now open because the tub is off; keep it active until all structural unknowns are closed.
- Clean and inspect all rails, crossmembers, and mount points before deciding patch vs section replacement.
- Treat body-mount procurement control as part of chassis fixing: early pre-`1/79` six-station main tub set, separate front support pair, sleeves/cups, `M10 x 1.25` class `8.8` hardware, and flat shim pack.
- Body-mount rubbers and shims are fit-critical and stay `NEW_ONLY`; preserve old samples and original shim packs by station until the dry trial fit is closed.
- Do not sign off chassis coating on mount seats until the body-mount dry set proves pedestal height, thread condition, shim need, and front-support stack.
- Close all structural unknowns here before paint/protection closeout.

### Electrical

- Freeze the electrical scope before buying. Baseline circuits first, optional audio/accessories later.
- Prefer one documented architecture over a mix of old loom, partial kit wiring, and ad-hoc additions.

### Mechanical Baseline (Engine While Stripped)

- Use stripped access to do high-value baseline maintenance first (hoses, leaks, cooling, service points, mounts inspection).
- Keep a written fault list with measured findings; hold upgrades until baseline reliability is closed.

### Mechanical Replacement Pack (Full Restore)

- `MUST REPLACE (baseline service + reliability)`: engine oil and filter, air filter, fuel filter, spark plugs, distributor cap/rotor tune-up consumables (if distributor ignition remains), accessory belts, radiator upper/lower hoses, heater hoses, thermostat and gasket, radiator cap, vacuum hoses, fuel-rated rubber lines with clamps, and brake flexible hose set.
- `INSPECT THEN REPLACE`: engine mounts, clutch master/slave hydraulics, and any additional cooling-system wear items found during pressure testing.
- `Decision rule`: keep these baseline replacements independent from optional upgrades (power steering conversion, premium shocks, audio, etc.) so reliability and safety close first.

### Steering, Brakes, and Suspension

- Resolve the current steering play and brake baseline before deciding on power steering conversion style or shock upgrades.
- Treat full suspension conversion as off-plan unless the project objective changes materially.

### Interior and Weatherproofing

- This phase starts only after rust repair, primer strategy, sealing, and leak paths are under control.
- The sequence is protection first, finish second.

## Critical Decision Gates

- `Harness strategy gate`: baseline starting point is now the hot rod 21-circuit harness path; only reopen the loom decision if strip-down exposes a hard compatibility problem.
- `Body repair gate`: lock the corrosion-protection stack only after a rust map exists.
- `Power steering gate`: choose retain/rebuild/manual versus conversion only after steering wear and mechanical packaging are inspected.
- `Shock/suspension gate`: shocks and steering refresh are baseline candidates; full suspension conversion is deferred unless a new project brief explicitly approves it.
- `Audio/android gate`: do not commit until the base wiring is working and the dash/interior design is frozen.

## Legal/Admin Control Model

- Punjab Excise has a current biometric-verification page for motor vehicle owners and links a transfer process-flow PDF from that page:
  - `https://excise.punjab.gov.pk/index.php/node/650`
- Punjab Excise also has a current number-plate request page that says deployment with reference to biometric verification is under process:
  - `https://excise.punjab.gov.pk/npr-tmp`
- Because of that, the tracker should keep plate status separate from transfer status. A replica or interim plate arrangement is not the same thing as a closed ownership/admin file.
- Any item without explicit evidence stays open or `needs_confirmation` even if it was discussed in chat.

## Cost Capture Rules

- One row per economic event. Do not bury multiple purchases inside one note if they can be split cleanly.
- Quotes stay as `quote` rows until ordered or paid.
- Use `phase` and `workstream` to keep spend tied to the build sequence.
- Use `evidence_ref` for the WhatsApp message id, receipt filename, invoice number, or similar proof anchor.
- Use `payment_status` and `delivery_status` independently. Something can be paid but not delivered, or delivered but not yet installed.
- Log all shipping, tools, consumables, outsourced repair costs, deposits, refunds, returned-core credits, and replacement purchases.
- Keep `admin` bucket separate from `tools`, `parts`, and `labour`.
- Optional-upgrade rows stay visible but should not be mixed into the baseline completion logic.

## Immediate Next Actions

1. Confirm seller biometric status and whether ownership transfer has actually been submitted.
2. Build a single legal/admin evidence pack for the transfer and number-plate path.
3. Keep the strip-down tagging process active so removed and outsourced parts stay traceable.
4. Freeze weld-zone map boundaries and execute cut -> fit -> weld -> immediate corrosion stack on each closed zone.
5. Run chassis fixing in parallel: deep-clean frame, inspect rails/crossmembers/mounts, and close the open issue checks before coating signoff.
6. Capture body-mount pedestal/captive-thread condition and lock shim + rubber + hardware refit plan before tub return.
7. Run the electrical reset track in parallel: baseline harness termination, grounding, and fuse/relay validation only.
8. Run stripped-engine maintenance in parallel with chassis access and log post-service defects.
9. Keep procurement gated by phase: immediate rust-control buys now, defer interior and optional upgrade buys.
10. Record exact prices for already received tools and consumables that are still missing amounts.
11. Re-run the story and summary scripts after each meaningful ledger or evidence update so the archive stays current.
