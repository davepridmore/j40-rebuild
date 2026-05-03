# Active Tracks Status Board (2026-04-23)

## Scope

- This board is a daily control view based on:
  - `data/manual/workstream_status.csv`
  - `data/manual/reassembly_work_packages.csv`
  - `docs/j40_welding_execution_plan_20260419.md` (including 2026-04-22 body-off update)
- Current reality: body is off; body welding and chassis fixing are both active in parallel.
- 2026-05-03 update: suspension upgrade is now the ordered Ironman Foam Cell path, controlled by `docs/suspension-workstream.md`.

## Track Snapshot

| Track | Status | Priority | Depends On | Immediate Next Move | Gate To Close |
| --- | --- | --- | --- | --- | --- |
| `site_setup` | `in_progress` | `high` | `-` | Stabilize covered work area, labeling, and storage flow before more parts move. | Vehicle can stay stripped without weather/part-loss risk. |
| `legal_admin` | `in_progress` | `critical` | `seller_biometric` | Confirm biometric transfer submission, plate status, and complete document pack. | Ownership/admin trail is explicit and auditable. |
| `stripdown_cataloguing` | `in_progress` | `critical` | `site_setup` | Keep controlled strip-down with tags, photos, and outbound job tracking. | Shell/loose parts/outsourced items catalogued with no orphan parts. |
| `body_chassis` | `in_progress` | `critical` | `stripdown_cataloguing` | Execute weld-zone cut/fab/weld/coating sequence and freeze refit interface points. | Body-off shell repairs are welded, sealed, and signed off zone by zone. |
| `chassis_fixing` | `in_progress` | `high` | `body_chassis` | Run cleanup sequence with wire cup first on non-flat frame geometry, then flats cleanup and issue closure before coating. | No unresolved structural defects; protection stack documented. |
| `electrical_reset` | `in_progress` | `high` | `stripdown_cataloguing` | Freeze baseline circuit list and lock harness strategy before further optional buys. | Baseline electrical system is clean, documented, and functional. |
| `local_market_procurement` | `in_progress` | `high` | `electrical_reset`, `chassis_fixing`, `mechanical_baseline` | Run the short market list for compact fuse carrier, EPS kit, body hardware, grommets, and sample-matched small parts. | Local-only problem parts are bought, quoted, or rejected with photos, prices, and sample notes. |
| `mechanical_baseline` | `in_progress` | `high` | `stripdown_cataloguing`, `body_chassis` | Run stripped-state engine maintenance checklist while access is open. | Baseline maintenance complete with post-service defect log. |
| `steering_brakes_suspension` | `queued` | `high` | `mechanical_baseline` | Track Ironman shipments while closing brake and steering baseline inspections. | Safe steering/braking baseline plus Ironman install gates closed. |
| `suspension_upgrade` | `queued` | `high` | `chassis_fixing` | Receive both Ironman shipments, contents-check the kit, write the torque sheet, then install per `docs/suspension-workstream.md`. | Ironman kit installed, aligned, road-tested, and 50 km / 500 km rechecks logged. |
| `interior_weatherproofing` | `queued` | `medium` | `body_chassis` | Keep interior stack gated until floor/body sealing is closed. | Cabin is sealed/dry and ready for trim. |
| `final_assembly_validation` | `queued` | `critical` | `electrical_reset`, `mechanical_baseline`, `body_chassis`, `chassis_fixing` | Build punch-list and validation checklist before reassembly starts. | Reassembled vehicle passes function and road checks. |
| `optional_upgrades` | `backlog` | `medium` | `final_assembly_validation` | Keep android/audio and non-Ironman suspension experiments deferred. | Optional scope approved only after baseline sign-off and budget check. |

## Active Body-Off Issue Closure Set (Chassis Track)

- `issue_steering_box_mount_crack_check` -> pending work
- `issue_front_spring_hanger_crack_check` -> pending work
- `issue_crossmember_end_thinning_check` -> pending work
- `issue_body_mount_captive_thread_repair` -> pending work
- `issue_brake_fuel_line_clip_corrosion` -> pending work
- `issue_chassis_ground_points_refresh` -> pending work

All six should be closed with photo evidence before final chassis coating signoff.

## Execution Order (Now)

1. Keep `WP01` body rust closure and `WP03` electrical baseline running in parallel.
2. Start `chassis_fixing` mechanical cleanup now: wire cup first on non-flat parts, then strip-disc/flap-disc on flatter faces, and close issue list in the same body-welding window.
3. Run `local_market_procurement` as a separate market pass for fuse carrier, EPS quote, small hardware, grommets, and sample-matched parts.
4. Start `WP04` mechanical baseline procurement/inspection flow (condition-based bundle, no upgrade creep).
5. Track Ironman suspension delivery only; do not begin final install until the main kit, separate `24635FE x2` front damper pair, torque sheet, safe support setup, and chassis hanger checks are closed.
6. Hold interior finish stack (`WP05`) until body sealing gate closes.
7. Keep `WP06` reassembly blocked until body + electrical + mechanical + suspension gates are explicitly closed.
