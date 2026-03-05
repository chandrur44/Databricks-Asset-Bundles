# GitHub Actions Setup Guide

This guide walks you through setting up automated CI/CD for your Databricks Asset Bundle.

**Repository**: https://github.com/chandrur44/Databricks-Asset-Bundles

---

## 🔐 Step 1: Add Repository Secrets

Go to your GitHub repository:
```
https://github.com/chandrur44/Databricks-Asset-Bundles/settings/secrets/actions
```

Click **"New repository secret"** and add these **5 secrets**:

### Required Secrets

| Secret Name | Value | Where to Get It |
|-------------|-------|-----------------|
| `DATABRICKS_DEV_HOST` | `https://xxxxx.cloud.databricks.com` | Your Dev workspace URL |
| `DATABRICKS_UAT_HOST` | `https://yyyyy.cloud.databricks.com` | Your UAT workspace URL |
| `DATABRICKS_PROD_HOST` | `https://zzzzz.cloud.databricks.com` | Your Prod workspace URL |
| `DATABRICKS_CLIENT_ID` | `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` | Service Principal Application ID |
| `DATABRICKS_CLIENT_SECRET` | `dapixxxxxxxxxxxxxxxxxx` | Service Principal Secret |

### How to Add Each Secret:

1. Click **"New repository secret"**
2. Name: `DATABRICKS_DEV_HOST`
3. Secret: `https://xxxxx.cloud.databricks.com`
4. Click **"Add secret"**
5. Repeat for all 5 secrets

---

## 🌍 Step 2: Configure Environments (Optional but Recommended)

Environments add protection rules and approvals.

### Create Dev Environment

1. Go to: `https://github.com/chandrur44/Databricks-Asset-Bundles/settings/environments`
2. Click **"New environment"**
3. Name: `dev`
4. Click **"Configure environment"**
5. (Optional) Add reviewers if you want approval before deploying to dev
6. Click **"Save protection rules"**

### Create UAT Environment

1. Click **"New environment"**
2. Name: `uat`
3. Click **"Configure environment"**
4. ✅ Enable **"Required reviewers"** (recommended)
5. Add 1-2 team members who should approve UAT deployments
6. Click **"Save protection rules"**

### Create Production Environment

1. Click **"New environment"**
2. Name: `production`
3. Click **"Configure environment"**
4. ✅ Enable **"Required reviewers"** (HIGHLY RECOMMENDED)
5. Add senior team members who should approve production deployments
6. ✅ (Optional) Enable **"Wait timer"** - e.g., 5 minutes delay
7. Click **"Save protection rules"**

---

## 📝 Step 3: Update Config Files

The config files already use environment variables, so they're dynamic!

**No changes needed** - the configs are already set up to use:
- `${env.DATABRICKS_CLIENT_ID}` from GitHub secrets
- Workspace URLs are set via environment variables in the workflow

### Verify Config Files:

**`config/dev.yml`:**
```yaml
workspace_host: "https://xxxxx.cloud.databricks.com"  # Update with your actual URL
service_principal_client_id: "${env.DATABRICKS_CLIENT_ID}"  # Already dynamic!
checkpoint_location: "s3://your-bucket/dev/checkpoints"  # Update with your S3 bucket
```

**`config/uat.yml`:**
```yaml
workspace_host: "https://yyyyy.cloud.databricks.com"  # Update with your actual URL
service_principal_client_id: "${env.DATABRICKS_CLIENT_ID}"  # Already dynamic!
checkpoint_location: "s3://your-bucket/uat/checkpoints"  # Update with your S3 bucket
```

**`config/prod.yml`:**
```yaml
workspace_host: "https://zzzzz.cloud.databricks.com"  # Update with your actual URL
service_principal_client_id: "${env.DATABRICKS_CLIENT_ID}"  # Already dynamic!
checkpoint_location: "s3://your-bucket/prod/checkpoints"  # Update with your S3 bucket
```

---

## 🚀 Step 4: How the CI/CD Works

### Automatic Deployments

| Branch | Trigger | Environment | Approval Required? |
|--------|---------|-------------|-------------------|
| `develop` | Push | Dev | No (automatic) |
| `main` | Push | UAT | Optional (if configured) |
| `main` | Manual or `[deploy-prod]` in commit | Production | Yes (required) |

### Workflow Behavior:

**When you push to `develop` branch:**
```bash
git checkout develop
git add .
git commit -m "Add new feature"
git push origin develop
```
→ **Automatically deploys to Dev** ✅

**When you push to `main` branch:**
```bash
git checkout main
git merge develop
git push origin main
```
→ **Automatically deploys to UAT** ✅

**When you want to deploy to Production:**

**Option 1: Manual Workflow Dispatch**
1. Go to: `https://github.com/chandrur44/Databricks-Asset-Bundles/actions`
2. Click **"Deploy Databricks Asset Bundle"**
3. Click **"Run workflow"**
4. Select `main` branch
5. Choose `prod` environment
6. Click **"Run workflow"**
7. Wait for approval (if reviewers configured)
8. Approve and deploy ✅

**Option 2: Commit Message Trigger**
```bash
git commit -m "Deploy critical fix [deploy-prod]"
git push origin main
```
→ **Triggers Production deployment** (requires approval) ✅

---

## 📋 Step 5: First Deployment Test

### Test Dev Deployment:

```bash
# 1. Make a small change
echo "# Test deployment" >> README.md

# 2. Commit to develop branch
git checkout develop
git add .
git commit -m "Test CI/CD deployment"
git push origin develop

# 3. Watch GitHub Actions
# Go to: https://github.com/chandrur44/Databricks-Asset-Bundles/actions

# 4. You should see the workflow running
# - Validate job runs first
# - Deploy-dev job runs after validation passes
```

### Monitor Deployment:

1. Go to Actions tab: `https://github.com/chandrur44/Databricks-Asset-Bundles/actions`
2. Click on the latest workflow run
3. Watch each job execute
4. Check the deployment summary at the bottom

---

## 🔄 Step 6: Workflow Details

### Jobs Execution Flow:

```
┌─────────────┐
│  Validate   │ ← Runs on all PRs and pushes
└──────┬──────┘
       │
       ├────────────────┬────────────────┐
       ▼                ▼                ▼
┌─────────────┐  ┌─────────────┐  ┌──────────────┐
│ Deploy Dev  │  │ Deploy UAT  │  │ Deploy Prod  │
│ (develop)   │  │   (main)    │  │  (manual)    │
└─────────────┘  └─────────────┘  └──────────────┘
```

### Job Conditions:

**Validate:**
- ✅ Runs on every push
- ✅ Runs on every pull request
- ✅ Validates all 3 environments

**Deploy Dev:**
- ✅ Only runs when pushing to `develop` branch
- ✅ Automatic (no approval needed)
- ✅ Uses `dev` environment

**Deploy UAT:**
- ✅ Only runs when pushing to `main` branch
- ✅ Optional approval (if configured)
- ✅ Uses `uat` environment

**Deploy Prod:**
- ✅ Only runs with manual trigger or `[deploy-prod]` in commit message
- ✅ Requires approval (if configured)
- ✅ Uses `production` environment
- ✅ Creates a git tag after successful deployment

---

## 🎯 Step 7: Best Practices

### Branch Strategy:

```
feature/* → develop → main → production
  ↓           ↓        ↓         ↓
 Local       Dev      UAT      Prod
```

**Development Flow:**
1. Create feature branch from `develop`
2. Make changes
3. Push to feature branch (validates only)
4. Create PR to `develop`
5. Merge to `develop` → Auto-deploys to Dev
6. Test in Dev
7. Create PR from `develop` to `main`
8. Merge to `main` → Auto-deploys to UAT
9. Test in UAT
10. Manual deploy to Production (with approval)

### Commit Messages:

```bash
# Regular development
git commit -m "Add data quality checks"

# Deploy to production
git commit -m "Deploy critical hotfix [deploy-prod]"

# Feature work
git commit -m "feat: Add new transformation logic"

# Bug fix
git commit -m "fix: Resolve null pointer in silver layer"
```

---

## 🛡️ Step 8: Security Best Practices

### ✅ DO:
- ✅ Use environment protection rules for UAT and Prod
- ✅ Require approvals for production deployments
- ✅ Rotate Service Principal secrets regularly
- ✅ Use separate Service Principals per environment (optional)
- ✅ Review deployment logs
- ✅ Test in Dev before promoting to UAT

### ❌ DON'T:
- ❌ Commit secrets to the repository
- ❌ Share Service Principal secrets in Slack/Email
- ❌ Skip UAT testing before production
- ❌ Deploy to production without approval
- ❌ Use the same Service Principal for all environments (not recommended)

---

## 📊 Step 9: Monitoring Deployments

### View Deployment History:

1. Go to **Actions** tab
2. Click **"Deploy Databricks Asset Bundle"**
3. See all deployment runs with status

### Check Deployment Status:

```bash
# Via GitHub CLI (optional)
gh run list --workflow=deploy.yml

# View specific run
gh run view <run-id>

# Watch live
gh run watch
```

### Deployment Summary:

After each deployment, check the workflow summary:
- Environment deployed to
- Workspace URL
- Commit SHA
- Deployed by (user)
- Timestamp

---

## 🔧 Step 10: Troubleshooting

### Issue: "Secret not found"
**Solution:**
1. Verify secret name matches exactly (case-sensitive)
2. Go to: `https://github.com/chandrur44/Databricks-Asset-Bundles/settings/secrets/actions`
3. Confirm all 5 secrets are present

### Issue: "Authentication failed"
**Solution:**
1. Verify Service Principal has Workspace Admin permissions
2. Check CLIENT_ID and CLIENT_SECRET are correct
3. Regenerate secret if needed

### Issue: "Workspace URL invalid"
**Solution:**
- AWS Databricks format: `https://xxxxx.cloud.databricks.com`
- No trailing slash
- Must be HTTPS

### Issue: "Deployment fails with 'bundle not found'"
**Solution:**
- Ensure `databricks.yml` is in repository root
- Check file is committed to git
- Verify branch is correct

### Issue: "Environment not found"
**Solution:**
1. Create environment in GitHub: Settings → Environments
2. Name must match exactly: `dev`, `uat`, `production`

---

## 🎓 Quick Reference

### Required GitHub Secrets (5):
```
DATABRICKS_DEV_HOST
DATABRICKS_UAT_HOST
DATABRICKS_PROD_HOST
DATABRICKS_CLIENT_ID
DATABRICKS_CLIENT_SECRET
```

### Required GitHub Environments (3):
```
dev
uat
production
```

### Deployment Commands:
```bash
# Deploy to Dev
git push origin develop

# Deploy to UAT
git push origin main

# Deploy to Prod (manual)
# Go to Actions → Run workflow → Select prod
```

---

## ✅ Setup Complete!

You're now ready to use automated CI/CD for your Databricks Asset Bundle!

**Next Steps:**
1. Add all 5 secrets
2. Create 3 environments
3. Update config files with your workspace URLs
4. Push to `develop` branch to test
5. Watch the magic happen! 🚀

---

**Repository**: https://github.com/chandrur44/Databricks-Asset-Bundles
