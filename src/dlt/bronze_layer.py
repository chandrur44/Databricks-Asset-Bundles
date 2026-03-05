# Databricks notebook source
# MAGIC %md
# MAGIC # DLT Bronze Layer
# MAGIC
# MAGIC Delta Live Tables bronze layer definitions

# COMMAND ----------

import dlt
from pyspark.sql import functions as F

# COMMAND ----------

# MAGIC %md
# MAGIC ## Bronze Tables - Raw Data Ingestion

# COMMAND ----------

@dlt.table(
    name="bronze_transactions",
    comment="Raw transaction data ingested from source systems",
    table_properties={
        "quality": "bronze",
        "pipelines.autoOptimize.zOrderCols": "transaction_id"
    }
)
def bronze_transactions():
    """Ingest raw transaction data"""
    return (
        spark.readStream
        .format("cloudFiles")
        .option("cloudFiles.format", "json")
        .option("cloudFiles.inferColumnTypes", "true")
        .load("dbfs:/mnt/raw/transactions")
        .withColumn("ingestion_timestamp", F.current_timestamp())
        .withColumn("source_file", F.input_file_name())
    )

# COMMAND ----------

@dlt.table(
    name="bronze_customers",
    comment="Raw customer data from source systems"
)
def bronze_customers():
    """Ingest raw customer data"""
    return (
        spark.readStream
        .format("cloudFiles")
        .option("cloudFiles.format", "json")
        .option("cloudFiles.inferColumnTypes", "true")
        .load("dbfs:/mnt/raw/customers")
        .withColumn("ingestion_timestamp", F.current_timestamp())
    )

# COMMAND ----------

# MAGIC %md
# MAGIC ## Data Quality Expectations

# COMMAND ----------

@dlt.table(
    name="bronze_transactions_validated",
    comment="Bronze transactions with quality checks"
)
@dlt.expect_or_drop("valid_transaction_id", "transaction_id IS NOT NULL")
@dlt.expect_or_drop("valid_amount", "amount > 0")
def bronze_transactions_validated():
    """Bronze data with quality expectations"""
    return dlt.read_stream("bronze_transactions")
