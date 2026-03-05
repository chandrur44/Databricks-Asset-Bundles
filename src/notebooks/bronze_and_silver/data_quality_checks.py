# Databricks notebook source
# MAGIC %md
# MAGIC # Data Quality Checks
# MAGIC
# MAGIC Automated data quality validation across all layers

# COMMAND ----------

# Get parameters
dbutils.widgets.text("environment", "dev", "Environment")
dbutils.widgets.text("catalog", "dev_catalog", "Catalog")
dbutils.widgets.text("schema", "dev_schema", "Schema")

environment = dbutils.widgets.get("environment")
catalog = dbutils.widgets.get("catalog")
schema = dbutils.widgets.get("schema")

# COMMAND ----------

from pyspark.sql import functions as F
from datetime import datetime

spark.sql(f"USE CATALOG {catalog}")
spark.sql(f"USE SCHEMA {schema}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Define Quality Checks

# COMMAND ----------

def check_null_percentage(table_name, column_name, threshold=0.05):
    """Check if null percentage is below threshold"""
    df = spark.table(f"{catalog}.{schema}.{table_name}")
    total = df.count()
    null_count = df.filter(F.col(column_name).isNull()).count()
    null_pct = null_count / total if total > 0 else 0

    return {
        "table": table_name,
        "check": f"null_percentage_{column_name}",
        "result": "PASS" if null_pct < threshold else "FAIL",
        "metric_value": null_pct,
        "threshold": threshold
    }

def check_duplicate_keys(table_name, key_columns):
    """Check for duplicate keys"""
    df = spark.table(f"{catalog}.{schema}.{table_name}")
    total = df.count()
    distinct = df.select(key_columns).distinct().count()

    return {
        "table": table_name,
        "check": f"duplicate_keys_{','.join(key_columns)}",
        "result": "PASS" if total == distinct else "FAIL",
        "metric_value": total - distinct,
        "threshold": 0
    }

def check_freshness(table_name, timestamp_column, max_age_hours=24):
    """Check data freshness"""
    df = spark.table(f"{catalog}.{schema}.{table_name}")
    max_timestamp = df.agg(F.max(timestamp_column)).collect()[0][0]

    if max_timestamp:
        age_hours = (datetime.now() - max_timestamp).total_seconds() / 3600
        result = "PASS" if age_hours < max_age_hours else "FAIL"
    else:
        age_hours = None
        result = "FAIL"

    return {
        "table": table_name,
        "check": f"freshness_{timestamp_column}",
        "result": result,
        "metric_value": age_hours,
        "threshold": max_age_hours
    }

# COMMAND ----------

# MAGIC %md
# MAGIC ## Run Quality Checks

# COMMAND ----------

quality_checks = []

# Bronze layer checks
quality_checks.append(check_null_percentage("bronze_transactions", "transaction_id", 0.01))
quality_checks.append(check_freshness("bronze_transactions", "ingestion_timestamp", 24))

# Silver layer checks
quality_checks.append(check_null_percentage("silver_transactions", "transaction_id", 0.0))
quality_checks.append(check_duplicate_keys("silver_transactions", ["transaction_id"]))
quality_checks.append(check_freshness("silver_transactions", "transaction_date", 48))

# Gold layer checks
quality_checks.append(check_null_percentage("gold_daily_metrics", "date", 0.0))
quality_checks.append(check_duplicate_keys("gold_daily_metrics", ["date", "currency"]))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Save Results

# COMMAND ----------

# Convert to DataFrame
df_results = spark.createDataFrame(quality_checks)
df_results = df_results.withColumn("check_timestamp", F.current_timestamp())

# Display results
display(df_results)

# Save to quality results table
(
    df_results.write
    .format("delta")
    .mode("append")
    .saveAsTable(f"{catalog}.{schema}.data_quality_results")
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Summary Report

# COMMAND ----------

failed_checks = df_results.filter(F.col("result") == "FAIL").count()
total_checks = df_results.count()

print("=" * 50)
print("Data Quality Check Summary")
print("=" * 50)
print(f"Total checks: {total_checks}")
print(f"Passed: {total_checks - failed_checks}")
print(f"Failed: {failed_checks}")
print("=" * 50)

if failed_checks > 0:
    print("\nFailed checks:")
    df_results.filter(F.col("result") == "FAIL").select("table", "check", "metric_value", "threshold").show(truncate=False)
    dbutils.notebook.exit("FAILED")
else:
    print("\nAll quality checks passed!")
    dbutils.notebook.exit("SUCCESS")
