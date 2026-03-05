# Databricks notebook source
# MAGIC %md
# MAGIC # Gold Layer - Business Aggregations
# MAGIC
# MAGIC This notebook creates gold layer aggregations for business consumption.
# MAGIC - Creates aggregated metrics
# MAGIC - Builds dimensional models
# MAGIC - Optimizes for query performance

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

spark.sql(f"USE CATALOG {catalog}")
spark.sql(f"USE SCHEMA {schema}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Read Silver Data

# COMMAND ----------

df_silver = spark.table(f"{catalog}.{schema}.silver_transactions")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Daily Aggregations

# COMMAND ----------

df_daily_metrics = (
    df_silver
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

# Write daily metrics
(
    df_daily_metrics.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .partitionBy("date")
    .saveAsTable(f"{catalog}.{schema}.gold_daily_metrics")
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Customer Aggregations

# COMMAND ----------

df_customer_metrics = (
    df_silver
    .filter(F.col("status") == "COMPLETED")
    .groupBy("customer_id")
    .agg(
        F.count("transaction_id").alias("total_transactions"),
        F.sum("amount").alias("lifetime_value"),
        F.avg("amount").alias("avg_transaction_value"),
        F.max("transaction_date").alias("last_transaction_date"),
        F.min("transaction_date").alias("first_transaction_date"),
        F.sum(
            F.when(F.col("is_large_transaction"), 1).otherwise(0)
        ).alias("large_transaction_count")
    )
    .withColumn("processing_timestamp", F.current_timestamp())
    .withColumn(
        "customer_segment",
        F.when(F.col("lifetime_value") > 100000, "Premium")
        .when(F.col("lifetime_value") > 10000, "Gold")
        .when(F.col("lifetime_value") > 1000, "Silver")
        .otherwise("Bronze")
    )
)

# Write customer metrics
(
    df_customer_metrics.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(f"{catalog}.{schema}.gold_customer_metrics")
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Optimize Tables

# COMMAND ----------

# Optimize and Z-ORDER
spark.sql(f"OPTIMIZE {catalog}.{schema}.gold_daily_metrics ZORDER BY (date)")
spark.sql(f"OPTIMIZE {catalog}.{schema}.gold_customer_metrics ZORDER BY (customer_id)")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Generate Summary Statistics

# COMMAND ----------

print("=" * 50)
print("Gold Layer Summary Statistics")
print("=" * 50)

daily_count = spark.table(f"{catalog}.{schema}.gold_daily_metrics").count()
customer_count = spark.table(f"{catalog}.{schema}.gold_customer_metrics").count()

print(f"Daily metrics records: {daily_count}")
print(f"Customer metrics records: {customer_count}")

# COMMAND ----------

dbutils.notebook.exit("Success")
