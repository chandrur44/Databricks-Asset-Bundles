# Quick Start - Deploy to AWS Databricks in 10 Steps

Follow these 10 steps to deploy your DAB to **AWS Databricks**.

---

## ✅ Step-by-Step Checklist

### ☐ **Step 1: Create Service Principal in Databricks** (5 minutes)

**In EACH workspace (Dev, UAT, Prod):**

1. Open workspace → **Settings** → **Admin Settings**
2. Click **Service Principals** → **Add Service Principal**
3. Name: `dab-deployment-sp`
4. Click on the service principal → **Generate Secret**
5. **Copy and save immediately**: Application ID + Secret

```
Application ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
Secret:         dapixxxxxxxxxxxxxxxxxxxx
```

Grant permissions:
- ✅ Workspace access
- ✅ Allow cluster creation
- ✅ CAN MANAGE on workspace

---

### ☐ **Step 2: Install Databricks CLI** (2 minutes)

```bash
curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh | sh
databricks --version  # Should be 0.200.0+
```

---

### ☐ **Step 3: Authenticate** (2 minutes)

```bash
databricks auth login --host https://xxxxx.cloud.databricks.com
```

---

### ☐ **Step 4: Update Config Files** (5 minutes)

**Edit `config/dev.yml`:**
```yaml
workspace_host: "https://xxxxx.cloud.databricks.com"      # Your Dev workspace
cluster_node_type: "i3.xlarge"                             # AWS instance type
checkpoint_location: "s3://your-bucket/dev/checkpoints"    # Your S3 bucket
data_location: "s3://your-bucket/dev/data"
```

**Edit `config/uat.yml`:**
```yaml
workspace_host: "https://yyyyy.cloud.databricks.com"      # Your UAT workspace
cluster_node_type: "i3.xlarge"
checkpoint_location: "s3://your-bucket/uat/checkpoints"
data_location: "s3://your-bucket/uat/data"
```

**Edit `config/prod.yml`:**
```yaml
workspace_host: "https://zzzzz.cloud.databricks.com"      # Your Prod workspace
cluster_node_type: "i3.2xlarge"                            # Larger for prod
checkpoint_location: "s3://your-bucket/prod/checkpoints"
data_location: "s3://your-bucket/prod/data"
```

---

### ☐ **Step 5: Set Environment Variables** (1 minute)

**Windows (PowerShell):**
```powershell
$env:DATABRICKS_CLIENT_ID="your-service-principal-app-id"
$env:DATABRICKS_CLIENT_SECRET="your-service-principal-secret"
```

**macOS/Linux:**
```bash
export DATABRICKS_CLIENT_ID="your-service-principal-app-id"
export DATABRICKS_CLIENT_SECRET="your-service-principal-secret"
```

**Note:** AWS Databricks doesn't need `DATABRICKS_TENANT_ID`

---

### ☐ **Step 6: Create Catalogs (Optional)** (5 minutes)

**In each workspace SQL Editor:**
```sql
CREATE CATALOG IF NOT EXISTS dev_catalog;  -- or uat_catalog, prod_catalog
CREATE SCHEMA IF NOT EXISTS dev_catalog.dev_schema;

-- Grant permissions
GRANT ALL PRIVILEGES ON CATALOG dev_catalog TO `<service-principal-app-id>`;
```

**Skip if you don't have Unity Catalog** - use `hive_metastore.default`

---

### ☐ **Step 7: Setup S3 Bucket (Optional)** (5 minutes)

```bash
# Create or use existing S3 bucket
aws s3 mb s3://your-databricks-data-bucket

# Update config files with your bucket name
```

---

### ☐ **Step 8: Validate Configuration** (1 minute)

```bash
cd "C:\Users\ChandruRames_av6qv\Downloads\New DAB"
databricks bundle validate -t dev
```

Should show: `✓ Configuration is valid`

---

### ☐ **Step 9: Deploy to Dev** (3 minutes)

```bash
databricks bundle deploy -t dev
```

Should show: `✓ Deployment complete!`

---

### ☐ **Step 10: Test Your Deployment** (5 minutes)

```bash
# Run a sample job
databricks bundle run sample_etl_job -t dev

# Check deployed resources
databricks bundle list -t dev
```

**Or check in Databricks UI:**
- Go to **Workflows** → See `dev_sample_etl_job`
- Go to **Delta Live Tables** → See `dev_sample_dlt_pipeline`

---

## 🎉 Success!

Your DAB is now deployed to Dev!

### Next Steps:

```bash
# Deploy to UAT
databricks bundle deploy -t uat

# Deploy to Prod
databricks bundle deploy -t prod
```

---

## 🔧 Quick Troubleshooting

| Error | Fix |
|-------|-----|
| "Service Principal not found" | Create SP in workspace Admin Settings |
| "Catalog does not exist" | Create catalog or use `hive_metastore.default` |
| "Permission denied" | Grant SP workspace access and CAN MANAGE role |
| "Invalid workspace URL" | Use format `https://xxxxx.cloud.databricks.com` (no trailing slash) |
| "S3 access denied" | Configure instance profile or S3 credentials |

---

## 🆚 AWS vs Azure Databricks Differences

| Aspect | AWS | Azure |
|--------|-----|-------|
| **Workspace URL** | `https://xxxxx.cloud.databricks.com` | `https://adb-xxx.azuredatabricks.net` |
| **Storage** | S3 (`s3://bucket/path`) | ADLS/Blob (`abfss://` or `dbfs://`) |
| **Instance Types** | AWS EC2 (i3.xlarge, r5.xlarge) | Azure VMs (Standard_DS3_v2) |
| **Tenant ID** | ❌ Not needed | ✅ Required |
| **Auth** | Service Principal (OAuth) | Service Principal (Azure AD) |

---

## 📚 More Help

- **Detailed guide**: [DEPLOYMENT_GUIDE_AWS.md](./DEPLOYMENT_GUIDE_AWS.md)
- **Requirements**: [QUICK_REQUIREMENTS.md](./QUICK_REQUIREMENTS.md)
- **Full docs**: [README.md](./README.md)

---

##**Total Time: ~35 minutes** ⏱️
