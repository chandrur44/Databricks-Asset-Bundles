# 🚀 START HERE - AWS Databricks DAB Deployment

Welcome! This project is configured for **AWS Databricks**.

---

## 📖 Quick Navigation

### **⚡ Want to Deploy Right Now?**
**👉 Go to: [QUICK_START_AWS.md](QUICK_START_AWS.md)**
- 10 simple steps
- 35 minutes to deploy
- Perfect for getting started fast

### **📚 Need Detailed Instructions?**
**👉 Go to: [DEPLOYMENT_GUIDE_AWS.md](DEPLOYMENT_GUIDE_AWS.md)**
- Complete phase-by-phase guide
- Troubleshooting included
- CI/CD setup instructions

### **✅ What Do I Need?**
**👉 Check: [QUICK_REQUIREMENTS.md](QUICK_REQUIREMENTS.md)**
- One-page requirements list
- Quick checklist

---

## 🔑 Key Requirements for AWS Databricks

### **Must Have:**
1. ✅ **3 AWS Databricks workspaces** (Dev, UAT, Prod)
   - Format: `https://xxxxx.cloud.databricks.com`

2. ✅ **Service Principal in each workspace**
   - Created in Databricks (not AWS IAM)
   - Application ID + Secret

3. ✅ **Databricks CLI** (v0.200.0+)
   ```bash
   curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh | sh
   ```

4. ✅ **Config files updated**
   - `config/dev.yml` - workspace URL + S3 bucket
   - `config/uat.yml` - workspace URL + S3 bucket
   - `config/prod.yml` - workspace URL + S3 bucket

5. ✅ **Environment variables**
   ```bash
   export DATABRICKS_CLIENT_ID="xxx"
   export DATABRICKS_CLIENT_SECRET="xxx"
   # NO TENANT_ID needed for AWS!
   ```

### **Recommended:**
- Unity Catalog catalogs/schemas
- S3 bucket for data storage
- GitHub repository for CI/CD

---

## 🆚 AWS vs Azure Databricks - Key Differences

| What | AWS Databricks | Azure Databricks |
|------|----------------|------------------|
| **Workspace URL** | `https://xxxxx.cloud.databricks.com` | `https://adb-xxx.azuredatabricks.net` |
| **Service Principal** | Created in Databricks UI | Created in Azure AD |
| **Storage** | S3: `s3://bucket/path` | ADLS/Blob: `abfss://` or `dbfs://` |
| **Instance Types** | EC2: `i3.xlarge`, `r5.xlarge` | VMs: `Standard_DS3_v2` |
| **Tenant ID** | ❌ Not needed | ✅ Required |
| **Authentication** | OAuth tokens | Azure AD |

---

## 📁 Config Files Already Updated for AWS

✅ **config/dev.yml** - Uses `i3.xlarge` + S3 paths
✅ **config/uat.yml** - Uses `i3.xlarge` + S3 paths
✅ **config/prod.yml** - Uses `i3.2xlarge` + S3 paths

**You just need to:**
1. Update workspace URLs
2. Update S3 bucket names
3. Update catalog names (if different)

---

## ⚡ Super Quick Deployment

```bash
# 1. Create Service Principal in each Databricks workspace
#    Settings → Admin Settings → Service Principals → Add

# 2. Update config files
vim config/dev.yml    # Update workspace_host and S3 bucket
vim config/uat.yml    # Update workspace_host and S3 bucket
vim config/prod.yml   # Update workspace_host and S3 bucket

# 3. Set environment variables
export DATABRICKS_CLIENT_ID="your-app-id"
export DATABRICKS_CLIENT_SECRET="your-secret"

# 4. Deploy!
databricks bundle validate -t dev
databricks bundle deploy -t dev
databricks bundle run sample_etl_job -t dev
```

---

## 📚 All Documentation

| Document | Purpose | When to Use |
|----------|---------|-------------|
| **[QUICK_START_AWS.md](QUICK_START_AWS.md)** | ⚡ 10-step deployment | Deploy now! |
| **[DEPLOYMENT_GUIDE_AWS.md](DEPLOYMENT_GUIDE_AWS.md)** | 📖 Complete guide | Need details |
| **[QUICK_REQUIREMENTS.md](QUICK_REQUIREMENTS.md)** | ✅ Requirements | What do I need? |
| **[README.md](README.md)** | 📚 Full documentation | Reference |
| **[PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)** | 🗺️ Architecture | Understand structure |

---

## 🎯 Your Next Action

**👉 Open: [QUICK_START_AWS.md](QUICK_START_AWS.md)**

Follow the 10 steps and you'll have your DAB deployed to AWS Databricks in 35 minutes!

---

## 💡 Common AWS Databricks Instance Types

| Instance Type | vCPUs | Memory | Use Case |
|---------------|-------|--------|----------|
| **i3.xlarge** | 4 | 30.5 GB | Dev, small workloads |
| **i3.2xlarge** | 8 | 61 GB | Production, medium workloads |
| **r5.xlarge** | 4 | 32 GB | Memory-intensive |
| **r5.2xlarge** | 8 | 64 GB | Large memory workloads |
| **m5.xlarge** | 4 | 16 GB | General purpose |
| **m5.2xlarge** | 8 | 32 GB | Balanced workloads |

---

## 📦 What Gets Deployed

When you run `databricks bundle deploy -t dev`:

✅ **3 Workflow Jobs**
- `dev_sample_etl_job` (Bronze → Silver → Gold)
- `dev_data_quality_job`
- `dev_sql_query_job`

✅ **2 DLT Pipelines**
- `dev_sample_dlt_pipeline`
- `dev_streaming_dlt_pipeline`

✅ **8 Notebooks** uploaded
✅ **3 SQL Queries** registered

---

## 🔧 GitHub CI/CD Setup

Add these secrets to your GitHub repository:

```
DATABRICKS_DEV_HOST       = https://xxxxx.cloud.databricks.com
DATABRICKS_UAT_HOST       = https://yyyyy.cloud.databricks.com
DATABRICKS_PROD_HOST      = https://zzzzz.cloud.databricks.com
DATABRICKS_CLIENT_ID      = <service-principal-app-id>
DATABRICKS_CLIENT_SECRET  = <service-principal-secret>
```

**Note:** NO `DATABRICKS_TENANT_ID` needed for AWS!

---

## ❓ FAQ

### Q: Do I need AWS IAM roles?
**A:** No! Service Principals are created in Databricks, not AWS IAM.

### Q: How do I give clusters access to S3?
**A:** Either:
- Configure instance profile with IAM role
- Use S3 access keys in cluster config
- Use Unity Catalog external locations

### Q: What about data mounts?
**A:** You can still mount S3 buckets to DBFS if needed, but Unity Catalog external locations are recommended.

### Q: Can I use the same Service Principal for all environments?
**A:** Yes, but it's more secure to create separate ones for each environment.

---

## 🆘 Quick Help

| Problem | Solution |
|---------|----------|
| "Invalid workspace URL" | Use `https://xxxxx.cloud.databricks.com` format |
| "Service Principal not found" | Create in Databricks UI, not AWS IAM |
| "S3 access denied" | Configure instance profile or credentials |
| "Catalog doesn't exist" | Create in SQL Editor or use `hive_metastore.default` |

---

**Ready to deploy? Start here: [QUICK_START_AWS.md](QUICK_START_AWS.md) 🚀**
