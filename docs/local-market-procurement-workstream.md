# Local Market Procurement Workstream (Retired)

Date retired: 2026-05-13

This is no longer an active workstream. The old Local Market lane was removed because each item now has a primary owner in another workstream or in the site setup tracker.

## Ownership Map

| Former local-market item | Current owner | Control reference |
| --- | --- | --- |
| Compact cabin fuse add-on | `electrical_reset` | [cabin-fuse-box-acquisition-20260503.md](cabin-fuse-box-acquisition-20260503.md) |
| EPS donor kit quote | `eps_vitz_upgrade` | [eps-bilal-ganj-kit-checklist.md](eps-bilal-ganj-kit-checklist.md) |
| Captive/clip/rivnut hardware | `body_chassis` / `chassis_rubbers` | `data/manual/procurement_queue.csv` rows for Kit C and body-mount hardware |
| Retaining clips and cotters | `body_chassis` | `part_body_retaining_clips_cotter_pin_pack` |
| Firewall and wiring grommets | `electrical_reset` | `part_firewall_grommet_set_small_medium`, `part_firewall_grommet_set_large_power` |
| Body-mount leftovers, sleeves, shims, washers | `chassis_rubbers` / `chassis_fixing` | [chassis-rubbers-workstream.md](chassis-rubbers-workstream.md) |
| Sample-matched pins, spacers, brackets | `body_chassis` / `fabrication_handoff` | `part_body_specialty_brackets_retainer_plates` and fabrication handoff rows |
| Brake-opening consumables | `brake_system` | `part_brake_fluid_bleed_consumables` |
| Mechanical service parts | `mechanical_baseline` | service rows in `data/manual/procurement_queue.csv` |
| Hose and pipe pack | `replacement_pipes` / `mechanical_baseline` | [longman-pipe-hose-order-spec-20260512.md](longman-pipe-hose-order-spec-20260512.md) |
| Brake booster / servo reman quote | `brake_system` | brake booster scout rows and brake workstream |
| Hardwood cribbing cut set | `suspension_upgrade` | [suspension-wood-cribbing-merchant-spec.md](suspension-wood-cribbing-merchant-spec.md) |
| Toolbench / workbench | `site_setup` | `tool_local_toolbench` in expenses and procurement queue |

## Rule

Do not create new Local Market tasks. Local buying is still allowed, but the task must stay under the workstream that owns the part, fitment, or safety gate.
