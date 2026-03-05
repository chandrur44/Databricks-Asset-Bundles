# Databricks notebook source
# MAGIC %md
# MAGIC # Bronze Layer - Data Ingestion
# MAGIC
# MAGIC This notebook ingests raw data into the bronze layer.
# MAGIC - Reads data from source systems
# MAGIC - Minimal transformations
# MAGIC - Stores in Delta format with metadata

# COMMAND ----------

# Get parameters
dbutils.widgets.text("environment", "dev", "Environment")
dbutils.widgets.text("catalog", "dev_catalog", "Catalog")
dbutils.widgets.text("schema", "dev_schema", "Schema")

environment = dbutils.widgets.get("environment")
catalog = dbutils.widgets.get("catalog")
schema = dbutils.widgets.get("schema")

print(f"Running in {environment} environment")
print(f"Target: {catalog}.{schema}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Setup

# COMMAND ----------

from pyspark.sql import functions as F
from datetime import datetime

# Set current catalog and schema
spark.sql(f"USE CATALOG {catalog}")
spark.sql(f"USE SCHEMA {schema}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Read Source Data

# COMMAND ----------

# Example: Read from cloud storage
source_path = f"dbfs:/mnt/{environment}/raw/transactions"

# Read raw data
df_raw = (
    spark.read
    .format("json")  # or csv, parquet, etc.
    .option("inferSchema", "true")
    .option("multiline", "true")
    .load(source_path)
)

# Add metadata columns
df_bronze = (
    df_raw
    .withColumn("ingestion_timestamp", F.current_timestamp())
    .withColumn("source_file", F.input_file_name())
    .withColumn("environment", F.lit(environment))
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Write to Bronze Table

# COMMAND ----------

# Write to Delta table with schema evolution
(
    df_bronze.write
    .format("delta")
    .mode("append")
    .option("mergeSchema", "true")
    .option("delta.enableChangeDataFeed", "true")
    .saveAsTable(f"{catalog}.{schema}.bronze_transactions")
)

print(f"Ingested {df_bronze.count()} records to bronze_transactions")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Data Quality Checks

# COMMAND ----------

# Basic validation
record_count = spark.table(f"{catalog}.{schema}.bronze_transactions").count()
null_count = spark.table(f"{catalog}.{schema}.bronze_transactions").filter(F.col("transaction_id").isNull()).count()

print(f"Total records: {record_count}")
print(f"Null transaction_ids: {null_count}")

if null_count > 0:
    print("WARNING: Found records with null transaction_id")

# COMMAND ----------

dbutils.notebook.exit("Success")
