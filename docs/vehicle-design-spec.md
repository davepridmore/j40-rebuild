# Vehicle Design Spec

## Purpose

This document defines the intended end-state of the J40 as a vehicle, not just as a project. It turns the current chat history and project evidence into a coherent design target that can guide parts, labour, sequencing, and trade-offs.

## Design Position

- Vehicle: 1978 Toyota Land Cruiser J40
- Current controlled basis: ex-military J40 converted to diesel, with the fitted engine positively identified from the owner-supplied block-stamp photograph as Toyota `2H`, serial `117299` (`2H-117299`): 3,980 cc, inline-six, 12-valve OHV, naturally aspirated diesel. Classify the fitted gearbox as Toyota `H55F` five-speed with high confidence: the existing whole-assembly photographs show the Toyota H41/H55F-family case and transfer-adaptor layout, while owner confirmation and the earlier WhatsApp/video record establish five forward gears. A unique gearbox assembly serial has not been captured; visible `33111`, `BYD`, and separate `3` marks are casting/part marks, not a serial. The August 2 steering photographs identify the as-fitted unit by housing, valve-head, port, sector-shaft, pitman-arm and pedestal-mount geometry as a Toyoda Koki late-40-Series factory-type hydraulic steering gear with high confidence. It is not original as-built equipment for this 1978 chassis, but is consistent with a later J40-family retrofit; the raised `25050` is a casting identifier, not a serial or complete Toyota service number. Exact `44110-xxxxx` identity remains unconfirmed.
- Design mode: OE-adjacent restoration with selective usability upgrades
- Intended use: reliable road-going classic 4x4 with improved drivability, lower cabin noise, cleaner wiring, and a more coherent interior
- Design rule: preserve the character of the truck while removing obvious hacks, noise, water ingress, and avoidable drivability pain

Evidence basis:

- `mcp_whatsapp_j40_messages.csv:1780` / `2026-05-17T11:05:54Z`, TLC 40 Series Owners: owner note says "1978 ex military, converted to diesel".
- `mcp_whatsapp_j40_messages.csv:1781` / `2026-05-17T11:06:16Z`, TLC 40 Series Owners: group member says it belonged to Jahanzaib from Lahore.
- `mcp_whatsapp_j40_messages.csv:1797` / `2026-05-17T11:47:47Z`, TLC 40 Series Owners: group member says "Your J40 has 2h engine with 5 speed gear. It was sold by Jahanzeb".
- `mcp_whatsapp_j40_messages.csv:1802` / `2026-05-17T12:10:28Z`, TLC 40 Series Owners: group member says Jahanzeb left the group after selling it.
- Owner-supplied block-stamp photograph received 2026-08-02 shows the `2H` engine code followed by serial `117299`. Record the engine as `2H-117299`. The supplied description places it in early-to-mid-1980s production, but no factory serial-to-date record is held in the project, so the build year remains an estimate rather than a procurement datum.

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
- use Toyota 2H workshop data and the measured as-fitted interfaces for engine-specific service parts, brackets, hoses and turbo hardware; the serial confirms the engine family but does not by itself prove every accessory or conversion interface

### 4. Steering, Brakes, and Ride

Target:
- steering should no longer feel vague or ship-like
- braking should feel modern enough to trust
- ride should be more controlled without becoming overbuilt or financially absurd

Proposed design hierarchy:
1. steering rebuild and wear-item correction
2. ordered Ironman Foamcell kit content check and suspension installation
3. brake baseline
4. replace the fitted late-40-Series factory-type hydraulic gear with a component-in-hand RHD J60/HJ60 steering-box upgrade, matched pitman/linkage and collapsible shaft; retain the current unit as the as-fitted baseline and match the 2H pump drive, reservoir and hoses to the selected J60 box
5. final ride-height, caster, and alignment validation

Design interpretation:
- power steering is already present as a later J40-family factory-type retrofit, but the planned upgrade remains a RHD J60/HJ60 hydraulic box conversion. The current box identification establishes the baseline; it does not cancel the J60 plan. The J80 route is superseded
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
- the active Rev I V44 appearance direction is one visibly closed, balanced centre panel between the unchanged OEM glovebox and speedometer. Its two upper corners use smooth radii consistent with the retained glovebox and speedometer openings; its side seams close the panel at those OEM boundaries; and its bottom is exactly the unchanged factory lower dashboard edge with 0 mm drop. It replaces the original ashtray pressing, central rectangular opening and lower slot without continuing to the far-right dashboard end. Every perimeter edge and radius must be traced directly before production release; V43's sharp-corner study and V41/V42 are superseded boundary studies
- the replacement section carries the purchased Pioneer DMH-AP6650BT with its 229 × 131 × 13 mm manufacturer-published front/nose flush with the panel. The V46-D1 A1 1:1 component sheet fixes this reference envelope, the 188 × 108 × 37 mm chassis, 196.608 × 114.15 mm effective display area and the official Schneider selector envelopes without pretending to fix their installation coordinates. All panel-perimeter, speedometer-side termination, corner-radius, aperture, rear-mount, duct and position data remain HOLD pending M1–M9 physical traces, actual parts and a complete rear buck; the controlled links are indexed by `data/manual/fabrication/dashboard_lcd_hvac_fascia_rev_i/README.md`
- the vehicle is right-hand drive. One line below the LCD carries seven bought black long-lever selectors—WIPERS, LIGHTS, SPOTS, AUX, BLOWER, A/C and FUEL STOP—plus a separate red HAZARD. Wipers, Lights and Blower are 3-position; Spots, Aux, A/C and Fuel Stop are 2-position. The Fuel Stop selector is a low-current RUN/STOP request subject to EEI-003; key OFF remains authoritative and the original manual stop cable remains the emergency fallback
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
| Engine | Retain and baseline Toyota `2H-117299`, 3,980 cc naturally aspirated inline-six diesel; use the stamp photo as identity evidence and measure all conversion interfaces | `identified_health_gate` |
| Turbo | Pursue the 2H low-mount CT26-flange / CT26-pattern TD05H 16G direction only after engine-health, goods-receipt and vehicle-clearance gates; commission at `5-7 psi` | `conditional_package_direction` |
| Steering | Baseline is the fitted Toyoda Koki late-40-Series factory-type hydraulic gear, exact service number open. Planned upgrade is a component-first RHD J60/HJ60 box, matched pitman/linkage and collapsible shaft with a measured, pressure/flow-matched 2H pump circuit; J80 is superseded | `j60_upgrade_component_gate` |
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
- Which exact RHD J60/HJ60 box, pitman arm, shaft/couplers and measured drag-link solution will be acquired, and how do they overlay the identified fitted J40-type gear and chassis interfaces?
- Does the truck want a discreet hidden modern screen, or would a more period dashboard treatment be better?
- What is the acceptable line between OE-adjacent and modernized in visible cabin elements?

## Immediate Design Tasks

1. Freeze the build as `OE-adjacent + hidden usability upgrades` unless a different brief is chosen.
2. Decide whether the Android/audio path is truly desired or should be cut from the first-pass design.
3. Decide whether the interior target is bench-seat based or current-seat based.
4. Create a paint and finish brief once more body evidence is available.
5. Create a wiring architecture sheet once the strip-down exposes the actual live circuits.
6. Complete the fitted J40-type hydraulic-gear interface survey, then acquire and bench-inspect the complete matched RHD J60/HJ60 conversion set before releasing any chassis, linkage or hose fabrication.
