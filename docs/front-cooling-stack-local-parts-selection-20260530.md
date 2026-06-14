# Front Cooling Stack Local Parts Selection - 2026-05-30

Purpose: select Pakistan-local parts for the J40 front cooling stack and A/C loop, using buyable supplier items while keeping fitment gates explicit where listings do not publish dimensions.

Fabrication package: [front_cooling_stack_rev_a](../data/manual/fabrication/front_cooling_stack_rev_a/README.md)

Buy sheet: [local_parts_selection_pakistan_20260530.csv](../data/manual/fabrication/front_cooling_stack_rev_a/local_parts_selection_pakistan_20260530.csv)

Known-price fit check: [known_price_fit_check_pakistan_20260530.csv](../data/manual/fabrication/front_cooling_stack_rev_a/known_price_fit_check_pakistan_20260530.csv)

Delivery spec: [l4tw-front-cooling-stack-delivery-spec-20260531.md](l4tw-front-cooling-stack-delivery-spec-20260531.md)

## Selected Package

| Area | Selected local route | Supplier lead | Release position |
| --- | --- | --- | --- |
| Radiator | Build or recore an HJ47/2H-pattern radiator from the old sample | Master Radiators first, KorTech second | Buy only after old sample dimensions, corrected mount tabs, hose necks, cap, drain, fan clearance, and pressure test are confirmed. |
| Condenser | Start with Snow Cool `MM CONDENSOR`; use Arsalan `Condenser Kia Sportage new model` as the large alternate | Snow Cool / Arsalan Autos | Final condenser is not released until the seller sends tape photos for width, height, depth, fitting side, port size, and bracket positions. |
| Small condenser fallback | Alto Pakistani 660cc condenser | Snow Cool / Arsalan Autos | Space-saving fallback only. Do not choose it if a larger parallel-flow condenser fits. |
| Fan | Slim `12V` pusher condenser fan assembly, `12-14 in`, complete with blade/shroud/mount feet | Cool Sun / Snow Cool / Arsalan Autos | Buy after condenser size is locked. Reject motor-only parts and through-fin mounting. |
| Receiver-drier | New R134a receiver-drier with matched O-ring ports and pressure-switch port | Snow Cool driers / Arsalan receiver driers | Buy sealed and keep capped until final assembly. Mount vertical on side upright. |
| Pressure switch | Binary or trinary switch matched to the drier/high-side port | Arsalan / Cool Sun / Snow Cool | Required before compressor clutch wiring is released. |
| Hoses | R134a barrier hoses, crimp fittings, service ports, HNBR O-rings | Arsalan / Cool Sun / Snow Cool; Sanpak as quality fallback | Crimp only after compressor, condenser, drier, firewall, and evaporator positions are locked. |
| Compressor | Reuse installed Sanden-type compressor | Existing vehicle; Arsalan/Sanpak replacement only if failed | Compatible in principle if the compressor gate passes. Reject any `24V` replacement unless the vehicle system is actually `24V`. |
| Cabin evaporator | Use the already ordered hidden/under-dash candidate if it passes mock-up; local fallback is Arsalan `Hang on 228 12V` | Arsalan Autos | Needed for the A/C loop, but not mounted on the front frame. |
| Frame steel | `50 x 50 x 4 mm` mild-steel angle, plus `3-4 mm` plate tabs/gussets | Local loha market/fabricator stock | Supports radiator, condenser, drier, and fan separately. |

## Known-Price Fit Read

If a fixed-price purchase is preferred, the best condenser style is a universal parallel-flow `14 x 23 in` unit. It is about `356 x 584 mm`, close to the design target of `14 x 22 in` / about `356 x 559 mm`, and is a cleaner fit than buying a condenser by another vehicle's model name.

Release the `14 x 23 in` condenser only if the dry-fit confirms:

- inside clear width at condenser tabs is at least `600 mm`
- clear height is at least `370 mm`
- condenser thickness is around `20-26 mm`
- fittings exit on a side where the receiver-drier and hoses can route cleanly
- grille/front-panel depth still accepts the condenser, `10-15 mm` radiator air gap, and optional slim pusher fan

The Alto condenser options will probably fit physically, but they are the fallback because they are smaller than ideal for a J40 cabin in Pakistan heat. Hilux/Vigo or Sportage condensers are not preferred unless the seller sends tape photos proving the exact size and fitting side; vehicle-specific tabs and pipe exits can easily make them harder to package than a universal condenser.

## Design Using These Parts

Front-to-rear stack:

```text
grille/front panel
slim 12V pusher fan on frame hoop
Snow Cool/Arsalan condenser on forward rubber-isolated tabs
10-15 mm minimum air gap
Master/KorTech 2H radiator on rear rubber-isolated tabs
engine fan and shroud
```

A/C refrigerant path:

```text
compressor discharge -> condenser inlet -> condenser outlet -> receiver-drier -> TXV/evaporator inlet -> evaporator outlet -> compressor suction
```

The radiator and condenser both remove heat to outside air, but they are separate systems. The radiator carries engine coolant. The condenser carries A/C refrigerant. They must sit in the same airflow stack without either part carrying the other part structurally.

## Supplier Quote Instructions

Ask the radiator supplier:

```text
Please quote a Toyota Land Cruiser J40/HJ47 2H radiator built from my old sample. I need corrected left and right mount tabs, same hose neck side/OD, same cap/overflow/drain positions, pressure/flow test, and no copy of the bad one-sided support leg.
```

Ask the condenser supplier:

```text
Please send tape photos for the condenser before payment: overall width, height, depth, fitting side, inlet/outlet size/thread, bracket locations, and whether it is parallel-flow/R134a suitable. It must mount by tabs, not through fins.
```

Ask the A/C hose shop:

```text
Please make R134a barrier hoses only after the compressor, condenser, drier, evaporator, and firewall positions are fixed. Match fittings to the actual ports, add service ports and HNBR O-rings, and nitrogen leak-check after crimping.
```

## Compressor Compatibility

The installed compressor can stay if these checks pass:

- `12V` clutch
- pulley groove and belt alignment under tension
- smaller high-side discharge port routed to condenser
- larger low-side suction port routed from evaporator
- actual port style identified before buying hose fittings
- R134a oil/refrigerant plan confirmed
- shaft seal and port leak test passed
- binary/trinary pressure switch installed before clutch operation

If it fails, replace with a Sanden-style `12V` V-pulley compressor that matches the existing 2H bracket and hose-head layout.

## Hard Holds

- Do not buy a radiator by model name only.
- Do not buy a condenser without tape photos and fitting proof.
- Do not use the radiator as a condenser bracket.
- Do not install the drier and leave it open to air.
- Do not crimp hoses before the final dry-fit.
- Do not fit a `24V` compressor or fan into a `12V` wiring system.
