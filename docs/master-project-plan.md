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
- Body and rust work is also live. Primer, prep solvent, seam sealer, cavity wax, and floor repair materials are on the active list; Raptor bedliner is tracked as on hand, and generic bed-lining/sound/foam/carpet buys stay gated until body closure.
- New photo evidence through `2026-04-20` shows wing removal/body-lift prep and underside access are mature enough to run body-off welding as an active track, with dedicated chassis and stripped-engine tracks in parallel.
- Steering feel remains a known problem. The suspension path is no longer hypothetical: the Ironman Foam Cell kit is ordered and must now be managed as an incoming safety-critical installation workstream with receipt, fitment, torque, alignment, and road-validation gates.

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
| `03b_chassis_fixing` | `in_progress` | Chassis track (active after tub separation): clean, inspect, repair/approve rails/crossmembers/mounts, then execute rust treatment, primer, seam/top protection, and cavity-wax closeout in order. | Chassis structural repairs are closed or explicitly approved and the coating/protection stack is documented with no unknowns remaining. |
| `04_electrical_reset` | `in_progress` | Remove junk wiring, define final architecture, buy only the core electrical materials, and install a documented harness. | Starting, charging, lights, horn, wipers, gauges, and required accessories work from a clean, documented loom. |
| `04c_local_market_procurement` | `in_progress` | Run one short in-person market lane for parts that need samples, photos, bench tests, or condition checks before purchase. | Local-only problem parts are bought, quoted, or explicitly rejected with evidence. |
| `05_mechanical_baseline` | `in_progress` | Engine-while-stripped track: run service/inspection tasks while access is open (leaks, cooling, hoses, fluids, tune consumables). | Engine baseline maintenance is complete and post-service defects are logged. |
| `06_steering_brakes_suspension` | `queued` | Resolve steering slack and brake baseline while receiving and installing the ordered Ironman Foam Cell suspension set under controlled gates. | Steering and braking are safe; Ironman suspension is contents-checked, installed, aligned, road-tested, and rechecked after settling. |
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
- Use `docs/window-parts-refurbishment-workflow-20260503.md` for the front vent/quarter window assemblies now tracked as `front_vent_window_assemblies` under `WP02`.

### Body-Off Welding Track

- Do not buy the full stack of finishing materials until the rust map and repair method are confirmed.
- Run in three layers: structural repair, corrosion protection, then finish/sealing materials.
- Keep this track focused on shell/body steel; feed chassis-specific items into the dedicated chassis track below.

### Chassis Fixing Track

- This track is now open because the tub is off; keep it active until all structural unknowns are closed.
- Clean and inspect all rails, crossmembers, and mount points before deciding patch vs section replacement.
- After inspection signoff, run the protection stack in order: rust treatment only where rust remains, full converter/residue removal and dry signoff, wax-and-grease wipe with flash-off, masking, zinc-rich 2K epoxy primer, seam sealer where required after primer, one exposed top protection by zone (chassis black/topcoat or Raptor), then HB Body U900 cavity-wax spray cans last in hidden sections.
- Do not assume black paint plus Raptor as a default stack. Use black/topcoat or Raptor by zone unless the product data confirms the exact cure, scuff, and recoat compatibility for putting Raptor over the black paint.
- Treat body-mount procurement control as part of chassis fixing: early pre-`1/79` six-station main tub set, separate front support pair, sleeves/cups, `M10 x 1.25` class `8.8` hardware, and flat shim pack.
- Body-mount rubbers and shims are fit-critical and stay `NEW_ONLY`; preserve old samples and original shim packs by station until the dry trial fit is closed.
- Do not sign off chassis coating on mount seats until the body-mount dry set proves pedestal height, thread condition, shim need, and front-support stack.
- Close all structural unknowns here before paint/protection closeout.

### Electrical

- Freeze the electrical scope before buying. Baseline circuits first, optional audio/accessories later.
- Prefer one documented architecture over a mix of old loom, partial kit wiring, and ad-hoc additions.

### Local Market Procurement

- Use `docs/local-market-procurement-workstream.md` for the short market run.
- This lane covers compact OEM fuse carrier, EPS kit quote, captive/clip hardware, grommets/rubber smalls, body-mount leftovers, sample-matched pins/brackets, brake-opening consumables, timber cribbing, and local mechanical service bundle.
- Every market item needs either buy evidence, quote evidence, or a reject note with photos/sample mismatch.

### Mechanical Baseline (Engine While Stripped)

- Use stripped access to do high-value baseline maintenance first (hoses, leaks, cooling, service points, in-place mount inspection).
- Current baseline keeps the engine installed. Do not buy an engine lift/hoist unless a later approved job actually requires engine support/removal.
- Keep a written fault list with measured findings; hold upgrades until baseline reliability is closed.

### Mechanical Replacement Pack (Full Restore)

- `MUST REPLACE (baseline service + reliability)`: engine oil and filter, air filter, fuel filter, diesel heat/glow plugs after exact engine-code/plug confirmation, accessory belts, radiator upper/lower hoses, heater hoses, thermostat and gasket, radiator cap, vacuum hoses, fuel-rated rubber lines with clamps, and brake flexible hose set.
- `INSPECT THEN REPLACE`: clutch master/slave hydraulics and any additional cooling-system wear items found during pressure testing.
- `INSPECTION NOTE ONLY`: engine mounts are removed from the active parts list because the engine stays installed. Photograph and check them after degreasing and under load; reopen a purchase only if they fail and another approved job already provides safe engine support.
- `Decision rule`: keep these baseline replacements independent from optional upgrades (power steering conversion, premium shocks, audio, etc.) so reliability and safety close first.

### Steering, Brakes, and Suspension

- Use `docs/suspension-workstream.md` as the start-here control sheet for the Ironman Foam Cell install.
- Use `docs/suspension-brake-merged-work-plan.md` as the combined workshop checklist when the Ironman suspension install and brake baseline refresh are run together.
- Use `docs/brake-suspension-order-links-20260503.md` for current brake-window order links; only hydraulic-opening consumables are ready now, while exact brake parts wait for `BR-CAPTURE-001`.
- Track the kit as two shipments: main Ironman set plus separate `24635FE x2` front damper pair.
- Do not buy alternate local/OME/Bilstein spring, shock, bush, shackle, or U-bolt options unless the Ironman receipt check proves a missing or incorrect item.
- Replace standard brake service parts as baseline work while preserving exact-part gates: front disc service parts by fitted conversion hardware, rear drum/cable parts by old samples and drum-open measurements, and hydraulic hoses/lines by fitting style, bracket retention, and old-sample/free length.
- Resolve brake hose slack, parking-brake cable route, rear hard-line routing, breather slack, steering damper clearance, shackle angle, ride height, alignment, brake bleed/adjustment, and post-install torque checks before road use.
- Current EPS route remains column-assist, not hydraulic, and does not require engine removal.

### Interior and Weatherproofing

- This phase starts only after rust repair, primer strategy, sealing, and leak paths are under control.
- The sequence is protection first, finish second.

## Critical Decision Gates

- `Harness strategy gate`: baseline starting point is now the hot rod 21-circuit harness path; only reopen the loom decision if strip-down exposes a hard compatibility problem.
- `Body repair gate`: lock the corrosion-protection stack only after a rust map exists.
- `Power steering gate`: choose retain/rebuild/manual versus conversion only after steering wear and mechanical packaging are inspected.
- `Suspension installation gate`: Ironman kit is the approved path. No install starts without both shipments, receipt check, supplier/OEM torque sheet, clean hanger inspection, safe support gear, and brake/steering clearance plan.
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
8. Run the local-market procurement lane as one short list for sample-matched and condition-gated buys.
9. Run stripped-engine maintenance in parallel with chassis access and log post-service defects.
10. Track Ironman suspension delivery and do only receipt/instruction prep until the complete kit and front damper pair are present; prepare the merged brake/suspension parts and tools checklist before the workshop window.
11. Keep procurement gated by phase: immediate rust-control buys now, defer interior and optional upgrade buys.
12. Record exact prices for already received tools and consumables that are still missing amounts.
13. Re-run the story and summary scripts after each meaningful ledger or evidence update so the archive stays current.
