# AWS Databricks - Updated Configuration Summary

Your DAB project has been **updated for AWS Databricks**. Here's what changed and how to deploy.

---

## ✅ What's Been Updated

### **1. Config Files** (`config/*.yml`)
✅ **Workspace URLs changed:**
- From: `https://adb-xxx.azuredatabricks.net` (Azure)
- To: `https://xxxxx.cloud.databricks.com` (AWS)

✅ **Instance types changed:**
- From: `Standard_DS3_v2` (Azure VMs)
- To: `i3.xlarge`, `i3.2xlarge` (AWS EC2)

✅ **Storage paths changed:**
- From: `dbfs:/mnt/dev/` (Azure mounts)
- To: `s3://your-bucket/dev/` (S3 buckets)

### **2. Documentation Created**
✅ **[DEPLOYMENT_GUIDE_AWS.md](DEPLOYMENT_GUIDE_AWS.md)** - Complete AWS deployment guide
✅ **[QUICK_START_AWS.md](QUICK_START_AWS.md)** - 10-step quick start for AWS
✅ **[START_HERE_AWS.md](START_HERE_AWS.md)** - AWS-specific navigation

### **3. Authentication Simplified**
✅ **No Azure Tenant ID needed** for AWS
✅ **Service Principals created in Databricks** (not AWS IAM)

---

## 🚀 How to Deploy to AWS Databricks

### **Step 1: Create Service Principal in Databricks**

**In each workspace (Dev, UAT, Prod):**

1. Go to **Settings** → **Admin Settings** → **Service Principals**
2. Click **Add Service Principal**
3. Name: `dab-deployment-sp`
4. Click **Generate Secret**
5. Save the **Application ID** and **Secret**

### **Step 2: Update Config Files**

**`config/dev.yml`:**
```yaml
workspace_host: "https://xxxxx.cloud.databricks.com"  # Your Dev workspace
checkpoint_location: "s3://your-bucket/dev/checkpoints"
data_location: "s3://your-bucket/dev/data"
```

**`config/uat.yml`:**
```yaml
workspace_host: "https://yyyyy.cloud.databricks.com"  # Your UAT workspace
checkpoint_location: "s3://your-bucket/uat/checkpoints"
data_location: "s3://your-bucket/uat/data"
```

**`config/prod.yml`:**
```yaml
workspace_host: "https://zzzzz.cloud.databricks.com"  # Your Prod workspace
checkpoint_location: "s3://your-bucket/prod/checkpoints"
data_location: "s3://your-bucket/prod/data"
```

### **Step 3: Set Environment Variables**

```bash
# Windows PowerShell
$env:DATABRICKS_CLIENT_ID="your-application-id"
$env:DATABRICKS_CLIENT_SECRET="your-secret"

# macOS/Linux
export DATABRICKS_CLIENT_ID="your-application-id"
export DATABRICKS_CLIENT_SECRET="your-secret"
```

**Note:** No `DATABRICKS_TENANT_ID` needed for AWS!

### **Step 4: Deploy**

```bash
# Validate
databricks bundle validate -t dev

# Deploy
databricks bundle deploy -t dev

# Test
databricks bundle run sample_etl_job -t dev
```

---

## 📋 Complete Requirements for AWS Databricks

### **Critical (Must Have):**

1. ✅ **3 AWS Databricks Workspaces**
   - Dev, UAT, Production
   - URLs like: `https://xxxxx.cloud.databricks.com`

2. ✅ **Service Principal per Workspace**
   - Created in Databricks UI (not AWS IAM)
   - Application ID + Secret
   - Workspace Admin permissions

3. ✅ **Databricks CLI** (v0.200.0+)
   ```bash
   curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh | sh
   ```

4. ✅ **GitHub Repository**
   - For version control and CI/CD

5. ✅ **5 GitHub Secrets** (not 6!)
   - `DATABRICKS_DEV_HOST`
   - `DATABRICKS_UAT_HOST`
   - `DATABRICKS_PROD_HOST`
   - `DATABRICKS_CLIENT_ID`
   - `DATABRICKS_CLIENT_SECRET`
   - ❌ NO `DATABRICKS_TENANT_ID` needed!

### **Recommended:**

6. ✅ **Unity Catalog**
   - Catalogs: `dev_catalog`, `uat_catalog`, `prod_catalog`
   - Schemas: `dev_schema`, `uat_schema`, `prod_schema`

7. ✅ **S3 Bucket**
   - For data storage: `s3://your-databricks-data`
   - Folders: `dev/`, `uat/`, `prod/`

---

## 🆚 AWS vs Azure: What Changed

| Aspect | Azure Databricks | AWS Databricks |
|--------|------------------|----------------|
| **Workspace URL** | `https://adb-xxx.azuredatabricks.net` | `https://xxxxx.cloud.databricks.com` |
| **Service Principal** | Azure AD | Databricks-native OAuth |
| **Tenant ID** | ✅ Required | ❌ Not needed |
| **Storage** | Azure Storage, ADLS | S3 |
| **Storage Paths** | `abfss://` or `dbfs:/mnt/` | `s3://bucket/path` |
| **Instance Types** | `Standard_DS3_v2` (Azure VM) | `i3.xlarge` (EC2) |
| **CLI Commands** | `az ad sp create-for-rbac` | Create in Databricks UI |
| **GitHub Secrets** | 6 secrets | 5 secrets (no tenant ID) |

---

## 📁 Files Modified

### **Updated:**
- ✅ `config/dev.yml` - AWS workspace URL, EC2 instances, S3 paths
- ✅ `config/uat.yml` - AWS workspace URL, EC2 instances, S3 paths
- ✅ `config/prod.yml` - AWS workspace URL, EC2 instances, S3 paths

### **Created:**
- ✅ `DEPLOYMENT_GUIDE_AWS.md` - Complete AWS deployment guide
- ✅ `QUICK_START_AWS.md` - 10-step AWS quick start
- ✅ `START_HERE_AWS.md` - AWS navigation guide
- ✅ `AWS_DATABRICKS_SETUP.md` - This file

### **Original Files (for reference):**
- 📄 `DEPLOYMENT_GUIDE.md` - Azure version (kept for reference)
- 📄 `QUICK_START.md` - Azure version (kept for reference)
- 📄 `START_HERE.md` - Azure version (kept for reference)

---

## 🎯 Your Next Steps

### **Quick Deployment (35 minutes):**
1. **Read:** [QUICK_START_AWS.md](QUICK_START_AWS.md)
2. **Follow the 10 steps**
3. **Deploy!**

### **Detailed Setup:**
1. **Read:** [START_HERE_AWS.md](START_HERE_AWS.md)
2. **Follow:** [DEPLOYMENT_GUIDE_AWS.md](DEPLOYMENT_GUIDE_AWS.md)
3. **Deploy!**

---

## 💡 AWS Databricks-Specific Tips

### **Instance Types:**
```yaml
# Development
cluster_node_type: "i3.xlarge"     # 4 cores, 30.5 GB RAM

# Production
cluster_node_type: "i3.2xlarge"    # 8 cores, 61 GB RAM

# Memory-intensive
cluster_node_type: "r5.2xlarge"    # 8 cores, 64 GB RAM

# General purpose
cluster_node_type: "m5.2xlarge"    # 8 cores, 32 GB RAM
```

### **S3 Access:**
```python
# Option 1: Use instance profile (recommended)
# Configure in cluster settings

# Option 2: Direct S3 access
spark.read.parquet("s3://bucket/path")

# Option 3: Unity Catalog external location
CREATE EXTERNAL LOCATION s3_data
URL 's3://your-bucket/data'
STORAGE CREDENTIAL aws_credential;
```

### **Unity Catalog:**
```sql
-- Create catalog
CREATE CATALOG IF NOT EXISTS dev_catalog;

-- Grant to Service Principal
GRANT ALL PRIVILEGES ON CATALOG dev_catalog
TO `<service-principal-application-id>`;
```

---

## 🔧 Common AWS Databricks Issues

### Issue: "Cannot create Service Principal"
**Solution:** You must be a workspace admin. Go to Admin Settings → Service Principals.

### Issue: "S3 access denied"
**Solution:**
- Option 1: Configure instance profile with S3 permissions
- Option 2: Add S3 credentials to cluster config
- Option 3: Use Unity Catalog external locations

### Issue: "Wrong workspace URL format"
**Solution:** AWS uses `https://xxxxx.cloud.databricks.com`, not Azure's `adb-xxx.azuredatabricks.net`

### Issue: "Tenant ID error"
**Solution:** AWS Databricks doesn't use Tenant IDs. Remove `DATABRICKS_TENANT_ID` from environment variables.

---

## 📞 Need Help?

- **Quick Start:** [QUICK_START_AWS.md](QUICK_START_AWS.md)
- **Detailed Guide:** [DEPLOYMENT_GUIDE_AWS.md](DEPLOYMENT_GUIDE_AWS.md)
- **Navigation:** [START_HERE_AWS.md](START_HERE_AWS.md)
- **Full Docs:** [README.md](README.md)

---

## ✅ Pre-Deployment Checklist

```
AWS Databricks Workspaces:
[ ] Dev workspace URL saved
[ ] UAT workspace URL saved
[ ] Prod workspace URL saved

Service Principals:
[ ] Created in Dev workspace
[ ] Created in UAT workspace
[ ] Created in Prod workspace
[ ] Application IDs saved
[ ] Secrets saved
[ ] Granted Workspace Admin permissions

Configuration:
[ ] config/dev.yml updated with workspace URL
[ ] config/uat.yml updated with workspace URL
[ ] config/prod.yml updated with workspace URL
[ ] S3 bucket names updated in all configs
[ ] Environment variables set (CLIENT_ID, CLIENT_SECRET)

Tools:
[ ] Databricks CLI installed (v0.200.0+)
[ ] Authenticated with dev workspace
[ ] GitHub repository created (optional)

Optional:
[ ] Unity Catalog catalogs created
[ ] S3 bucket created
[ ] Instance profile configured (for S3 access)
```

---

**Ready to deploy? → [QUICK_START_AWS.md](QUICK_START_AWS.md) 🚀**
