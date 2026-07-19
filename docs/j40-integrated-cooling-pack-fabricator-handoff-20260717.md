# J40 Integrated Cooling Pack — Fabricator Handoff — Rev B

## Release status

This document releases a full-size mock-up and quotation. It does **not** release final core manufacture until the seven `M` dimensions in the measurement sheet have been recorded on the vehicle.

The structural decision is already made: retain the existing formed vertical radiator support and weld an identical vertical support on the **left side**. Do not redesign those supports. If component mounting faces do not align, use small removable adapter tabs between the supports and the cooling components.

Dimension schedule: [integrated_cooling_pack_dimensions_rev_b.csv](../data/manual/fabrication/front_cooling_stack_rev_a/integrated_cooling_pack_dimensions_rev_b.csv)

Fabrication elevation: [integrated_cooling_pack_front_elevation_rev_b.svg](../data/manual/fabrication/front_cooling_stack_rev_a/integrated_cooling_pack_front_elevation_rev_b.svg)

## Required assembly

Fabricate one modular cooling package within the opening between the two structural uprights. The three heat exchangers remain separate pressure circuits and must be individually removable:

1. rear engine-coolant radiator;
2. middle R134a condenser;
3. lower-front charge-air intercooler.

The fabricator may manufacture the radiator, intercooler, tanks, shrouds, side rails and adapters. Use a standard replaceable parallel-flow condenser unless the A/C specialist can document the pressure rating, refrigerant compatibility and replacement specification of a custom condenser.

## Fixed design target

All dimensions are millimetres.

| Item | Target manufacture size | Limit / note |
| --- | ---: | --- |
| Radiator core | `530 W × 435 H × 64 D` | Copper/brass high-efficiency four-row HJ47/2H pattern. `540 W × 435 H × 60 D` allowed only if `M1 ≥ 550`. |
| Radiator overall width | `≤ M1 - 10` | Maintain at least `5` clearance each side. Mounting ears may enter the upright face area. |
| Coolant necks | `38 OD` | Exact side, angle and centre positions transferred from old radiator/engine hose mock-up. |
| Condenser body | `559 W × 356 H × 21 D` nominal | Standard `14 × 22 in` parallel-flow R134a unit; absolute body maximum `600 W × 370 H × 25 D`. |
| Intercooler core | `500 W × 180 H × 60 D` | Custom bar-and-plate aluminium; `2.25 in / 57 OD` outlets; maximum core `520 W × 200 H × 65 D`. |
| Intercooler overall width | `≤ M1 - 10` | End-tank/outlet envelope must clear uprights, steering and bodywork. Angle outlets rearward/upward only after charge-pipe route is marked. |
| Radiator–condenser clear gap | `15` | `10` absolute minimum at the closest point. |
| Condenser–intercooler clear gap | `10` | Intercooler sits forward of the condenser over the lower band. |
| Rear fan-tip clearance | `≥ 20` static | Final requirement is `M5`; check through full engine movement. Prefer `25–30`. |
| Lower intercooler edge | `≥ 25` above lowest protected frame line | Must not become the first impact point and must retain drain/service access. |
| Component edge clearance | `5` each side minimum | No tank, manifold or fitting may rub an upright. |

The `500 × 180 × 60` intercooler is deliberately modest for the conservative `5–7 psi` 2H turbo plan. Do not substitute a thick, full-height universal intercooler merely because it has a higher advertised horsepower rating.

## Front-to-rear arrangement

```text
FRONT / GRILLE
  upper band: removable slim A/C pusher fan
  lower band: 500 × 180 × 60 intercooler
  10 clear
  559 × 356 × 21 A/C condenser
  15 clear
  530 × 435 × 64 engine radiator
  rear shroud and engine-driven fan
ENGINE
```

The intercooler covers only the lower `180` mm band. The condenser pusher fan is mounted principally in the upper band. Do not mount a fan through any core using plastic rods.

The nominal heat-exchanger stack excluding the front fan is `170 mm`: `60 intercooler + 10 gap + 21 condenser + 15 gap + 64 radiator`. Allow `5–10` additional tolerance for seams, brackets and imperfect planes. `M4` must therefore be at least `180 mm` without the pusher fan. If a fan overlaps the intercooler in depth, add its measured depth; if it remains completely above the intercooler, the lower-band depth remains `180 mm`.

## Structural and mounting detail

- Existing and duplicated uprights: measured `410` high, `48` main mounting face, `4` mild steel, `58` top return, `70` chassis bridge and `80` outer saddle leg.
- Duplicate the existing upright as a handed/mirrored part on the left side. The vehicle owner has selected welding for this second upright; clean to sound metal, dry-fit the entire pack first, use short balanced welds, verify the opening after cooling and corrosion-protect both sides.
- Do not weld radiator, condenser, intercooler or fan mounts permanently to their tanks or cores.
- Use two removable vertical side rails, `30 × 3` mild-steel flat or `25 × 25 × 3` angle, between the structural uprights. Cut their final length to `M2 - 10` and retain `5` top/bottom clearance.
- Attach each side rail to each structural upright with two M8 class 8.8 bolts: four bolts total. Use `9 × 20` vertical slots in the **adapter tabs**, not in the structural uprights.
- Adapter tabs: four pieces, `50 W × 70 H × 4`, with one `9 × 20` vertical slot. Bend/joggle only the measured offset `M7`; maximum unsupported offset `20`. For `M7 > 20`, use a boxed spacer with two shear faces, not a long flat tab.
- Radiator weight sits on two lower `3–4` mm saddles with `5` mm EPDM pads. Upper tabs only restrain it. Use M8 bolts with large washers and rubber bushes; do not pull the core out of square.
- Condenser mounts from four separate `3` mm tabs with rubber washers and M6 bolts.
- Intercooler mounts from four separate `4` mm tabs with M8 bolts and rubber isolators. Allow `2–3` mm thermal movement at one upper mounting point using a horizontal slot.
- Provide removable upper and lower crossrails only where the actual components need them. Use `25 × 25 × 3` angle; bolt them between side rails. Do not place a rail across the radiator core face.
- Receiver-drier mounts vertically outside the main airflow on the condenser-outlet side using a rubber-lined removable clamp.

## Tanks, fittings and serviceability

### Radiator

- Copy the old radiator’s upper/lower neck side and angles unless the installed hose mock-up proves a cleaner route.
- Include filler neck/cap, overflow barb and accessible drain.
- Pressure- and flow-test before painting. Record the test pressure used.
- Provide a close-fitting rear fan shroud. Target fan insertion into the shroud opening is `35–50%` of blade depth after the engine/body are installed; site measurement controls.

### Intercooler

- Aluminium bar-and-plate core; TIG-welded formed end tanks with internal transitions, not abrupt square boxes.
- Two `57 mm OD` outlets, bead-rolled or welded retaining beads. No plain un-beaded pipe ends.
- End-tank/outlet orientation remains a hold until turbo hot-side and intake cold-side routes are marked. Prefer one outlet each side if that avoids tight 180-degree piping; do not assume both on one side.
- Pressure-test at `20 psi / 1.38 bar` with the core submerged or leak-detection solution applied. This test pressure is comfortably above the initial `5–7 psi` operating target without pretending to certify an unknown core beyond its maker’s rating.

### Condenser and A/C fan

- Condenser target has same-side #8 inlet and #6 outlet O-ring fittings, with side manifolds vertical. Confirm actual threads before hose crimping.
- Start with one slim `12 in` pusher fan in the upper band. Maximum target envelope `330 diameter × 65 deep`; actual fan current and airflow must be recorded before relay/fuse selection.
- Use a removable fan hoop or crossrail. Confirm pusher direction with a paper-strip airflow test before refrigerant charging.

## Mandatory vehicle measurements

Record these after the second upright is tacked in place, with grille/front panel, bonnet latch, engine fan and body position represented:

| ID | Measurement | How to measure | Release criterion |
| --- | --- | --- | --- |
| `M1` | Minimum clear inside width between uprights | Top, middle and bottom; record all three and use the smallest | `≥ 540` for 530 core; `≥ 550` for 540 core; `≥ 569` for unmodified 559 condenser plus side clearance unless its brackets sit forward of the faces. |
| `M2` | Clear vertical opening | Lowest support/pad plane to bonnet/latch obstruction | Must accept radiator overall height plus `10` clearance; core height alone is not sufficient. |
| `M3` | Grille to radiator front-face plane | At upper fan band and lower intercooler band | Lower band `≥ 180`; upper band must accept condenser/gaps plus selected fan depth. |
| `M4` | Available lower-band stack depth | Grille/guard to radiator rear-component datum | `≥ 180` plus `5–10` fabrication tolerance. |
| `M5` | Radiator rear face to engine fan tips | Check closest blade through a full rotation | `≥ 20` static; `25–30` preferred. |
| `M6` | Lowest safe intercooler edge | Relative to front crossmember/bumper protection line | `≥ 25` above protected lowest line. |
| `M7` | Upright face to component side-rail offset | Each of four corners | `0–20` for simple adapter tab; box the spacer if greater. |

Also record coolant-neck centres/angles, condenser port side, turbo compressor outlet position, intake-plenum inlet position, bonnet closure and the service-removal path.

## Decision rules if the target does not fit

1. Protect radiator size and rear fan clearance first.
2. Reduce intercooler thickness from `60` to `50` only with a reputable high-efficiency core; do not reduce below `450 × 160 × 50` without a charge-temperature/pressure-drop review.
3. Move or split the pusher fan before reducing radiator area.
4. Use a `14 × 20 in` condenser only after the A/C specialist accepts the reduced capacity for Lahore traffic conditions.
5. If `M4 < 170`, stop: the proposed air-to-air triple stack does not fit. Review a remote/water-to-air charge cooler rather than crushing gaps or placing components against each other.

## Fabricator delivery evidence

- Completed measurement sheet with `M1–M7` and photographs showing the tape/ruler.
- Front and side photographs of the full cardboard/plywood mock-up.
- Tack-fit photographs with grille, bonnet/latch and fan represented.
- Dimensioned as-built sketch showing all core bodies, tank envelopes, ports, mounting holes and adapter offsets.
- Radiator pressure/flow result, intercooler `20 psi` leak-test result and condenser/A/C-shop pressure-test evidence.
- Bare-metal pre-paint photographs of every bracket and weld.
- Installed clearance photographs and warm idle/A/C-on validation results.
