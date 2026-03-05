# Databricks notebook source
# MAGIC %md
# MAGIC # Silver Layer - Data Transformation
# MAGIC
# MAGIC This notebook transforms bronze data into the silver layer.
# MAGIC - Cleans and validates data
# MAGIC - Applies business rules
# MAGIC - Deduplication and standardization

# COMMAND ----------

# Get parameters
dbutils.widgets.text("environment", "dev", "Environment")
dbutils.widgets.text("catalog", "dev_catalog", "Catalog")
dbutils.widgets.text("schema", "dev_schema", "Schema")

environment = dbutils.widgets.get("environment")
catalog = dbutils.widgets.get("catalog")
schema = dbutils.widgets.get("schema")

print(f"Running in {environment} environment")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Setup

# COMMAND ----------

from pyspark.sql import functions as F
from pyspark.sql.window import Window

spark.sql(f"USE CATALOG {catalog}")
spark.sql(f"USE SCHEMA {schema}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Read Bronze Data

# COMMAND ----------

df_bronze = spark.table(f"{catalog}.{schema}.bronze_transactions")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Data Cleaning and Transformation

# COMMAND ----------

# Remove duplicates
window_spec = Window.partitionBy("transaction_id").orderBy(F.col("ingestion_timestamp").desc())

df_cleaned = (
    df_bronze
    # Remove duplicates - keep latest
    .withColumn("row_num", F.row_number().over(window_spec))
    .filter(F.col("row_num") == 1)
    .drop("row_num")
    # Data type conversions
    .withColumn("amount", F.col("amount").cast("decimal(18,2)"))
    .withColumn("transaction_date", F.to_date("transaction_timestamp"))
    # Standardize fields
    .withColumn("status", F.upper(F.trim(F.col("status"))))
    .withColumn("currency", F.upper(F.trim(F.col("currency"))))
    # Add business logic
    .withColumn(
        "is_large_transaction",
        F.when(F.col("amount") > 10000, True).otherwise(False)
    )
    .withColumn(
        "transaction_category",
        F.when(F.col("amount") < 100, "small")
        .when(F.col("amount") < 1000, "medium")
        .otherwise("large")
    )
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Data Quality Validations

# COMMAND ----------

# Filter out invalid records
df_silver = (
    df_cleaned
    .filter(F.col("transaction_id").isNotNull())
    .filter(F.col("amount") > 0)
    .filter(F.col("status").isin(["COMPLETED", "PENDING", "FAILED"]))
)

invalid_count = df_cleaned.count() - df_silver.count()
print(f"Filtered out {invalid_count} invalid records")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Write to Silver Table

# COMMAND ----------

(
    df_silver.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .option("delta.enableChangeDataFeed", "true")
    .saveAsTable(f"{catalog}.{schema}.silver_transactions")
)

print(f"Processed {df_silver.count()} records to silver_transactions")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Create Silver Views

# COMMAND ----------

# Create view for active transactions
spark.sql(f"""
CREATE OR REPLACE VIEW {catalog}.{schema}.vw_active_transactions AS
SELECT
    transaction_id,
    customer_id,
    amount,
    currency,
    status,
    transaction_date,
    is_large_transaction,
    transaction_category
FROM {catalog}.{schema}.silver_transactions
WHERE status = 'COMPLETED'
    AND transaction_date >= CURRENT_DATE - INTERVAL 90 DAYS
""")

# COMMAND ----------

dbutils.notebook.exit("Success")
