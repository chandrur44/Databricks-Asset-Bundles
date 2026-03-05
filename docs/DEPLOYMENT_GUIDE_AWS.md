# Deployment Guide - AWS Databricks

This guide walks you through deploying your Databricks Asset Bundle on **AWS Databricks**.

---

## 📋 Prerequisites Check

Before you begin, ensure you have:
- [ ] 3 AWS Databricks workspaces (Dev, UAT, Prod)
- [ ] Service Principal created in each workspace
- [ ] GitHub repository created
- [ ] Databricks CLI installed (v0.200.0+)

---

## 🚀 Step-by-Step Deployment

### **PHASE 1: Service Principal Setup (20 minutes)**

#### Step 1.1: Create Service Principal in Databricks

**Do this for EACH workspace (Dev, UAT, Prod):**

1. Open your Databricks workspace
2. Click **Settings** (gear icon) → **Admin Settings**
3. Click **Service Principals** in the left menu
4. Click **Add Service Principal** button
5. Enter a name: `dab-deployment-sp`
6. Click **Add**
7. Click on the newly created service principal
8. Click **Generate Secret** to create OAuth secret
9. **IMPORTANT**: Copy and save the secret immediately (you can't see it again!)
10. Save the **Application ID** (Client ID) and **Secret**

**What you need from each workspace:**
```
Application ID (Client ID): xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
Secret:                     dapi1234567890abcdef (or similar)
```

#### Step 1.2: Grant Permissions

For each service principal in each workspace:

1. Click on the service principal
2. Go to **Entitlements** tab
3. Enable:
   - ✅ Workspace access
   - ✅ Databricks SQL access
   - ✅ Allow cluster creation
4. Go to **Permissions** tab
5. Grant **CAN MANAGE** on workspace

**For Unity Catalog (if enabled):**
- Grant permissions on catalogs and schemas (covered in Phase 4)

---

### **PHASE 2: Local Setup (15 minutes)**

#### Step 2.1: Install Databricks CLI

```bash
# For macOS/Linux
curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh | sh

# For Windows (PowerShell as Admin)
winget install Databricks.DatabricksCLI

# Or download from: https://github.com/databricks/cli/releases

# Verify installation
databricks --version
# Should show version 0.200.0 or higher
```

#### Step 2.2: Authenticate with Dev Workspace

**Option A: OAuth (Recommended for Development)**

```bash
# Replace with your Dev workspace URL
databricks auth login --host https://xxxxx.cloud.databricks.com

# This will open a browser for OAuth authentication
# Follow the prompts to authenticate

# Verify authentication
databricks current-user me
```

**Option B: Service Principal (Recommended for CI/CD)**

Create a `.databrickscfg` file in your home directory:

**Windows:** `C:\Users\<username>\.databrickscfg`
**macOS/Linux:** `~/.databrickscfg`

```ini
[dev]
host = https://xxxxx.cloud.databricks.com
client_id = <service-principal-application-id>
client_secret = <service-principal-secret>

[uat]
host = https://yyyyy.cloud.databricks.com
client_id = <service-principal-application-id>
client_secret = <service-principal-secret>

[prod]
host = https://zzzzz.cloud.databricks.com
client_id = <service-principal-application-id>
client_secret = <service-principal-secret>
```

**⚠️ IMPORTANT:** Add `.databrickscfg` to `.gitignore` (already done)

#### Step 2.3: Navigate to DAB Project

```bash
cd "C:\Users\ChandruRames_av6qv\Downloads\New DAB"
```

---

### **PHASE 3: Configuration (20 minutes)**

#### Step 3.1: Update Environment Config Files

**Edit `config/dev.yml`:**

```yaml
variables:
  workspace_host: "https://xxxxx.cloud.databricks.com"  # ← CHANGE THIS TO YOUR DEV WORKSPACE URL
  service_principal_client_id: "${env.DATABRICKS_CLIENT_ID}"

  catalog_name: "dev_catalog"      # ← CHANGE if different
  schema_name: "dev_schema"        # ← CHANGE if different
  resource_prefix: "dev_"

  cluster_node_type: "i3.xlarge"   # ← CHANGE to your preferred AWS instance type
  cluster_autoscale_min: 1
  cluster_autoscale_max: 3

  checkpoint_location: "s3://your-bucket/dev/checkpoints"  # ← CHANGE to your S3 bucket
  data_location: "s3://your-bucket/dev/data"               # ← CHANGE to your S3 bucket
```

**Common AWS Instance Types:**
- `i3.xlarge` - 4 cores, 30.5 GB RAM (general purpose)
- `i3.2xlarge` - 8 cores, 61 GB RAM
- `r5.xlarge` - 4 cores, 32 GB RAM (memory optimized)
- `r5.2xlarge` - 8 cores, 64 GB RAM

**Edit `config/uat.yml`:**

```yaml
variables:
  workspace_host: "https://yyyyy.cloud.databricks.com"  # ← CHANGE THIS TO YOUR UAT WORKSPACE URL
  service_principal_client_id: "${env.DATABRICKS_CLIENT_ID}"

  catalog_name: "uat_catalog"
  schema_name: "uat_schema"
  resource_prefix: "uat_"

  cluster_node_type: "i3.xlarge"
  cluster_autoscale_min: 2
  cluster_autoscale_max: 5

  checkpoint_location: "s3://your-bucket/uat/checkpoints"
  data_location: "s3://your-bucket/uat/data"
```

**Edit `config/prod.yml`:**

```yaml
variables:
  workspace_host: "https://zzzzz.cloud.databricks.com"  # ← CHANGE THIS TO YOUR PROD WORKSPACE URL
  service_principal_client_id: "${env.DATABRICKS_CLIENT_ID}"

  catalog_name: "prod_catalog"
  schema_name: "prod_schema"
  resource_prefix: "prod_"

  cluster_node_type: "i3.2xlarge"  # Larger for production
  cluster_autoscale_min: 2
  cluster_autoscale_max: 10

  checkpoint_location: "s3://your-bucket/prod/checkpoints"
  data_location: "s3://your-bucket/prod/data"
```

#### Step 3.2: Update databricks.yml

**Edit the main `databricks.yml` file:**

Find the `targets` section and update the `run_as` configuration:

```yaml
targets:
  dev:
    mode: development
    default: true
    workspace:
      host: ${var.workspace_host}
    run_as:
      service_principal_name: ${var.service_principal_client_id}  # ← This is correct for AWS

  uat:
    mode: development
    workspace:
      host: ${var.workspace_host}
    run_as:
      service_principal_name: ${var.service_principal_client_id}

  prod:
    mode: production
    workspace:
      host: ${var.workspace_host}
    run_as:
      service_principal_name: ${var.service_principal_client_id}
```

#### Step 3.3: Update Email Notifications (Optional)

**Edit `resources/jobs.yml`:**

```yaml
email_notifications:
  on_failure:
    - your-data-team@company.com    # ← CHANGE THIS
  on_success:
    - your-data-team@company.com    # ← CHANGE THIS
```

#### Step 3.4: Set Environment Variables

**For Windows (PowerShell):**
```powershell
$env:DATABRICKS_CLIENT_ID="<service-principal-application-id>"
$env:DATABRICKS_CLIENT_SECRET="<service-principal-secret>"
```

**For macOS/Linux (Bash):**
```bash
export DATABRICKS_CLIENT_ID="<service-principal-application-id>"
export DATABRICKS_CLIENT_SECRET="<service-principal-secret>"
```

**Note:** For AWS Databricks, you **don't need** `DATABRICKS_TENANT_ID`

---

### **PHASE 4: Unity Catalog Setup (Optional but Recommended - 20 minutes)**

#### Step 4.1: Create Catalogs and Schemas

**In Dev Workspace SQL Editor:**
```sql
CREATE CATALOG IF NOT EXISTS dev_catalog;
CREATE SCHEMA IF NOT EXISTS dev_catalog.dev_schema;

-- Grant permissions to Service Principal
GRANT ALL PRIVILEGES ON CATALOG dev_catalog TO `<service-principal-application-id>`;
GRANT ALL PRIVILEGES ON SCHEMA dev_catalog.dev_schema TO `<service-principal-application-id>`;
```

**In UAT Workspace:**
```sql
CREATE CATALOG IF NOT EXISTS uat_catalog;
CREATE SCHEMA IF NOT EXISTS uat_catalog.uat_schema;

GRANT ALL PRIVILEGES ON CATALOG uat_catalog TO `<service-principal-application-id>`;
GRANT ALL PRIVILEGES ON SCHEMA uat_catalog.uat_schema TO `<service-principal-application-id>`;
```

**In Prod Workspace:**
```sql
CREATE CATALOG IF NOT EXISTS prod_catalog;
CREATE SCHEMA IF NOT EXISTS prod_catalog.prod_schema;

GRANT ALL PRIVILEGES ON CATALOG prod_catalog TO `<service-principal-application-id>`;
GRANT ALL PRIVILEGES ON SCHEMA prod_catalog.prod_schema TO `<service-principal-application-id>`;
```

**If you don't have Unity Catalog:**
Update your config files to use the default metastore:
```yaml
catalog_name: "hive_metastore"
schema_name: "default"
```

---

### **PHASE 5: S3 Bucket Setup (Optional but Recommended - 15 minutes)**

#### Step 5.1: Create S3 Buckets

```bash
# Create S3 bucket (or use existing)
aws s3 mb s3://your-databricks-data-bucket

# Create folder structure
aws s3api put-object --bucket your-databricks-data-bucket --key dev/
aws s3api put-object --bucket your-databricks-data-bucket --key uat/
aws s3api put-object --bucket your-databricks-data-bucket --key prod/
```

#### Step 5.2: Configure Instance Profile (Optional)

For production, configure an instance profile to allow Databricks clusters to access S3:

1. Create IAM role with S3 access
2. Attach to Databricks instance profile
3. Update cluster configuration to use instance profile

**Or use direct S3 access with credentials in cluster config**

---

### **PHASE 6: First Deployment to Dev (15 minutes)**

#### Step 6.1: Validate Configuration

```bash
cd "C:\Users\ChandruRames_av6qv\Downloads\New DAB"

# Validate the configuration
databricks bundle validate -t dev
```

**Expected output:**
```
✓ Configuration is valid
```

**If you see errors:**
- Check workspace URL format (`https://xxxxx.cloud.databricks.com`)
- Verify service principal has permissions
- Check catalog/schema names exist

#### Step 6.2: Deploy to Dev

```bash
# Deploy all resources to Dev environment
databricks bundle deploy -t dev
```

**Expected output:**
```
Uploading artifacts...
Deploying resources...
✓ Jobs deployed
✓ Pipelines deployed
✓ Queries deployed
Deployment complete!
```

#### Step 6.3: Verify Deployment

**Check in Databricks UI:**
1. Open your Dev workspace
2. Go to **Workflows** → You should see:
   - `dev_sample_etl_job`
   - `dev_data_quality_job`
   - `dev_sql_query_job`
3. Go to **Delta Live Tables** → You should see:
   - `dev_sample_dlt_pipeline`
   - `dev_streaming_dlt_pipeline`

**Or check via CLI:**
```bash
databricks bundle list -t dev
```

---

### **PHASE 7: Test Your Deployment (15 minutes)**

#### Step 7.1: Run a Sample Job

```bash
# Run the sample ETL job
databricks bundle run sample_etl_job -t dev
```

**Note:** The job may fail initially if you don't have sample data in S3. This is expected!

#### Step 7.2: Verify in UI

1. Go to **Workflows** → **dev_sample_etl_job** → **Runs**
2. Click on the latest run
3. Check the execution flow

---

### **PHASE 8: Deploy to UAT and Prod (10 minutes each)**

```bash
# Deploy to UAT
databricks bundle deploy -t uat

# Deploy to Prod
databricks bundle deploy -t prod
```

---

### **PHASE 9: Setup GitHub CI/CD (30 minutes)**

#### Step 9.1: Add GitHub Secrets

Go to your GitHub repository → **Settings** → **Secrets and variables** → **Actions**

Add these secrets:

| Secret Name | Value | Example |
|-------------|-------|---------|
| `DATABRICKS_DEV_HOST` | `https://xxxxx.cloud.databricks.com` | Dev workspace URL |
| `DATABRICKS_UAT_HOST` | `https://yyyyy.cloud.databricks.com` | UAT workspace URL |
| `DATABRICKS_PROD_HOST` | `https://zzzzz.cloud.databricks.com` | Prod workspace URL |
| `DATABRICKS_CLIENT_ID` | `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` | Service Principal Application ID |
| `DATABRICKS_CLIENT_SECRET` | `dapixxxxxxxxxxxx` | Service Principal Secret |

**Note:** AWS Databricks doesn't need `DATABRICKS_TENANT_ID`

#### Step 9.2: Create GitHub Actions Workflow

**Create `.github/workflows/deploy.yml`:**

```yaml
name: Deploy DAB to AWS Databricks

on:
  push:
    branches:
      - main
      - develop
  pull_request:
    branches:
      - main

jobs:
  deploy-dev:
    name: Deploy to Dev
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/develop'

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Install Databricks CLI
        run: |
          curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh | sh
          databricks --version

      - name: Deploy to Dev
        env:
          DATABRICKS_HOST: ${{ secrets.DATABRICKS_DEV_HOST }}
          DATABRICKS_CLIENT_ID: ${{ secrets.DATABRICKS_CLIENT_ID }}
          DATABRICKS_CLIENT_SECRET: ${{ secrets.DATABRICKS_CLIENT_SECRET }}
        run: |
          databricks bundle deploy -t dev

  deploy-uat:
    name: Deploy to UAT
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Install Databricks CLI
        run: |
          curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh | sh

      - name: Deploy to UAT
        env:
          DATABRICKS_HOST: ${{ secrets.DATABRICKS_UAT_HOST }}
          DATABRICKS_CLIENT_ID: ${{ secrets.DATABRICKS_CLIENT_ID }}
          DATABRICKS_CLIENT_SECRET: ${{ secrets.DATABRICKS_CLIENT_SECRET }}
        run: |
          databricks bundle deploy -t uat

  deploy-prod:
    name: Deploy to Prod (Manual)
    runs-on: ubuntu-latest
    if: github.event_name == 'workflow_dispatch'
    environment: production

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Install Databricks CLI
        run: |
          curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh | sh

      - name: Deploy to Production
        env:
          DATABRICKS_HOST: ${{ secrets.DATABRICKS_PROD_HOST }}
          DATABRICKS_CLIENT_ID: ${{ secrets.DATABRICKS_CLIENT_ID }}
          DATABRICKS_CLIENT_SECRET: ${{ secrets.DATABRICKS_CLIENT_SECRET }}
        run: |
          databricks bundle deploy -t prod
```

---

## ✅ Deployment Complete!

You should now have:
- ✅ Service Principals created in all workspaces
- ✅ DAB deployed to Dev, UAT, Prod
- ✅ CI/CD pipeline set up in GitHub
- ✅ Jobs and pipelines running

---

## 🔧 Troubleshooting

### Error: "Service Principal not found"
**Solution:** Create Service Principal in workspace → Admin Settings → Service Principals

### Error: "Catalog does not exist"
**Solution:** Create catalog or update config to use `hive_metastore.default`

### Error: "Permission denied"
**Solution:**
- Grant Service Principal workspace access
- Grant CAN MANAGE permissions
- Grant catalog/schema permissions

### Error: "Invalid workspace URL"
**Solution:** Use format `https://xxxxx.cloud.databricks.com` (no trailing slash)

### Error: "S3 access denied"
**Solution:** Configure instance profile or S3 credentials

---

## 📊 Key Differences: AWS vs Azure Databricks

| Aspect | AWS Databricks | Azure Databricks |
|--------|----------------|------------------|
| **Workspace URL** | `https://xxxxx.cloud.databricks.com` | `https://adb-xxx.azuredatabricks.net` |
| **Authentication** | Service Principal (OAuth) | Service Principal (Azure AD) |
| **Storage** | S3 (`s3://bucket/path`) | ADLS (`abfss://`) or Blob |
| **Instance Types** | AWS EC2 (i3.xlarge, r5.xlarge) | Azure VMs (Standard_DS3_v2) |
| **Tenant ID** | Not needed | Required for Azure AD |
| **IAM** | AWS IAM roles | Azure AD & RBAC |

---

## 🎉 Next Steps

1. Add your actual data sources (S3 buckets)
2. Customize notebooks with your data pipelines
3. Set up S3 mounts or instance profiles
4. Configure job schedules
5. Create Databricks SQL dashboards
6. Monitor job runs and set up alerts

---

**Your AWS Databricks DAB is now deployed! 🚀**
