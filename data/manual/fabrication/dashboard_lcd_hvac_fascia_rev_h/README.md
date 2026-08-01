# J40 RHD full-width 9-inch LCD / four-outlet dashboard - Rev H

Rev H replaces the complete visible dashboard face with one restrained body-colour CNC-formed panel while retaining and transferring the original Toyota speedometer assembly and the original asymmetric glovebox lid, knob, hinges/latch and black instruction plate. The ashtray is deleted. A true 9-inch display reference sits centrally. Exactly four larger silver circular A/C outlets are used: the two end outlets remain high, while the symmetric inner pair sits wholly below the LCD in two local rounded pods. The normal lower edge is not dropped full-width. It rises around the right-hand-drive steering column in a radiused U-relief, and all controls sit in a compact two-row bank at the extreme right.

This package is ready to send for **quotation and a full-size disposable CNC template**. It is deliberately not a production vehicle-cut release: the nominal coordinate envelope is X=0…1260 mm and Y=-35…220 mm (1260 x 255 mm overall only where the local pods project) and cannot replace a physical trace of this vehicle. Only `CUT_TEMPLATE_OUTER` in `full_width_fit_template_rev_h.dxf` may be cut now, and only in MDF/card/cheap plastic. Every metal or vehicle feature remains `HOLD_*` until M1-M10 are signed.

## Locked layout

- Right-hand drive. Passenger is left; driver is right.
- One full-width visible face in 1.5 mm CR4 mild steel, low-gloss body colour.
- Original glovebox and speedometer are retained/reinstalled; their exact shapes and mounts are direct-transfer features, not nominal CNC geometry. In every owner-photo visual they are also **visual no-touch regions**: preserve their original colour, finish, patina, markings, controls and location exactly. The bare-shell visual may add only the correct original cluster copied from the assembled owner-photo reference into its existing factory opening.
- Screen active-image reference: **199.2 x 112.1 mm**, **228.6 mm / 9.000 inch diagonal**, 16:9. Its centre is constrained to the fascia centreline at nominal **X630.0/Y144.0**. This does not establish a real LCD chassis: the local Sehgal 9-inch listing has no mechanical drawing, so its aperture, bezel, rear body, mounts and connectors are M4-M5 HOLD.
- Four matching generic vents: **Ø87 visible silver/chrome face** and **Ø75 panel-opening reference**, dark directional core, hidden retention. Nominal centres are ((50.0, 168.5), (464.0, 20.0), (796.0, 20.0), (1210.0, 168.5)). V1/V4 remain high at **Y=168.5**, with their Ø87 bezel tops at **Y=212.0**, aligned with the LCD-bezel top. V2/V3 are lowered to **Y=20.0**; each visible face spans Y=-23.5…63.5 and therefore sits 12.5 mm below the nominal LCD-bezel bottom at Y=76.0. Their identical local pods descend to **Y=-35.0**, 85 mm below the normal Y=50.0 edge. The inner pair is exactly mirrored at **X=464.0 / 796.0**, or **±166.0 mm** about the LCD/fascia centreline. Ø75 is **not** a released production cut.
- The upper band remains **OEM glovebox | centred 9-inch LCD | OEM speedometer**. The outer vents occupy the far ends; the lowered inner pair uses otherwise empty space below and either side of the LCD without overlapping its bezel.
- The outer visible vent faces sit **6.5 mm** from the nominal usable-face ends; their Ø75 reference cuts retain **12.5 mm**. These tight lands are template/sample controlled and the outlets never move into the side returns.
- The nominal RHD steering-column axis is **X=930.0**, aligned with the retained cluster centre. The lower edge has a **130 mm-wide x 32 mm-rise** radiused U-relief and a nominal **130 x 105 mm** swept keep-out. These dimensions communicate packaging intent only: M1/M3/M9 must directly trace the installed column, shroud, stalks, bracket and full movement before any production cut. No switch, duct, carrier or rear stack may enter the signed keep-out.
- At the extreme right, fully outside that keep-out, exactly seven industrial rotary selectors plus one separate red hazard form **two rows of four**. Nominal columns are **X=(1096.0, 1144.0, 1192.0, 1240.0)**, with top **Y=88** and bottom **Y=30**: 48 mm horizontal / 58 mm vertical pitch. Schneider Harmony XB4 reference: **Ø22.5 panel cut** and **68 mm rear envelope**. Head/lever sweep, anti-rotation, right-outlet duct route, rear stacks and driver clearance remain M6/M8/M9 HOLD. Engrave labels 3 mm high with black infill.

## Exact visible controls

| Position | Label | Hardware / states | What it does |
|---|---|---|---|
| Top 1/4 | WIPERS | 3-position: OFF / LOW / HIGH | Parks the wipers in OFF and selects low or high wipe. |
| Top 2/4 | LIGHTS | 3-position: OFF / SIDE / HEAD | Selects master exterior-light state; original dip/high-low remains. |
| Top 3/4 | SPOTS | 2-position: OFF / ON | Commands T5 spot-lamp relay. |
| Top 4/4 | AUX | 2-position: OFF / ON | Commands reserved accessory relay B2. |
| Bottom 1/4 | BLOWER | 3-position: OFF / LOW / HIGH | Sends OFF/LOW/HIGH requests to the measured blower controller. |
| Bottom 2/4 | A/C | 2-position: OFF / ON | Requests B1 compressor cooling through thermostat/trinary/pressure safeties. |
| Bottom 3/4 | ENGINE | 2-position: RUN / STOP | Sends a low-current command through the validated fuel-stop interface; key OFF remains authoritative and the manual cable remains the fallback. |
| Bottom 4/4 | HAZARD | separate red pushbutton: OFF / FLASH | Operates the hazard/flasher circuit. |

The bank contains exactly **7 selectors + 1 hazard**. The formerly unallocated seventh selector is now `ENGINE`, with `RUN / STOP` engraving. It is a command device only: do not route stop-solenoid or motor current through it. Before wiring, EEI-003 must identify whether this vehicle uses an energise-to-run or energise-to-stop device and establish a fail-safe relay/controller interface. Key OFF must always stop the engine, and the original/manual diesel stop cable remains the independent mechanical fallback. The earlier concealed-needle fuel-stop plan is superseded; that part may remain uninstalled or be reassigned only after a separate security review. Also retain the original indicator stalk, dip/high-low control, horn actuation, keyed ignition, winch third lever and identified mechanical cables.

All selectors command fused relay/controller inputs only. No selector carries lamp, wiper-motor, blower, compressor-clutch, fuel-stop-device or accessory load current. Baseline mapping: T1 low beam, T2 high beam, T3 horn, T4 condenser fan, T5 spots, B1 A/C clutch request and B2 AUX. B3-B5 remain unassigned relay capacity until EEI-003 selects the correct ENGINE interface. Size the blower and A/C branches after actual current measurement. At M10 prove wiper park with washer retained separately, the complete OFF/SIDE/HEAD lighting truth table with original dip selection, measured blower control, A/C safety/fan logic, isolated hazard logic, and ENGINE RUN/STOP plus authoritative key-off and manual-cable fallback.

Cabin temperature/blend is deliberately outside the seven-selector allocation. Retain the delivered evaporator's measured thermostat/controller, and add a separate matched remote thermostat or heat/blend control only if physical inspection proves it is required. The visible `A/C` selector is compressor request only and remains interlocked through thermostat and pressure safeties.

## Construction intent

- Laser or waterjet the final face only after approved production geometry is derived from the signed template. Press-form returns after a cheap-sheet trial.
- Keep the visible face one piece. Concealed rear stiffener rails, local vent rings/doublers and the LCD carrier may be separate and welded, riveted or bolted as appropriate.
- Use approximately 15 mm returns where the vehicle permits. Where the compact right control channel prevents a continuous fold, use a concealed rear flange/doubler rather than exposed fasteners.
- Transfer LCD mass and control loads into retained cowl/dashboard structure through a rear carrier; never hang the display from the 1.5 mm skin alone.
- Use hidden M5 service fasteners at no more than 150 mm pitch where the physical structure permits. Allow cabin-side removal of the LCD and vents.
- Do not cut or weaken the cowl, A-pillars, firewall or steering-column support. Establish a continuous 20-25 mm attachment land where the vehicle permits.
- Cut approved vehicle sheet initially undersize, trim progressively, radius/deburr every edge and epoxy-prime exposed steel immediately.

## HVAC packaging

Use four branches from a balanced plenum, sized only after the received vent sample establishes the actual spigot OD and retention depth. Do not assume a 3-inch hose from the Ø75 face-cut reference. Do not crush ducts or block the glovebox, original instruments, steering column, loom, LCD connections, demist system or service removal. The lowered inner pods intentionally create extra rear neck/elbow depth, but their 85 mm local projection is a packaging envelope, not a proved clearance. At M8/M9 mock the two inner vents, all four duct bends, LCD carrier, retained components, selector contact stacks, column/shroud through full sweep, driver knees and every gear/transfer/winch lever position. Acceptance requires an as-built visible V2/V3-rim-to-LCD gap of at least **8 mm**, at least **10 mm** between inner-vent retainers/ducts and fixed LCD/cluster/support hardware, at least **20 mm** to the signed moving column/shroud/stalk swept envelope, and no duct minor axis below **90%** of its round ID. Actual bought-vent drawings and the complete rear mock-up control every aperture, retainer, hose ID and bend radius.

## Procurement and dimensional provenance

- The cost-conscious reference is the common silver/chrome ABS **Ø87 face / Ø75 opening** generic outlet family. It is a reference listing, not a released part: buy four visually and mechanically matched outlets from a single batch at a local Pakistan automotive A/C counter, then complete M7 calipers before any vent holes are cut. The Joom listing records the published family dimensions; `component_procurement_and_sample_plan.csv` records the source and sample path.
- The matching Daraz lead is currently unavailable and publishes no usable dimensions, so it is not a source of truth. The Restomod Air Diablo billet outlet is retained only as a premium import fallback; it would require a different M7 cut/duct detail.
- Sehgal Motors' locally listed 9-inch universal LCD is the procurement baseline, but it publishes no chassis/cutout dimensions. Purchase/borrow a sample or obtain a manufacturer drawing before releasing M4-M5.
- A public 1968-1978 replacement-panel listing gives **1400 x 250 x 100 mm**, confirming that broad dashboard dimensions are publicly listed. It is a centimetre-resolution vendor product envelope—not an installed 1978 RHD face outline, bend schedule or aperture/datum drawing—and Toyota EPC records configuration-specific panels. Therefore the Rev H **X=0…1260 / Y=-35…220** coordinate model remains a proportional quote/template datum, not an OEM dimension. M1 physical trace/scan still controls production. `dimensional_provenance_audit.csv` records the source URL and every release boundary.

## CNC layer rules

- `CUT_TEMPLATE_OUTER`: released only for the disposable full-size fit template.
- Every layer beginning `HOLD_`: construction/reference geometry only; never send directly to a production toolpath.
- `HOLD_FASCIA_OUTER`: nominal one-piece shape used to quote and create the first template; replace with the signed M1 vehicle trace.
- OEM, LCD, vent, switch, hazard, mounting and support geometry remains HOLD until its named measurement gate passes.

## Production gates

`measurement_and_release_schedule.csv` defines M1-M10: full vehicle perimeter/structure; OEM glovebox; OEM speedometer; LCD face drawing; LCD rear package; seven selectors plus hazard; four real vents; four-duct mock-up; signed full-size prototype; then continuity and live functional tests. No production metal or vehicle cut is authorised before all applicable gates are signed.

## Package contents

- `j40_dashboard_lcd_hvac_fascia_rev_h_shop_spec.pdf` - four-page shop specification.
- `dashboard_lcd_hvac_fascia_rev_h_dimensioned_front.svg` - dimensioned front design/release diagram.
- Two paired owner-photo overlays and the bought-selector reference image.
- `full_width_fascia_master_rev_h.dxf` - all-HOLD metal master/reference.
- `full_width_fit_template_rev_h.dxf` - disposable template outer cut plus HOLD component references.
- `right_control_bank_template_rev_h.dxf` - exact eight visible stations, all HOLD.
- `lcd_rear_support_reference_rev_h.dxf` - reference only, all HOLD.
- Eight CSVs covering cut/release, fascia coordinates, switch positions, M1-M10 evidence, dimensional provenance, procurement/sample controls, HVAC control interfaces and visual ratios.
- `visualisation_prompt_record.md` - reproducible image-edit prompt set and mode.

## Acceptance

The installed face reads as an original-adjacent J40 dashboard; the OEM glovebox and speedometer function normally and retain their original visible identity and factory openings; the display proves a 9-inch active diagonal and remains serviceable; the LCD centre lies exactly on the signed fascia centreline; the midpoint of the two lowered inner outlets lies on that same centreline with equal left/right offsets; exactly four matching large outlets receive unobstructed air; the two outer bezel tops align with the LCD-bezel top while both inner faces sit fully below the LCD; exactly seven labelled selectors plus the separate hazard occupy the signed two-row extreme-right bank and match the schedule; the normal lower edge remains at its original shallow datum except for the two local vent pods, column relief and compact control return; M8/M9 prove the 85 mm pod projections and all stated 8/10/20 mm clearance minima against the actual LCD, cluster, ducts, column, knees and levers; no duct, rear switch stack or driver contact clashes; no retained structure is weakened; and every M10 electrical/functional test passes without interference, voltage drop, overheating, rattle or unintended operation.
