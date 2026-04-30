# Project Control UI

This UI provides a navigable view over:

- core workstreams and their status
- part-ordering queue and in-flight deliveries
- project package steps (`WP01` .. `WP06`)
- linked image evidence from the photo inventory

## Rebuild Data

Regenerate the dashboard data after tracker updates:

```bash
python3 scripts/build_project_control_ui.py
```

Then open:

- `docs/project-control-ui/index.html`

