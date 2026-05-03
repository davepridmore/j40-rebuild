# Suspension + Brake Merged Work Plan

- Updated: 2026-05-03
- Vehicle: 1978 Toyota Land Cruiser J40
- Start-here sources: [suspension-workstream.md](suspension-workstream.md), [brake-workstream.md](brake-workstream.md), [brake_system_requirements.csv](../data/manual/brake_system_requirements.csv)

## Decision

Run the Ironman Foam Cell suspension change and the brake baseline refresh as one controlled workshop window.

The working brake architecture remains `front disc / rear drum`. The plan now assumes normal brake service parts will be replaced on both axles as baseline work:

- Front: pads/hardware, front flex hoses, caliper seal/rebuild or caliper replacement as required by fitted caliper family, and rotor machine/replace decision by measured rotor condition.
- Rear: parking-brake cable set, axle hard lines, rear center flex hose, wheel cylinders, shoes, springs/hold-downs/adjusters, and line/cable clips.
- System: brake fluid, bleed consumables, cap/plug set, and master/reservoir/proportioning inspection with replacement only after the installed layout is identified.

This does not approve rear-disc conversion or a wholesale brake architecture change. It approves a standard safety refresh of the system already fitted to the truck.

## Why This Work Is Merged

The suspension change is the right time to handle rear brake cables and rear axle brake lines because the axle, springs, shocks, U-bolts, line clips, and cable routes are all exposed. It is also the only sensible time to confirm brake hose and parking-brake cable slack at full droop with the new Ironman geometry.

Do not final-close suspension until brake hose, hard-line, parking-brake cable, breather, steering damper, and shock clearances all pass at static height and supported droop.

## Work Sequence

| Step | Work | Gate |
| --- | --- | --- |
| 1 | Inventory Ironman shipments, support gear, brake parts, and brake-specific tools. | No work starts until the main kit, front damper pair, rated stands, jack, cribbing/chocks, torque wrench, and brake capture tools are available or assigned to the workshop. |
| 2 | Photograph and measure existing brake layout before removal. | `BR-CAPTURE-001` is complete: wide route photos plus close-ups with labels/ruler for front calipers, hose ends, rear cable ends, rear line fittings, clips, rear drum internals, and master/proportioning layout. |
| 3 | Remove rear parking-brake cables and rear axle hard lines only after labels/photos. | Old cables stay intact as length/end samples; hard lines stay as bend templates; every open hydraulic port is capped. |
| 4 | Open rear drums and front disc hardware for standard brake service identification. | Rear shoe dimensions, wheel-cylinder pattern, spring layout, front pad shape, caliper ports, rotor condition, and hose fittings are recorded. |
| 5 | Order or release exact brake parts from the measured samples. | No catalog-only ordering for the front conversion or rear cables. Use fitted hardware and old samples. |
| 6 | Install Ironman suspension and brake parts with axle supported independently. | No brake hose or cable is used as an axle travel limiter. U-bolts are new only. |
| 7 | Route rear cables, rear hard lines, rear center hose, and front hoses with the new suspension at droop. | Lines/cables are clipped, protected from chafe, clear of U-bolts/shocks/springs/tyres/exhaust, and slack at full droop. |
| 8 | Bleed, adjust, torque, align, and road-validate. | Pressure bleed, leak test, rear drum adjustment, parking-brake hold/release test, alignment, low-speed yard test, short road test, 50 km recheck, and 500 km recheck. |

## Brake Parts Checklist

| Item | Qty | Status | Release rule |
| --- | ---: | --- | --- |
| Ironman Foam Cell main suspension kit | 1 kit | Ordered, pending delivery | Count against [suspension-workstream.md](suspension-workstream.md). |
| Ironman `24635FE` front damper pair | 2 | Ordered as separate shipment | Must arrive before final suspension assembly or road validation. |
| Hardwood cribbing and wedge chocks | 8 blocks + 4 wedges | Purchase-ready | Order from [suspension-wood-cribbing-merchant-spec.md](suspension-wood-cribbing-merchant-spec.md). |
| Front disc pads and retaining hardware | 1 axle set | Needs fitted-caliper identification | Buy by pad shape/caliper family from the truck, not by year alone. |
| Front caliper rebuild kits or replacement calipers | 2 sides | Needs fitted-caliper identification | Replace/rebuild if seized, leaking, torn boots, damaged pistons, or unknown unsafe condition. |
| Front rotors | 2 | Inspect/machine/replace | Replace or machine only after diameter/thickness/runout/scoring check. |
| Front flexible brake hoses | 2 | Spec hold | Match caliper end, chassis bracket, free length, and full-lock/full-droop clearance. |
| Rear parking-brake cable set | 1 left/right set | Spec hold | Match both rear cable lengths, sheath lengths, backing-plate ends, equalizer ends, clips, return springs, and adjuster hardware. |
| Rear axle hard brake lines | 2 axle tubes plus fittings | Spec hold | Recreate in brake-rated `4.75 mm / 3/16 in` tube using old lines as bend templates. No bare copper. |
| Rear center flexible brake hose | 1 | Spec hold | Match fitting style and full-droop length with Ironman suspension. |
| Rear wheel cylinders | 2 | Drum-open identification | Buy as a pair after bore, port thread, bolt pattern, pushrod style, and side are confirmed. |
| Rear shoes and spring/adjuster hardware | 1 axle set | Drum-open identification | Buy after drum ID, shoe width, adjuster style, and spring layout are recorded. |
| Rear drums | 2 | Inspect/machine/replace | Machine or replace only if scored, cracked, stepped, or beyond service limit. |
| Brake-line and parking-brake cable clips | As counted | Count hold | Replace corroded/missing clips and add rubber-lined P-clips where original support is missing. |
| Brake master/reservoir/proportioning service parts | As fitted | Inspection hold | Replace only after current master, reservoir, booster, ports, and proportioning layout are photographed and checked. |
| Hydraulic-opening prep consumables | Enough for full bleed/line opening | Purchase-ready | Buy line caps/plugs, clear bleed hose/bottle or bleeder kit, brake cleaner, rags, gloves, and catch tray before any hydraulic line is opened. |
| Brake fluid | 2 L sealed total unless workshop specifies more | Purchase-ready | Use sealed fresh DOT 3 brake fluid meeting SAE J1703 / FMVSS No. 116 DOT 3; do not use DOT 5 or mix unknown old fluid. |
| Copper grease | On hand | Received | Use sparingly on appropriate brake contact points only, never on friction surfaces. |

## Tools And Support Checklist

| Tool/support | Current tracker read | Needed before work |
| --- | --- | --- |
| 3T trolley jack | Ordered, pending delivery | Must be received or workshop must provide equivalent. |
| Four rated 3T jack stands | Ordered, pending delivery | Must be received; cribbing is supplemental, not a stand substitute. |
| Hardwood cribbing and wedge chocks | Purchase-ready, not ordered | Buy before suspension/brake work if work is done at home. |
| Wheel chocks | Covered by wedge chock plan if built correctly | Use on the axle not being lifted. |
| Torque wrench | Received | Required for suspension, wheel, and disturbed bracket fasteners. |
| 24 inch breaker bar | Planned/open | Buy or confirm workshop equivalent before old spring/U-bolt work. |
| Metric socket/spanner set | Received tool set | Confirm sizes for spring, shackle, shock, wheel, and brake fittings. |
| Flare-nut/line wrenches | Not clearly tracked | Required for brake hard lines and flex hose fittings. |
| Brake line cutter, bender, and flaring tool | Not clearly tracked | Required if fabricating lines at home; otherwise confirm the brake shop provides them. |
| Brake bleeder bottle/vacuum bleeder and clear hose | Not clearly tracked | Required for hydraulic closeout. |
| Brake spring pliers/hold-down tool | Not clearly tracked | Required for rear drum spring/hardware work unless workshop provides them. |
| Caliper piston tool or C-clamp | Not clearly tracked | Required for front pad/caliper service. |
| Digital caliper/tape | Digital caliper planned/open | Needed for cable lengths, shoe width, drum ID, rotor thickness, hose/fitting checks, and bracket dimensions. |
| Line caps/plugs | Not clearly tracked | Required before any hydraulic line is opened. |
| Brake cleaner, rags, catch tray, nitrile gloves, eye protection | Partially tracked as cleaning/PPE | Must be ready before opening drums or hydraulic lines. |
| Camera/phone, labels/paint marker, ruler/tape, and clean background board | Available by workflow | Required for `BR-CAPTURE-001` before removal so old parts remain usable as samples and order evidence. |

## No-Go Conditions

- Any brake line is opened without caps/plugs, bleed plan, and brake fluid available.
- The rear parking-brake cables are cut or discarded before both ends and lengths are recorded.
- Front brake parts are ordered only from `1978 J40` catalog logic without identifying the fitted disc conversion hardware.
- Suspension is allowed to droop with brake hoses, hard lines, parking-brake cables, breathers, or wiring under tension.
- Final road test happens before brake bleed, leak test, rear adjustment, parking-brake test, suspension torque marks, and alignment.

## Closeout Evidence

Store these with the workstream before calling the merged job complete:

- Ironman receipt and contents photos for both shipments.
- Baseline and post-install suspension measurements.
- Rear cable and rear hard-line removal photos, labels, and old samples.
- Brake order-release close-up pack `BR-CAPTURE-001`.
- Rear drum internal photos before disassembly.
- Front caliper/pad/hose/rotor identification photos.
- Brake parts receipts and installed photos.
- Bleed/leak test record.
- Parking-brake hold/release adjustment record.
- Alignment record.
- 50 km and 500 km suspension/brake recheck records.
