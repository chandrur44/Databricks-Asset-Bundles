# Databricks notebook source
# MAGIC %md
# MAGIC # DLT Streaming Ingestion
# MAGIC
# MAGIC Real-time data ingestion from streaming sources

# COMMAND ----------

import dlt
from pyspark.sql import functions as F

# COMMAND ----------

# MAGIC %md
# MAGIC ## Streaming Sources

# COMMAND ----------

@dlt.table(
    name="streaming_events",
    comment="Real-time event stream from Kafka/Event Hub"
)
def streaming_events():
    """Ingest streaming events"""
    return (
        spark.readStream
        .format("kafka")  # or eventhubs
        .option("kafka.bootstrap.servers", "<kafka-broker>:9092")
        .option("subscribe", "events-topic")
        .option("startingOffsets", "latest")
        .load()
        .select(
            F.col("key").cast("string"),
            F.from_json(F.col("value").cast("string"), schema).alias("data")
        )
        .select("key", "data.*")
        .withColumn("ingestion_timestamp", F.current_timestamp())
    )

# COMMAND ----------

@dlt.table(
    name="streaming_events_enriched",
    comment="Enriched streaming events"
)
@dlt.expect_or_drop("valid_event_id", "event_id IS NOT NULL")
def streaming_events_enriched():
    """Enrich streaming events with reference data"""
    df_events = dlt.read_stream("streaming_events")
    df_customers = dlt.read("silver_customers_scd2").filter(F.col("__END_AT").isNull())

    return (
        df_events
        .join(df_customers, "customer_id", "left")
        .select(
            "event_id",
            "event_type",
            "customer_id",
            "customer_name",
            "customer_segment",
            "event_timestamp",
            "ingestion_timestamp"
        )
    )
