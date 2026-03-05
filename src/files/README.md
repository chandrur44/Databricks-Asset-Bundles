# Files Directory

This directory is for storing additional files that need to be deployed to Databricks workspaces.

## What Goes Here

### 1. **Python Wheels (.whl)**
Custom Python packages built for your project:
```
src/files/
├── my_custom_library-1.0.0-py3-none-any.whl
└── data_processing_utils-2.1.0-py3-none-any.whl
```

### 2. **JAR Files (.jar)**
Java/Scala libraries or Spark JARs:
```
src/files/
├── custom-spark-extensions-1.0.jar
└── external-connectors-2.3.1.jar
```

### 3. **Init Scripts**
Cluster initialization scripts:
```
src/files/
├── init_scripts/
│   ├── install_dependencies.sh
│   └── configure_cluster.sh
```

### 4. **Configuration Files**
JSON, YAML, or other configuration files:
```
src/files/
├── configs/
│   ├── app_config.json
│   └── mapping_rules.yaml
```

### 5. **Data Files (Small)**
Small reference data files (lookup tables, etc.):
```
src/files/
├── reference_data/
│   ├── country_codes.csv
│   └── category_mapping.json
```

## Usage in DAB

These files are automatically uploaded to your workspace when you deploy:

### In databricks.yml:
```yaml
artifacts:
  files:
    type: file
    path: ./src/files
```

### Reference in Jobs:
```yaml
resources:
  jobs:
    my_job:
      tasks:
        - task_key: my_task
          libraries:
            - whl: "${workspace.file_path}/my_custom_library-1.0.0-py3-none-any.whl"
            - jar: "${workspace.file_path}/custom-spark-extensions-1.0.jar"
```

### Reference in Notebooks:
```python
# Install a wheel from the files directory
%pip install /Workspace/path/to/your/wheel.whl

# Read a config file
import json
with open("/Workspace/path/to/config.json", "r") as f:
    config = json.load(f)
```

## Best Practices

1. **Version your files**: Include version numbers in filenames (e.g., `library-1.0.0.whl`)
2. **Keep files small**: Large files should be stored in cloud storage (Azure Blob, ADLS)
3. **Document dependencies**: Add a requirements.txt or list dependencies in comments
4. **Use .gitignore**: Consider ignoring compiled artifacts if they're built in CI/CD

## Examples

### Building a Python Wheel
```bash
# In your Python package directory
python setup.py bdist_wheel

# Copy to files directory
cp dist/my_package-1.0.0-py3-none-any.whl src/files/
```

### Creating an Init Script
```bash
#!/bin/bash
# src/files/init_scripts/install_custom_tools.sh

# Install custom tools on cluster startup
pip install custom-monitoring-tool
echo "Custom tools installed"
```

## Current Status

✅ Directory created and ready to use
📝 Add your files here as needed
🚫 Don't commit large binary files (use cloud storage instead)

---

**Note**: This folder starts empty by design. Add files here as your project requires them.
