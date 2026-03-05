# Databricks Asset Bundle (DAB) Project

This repository contains a complete Databricks Asset Bundle (DAB) setup for managing and version-controlling all Databricks assets across multiple environments.

## Overview

This DAB project provides:
- **Multi-environment support**: Dev, UAT, and Production environments
- **Complete asset management**: Workflows, notebooks, DLT pipelines, and SQL queries
- **Version control**: Git-based version control for all assets
- **Easy deployment**: Simple CLI commands to deploy to any environment
- **Starter templates**: Sample notebooks, jobs, and pipelines to get started quickly

## Project Structure

```
.
├── databricks.yml              # Main DAB configuration
├── config/                     # Environment-specific configurations
│   ├── dev.yml
│   ├── uat.yml
│   └── prod.yml
├── resources/                  # Asset definitions
│   ├── jobs.yml               # Workflow job definitions
│   ├── pipelines.yml          # DLT pipeline definitions
│   └── queries.yml            # SQL query definitions
├── src/                       # Source code
│   ├── notebooks/             # Databricks notebooks
│   │   ├── bronze_and_silver/ # Bronze and Silver layer notebooks
│   │   │   ├── bronze_ingestion.py
│   │   │   ├── silver_transformation.py
│   │   │   └── data_quality_checks.py
│   │   └── gold/              # Gold layer notebooks
│   │       └── gold_aggregation.py
│   ├── dlt/                   # Delta Live Tables notebooks
│   │   ├── bronze_layer.py
│   │   ├── silver_layer.py
│   │   ├── gold_layer.py
│   │   └── streaming_ingestion.py
│   ├── sql/                   # SQL scripts
│   │   └── daily_metrics.sql
│   └── files/                 # Additional files (JARs, wheels, etc.)
└── tests/                     # Test files

```

## Prerequisites

### 1. Databricks Workspaces

You need three Databricks workspaces:
- **Development (DEV)**: For development and testing
- **User Acceptance Testing (UAT)**: For user acceptance testing
- **Production (PROD)**: For production workloads

**Workspace URLs Format**: `https://adb-<workspace-id>.<region>.azuredatabricks.net`

### 2. Service Principal (Required for Each Environment)

Create an Azure Service Principal for automated deployments:

#### Create Service Principal in Azure Portal:
```bash
# Using Azure CLI
az ad sp create-for-rbac --name "databricks-dab-sp-{env}" --role contributor --scopes /subscriptions/{subscription-id}
```

This will output:
```json
{
  "appId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",          # This is your Client ID
  "password": "xxxxxxxxxxxxxxxxxxxxxxxxxxxx",                # This is your Client Secret
  "tenant": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"          # This is your Tenant ID
}
```

#### Register Service Principal in Databricks:

For each workspace, add the service principal:
1. Go to Databricks Workspace → **Admin Settings** → **Service Principals**
2. Click **Add Service Principal**
3. Enter the Application (Client) ID
4. Grant appropriate permissions (Workspace Admin for deployment)

**Note**: You can use the same service principal for all environments or create separate ones for better security isolation.

### 3. Unity Catalog Setup

Ensure Unity Catalog is enabled in your workspaces:
- Create catalogs for each environment: `dev_catalog`, `uat_catalog`, `prod_catalog`
- Grant service principal appropriate permissions on catalogs and schemas

### 4. GitHub Repository

Create a GitHub repository to store this DAB project:
```bash
git init
git remote add origin https://github.com/{your-org}/{your-repo}.git
git add .
git commit -m "Initial DAB setup"
git push -u origin main
```

### 5. Local Development Tools

Install required tools:

#### Databricks CLI
```bash
# Install Databricks CLI (version 0.200.0 or higher required for DAB)
curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh | sh

# Or using pip
pip install databricks-cli
```

#### Verify Installation
```bash
databricks --version
```

### 6. Authentication Setup

#### Option A: OAuth (Recommended for Development)
```bash
databricks auth login --host https://adb-<workspace-id>.<region>.azuredatabricks.net
```

#### Option B: Service Principal (Recommended for CI/CD)
Set environment variables:
```bash
export DATABRICKS_HOST="https://adb-<workspace-id>.<region>.azuredatabricks.net"
export DATABRICKS_CLIENT_ID="<service-principal-client-id>"
export DATABRICKS_CLIENT_SECRET="<service-principal-client-secret>"
export DATABRICKS_TENANT_ID="<azure-tenant-id>"
```

Or create a `.databricks/config` file (don't commit this):
```ini
[dev]
host = https://adb-<workspace-id>.<region>.azuredatabricks.net
client_id = <service-principal-client-id>
client_secret = <service-principal-client-secret>
tenant_id = <azure-tenant-id>

[uat]
host = https://adb-<workspace-id>.<region>.azuredatabricks.net
client_id = <service-principal-client-id>
client_secret = <service-principal-client-secret>
tenant_id = <azure-tenant-id>

[prod]
host = https://adb-<workspace-id>.<region>.azuredatabricks.net
client_id = <service-principal-client-id>
client_secret = <service-principal-client-secret>
tenant_id = <azure-tenant-id>
```

## Configuration

### 1. Update Environment Configurations

Edit the configuration files for each environment:

#### `config/dev.yml`
```yaml
variables:
  workspace_host: "https://adb-<workspace-id>.azuredatabricks.net"  # Update this
  service_principal_client_id: "${env.DATABRICKS_CLIENT_ID}"
  catalog_name: "dev_catalog"
  schema_name: "dev_schema"
```

Do the same for `config/uat.yml` and `config/prod.yml`.

### 2. Update Resource Definitions

Customize the resources in the `resources/` directory:
- `jobs.yml`: Define your workflow jobs
- `pipelines.yml`: Define your DLT pipelines
- `queries.yml`: Define your SQL queries

## Deployment

### Validate Configuration

Before deploying, validate your configuration:
```bash
# Validate for dev environment
databricks bundle validate -t dev

# Validate for other environments
databricks bundle validate -t uat
databricks bundle validate -t prod
```

### Deploy to Development

```bash
# Deploy to dev environment
databricks bundle deploy -t dev

# Run a specific job
databricks bundle run sample_etl_job -t dev
```

### Deploy to UAT

```bash
# Deploy to UAT
databricks bundle deploy -t uat

# Run jobs in UAT
databricks bundle run sample_etl_job -t uat
```

### Deploy to Production

```bash
# Deploy to production (requires approval in CI/CD)
databricks bundle deploy -t prod
```

## CI/CD Setup

### GitHub Actions Example

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy DAB

on:
  push:
    branches:
      - main
      - develop
  pull_request:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install Databricks CLI
        run: |
          curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh | sh

      - name: Deploy to Dev
        if: github.ref == 'refs/heads/develop'
        env:
          DATABRICKS_HOST: ${{ secrets.DATABRICKS_DEV_HOST }}
          DATABRICKS_CLIENT_ID: ${{ secrets.DATABRICKS_CLIENT_ID }}
          DATABRICKS_CLIENT_SECRET: ${{ secrets.DATABRICKS_CLIENT_SECRET }}
          DATABRICKS_TENANT_ID: ${{ secrets.DATABRICKS_TENANT_ID }}
        run: |
          databricks bundle deploy -t dev

      - name: Deploy to UAT
        if: github.ref == 'refs/heads/main'
        env:
          DATABRICKS_HOST: ${{ secrets.DATABRICKS_UAT_HOST }}
          DATABRICKS_CLIENT_ID: ${{ secrets.DATABRICKS_CLIENT_ID }}
          DATABRICKS_CLIENT_SECRET: ${{ secrets.DATABRICKS_CLIENT_SECRET }}
          DATABRICKS_TENANT_ID: ${{ secrets.DATABRICKS_TENANT_ID }}
        run: |
          databricks bundle deploy -t uat

      - name: Deploy to Prod (Manual Approval Required)
        if: github.event_name == 'workflow_dispatch'
        env:
          DATABRICKS_HOST: ${{ secrets.DATABRICKS_PROD_HOST }}
          DATABRICKS_CLIENT_ID: ${{ secrets.DATABRICKS_CLIENT_ID }}
          DATABRICKS_CLIENT_SECRET: ${{ secrets.DATABRICKS_CLIENT_SECRET }}
          DATABRICKS_TENANT_ID: ${{ secrets.DATABRICKS_TENANT_ID }}
        run: |
          databricks bundle deploy -t prod
```

### Required GitHub Secrets

Add these secrets to your GitHub repository (Settings → Secrets):
- `DATABRICKS_DEV_HOST`
- `DATABRICKS_UAT_HOST`
- `DATABRICKS_PROD_HOST`
- `DATABRICKS_CLIENT_ID`
- `DATABRICKS_CLIENT_SECRET`
- `DATABRICKS_TENANT_ID`

## Usage

### Adding New Notebooks

1. Create notebook in the appropriate folder:
   - For Bronze/Silver layer: `src/notebooks/bronze_and_silver/`
   - For Gold layer: `src/notebooks/gold/`
2. Add to job definition in `resources/jobs.yml`
3. Deploy: `databricks bundle deploy -t dev`

### Adding New DLT Pipelines

1. Create DLT notebook in `src/dlt/`
2. Add pipeline definition in `resources/pipelines.yml`
3. Deploy: `databricks bundle deploy -t dev`

### Adding New SQL Queries

1. Create SQL file in `src/sql/`
2. Add query definition in `resources/queries.yml`
3. Deploy: `databricks bundle deploy -t dev`

## Asset Migration Between Environments

Assets automatically promote through environments:
1. **Dev**: Development and testing
2. **UAT**: User acceptance testing (promoted from dev via git merge)
3. **Prod**: Production (promoted from uat via git merge/tag)

Simply merge your code to the appropriate branch and the CI/CD pipeline will deploy to the target environment.

## Monitoring and Debugging

### View Deployed Resources
```bash
# List all resources in dev
databricks bundle list -t dev

# Get details of a specific job
databricks jobs get-run <run-id>
```

### View Logs
```bash
# Stream job logs
databricks jobs get-output <run-id>
```

### Destroy Resources (Caution!)
```bash
# Remove all deployed resources (use with caution)
databricks bundle destroy -t dev
```

## Best Practices

1. **Never commit secrets**: Use environment variables or secret management
2. **Test in dev first**: Always test changes in dev before promoting
3. **Use feature branches**: Create feature branches for new development
4. **Code reviews**: Require PR reviews before merging to main
5. **Incremental deployment**: Deploy small, incremental changes
6. **Monitor job runs**: Set up alerts for job failures
7. **Use Unity Catalog**: Leverage Unity Catalog for governance
8. **Document changes**: Keep this README and inline documentation updated

## Troubleshooting

### Authentication Issues
```bash
# Re-authenticate
databricks auth login --host <workspace-url>

# Verify authentication
databricks current-user me
```

### Validation Errors
```bash
# Check for configuration errors
databricks bundle validate -t dev

# View detailed error messages
databricks bundle deploy -t dev --debug
```

### Permission Issues
- Verify service principal has necessary permissions
- Check Unity Catalog grants
- Ensure workspace access is configured

## Support and Resources

- [Databricks Asset Bundles Documentation](https://docs.databricks.com/dev-tools/bundles/index.html)
- [Databricks CLI Documentation](https://docs.databricks.com/dev-tools/cli/index.html)
- [Unity Catalog Documentation](https://docs.databricks.com/data-governance/unity-catalog/index.html)

## License

[Your License Here]
