# J40 Front Cooling Stack Frame - Rev A

Purpose: fabricate a front cooling-stack frame that carries the engine radiator, A/C condenser, optional pusher fan, and receiver-drier from the chassis/front-support structure instead of hanging any load from the radiator core or condenser fins.

This package is a fabrication design release for mock-up and shop discussion. It supersedes the idea of only adding a small missing radiator leg if the front support is being rebuilt as two full-height uprights. The existing `front_radiator_two_side_retention_rev_a` bracket remains the measurement basis for the radiator-side upright geometry.

Pakistan-local buy package: [local_parts_selection_pakistan_20260530.csv](local_parts_selection_pakistan_20260530.csv), [known_price_fit_check_pakistan_20260530.csv](known_price_fit_check_pakistan_20260530.csv), and [front-cooling-stack-local-parts-selection-20260530.md](../../../../docs/front-cooling-stack-local-parts-selection-20260530.md).

L4TW delivery spec: [delivery_spec_l4tw_20260531.csv](delivery_spec_l4tw_20260531.csv) and [l4tw-front-cooling-stack-delivery-spec-20260531.md](../../../../docs/l4tw-front-cooling-stack-delivery-spec-20260531.md).

## Design Intent

- Build two full-height left/right cooling-stack uprights from the chassis/front-support rail up to the radiator top plane.
- Use the uprights as the structure for both cooling systems:
  - engine radiator on rubber-isolated rear tabs
  - A/C condenser on separate forward tabs
  - optional condenser pusher fan on a separate fan hoop/crossbar
  - receiver-drier on a removable side clamp bracket
- Keep the stack serviceable: radiator, condenser, fan, and drier must be removable without cutting welded parts.
- Do not drill, weld, or hard-clamp through radiator tanks, radiator core, condenser tubes, or condenser fins.
- Preserve fan, belt, pulley, hose, bonnet latch, grille, and front panel clearance before final drilling.

## Working Component Picks

| Component | Working pick | Release rule |
| --- | --- | --- |
| Engine radiator | HJ47 / 2H radiator pattern, Toyota reference `16400-68030`, common aftermarket core about `435 x 530-540 x 60-64 mm` | Buy or build only after old radiator sample and leg spacing confirm hose necks, cap, drain, mounts, and fan clearance. |
| A/C condenser | Parallel-flow R134a condenser; start with `14 x 22 in` / about `356 x 559 x 21 mm`; upgrade to `14 x 24 in` only if the grille/upright opening proves it | Must mount forward of radiator with its own rubber-isolated tabs and at least `10-15 mm` radiator air gap. |
| Receiver-drier | R134a drier with `#6` O-ring ports and binary/trinary switch port | Mount vertical on side upright, after condenser outlet and before TXV/evaporator feed. |
| Optional pusher fan | Slim `12-14 in` condenser pusher fan | Mount to frame/fan hoop, not through condenser or radiator fins. Verify grille clearance. |
| Existing compressor | Sanden-type compact compressor already installed on 2H bracket | Likely compatible with the above if clutch voltage, belt alignment, R134a oil state, leak test, and port fittings pass the compressor gate below. |

## Pakistan Local Buy List

| Component | Selected local route | Supplier lead | Hold before payment |
| --- | --- | --- | --- |
| Engine radiator | Custom/recored HJ47/2H-pattern radiator from old sample | Master Radiators preferred; KorTech alternate | Old sample dimensions, necks, cap, drain, corrected tabs, fan clearance, and pressure test. |
| A/C condenser | Snow Cool `MM CONDENSOR` first; Arsalan `Condenser Kia Sportage new model` as large alternate | Snow Cool / Arsalan Autos | Tape photos for overall size, thickness, fitting side, port size/thread, bracket tabs, and parallel-flow/R134a suitability. |
| Condenser fan | Slim `12V` pusher fan assembly, complete with blade/shroud/mount feet | Cool Sun / Snow Cool / Arsalan Autos | Diameter, depth, current draw, pusher airflow direction, and grille clearance. |
| Receiver-drier | New R134a receiver-drier with matched O-ring ports and switch port | Snow Cool driers / Arsalan receiver driers | Sealed caps, flow arrow, port size/thread, and binary/trinary switch compatibility. |
| Hoses/fittings | R134a barrier hose set with service ports and HNBR O-rings | Arsalan / Cool Sun / Snow Cool; Sanpak fallback | Actual compressor/condenser/drier/evaporator port match and dry-fit routing before crimping. |
| Compressor | Reuse installed Sanden-type compressor unless it fails the gate | Existing compressor; Arsalan/Sanpak replacement if needed | `12V` clutch, pulley alignment, port style, R134a oil plan, and leak test. |

Known-price preference: choose a universal `14 x 23 in` condenser before vehicle-specific Alto/Hilux/Vigo/Sportage condensers if the inside upright spacing is at least `600 mm`. It is closest to the planned `14 x 22 in` envelope and avoids adapting another vehicle's fixed brackets.

## Cooling Stack Layout

Front to rear:

```text
front grille
optional slim pusher fan
A/C condenser
10-15 mm minimum air gap
engine radiator
engine fan / shroud / engine
```

A/C refrigerant path:

```text
compressor discharge -> condenser inlet -> condenser outlet -> receiver-drier -> TXV/evaporator inlet -> evaporator outlet -> compressor suction
```

Engine coolant path remains separate:

```text
engine hot outlet -> radiator inlet -> radiator core -> radiator outlet -> engine inlet
```

## Structural Design

### Uprights

- Use `50 x 50 x 4 mm` mild-steel angle/L-section where possible, matching the existing `48-50 mm` radiator bracket face basis.
- If angle does not package cleanly, use `40 x 40 x 3-4 mm` box/SHS or formed `4 mm` plate with the same attachment logic.
- Each upright starts from a chassis/front-support rail saddle or sound welded/bolted chassis pickup and rises to the radiator top plane.
- Final height is site-fit from the actual chassis rail to the radiator top support line. Do not cut final height from photos.

### Lower Attachments

- Preferred: bolt-through saddles around the chassis/front-support rail with crush tubes/spacers where boxed metal is clamped.
- Welding to chassis/front support is allowed only after dry-fit proves no removable saddle route works and the weld zone is cleaned back to sound metal.
- Do not rely on a single side. Both uprights must carry load.

### Crossmembers And Tabs

- Fit removable upper and lower crossbars between uprights only if needed for stiffness or fan/condenser support.
- Use slotted tabs for radiator and condenser pickup points so final radiator/condenser tolerances can be absorbed without pulling either core out of plane.
- Add small gussets to upright-to-tab joints, not large closed boxes that trap rust or block tool access.

## Compressor Compatibility Gate

The photo and inventory identify the compressor as a Sanden-type compact A/C compressor already mounted to the 2H engine. The proposed condenser/drier layout is compatible in principle, but release requires:

1. Confirm clutch voltage is `12V`.
2. Confirm belt groove and pulley alignment under tension; no belt rub on radiator support, hoses, or fan shroud.
3. Identify suction and discharge ports:
   - discharge/high side is the smaller hot line to condenser, normally `#8`
   - suction/low side is the larger return line from evaporator, normally `#10`
4. Confirm port style: O-ring pad/manifold, rotolock, or adapter fittings. Buy hose fittings to match the actual compressor head, not the assumed Sanden pattern.
5. Confirm refrigerant/oil plan. If the old system was unknown or R12/mineral oil, flush or rebuild/replace as the A/C shop recommends before R134a charging.
6. Leak-test compressor shaft seal and ports before crimping final hoses.
7. Fit pressure protection through a binary/trinary switch on the drier or high-side line so the compressor cannot run with no charge or excessive head pressure.

Compatibility conclusion: the front condenser/drier package should work with the existing Sanden-type compressor if the above checks pass. If the compressor fails any check, keep the frame design and substitute a fresh Sanden-style R134a compressor with matching pulley and port head.

## Required Site Measurements Before Cutting Final Metal

| Measurement | Requirement |
| --- | --- |
| Upright spacing | Clear distance between planned inside faces of left/right uprights at radiator tab height and condenser tab height. |
| Chassis pickup | Rail width, boxed-section depth, hole condition, bolt route, and crush-tube/spacer need. |
| Radiator | Overall width/height/thickness, core width/height/thickness, mounting-ear hole centres, top/bottom neck side and OD, cap and drain position. |
| Condenser | Overall width/height/thickness, fitting side, inlet/outlet orientation, bracket-hole locations, and grille clearance. |
| Fan clearance | Engine fan/shroud to radiator rear face after uprights are tightened. |
| Front clearance | Grille/front panel to condenser/fan front face with bonnet/latch closed. |
| Hose routing | Upper/lower coolant hoses and A/C discharge/suction/liquid line sweep with engine movement. |

## No-Go Conditions

- Radiator or condenser tied through fins with zip ties, rods, wire, or hard bolts.
- Condenser hanging from radiator brackets or radiator tank.
- Radiator support relying on only one upright.
- Bracket pulls radiator closer to fan or twists a tank/core.
- Compressor hose crimping before condenser, drier, firewall, evaporator, and compressor port positions are locked.
- Drier installed early and left open to air.
