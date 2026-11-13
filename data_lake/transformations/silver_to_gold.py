
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    sum as spark_sum,
    count,
    current_timestamp
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]

ORDERS_PATH = PROJECT_ROOT / "data_lake" / "silver" / "orders"
ITEMS_PATH = PROJECT_ROOT / "data_lake" / "silver" / "orderitems"

GOLD_ORDER_PATH = PROJECT_ROOT / "data_lake" / "gold" / "order_sales"
GOLD_PRODUCT_PATH = PROJECT_ROOT / "data_lake" / "gold" / "product_sales"

spark = (
    SparkSession.builder
    .appName("BeautyItalia-Silver-To-Gold")
    .master("local[3]")
    .getOrCreate()
)

# Read Silver datasets
orders_df = spark.read.parquet(str(ORDERS_PATH))
items_df = spark.read.parquet(str(ITEMS_PATH))

# Calculate revenue for each order
order_metrics = (
    items_df
    .withColumn(
        "LineRevenue",
        col("Quantity") * col("UnitPrice")
    )
    .groupBy("OrderID")
    .agg(
        spark_sum("LineRevenue").alias("TotalRevenue"),
        spark_sum("Quantity").alias("TotalQuantity"),
        count("OrderItemID").alias("TotalOrderItems")
    )
)

# Join order information with calculated metrics
order_sales = (
    orders_df
    .join(order_metrics, on="OrderID", how="left")
    .withColumn("GoldProcessedAt", current_timestamp())
)

# Save Gold order-level dataset
order_sales.write.mode("overwrite").parquet(str(GOLD_ORDER_PATH))

print("Gold order sales records:", order_sales.count())
order_sales.orderBy("OrderID").show(truncate=False)

# Product-level sales analysis
product_sales = (
    items_df
    .withColumn(
        "LineRevenue",
        col("Quantity") * col("UnitPrice")
    )
    .groupBy("ProductID")
    .agg(
        spark_sum("Quantity").alias("UnitsSold"),
        spark_sum("LineRevenue").alias("TotalRevenue")
    )
    .orderBy(col("TotalRevenue").desc())
)

product_sales.write.mode("overwrite").parquet(str(GOLD_PRODUCT_PATH))

print("Gold product sales records:", product_sales.count())
product_sales.show(truncate=False)

spark.stop()
