# Naturally Aspirated Cooling Connector Arms + Holders — Rev P

This is the controlled fabrication handoff for the naturally aspirated cooling-pack mount. It records the owner's 15 August 2026 correction that the two radiator arms are **loose parts and are not attached to the chassis**. They may therefore be shortened or replaced on the bench and made directly to the real chassis connector interfaces.

Rev P supersedes Rev O. It retains Rev O's shortened connector arms and holder scope while replacing the former chained centring rule with direct vehicle-centreline control. Rev O already superseded the Rev N X2-adapter arrangement and the nominal 410 mm / 4 mm dimensions in `front_radiator_two_side_retention_rev_a`; none of those older values may be used for final cutting, drilling or material purchase.

## Controlled load path

`R0 → R1 lower saddles → X1 seats → X0 crossmember → shortened A0-L/A0-R arms with A1 connector ends → verified chassis connectors`

R3-U locates only. Optional R3-L stabilises only. G1/G2 carry only the G0 perimeter frame. C1, F1 and F2 are independent carriers. No tank, solder seam, fin pack, mesh or heat-exchanger core may carry mounting load.

## Critical sizing rule

Each A0 arm starts at the actual A0-D connector bearing plane and stops at the highest released functional bracket/interface. No unused tall projection remains. Final height is a datum-derived drawing value, never a photograph-scaled or inherited nominal dimension.

The actual loose arm blanks may be reworked only after identity, material, thickness/section, straightness, corrosion, old holes, cracking and heat damage are accepted. If they cannot satisfy the released connector, edge-distance and load requirements, fabricate a new matched pair from certified weldable structural steel.

## Central alignment rule

`CL0` is a fixed-datum centre record, not a visual judgement. Project the vehicle longitudinal centre plane (`VCL`) at the G0, FS and C0 mounting planes. Hold the complete repaired G0 perimeter-frame outer-envelope centre, complete mounted FS frame/rotor datum and C0 usable-fin-field lateral centreline each within `±2 mm` laterally of VCL. Separately, hold G0 within `±2 mm X/Z` of the measured usable fixed vehicle-grille aperture centre and FS within `±2 mm X/Z` of the C0 usable-fin-field centre. The fixed vehicle grille/body opening is not G0; G0 is the removable expanded-mesh stone guard. Represent all frames, tabs, guards, plugs, cable bends and service envelopes, but do not substitute those clearance envelopes for the perimeter-frame or frame/rotor centring datums. Measure every direct VCL offset independently: no tolerance stacking. If the complete assemblies cannot satisfy both the direct and local limits, revise G1/G2, C1 or F1 before release; do not approve an offset by eye.

## Photo-backed mock-up baseline

The controlled tape photographs now pre-populate the first full-size fixture: R0 body height is approximately `610 mm`, R0 cap/highest point is approximately `635 mm`, and the C0 body is approximately `540 × 465 mm`. These three readings are **LOCKED FOR MOCK-UP**, not final fabrication dimensions. The photographed R0 horizontal span of approximately `635 mm`, FL ring of approximately `450–480 mm`, and FS ring/frame of approximately `240–255 mm` / up to about `280 mm` are **PROVISIONAL**. Depths, holes, lower-saddle centres, connectors, brackets and vehicle fit remain **HOLD**. The signed square direct measurements in `measurement_basis.csv` supersede any photo reading for final fabrication.

## Holder scope

- `G1-L/R`: lower rubber-faced grille/stone-guard cradles for the sound G0 perimeter frame.
- `G2-L/R`: removable upper/side grille/stone-guard keepers with positive accessible retention.
- `R0-E`: radiator-shop repair/reproduction of released sound radiator-side ears or tabs.
- `R3-U-L/R`: short sleeved-EPDM upper radiator keepers; locator/restraint only.
- `R3-L-L/R`: optional lower-side stabilisers; no vertical load and no copy of the historical added leg.
- `F2`: independent rear fan/shroud carrier and seal land; no tank/core load.

## Handoff sequence

1. Load the photo-backed mock-up baselines already recorded in `measurement_basis.csv`, then replace/complete the final records from square direct measurement of the actual chassis connectors, guard, R0 radiator and retained components.
2. Make rigid A0-D-L/R, B0, S0, CL0, G0-H and R0-H templates from fixed vehicle datums, projecting VCL directly at the G0, FS and C0 planes.
3. Inspect the two loose arm blanks and record retain/rework/replace decisions.
4. Produce a competent-person structural calculation and drawing for X0/X1/A0/A1, connector bearing, welds, fasteners, torque and proof fixture.
5. Bench-cut/jig the shortened mirror-handed A0 assemblies; never trim an installed structural member.
6. Design G1/G2 from G0-H/CL0 and R3/R0-E from R0-H. Design F1 from CL0 and the complete FS/C0 maps. G1/G2 and F1 must each satisfy their direct VCL limit as well as their local aperture/C0 limit. Every holder must have an assigned load/function and service path.
7. Complete an opaque bare-metal 1:1 dry fit with actual rubbers, hardware, hoses, wiring and service tools.
8. After structural release, apply a **total** static proof load of `2 × MR`, distributed between the two S0 saddle centres in the released loaded-radiator distribution, for 10 minutes without local point-loading.
9. Complete `inspection_checklist.csv`, coat, assemble and commission under the Rev P guide.

## Files

- `fabricator_cut_list.csv` — complete make/buy mounting schedule; all final dimensions held.
- `measurement_basis.csv` — mandatory measurement and template record.
- `inspection_checklist.csv` — fabrication, proof, finish and installation gates.

The controlling narrative is `docs/J40-naturally-aspirated-cooling-pack-restoration-guide-rev-p-20260816.md`.
