# Reassembly, Dependency, and Procurement Plan

- Generated: 2026-05-12 04:22:14
- Work packages: `data/manual/reassembly_work_packages.csv`
- Dependency edges: `data/manual/reassembly_dependency_edges.csv`
- Component disposition: `data/manual/component_disposition_plan.csv`
- Procurement decisions: `data/manual/procurement_decision_matrix.csv`

## Current Evidence Snapshot

- `electrical_rework` photos: 18
- `rust_assessment` photos: 51
- `stripdown_cataloguing` photos: 110

## Bifurcated Dependency Lanes

- `body_structure`: 1 work package(s)
- `body_weather_seal`: 1 work package(s)
- `electrical`: 1 work package(s)
- `integration`: 1 work package(s)
- `interior`: 1 work package(s)
- `mechanical`: 1 work package(s)

## Procurement Decisions

- `buy_now`: 4
- `buy_remaining_brake_bleed_consumables`: 1
- `capture_body_hardware_samples_then_order`: 6
- `capture_spec_then_buy`: 9
- `confirm_price_then_buy`: 8
- `defer_duplicate_overlap`: 4
- `defer_optional`: 1
- `hold_until_body_closed`: 1
- `inspect_confirm_then_buy_standard`: 3
- `next_phase_gate`: 1
- `research_compare_then_select`: 1
- `review`: 2
- `track_ordered_delivery`: 7
- `verify_stock_before_buy`: 2

## Component Reuse/Refurbish Decisions

- `clean_store_for_reuse`: 1
- `refurbish_send_out`: 4
- `refurbish_service_subcomponents`: 3
- `remove_nonbaseline_and_refit_clean`: 1
- `repair_in_place`: 1
- `review`: 44

## Immediate Execution Focus

- Close `WP01` + `WP03` in parallel: body rust closure and electrical baseline finalization are both active and should keep moving.
- Hold final chassis primer/Raptor until the bracket work plan closes: analysis register, design release, radiator/battery/auxiliary/exhaust implementation, and validation photos.
- Run `WP04` procurement now: 22 mechanical rows still require buy execution.
- Avoid duplicate buys: 2 rows are flagged as likely already on hand and should be physically stock-checked first.
- Keep interior finish gated: bedliner application/sound/foam/carpet stay blocked until body sealing gate is formally closed, with no extra bed-lining purchase in the baseline.
