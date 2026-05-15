# 1978 Toyota Land Cruiser J40 Rebuild Archive

This repository captures the rebuild of the 1978 Land Cruiser J40 as an evidence-backed archive and project-control workspace:

- WhatsApp chats and media
- manually dropped photos
- tools / parts / labour spend
- legal / admin status tracking
- workstream and phase tracking
- build decisions, milestones, and story outputs

The current setup is intentionally data-first. It gives you a clean place to keep evidence now, while preserving enough structure to produce a restoration story, spend summary, and project control layer as the rebuild moves forward.

## What This Project Tracks

- `tools`: workshop equipment and electrical tools
- `parts`: vehicle parts, consumables, trim, wiring, bodywork materials
- `labour`: painter, electrician, welder, denter, upholstery, mechanical work
- `admin`: registration and other non-restoration vehicle costs, kept separate from restoration totals
- `legal statuses`: ownership transfer, inspection, number-plate position, and document-pack completeness
- `workstreams`: the current phase/state of legal, strip-down, body, electrical, mechanical, interior, and validation work

Only chat content related to this build should be included. The importer treats the `Fj40` group as a build thread and filters the direct `Akbar Khan` export down to restoration-relevant messages only.

## Repository Layout

- `data/config/project.json`: import paths, relevance rules, and project metadata
- `data/config/whatsapp_target_numbers.json`: two-number target map for WhatsApp MCP reads
- `data/manual/expenses.csv`: manually maintained spend ledger with phase/workstream/evidence/payment/delivery fields
- `data/manual/procurement_queue.csv`: active purchasing queue filtered out of the main expense ledger
- `data/manual/j40_costs_workbook_rows.csv`: normalized extract of `/Users/davidpridmore/Documents/J40_Costs.xlsx` cost-like sheets
- `data/manual/j40_costs_expenses_reconciliation.csv`: workbook-to-ledger match status against `expenses.csv`
- `data/manual/j40_workbook_sheet_profiles.csv`: sheet-by-sheet structure profile across all workbook tabs
- `data/manual/j40_workbook_tidy_backlog.csv`: prioritized workbook tidy issues
- `data/manual/j40_costs_cost_tabs_tidy.csv`: normalized tidy extract of cost tabs (`Tools`, `Parts`, `Substances`, `Wiring`, `Service`)
- `data/manual/reassembly_work_packages.csv`: phased reassembly work packages with gate logic
- `data/manual/reassembly_dependency_edges.csv`: hard and parallel dependencies between reassembly work packages
- `data/manual/component_disposition_plan.csv`: component-level reuse vs refurbish vs repair recommendations
- `data/manual/procurement_decision_matrix.csv`: buy-now vs verify-stock vs defer decisions for open parts rows
- `data/manual/procurement_decision_matrix_pass2.csv`: tub-off-focused second-pass procurement decisions (minimize immediate spend)
- `data/manual/procurement_local_baskets_pass2.csv`: local bundle strategy (rust-minimum, electrical top-up, mechanical Toyota-common bundle)
- `data/manual/brake_system_requirements.csv`: rear brake cable, hard-line, hose, drum, and retaining-clip replacement matrix
- `data/manual/chassis_rubber_requirements.csv`: acquisition/fabrication status matrix for body-mount rubbers, sleeves, cups, shims, and mount hardware
- `data/manual/replacement_pipe_ordering_specs.csv`: curated location/photo/spec matrix for replacement pipes, hoses, hard lines, and the made-to-order coolant pipe sample
- `data/manual/replacement_pipe_photo_intake.csv`: shot-by-shot photo intake checklist for replacement pipe/hose names, placements, media IDs, and measurement targets
- `data/manual/fabrication_handoff_requirements.csv`: UI-facing package list for rubber and electrical fabrication PDF/DXF/SVG handoff
- `data/manual/fabrication/`: ready-to-send DXF/SVG/PDF fabrication packages for rubber recreation and electrical mounting parts
- `data/manual/workbook_tabs/`: per-tab CSV exports for quick review outside Excel
- `data/manual/j40-master-tracker.xlsx`: single Excel workbook generated from `expenses.csv` with `Initial Price`, `Purchase Registration`, `Purchase of Goods`, and `Purchase of Services` tabs
- `data/manual/legal_statuses.csv`: current legal/admin tracker
- `data/manual/workstream_status.csv`: current workstream and phase tracker
- `data/manual/component_jobs.csv`: removable components, outbound jobs, and reassembly-relevant part-flow tracker
- `data/manual/paint_refinish_whatsapp_media_queue.csv`: paint-refinish evidence queue extracted from WhatsApp attachments with send/return/progress buckets
- `data/manual/whatsapp_j40_chat_candidates.csv`: WhatsApp MCP-discovered J40 chat candidates (by profile, score, and fetch status)
- `data/manual/design_decisions.csv`: structured vehicle-design decisions and open design reviews
- `data/manual/photo_inventory.csv`: per-media inventory with component, stage, and confidence tags
- `data/manual/other_build_reference_media.csv`: curated other-build and workshop-sample image manifest for the dashboard
- `data/manual/photo_component_summary.csv`: grouped component summary from the photo inventory
- `data/inbox/photos/`: drop extra project photos here
- `data/raw/imports/`: extracted WhatsApp exports and media
- `data/processed/generated/`: generated message indexes, media indexes, and cost candidates
- `data/pakwheels/<listing_id>/`: listing-gallery snapshots, run history, and archived gallery images
- `data/reference/other_j40_builds/`: drop-zone for images from other J40 builds used as references
- `docs/master-project-plan.md`: the working master plan for the rebuild
- `docs/vehicle-design-spec.md`: the intended end-state of the vehicle itself
- `docs/restoration-story.md`: generated draft story / timeline
- `docs/photo-catalog.md`: generated photo categorization report and lookup guide
- `docs/j40-costs-workbook-reconciliation.md`: workbook registration and reconciliation summary
- `docs/j40-workbook-tabs-and-tidy-plan.md`: workbook-wide tab inventory and tidy plan
- `docs/j40-costs-tidy-extract.md`: normalized cost-tab tidy summary
- `docs/reassembly-dependency-procurement-plan.md`: integrated reassembly sequencing + dependency split + procurement actions
- `docs/procurement-pass2-tub-off.md`: second-pass procurement simplification for tub-off stage and local Pakistan sourcing assumptions
- `docs/suspension-workstream.md`: start-here tracker and installation control sheet for the incoming Ironman Foam Cell suspension set
- `docs/replacement-pipes-workstream.md`: start-here tracker for replacement pipes, hoses, hard lines, and made-to-order pipe samples
- `docs/fabrication-handoff-index.md`: send-out index for rubber and electrical fabrication packages
- `photos/index/`: generated lookup folders by component group, specific component, and stage
- `scripts/import_whatsapp.py`: parses chats, extracts media, filters relevance
- `scripts/import_whatsapp_mcp_j40.py`: discovers J40 chats from WhatsApp MCP profiles and exports normalized chat/message/media indexes
- `scripts/generate_story.py`: builds the current restoration story from the indexed evidence
- `scripts/build_master_workbook.py`: builds the single Excel workbook from `expenses.csv`
- `scripts/build_photo_inventory.py`: categorizes `photos/` media and rebuilds inventory + lookup folders
- `scripts/register_cost_workbook.py`: registers and reconciles `J40_Costs.xlsx` against `expenses.csv`
- `scripts/analyze_cost_workbook_tabs.py`: analyzes all workbook tabs, exports per-sheet CSVs, and builds tidy backlog
- `scripts/tidy_cost_workbook.py`: normalizes the five cost tabs into a clean operational extract
- `scripts/build_reassembly_dependency_plan.py`: builds reassembly work packages, dependency graph, component disposition plan, and procurement decision matrix
- `scripts/build_procurement_pass2_tub_off.py`: shrinks the active buy list for tub-off, defers non-baseline scope, and groups local bundle buys
- `scripts/sync_planning_into_cost_workbook.py`: writes all reconciled planning outputs back into `J40_Costs.xlsx` as managed tabs
- `scripts/reconcile_full_cost_workbook.py`: full in-place workbook reconciliation pass (header fixes, mixed-tab splits, tab cleanup, consolidated planning tabs)
- `scripts/build_engine_transmission_comparison.py`: models current-engine vs engine-swap completion costs (including transmission paths) and writes results into `J40_Costs.xlsx`
- `scripts/update_tub_off_refit_and_suspension_plan.py`: writes tub-off to tub-refit control plan, activates the ordered Ironman Foam Cell suspension path, and syncs related workbook tabs
- `scripts/move_wiring_fasteners_to_parts.py`: moves nut/bolt/washer-style rows from `Wiring` into `Parts` so parts tracking stays centralized
- `scripts/track_pakwheels_gallery.py`: snapshots a PakWheels listing gallery and tracks image additions/removals over time
- `scripts/build_project_control_ui.py`: builds `docs/project-control-ui/data.js` for the local project dashboard (workstreams, part ordering, project-step status, WhatsApp samples, and other-build references)
- `scripts/build_paint_refinish_whatsapp_media_queue.py`: extracts paint-refinish photos/videos from WhatsApp media index into send/return/in-progress queues
- `scripts/auth_whatsapp_mcp.sh`: QR-auth helper for WhatsApp MCP profiles (`1` and `2`)
- `tools/generate_rubber_recreation_fabrication_pack.py`: generates the rubber recreation DXF/SVG/PDF fabrication package
- `tools/generate_electrical_module_drawings.py`, `tools/generate_midi5_plate_mount_rev_c.py`, `tools/generate_midi5_enclosure_rev_d.py`, `tools/generate_relay_mount_rev_c.py`: generate the electrical mounting DXF/SVG/PDF fabrication packages; Rev D is the current MIDI enclosure route

## How To Use

1. Drop extra loose photos into `data/inbox/photos/`.
2. Drop reference photos from other J40 builds into `data/reference/other_j40_builds/`.
3. Add curated WhatsApp or workshop sample images to `data/manual/other_build_reference_media.csv`.
4. Update `data/manual/expenses.csv` whenever you buy, quote, receive, install, refund, or defer anything that changes project cost.
5. Set `procurement_stage` in `data/manual/expenses.csv` so each line item stays operationally visible:
   - `purchase_ready`: ready to order now
   - `ordered_pending_delivery`: order has been placed and is waiting to arrive
   - `needs_confirmation`: user says it may already be ordered or delivered, but proof still needs to be reconciled
   - `received_candidate`: likely purchased / delivered, but still needs item-level confirmation
   - `next_phase_purchase`: valid item, but not yet on the critical path
   - `researching`: still being compared or scoped
   - `deferred_until_body_closed`: do not buy until body/floor work reaches the right point
   - `deferred_optional`: non-baseline upgrades or nice-to-haves
   - `received` / `completed`: no longer belongs in the active queue
6. Use `data/manual/procurement_queue.csv` as the working buy list and reconciliation list.
7. Update `data/manual/legal_statuses.csv` whenever a legal/admin step changes state.
8. Update `data/manual/workstream_status.csv` whenever a phase actually moves or gets blocked.
9. Update `data/manual/component_jobs.csv` whenever a removable component is tagged, sent out, returned, stored, or reinstalled.
10. Rebuild the local photo catalog and lookup folders whenever you add files into `photos/`:

```bash
python3 scripts/build_photo_inventory.py
```

To pull selected recent media from Google Photos via Picker API into `photos/`:

```bash
python3 scripts/import_google_photos_picker.py \
  --client-secrets /Users/davidpridmore/.codex/client_secret.json \
  --recent-days 120 \
  --open-browser
```

Personal-account on-demand command (personal OAuth client, import + filter + analysis refresh):

```bash
./scripts/run_personal_photos_picker_on_demand.sh
```

Optional environment overrides:

```bash
CLIENT_SECRETS=/absolute/path/to/oauth_client.json \
RECENT_DAYS=30 \
MOVE_NON_CAR=1 \
./scripts/run_personal_photos_picker_on_demand.sh
```

After import, run:

```bash
python3 scripts/build_photo_inventory.py
python3 scripts/reconcile_component_jobs_photo_inventory.py
python3 scripts/build_paint_refinish_media_queue.py
python3 scripts/build_paint_refinish_whatsapp_media_queue.py
```

`build_paint_refinish_media_queue.py` writes `data/manual/paint_refinish_media_queue.csv` with three evidence buckets:
`prepared_for_send_out`, `returned_from_painter`, and `in_progress_video`.

`build_paint_refinish_whatsapp_media_queue.py` writes `data/manual/paint_refinish_whatsapp_media_queue.csv`
from `data/processed/generated/media_index.csv` and `whatsapp_messages.json` with the same three buckets plus
`classification_confidence` and `classification_reason` for review.

To avoid custom client-secrets entirely, you can use `gcloud` ADC credentials:

```bash
gcloud auth application-default login \
  --scopes=https://www.googleapis.com/auth/photospicker.mediaitems.readonly

python3 scripts/import_google_photos_picker.py \
  --auth-mode adc \
  --recent-days 120
```

Automated ingest mode (recommended in this repo):

- Drop Google Takeout archives into: `data/inbox/takeout/`
- Supported archive formats: `.zip`, `.tgz`, `.tar.gz`
- Cron scanner script: `scripts/scan_takeout_ingest_once.sh`
- Install cron automation: `scripts/install_photo_ingest_cron.sh`
- Remove cron automation: `scripts/uninstall_photo_ingest_cron.sh`
- Current automation status file: `docs/photo_ingest_automation_status.md`

Helper to stage archives from Downloads:

```bash
./scripts/stage_takeout_from_downloads.sh
```

On-demand full ingest + car-related filtering + analysis refresh:

```bash
./scripts/run_photo_ingest_on_demand.sh
```

This command stages archives, ingests media, moves probable non-car files to `photos/non_car_review/`, and refreshes inventory/catalog/reconciliation outputs.

`rclone` note:

- Google Photos Library API policy now limits API reads to media created by the same app/client.
- This means `rclone` is no longer reliable for full phone-library sync in this project.
- Use the Picker on-demand flow above for recent selected media, or Google Takeout ingest for full-library snapshots.

If you still want to run `rclone` (for app-created media only), use:

```bash
./scripts/sync_google_photos_pipeline.sh pridmoredave-gphotos:
```

This command:

- copies recent media from `media/all` into `photos/` (`MAX_AGE` default `540d`)
- rebuilds `data/manual/photo_inventory.csv`
- refreshes `docs/photo-catalog.md`
- refreshes `data/manual/component_jobs_photo_reconciliation.csv` and its report

You can tune the pull window, for example:

```bash
MAX_AGE=180d ./scripts/sync_google_photos_pipeline.sh pridmoredave-gphotos:
```

9. Register and reconcile the external workbook whenever it changes:

```bash
python3 scripts/register_cost_workbook.py --workbook /Users/davidpridmore/Documents/J40_Costs.xlsx
```

10. Run workbook-wide tab analysis and tidy extraction:

```bash
python3 scripts/analyze_cost_workbook_tabs.py --workbook /Users/davidpridmore/Documents/J40_Costs.xlsx
python3 scripts/tidy_cost_workbook.py --workbook /Users/davidpridmore/Documents/J40_Costs.xlsx
```

11. Build reassembly and procurement execution planning artifacts:

```bash
python3 scripts/build_reassembly_dependency_plan.py
```

12. Run the tub-off second-pass procurement simplification:

```bash
python3 scripts/build_procurement_pass2_tub_off.py
```

13. Sync all planning/reconciliation outputs into the main workbook (keeps original tabs and adds managed planning tabs):

```bash
python3 scripts/sync_planning_into_cost_workbook.py --workbook /Users/davidpridmore/Documents/J40_Costs.xlsx
```

The sync command creates a timestamped backup copy before writing:

- `/Users/davidpridmore/Documents/J40_Costs.backup_YYYYMMDD_HHMMSS.xlsx`

14. Run a full workbook reconciliation and simplification pass when tabs drift or mixed content appears:

```bash
python3 scripts/reconcile_full_cost_workbook.py --workbook /Users/davidpridmore/Documents/J40_Costs.xlsx
```

15. Build the engine/transmission scenario comparison and write it into the workbook:

```bash
python3 scripts/build_engine_transmission_comparison.py --workbook /Users/davidpridmore/Documents/J40_Costs.xlsx
```

16. Sync tub-off/refit execution control, mount/rubber procurement, and ordered Ironman Foam Cell suspension decisions:

```bash
python3 scripts/update_tub_off_refit_and_suspension_plan.py --workbook /Users/davidpridmore/Documents/J40_Costs.xlsx
```

17. Move fastener rows from `Wiring` into `Parts`:

```bash
python3 scripts/move_wiring_fasteners_to_parts.py --workbook /Users/davidpridmore/Documents/J40_Costs.xlsx
```

This command creates a backup before edits:

- `/Users/davidpridmore/Documents/J40_Costs.full_reconcile_backup_YYYYMMDD_HHMMSS.xlsx`

18. Rebuild dashboard data for the local project-control UI:

```bash
python3 scripts/build_project_control_ui.py
```

Then start the local dashboard server:

```bash
./start-dashboard.command
```

15. Run:

```bash
python3 scripts/import_whatsapp.py
python3 scripts/import_whatsapp_mcp_j40.py
python3 scripts/build_paint_refinish_whatsapp_media_queue.py
python3 scripts/generate_story.py
python3 scripts/build_master_workbook.py
```

The first command extracts and indexes chats, media, and cost candidates.
The second command discovers J40-related chats from your two WhatsApp MCP profiles and exports normalized chat/message/media tables.
The third command builds the WhatsApp-derived paint evidence queue.
The fourth command produces the draft story and spend snapshot.
The fifth command produces the single Excel workbook for review and sharing, focused on initial pricing and purchase registration control.

The workbook tabs are centered on purchase control:

- `Initial Price`: quoted/initial prices captured so far
- `Purchase Registration`: registration state for each row (`registered`, `registered_needs_confirmation`, `quote_only`, `planned`, `researching`)
- `Purchase of Goods`: goods-only rows (`tools` + `parts`)
- `Purchase of Services`: services-only rows (`labour` + `admin`)

To keep a PakWheels listing gallery tracked over time, run:

```bash
python3 scripts/track_pakwheels_gallery.py --url "https://www.pakwheels.com/used-cars/toyota-land-cruiser-1984-for-sale-in-islamabad-10076971"
```

Each run appends a timestamped snapshot and updates:

- `data/pakwheels/<listing_id>/gallery_runs.csv`
- `data/pakwheels/<listing_id>/gallery_history.csv`
- `data/pakwheels/<listing_id>/archive/` (deduplicated image files)
- `data/pakwheels/<listing_id>/snapshots/<run>/` (per-run URLs + manifest)

## Cost Control Notes

- `phase` and `workstream` tie spend to the plan in `docs/master-project-plan.md`.
- `evidence_ref` should point to a WhatsApp message id, invoice, receipt filename, or similar proof anchor.
- `payment_status` and `delivery_status` should be maintained independently.
- `procurement_stage` is the operational layer on top of financial status; use it to separate "ready to buy now" from "quoted", "received but not fully reconciled", and "deferred".
- Keep `admin` costs separate from restoration costs.
- Quotes and optional upgrades should stay visible, but they should not be confused with confirmed baseline spend.
- `data/manual/procurement_queue.csv` should only contain live items that still need purchase, confirmation, or decision work.

## Seeded Data

The repo already includes:

- the two WhatsApp exports you pointed to in `/Users/davidpridmore/Downloads`
- your current purchase list, separated into received / planned / research items
- known spend items and quote items visible in the chats

Amounts without a confirmed number stay in the ledger with `amount_status=missing` so they are visible but do not distort totals.

## Gmail / Order Status

Project-local MCP is configured in `.ai/mcp/mcp.json` with server `google-orders-receipts` (Gmail + Drive only).

One-time setup:

```bash
bash scripts/auth_orders_receipts_mcp.sh
```

If your OAuth credentials are in a different file, set:

```bash
GOOGLE_WORKSPACE_CREDENTIALS_PATH=/absolute/path/to/credentials.json bash scripts/auth_orders_receipts_mcp.sh
```

Build a full order/receipt verification queue for all `parts` and `tools` rows:

```bash
python3 scripts/build_orders_receipts_audit_queue.py
```

This writes `data/manual/orders_receipts_audit_queue.csv` with:

- audit priority (`high|medium|low`)
- recommended audit status per row
- Gmail/Drive search queries for order confirmation and receipt/invoice proof

## WhatsApp MCP (2 Numbers)

Project-local MCP is configured in `.ai/mcp/mcp.json` with:

- `whatsapp-number-1`
- `whatsapp-number-2`

Each server uses a separate auth/session directory and media storage path:

- `.ai/mcp/auth/whatsapp-number-1` -> `data/raw/imports/mcp_whatsapp_number_1`
- `.ai/mcp/auth/whatsapp-number-2` -> `data/raw/imports/mcp_whatsapp_number_2`

One-time QR auth for each number profile:

```bash
bash scripts/auth_whatsapp_mcp.sh 1
bash scripts/auth_whatsapp_mcp.sh 2
```

After each login is confirmed, stop the auth process with `Ctrl+C`.

Set your two target numbers in:

- `data/config/whatsapp_target_numbers.json`

Use E.164 format (example: `+923001234567`), one number for each server profile.

Import J40-focused chat metadata and media indexes from the two WhatsApp MCP profiles:

```bash
python3 scripts/import_whatsapp_mcp_j40.py
```

This writes:

- `data/manual/whatsapp_j40_chat_candidates.csv`
- `data/processed/generated/mcp_whatsapp_j40_messages.json`
- `data/processed/generated/mcp_whatsapp_j40_media_index.csv`
