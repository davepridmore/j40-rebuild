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

- `./start-dashboard.command`

The launcher serves the repo at `http://127.0.0.1:<port>/docs/project-control-ui/`
so video controls and media loading behave like the deployed dashboard.

## Deploy

The GitHub Actions workflow at `.github/workflows/deploy-project-control-ui.yml`
publishes a public S3 static website from a staged artifact. It does not sync the
repo, `data/`, or raw deliverables. The staging step copies:

- `docs/project-control-ui/index.html`
- `docs/project-control-ui/app.js`
- `docs/project-control-ui/styles.css`
- `docs/project-control-ui/assets/`
- a public copy of `docs/project-control-ui/data.js`
- only media files referenced by that public dashboard data, copied into
  `assets/dashboard-media/` with generated names

The workflow creates or updates this bucket:

```text
j40-rebuild-dashboard
```

Required GitHub secret:

```text
AWS_ROLE_ARN
```

Required GitHub variable for CloudFront cache invalidation:

```text
CLOUDFRONT_DISTRIBUTION_ID
```

That role should belong to the private AWS account used for this project. The
private account email is not stored in the workflow. The role needs to allow S3
bucket creation, bucket website configuration, bucket tagging, bucket policy
updates, and object sync/delete for the dashboard bucket.

If the private AWS profile is available locally, bootstrap the S3 bucket,
website policy, GitHub OIDC role, and GitHub secret with:

```bash
AWS_PROFILE=default scripts/bootstrap_project_control_aws_oidc.sh
```

Use a different `AWS_PROFILE` value if the private account is stored under
another local profile name. Then run the deploy:

```bash
gh workflow run deploy-project-control-ui.yml --repo davepridmore/j40-rebuild --ref main
```

The S3 website URL is:

```text
http://j40-rebuild-dashboard.s3-website-ap-southeast-1.amazonaws.com/docs/project-control-ui/
```

The public HTTPS URL is served through CloudFront:

```text
https://dbvg4yfpnc4tj.cloudfront.net/docs/project-control-ui/
```
