# Toyota 2H Turbo Suitability and Options

## Preliminary Verdict

The retained Toyota 2H is a plausible candidate for a conservative turbocharger conversion if its measured health is good. The build should target earlier, more usable road torque and reduced altitude power loss—not maximum dyno output.

The preferred starting concept is:

- a modern wastegated turbo in the Garrett GT2256 / small GT25 or Holset HX30-class response range;
- approximately `5-7 psi` initial boost, with any move toward `8-10 psi` requiring clean logged EGT, coolant temperature, boost control, smoke, and oil-pressure results;
- an intercooler included in the packaging plan;
- a free-flowing single exhaust sized and routed by the fabricator after the turbo outlet is fixed;
- pre-turbine EGT, boost, oil-pressure, and coolant-temperature instrumentation installed before fuelling changes;
- injection-pump calibration by a diesel specialist only after the air system is complete and leak-free.

This is a preliminary engineering direction, not a parts release. The turbo model, turbine housing, manifold, boost target, and fuelling setting remain open until the checks below are complete.

## What The Project Already Establishes

| Item | Current project basis | Confidence / consequence |
| --- | --- | --- |
| Engine | Toyota `2H`, naturally aspirated diesel, six glow plugs | High enough for planning; photograph the block/ID marks before ordering engine-specific hardware. |
| Cooling layout | `HJ47 / 2H`-style hose and radiator pattern | Strong project evidence; the planned 70-series radiator/condenser stack still needs an as-installed heat-rejection test. |
| Gearbox | Five-speed; `H55F` is the active candidate | Do not set a torque target until case/top-cover marks confirm it and oil/debris condition is checked. |
| Intended vehicle | 1978 J40 restoration, road and utility use | Favors low-rpm response, controlled cylinder pressure, and durability over peak power. |
| Exhaust | Final route and hangers are not yet frozen | Helpful: the downpipe, heat shields, and full exhaust can be designed around the chosen turbo while access is open. |
| A/C and cooling work | Front radiator/condenser/fan package is being redesigned | Turbo heat load, condenser obstruction, fan/shroud performance, and under-bonnet airflow must be validated together. |

## Why A Conservative Setup Fits

The 2H is a large, low-speed diesel. A rough planning calculation for a `4.0 L` engine at about `3,500 rpm` and `80%` volumetric efficiency gives naturally aspirated airflow near `15 lb/min`. At pressure ratios associated with modest boost, the useful compressor demand is broadly in the low-to-mid `20 lb/min` region. This is a sizing guide only; final matching must include altitude, air temperature, target rpm, pressure losses, and an actual compressor map.

A larger turbo may advertise more peak airflow but can move boost later in the rev range, increase smoke before spool, and make the truck less pleasant in normal use. A very small turbo can give excellent response but create high exhaust backpressure and EGT at sustained load. Compressor selection and turbine selection therefore have to be checked separately.

## Configuration Choices

| Choice | Indicative hardware direction | Character | Main advantages | Main cautions | Position |
| --- | --- | --- | --- | --- | --- |
| A — conservative response | Garrett `GT2256` / equivalent modern wastegated unit, final housing by map and drive-pressure check | Earliest useful boost, strong road drivability | Best match to modest airflow goal; compact packaging; supports low initial boost | Avoid a turbine housing so small that sustained-load backpressure and EGT rise sharply | **Preferred starting point** |
| B — balanced headroom | Small `GT25` family or compact `HX30`-class unit, map-verified | Slightly later boost with more airflow margin | Better headroom if later testing supports `8-10 psi`; robust common diesel architecture | More sensitive to turbine housing choice; may sacrifice low-speed response | Shortlist after measurements |
| C — period/simple conversion | Proven 2H-specific manifold and conventional journal-bearing wastegated turbo kit | Depends heavily on the actual kit | Easier manifold/downpipe solution and potentially easier local service | Many kits use old or poorly documented turbo matches; condition, map, oil restriction, and wastegate control can be unknown | Accept only with full identification and test evidence |
| D — large power-oriented turbo | Large CT26/HX35-class or similar | Late spool and high peak headroom | Supports power levels outside this plan | Poor fit to the airflow goal; encourages excess fuel and driveline load; packaging and heat burden rise | **Do not pursue for the current objective** |

Model-family names describe a sizing direction, not interchangeable purchase approvals. Wheel trims, turbine housings, wastegate settings, and counterfeit/rebuilt condition can make two apparently identical turbos behave very differently.

## Proposed Operating Envelope

| Parameter | Initial plan | Release rule |
| --- | --- | --- |
| Boost | `5-7 psi` initial calibration | Stable wastegate control, no charge leaks, clean smoke response, acceptable EGT/coolant temperature, and healthy hot oil pressure. |
| Higher boost | Consider no more than roughly `8-10 psi` within this conservative path | Only after logged loaded testing, diesel-specialist fuelling review, and clutch/driveline acceptance. This is not pre-approved. |
| EGT sensor | Pre-turbine thermocouple | Install before adding fuel; agree the continuous and short-duration alarm limits with the engine builder/tuner for this exact sensor position and engine. |
| Intercooling | Plan to fit | May be omitted only if logged compressor-outlet/intake temperatures and packaging analysis justify it; A/C condenser and radiator airflow cannot be compromised. |
| Fuelling | Baseline pump setting until turbo system is proven | Adjust gradually on measured boost/EGT with no sustained visible smoke. |
| Exhaust | Low-restriction system with flex provision, heat shields, and serviceable joints | Final diameter and muffler selected after turbo outlet and full chassis/body clearances are known. |

## Engine Suitability Checks

Perform these on a fully warmed engine wherever applicable and record the raw readings, test method, oil grade, coolant condition, ambient temperature, and instrument used.

1. Photograph the engine number/code, injection pump tag, injector type, exhaust manifold face, oil-filter housing, vacuum-pump arrangement, sump, and both sides of the engine bay.
2. Compression-test all six cylinders with the same gauge and cranking procedure. Judge both absolute pressure against the correct 2H manual and cylinder-to-cylinder spread.
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
- Intercooler position that does not starve the A/C condenser and radiator; measure the complete cooling stack pressure/temperature performance, not each component in isolation.
- Heat shielding and thermal barriers around the turbine, manifold, downpipe, brake/clutch hydraulics, wiring, bonnet, and intake plumbing.
- Service removal path for the oil filter, starter, alternator, belts, A/C compressor, and turbo itself.

## Complete Connection Schedule

| Connection | From | To | Medium / signal | Control and acceptance |
| --- | --- | --- | --- | --- |
| Exhaust inlet | 2H exhaust ports and turbo manifold | Turbine inlet | Hot exhaust gas | Flat sealed flanges, heat-rated studs/gaskets, supported turbo, no cracks or leaks. |
| Exhaust outlet | Turbine outlet | Downpipe, flex joint, muffler and tailpipe | Hot exhaust gas | Serviceable flange/V-band, smooth first bend, independent hangers, body/line/propshaft clearance. |
| Clean-air inlet | Sealed serviceable air cleaner | Compressor inlet | Filtered intake air | Collapse-resistant duct, supported airbox, engine-movement allowance, no unfiltered joints. |
| Charge-air hot side | Compressor outlet | Intercooler inlet | Pressurised hot air | Beaded pipe, reinforced couplers, matched clamps, pressure/leak test. |
| Charge-air cold side | Intercooler outlet | 2H intake adapter/plenum | Pressurised cooled air | Short supported route, even plenum entry, boost-reference ports, pressure/leak test. |
| Oil supply | Verified 2H oil-gallery take-off | Turbo bearing-housing inlet | Pressurised engine oil | Measured port thread/pressure, manufacturer-specified line and restrictor only if required, heat protection. |
| Oil drain | Turbo bearing-housing outlet | Sump bung above normal oil level | Gravity oil return | Large bore, continuous fall, no trap/kink, sump removed/cleaned for welding, leak test. |
| Turbo coolant (conditional) | Approved engine cooling take-off | Water-cooled bearing housing and approved return | Engine coolant | Only if chosen turbo requires it; correct flow direction, no air trap, heater/cooling function retained. |
| Crankcase ventilation | 2H breather through sized separator | Clean-air duct before compressor | Blow-by gas and oil mist | Measured blow-by basis, low restriction, serviceable separator, no open oily vent near exhaust. |
| Wastegate reference | Intake plenum/compressor reference per turbo specification | Internal wastegate actuator | Pneumatic boost pressure | Short heat-safe hose, secure barbs, fail-safe mechanical actuator, initial 5-7 psi setting. |
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
8. Install and validate at baseline fuelling, then tune progressively from `5-7 psi` with logged evidence.

## References

- Project evidence: [master-project-plan.md](master-project-plan.md), [engine-radiator-recore-release-20260529.md](engine-radiator-recore-release-20260529.md), [front-cooling-stack-fabrication-plan-20260530.md](front-cooling-stack-fabrication-plan-20260530.md), and `data/manual/procurement_decision_matrix.csv`.
- BorgWarner, “MatchBot: A Shortcut Method”: turbo matching inputs include displacement, ambient temperature, altitude, fuel, engine speed, and boost; compressor and turbine stages must both be matched. <https://www.borgwarner.com/aftermarket/boosting-technologies/news/2022/05/20/matchbot-a-shortcut-method>
- BorgWarner, “Understanding Compressor Maps: Sizing a Turbocharger”: compressor operation must remain within the mapped operating and turbo-speed limits. <https://www.borgwarner.com/aftermarket/transmission-technologies/news?date=2022-05-23&itemurl=understanding-compressor-maps-sizing-a-turbocharger>
