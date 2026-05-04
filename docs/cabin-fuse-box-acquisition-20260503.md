# Cabin Fuse Box Acquisition - 2026-05-03

Purpose: source compact internal/cabin fuse protection around the actual reusable compact block/reference form, not a large marine/RV power distribution panel.

Updated visual reference: `deliverables/selling_site_images/images/manual_overrides/compact_cabin_fuse_box_user_photo_20260504.png`, the user-supplied actual compact old-OEM fuse box. This replaces the old extracted `junction_block.png` line drawing, the red MIDI holder photo, and any generated/generic fuse-box image for the dashboard and market brief.

## Target Spec

The wiring procurement requirement is `3` separately fed under-dash fuse groups. The older P2 market spec expressed this as three compact 6-way boxes, but a single OEM-style fuse/junction box is acceptable if it has three isolated input buses. The user-supplied 12-fuse donor block can also be reused for two feed groups if the rear terminals pass continuity and condition checks:

- `6` fuses minimum on the constant battery feed.
- `6` fuses minimum on the ignition-on / run feed.
- `6` fuses minimum on the ignition part-way / ACC feed.
- A single Hyundai/OEM cabin fuse box can consolidate the three boxes only if those three feed groups stay electrically isolated.
- A 12-fuse donor block plus one matching compact OEM-style add-on is acceptable: use the 12-way for two groups of 6 and the add-on for the remaining 6-fuse group.
- Do not buy a single-bus universal/portable block unless it can be safely split into three isolated buses by the electrician.

Fuse count by input type:

| Input group | Minimum positions | Key behavior |
| --- | ---: | --- |
| Constant battery | 6 | Live with key off |
| Ignition-on / RUN | 6 | Live in IGN/RUN, not live with key off |
| Ignition part-way / ACC | 6 | Live in accessory/part-way key position as specified by the ignition switch plan |

If the final circuit map needs more than 18 total under-dash branch fuses, use an OEM box with enough extra positions in the correct feed groups, or add a small auxiliary block for the short group. Do not count any existing under-bonnet fuse/relay hardware as under-dash fuse capacity.

Current preferred architecture after the 2026-05-04 rear photo:

- Reuse the existing 12-fuse donor block if each fuse position has independent rear terminals, no hidden shared bus, and all terminals are tight after cleaning.
- Assign the 12-way donor block to two groups of 6 fuses each.
- Buy one matching compact OEM-style add-on block for the third feed group. It does not have to be exactly 6-way; an 8/10/12-way old under-dash block is acceptable if it is as compact as the existing donor and six positions can be cleanly wired.
- Prefer using the best-insulated/cleanest block for the always-live constant-battery group if the existing donor block lacks a proper cover or rear terminal protection.
- Protect exposed rear terminals with an insulated back cover, boots, or a mounted enclosure.

Preferred form:

- Standard ATO/ATC medium blade fuses.
- Compact old-OEM fuse carrier shape matching the existing 12-way donor block as closely as possible.
- Narrow under-dash shape, similar to a two-column fuse block; avoid modern marine/RV covered blocks if they are physically larger than the donor block.
- Target physical envelope: roughly no larger than `130 x 70 x 45 mm` unless the electrician approves the mounting location.
- 6.3 mm male blade/Lucar terminals on the underside or rear, or clean serviceable pigtails.
- Used donor pigtails should be at least `100 mm` long so the electrician can splice and strain-relieve them correctly.
- Mounting tabs or screw holes suitable for an under-dash bracket.
- Separate branch circuits; no hidden shared output wiring unless the electrician maps it.
- Three isolated power inputs if using one consolidated OEM/Hyundai box.
- Same model for all boxes if buying multiple units instead of one consolidated box.
- Maximum branch fuse rating must be treated as `30A` unless the actual fuse-box manufacturer marks a higher per-circuit rating.

Use the existing reusable compact block as the shape and compactness reference. Do not source bulky universal/marine-style blocks unless all compact OEM local options fail.

## Consolidated OEM Fuse Box Acceptance

An OEM Hyundai-style fuse/junction box is acceptable if it passes these checks:

- It has at least three independent input pins/studs/wires suitable for constant, IGN/RUN, and ACC/part-way feeds.
- With all fuses removed, continuity testing shows no internal connection between the three input groups.
- Each fuse slot is mapped to exactly one input group before installation.
- The mapped slots provide at least 6 constant, 6 IGN/RUN, and 6 ACC/part-way protected outputs.
- Any factory relay or shared-bus section that cannot be confidently mapped is left unused.

## Existing 12-Way Donor Block Acceptance

The 2026-05-04 front/rear photos show a compact 12-fuse block that appears reusable if bench testing confirms the rear terminals are individually serviceable.

- Remove all fuses and continuity-test every pair of rear terminals.
- Confirm there is no continuity between unrelated fuse positions unless the electrician deliberately adds a feed jumper.
- Clean dust and stray copper strands from the rear before use.
- Reject the block if any fuse clip is loose, overheated, cracked, or missing.
- Use proper crimped jumpers or a covered bus feed for each 6-fuse group; do not use twisted copper wire as a feed bridge.
- Label the two groups on the 12-way block as two of `CONSTANT`, `IGN/RUN`, and `ACC`, then label the external 6-way as the remaining group.

## Current Buy Candidates - 2026-05-04

Reference product for local market:

- `Suzuki Mehran fuse box available` / `Suzuki Mehran Genuine Fuse Box`.
- Search terms: `Mehran under-dash fuse box`, `Mehran cabin fuse box`, `Mehran fuse carrier`, `Alto/Mehran fuse box`.
- Target donor: old Suzuki Mehran/Alto passenger-compartment fuse box, not engine-bay relay box and not fuse-box cover only.
- Donor priority: `1` Suzuki Mehran/Maruti 800 passenger-compartment fuse carrier, `2` Daihatsu Cuore cabin fuse carrier, `3` old Suzuki Alto, `4` compact old Toyota/Hyundai/Honda cabin fuse carrier, `5` modern Picanto/Hyundai-style junction box only if three isolated buses can be mapped and the box physically fits.
- Current OLX references found 2026-05-04: Multan/Gulgasht Colony listings around `Rs 1,100` to `Rs 1,300`.

Stable reference links:

- Suzuki/Maruti 800 genuine parts-catalog reference, Electrical `36 - WIRING HARNESS`: https://ftp.gforceparts.com/en/catalog/genuine/unit?c=SUZUKI201905&cid=1268&q=MA3ECA11S00938858&uid=40770&vid=0
- Catalog terms from that reference: `36717M80021 COVER, FUSE BOX`, `36791M84100 BRACKET, FUSE BOX`, and `36610N84721 HARNESS ASSY, WIRING NO.1`.
- Visual reference for the old Suzuki compact fuse-box family: https://www.suzuki-diely.sk/product/poistkova-skrinka-samurai-13/
- Official Maruti Suzuki genuine-parts fuse category, for fuse type reference only: https://www.marutisuzuki.com/genuine-parts/electrical/electrical-components/fuses
- Maruti 800 service manual reference showing the vehicle fuse box in wiring circuits: https://www.manualslib.com/manual/2075205/Maruti-Suzuki-Maruti-800.html

Selected visual reference from the user-supplied compact fuse-box photo:

- Maruti/Mehran-style compact fuse carrier with fuse-cover legend and rear pigtails.
- This form factor is acceptable and preferred over marine/RV or modern universal fuse blocks.
- If sourced in good condition, it can serve as the third 6-fuse group by using six clean fuse positions, or can replace the current 12-way donor for two groups if it has enough positions and better terminals.
- Buy with the cover and pigtails attached. Reject cover-only listings.

Procurement caution: some catalogs list `36717M80021` as `COVER, FUSE BOX`, while parts sellers may use the same family reference for the complete small fuse-box assembly. The market order is for the complete compact fuse carrier with rear terminals/pigtails, not just the cover.

Recommended first call/order candidate:

| Rank | Source | Link | Use |
| --- | --- | --- | --- |
| 1 | Reuse existing 12-way donor block plus buy one matching compact OEM-style add-on | User front/rear photos 2026-05-04 | Best current architecture if bench testing passes. The add-on should match the donor block's compact old-OEM form factor; it can be 8/10/12-way if only six positions are used. |
| 2 | Maruti/Mehran-style compact fuse carrier with cover and pigtails | User image 2026-05-04; visual reference https://www.suzuki-diely.sk/product/poistkova-skrinka-samurai-13/ | Preferred reference product. Image shows the right compact old-OEM body, cover/legend, and pigtails. Buy this style locally if terminals are clean and at least six fuse positions are usable. |
| 3 | Suzuki/Maruti 800 compact fuse-box family - stable catalog reference | https://ftp.gforceparts.com/en/catalog/genuine/unit?c=SUZUKI201905&cid=1268&q=MA3ECA11S00938858&uid=40770&vid=0 | Best stable web reference for the old Suzuki/Maruti compact fuse-box family. Use catalog terms `COVER, FUSE BOX`, `BRACKET, FUSE BOX`, and `HARNESS ASSY, WIRING NO.1` to explain the target, but buy the complete compact fuse carrier with rear terminals/pigtails, not the cover alone. |
| 4 | Suzuki Mehran fuse box available / Suzuki Mehran Genuine Fuse Box - market term | Local market / OLX search | Best current Pakistan source class because market results show old compact OEM-style fuse blocks, not bulky universal boxes. Search result examples found `Rs 1,100` to `Rs 1,300`, Gulgasht Colony, Multan. Buy only after front/rear/side photos confirm it is the same compactness as the existing donor and has six usable fuse positions. |
| 5 | Toyota Corolla fuse box - OLX Lahore / Model Town Extension | https://www.olx.com.pk/model-town_g5000051/spare-parts_c82/q-corolla | Backup only if the add-on must come from a Toyota donor or the Mehran leads fail. Search result shows `Corolla fuse box call 03228024104`, `Rs 5,000`, Model Town Extension, Lahore, and the visible photo shows rear wiring/pigtails. Likely larger than needed for the third 6-fuse group. |

Deprioritized candidates:

- Kia Picanto 2019-2024 Fuse Box - PakAutoParts: technically promising and likely to expose BATT/IGN/ACC feed groups, but current listing is used, visually imperfect, and expensive at `PKR 35,000`.
- Hyundai Tucson 2022-2025 Fuse Box Kit - PakAutoParts: call-for-price and the photo does not prove it is the desired cabin/interior junction box.
- Daraz/Blue Sea/marine-style 6-way blocks: electrically valid but no longer preferred because they do not match the compactness of the reusable 12-way donor block.

Kia Picanto official manual support: the 2024 Picanto owner manual documents a driver's side fuse panel, says the panel-cover label gives fuse name/capacity, and lists the engine compartment feed for the `PDM Relay Box (IG1 Relay, ACC Relay)` / ignition switch plus multiple Instrument Panel Junction Block feeds. This supports the assumption that a Picanto OEM junction block can expose the required BATT/IGN/ACC feed groups after bench mapping.

## Buy / Quote Sources

| Source | Link | Use |
| --- | --- | --- |
| Bilal Ganj / Montgomery Road electrical supplier | Local market | Preferred. Ask first for one compact old-OEM under-dash fuse carrier matching the existing 12-way donor block's size and terminal style. It can have 8/10/12 positions as long as six can be used cleanly for the third feed group. If the 12-way fails testing, ask for one compact OEM cabin fuse/junction box with three isolated input groups, or `3` matching clean OEM-style internal fuse blocks. Toyota/Suzuki/Daihatsu/Hyundai/Honda small under-dash blocks are better than bulky marine/RV blocks. |
| PakAutoParts fuse-box category | https://pakautoparts.pk/fuse-boxes | Pakistan used-OEM source/check page. The category shows local OEM fuse boxes and model filters; confirm exact dimensions, cover, pigtails, and circuit count before buying. |
| PakAutoParts Daihatsu Cuore fuse box | https://pakautoparts.pk/daihatsu-cuore-fuse-box | Local OEM-style example checked 2026-05-03: used genuine Daihatsu fuse box, shown at PKR 12,500. Use as a donor candidate only after availability, front/rear/scale photos, cover, pigtails, and terminal condition are confirmed. |
| Suzuki/Maruti 800 parts-catalog fuse-box reference | https://ftp.gforceparts.com/en/catalog/genuine/unit?c=SUZUKI201905&cid=1268&q=MA3ECA11S00938858&uid=40770&vid=0 | Stable reference for old compact Suzuki/Maruti fuse-box family. Shows `COVER, FUSE BOX`, `BRACKET, FUSE BOX`, and wiring harness assembly context. |
| Suzuki-diely old Suzuki fuse-box visual reference | https://www.suzuki-diely.sk/product/poistkova-skrinka-samurai-13/ | Visual reference for similar compact old Suzuki fuse-box form factor. Not a Pakistan buy source and currently out of stock; use only to show the physical style. |
| Official Maruti Suzuki genuine fuse category | https://www.marutisuzuki.com/genuine-parts/electrical/electrical-components/fuses | Official fuse-type reference only. It shows genuine Suzuki fuse listings, but not the Mehran/Maruti 800 fuse-box carrier itself. |
| Daraz 6-way automotive blade fuse box | https://www.daraz.pk/products/6-ways-12-24v-automotive-circuit-blade-fuse-box-for-car-truck-vehicle-i486699111.html | Electrically suitable but not the desired compact old-OEM form factor, and out of stock on 2026-05-04. Do not buy unless local compact OEM donor options fail. |
| Daraz 12-way portable automotive fuse box | https://www.daraz.pk/products/portable-12-way-car-fuse-box-universal-automotive-box-holder-with-led-indicator-black12v24v-power-distribution-i472891084.html | Live Pakistan fallback checked 2026-05-03. Seller: Mughal Electronics RYK. Price shown: PKR 4,500 plus PKR 190 delivery. Too bulky for buying three under-dash units; use only if the electrician approves a revised layout. |
| Daraz automotive fuse/accessory search | https://www.daraz.pk/automotive-fuses-accessories/?q=fuse%20box | Re-check for newer 6-way/8-way OEM-style local listings before payment. |
| Daraz 4-way waterproof blade fuse holder | https://www.daraz.pk/products/new-4-way-blade-fuse-holder-box-waterproof-with-4pcs-for-12v-24v-auto-car-i277001027.html | Do not buy now: out of stock on 2026-05-03 and only 4 circuits. Use only as a visual reference if restocked. |
| Sehgal Motors "Car Fuse Box with Standard Medium Blade Fuses" | https://sehgalmotors.pk/products/fuse-60a-box-fuse-kit-for-trucks-and-cars | Do not buy for this item. The listing is a fuse assortment/storage box, not an installable cabin fuse holder. |

## Local Market Order Text

Copy/paste this to Bilal Ganj, Montgomery Road, or the auto electrician:

> Need compact internal/cabin blade fuse protection for a 1978 Toyota Land Cruiser J40 rewire. Match the attached existing compact reference photo, not a large marine/RV panel.
>
> Need three separate under-dash power groups: constant battery, ignition-on/RUN, and ignition part-way/ACC. Each group needs at least 6 fuse positions. We already have one compact old-OEM 12-fuse donor block that may handle two groups if testing proves the rear terminals are individual and clean. Quote one matching compact old-OEM fuse carrier for the third group. It can be 6/8/10/12-way; we only need six usable fuse positions, but it must be similar compactness to the attached donor block.
>
> Reference product: Maruti/Mehran-style compact under-dash fuse carrier with cover/legend and rear pigtails, also sold as `Suzuki Mehran fuse box available`, `Suzuki Mehran Genuine Fuse Box`, or `Mehran cabin fuse box`. Standard ATO/ATC medium blade fuse type, compact old under-dash body, mounting tabs, and rear/underside terminals or clean serviceable pigtails preferred. Small OEM donor boxes from Suzuki Mehran/Alto, Daihatsu Cuore, old Toyota, Hyundai, or Honda are acceptable if condition is clean.
>
> Target size is roughly no bigger than 130 x 70 x 45 mm unless the electrician approves the bracket location. Used pigtails should be at least 100 mm long. If it is a single larger OEM junction box, it must have three isolated input groups that can be mapped as BATT, IGN/RUN, and ACC.
>
> These are for under-dash cabin branch circuits only. Do not quote relay blocks, loose fuse assortment boxes, or large marine/RV panels.
>
> Reject melted, brittle, cracked, corroded, loose-terminal, missing-cover, or cut-too-short used fuse boxes. Send photos of front, rear/terminal side, side profile, cover, and a ruler/hand scale before purchase.

## Acceptance Checks

- Cover fits and clips securely.
- Every fuse grips tightly; no loose fuse terminals.
- No heat discoloration, melted plastic, corrosion, broken locks, or cracked mounting ears.
- Terminal type and orientation are visible before payment.
- Supplier sends front, rear, side, and scale photos before purchase if not buying in person.
- If used OEM blocks are selected, pigtails must be long enough to splice properly and every circuit must be continuity-tested.
- Confirm each branch circuit is fused at `30A` or lower unless the box is clearly rated higher by the manufacturer.
- For a consolidated OEM box, mark every fuse slot as `CONSTANT`, `IGN/RUN`, `ACC`, or `UNUSED` before installation.
