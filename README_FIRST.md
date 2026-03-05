# 🚀 Databricks Asset Bundle - AWS Databricks

Welcome! This is a complete Databricks Asset Bundle configured for **AWS Databricks**.

---

## 📖 Documentation Guide

### **👉 Start Here:**
**[START_HERE_AWS.md](START_HERE_AWS.md)** - Main navigation guide

### **Quick Deployment:**
**[QUICK_START_AWS.md](QUICK_START_AWS.md)** - 10 steps to deploy (35 minutes)

### **Detailed Guide:**
**[DEPLOYMENT_GUIDE_AWS.md](DEPLOYMENT_GUIDE_AWS.md)** - Complete deployment instructions

### **Setup Summary:**
**[AWS_DATABRICKS_SETUP.md](AWS_DATABRICKS_SETUP.md)** - What's configured and how to deploy

### **Reference:**
- **[README.md](README.md)** - Full project documentation
- **[PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)** - Project structure and architecture

---

## ⚡ Quick Start

```bash
# 1. Update config files with your workspace URLs
vim config/dev.yml
vim config/uat.yml
vim config/prod.yml

# 2. Set environment variables
export DATABRICKS_CLIENT_ID="your-app-id"
export DATABRICKS_CLIENT_SECRET="your-secret"

# 3. Deploy
databricks bundle validate -t dev
databricks bundle deploy -t dev
```

---

## 📋 What You Need

1. ✅ 3 AWS Databricks workspaces (Dev, UAT, Prod)
2. ✅ Service Principal in each workspace
3. ✅ Databricks CLI (v0.200.0+)
4. ✅ Config files updated
5. ✅ S3 bucket (recommended)

---

## 🎯 Key Points for AWS Databricks

- **Workspace URL**: `https://xxxxx.cloud.databricks.com`
- **Instance Types**: `i3.xlarge`, `i3.2xlarge` (EC2)
- **Storage**: S3 (`s3://bucket/path`)
- **No Tenant ID** needed (unlike Azure)
- **Service Principal** created in Databricks UI (not AWS IAM)

---

**Ready to deploy? → [START_HERE_AWS.md](START_HERE_AWS.md) 🚀**
