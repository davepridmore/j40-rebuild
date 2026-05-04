# Bilal Ganj P2 Buy Sheet (Specs + Images + Prices)

Date: 2026-04-15  
Source of truth: `J40_Costs.xlsx` (`Parts` tab, P2 rows)

Note: the 10-way relay/fuse block is already bought and remains valid as specified. The separate cabin/interior car fuse boxes are not ordered; buy compact covered blade-fuse boxes separately.

## What To Buy First (De-duplicated)

1. **Body mount fastener pack (roll-up of Kits A+B+C+D)**
   - Workbook rows: `11` (roll-up), detailed specs in `225,226,227,228`
   - **Exact spec**:
     - **Kit A (tub-to-chassis mounts)**:  
       M10x1.25 class 8.8 bolts x16, M10 nuts (nyloc + all-metal mix) x24, M10 flat washers x40, M10 spring washers x20, M10 sleeves/spacers x16, M12 class 8.8 bolts x4, M12 nuts x6, M12 flat washers x12, M12 spring washers x6.  
       Buy +20% spares.
     - **Kit B (body panel/bracket hardware)**:  
       M6x1.0 class 8.8 bolts (12/16/20/25mm) x220, M6 nyloc nuts x160, M6 flange nuts x80, M6 flat washers x300, M6 spring washers x140, M8x1.25 class 8.8 bolts (16/20/25/30mm) x120, M8 nyloc nuts x90, M8 flange nuts x40, M8 flat washers x180, M8 spring washers x90.
     - **Kit C (captive/clip/rivnut)**:  
       M6 captive/clip nuts x120, M8 captive/clip nuts x60, weld nuts M6 x30, weld nuts M8 x20, rivnuts M6 steel x30, rivnuts M8 steel x20 (yellow-zinc or corrosion-resistant finish).
     - **Kit D (grounding hardware)**:  
       M6 star washers x120, M8 star washers x80, M10 star washers x40, serrated flange nuts M6 x40, serrated flange nuts M8 x20, conductive anti-corrosion paste x1 tube.
   - **Estimated price (PKR)**: `45,000 - 105,000` (avg `72,000`)

2. **Body-to-chassis mount rubber kit**
   - Workbook row: `12`
   - **Exact spec**:
     - OEM-style body mount biscuits/insulators + steel sleeves/cup washers for all mount points.
     - Must fit the mount stack and hardware above (`M10/M12` mounting hardware used in this project).
     - Verify **rubber hardness and height** against your old samples before purchase.
   - **Estimated price (PKR)**: `15,000 - 60,000` (avg `30,000`)

3. **Ignition lock security fix**
   - Workbook row: `39`
   - **Exact spec**:
     - Preferred: re-key existing barrel + matched key set (local locksmith).
     - Alternative: 40-series style ignition barrel + key set (ACC/IGN/START switch positions).
   - **Estimated price (PKR)**: `4,000 - 25,000` (avg `12,000`)

4. **Compact cabin fuse boxes**
   - Ledger entry: `part_cabin_compact_fuse_boxes`
   - Workbook correction: row `57` / `INV-0081` is a wrong generic listing and is **not** purchased stock.
   - **Exact spec**:
     - Required groups: **3 isolated under-dash fuse groups**.
     - Capacity: **6 constant-battery fuses, 6 ignition-on/RUN fuses, and 6 ignition part-way/ACC fuses minimum**.
     - Consolidated option: one Hyundai/OEM cabin fuse box is acceptable if continuity testing proves three isolated input buses and enough mapped slots for each group.
     - Fuse type: ATO/ATC blade fuse format.
     - Body: compact/OEM-style, covered, secure lid, strong terminals, no heat damage if donor.
     - Use for cabin/interior branch circuits only; do not substitute the already-bought relay block or MIDI/ANL holder.
     - Per-circuit limit: treat as 30A maximum unless the fuse-box manufacturer marks a higher rating.
     - Daraz live candidate checked 2026-05-03: Mughal Electronics RYK 12-way block, `138.25 x 85 x 36.5 mm`; fallback only because three are too bulky for under dash.
     - Reject single-bus blocks that cannot be split into the three input groups, large open universal blocks, loose fuse assortment boxes, relay blocks, and buying three bulky 12-way blocks for the cabin bracket.
   - **Estimated price (PKR)**: `11,100 - 21,000` (avg `15,000`)

5. **Electrical power steering (EPS) complete conversion kit**
   - Workbook row: `210`
   - **Exact spec (must be included in one kit)**:
     - Column-assist EPS unit: motor + torque sensor + reduction gear
     - EPS controller/ECU (or integrated control module)
     - Matching connectors with pigtails (minimum 150mm leads, for identification/bench-test only)
     - Upper + lower intermediate shafts with U-joints
     - Steering coupler/spline adapters for FJ40 side fitment
     - Column mount/clamp bracket set + firewall support bracket
     - New 60A fused feed path wiring/hardware + new ignition trigger lead
     - Fail-safe manual steering operation when assist is off
     - Column-assist conversion only; engine stays installed, with no engine lift or hydraulic pump hardware in this scope.
   - **Bench test before payment**:
     - No motor grinding noise
     - No jerky or delayed assist on smooth wheel rotation
     - Minimal free play/backlash at input-output hand check
   - **Estimated price (PKR)**: `54,000 - 136,000` (avg `90,000`)

## Estimated Total

- **Core P2-A + P2-B pack (without EPS)**
  - Low: `75,100 PKR`
  - Average: `129,000 PKR`
  - High: `211,000 PKR`

- **Core pack + EPS**
  - Low: `129,100 PKR`
  - Average: `219,000 PKR`
  - High: `347,000 PKR`

## Local Photos To Take On Phone (Your Car References)

- Body mount condition and geometry:
  - `/Users/davidpridmore/IdeaProjects/J40/photos/index/by_specific_component/body_mount_and_crossmember_detail/20260405_234546.jpg`
  - `/Users/davidpridmore/IdeaProjects/J40/photos/index/by_specific_component/frame_and_mount_points/20260405_234802.jpg`
  - `/Users/davidpridmore/IdeaProjects/J40/photos/index/by_specific_component/floor_seam_and_body_mount_rust/20260405_234652.jpg`
- Ignition/dash reference:
  - `/Users/davidpridmore/IdeaProjects/J40/photos/index/by_specific_component/dashboard_and_cabin_stripdown/20260323_180218.jpg`
  - `/Users/davidpridmore/IdeaProjects/J40/photos/index/by_specific_component/dashboard_fascia_trim/20260412_223534.jpg`
- EPS fitment context:
  - `/Users/davidpridmore/IdeaProjects/J40/photos/index/by_specific_component/driver_footwell_firewall_and_wiring/20260321_235600.jpg`
  - `/Users/davidpridmore/IdeaProjects/J40/photos/index/by_specific_component/steering_and_suspension_linkages/20260406_031010.jpg`

## Online Reference Images (Show Vendors The Style)

- FJ40 body mount kit style (shape/stack reference):  
  https://btbprod.com/product/body-mount-kit-fj40-1958-78-after-market-style/  
  https://daystarproducts.com/products/daystar-kt04003bk
- Ignition lock set style reference:  
  https://www.cityracerllc.com/products/ignition-cylinder-lock-set-for-75-and-later-toyota-land-cruiser-fj40

## Bilal Ganj Purchase Rules (To Avoid Wrong Parts)

- Confirm **metric thread pitch** with nut gauge: `M10x1.25` and `M8x1.25` where specified.
- Reject structural bolts without clear class marking (`8.8` minimum for these kits).
- For rubber mounts, buy only after physical sample fit (ID/OD/height + sleeve length).
- Buy the compact cabin fuse boxes as a separate open item; do not count the relay block or the old not-purchased workbook row as cabin fuse-box stock. Current requirement is three isolated under-dash fuse groups: constant, IGN/RUN, and ACC, with 6 fuse positions minimum per group.
- Do not double-buy duplicates: row `11` and detailed rows `225-228` cover the fastener kits; row `12` covers the rubber kit; row `13` covers shims/spacers.
