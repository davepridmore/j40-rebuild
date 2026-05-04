# Parts List Cleanup Decisions - 2026-05-04

Source update: user cleanup pass on the still-required / need-to-order list.

## Closed Or Removed Rows

- Drop separate `8mm split wiring pipe / loom pipe`. Existing 8/10mm sleeve stock is already tracked as received, and 8mm is not required as a separate active order.
- `Dashboard fascia / auxiliary switch panel` is received.
- `Hazard: red latching pushbutton` is received.
- `Starter interrupt security relay path` is received; wiring/install remains an electrical task.
- `Insulated Thimbles Male lug 4mm Yellow` is not an active buy because Deutsch connector stock is on hand. Reopen only for a confirmed non-Deutsch terminal gap.
- `Remove old LEDS` is removed from procurement. It is a service/electrical cleanup task, not a parts order.
- `HB BODY 999 seam sealer` is already tracked as Autohub order `1761310`, quantity 3 cartridges. Do not rebuy; only confirm physical tube count on receipt.
- `Primer` is already tracked as Daraz order `242366749280938` for the Hi-Build Zinc Rich Epoxy Primer EC 11 two-pack set. Do not buy a second generic primer.
- `Fuel-stop ignition-control hardware top-up` is stock-audit only. Use on-hand relay/fuse/terminal stock and any suitable donor pigtails first; reopen only if final fuel-stop wiring is short.
- `Vacuum hose refresh kit` is stock-audit first because similar hose stock was already ordered.

## Loom Pipe Lengths

For the 1978 J40 / HJ47-style 2H installation:

- No extra 8mm split pipe.
- If a top-up is needed after final routing, use `12mm split loom x 10m` for cabin, dash, lighting, and small branch runs.
- If a top-up is needed after final routing, use `16mm split loom x 6m` for under-bonnet and cabin trunk runs.
- Existing received sleeve stock already covers 8/10/14/16/20mm in 5m lengths; count it physically before buying.

## Sound Dampening Estimate

Defer until the body is welded, sealed, dry, and ready for interior stack-up.

- Minimum useful cabin estimate: `3.5-4.0 m2` / `38-43 sqft` of 3mm butyl/aluminium damping sheet.
- Sheet-count basis: `10` large `460x800mm` sheets minimum.
- Use `12` sheets if also covering doors, tailgate, or hardtop side panels.

## Body Mount Hardware Spec

Body-mount hardware is not covered by generic Millat bolts alone. Millat stock can cover generic metric nuts/bolts/washers, but the body-mount release still needs crush sleeves, cup/seat washers, repair material, and final length validation.

Exact release-held hardware spec:

- Main sleeves: `8` blanks, ID `10.8-11.0mm` for M10.
- Cup/seat washers: `14`.
- Trial bolts: M10 x 1.25, class 8.8 minimum, `70/80/90/100mm x4 each`.
- Nut/washer repair pack: all-metal nuts x12, nyloc nuts x12, flat washers x40, spring washers x20, M10 x 1.25 weld nuts x4, and 3mm repair tabs x4.
- M12 front-support pack: hold until measured.
- Shims/spacers belong with body-mount/rubber ordering: slotted steel `1/2/3/5mm x12 each`, plus thick control spacers `5/10/15mm x4 each`.

## Hose And Rubber Scope

Generic hose rows were suppressed. Exact hose rows remain in the hose/rubber workstream.

- Fuel: diesel-rated `8mm ID x 3000mm` feed, `6mm ID x 2000mm` return/bleed, `3.2-3.5mm ID x 1000mm` leak-off hose, rolled-edge fuel-injection clamps.
- Heater: EPDM SAE J20R3 or better, expected `16mm / 5/8in ID`, `400mm` inlet and `280mm` outlet cut lengths after nipple measurement.
- Vacuum/breather: reinforced `10-12mm ID x 2000mm` vacuum hose plus oil-resistant `16-19mm ID x 1000mm` breather hose, only after stock audit.
- Brake hoses: buy complete crimped brake hydraulic hose assemblies, not generic hose. Baseline order shape is `2 front flex hose assemblies + 1 rear center frame-to-axle hose`, DOT/SAE J1401 or OEM-equivalent, released by fitted end fittings, brackets, and old-sample/free length.

## Clutch Hydraulic Kit

This remains inspect-first, but the exact parts are now defined:

- Clutch master cylinder rebuild kit or complete master cylinder, matched to bore, pushrod, reservoir/pipe outlet, port thread, and flare/seat.
- Clutch slave cylinder rebuild kit or complete slave cylinder, matched to bore, pushrod/clevis, mount ears, bleeder position, port thread, and flare/seat.
- Clutch flex hose only if failed, ordered by free length, end fittings, bracket retention, and movement clearance.
- `1500mm` of `4.75mm / 3/16in` brake/clutch-rated hard-line blank only if the hard line is replaced.
- Use DOT 3 shared brake/clutch fluid and verify leak-free operation after bleeding.

## Gearbox Top Cover

Move gearbox top-cover service into its own workstream. The existing top cover is poor, so do not buy only detents/bushes/shift-seat parts blindly. First decide whether to source a replacement top cover or repair/weld the current one, then order the related service items.

## A/C Compressor Rows

`Sanden-type compressor` means the compact automotive A/C compressor style/family. The row is reuse/on-hand, not a current purchase. Before reuse, verify clutch voltage, pulley groove, ports, shaft seal/leaks, and oil/refrigerant compatibility.

`Engine-specific compressor bracket and belt solution` means the mounting and belt-alignment package for the Toyota 2H installation: compressor bracket, spacers, adjuster or idler if used, pulley alignment, belt section, and final belt length. Reuse unless the bracket is cracked, missing, or misaligned.
