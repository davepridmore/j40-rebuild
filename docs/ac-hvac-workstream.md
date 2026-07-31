# A/C HVAC Retrofit Workstream

- Created: 2026-05-30
- Workstream ID: `ac_hvac_retrofit`
- Parent phases: `07_interior_weatherproofing`, `05_mechanical_baseline`, `04_electrical_reset`
- Primary gates: `AC-CABIN-001`, `AC-FRONTPACK-001`, `AC-HOSE-001`, `AC-ELEC-001`, `AC-CHARGE-001`
- Related docs: [hvac-evaporator-blower-sourcing-20260514.md](hvac-evaporator-blower-sourcing-20260514.md), [hvac-dashboard-vent-duct-layout-20260602.md](hvac-dashboard-vent-duct-layout-20260602.md), [front-cooling-stack-fabrication-plan-20260530.md](front-cooling-stack-fabrication-plan-20260530.md), [front-cooling-stack-local-parts-selection-20260530.md](front-cooling-stack-local-parts-selection-20260530.md), [l4tw-front-cooling-stack-delivery-spec-20260531.md](l4tw-front-cooling-stack-delivery-spec-20260531.md), [amir-montgomery-road-shopping-list-20260527.md](amir-montgomery-road-shopping-list-20260527.md), [electrical-diagram-reconciliation-20260518.md](electrical-diagram-reconciliation-20260518.md)

## Decision

Treat the A/C as its own workstream because it crosses the hidden cabin evaporator package, front condenser/drier layout, compressor and bracket inspection, barrier-hose fabrication, condensate drain, controls, blower loads, and relay/fuse wiring.

The selected direction remains a hidden cabin-side evaporator/core/case with owner-selected external blowers where practical. A complete under-dash unit is acceptable only as a candidate if its case, drain, fittings, outlet face, and blower section can be adapted without creating a bulky visible hang-on unit.

## Order Capture - 2026-05-30

| Source | Evidence | Status | Use |
| --- | --- | --- | --- |
| AliExpress | `gmail_msg_19e78b8a26f000c1`, `bank_alert_19e78b8dbe36d812`, order `3073062248277489` | Ordered and paid, PKR 36,942 | Candidate universal 4-hole A/C evaporator / cool-heat 12V unit. Accept only after physical measurement, leak test, airflow test, and under-dash mock-up. |
| Alibaba Trade Assurance | `gmail_msg_19e76240ad0d5bc6`, order `302575831501027345` | Needs payment/active-order confirmation, USD 45 email total | Possible under-dash A/C evaporator assembly sample. Do not count as confirmed spend until payment/order state is proven. |

The Daraz order `243852333280938` from the same Gmail refresh is an NVME SSD enclosure and is not project spend.

## Owner Purchase Update - 2026-05-31

Owner reports a major A/C purchase intended to secure the cabin cooling package / slimline under-dash A/C direction. Exact product, seller, order number, and shipped contents are still pending confirmation.

Control position:

- Treat the purchased under-dash/slimline unit as the active cabin evaporator candidate once order proof or arrival photos are available.
- The owner authorises the Rev E centre-dash opening once its 1:1 template is placed clear of the glovebox/instruction panel and speedometer pressing. Do not release actual LCD/control/vent apertures, evaporator brackets, drain holes, firewall/bulkhead holes, or final hose crimps until the relevant hardware is physically measured and mocked in the J40.
- The front-pack hose layout must now be released as a complete loop: compressor, condenser, receiver-drier, pressure switch, cabin evaporator/TXV, suction return, service ports, and protected firewall pass-throughs.
- If the purchased unit includes a blower, controls, or heat function, accept those only after current draw, airflow, drain, outlet face, and under-dash clearance are proven.

## Owner Layout Update - 2026-06-02

Owner reports a condenser has been bought and should sit in the front compartment/front cooling stack. Treat it as the active condenser candidate only after dimensions, fitting side, port type, fan/radiator clearance, drier position, and hose exit direction are proven with photos or dry-fit.

Cabin distribution direction:

- Plan for four directional outlets: two circular satin-silver outlets integrated flush into the lower corners of the Rev E centre fascia and two longer duct runs to small directional outlets just behind the front-door pillar area.
- Use 2.5 inch vent hose and 2.5 inch hose-neck louvers as the default reference geometry unless the purchased evaporator/plenum proves another outlet size.
- Front dash outlets should be matched circular directional vents with satin/brushed-silver faces, hidden rear retainers, no exposed front screws, and an approximately 65-70 mm maximum visible diameter. Rear/pillar outlets remain separate pod or eyeball units aimed inward and rearward.
- The centre opening may be cut from the placed Rev E 1:1 template. Keep the vent cutouts and final duct runs on HOLD until the bought vent dimensions, evaporator outlet count, plenum shape, blower position and bend radius are mocked in the vehicle.
- Use [hvac-dashboard-vent-duct-layout-20260602.md](hvac-dashboard-vent-duct-layout-20260602.md) as the active vent/duct buy spec.

## Gates

### `AC-CABIN-001` - Cabin Evaporator Package

- Confirm case dimensions, coil face, core depth, intake face, outlet count/OD, refrigerant fittings, TXV/expansion valve, drain nipple, mounting tabs, and service access.
- Bench pressure/vacuum leak-test before installation.
- Bench airflow-test with the selected external blowers, not only the unit's included blower if present.
- Cardboard-mock under the J40 dash before cutting brackets, ducts, or drain holes.
- Confirm the purchased slimline/under-dash unit can route condensate outside the cabin and can connect to barrier hoses without sharp bends or service-blocking fittings.
- Confirm the evaporator/plenum can support the planned four-outlet distribution without starving demist airflow.

### `AC-FRONTPACK-001` - Condenser, Drier, Compressor

- Size condenser to the radiator/core-support opening with radiator, grille, fan, bonnet latch, and hose clearance proven.
- Confirm the owner-bought condenser's actual core size, total width over tabs, thickness, fitting side, port style, and fan clearance before treating it as released.
- Use [front_cooling_stack_rev_a](../data/manual/fabrication/front_cooling_stack_rev_a/README.md) as the active fabrication mock-up for the two-upright radiator/condenser/drier/fan frame.
- Use [front-cooling-stack-local-parts-selection-20260530.md](front-cooling-stack-local-parts-selection-20260530.md) as the Pakistan-local buy list. Local listings are quote anchors, not fitment releases, until tape photos and fitting proof are received.
- Use [l4tw-front-cooling-stack-delivery-spec-20260531.md](l4tw-front-cooling-stack-delivery-spec-20260531.md) as the acceptance spec for shop/fabricator delivery.
- Install a new receiver-drier only after condenser and hose layout are fixed.
- Inspect existing compressor/bracket/clutch/pulley alignment before buying a replacement; the current compressor is treated as Sanden-type reuse only after clutch voltage, pulley alignment, port style, oil/refrigerant, and leak checks pass.

### `AC-HOSE-001` - Hose And Bulkhead

- Do not crimp final barrier hoses until evaporator, condenser, drier, compressor, service ports, and firewall/bulkhead positions are locked.
- Use refrigerant-compatible barrier hose, fittings, HNBR O-rings, and protected pass-throughs only.
- Route the A/C lines as a complete circuit: compressor discharge to condenser, condenser outlet to drier, drier to TXV/evaporator inlet, evaporator outlet to compressor suction.

### `AC-ELEC-001` - Controls And Wiring

- Size fuses, relays, wire, connectors, and grounds from measured blower, compressor-clutch, and condenser-fan loads.
- Wire pressure-switch logic through the final relay/fuse plan before charging.

### `AC-CHARGE-001` - Final Validation

- Deep vacuum, leak hold, measured oil/refrigerant charge, blower-speed check, compressor-clutch cutout check, condenser-fan request, condensate drain water test, and cabin airflow/demist checks must all pass before closure.
