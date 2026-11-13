
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    trim,
    upper,
    current_timestamp
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]

spark = (
    SparkSession.builder
    .appName("BeautyItalia-Bronze-To-Silver")
    .master("local[3]")
    .getOrCreate()
)


def process_table(table, required_columns):
    bronze_path = PROJECT_ROOT / "data_lake" / "bronze" / table
    silver_path = PROJECT_ROOT / "data_lake" / "silver" / table
    rejected_path = PROJECT_ROOT / "data_lake" / "silver" / f"rejected_{table}"

    df = spark.read.parquet(str(bronze_path))

    print(f"\n{table} Bronze records: {df.count()}")

    cleaned_df = df.withColumn(
        "ProcessedAt", current_timestamp()
    )

    if table == "orders":
        cleaned_df = (
            cleaned_df
            .withColumn("OrderSource", upper(trim(col("OrderSource"))))
            .withColumn("OrderStatus", upper(trim(col("OrderStatus"))))
        )

        valid_condition = (
            col("OrderID").isNotNull()
            & col("CustomerID").isNotNull()
            & col("OrderDate").isNotNull()
            & col("OrderSource").isin("ECOMMERCE", "RETAIL")
            & col("OrderStatus").isin("COMPLETED", "PROCESSING", "SHIPPED")
        )

        deduplication_key = ["OrderID"]

    else:
        valid_condition = (
            col("OrderItemID").isNotNull()
            & col("OrderID").isNotNull()
            & col("ProductID").isNotNull()
            & (col("Quantity") > 0)
            & (col("UnitPrice") >= 0)
        )

        deduplication_key = ["OrderItemID"]

    valid_df = cleaned_df.filter(valid_condition)
    rejected_df = cleaned_df.filter(~valid_condition)

    silver_df = valid_df.dropDuplicates(deduplication_key)

    silver_df.write.mode("overwrite").parquet(str(silver_path))
    rejected_df.write.mode("overwrite").parquet(str(rejected_path))

    print(f"{table} Silver records: {silver_df.count()}")
    print(f"{table} Rejected records: {rejected_df.count()}")

    silver_df.show(truncate=False)


process_table("orders", ["OrderID"])
process_table("orderitems", ["OrderItemID"])

spark.stop()
