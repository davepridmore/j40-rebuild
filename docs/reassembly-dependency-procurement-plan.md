# Reassembly, Dependency, and Procurement Plan

- Generated: 2026-04-22 03:50:30
- Work packages: `data/manual/reassembly_work_packages.csv`
- Dependency edges: `data/manual/reassembly_dependency_edges.csv`
- Component disposition: `data/manual/component_disposition_plan.csv`
- Procurement decisions: `data/manual/procurement_decision_matrix.csv`

## Current Evidence Snapshot

- `electrical_rework` photos: 129
- `rust_assessment` photos: 33
- `stripdown_cataloguing` photos: 106

## Bifurcated Dependency Lanes

- `body_structure`: 1 work package(s)
- `body_weather_seal`: 1 work package(s)
- `electrical`: 1 work package(s)
- `integration`: 1 work package(s)
- `interior`: 1 work package(s)
- `mechanical`: 1 work package(s)

## Procurement Decisions

- `buy_now_from_quote`: 1
- `confirm_order_state`: 1
- `confirm_price_then_buy`: 25
- `defer_duplicate_overlap`: 14
- `defer_optional`: 1
- `inspect_then_buy`: 2
- `next_phase_gate`: 4
- `research_compare_then_select`: 1
- `verify_stock_before_buy`: 4

## Component Reuse/Refurbish Decisions

- `clean_store_for_reuse`: 1
- `refurbish_send_out`: 5
- `refurbish_service_subcomponents`: 2
- `remove_nonbaseline_and_refit_clean`: 1
- `repair_in_place`: 1
- `review`: 11

## Immediate Execution Focus

- Close `WP01` + `WP03` in parallel: body rust closure and electrical baseline finalization are both active and should keep moving.
- Run `WP04` procurement now: 18 mechanical rows still require buy execution.
- Avoid duplicate buys: 4 rows are flagged as likely already on hand and should be physically stock-checked first.
- Keep interior stack gated: bed lining/sound/foam/carpet stay blocked until body sealing gate is formally closed.
