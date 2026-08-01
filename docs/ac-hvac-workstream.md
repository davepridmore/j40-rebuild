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
- At that time the owner authorised replacing the complete visible dash face to the Rev H architecture. That four-outlet architecture is now historical and superseded by Rev I below; its requirement to transfer the structural cowl/A-pillar/column boundaries and retained OEM glovebox and speedometer assemblies with a disposable full-size template remains active. Do not release production metal, LCD/control/vent apertures, evaporator brackets, drain holes, firewall/bulkhead holes, or final hose crimps until the relevant hardware is physically measured and mocked in the J40.
- The front-pack hose layout must now be released as a complete loop: compressor, condenser, receiver-drier, pressure switch, cabin evaporator/TXV, suction return, service ports, and protected firewall pass-throughs.
- If the purchased unit includes a blower, controls, or heat function, accept those only after current draw, airflow, drain, outlet face, and under-dash clearance are proven.

## Superseded Owner Layout Record - 2026-08-01 Rev H

Owner reports a condenser has been bought and should sit in the front compartment/front cooling stack. Treat it as the active condenser candidate only after dimensions, fitting side, port type, fan/radiator clearance, drier position, and hose exit direction are proven with photos or dry-fit.

Historical cabin distribution record; do not buy or fabricate from these four-outlet coordinates:

- Plan for four identical circular satin-silver outlets integrated into the Rev H dashboard. Keep the two end outlets high and close to the usable flat-face ends, with nominal centres at `Y=168.5 mm` and their `Ø87 mm` bezel tops aligned to the LCD-bezel top at `Y=212.0 mm`. V1 must be wholly on fixed fascia outboard of the direct-traced glovebox: retain at least `10 mm` real fixed-metal land from its bezel to the lid boundary, and keep its aperture, retainer, duct and service land outside the lid perimeter, hinges/latch, opening and complete sweep. Route its supported duct above/outboard of that sweep. Lower the inner pair to centres at `Y=20.0 mm`, symmetric at `X=464/796 mm` about the shared LCD/fascia centreline `X=630 mm`; their faces span `Y=-23.5…63.5 mm`, leaving a nominal `12.5 mm` vertical gap below the LCD bezel. Place each inner outlet in its own rounded body-colour pod down to `Y=-35.0 mm`. Do not put the end pair in the side returns or A-pillars.
- Use the common `Ø87 mm` visible face / `Ø75 mm` opening family only as a low-cost geometry reference. Buy four matching samples from one batch in Pakistan and measure the face, cutout, retainer, spigot and depth before releasing holes. Prefer 2.5 inch duct only if the measured vent and evaporator outlets support it.
- Keep the normal fascia lower edge at `Y=50.0 mm`; only the two local inner-vent pods descend 85 mm to `Y=-35.0 mm`, plus the steering-column relief and compact extreme-right control return. Mock all four supported duct branches and prove the two deeper vent necks/elbows and their pods clear the retained glovebox, original cluster, steering column and shroud through full sweep, LCD connectors, selector contact stacks, driver knees, all gear/transfer/winch lever positions and service paths. Before release, measure and photograph at least `8 mm` visible inner-rim-to-LCD clearance, `10 mm` from each inner vent retainer/duct to fixed LCD/cluster/support hardware, and `20 mm` to the signed steering-column/shroud/stalk swept envelope; reject any duct section ovalised below `90%` of its round inside diameter.
- Consolidate exactly seven Schneider selectors plus a separate red hazard in a compact two-row bank at the extreme right. Use four nominal columns at `X=1096/1144/1192/1240 mm`, top row `Y=88 mm` and bottom row `Y=30 mm` (48 mm horizontal and 58 mm vertical pitch). Top row is `WIPERS | LIGHTS | SPOTS | AUX`; bottom row is `BLOWER | A/C | ENGINE | HAZARD`. `WIPERS`, `LIGHTS`, `BLOWER` are 3-position; `SPOTS`, `AUX`, `A/C`, `ENGINE` are 2-position. `ENGINE` uses the former spare position as a low-current RUN/STOP request subject to EEI-003, authoritative key-OFF shutdown and the retained manual stop cable. Keep cabin thermostat/temperature/blend with the delivered evaporator controller, outside this seven-selector count.
- Treat the retained glovebox and speedometer as visual no-touch regions as well as functional transfers: preserve their existing position, outline, finish, colour, patina, markings, knob/plate, gauge faces, glass and needles. Do not move, refinish, recolour, restyle or reinterpret either assembly; the replacement fascia must meet their direct-transferred edges.
- Cut only the disposable Rev H fit template before M1-M10 sign-off. Keep the production face, vent cutouts and final duct runs on HOLD until the bought parts, evaporator outlet count, plenum shape, blower position and bend radius are mocked in the vehicle.
- The Rev H four-outlet vent record is retained in [hvac-dashboard-vent-duct-layout-20260602.md](hvac-dashboard-vent-duct-layout-20260602.md); its four-vent purchasing and fabrication instructions are superseded by the Rev I direction below.

## Owner Two-Outlet Revision - 2026-08-01 Rev I Direction

The owner now prefers a smaller cabin package and a factory-height fascia with exactly two occupant outlets. This supersedes only the Rev H four-outlet distribution; retain the central LCD, original glovebox/speedometer transfer, factory column relief and control-bank decisions in Rev I.

- Retain two matched, generously sized directional outlets high at the fixed outer/end regions, one aimable at the passenger and one at the driver. Delete the Rev H inner/lower pair and its pods. Use two supported end branches and prove useful balanced flow, bend radius and service clearance in the full-depth mock-up.
- Seek a genuinely compact 12V cooling evaporator with two real duct takeoffs, or a compact core/case with a sealed two-takeoff plenum. Do not interpret two decorative front louvers as proof of two duct connections.
- The ordered AliExpress four-hole unit is no longer the primary final-install candidate because its outlet count and reported package size conflict with this direction. Measure and test it on arrival before deciding whether it can be returned, resold, or retained as donor/spare hardware.
- Do not cap two outlets on a four-port case as the default solution. That can halve the available discharge area and increase static pressure; accept an adapter only after a sealed-plenum and full-speed airflow/freeze test proves the coil and blower remain healthy.
- Keep all Rev H vent apertures and duct coordinates on HOLD. Issue a Rev I fascia/console layout only after the vehicle's available `W x H x D` envelope, fitting side, drain fall, service-removal path, and the selected unit and louver necks are physically measured.
- Preserve windscreen demist separately: retain the original heater/demist path, or provide dedicated small demist takeoffs from the new plenum. The two occupant outlets must not be treated as the only safety-demist provision.

Use [hvac-dashboard-vent-duct-layout-20260602.md](hvac-dashboard-vent-duct-layout-20260602.md) for the active two-outlet gates and the superseded Rev H record.

## Gates

### `AC-CABIN-001` - Cabin Evaporator Package

- Confirm case dimensions, coil face, core depth, intake face, outlet count/OD, refrigerant fittings, TXV/expansion valve, drain nipple, mounting tabs, and service access.
- Bench pressure/vacuum leak-test before installation.
- Bench airflow-test with the selected external blowers, not only the unit's included blower if present.
- Cardboard-mock under the J40 dash before cutting brackets, ducts, or drain holes.
- Confirm the purchased slimline/under-dash unit can route condensate outside the cabin and can connect to barrier hoses without sharp bends or service-blocking fittings.
- Confirm the evaporator/plenum has two usable occupant-vent takeoffs and can support the planned two-outlet distribution without starving the retained or dedicated demist path.

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
- Use the public 3-position `BLOWER` selector only as an input to the measured resistor/PWM/relay arrangement and the 2-position `A/C` selector only as a compressor request through thermostat and pressure safeties. Retain or separately mount the delivered unit's thermostat/temperature/blend controller. The `ENGINE` selector is outside the HVAC circuit and remains electrically on HOLD until EEI-003 proves the correct fail-safe interface.

### `AC-CHARGE-001` - Final Validation

- Deep vacuum, leak hold, measured oil/refrigerant charge, blower-speed check, compressor-clutch cutout check, condenser-fan request, condensate drain water test, and cabin airflow/demist checks must all pass before closure.
