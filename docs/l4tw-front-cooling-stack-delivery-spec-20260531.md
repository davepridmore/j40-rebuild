# L4TW Front Cooling Stack Delivery Specification - 2026-05-31

Purpose: define the specific delivery requirements for the J40/2H front cooling stack and A/C front pack. This is the build target for the fabricator and A/C shop; price is secondary to fit, cooling performance, serviceability, and evidence.

Fabrication package: [front_cooling_stack_rev_a](../data/manual/fabrication/front_cooling_stack_rev_a/README.md)

Acceptance matrix: [delivery_spec_l4tw_20260531.csv](../data/manual/fabrication/front_cooling_stack_rev_a/delivery_spec_l4tw_20260531.csv)

## Delivered System

The delivered system must include:

- correctly fitted 2H/J40 engine radiator
- two-sided structural front cooling-stack frame
- R134a parallel-flow A/C condenser
- optional-but-packaged slim `12V` pusher fan provision
- new receiver-drier and pressure protection switch
- purchased slimline/under-dash cabin evaporator accepted into the full A/C loop
- verified existing Sanden-type compressor or approved replacement
- R134a barrier hoses and service ports
- final pressure, leak, airflow, electrical, and cooling validation

The radiator, condenser, fan, and drier must be separately mounted and serviceable. No part may be hung from radiator or condenser fins/tubes/tanks.

## Build Specification

| Area | Specific requirement |
| --- | --- |
| Radiator | Use the old radiator as the master pattern. Build/recore to the J40/HJ47/2H envelope, preserving hose neck side/OD, cap, overflow, drain, fan/shroud clearance, and corrected left/right mounting. Candidate core basis is about `435 x 530-540 x 60-64 mm`, but the old sample controls. |
| Radiator support | Radiator must sit on lower rubber-isolated pads/saddles and be retained on both sides. Do not copy the previous bad one-sided support leg. |
| Main frame | Build two full-height uprights from chassis/front support to radiator top plane. Preferred material is `50 x 50 x 4 mm` mild-steel angle. Accept `40 x 40 x 3-4 mm` box/formed plate only if it packages better. |
| Frame attachment | Prefer bolt-through saddles with crush tubes/spacers where boxed metal is clamped. Welding is allowed only to cleaned, sound metal after dry-fit proves the bolted route is not practical. |
| Condenser | Use an R134a parallel-flow condenser. Target envelope is `14 x 22 in`; known-price fit candidate is `14 x 23 in` / about `356 x 584 x 20-26 mm`. Release the `14 x 23 in` unit only if the clear mounting width is at least `600 mm` and clear height is at least `370 mm`. |
| Condenser mounting | Mount condenser ahead of radiator on its own rubber-isolated tabs, with at least `10-15 mm` air gap to the radiator. No through-fin rods, zip ties, wire, or radiator-mounted condenser brackets. |
| Pusher fan | Package for a slim `12V` pusher fan, `12-14 in`, complete with blade/shroud/mount feet. Mount fan to frame hoop/crossbar only. Current draw and airflow direction must be known before wiring. |
| Drier | Install a new sealed R134a receiver-drier, vertical, near condenser outlet. Match ports to the selected condenser/liquid line. Keep capped until final assembly. |
| Pressure protection | Install binary or trinary pressure protection before compressor clutch operation. If trinary is used, condenser fan request can be controlled through it. |
| Cabin evaporator interface | The purchased slimline/under-dash A/C unit is accepted only after physical measurement, under-dash mock-up, drain routing, airflow test, fitting/TXV identification, and leak test. It must not force a bulky visible hang-on installation. |
| Compressor | Reuse installed Sanden-type compressor only if it passes: `12V` clutch, pulley alignment, suction/discharge port identification, fitting compatibility, R134a oil plan, and leak test. Replacement must be `12V`, V-pulley, bracket-compatible, and port-compatible. |
| Hoses | Use R134a barrier hose with matched crimp fittings, service ports, and HNBR O-rings. Crimp only after radiator, condenser, drier, evaporator, firewall/bulkhead, and compressor positions are fixed. Required circuit is compressor discharge to condenser, condenser to drier, drier to TXV/evaporator inlet, evaporator outlet to compressor suction. |
| Electrical | Fan, compressor clutch, and blower feeds must be relay/fuse protected and sized from measured current draw. Pressure switch logic must cut compressor clutch on low or excessive pressure. |
| Corrosion protection | Deburr all brackets and frame parts. Prime/coat only after successful dry-fit, final drilling, and weld inspection. Do not cover unverified holes/welds with Raptor. |

## Required Evidence

The shop must send these before the job is accepted:

1. Radiator sample video: old radiator beside new/recore unit, showing necks, cap, drain, mounts, and pressure/flow test.
2. Frame dry-fit photos: both uprights mounted, lower saddles/pads shown, radiator sitting square without twist.
3. Condenser dry-fit photos: tape visible for width/height/depth, port side shown, `10-15 mm` radiator gap shown.
4. Fan clearance video if fitted: grille/front-panel clearance, fan mounted to frame, no through-fin mount.
5. Drier photo: vertical mounting, capped until final assembly, hose directions marked.
6. Compressor check photos: clutch voltage, pulley alignment, suction/discharge ports, and leak/oil note.
7. Cabin evaporator photos: all-side measurements, under-dash mock-up, drain route, outlet face, fitting/TXV details, and blower/current notes.
8. Hose route photos before crimp: compressor, condenser, drier, firewall/bulkhead, evaporator, and service-port positions.
9. Final validation: cooling-system pressure test, A/C vacuum hold/leak test, clutch cutout test, condenser fan test, warm idle/running clearance video.

## Acceptance Rules

The delivery fails if any of these are present:

- radiator supported from one side only
- condenser or fan tied through fins
- condenser hanging from radiator brackets or radiator tanks
- radiator twisted or pulled by brackets or hose tension
- drier opened and left exposed before final assembly
- final hoses crimped before all component positions are locked
- purchased under-dash unit forces a bulky or service-blocking installation
- `24V` fan/compressor fitted to a `12V` system
- compressor operated without pressure-switch protection
- grille, bonnet latch, engine fan, belts, hoses, or service removal blocked after final tightening

## Shop Instruction Summary

```text
Deliver a complete, serviceable J40/2H A/C and front cooling stack: corrected radiator, two-side structural frame, R134a parallel-flow condenser, fan provision, new drier, pressure switch, accepted slimline under-dash evaporator, verified compressor, and crimped barrier hoses. Fit and validation control the purchase decision. Do not select parts by lowest price or by vehicle name alone.
```
