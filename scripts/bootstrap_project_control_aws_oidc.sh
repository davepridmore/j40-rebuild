#!/usr/bin/env bash
set -euo pipefail

AWS_PROFILE="${AWS_PROFILE:-default}"
AWS_REGION="${AWS_REGION:-ap-southeast-1}"
GITHUB_REPO="${GITHUB_REPO:-davepridmore/j40-rebuild}"
ROLE_NAME="${ROLE_NAME:-J40ProjectControlGitHubDeploy}"
POLICY_NAME="${POLICY_NAME:-ProjectControlS3Deploy}"
OWNER_TAG="${OWNER_TAG:-private-pridmoredave}"
S3_BUCKET="${S3_BUCKET:-j40-rebuild-dashboard}"
GITHUB_OIDC_THUMBPRINT="${GITHUB_OIDC_THUMBPRINT:-6938fd4d98bab03faadb97b34396831e3780aea1}"

for command in aws gh jq; do
  if ! command -v "$command" >/dev/null 2>&1; then
    echo "Missing required command: $command" >&2
    exit 1
  fi
done

ACCOUNT_ID="$(aws sts get-caller-identity --profile "$AWS_PROFILE" --query Account --output text)"
BUCKET_NAME="$S3_BUCKET"
OIDC_PROVIDER_ARN="arn:aws:iam::${ACCOUNT_ID}:oidc-provider/token.actions.githubusercontent.com"
ROLE_ARN="arn:aws:iam::${ACCOUNT_ID}:role/${ROLE_NAME}"

TRUST_DOC="$(mktemp)"
POLICY_DOC="$(mktemp)"
BUCKET_POLICY_DOC="$(mktemp)"
trap 'rm -f "$TRUST_DOC" "$POLICY_DOC" "$BUCKET_POLICY_DOC"' EXIT

cat >"$TRUST_DOC" <<JSON
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "${OIDC_PROVIDER_ARN}"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
        },
        "StringLike": {
          "token.actions.githubusercontent.com:sub": "repo:${GITHUB_REPO}:ref:refs/heads/main"
        }
      }
    }
  ]
}
JSON

cat >"$POLICY_DOC" <<JSON
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ManageDashboardBucket",
      "Effect": "Allow",
      "Action": [
        "s3:CreateBucket",
        "s3:GetBucketLocation",
        "s3:GetBucketPolicy",
        "s3:GetBucketPublicAccessBlock",
        "s3:GetBucketTagging",
        "s3:GetBucketWebsite",
        "s3:ListBucket",
        "s3:PutBucketPolicy",
        "s3:PutBucketPublicAccessBlock",
        "s3:PutBucketTagging",
        "s3:PutBucketWebsite"
      ],
      "Resource": "arn:aws:s3:::${BUCKET_NAME}"
    },
    {
      "Sid": "SyncDashboardObjects",
      "Effect": "Allow",
      "Action": [
        "s3:AbortMultipartUpload",
        "s3:DeleteObject",
        "s3:GetObject",
        "s3:ListMultipartUploadParts",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::${BUCKET_NAME}/*"
    }
  ]
}
JSON

cat >"$BUCKET_POLICY_DOC" <<JSON
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadDashboardSite",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::${BUCKET_NAME}/*"
    }
  ]
}
JSON

if aws iam get-open-id-connect-provider \
  --profile "$AWS_PROFILE" \
  --open-id-connect-provider-arn "$OIDC_PROVIDER_ARN" >/dev/null 2>&1; then
  echo "Using existing GitHub OIDC provider: ${OIDC_PROVIDER_ARN}"
else
  echo "Creating GitHub OIDC provider: ${OIDC_PROVIDER_ARN}"
  aws iam create-open-id-connect-provider \
    --profile "$AWS_PROFILE" \
    --url "https://token.actions.githubusercontent.com" \
    --client-id-list "sts.amazonaws.com" \
    --thumbprint-list "$GITHUB_OIDC_THUMBPRINT" >/dev/null
fi

if aws iam get-role --profile "$AWS_PROFILE" --role-name "$ROLE_NAME" >/dev/null 2>&1; then
  echo "Updating role trust policy: ${ROLE_NAME}"
  aws iam update-assume-role-policy \
    --profile "$AWS_PROFILE" \
    --role-name "$ROLE_NAME" \
    --policy-document "file://${TRUST_DOC}"
else
  echo "Creating role: ${ROLE_NAME}"
  aws iam create-role \
    --profile "$AWS_PROFILE" \
    --role-name "$ROLE_NAME" \
    --assume-role-policy-document "file://${TRUST_DOC}" \
    --tags "Key=Owner,Value=${OWNER_TAG}" "Key=Project,Value=J40" >/dev/null
fi

echo "Putting inline S3 deploy policy: ${POLICY_NAME}"
aws iam put-role-policy \
  --profile "$AWS_PROFILE" \
  --role-name "$ROLE_NAME" \
  --policy-name "$POLICY_NAME" \
  --policy-document "file://${POLICY_DOC}"

echo "Setting GitHub Actions secret AWS_ROLE_ARN on ${GITHUB_REPO}"
gh secret set AWS_ROLE_ARN --repo "$GITHUB_REPO" --body "$ROLE_ARN"

if aws s3api head-bucket --profile "$AWS_PROFILE" --bucket "$BUCKET_NAME" >/dev/null 2>&1; then
  echo "Using existing bucket: ${BUCKET_NAME}"
else
  echo "Creating bucket: ${BUCKET_NAME}"
  aws s3api create-bucket \
    --profile "$AWS_PROFILE" \
    --bucket "$BUCKET_NAME" \
    --region "$AWS_REGION" \
    --create-bucket-configuration "LocationConstraint=${AWS_REGION}" >/dev/null
fi

echo "Configuring public static website bucket: ${BUCKET_NAME}"
aws s3api put-bucket-tagging \
  --profile "$AWS_PROFILE" \
  --bucket "$BUCKET_NAME" \
  --tagging "TagSet=[{Key=Owner,Value=${OWNER_TAG}},{Key=Project,Value=J40},{Key=ManagedBy,Value=GitHubActions}]"

aws s3api put-public-access-block \
  --profile "$AWS_PROFILE" \
  --bucket "$BUCKET_NAME" \
  --public-access-block-configuration \
    BlockPublicAcls=false,IgnorePublicAcls=false,BlockPublicPolicy=false,RestrictPublicBuckets=false

aws s3api put-bucket-policy \
  --profile "$AWS_PROFILE" \
  --bucket "$BUCKET_NAME" \
  --policy "file://${BUCKET_POLICY_DOC}"

aws s3api put-bucket-website \
  --profile "$AWS_PROFILE" \
  --bucket "$BUCKET_NAME" \
  --website-configuration '{
    "IndexDocument": {"Suffix": "index.html"},
    "ErrorDocument": {"Key": "index.html"}
  }'

cat <<TEXT

Configured GitHub deploy role.

AWS account: ${ACCOUNT_ID}
AWS region:  ${AWS_REGION}
GitHub repo: ${GITHUB_REPO}
S3 bucket:   ${BUCKET_NAME}
Role ARN:    ${ROLE_ARN}

Next:
  gh workflow run deploy-project-control-ui.yml --repo ${GITHUB_REPO} --ref main
TEXT
