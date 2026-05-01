# Photo Ingest Automation Status

- Updated: 2026-05-02 01:41:24 +0500
- Personal OAuth client configured: `project 975499870450` (`perception-website`)
- Enabled APIs on personal project:
  - `photospicker.googleapis.com`
  - `photoslibrary.googleapis.com`
- Primary mode: `on-demand personal picker import + analysis refresh`
- Full-library mode: `Google Takeout archive ingest`
- Latest personal picker run:
  - Run ID: `20260502T013759`
  - Picker items selected: `14`
  - Downloaded: `14`
  - Car-related kept after filter: `14`
  - Moved to `photos/non_car_review`: `0`
  - Current indexed media count: `572`
  - Date coverage now reaches: `2026-05-02`

## Primary Flow (Personal On-Demand)

1. Run `./scripts/run_personal_photos_picker_on_demand.sh`.
2. Open picker URL and select new J40 media.
3. Script imports into `photos/`, filters probable non-car media, rebuilds catalog and reconciliation.
4. Updated outputs:
   - `data/manual/photo_inventory.csv`
   - `data/manual/photo_non_car_filter_report.csv`
   - `docs/photo-catalog.md`
   - `docs/component-jobs-photo-reconciliation.md`

## Full-Library Snapshot Flow (Takeout)

1. Place Google Takeout archive in `data/inbox/takeout/` (`.zip`, `.tgz`, `.tar.gz`).
2. Run `./scripts/run_photo_ingest_on_demand.sh`.
3. Ingest all media from archive and refresh analysis outputs.

## Notes

- Google Photos Library API policy limits API reads for many clients; `rclone` path is not treated as full-library reliable.
- For complete historical coverage, continue using Takeout imports.
