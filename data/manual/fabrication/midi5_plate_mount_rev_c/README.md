# J40 5-Way MIDI Plate Mount Pack - Rev C

This pack replaces the earlier boxed MIDI concept with an open plate-mount arrangement.

## Why Rev C exists

The earlier rear-panel concept implied the MIDI cables would have to leave rearward through a panel.
From your holder photos, that is not the natural cable path. These holders want the branch cables to leave
in-plane from the side, and the common bus feed to leave from its own side/end connection.

Rev C therefore uses:

1. `midi5_mount_plate_rev_c` - structural aluminium mount plate
2. `midi5_holder_subplate_rev_c` - non-conductive holder board

## 3D Visualisation

- `midi5_plate_mount_rev_c_3d_visualisation.html` is the interactive browser assembly view.
- `midi5_plate_mount_rev_c_3d_visualisation.svg` is the static fallback visual.

## Advantages

- No forced `90 degree` rearward cable exit
- Better space for heavy cable bend radius
- Easier service access to the fuse covers
- Simpler fabrication than a boxed enclosure
- Cable support can be added with P-clips after final routing is known

## Materials

- Mount plate: `3.0 mm 5052-H32 aluminium`
- Holder subplate: `5.0 mm HDPE, ABS, G10, or phenolic`

## Notes

- Use `10-12 mm` spacers between the holder board and the mount plate.
- Use the small side holes in the aluminium plate for cable P-clips or saddle clamps.
- Keep the common feed on the bus side and the five fused outputs on the branch side.
- This pack defines the MIDI holder plate and insulating subplate only. The vehicle-side battery tray / cutoff carrier is controlled by `docs/front-engine-bay-mounting-fabrication-plan-20260508.md` and remains on site-measurement hold.
