# Naturally Aspirated Cooling Connector Arms + Holders — Rev O

This is the controlled fabrication handoff for the naturally aspirated cooling-pack mount. It records the owner's 15 August 2026 correction that the two radiator arms are **loose parts and are not attached to the chassis**. They may therefore be shortened or replaced on the bench and made directly to the real chassis connector interfaces.

Rev O supersedes the Rev N X2-adapter arrangement and the nominal 410 mm / 4 mm dimensions in `front_radiator_two_side_retention_rev_a`. Those older values must not be used for final cutting, drilling or material purchase.

## Controlled load path

`R0 → R1 lower saddles → X1 seats → X0 crossmember → shortened A0-L/A0-R arms with A1 connector ends → verified chassis connectors`

R3-U locates only. Optional R3-L stabilises only. G1/G2 carry only the G0 perimeter frame. C1, F1 and F2 are independent carriers. No tank, solder seam, fin pack, mesh or heat-exchanger core may carry mounting load.

## Critical sizing rule

Each A0 arm starts at the actual A0-D connector bearing plane and stops at the highest released functional bracket/interface. No unused tall projection remains. Final height is a datum-derived drawing value, never a photograph-scaled or inherited nominal dimension.

The actual loose arm blanks may be reworked only after identity, material, thickness/section, straightness, corrosion, old holes, cracking and heat damage are accepted. If they cannot satisfy the released connector, edge-distance and load requirements, fabricate a new matched pair from certified weldable structural steel.

## Central alignment rule

`CL0` is a fixed-datum centre record, not a visual judgement. Hold the repaired G0 perimeter centre within 2 mm of the usable grille-aperture centre in both axes. Hold the C0 usable-fin-field lateral centreline within 2 mm of the vehicle longitudinal centre plane. Hold the FS motor/rotor axis within 2 mm of the C0 usable-fin-field centre laterally and vertically. The complete guard and complete fan frame, tabs, guard, plug, cable bend and service envelope must fit at those coordinates. If they do not, revise the carriers before release; do not approve an offset by eye.

## Holder scope

- `G1-L/R`: lower rubber-faced grille/stone-guard cradles for the sound G0 perimeter frame.
- `G2-L/R`: removable upper/side grille/stone-guard keepers with positive accessible retention.
- `R0-E`: radiator-shop repair/reproduction of released sound radiator-side ears or tabs.
- `R3-U-L/R`: short sleeved-EPDM upper radiator keepers; locator/restraint only.
- `R3-L-L/R`: optional lower-side stabilisers; no vertical load and no copy of the historical added leg.
- `F2`: independent rear fan/shroud carrier and seal land; no tank/core load.

## Handoff sequence

1. Complete `measurement_basis.csv` from the actual chassis connectors, guard, R0 radiator and retained components.
2. Make rigid A0-D-L/R, B0, S0, CL0, G0-H and R0-H templates from fixed vehicle datums.
3. Inspect the two loose arm blanks and record retain/rework/replace decisions.
4. Produce a competent-person structural calculation and drawing for X0/X1/A0/A1, connector bearing, welds, fasteners, torque and proof fixture.
5. Bench-cut/jig the shortened mirror-handed A0 assemblies; never trim an installed structural member.
6. Design G1/G2 from G0-H/CL0 and R3/R0-E from R0-H. Design F1 from CL0 and the complete FS/C0 maps. Every holder must have an assigned load/function and service path.
7. Complete an opaque bare-metal 1:1 dry fit with actual rubbers, hardware, hoses, wiring and service tools.
8. After structural release, apply a **total** static proof load of `2 × MR`, distributed between the two S0 saddle centres in the released loaded-radiator distribution, for 10 minutes without local point-loading.
9. Complete `inspection_checklist.csv`, coat, assemble and commission under the Rev O guide.

## Files

- `fabricator_cut_list.csv` — complete make/buy mounting schedule; all final dimensions held.
- `measurement_basis.csv` — mandatory measurement and template record.
- `inspection_checklist.csv` — fabrication, proof, finish and installation gates.

The controlling narrative is `docs/J40-naturally-aspirated-cooling-pack-restoration-guide-rev-o-20260815.md`.
