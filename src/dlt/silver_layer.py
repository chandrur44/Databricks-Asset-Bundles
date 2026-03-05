# Databricks notebook source
# MAGIC %md
# MAGIC # DLT Silver Layer
# MAGIC
# MAGIC Delta Live Tables silver layer with cleaned and transformed data

# COMMAND ----------

import dlt
from pyspark.sql import functions as F
from pyspark.sql.window import Window

# COMMAND ----------

# MAGIC %md
# MAGIC ## Silver Tables - Cleaned and Transformed Data

# COMMAND ----------

@dlt.table(
    name="silver_transactions",
    comment="Cleaned and validated transaction data",
    table_properties={
        "quality": "silver",
        "pipelines.autoOptimize.zOrderCols": "transaction_date,customer_id"
    }
)
@dlt.expect_or_drop("valid_status", "status IN ('COMPLETED', 'PENDING', 'FAILED')")
@dlt.expect_or_drop("positive_amount", "amount > 0")
@dlt.expect("no_null_customer", "customer_id IS NOT NULL")
def silver_transactions():
    """Transform bronze transactions to silver"""

    # Window for deduplication
    window_spec = Window.partitionBy("transaction_id").orderBy(F.col("ingestion_timestamp").desc())

    return (
        dlt.read_stream("bronze_transactions_validated")
        # Deduplication
        .withColumn("row_num", F.row_number().over(window_spec))
        .filter(F.col("row_num") == 1)
        .drop("row_num")
        # Data type conversions
        .withColumn("amount", F.col("amount").cast("decimal(18,2)"))
        .withColumn("transaction_date", F.to_date("transaction_timestamp"))
        # Standardization
        .withColumn("status", F.upper(F.trim(F.col("status"))))
        .withColumn("currency", F.upper(F.trim(F.col("currency"))))
        # Business logic
        .withColumn("is_large_transaction", F.when(F.col("amount") > 10000, True).otherwise(False))
        .withColumn(
            "transaction_category",
            F.when(F.col("amount") < 100, "small")
            .when(F.col("amount") < 1000, "medium")
            .otherwise("large")
        )
        .withColumn("processed_timestamp", F.current_timestamp())
    )

# COMMAND ----------

@dlt.table(
    name="silver_customers",
    comment="Cleaned customer dimension"
)
@dlt.expect_or_drop("valid_customer_id", "customer_id IS NOT NULL")
def silver_customers():
    """Transform bronze customers to silver"""
    return (
        dlt.read_stream("bronze_customers")
        .withColumn("customer_name", F.trim(F.col("customer_name")))
        .withColumn("email", F.lower(F.trim(F.col("email"))))
        .withColumn("processed_timestamp", F.current_timestamp())
    )

# COMMAND ----------

# MAGIC %md
# MAGIC ## Apply SCD Type 2 for Customer Dimension

# COMMAND ----------

dlt.create_streaming_table(
    name="silver_customers_scd2",
    comment="Customer dimension with SCD Type 2"
)

dlt.apply_changes(
    target="silver_customers_scd2",
    source="silver_customers",
    keys=["customer_id"],
    sequence_by="processed_timestamp",
    stored_as_scd_type="2",
    track_history_column_list=["customer_name", "email", "phone", "address"]
)
