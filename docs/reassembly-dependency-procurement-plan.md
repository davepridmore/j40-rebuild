# Reassembly, Dependency, and Procurement Plan

- Generated: 2026-05-18 09:34:36
- Work packages: `data/manual/reassembly_work_packages.csv`
- Dependency edges: `data/manual/reassembly_dependency_edges.csv`
- Component disposition: `data/manual/component_disposition_plan.csv`
- Procurement decisions: `data/manual/procurement_decision_matrix.csv`

## Current Evidence Snapshot

- `electrical_rework` photos: 18
- `electrical_reference` diagrams: 1
- Electrical diagram reconciliation rows: 17
- `rust_assessment` photos: 63
- `stripdown_cataloguing` photos: 111

## Bifurcated Dependency Lanes

- `body_structure`: 1 work package(s)
- `body_weather_seal`: 1 work package(s)
- `electrical`: 1 work package(s)
- `integration`: 1 work package(s)
- `interior`: 1 work package(s)
- `mechanical`: 1 work package(s)

## Procurement Decisions

- `buy_now`: 12
- `buy_remaining_brake_bleed_consumables`: 1
- `capture_body_hardware_samples_then_order`: 6
- `capture_spec_then_buy`: 13
- `confirm_price_then_buy`: 23
- `defer_duplicate_overlap`: 4
- `defer_optional`: 1
- `hold_until_body_closed`: 1
- `inspect_confirm_then_buy_standard`: 4
- `research_compare_then_select`: 1
- `review`: 2
- `track_ordered_delivery`: 5
- `verify_stock_before_buy`: 3

## Component Reuse/Refurbish Decisions

- `clean_store_for_reuse`: 1
- `refurbish_send_out`: 4
- `refurbish_service_subcomponents`: 2
- `remove_nonbaseline_and_refit_clean`: 1
- `review`: 58

## Immediate Execution Focus

- Close `WP01` + `WP03` in parallel: body rust closure and electrical baseline finalization are both active and should keep moving.
- Use `data/raw/imports/J40.jpg` as the WP03 viewable wiring diagram and keep `data/raw/imports/J40.graffle` as the editable source; export a fresh JPG after any diagram change.
- Work WP03 from `data/manual/electrical_diagram_reconciliation_20260518.csv`: close the firewall/pass-through, connector/pinout, heavy-cable stock, HVAC, EPS, fuel-stop, and rear-camera holds before final wrap.
- Hold final chassis primer/Raptor until the bracket work plan closes: analysis register, design release, radiator/battery/auxiliary/exhaust implementation, and validation photos.
- Run `WP04` procurement now: 36 mechanical rows still require buy execution.
- Run `GB-TOP-CAPTURE-001` before buying gearbox top-cover service parts; current top cover must be approved, repaired, or replaced as a matched assembly first.
- Close `DIFF-CAPTURE-001` during the rear brake/suspension window before axle coating, alignment, or road validation.
- Avoid duplicate buys: 3 rows are flagged as likely already on hand and should be physically stock-checked first.
- Keep interior finish gated: bedliner application/sound/foam/carpet stay blocked until body sealing gate is formally closed, with no extra bed-lining purchase in the baseline.
