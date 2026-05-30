# J40 Digital Twin As-Fitted Cable And Route Scope - 2026-05-31

## Decision

The J40 3D model is no longer only a visual scaffold. It must become an as-fitted packaging model for the actual truck before fabrication and closeout decisions rely on it.

Treat "every cable" as every service-critical routed item:

- electrical cables, wiring looms, earth straps, fuse/relay branches, sensor wires, lighting feeds, A/C compressor and fan wiring
- brake, clutch, fuel, vacuum, refrigerant, coolant, overflow, drain, and heater hoses or hard lines
- parking-brake, throttle, choke, fuel-stop, heater-control, and other mechanical control cables
- accessory wiring or hoses added during the rebuild, including condenser fan, under-dash evaporator, relays, MIDI fuse outputs, and front lamps

No route is released by a generic "loom blob" or hidden line. If it can foul, melt, rub, leak, block service access, or affect fabrication, it needs a named route ID and visible CAD centerline.

## Drive And Drivetrain Orientation Hold

The drive layout and drivetrain orientation must be verified against the actual as-fitted truck, not assumed from a generic FJ40 model.

Release checks:

- right-hand-drive steering wheel, pedal box, brake booster/master, clutch master, steering column, steering box, pitman arm, drag link, and tie rod orientation
- 2H engine position, alternator/compressor side, starter side, fan/radiator centerline, gearbox and transfer-case position
- front and rear prop-shaft angles, transfer outputs, yoke clocking, axle differential offsets, and handbrake or parking-brake hardware relationship
- cabin control direction and reach: gear lever, transfer levers, handbrake, throttle/choke/fuel-stop if retained

Until those are checked, the model can show visual intent but must not be used as release geometry for brackets, routing clips, A/C hoses, hard lines, or body closeout.

## Model Levels

| Level | Use | Release Meaning |
| --- | --- | --- |
| L0 | envelope/block placeholder | visual packaging only |
| L1 | routed centerline | start/end points, pass-throughs, and approximate path are visible |
| L2 | physical route envelope | outside diameter, bend radius, clip points, service sweep, and clearance zones are captured |
| L3 | fabrication/release geometry | bracket holes, clamp tabs, grommets, bulkheads, hose lengths, and fitting clocks are measured |

All new route work should be planned to at least L2. Anything used to cut, drill, weld, crimp, or wrap must reach L3.

## Required Route Families

Electrical power:

- battery positive to cutoff/kill switch
- cutoff output to relay box feed and MIDI common feed
- all five MIDI output branches, including the enlarged far-side output carrying two cables
- battery negative to chassis, engine block, body, and any supplemental earth straps
- starter main cable and solenoid trigger
- alternator B+ cable, regulator/sense/exciter wiring, and charge warning branch

Engine and front loom:

- engine sender wiring, injection-pump/fuel-stop wiring, glow circuit where present, temperature/oil/charge sender branches
- headlamp, front marker/indicator, horn, auxiliary lamp, and front earth routes
- A/C compressor clutch feed, pressure/trinary switch wiring, condenser fan relay output, and fan earth
- firewall/bulkhead pass-throughs, grommets, clips, abrasion sleeves, and drip loops

Cabin and HVAC:

- under-dash evaporator blower feed, control panel wiring, thermostat/sensor wiring, drain hose, and refrigerant hose pass-throughs
- dash harness branches, gauge/switch wiring, EPS/controller routes if retained, and pedal/column clearance sweeps

Chassis, brake, fuel, and rear body:

- front brake hard lines, flex hoses, master/proportioning connections, and tube clips
- rear axle hard lines, center flex hose, rear brake T, wheel-cylinder lines, and clip locations
- parking-brake cables, equalizer, clevises, frame/axle clips, spring clearance, and movement arc
- fuel supply, return, leak-off, filler neck, vent, sender wiring, and tank access/service routes
- rear body/tail lamp/number plate/fuel-sender loom and body-to-chassis flex section

A/C and cooling:

- compressor discharge to condenser, condenser outlet to receiver-drier, drier to evaporator/expansion valve, evaporator suction to compressor
- drier bracket and pressure switch service clearance
- heater hoses, radiator hoses, overflow bottle hose, condensate drain, and fan/shroud clearance

Control and service cables:

- throttle, choke, fuel-stop, heater-control, handbrake, speedometer cable, and any cable that crosses the firewall, floor, frame, or moving driveline area

## Evidence Required Per Route

Each route needs enough evidence to answer these before release:

- What are the two endpoints?
- Where does it pass through sheet metal, frame, bulkhead, bracket, or grommet?
- What is the outside diameter or bundle size?
- What is the minimum bend radius?
- What clips, P-clips, tabs, saddles, grommets, sleeves, or guards hold it?
- What can it touch at full steering lock, suspension travel, engine movement, bonnet close, body fit, or vibration?
- What heat sources and sharp edges are nearby?
- Can the part still be serviced without cutting a wrapped loom or removing welded brackets?

Photo-only routes can enter the CAD as L1. Fabrication or crimping routes need ruler photos, removed-part samples, component dimensions, or direct truck measurements before release.

## CAD Acceptance Rules

- Every route gets a stable `route_id`.
- Every route is visible in the CAD/viewer as a named path, sweep, tube, hose, cable, loom, or clearance envelope.
- Every firewall/pass-through has a matching hole/grommet/bulkhead entry.
- Every clip or support point is represented or listed as missing.
- Every moving-clearance route has a recorded clearance check.
- Every A/C hose has port style, fitting angle, hose size, and crimp/service clearance held before purchase or charge.
- Every brake/fuel hard line has clip and corrosion/abrasion protection shown before chassis coating.
- Every electrical heavy cable has bend sweep, lug clocking, fuse/cutoff relationship, and chafe protection shown before final wrap.

The route backlog lives at `data/manual/cad/j40_reference_model/05_reports/j40_as_fitted_route_model_scope_20260531.csv`.
