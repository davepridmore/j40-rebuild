# J40 As-Fitted Route Pakistan Purchase BOM - 2026-05-31

Control CSV: `data/manual/j40_as_fitted_route_pakistan_purchase_bom_20260531.csv`

This is the Pakistan buy sheet for the routes now shown in the 3D model. It converts the as-fitted route scope into runner/shop purchase language.

## Rule

Buy exact parts by spec and sample, not by generic vehicle name.

The model has route IDs; the BOM has buy IDs. A route is not physically released until the relevant buy IDs are sample-matched, dry-fitted, and checked for clearance.

## Priority Buys

P0 items to resolve first:

- `PK-RTE-RAD-001`: HJ47/2H radiator built or recored from the old sample.
- `PK-RTE-STEEL-001`: `50 x 50 x 4 mm` mild-steel angle plus `3-4 mm` plate for the two-side cooling-stack frame and route supports.
- `PK-RTE-COND-001`: universal parallel-flow condenser, `14 x 23 in` overall, `#6/#8` male O-ring fittings.
- `PK-RTE-EVAP-001`: confirm the already purchased under-dash unit; fallback is a local `228` 12V hang-on unit only if the current unit fails.
- `PK-RTE-HOSE-COOL-001`: EPDM coolant and heater hose stock.
- `PK-RTE-FUEL-HOSE-001`: diesel fuel feed, return, leak-off hose, and rolled-edge clamps.
- `PK-RTE-BRAKE-PIPE-001`: `4.75 mm / 3/16 in` brake-rated hard-line tube and fittings.
- `PK-RTE-BRAKE-HOSE-001`: complete crimped brake hose assemblies to old samples.
- `PK-RTE-PCLIP-001`: rubber-lined P-clip assortment for every cable, hose, and line route.

## A/C Buy Set

The local A/C set is:

- universal parallel-flow condenser, `14 x 23 in`, `#6/#8` O-ring ports
- slim `12V` pusher fan, `12-14 in`, with shroud and mount feet
- sealed R134a receiver-drier with `3/8` O-ring ports and pressure-switch port
- binary or trinary pressure switch with known thread and logic
- R134a barrier hose set: `#6` liquid hose `3 m`, `#8` discharge hose `1.5 m`, `#10` suction hose `2 m`
- O-ring crimp fittings, ferrules, service ports, HNBR O-rings, and firewall pass-through grommets or bulkheads
- Sanden SP-10 or ND8 oil only after the installed compressor passes its gate

Crimp nothing until the compressor, condenser, drier, firewall, and evaporator positions are physically locked.

## Safety-Critical Holds

Brake items are exact-spec only:

- hard line must be automotive brake-rated `4.75 mm / 3/16 in` steel or CuNi tube
- flex hoses must be complete crimped brake hose assemblies with DOT or SAE J1401-equivalent marking or supplier proof
- flare type and fitting thread are copied from the old sample; `M10x1` is only a candidate until confirmed
- no compression fittings, bare copper tube, fuel hose, hydraulic hose substitution, or seller-led fit decision

Electrical heavy cable is stock-check-first:

- use received cable and sleeve inventory before buying more
- if short, top up with fine-strand copper cable, not CCA: red `25 mm2 x 3 m`, black `25 mm2 x 2 m`, red `16 mm2 x 3 m`, and red/black `10 mm2 x 3 m`
- buy matching tinned lugs, adhesive heatshrink, and rubber-lined supports

## Sources Checked

- Master Radiators: Pakistani radiator manufacturer lead for copper/brass or aluminium radiator work.
- KorTech: Pakistani radiator manufacturer with custom radiator capability.
- Snow Cool: Pakistan automotive A/C supplier with condensers, evaporators, hang-on units, and driers listed.
- Arsalan Autos: Lahore A/C parts supplier listing Sanden compressors, `Hang on 228 12v`, condensers, O-rings, oil, and R134a gas.
- Longman Mills: Lahore rubber-products supplier for hose pipes and custom rubber parts.
- National Rubber Co: Pakistan EPDM radiator hose supplier with SAE J20 R4 / OEM-spec language.
- SNA Industries: Pakistan supplier lead for steel brake pipes and brake hoses.

## Runner Instruction

For each line, the runner should return:

- shop name and phone
- item photo
- tape/caliper photo for size-sensitive parts
- label/marking photo
- price and warranty/return condition
- old-sample comparison photo where required

No payment on sample-gated lines until the proof columns in the CSV are satisfied.
