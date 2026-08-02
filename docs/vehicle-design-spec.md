# Vehicle Design Spec

## Purpose

This document defines the intended end-state of the J40 as a vehicle, not just as a project. It turns the current chat history and project evidence into a coherent design target that can guide parts, labour, sequencing, and trade-offs.

## Design Position

- Vehicle: 1978 Toyota Land Cruiser J40
- Chat-confirmed basis: ex-military J40, converted to diesel, Toyota 2H engine, 5-speed gearbox, previously associated with/sold by Jahanzeb.
- Design mode: OE-adjacent restoration with selective usability upgrades
- Intended use: reliable road-going classic 4x4 with improved drivability, lower cabin noise, cleaner wiring, and a more coherent interior
- Design rule: preserve the character of the truck while removing obvious hacks, noise, water ingress, and avoidable drivability pain

Evidence basis:

- `mcp_whatsapp_j40_messages.csv:1780` / `2026-05-17T11:05:54Z`, TLC 40 Series Owners: owner note says "1978 ex military, converted to diesel".
- `mcp_whatsapp_j40_messages.csv:1781` / `2026-05-17T11:06:16Z`, TLC 40 Series Owners: group member says it belonged to Jahanzaib from Lahore.
- `mcp_whatsapp_j40_messages.csv:1797` / `2026-05-17T11:47:47Z`, TLC 40 Series Owners: group member says "Your J40 has 2h engine with 5 speed gear. It was sold by Jahanzeb".
- `mcp_whatsapp_j40_messages.csv:1802` / `2026-05-17T12:10:28Z`, TLC 40 Series Owners: group member says Jahanzeb left the group after selling it.

## Design North Star

- Exterior and body should read as a proper J40, not a heavily modernized custom build.
- Mechanical and electrical systems should feel tighter, safer, and more dependable than the current truck.
- Interior should become cleaner, quieter, and more usable without losing the basic utilitarian identity of the vehicle.
- Upgrades should mostly be hidden, reversible, or visually restrained unless there is a clear reason not to do so.

## Design Principles

- `OE-adjacent, not concours`: aim for something that could plausibly have been built well, rather than a museum-original truck.
- `Function over gimmicks`: every visible change should improve use, durability, serviceability, or weather protection.
- `Repair before upgrade`: structural, weather, wiring, and baseline mechanical integrity come before comfort and audio.
- `Document every deviation`: if the build leaves stock, the reason and resulting spec should be recorded.
- `Serviceable by the next person`: wiring, parts choices, and fastener decisions should not trap the next owner or mechanic.

## Evidence-Based Direction

The following signals appear directly in chat evidence and form the backbone of the design:

- steering currently feels poor and a power-steering upgrade is desired
- electrical system should be stripped and rebuilt cleanly
- random LEDs, speakers, light bars, and extra wiring have already started coming out
- cabin noise reduction matters
- roof drainage/body issues matter
- removable body parts are expected to be sent out individually for quality repair
- bench-seat conversion is being considered
- interior should be refreshed after rust, sealing, and floor treatment
- a flush-mounted Android screen and some audio upgrades are being explored
- premium shocks and brake/steering upgrades are on the table, but a full suspension conversion is not baseline work

## Vehicle-Level Target

### 1. Exterior and Body

Target:
- straight, properly repaired body panels
- repaired roof channels and resolved water ingress paths
- corrected rust and pinhole issues before finish materials go down
- period-appropriate outward appearance
- no visibly half-finished panel, seal, or trim decisions

Design interpretation:
- keep the truck visually recognisable as a J40
- favor good panel fit and corrosion protection over radical visual customization
- removable components should be restored to a consistent standard, not patched at mixed quality levels

### 2. Chassis and Underbody

Target:
- structurally sound chassis
- repaired and protected floor
- rust treatment and sealing done in the correct order
- underbody decisions driven by longevity, not shortcuts

Design interpretation:
- structural work is a mandatory design layer, not hidden workshop housekeeping
- floor repairs, primer, seam treatment, and bed/floor coatings should form a coherent system

### 3. Mechanical Character

Target:
- retain the current engine for now unless hard inspection evidence pushes against that
- service and baseline the powertrain before entertaining replacement ideas
- reduce “old truck plus deferred maintenance” feel without turning the build into an engine-swap project

Design interpretation:
- current bias is toward keeping the existing engine
- mechanical baseline should deliver confidence, not necessarily originality purity
- replacement-engine thinking remains exploratory and off the current baseline path

### 4. Steering, Brakes, and Ride

Target:
- steering should no longer feel vague or ship-like
- braking should feel modern enough to trust
- ride should be more controlled without becoming overbuilt or financially absurd

Proposed design hierarchy:
1. steering rebuild and wear-item correction
2. ordered Ironman Foamcell kit content check and suspension installation
3. brake baseline
4. RHD J60/HJ60 hydraulic power-steering conversion using a component-in-hand frame plate, shaft, linkage and 2H pump package
5. final ride-height, caster, and alignment validation

Design interpretation:
- power steering is a real design goal, not just a repair item; the active route is a RHD J60/HJ60 hydraulic steering-box conversion with a 2H-compatible pump, superseding the prior column-EPS plan
- the Ironman Foamcell kit is now the suspension baseline
- front disc brakes fit the “usable classic” direction
- full spring / 4-link conversion is explicitly outside the baseline design

### 5. Electrical Architecture

Target:
- one coherent documented wiring system
- labeled circuits
- sensible fuse and relay layout
- proper cable protection, routing, grounds, and connectors
- removal of random accessory-era wiring clutter

Design interpretation:
- baseline circuits first: starting, charging, lights, horn, wipers, gauges, heater, reverse lights
- add-ons should hang off a clean architecture rather than distort it
- hidden reliability matters more than chasing a superficially stock loom
- serviceability and documentation matter more than purity

### 6. Lighting

Target:
- simpler, cleaner lighting with better reliability
- remove poor-quality add-on lighting clutter
- improve headlight performance via proper relays and better-supported hardware

Design interpretation:
- H4-style headlight upgrade is aligned with the evidence-based electrical plan
- light bars and random accessory lighting should not define the truck

### 7. Interior

Target:
- quieter cabin
- cleaner, less hacked interior
- refreshed trim after leaks, rust, and floor layers are solved
- more coherent seating and cargo usability

Design interpretation:
- sound deadening, foam, and carpet are part of the intended final package
- bench-seat conversion is a viable interior direction if mounting and usability work cleanly
- interior should feel restored and usable, not luxury-custom

### 8. Dashboard and Infotainment

Target:
- if modern infotainment is retained, it should be integrated cleanly rather than looking bolted on
- fuse-box and service access should not be sacrificed for speakers or screen placement

Design interpretation:
- the selected direction is a restrained, body-colour one-piece CNC replacement for the complete visible dashboard face, deleting and closing over the separate small ashtray while directly transferring the original large asymmetric plate-and-knob glovebox, original J40 speedometer assembly, factory-height lower edge and steering-column relief; the active selection, dimensional confidence and production holds are controlled by `data/manual/fabrication/dashboard_lcd_hvac_fascia_rev_i/README.md`
- the nominal 9-inch LCD active image—provisionally 198.91 × 111.89 mm inside an approximately 211.10 × 126.50 mm module—is centred in both axes on the complete traced factory-height fascia; the active Rev I V32 visual direction retains exactly two Ø87 mm target directional A/C outlet faces slightly higher and inward on one common datum, starts with the complete original cluster in its installed-photo relationship immediately above the steering-column shroud, deletes the Rev H inner/lower outlets and pods, and holds the exact height, glovebox/ashtray closure, cluster/column geometry, outlet centres, Ø75 mm target mounting interface, approximately 22 mm target body projection, all final apertures and the behind-dash package until the vehicle, all four bought louvers, compact two-takeoff evaporator and complete service envelope are physically measured and coupon-tested; if the higher/inboard rear package conflicts, move the outlet outward within signed fixed fascia land without moving either OEM assembly or increasing dash height
- the vehicle is right-hand drive. Exactly seven bought long-handle selectors sit together in the far-right 2 x 4 bank: Wipers, Lights, Spots and Aux above Blower, A/C and Fuel Stop, with a separate red Hazard in the eighth position. Wipers, Lights and Blower are 3-position; Spots, Aux, A/C and Fuel Stop are 2-position. The Fuel Stop selector is a low-current RUN/STOP request subject to EEI-003; key OFF remains authoritative and the original manual stop cable remains the emergency fallback
- any screen/audio plan must follow the cleaned electrical architecture and final dash packaging
- visible aftermarket clutter is contrary to the design direction

### 9. Audio

Target:
- restrained audio upgrade if kept
- no wiring mess, no compromised service access, no visible nonsense

Design interpretation:
- speaker wire, amplifier kit, and under-seat subwoofer are optional candidates
- audio should stay subordinate to the vehicle architecture
- if audio packaging conflicts with wiring access or OE-adjacent dash layout, audio loses

## Proposed Final Character

The target truck is:

- visually classic
- mechanically more confidence-inspiring
- electrically modern in reliability but not loud in appearance
- quieter and more weatherproof inside
- upgraded where the truck is genuinely weak
- restrained where novelty would compromise the identity of the build

In practical terms, that means:

- clean body and roof repair
- repaired floor and proper sealing stack
- re-architected wiring
- improved headlights and basic electrical usability
- steering/brake/suspension improvements that make it nicer to drive
- OE-adjacent interior with noise control and cleaner trim
- optional modern screen/audio only if integrated cleanly

## Proposed System Decisions

| System | Proposed Direction | Decision State |
| --- | --- | --- |
| Body style | Keep recognisable J40 form and panel language | `proposed` |
| Body restoration | Repair removable panels individually to a consistent standard | `proposed` |
| Roof | Remove, correct channels/water issues, refinish properly | `proposed` |
| Chassis/floor | Repair and protect before finish layers | `proposed` |
| Engine | Keep current engine pending inspection evidence | `proposed` |
| Steering | Rebuild baseline, pursue column-assist EPS through the General EPS Adapter route if packaging validates | `proposed` |
| Brakes | Upgrade toward more confidence-inspiring road use | `proposed` |
| Suspension | Ironman Foamcell kit ordered; track two shipments and validate fitment | `ordered` |
| Full suspension conversion | Out of baseline scope | `deferred` |
| Wiring | Full clean rewire / respin with documented architecture | `proposed` |
| Lighting | Relay-based clean lighting, better headlight performance | `proposed` |
| Interior finish | Sound deadening + foam + carpet after body sealing | `proposed` |
| Seating | Bench-seat conversion under packaging review | `under_review` |
| Dash | Keep visually disciplined, avoid clutter | `proposed` |
| Android screen | Optional, only if flush and integrated cleanly | `under_review` |
| Audio system | Optional and subordinate to serviceability | `under_review` |

## Baseline vs Optional

### Baseline Design Scope

- body and rust correction
- roof/water-path repair
- floor repair and sealing stack
- coherent wiring reset
- basic lighting correctness
- steering/brake baseline improvement
- weatherproofing and interior noise reduction
- trim reassembly to a coherent standard

### Optional Design Scope

- flush Android head unit
- amplifier and subwoofer
- premium non-essential audio packaging
- ambitious suspension experimentation
- engine replacement

## Open Design Questions

- What visual finish direction is intended for the exterior: preserve current palette, return to stock-adjacent color, or choose a new classic-appropriate finish?
- Are bench seats actually wanted after packaging/ergonomics review, or just being considered?
- Does the General EPS Adapter mock-up prove electric assist is safe/serviceable enough to proceed, or should the project fall back to rebuilt manual steering plus geometry cleanup?
- Does the truck want a discreet hidden modern screen, or would a more period dashboard treatment be better?
- What is the acceptable line between OE-adjacent and modernized in visible cabin elements?

## Immediate Design Tasks

1. Freeze the build as `OE-adjacent + hidden usability upgrades` unless a different brief is chosen.
2. Decide whether the Android/audio path is truly desired or should be cut from the first-pass design.
3. Decide whether the interior target is bench-seat based or current-seat based.
4. Create a paint and finish brief once more body evidence is available.
5. Create a wiring architecture sheet once the strip-down exposes the actual live circuits.
6. Create a steering/brake decision memo after baseline inspection, including General EPS Adapter mock-up evidence before any irreversible steering fabrication.
