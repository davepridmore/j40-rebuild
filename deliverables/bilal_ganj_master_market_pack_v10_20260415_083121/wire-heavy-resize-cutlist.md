# Heavy Wire Resize Cut List (Bilal Ganj)

Date: 2026-04-15  
Based on: `wire_requirements.csv` + `loom_layout.csv` + current photo check

## What I Checked

- Requirements show the heavy feed should be split into multiple labeled segments, not one long continuous run.
- Your attached photo shows a long heavy red run coiled with the fuse hardware, which likely needs splitting.

## Must-Split Main Feed (25 mm² Red / ~4 AWG)

Cut and label these as separate segments (target lengths before terminal crimp):

1. `PWR-04` - Battery positive -> 100A breaker input - **0.30 m**
2. `PWR-05` - 100A breaker output -> junction stud - **0.60 m**
3. `PWR-06` - Junction stud -> ANL/MIDI fuse block input - **0.30 m**

Also keep these as separate heavy branches:

4. `PWR-10` - ANL fused output -> glow plug feed - **1.00 m**
5. `PWR-11` - ANL fused output -> EPS feed - **1.00 m**

Total 25 mm² expected cut length: **3.20 m**.
Ask shop to add **+50 mm service slack per segment** unless terminal position is final.

## Other Heavy Wires (Keep as Independent Runs)

- `PWR-13` Junction -> relay bank: **16 mm² (~6 AWG)**, **1.00 m**
- `PWR-09` ANL -> amp/sub: **16 mm² (~6 AWG)**, **5.00 m**
- `PWR-14` Junction -> ignition relay: **10 mm² (~8 AWG)**, **1.50 m**
- `PWR-15` Junction -> dash constant feed: **10 mm² (~8 AWG)**, **1.20 m**
- `PWR-07` ANL -> accessory area #1: **6 mm² (~10 AWG)**, **1.50 m**
- `PWR-08` ANL -> accessory area #2: **6 mm² (~10 AWG)**, **1.50 m**

## Shop Instructions

- Do **not** leave the main 25 mm² path as one continuous long cable.
- Crimp proper lugs on both ends for each segment (stud size matched on-site).
- Heat-shrink and mark each cable with the ID (`PWR-04`, `PWR-05`, etc.).
- Keep a little service slack, but stay near target lengths.
- If current cable already has lugs on both ends, cut and re-terminate only after confirming exact stud sizes.

## Mechanic Verification Before Leaving

- Continuity check each segment end-to-end.
- Confirm no strand damage near crimp points.
- Confirm lug hole size matches actual studs (battery, breaker, junction, ANL block, EPS/glow studs).
- Confirm routing path avoids sharp edges and moving parts.

## Note on EPS Feed Size

- Current reconciled requirement in `wire_requirements`/`loom_layout` uses **25 mm²** for `PWR-11` EPS feed.
- One older build note references `6 AWG` for EPS; treat that as legacy. Keep the heavier 25 mm² plan unless you intentionally re-spec the EPS power path.
