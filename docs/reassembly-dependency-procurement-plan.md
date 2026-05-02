# Reassembly, Dependency, and Procurement Plan

- Generated: 2026-05-02 06:33:21
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

- `confirm_price_then_buy`: 9
- `defer_duplicate_overlap`: 7
- `defer_optional`: 1
- `inspect_then_buy`: 2
- `next_phase_gate`: 3
- `research_compare_then_select`: 1
- `review`: 14
- `track_ordered_delivery`: 4
- `verify_stock_before_buy`: 3

## Component Reuse/Refurbish Decisions

- `clean_store_for_reuse`: 1
- `refurbish_send_out`: 4
- `refurbish_service_subcomponents`: 2
- `remove_nonbaseline_and_refit_clean`: 1
- `repair_in_place`: 1
- `review`: 31

## Immediate Execution Focus

- Close `WP01` + `WP03` in parallel: body rust closure and electrical baseline finalization are both active and should keep moving.
- Run `WP04` procurement now: 5 mechanical rows still require buy execution.
- Avoid duplicate buys: 3 rows are flagged as likely already on hand and should be physically stock-checked first.
- Keep interior stack gated: bed lining/sound/foam/carpet stay blocked until body sealing gate is formally closed.
