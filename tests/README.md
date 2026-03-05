# Tests Directory

This directory contains tests for your Databricks notebooks, DLT pipelines, and data transformations.

## Test Structure

```
tests/
├── unit/                    # Unit tests for individual functions
│   ├── test_transformations.py
│   └── test_data_quality.py
├── integration/             # Integration tests for workflows
│   ├── test_etl_pipeline.py
│   └── test_dlt_pipeline.py
└── fixtures/               # Test data and fixtures
    ├── sample_data.json
    └── expected_results.csv
```

## Testing Frameworks

### Option 1: pytest (Recommended)
```python
# tests/unit/test_transformations.py
import pytest
from pyspark.sql import SparkSession

@pytest.fixture(scope="session")
def spark():
    return SparkSession.builder \
        .appName("test") \
        .master("local[*]") \
        .getOrCreate()

def test_bronze_ingestion(spark):
    # Test your transformation logic
    input_data = [
        {"id": 1, "amount": 100},
        {"id": 2, "amount": 200}
    ]
    df = spark.createDataFrame(input_data)

    # Add your transformation logic
    result = df.filter(df.amount > 150)

    assert result.count() == 1
```

### Option 2: unittest
```python
# tests/unit/test_data_quality.py
import unittest
from pyspark.sql import SparkSession

class TestDataQuality(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spark = SparkSession.builder \
            .appName("test") \
            .master("local[*]") \
            .getOrCreate()

    def test_null_check(self):
        data = [{"id": 1}, {"id": None}]
        df = self.spark.createDataFrame(data)

        null_count = df.filter(df.id.isNull()).count()
        self.assertEqual(null_count, 1)

if __name__ == '__main__':
    unittest.main()
```

## Running Tests Locally

### Install dependencies
```bash
pip install pytest pytest-spark pyspark
```

### Run all tests
```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/unit/test_transformations.py

# Run with coverage
pytest --cov=src tests/
```

## CI/CD Integration

Add to your GitHub Actions workflow:

```yaml
# .github/workflows/test.yml
name: Run Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: |
          pip install pytest pytest-spark pyspark

      - name: Run tests
        run: pytest tests/ -v
```

## Testing Databricks Notebooks

### Using dbx (Databricks CLI Extensions)
```bash
# Install dbx
pip install dbx

# Run notebook tests in Databricks
dbx execute --cluster-name=test-cluster notebook_name
```

### Using Databricks Connect
```python
# tests/integration/test_notebook_execution.py
from databricks_connect import DatabricksSession

def test_notebook_execution():
    spark = DatabricksSession.builder.getOrCreate()

    # Run your notebook programmatically
    result = spark.sql("SELECT COUNT(*) FROM dev_catalog.dev_schema.bronze_transactions")

    assert result.collect()[0][0] > 0
```

## DLT Pipeline Testing

Test DLT pipeline expectations:

```python
# tests/integration/test_dlt_pipeline.py
def test_dlt_expectations(spark):
    # Test that expectations work correctly
    test_data = [
        {"transaction_id": "1", "amount": 100},
        {"transaction_id": None, "amount": 200}  # Should be dropped
    ]

    df = spark.createDataFrame(test_data)

    # Simulate expectation
    valid_df = df.filter(df.transaction_id.isNotNull())

    assert valid_df.count() == 1
```

## Best Practices

1. **Test early and often**: Write tests as you develop
2. **Use fixtures**: Reuse test data and setup code
3. **Mock external dependencies**: Don't test actual data sources in unit tests
4. **Test edge cases**: Null values, empty datasets, large datasets
5. **Integration tests**: Test complete workflows end-to-end
6. **Data quality tests**: Validate data transformations produce expected results

## Sample Test Data

Store sample test data in `tests/fixtures/`:

```json
// tests/fixtures/sample_transactions.json
[
  {"transaction_id": "1", "amount": 100, "status": "COMPLETED"},
  {"transaction_id": "2", "amount": 200, "status": "PENDING"}
]
```

Load in tests:
```python
import json
import os

def load_test_data():
    fixture_path = os.path.join(os.path.dirname(__file__), "fixtures/sample_transactions.json")
    with open(fixture_path) as f:
        return json.load(f)
```

## Current Status

✅ Directory created and ready for tests
📝 Add your test files here
🧪 Set up pytest or unittest framework
🔄 Integrate with CI/CD pipeline

---

**Note**: Start with unit tests for transformation logic, then add integration tests for complete workflows.
