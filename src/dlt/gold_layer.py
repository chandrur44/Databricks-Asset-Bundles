# Databricks notebook source
# MAGIC %md
# MAGIC # DLT Gold Layer
# MAGIC
# MAGIC Delta Live Tables gold layer with aggregated business metrics

# COMMAND ----------

import dlt
from pyspark.sql import functions as F

# COMMAND ----------

# MAGIC %md
# MAGIC ## Gold Tables - Business Aggregations

# COMMAND ----------

@dlt.table(
    name="gold_daily_metrics",
    comment="Daily aggregated transaction metrics",
    table_properties={
        "quality": "gold"
    }
)
def gold_daily_metrics():
    """Daily transaction metrics"""
    return (
        dlt.read("silver_transactions")
        .filter(F.col("status") == "COMPLETED")
        .groupBy(
            F.col("transaction_date").alias("date"),
            "currency"
        )
        .agg(
            F.count("transaction_id").alias("transaction_count"),
            F.sum("amount").alias("total_amount"),
            F.avg("amount").alias("avg_amount"),
            F.min("amount").alias("min_amount"),
            F.max("amount").alias("max_amount"),
            F.countDistinct("customer_id").alias("unique_customers")
        )
        .withColumn("processing_timestamp", F.current_timestamp())
    )

# COMMAND ----------

@dlt.table(
    name="gold_customer_metrics",
    comment="Customer lifetime metrics and segmentation"
)
def gold_customer_metrics():
    """Customer aggregated metrics"""
    return (
        dlt.read("silver_transactions")
        .filter(F.col("status") == "COMPLETED")
        .groupBy("customer_id")
        .agg(
            F.count("transaction_id").alias("total_transactions"),
            F.sum("amount").alias("lifetime_value"),
            F.avg("amount").alias("avg_transaction_value"),
            F.max("transaction_date").alias("last_transaction_date"),
            F.min("transaction_date").alias("first_transaction_date"),
            F.sum(F.when(F.col("is_large_transaction"), 1).otherwise(0)).alias("large_transaction_count")
        )
        .withColumn(
            "customer_segment",
            F.when(F.col("lifetime_value") > 100000, "Premium")
            .when(F.col("lifetime_value") > 10000, "Gold")
            .when(F.col("lifetime_value") > 1000, "Silver")
            .otherwise("Bronze")
        )
        .withColumn("processing_timestamp", F.current_timestamp())
    )

# COMMAND ----------

@dlt.table(
    name="gold_customer_360",
    comment="Complete customer 360 view combining transactions and profile"
)
def gold_customer_360():
    """Customer 360 view"""
    df_customers = dlt.read("silver_customers_scd2").filter(F.col("__END_AT").isNull())
    df_metrics = dlt.read("gold_customer_metrics")

    return (
        df_customers
        .join(df_metrics, "customer_id", "left")
        .select(
            "customer_id",
            "customer_name",
            "email",
            "phone",
            "address",
            "total_transactions",
            "lifetime_value",
            "avg_transaction_value",
            "last_transaction_date",
            "first_transaction_date",
            "customer_segment"
        )
    )
