# Manual Photo Drop Ingest

Use this when you want to hand over a batch of photos directly (not via Google Photos picker).

## Drop Folder

- Put files here: `data/inbox/manual_photo_drop/`
- Subfolders are allowed.
- Supported media: `.jpg .jpeg .png .webp .bmp .heic .heif .mp4 .mov .avi .mkv`

## Run

```bash
./scripts/run_manual_photo_drop_ingest.sh
```

What this does:

1. Imports from the drop folder into `photos/`.
2. Deduplicates by exact file hash:
   - Skips files already present in `photos/`.
   - Skips duplicate files within the same batch.
3. Archives source files and writes run logs in:
   - `data/raw/imports/manual_photo_drop/<run_id>/`
4. Rebuilds:
   - `data/manual/photo_inventory.csv`
   - `docs/photo-catalog.md`
   - `docs/component-jobs-photo-reconciliation.md`
   - `docs/project-control-ui/data.js`

## Useful Options

- Keep source files in the drop folder (copy mode):

```bash
COPY_ONLY=1 ./scripts/run_manual_photo_drop_ingest.sh
```

- Custom folders:

```bash
INBOX_DIR=/path/to/drop ARCHIVE_DIR=/path/to/archive ./scripts/run_manual_photo_drop_ingest.sh
```
