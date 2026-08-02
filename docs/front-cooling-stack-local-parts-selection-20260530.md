# Front Cooling Stack Local Parts Selection - 2026-05-30

> **SUPERSEDED — DO NOT BUY OR BUILD TO THIS LAYOUT:** The current controlled source is the [Rev F integrated cooling-pack specification](J40-integrated-cooling-pack-fabricator-specification-rev-c.md). It specifies exactly two centred front electric pushers plus the retained rear engine-driven mechanical puller, with no fourth/additional fan without a new controlled revision. Relay Rev D and MIDI Rev D share one removable protected plate fixed only to structural cooling-stack carrier metal, outside active fin/sealed airflow; the master cutoff remains battery-side. Retain this file only for historical supplier leads and donor references.

Purpose: select Pakistan-local parts for the J40 front cooling stack and A/C loop, using buyable supplier items while keeping fitment gates explicit where listings do not publish dimensions.

Fabrication package: [front_cooling_stack_rev_a](../data/manual/fabrication/front_cooling_stack_rev_a/README.md)

Buy sheet: [local_parts_selection_pakistan_20260530.csv](../data/manual/fabrication/front_cooling_stack_rev_a/local_parts_selection_pakistan_20260530.csv)

Known-price fit check: [known_price_fit_check_pakistan_20260530.csv](../data/manual/fabrication/front_cooling_stack_rev_a/known_price_fit_check_pakistan_20260530.csv)

Delivery spec: [l4tw-front-cooling-stack-delivery-spec-20260531.md](l4tw-front-cooling-stack-delivery-spec-20260531.md)

## Selected Package

| Area | Selected local route | Supplier lead | Release position |
| --- | --- | --- | --- |
| Radiator | Source a Toyota Land Cruiser 70-series diesel radiator, preferably `HZJ75` / `HZJ78` / `HZJ79` / `1HZ` | Bilal Ganj / Montgomery Road / Land Cruiser parts suppliers | Primary task is donor identity and condition, not final fitment release. New is preferred; clean used is acceptable only if undamaged and return/exchange terms are clear. |
| Condenser | Source the matching 70-series A/C condenser from the same donor family if available | Same 70-series donor supplier first; Snow Cool / Arsalan only as fallback | Primary task is matching 70-series identity and condition. Final mounting, spacing, hose routing, and cradle design remain owner/fabricator work after parts are in hand. |
| Condenser fallback | Hilux Vigo/Revo diesel, Sportage, or universal parallel-flow condenser only if the 70-series condenser is unavailable | Snow Cool / Arsalan Autos / A/C market | Fallback only. Do not choose an Alto/small-car condenser unless the front opening cannot take a larger condenser. |
| Fan | Slim `12V` pusher condenser fan assembly, `12-14 in`, complete with blade/shroud/mount feet | Cool Sun / Snow Cool / Arsalan Autos | Buy after condenser size is locked. Reject motor-only parts and through-fin mounting. |
| Receiver-drier | New R134a receiver-drier with matched O-ring ports and pressure-switch port | Snow Cool driers / Arsalan receiver driers | Buy sealed and keep capped until final assembly. Mount vertical on side upright. |
| Pressure switch | Binary or trinary switch matched to the drier/high-side port | Arsalan / Cool Sun / Snow Cool | Required before compressor clutch wiring is released. |
| Hoses | R134a barrier hoses, crimp fittings, service ports, HNBR O-rings | Arsalan / Cool Sun / Snow Cool; Sanpak as quality fallback | Crimp only after compressor, condenser, drier, firewall, and evaporator positions are locked. |
| Compressor | Reuse installed Sanden-type compressor | Existing vehicle; Arsalan/Sanpak replacement only if failed | Compatible in principle if the compressor gate passes. Reject any `24V` replacement unless the vehicle system is actually `24V`. |
| Cabin evaporator | Use the already ordered hidden/under-dash candidate if it passes mock-up; local fallback is Arsalan `Hang on 228 12V` | Arsalan Autos | Needed for the A/C loop, but not mounted on the front frame. |
| Frame steel | `50 x 50 x 4 mm` mild-steel angle, plus `3-4 mm` plate tabs/gussets | Local loha market/fabricator stock | Supports radiator, condenser, drier, and fan separately. |

## Active Task - 70-Series Donor Stack

Source a genuine Toyota Land Cruiser 70-series diesel radiator and matching A/C condenser as the preferred front-pack donor. The target donor family is `HZJ75`, `HZJ78`, `HZJ79`, or other `1HZ` diesel 70-series with factory A/C.

The market-side task is deliberately limited: confirm donor identity, part condition, price, and return/exchange terms. Final J40 fitment, second-side mount fabrication, hose routing, condenser spacing, and cradle design stay with the owner/fabricator after the parts are in hand.

Ask Amir or the shop:

```text
Find a genuine Toyota Land Cruiser 70-series diesel radiator and matching A/C condenser, preferably HZJ75/HZJ78/HZJ79/1HZ with A/C. New is preferred; clean used is acceptable only if undamaged. Send photos of the radiator, condenser, part numbers/markings if present, price, and return/exchange terms.
```

Immediate rejects:

- Not actually 70-series Land Cruiser diesel, or clearly a small-car substitute.
- Radiator leaking, rotten, crushed, badly repaired, or with damaged plastic tanks if plastic-tank type.
- Condenser ports broken, oil-stained, or fins/tubes badly smashed.
- Seller will not allow return/exchange if the part proves wrong after trial fit.

## Known-Price Fit Read

If the 70-series donor condenser cannot be sourced, the fixed-price fallback is a universal parallel-flow `14 x 23 in` unit. It is about `356 x 584 mm`, close to the design target of `14 x 22 in` / about `356 x 559 mm`, and is a cleaner fallback than buying an unrelated condenser by another vehicle's model name.

Release the `14 x 23 in` condenser only if the dry-fit confirms:

- inside clear width at condenser tabs is at least `600 mm`
- clear height is at least `370 mm`
- condenser thickness is around `20-26 mm`
- fittings exit on a side where the receiver-drier and hoses can route cleanly
- grille/front-panel depth still accepts the condenser, `10-15 mm` radiator air gap, and optional slim pusher fan

The Alto condenser options will probably fit physically, but they are the fallback because they are smaller than ideal for a J40 cabin in Pakistan heat. Hilux/Vigo or Sportage condensers are secondary fallbacks if the 70-series condenser is unavailable.

## Design Using These Parts

Front-to-rear stack:

```text
grille/front panel
slim 12V pusher fan on frame hoop
70-series or fallback condenser on forward rubber-isolated tabs
10-15 mm minimum air gap
70-series diesel radiator on rear rubber-isolated tabs
engine fan and shroud
```

A/C refrigerant path:

```text
compressor discharge -> condenser inlet -> condenser outlet -> receiver-drier -> TXV/evaporator inlet -> evaporator outlet -> compressor suction
```

The radiator and condenser both remove heat to outside air, but they are separate systems. The radiator carries engine coolant. The condenser carries A/C refrigerant. They must sit in the same airflow stack without either part carrying the other part structurally.

## Supplier Quote Instructions

Ask the donor parts supplier:

```text
Find a genuine Toyota Land Cruiser 70-series diesel radiator and matching A/C condenser, preferably HZJ75/HZJ78/HZJ79/1HZ with A/C. New is preferred; clean used is acceptable only if undamaged. Send photos of the radiator, condenser, part numbers/markings if present, price, and return/exchange terms.
```

Ask the fallback condenser supplier only if the 70-series condenser is unavailable:

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

- Do not accept a small-car substitute as a 70-series donor radiator/condenser package.
- Do not buy a fallback/universal condenser without tape photos and fitting proof.
- Do not use the radiator as a condenser bracket.
- Do not install the drier and leave it open to air.
- Do not crimp hoses before the final dry-fit.
- Do not fit a `24V` compressor or fan into a `12V` wiring system.
