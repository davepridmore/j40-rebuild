# Toyota 2H (Serial 117299) Turbo Suitability and Options

> **Identity update 2026-08-02:** the owner-supplied block-stamp photograph shows `2H 117299`. Record the engine as `2H-117299`. The reported early-to-mid-1980s production date is plausible but remains unverified without a factory serial-to-date source.

## Preliminary Verdict

The fitted engine is positively classified as Toyota `2H-117299`: a 3,980 cc inline-six, 12-valve OHV, naturally aspirated indirect-injection diesel, with typical published naturally aspirated output around `105-107 PS` (`77-80 kW`). A conservative turbo conversion remains an engineering option only if measured health passes. The objective remains earlier usable road torque and reduced altitude power loss—not maximum dyno output.

The controlled starting direction is:

- a Toyota `2H`-specific low-mount manifold with CT26 four-bolt flange, verified against the supplied part and the actual head;
- a compact CT26-pattern `TD05H 16G` with documented `7 cm² / approximately .49 A/R` turbine housing and internal wastegate, subject to map/specification and goods-receipt checks;
- `5-7 psi` initial calibration at baseline fuelling. Any move toward `8-10 psi` requires a new written engine-builder/diesel-specialist release based on logged EGT, coolant temperature, oil pressure, boost/drive pressure, smoke and head-sealing evidence;
- an intercooler included in the packaging plan;
- a free-flowing single exhaust sized and routed by the fabricator after the turbo outlet is fixed;
- pre-turbine EGT, boost, oil-pressure, and coolant-temperature instrumentation installed before fuelling changes;
- injection-pump calibration by a diesel specialist only after the air system is complete and leak-free.

This is a package-direction release, not a blind bolt-in release. Engine identity is closed, but the exact manifold-to-head, turbo-to-manifold, oil-gallery, sump, intake, steering and accessory interfaces still require physical verification. See [2h-turbo-recommended-build-process-20260801.md](2h-turbo-recommended-build-process-20260801.md).

## Rev G Cooling Boundary — Capacity, Not Engine Approval

The cooling package is now specified as a **hard 50°C release condition**, not a general hot-weather preference: `50°C` dry-bulb air measured at the grille/cooling-pack inlet, with A/C operating, plus a `52°C` ten-minute heat soak and hot restart. The engine radiator must prove at least `115 kW` continuous heat rejection after stabilisation and `130 kW` for ten minutes. The main radiator/condenser path uses the engine-driven puller with a sealed full-face shroud (`≥9,000 m³/h` installed at `125 Pa` and `1,500 rpm`) plus independently fused/relayed A/C pushers (`≥3,000 m³/h` installed at `75 Pa` and `13.5 V`).

Charge cooling follows the active Rev G integrated front-pack architecture. Its core position, airflow and pressure-loss requirements must be validated with the final 2H compressor match and actual charge flow; superseded side/wing-cooler assumptions are not a release basis.

The defined `150 bhp` cooling-system thermal-design envelope is a heat-rejection capacity requirement only. It is not approval for `2H-117299` to produce that power or to run arbitrary boost. Initial turbo calibration remains `5-7 psi`; cooling capacity does not waive the separate engine-builder/diesel-specialist release required for any move toward `8-10 psi`.

## What The Project Already Establishes

| Item | Current project basis | Confidence / consequence |
| --- | --- | --- |
| Engine | Toyota `2H-117299`, 3,980 cc naturally aspirated diesel | High confidence: owner-supplied block-stamp photograph shows the 2H prefix and serial. Record castings and interfaces for fitment, not reclassification. |
| Cooling layout | Converted-vehicle, HJ47/2H-style hose and radiator arrangement | Strong engine-family basis, but this converted vehicle still requires measured hose, neck, fan and shroud interfaces. |
| Gearbox | Fitted five-speed; exact type unconfirmed | The engine serial does not identify the transmission. Do not order H55F-specific oil/parts or set a torque target until case/top-cover marks confirm the unit. |
| Intended vehicle | 1978 J40 restoration, road and utility use | Favors low-rpm response, controlled cylinder pressure, and durability over peak power. |
| Exhaust | Final route and hangers are not yet frozen | Helpful: the downpipe, heat shields, and full exhaust can be designed around the chosen turbo while access is open. |
| A/C and cooling work | 50°C Rev G cooling system is being designed | Turbo heat load, condenser obstruction, installed fan performance, shroud sealing and charge-air performance must be validated together on the 2H installation. |

## Why A Conservative Setup Fits

The 2H is a large, low-speed diesel. A rough planning calculation for `3.98 L` at about `3,500 rpm` and `80%` volumetric efficiency gives naturally aspirated airflow near `15 lb/min`. At modest boost, useful compressor demand is broadly in the low-to-mid `20 lb/min` region. This is a sizing guide only; final matching must include altitude, air temperature, target rpm, pressure losses, measured volumetric efficiency and an actual compressor map.

A larger turbo may advertise more peak airflow but can move boost later in the rev range, increase smoke before spool, and make the truck less pleasant in normal use. A very small turbo can give excellent response but create high exhaust backpressure and EGT at sustained load. Compressor selection and turbine selection therefore have to be checked separately.

## Configuration Choices

| Choice | Indicative hardware direction | Character | Main advantages | Main cautions | Position |
| --- | --- | --- | --- | --- | --- |
| A — controlled low-mount direction | 2H low-mount CT26-flange manifold plus CT26-pattern `TD05H 16G`, documented `7 cm² / approximately .49 A/R`, internal wastegate | Early road response | Matches the identified engine family and existing planning direction | Verify exact supplied trim, actuator, maps, porting, oil interfaces and vehicle clearance | **Selected, subject to gates** |
| B — balanced alternative | Small GT25-family or compact HX30-class unit, map-verified | Slightly later response with more airflow margin | Potential headroom if later testing justifies it | Turbine choice and fabrication may sacrifice low-speed response | Shortlist only after measurements |
| C — period/simple 2H conversion | Fully identified, proven 2H-specific journal-bearing wastegated kit | Depends on actual kit | Potentially simpler local service | Age, condition, map, oil restriction and wastegate control can be unknown | Consider only with full identification and test evidence |
| D — large power-oriented turbo | Large original-style CT26/HX35-class or similar | Late spool and high peak headroom | Supports power levels outside this plan | Poor fit to the airflow goal; encourages excess fuel and driveline load; packaging and heat burden rise | **Do not pursue for the current objective** |

Model-family names describe a sizing direction, not interchangeable purchase approvals. Wheel trims, turbine housings, wastegate settings, and counterfeit/rebuilt condition can make two apparently identical turbos behave very differently.

## Proposed Operating Envelope

| Parameter | Initial plan | Release rule |
| --- | --- | --- |
| Boost | `5-7 psi` initial calibration | Baseline fuelling, stable wastegate control, no charge leaks, clean smoke response, acceptable EGT/coolant temperature, and healthy hot oil pressure. |
| Higher boost | Consider no more than roughly `8-10 psi` within this conservative path | Not pre-approved; requires loaded logs, drive-pressure review, head-sealing assessment, diesel-specialist fuelling review, and written engine-builder plus clutch/driveline acceptance. |
| EGT sensor | Pre-turbine thermocouple | Install before adding fuel; agree the continuous and short-duration alarm limits with the engine builder/tuner for this exact sensor position and engine. |
| Intercooling | Intercooling remains mandatory | Revalidate the active integrated Rev G front-pack core against the final 2H turbo match, actual charge flow, A/C load and 50°C test condition. |
| Fuelling | Baseline pump setting until turbo system is proven | Adjust gradually on measured boost/EGT with no sustained visible smoke. |
| Exhaust | Low-restriction system with flex provision, heat shields, and serviceable joints | Final diameter and muffler selected after turbo outlet and full chassis/body clearances are known. |

## Engine Suitability Checks

Perform these on a fully warmed engine wherever applicable and record the raw readings, test method, oil grade, coolant condition, ambient temperature, and instrument used.

1. Photograph the engine number/code, injection pump tag, injector type, exhaust manifold face, oil-filter housing, vacuum-pump arrangement, sump, and both sides of the engine bay.
2. Compression-test all six cylinders with the same gauge and cranking procedure. Judge both absolute pressure against the correct Toyota 2H manual and cylinder-to-cylinder spread.
3. If compression is questionable, run leak-down or targeted diagnosis before considering boost.
4. Measure oil pressure cold and fully hot at idle and at specified test rpm; compare with the correct Toyota manual specification.
5. Check crankcase pressure/blow-by warm, ideally with a measured manometer result rather than an oil-cap impression alone.
6. Pressure-test the cooling system and cap; verify thermostat operation, fan/shroud condition, pump condition, radiator flow, and temperature stability on a sustained loaded baseline run.
7. Test injectors for opening pressure, pattern, leakage, and balance; inspect/calibrate the injection pump with a diesel specialist.
8. Record baseline exhaust smoke and, if possible, pre-turbine EGT on a repeatable loaded route before changing fuelling.
9. Inspect oil consumption, coolant consumption, oil/coolant cross-contamination, rear-main/front-seal leakage, and abnormal bearing or combustion noise.
10. Confirm clutch slip margin in a high-gear loaded test only after the vehicle is otherwise safe, then inspect gearbox/transfer and differential oils for debris.

### Immediate No-Go Findings

- one or more materially weak cylinders or a wide unexplained compression spread;
- low hot oil pressure;
- heavy measured blow-by or significant oil consumption;
- coolant pressurisation, overheating, poor radiator flow, or unresolved head-gasket evidence;
- injector dribble, uncontrolled pump fuelling, or heavy baseline smoke;
- clutch slip, serious gearbox/transfer noise, or significant metal in drivetrain oil;
- no safe gravity oil-drain path from the proposed turbo location to the sump;
- unavoidable exhaust heat exposure to brake, clutch, fuel, A/C, steering, wiring, or body components.

## Packaging Decisions To Capture While Stripped

- Turbo/manifold position relative to bonnet, wing, steering, starter, alternator, oil filter, vacuum pump, A/C compressor, engine mount, and service-tool access.
- Downpipe route and engine-movement envelope; keep it clear of brake/clutch lines, fuel hoses, wiring, A/C hoses, floor, and body mounts.
- Turbo oil-feed source and measured pressure; specify the feed/restrictor to the chosen turbo manufacturer's requirement.
- Oil-drain fall, diameter, entry angle, and sump entry above the normal oil level; no uphill section or tight bend.
- Air-cleaner-to-compressor route and compressor-to-intercooler-to-manifold route with flexible engine-movement joints.
- Active integrated-front-pack intercooler position, ducting and service access; measure the complete cooling and charge-air systems under installed pressure/temperature conditions, not each core in isolation.
- Heat shielding and thermal barriers around the turbine, manifold, downpipe, brake/clutch hydraulics, wiring, bonnet, and intake plumbing.
- Service removal path for the oil filter, starter, alternator, belts, A/C compressor, and turbo itself.

## Complete Connection Schedule

| Connection | From | To | Medium / signal | Control and acceptance |
| --- | --- | --- | --- | --- |
| Exhaust inlet | Measured 2H exhaust ports and verified 2H low-mount manifold | Turbine inlet | Hot exhaust gas | Flat sealed flanges, heat-rated studs/gaskets, supported turbo, no cracks or leaks. |
| Exhaust outlet | Turbine outlet | Downpipe, flex joint, muffler and tailpipe | Hot exhaust gas | Serviceable flange/V-band, smooth first bend, independent hangers, body/line/propshaft clearance. |
| Clean-air inlet | Sealed serviceable air cleaner | Compressor inlet | Filtered intake air | Collapse-resistant duct, supported airbox, engine-movement allowance, no unfiltered joints. |
| Charge-air hot side | Compressor outlet | Intercooler inlet | Pressurised hot air | Beaded pipe, reinforced couplers, matched clamps, pressure/leak test. |
| Charge-air cold side | Intercooler outlet | Measured 2H intake adapter/plenum | Pressurised cooled air | Short supported route, even plenum entry, boost-reference ports, pressure/leak test. |
| Oil supply | Verified 2H oil-gallery take-off | Turbo bearing-housing inlet | Pressurised engine oil | Measured port thread/pressure, manufacturer-specified line and restrictor only if required, heat protection. |
| Oil drain | Turbo bearing-housing outlet | Sump bung above normal oil level | Gravity oil return | Large bore, continuous fall, no trap/kink, sump removed/cleaned for welding, leak test. |
| Turbo coolant (conditional) | Approved engine cooling take-off | Water-cooled bearing housing and approved return | Engine coolant | Only if chosen turbo requires it; correct flow direction, no air trap, heater/cooling function retained. |
| Crankcase ventilation | 2H breather through sized separator | Clean-air duct before compressor | Blow-by gas and oil mist | Measured blow-by basis, low restriction, serviceable separator, no open oily vent near exhaust. |
| Wastegate reference | Intake plenum/compressor reference per turbo specification | Internal wastegate actuator | Pneumatic boost pressure | Short heat-safe hose, secure barbs, fail-safe mechanical actuator, initial `5-7 psi` setting. |
| Boost gauge/reference | Intake plenum | Mechanical gauge or electronic pressure sensor | Pneumatic pressure / electrical signal | Dedicated sealed port, damped signal if necessary, no leak-prone unsupported tee. |
| Pump boost compensation (conditional) | Intake plenum | Injection-pump aneroid/compensator | Pneumatic boost pressure | Only if diesel specialist confirms a suitable compensator; no blind fuel-screw-only tuning. |
| EGT measurement | Pre-turbine exhaust manifold | EGT gauge/controller | Thermocouple millivolt signal | Correct probe depth, compression fitting, correct extension-wire alloy/polarity, separated protected routing. |
| Oil-pressure measurement | Verified 2H oil gallery | Gauge/sender and retained warning function | Pressure / electrical signal | Supported adapter, correct thread/range, no heavy sender hanging from an unsupported tee. |
| Coolant-temperature measurement | Representative engine outlet/head point | Gauge/sender and retained warning function | Temperature-dependent electrical signal | Correct thread/calibration; compare against workshop reference during validation. |
| Gauge power | New fused ignition-switched instrument branch | EGT/boost/oil/coolant instruments | 12 V electrical | Fuse by measured load and wire size, labelled connector, clean ground, key-off shutdown. |
| Gauge illumination | Dash lighting/dimmer circuit if compatible | Gauge illumination inputs | 12 V electrical | Confirm dimmer compatibility; otherwise use documented switched illumination feed. |
| Alarm outputs | Instrument alarm outputs, if fitted | Warning lamp/buzzer | Low-current electrical signal | Relay only if load requires; test alarms before road tuning. |
| Electric fan (if required) | Battery-protected distribution through fuse/relay | Intercooler/condenser fan | High-current 12 V electrical | Measure inrush/running current; temperature/A-C/manual logic; override must not bypass pressure protection. |

### Electrical Architecture

The recommended wastegated turbo is mechanically controlled and does not need an ECU, CAN connection, electronic throttle, or boost-control solenoid. The electrical addition is a dedicated instrument/protection branch:

1. Take one ignition-switched trigger from the documented fuse/relay architecture, not directly from an old unidentified engine wire.
2. Feed a small dedicated fuse block or labelled fused branch sized to the actual gauge set.
3. Provide a clean instrument ground returned to the approved dash/body ground point; verify voltage drop to battery negative.
4. Route EGT thermocouple extension cable as supplied by the instrument manufacturer without substituting ordinary copper wire; preserve polarity and keep it away from alternator, starter and relay-bank noise.
5. Route boost-sensor, oil-pressure and coolant-sender wiring in heat/oil-resistant loom with service loops, grommets, strain relief and labelled connectors.
6. Keep sensor wiring away from the turbine/downpipe and separated from starter, alternator, winch, fan and compressor-clutch high-current runs.
7. Retain independent factory warning functions where possible; new gauges supplement rather than silently replace oil-pressure or coolant warnings.
8. Bench-test gauge sweep, sender response, alarm outputs, dimming and key-off behavior before closing the dash and firewall loom.

## Recommended Decision Sequence

1. Confirm engine and gearbox identity.
2. Complete compression, hot oil-pressure, blow-by, cooling, injector, and pump checks.
3. Set the performance objective in words: earlier torque and hill/altitude drivability, not maximum output.
4. Capture the engine-bay, oil-drain, intercooler, downpipe, and cooling-stack measurements.
5. Compare mapped GT2256-size and small GT25/HX30-size candidates at the intended rpm, boost, Lahore/Karachi summer inlet temperature, and expected altitude use.
6. Choose the turbine housing using response and expected drive pressure, not compressor name alone.
7. Approve one complete bill of materials, including gauges, oil plumbing, intercooler/charge plumbing, wastegate control, exhaust, heat protection, gaskets, fasteners, and spare service parts.
8. Install and validate at baseline fuelling, then commission progressively within `5-7 psi` with logged evidence. Treat any move toward `8-10 psi` as a separate release decision.

## References

- Owner-supplied block-stamp photograph dated 2026-08-02: visible `2H` engine-code prefix and serial `117299`; this is the controlling engine-family evidence.
- Specter Off-Road's Toyota manual catalog separates the 2H manual period from the earlier H family; it is supporting family-era context, not a serial-to-date decoder. <https://www.sor.com/cat/223e>

- Project evidence: [master-project-plan.md](master-project-plan.md), [engine-radiator-recore-release-20260529.md](engine-radiator-recore-release-20260529.md), [front-cooling-stack-fabrication-plan-20260530.md](front-cooling-stack-fabrication-plan-20260530.md), and `data/manual/procurement_decision_matrix.csv`.
- BorgWarner, “MatchBot: A Shortcut Method”: turbo matching inputs include displacement, ambient temperature, altitude, fuel, engine speed, and boost; compressor and turbine stages must both be matched. <https://www.borgwarner.com/aftermarket/boosting-technologies/news/2022/05/20/matchbot-a-shortcut-method>
- BorgWarner, “Understanding Compressor Maps: Sizing a Turbocharger”: compressor operation must remain within the mapped operating and turbo-speed limits. <https://www.borgwarner.com/aftermarket/transmission-technologies/news?date=2022-05-23&itemurl=understanding-compressor-maps-sizing-a-turbocharger>
