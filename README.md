# Databricks Asset Bundle - AWS Databricks

Complete Databricks Asset Bundle (DAB) with automated CI/CD for AWS Databricks.

**Repository**: https://github.com/chandrur44/Databricks-Asset-Bundles

---

## 🚀 Quick Start

### **New to this project?**
**👉 Start here: [docs/README_FIRST.md](docs/README_FIRST.md)**

### **Want to deploy quickly?**
**👉 Follow: [docs/QUICK_START_AWS.md](docs/QUICK_START_AWS.md)** (10 steps, 35 minutes)

### **Setting up GitHub CI/CD?**
**👉 Read: [docs/GITHUB_QUICK_SETUP.md](docs/GITHUB_QUICK_SETUP.md)** (Quick checklist)

---

## 📋 What This Project Provides

✅ **Multi-environment support** - Dev, UAT, Production
✅ **Automated CI/CD** - GitHub Actions workflow included
✅ **Complete DAB structure** - Jobs, notebooks, DLT pipelines, SQL queries
✅ **AWS Databricks optimized** - S3 storage, EC2 instances
✅ **Fully dynamic** - Configure via GitHub secrets
✅ **Starter templates** - Sample notebooks and jobs ready to customize

---

## 📁 Project Structure

```
.
├── databricks.yml              # Main DAB configuration
├── .github/workflows/          # GitHub Actions CI/CD
├── config/                     # Environment configs (dev, uat, prod)
├── resources/                  # Jobs, pipelines, queries
├── src/
│   ├── notebooks/             # Python notebooks
│   ├── dlt/                   # Delta Live Tables
│   ├── sql/                   # SQL scripts
│   └── files/                 # Additional files
├── tests/                     # Test files
└── docs/                      # Documentation
```

---

## 🎯 Key Features

### **Automated Deployments**
- Push to `develop` → Auto-deploys to **Dev**
- Push to `main` → Auto-deploys to **UAT**
- Manual workflow → Deploys to **Prod** (with approval)

### **Everything is Dynamic**
- No hardcoded secrets
- All credentials in GitHub secrets
- Environment-specific configurations
- Easy to update and maintain

### **AWS Databricks Ready**
- S3 storage paths configured
- EC2 instance types (i3.xlarge, i3.2xlarge)
- Unity Catalog support
- Service Principal authentication

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| **[README_FIRST.md](docs/README_FIRST.md)** | 👈 **Start here** - Main navigation |
| **[QUICK_START_AWS.md](docs/QUICK_START_AWS.md)** | ⚡ Deploy in 10 steps (35 min) |
| **[GITHUB_QUICK_SETUP.md](docs/GITHUB_QUICK_SETUP.md)** | 🔧 GitHub CI/CD setup checklist |
| **[GITHUB_SETUP.md](docs/GITHUB_SETUP.md)** | 📖 Complete GitHub setup guide |
| **[DEPLOYMENT_GUIDE_AWS.md](docs/DEPLOYMENT_GUIDE_AWS.md)** | 📚 Detailed deployment instructions |
| **[AWS_DATABRICKS_SETUP.md](docs/AWS_DATABRICKS_SETUP.md)** | ⚙️ AWS configuration summary |
| **[START_HERE_AWS.md](docs/START_HERE_AWS.md)** | 🗺️ AWS navigation guide |
| **[PROJECT_OVERVIEW.md](docs/PROJECT_OVERVIEW.md)** | 📊 Architecture overview |
| **[FINAL_SETUP.md](docs/FINAL_SETUP.md)** | ✅ Complete setup summary |

---

## 🔐 Prerequisites

### **Required:**
1. ✅ **3 AWS Databricks workspaces** (Dev, UAT, Prod)
2. ✅ **Service Principal** in each workspace
3. ✅ **GitHub repository** (this one!)
4. ✅ **Databricks CLI** (v0.200.0+)

### **GitHub Secrets (5 required):**
```
DATABRICKS_DEV_HOST
DATABRICKS_UAT_HOST
DATABRICKS_PROD_HOST
DATABRICKS_CLIENT_ID
DATABRICKS_CLIENT_SECRET
```

**👉 See [docs/GITHUB_QUICK_SETUP.md](docs/GITHUB_QUICK_SETUP.md) for setup instructions**

---

## 🚀 Quick Deployment

```bash
# 1. Clone the repository
git clone https://github.com/chandrur44/Databricks-Asset-Bundles.git
cd Databricks-Asset-Bundles

# 2. Update config files (config/dev.yml, uat.yml, prod.yml)
vim config/dev.yml  # Add your workspace URL and S3 bucket

# 3. Set environment variables
export DATABRICKS_CLIENT_ID="your-app-id"
export DATABRICKS_CLIENT_SECRET="your-secret"

# 4. Deploy to Dev
databricks bundle validate -t dev
databricks bundle deploy -t dev

# 5. Test
databricks bundle run sample_etl_job -t dev
```

---

## 🔄 CI/CD Workflow

```
develop branch → Validates → Deploys to Dev (automatic)
    ↓
main branch → Validates → Deploys to UAT (automatic)
    ↓
Manual trigger → Validates → Deploys to Prod (requires approval)
```

---

## 📦 What's Included

### **Notebooks (8 files)**
- Bronze layer ingestion
- Silver layer transformation
- Gold layer aggregation
- Data quality checks
- DLT pipelines (batch + streaming)

### **Jobs (3 workflows)**
- Sample ETL job (Bronze → Silver → Gold)
- Data quality job
- SQL query job

### **Pipelines (2 DLT)**
- Batch processing pipeline
- Streaming pipeline

### **SQL Queries (3 files)**
- Daily metrics
- Customer analysis
- Data quality reporting

---

## 🛠️ Configuration

All configurations are in the `config/` directory:
- `config/dev.yml` - Development environment
- `config/uat.yml` - UAT environment
- `config/prod.yml` - Production environment

**Dynamic variables:**
- `${env.DATABRICKS_CLIENT_ID}` - From GitHub secrets
- Workspace URLs - Set per environment
- S3 buckets - Set per environment
- Instance types - Set per environment

---

## 🆘 Need Help?

1. **Quick questions?** Check [docs/README_FIRST.md](docs/README_FIRST.md)
2. **Setup help?** Read [docs/GITHUB_QUICK_SETUP.md](docs/GITHUB_QUICK_SETUP.md)
3. **Deployment issues?** See [docs/DEPLOYMENT_GUIDE_AWS.md](docs/DEPLOYMENT_GUIDE_AWS.md)
4. **GitHub Actions not working?** Read [docs/GITHUB_SETUP.md](docs/GITHUB_SETUP.md)

---

## 🔗 Quick Links

- **Add GitHub Secrets**: https://github.com/chandrur44/Databricks-Asset-Bundles/settings/secrets/actions
- **Create Environments**: https://github.com/chandrur44/Databricks-Asset-Bundles/settings/environments
- **View Actions**: https://github.com/chandrur44/Databricks-Asset-Bundles/actions
- **Branches**:
  - [develop](https://github.com/chandrur44/Databricks-Asset-Bundles/tree/develop) - For Dev deployments
  - [main](https://github.com/chandrur44/Databricks-Asset-Bundles/tree/main) - For UAT deployments

---

## 📊 Repository Stats

- **32 files** tracked
- **8 notebooks** ready to customize
- **3 workflow jobs** defined
- **2 DLT pipelines** configured
- **3 environments** supported
- **100% dynamic** configuration

---

## ✅ Getting Started Checklist

```
GitHub Setup:
☐ Fork or clone this repository
☐ Add 5 GitHub secrets
☐ Create 3 GitHub environments (dev, uat, production)

Configuration:
☐ Update config/dev.yml with your Dev workspace URL
☐ Update config/uat.yml with your UAT workspace URL
☐ Update config/prod.yml with your Prod workspace URL
☐ Update S3 bucket names in all config files

Deployment:
☐ Push to develop branch to deploy to Dev
☐ Push to main branch to deploy to UAT
☐ Use manual workflow to deploy to Prod
```

---

## 🎉 You're Ready!

Your Databricks Asset Bundle is:
- ✅ Version controlled
- ✅ Fully automated
- ✅ 100% dynamic
- ✅ Production ready

**Start here: [docs/README_FIRST.md](docs/README_FIRST.md)** 🚀

---

## 📄 License

[Your License Here]

---

**Made with ❤️ for AWS Databricks**
