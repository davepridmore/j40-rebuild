# J40 Costs Workbook Tidy Extract

- Generated: 2026-04-15 02:39:12
- Workbook: `/Users/davidpridmore/Documents/J40_Costs.xlsx`
- Output: `data/manual/j40_costs_cost_tabs_tidy.csv`
- Total extracted rows: 192

## Rows By Sheet

- `Parts`: 25
- `Service`: 2
- `Substances`: 22
- `Tools`: 41
- `Wiring`: 102

## Row Disposition

- `line_item`: 121
- `schema_mismatch`: 9
- `section_header`: 62

## Normalized Received Status (line-item only)

- `blank`: 29
- `other`: 1
- `yes`: 91

## Normalized Paid Status (line-item only)

- `blank`: 32
- `cancelled`: 2
- `cod`: 2
- `no`: 3
- `yes`: 82

## Schema-Mismatch Rows (likely wrong tab)

- `Wiring#144` Front Leaf Springs (suggested target: Suspension)
- `Wiring#145` Rear Leaf Springs (suggested target: Suspension)
- `Wiring#146` Front Shocks (suggested target: Suspension)
- `Wiring#147` Rear Shocks (suggested target: Suspension)
- `Wiring#148` Greasable Shackle (Front) (suggested target: Suspension)
- `Wiring#149` Greasable Shackle (Rear) (suggested target: Suspension)
- `Wiring#150` Bushing Kit (suggested target: Suspension)
- `Wiring#151` U-Bolt Kit (suggested target: review)
- `Wiring#152` Rear Anti-Inversion Kit (suggested target: Suspension)
