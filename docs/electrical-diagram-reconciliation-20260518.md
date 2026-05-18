# Electrical Diagram Reconciliation - 2026-05-18

Sources reconciled:

- `data/raw/imports/J40.jpg`
- `data/raw/imports/J40.graffle`
- `data/manual/electrical_diagram_reconciliation_20260518.csv`
- `data/manual/workbook_tabs/electrical_master.csv`
- `data/manual/engine_electrical_inputs_reconciliation_20260517.csv`
- `data/manual/cabin_engine_firewall_holes_survey_20260517.csv`
- `data/manual/fabrication_handoff_requirements.csv`
- `data/manual/procurement_queue.csv`
- `data/manual/expenses.csv`

The Graffle file was parsed directly and yielded 140 diagram labels. The reconciliation keeps the diagram as the functional topology reference, while the electrical master remains the controlling as-built record for relay positions, connector IDs, loom IDs, minimum gates, and final test closure.

## Confirmed Alignment

- The diagram agrees with the power-corner plan: battery to 100A breaker to MIDI fuse holders and relay bank.
- Relay-bank labels align with the active relay quick lookup: low beam, high beam, horn, condenser fan, spot lamps, A/C clutch, auxiliary, and spare capacity.
- Front and rear loom labels align with the front trunk, rear loom, ignition, left branch, right branch, and VC loom sections.
- Engine-side labels align with the May 17 starter, alternator, sender, and fuel-stop reconciliation, but those circuits still require terminal proof.
- Fabrication handoff packages for the battery power carrier, Relay Rev D, MIDI Rev D, and cutoff/kill-switch guard are consistent with the diagram topology.

## Open Holds

- The diagram does not assign firewall hole IDs, grommet sizes, or reuse/closure decisions; the firewall survey remains controlling for pass-throughs.
- The diagram does not replace X1-X10 connector and pin continuity records.
- Heavy cable sizes shown in the diagram must be reconciled against physical stock and installed route lengths before buying more cable.
- Rear-view camera, stereo, EPS, HVAC, and other convenience/upgrade circuits stay gated behind their specific workstream and procurement decisions.
- Fuel-stop and diesel shutdown behavior must be proven live with the manual cutoff retained as backup.

## Dashboard Impact

The dashboard now exposes the reconciliation table inside the Electrical Specs and Layout section, and the workstream evidence still uses `J40.jpg` as the visible wiring diagram image.
