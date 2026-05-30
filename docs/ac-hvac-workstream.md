# A/C HVAC Retrofit Workstream

- Created: 2026-05-30
- Workstream ID: `ac_hvac_retrofit`
- Parent phases: `07_interior_weatherproofing`, `05_mechanical_baseline`, `04_electrical_reset`
- Primary gates: `AC-CABIN-001`, `AC-FRONTPACK-001`, `AC-HOSE-001`, `AC-ELEC-001`, `AC-CHARGE-001`
- Related docs: [hvac-evaporator-blower-sourcing-20260514.md](hvac-evaporator-blower-sourcing-20260514.md), [amir-montgomery-road-shopping-list-20260527.md](amir-montgomery-road-shopping-list-20260527.md), [electrical-diagram-reconciliation-20260518.md](electrical-diagram-reconciliation-20260518.md)

## Decision

Treat the A/C as its own workstream because it crosses the hidden cabin evaporator package, front condenser/drier layout, compressor and bracket inspection, barrier-hose fabrication, condensate drain, controls, blower loads, and relay/fuse wiring.

The selected direction remains a hidden cabin-side evaporator/core/case with owner-selected external blowers where practical. A complete under-dash unit is acceptable only as a candidate if its case, drain, fittings, outlet face, and blower section can be adapted without creating a bulky visible hang-on unit.

## Order Capture - 2026-05-30

| Source | Evidence | Status | Use |
| --- | --- | --- | --- |
| AliExpress | `gmail_msg_19e78b8a26f000c1`, `bank_alert_19e78b8dbe36d812`, order `3073062248277489` | Ordered and paid, PKR 36,942 | Candidate universal 4-hole A/C evaporator / cool-heat 12V unit. Accept only after physical measurement, leak test, airflow test, and under-dash mock-up. |
| Alibaba Trade Assurance | `gmail_msg_19e76240ad0d5bc6`, order `302575831501027345` | Needs payment/active-order confirmation, USD 45 email total | Possible under-dash A/C evaporator assembly sample. Do not count as confirmed spend until payment/order state is proven. |

The Daraz order `243852333280938` from the same Gmail refresh is an NVME SSD enclosure and is not project spend.

## Gates

### `AC-CABIN-001` - Cabin Evaporator Package

- Confirm case dimensions, coil face, core depth, intake face, outlet count/OD, refrigerant fittings, TXV/expansion valve, drain nipple, mounting tabs, and service access.
- Bench pressure/vacuum leak-test before installation.
- Bench airflow-test with the selected external blowers, not only the unit's included blower if present.
- Cardboard-mock under the J40 dash before cutting brackets, ducts, or drain holes.

### `AC-FRONTPACK-001` - Condenser, Drier, Compressor

- Size condenser to the radiator/core-support opening with radiator, grille, fan, bonnet latch, and hose clearance proven.
- Install a new receiver-drier only after condenser and hose layout are fixed.
- Inspect existing compressor/bracket/clutch/pulley alignment before buying a replacement.

### `AC-HOSE-001` - Hose And Bulkhead

- Do not crimp final barrier hoses until evaporator, condenser, drier, compressor, service ports, and firewall/bulkhead positions are locked.
- Use refrigerant-compatible barrier hose, fittings, HNBR O-rings, and protected pass-throughs only.

### `AC-ELEC-001` - Controls And Wiring

- Size fuses, relays, wire, connectors, and grounds from measured blower, compressor-clutch, and condenser-fan loads.
- Wire pressure-switch logic through the final relay/fuse plan before charging.

### `AC-CHARGE-001` - Final Validation

- Deep vacuum, leak hold, measured oil/refrigerant charge, blower-speed check, compressor-clutch cutout check, condenser-fan request, condensate drain water test, and cabin airflow/demist checks must all pass before closure.
