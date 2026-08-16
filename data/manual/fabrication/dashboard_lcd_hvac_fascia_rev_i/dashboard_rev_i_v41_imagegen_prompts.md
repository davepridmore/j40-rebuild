# Rev I V41 ImageGen record

Mode: built-in `image_gen`, using local image references. No fallback model was used.

## Straight-on transfer prompt

```text
Create a realistic straight-on fabrication design photomontage of the Toyota J40 dashboard.

REFERENCE PRIORITY:
1. The FIRST image is the mandatory base photograph and camera/view. Preserve its straight-on wide view, complete dashboard shell, cream paint, OEM glovebox at left, right-hand-drive instrument-cluster/steering-column structure, doors, cabin and workshop surroundings.
2. The SECOND image is design-intent reference only. Transfer its basic idea: one flush body-colour replacement panel, a recessed/coplanan 9-inch Pioneer screen, and one compact control row. Do not copy its oblique camera angle or distort the base.

GEOMETRY — CRITICAL:
- Keep the large asymmetric silver OEM glovebox and its black instruction plate/knob completely unchanged.
- Make ONE removable formed-steel replacement dashboard skin immediately to the RIGHT of the glovebox.
- Its LEFT seam must run closely alongside and parallel to the glovebox's curved/sloping right-hand edge, beginning at the factory upper dash fold and ending at the original lower dash edge. This is not a small rectangle or floating fascia.
- Its TOP edge must follow the existing long factory upper fold.
- Its BOTTOM edge must follow the existing normal dashboard lower line with zero downward extension.
- Its RIGHT edge must finish just before the retained speedometer/instrument-cluster and steering-column/scallop zone. Do not cover, move, delete or redesign the driver instrument-cluster structure.
- The replacement section must completely consume and eliminate the original small silver ashtray, the central large rectangular aperture, and the lower rectangular slot/opening. None of those old features may remain visible.
- The new skin is body-colour warm ivory/cream, coplanar with the surrounding dash, with a narrow realistic 2–3 mm shadow/service seam around its physical perimeter. No raised pod, no rounded plaque, no thick black surround and no downward hanging console.

COMPONENT LAYOUT:
- Install a Pioneer DMH-AP6650BT-style 9-inch landscape display in the upper half of the new panel. The visible face is about 229 mm wide by 131 mm high. It must be shallow, cleanly recessed, and its front glass/bezel exactly flush with the new panel—not floating in front.
- Put exactly SEVEN matching compact black lever/rocker selectors in one straight horizontal row beneath the screen.
- Add exactly ONE separate red hazard switch in that same row, after the seven black selectors.
- No additional switches, knobs, vents, ashtrays, badges, openings, or decorative trim.
- Keep adequate cream metal margin around the screen and controls; the composition should look buildable, restrained, period sympathetic and symmetrical within the available replacement section.

PHOTOGRAPHIC REQUIREMENTS:
- Do not beautify or restore unrelated parts. Preserve the workshop condition, scratches, rust, holes, floor, steering column and surrounding dashboard exactly as the base photograph.
- Use the base photograph's perspective and illumination. The result must clearly read as an overlay/design installed on the actual straight-on dashboard, not a new dashboard or studio render.
- No red markup, labels, measurements or arrows.
```

## Accepted correction prompt

```text
Correct the FIRST image, which is the current straight-on J40 dashboard design draft. The SECOND image is only a geometry-intent reference. Keep the FIRST image's exact straight-on camera, crop, complete vehicle/workshop background, cream body colour, unchanged OEM glovebox, screen size and location, right-hand instrument-cluster/column area, panel top edge, panel bottom edge and panel right termination.

Make ONLY these two design corrections:

1. LEFT PANEL SEAM: move the replacement panel's visible left perimeter leftward so it runs immediately alongside and parallel to the OEM glovebox's curved/sloping right-hand boundary, with only a narrow realistic 2–3 mm service gap. Begin this seam at the factory upper dash fold beside the glovebox's upper-right corner; follow the glovebox-side line downward behind the foreground gear lever where necessary; meet the existing lower dashboard line beside the glovebox's lower-right corner. The new panel must begin there and continue without interruption to the retained driver-cluster boundary. There must be no broad strip of old cream dashboard or remnant ashtray area between the glovebox and the new panel. Do not alter the glovebox itself.

2. CONTROL COUNT: beneath the screen show exactly SEVEN matching compact black lever/rocker selectors, followed by exactly ONE separate red hazard switch. Remove any eighth black selector. Keep them in one straight, evenly spaced horizontal line.

The old ashtray, original central rectangular aperture and original lower slot must remain completely absent. Keep the 9-inch Pioneer display cleanly recessed with its glass/bezel flush to the panel. The replacement must remain one coplanar full-height body-colour formed-steel section, not a rounded plaque, small rectangular cassette, raised pod or dropped console. Do not add vents, openings, knobs, switches, badges, labels, arrows, or decorative trim. Preserve the first image's photographic realism and unfinished vehicle condition.
```

Historical accepted output: `dashboard_rev_i_v41_front_on_full_section_body_colour.png`. V43 now supersedes its panel-boundary interpretation.

The two charcoal/alternate finish generations after V40 were rejected because they reintroduced original openings and changed the component layout. They are not project design files.
