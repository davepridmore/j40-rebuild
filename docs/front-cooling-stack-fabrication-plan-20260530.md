# Front Cooling Stack Fabrication Plan - 2026-05-30

> **Superseded cooling layout:** For current manufacture, use the [Rev E integrated cooling-pack specification](J40-integrated-cooling-pack-fabricator-specification-rev-c.md). It replaces this historical plan's lower-front intercooler, optional single pusher and side-mounted drier/electrical direction with a measured-fit main pack, two central matched Toyota/Denso candidate pushers, rear/upper service parts and a compact fore-aft side charge-air pack. Retain this file only for the original support-frame history and electrical-enclosure references.

Purpose: define the fabrication direction for replacing the weak one-sided radiator support with a full front cooling-stack frame that can carry the engine radiator, A/C condenser and turbo intercooler cleanly.

Current integrated fabricator handoff: [j40-integrated-cooling-pack-fabricator-handoff-20260717.md](j40-integrated-cooling-pack-fabricator-handoff-20260717.md). It retains the decided existing upright plus one welded identical mirrored upright and adds separately removable cooling components using small adapter tabs.

Fabrication package: [data/manual/fabrication/front_cooling_stack_rev_a](../data/manual/fabrication/front_cooling_stack_rev_a/README.md)

Pakistan-local parts selection: [front-cooling-stack-local-parts-selection-20260530.md](front-cooling-stack-local-parts-selection-20260530.md)

L4TW delivery spec: [l4tw-front-cooling-stack-delivery-spec-20260531.md](l4tw-front-cooling-stack-delivery-spec-20260531.md)

## Decision

Use the existing full-height chassis/front-support upright and weld an identical mirrored upright on the left side. The radiator, A/C condenser, lower-front turbo intercooler, optional upper-band pusher fan, receiver-drier, and removable relay/fuse plate mount to those uprights as separate serviceable parts.

The radiator must not support the condenser, intercooler, or electrical plate. The condenser must not support the fan or intercooler. Nothing should be tied through any core or fins, and no electrical bracket may load or be drilled into a radiator tank, neck, seam, or isolated radiator mount.

## Component Direction

| Component | Direction |
| --- | --- |
| Radiator | Start with HJ47 / 2H radiator pattern, Toyota reference `16400-68030`, or build a modern copper/brass/aluminium unit to that sample envelope. |
| Condenser | Start with Snow Cool `MM CONDENSOR` as the local quote item, keeping a `14 x 22 in` parallel-flow R134a envelope target. Use Arsalan `Condenser Kia Sportage new model` as the larger alternate if tape photos prove it fits. |
| Drier | New R134a receiver-drier with switch port, mounted vertical on the cooling-stack side upright. Buy from Snow Cool/Arsalan only after condenser and fitting sizes are known. |
| Fan | Optional slim `12V` pusher fan assembly, carried by the frame/fan hoop, not fin-mounted. |
| Relay box | Reuse Relay Rev D on its `360 x 245 x 3 mm` base and `300 x 197 x 3 mm` insulator, bolted to a removable plate on the structural cooling-stack upright/accessory rail with its cover serviceable. |
| MIDI fuse enclosure | Reuse MIDI Rev D (`210 x 165 x 65 mm`) on the same structural accessory plate or an adjacent removable plate, protected from splash and heat with the hinged lid, grommets, and cable bends serviceable. |
| Compressor | Reuse the installed Sanden-type compressor only after compatibility checks pass; replace locally with a `12V` Sanden-style V-pulley unit only if it fails the gate. |

## Compressor Compatibility Read

The installed compressor in the photos and parts ledger is treated as a Sanden-type compact compressor on the 2H bracket. It should be compatible with a universal parallel-flow condenser and receiver-drier if the A/C shop confirms:

- `12V` clutch
- pulley groove and belt alignment under tension
- high-side discharge fitting from compressor to condenser, typically smaller `#8`
- low-side suction fitting from evaporator back to compressor, typically larger `#10`
- actual compressor head fitting style and adapters
- R134a-compatible oil/refrigerant plan
- no shaft-seal or port leaks
- binary/trinary pressure switch protection before compressor clutch operation

If those checks fail, keep the same front cooling-stack frame and replace the compressor with a fresh Sanden-style R134a unit that matches the 2H bracket, pulley, and hose-head layout.

## Fabrication Sequence

1. Mock the new HJ47/2H radiator or sample radiator between the planned uprights.
2. Set the radiator plane by fan clearance and hose sweep, not by the old bad support leg.
3. Set the condenser in front of the radiator with a `10-15 mm` minimum air gap.
4. Check grille/front-panel depth with the optional pusher fan in place.
5. Mark radiator tabs from the real radiator with rubber washers/pads installed.
6. Mark condenser tabs from the selected condenser; do not use through-fin mounting rods.
7. Mount the receiver-drier vertical on the side upright near the condenser outlet.
8. Confirm compressor discharge and suction fitting routes before hose crimping.
9. Template the relay and MIDI enclosures on a removable structural-carrier plate; prove core airflow, fan/shroud, hose, cap, drain, bonnet, grille, lid/cover, cable-bend, and radiator-removal clearances.
10. Mark cable supports, protected pass-throughs, earth point, and service-disconnect boundary before coating.
11. Deburr, corrosion-protect, and final-fit the frame only after all dry-fit checks pass.

## Hard Holds

- No final hose crimping until condenser, drier, firewall/bulkhead, evaporator, and compressor positions are locked.
- No drier opened to air until final assembly/charge preparation.
- No primer/Raptor over the front support area until cooling-stack holes, welds, and brackets are validated.
- No random radiator buy unless necks, cap, drain, bracket spacing, and fan clearance match the vehicle.
- No electrical-plate holes until the real Relay Rev D and MIDI Rev D parts, cable exits, airflow aperture, heat/splash exposure, and radiator service path have been dry-fitted.
- No relay/fuse mounting directly to the radiator core, fins, tanks, necks, seams, or rubber-isolated radiator mounts.
