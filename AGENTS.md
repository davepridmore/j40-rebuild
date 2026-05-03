# Agent Instructions

## Google Photos Intake

When the user wants to provide project photos from Google Photos, use the repo picker workflow instead of a local macOS file picker:

```bash
./scripts/run_personal_photos_picker_on_demand.sh
```

The command opens the Google Photos Picker in the browser, waits for the user to select media and click Done, imports the selected items into `photos/`, filters probable non-car media, rebuilds `data/manual/photo_inventory.csv`, and refreshes `docs/photo-catalog.md` plus `docs/component-jobs-photo-reconciliation.md`.

Useful overrides:

```bash
RECENT_DAYS=30 ./scripts/run_personal_photos_picker_on_demand.sh
MOVE_NON_CAR=0 ./scripts/run_personal_photos_picker_on_demand.sh
```
