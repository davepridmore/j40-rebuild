# Gearbox Oil Service Workstream

Created: 2026-05-29

Workstream ID: `gearbox_oil_service`

Parent phase: `05_mechanical_baseline`

Vehicle: 1978 Toyota Land Cruiser J40, 2H diesel

## Purpose

Turn `Transmission/gearbox oil service - drain inspect and refill` into a controlled buying and workshop requirement. This is not a blind fluid change. It is a gearbox condition check with a refill only after the fitted gearbox, oil specification, quantity, plugs, and sealing washers are confirmed.

This workstream coordinates with `docs/gearbox-top-cover-workstream.md`. If the top cover or shift tower is opened, the oil service should close after that work is sealed. If the top cover is not opened, the drain inspection still runs as its own mechanical-baseline gate.

## Buying Requirement

Buy only after the workshop identifies the fitted gearbox and confirms the manual oil grade and fill quantity for that gearbox.

## Manual Lookup Result

Manual sources now give a clear candidate path, but they also show why the fitted gearbox still has to be identified before buying.

| Confirmed fitted gearbox | Manual basis | Gearbox oil requirement | Buy quantity rule |
| --- | --- | --- | --- |
| H41/H42 4-speed matched to the Aug. 1980 40/60-series Land Cruiser chassis/body manual | Toyota Land Cruiser Repair Manual, Aug. 1980, FJ40/FJ43/FJ45/FJ60, BJ40/BJ42/BJ43/BJ45/BJ46/BJ60, HJ47/HJ60 | SAE90 gear oil, API GL-4 or GL-5 | 3.1 L gearbox capacity; buy 4 L to cover fill plus small top-up allowance |
| H41 matched to the later Land Cruiser service-spec sheet | Later Toyota Land Cruiser service specification, lubricant table | SAE75W-90 gear oil, API GL-4 or GL-5 | 3.5 L gearbox capacity; buy 4 L |
| H55F 5-speed matched to the later Land Cruiser service-spec sheet | Later Toyota Land Cruiser service specification, lubricant table | SAE75W-90 gear oil, API GL-4 or GL-5 | 4.9 L gearbox capacity; buy 5 L |

Use the H41/H42 4-speed row only if the workshop confirms the current gearbox is that older 4-speed family by case marks, top-cover/shift layout, transfer interface, and shift pattern. If the gearbox is a later H41, H55F, or unknown swap, use the matching manual sheet instead. Capacity differences are enough that "Land Cruiser gearbox oil" is not a safe purchase description.

Current identification update, 2026-05-29: use the WhatsApp-confirmed basis from `mcp_whatsapp_j40_messages.csv:1797` (`2026-05-17T11:47:47Z`, TLC 40 Series Owners): "Your J40 has 2h engine with 5 speed gear. It was sold by Jahanzeb". Treat the H55F 5-speed row as the active candidate unless case/top-cover marks prove a different 5-speed swap. If H55F is confirmed, buy SAE75W-90 gear oil, API GL-4 or GL-5, quantity 5 L, plus matched drain/fill plug washers. Do not use the older H41/H42 4-speed SAE90 / 3.1 L row for this gearbox.

Lookup sources:

- Toyota Land Cruiser Repair Manual, Aug. 1980, hosted scan: `https://pdfcoffee.com/tm-toyota-manual-de-taller-toyota-land-cruiser-1980-en-ingles-pdf-pdf-free.html`
- Later Toyota Land Cruiser lubricant service-spec sheet: `https://toyotamanuals.gitlab.io/landcruiserjul2009/rm/rm183e/m_a_0032.pdf`

Required buying package:

- Correct manual gearbox oil for the fitted gearbox, in enough quantity to fill the gearbox plus a small top-up allowance.
- New drain plug and fill plug sealing washers or gaskets matched to the actual plugs.
- Clear sample cup or bottle with label for the drained oil inspection.
- Clean drain pan that has not been used for dirty engine oil or brake work.
- Filler pump or hose that can reach the gearbox fill port.
- Nitrile gloves, clean rags, and cleanup solvent if workshop stock is not being used.

Vendor or runner text:

```text
Need manual gearbox oil service consumables for the gearbox currently fitted to a 1978 Toyota Land Cruiser J40 with WhatsApp-confirmed 2H diesel and 5-speed gear. Quote the H55F 5-speed candidate: SAE75W-90 gear oil, API GL-4 or GL-5, 4.9 L capacity, buy 5 L after case/top-cover marks confirm H55F or the matching 5-speed manual spec. Supply new drain/fill plug sealing washers matched to the actual plugs and a filler pump or hose if the workshop does not supply one. Do not substitute differential/hypoid LSD oil, engine oil, brake fluid, or transfer-case oil. Before refill, drain oil into a clean pan, inspect the oil sample, plug magnet, and debris; stop if water or heavy metal is found.
```

Purchase hold:

- If gearbox model, oil grade, or fill quantity is unknown, collect prices/photos only. Do not pay.
- Because WhatsApp history confirms 2H engine with 5-speed gear, use the H55F 5-speed candidate until proven otherwise: SAE75W-90, API GL-4 or GL-5, 4.9 L capacity, buy 5 L after confirmation.
- Do not count Liqui Moly Touring High Tech SHPD-Motor Oil 15W-40 as gearbox oil; it is engine oil unless the fitted gearbox manual explicitly calls for engine oil.
- If the seller offers generic axle/differential oil as a substitute, reject it unless the fitted gearbox manual explicitly allows it.
- If drain/fill plug washers cannot be matched, photograph and measure the plug seat before buying.

## Pre-Work Gates

Close these before draining:

- Fitted gearbox is identified by casting/code, installed layout, or manual match.
- Fill plug can be loosened before the drain plug is opened.
- Vehicle is level and safely supported.
- Drain pan, clear sample cup, labels, light, and camera are ready.
- Drain/fill plug sockets fit correctly and do not round the plugs.
- Replacement sealing washers are present or confirmed reusable by the workshop.
- Manual/spec source gives oil grade, fill level method, fill quantity, and plug torque if available.

## Work Instructions

1. Photograph gearbox exterior, fill plug, drain plug, leaks, breather area, and current related routing before cleaning or draining.
2. Clean around the fill plug and drain plug so dirt does not enter the gearbox.
3. Confirm the fill plug opens before draining. If it does not open, stop.
4. Drain into a clean pan. Take an oil sample into a clear cup or bottle.
5. Photograph oil color, water separation, glitter, sludge, plug magnet, drain plug, and debris.
6. Inspect for burnt smell, heavy metal flakes, water/milkiness, chunks, and abnormal sludge.
7. If inspection is acceptable, refit drain plug with correct washer/gasket and torque basis.
8. Fill only through the correct fill port using the confirmed oil until the manual fill level/quantity is reached.
9. Refit fill plug with correct washer/gasket and torque basis.
10. Static-shift through all gears, then run or yard-test only when safe.
11. Recheck for leaks after first run, after yard movement, and again after the first real drive interval.

## Stop Conditions

Stop and reclassify to gearbox fault diagnosis or rebuild decision if any of these appear:

- Fill plug will not open.
- Gearbox model or oil spec is unconfirmed.
- Wrong oil has already been bought and no manual basis supports it.
- Water, milkiness, heavy glitter, flakes, chunks, bearing pieces, teeth pieces, or burnt oil is found.
- Drain/fill plug threads, casing threads, or plug seats are damaged.
- Gearbox has abnormal bearing noise, gear clash, jumping out of gear, or severe shift-tower wear.
- Top-cover work remains open and would require draining/refilling again.

## Evidence Pack

Save or attach:

- Gearbox identification photo or manual/spec basis.
- Fill plug open photo before draining.
- Drain plug and magnet/debris photos.
- Clear oil sample photo.
- Oil product photo showing grade/spec and quantity.
- Washer/gasket photo or note if reused by workshop decision.
- Filled-level/refill proof.
- Post-run leak-check photos.

## Closeout Gate

The workstream closes only when:

- Correct oil grade and fill quantity are recorded.
- Drain inspection found no stop-condition contamination or the issue was escalated.
- Gearbox is filled and plugs are sealed.
- Static shift and yard shift checks pass.
- Post-test leak checks pass.
- Any remaining gearbox findings are logged as separate defect rows.
