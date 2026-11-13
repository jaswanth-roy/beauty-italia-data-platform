
import os
from pathlib import Path

from dotenv import load_dotenv
from pyspark.sql import SparkSession

# Load credentials
PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

# JDBC driver
JDBC_JAR = PROJECT_ROOT / "drivers" / "mssql-jdbc-13.6.0.jre11.jar"

# SQL Server connection
host = os.environ["DB_HOST"]
port = os.environ["DB_PORT"]
database = os.environ["DB_NAME"]
username = os.environ["DB_USER"]
password = os.environ["DB_PASSWORD"]

jdbc_url = (
    f"jdbc:sqlserver://{host}:{port};"
    f"databaseName={database};"
    "encrypt=true;"
    "trustServerCertificate=true;"
)

# Start Spark
spark = (
    SparkSession.builder
    .appName("BeautyItalia-SQLServer-Ingestion")
    .master("local[3]")
    .config("spark.jars", str(JDBC_JAR))
    .getOrCreate()
)

# # Read Orders from SQL Server
# orders_df = (
#     spark.read
#     .format("jdbc")
#     .option("url", jdbc_url)
#     .option("dbtable", "dbo.Orders")
#     .option("user", username)
#     .option("password", password)
#     .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver")
#     .load()
# )

# print("SQL Server extraction successful!")
# print(f"Total orders: {orders_df.count()}")

# orders_df.show(truncate=False)

# # Write Bronze Parquet
# bronze_path = PROJECT_ROOT / "data_lake" / "bronze" / "orders"

# orders_df.write.mode("overwrite").parquet(str(bronze_path))

# print(f"Bronze data saved to: {bronze_path}")

# spark.stop()



# Extract Orders and OrderItems from SQL Server
tables = ["Orders", "OrderItems"]

for table in tables:
    df = (
        spark.read
        .format("jdbc")
        .option("url", jdbc_url)
        .option("dbtable", f"dbo.{table}")
        .option("user", username)
        .option("password", password)
        .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver")
        .load()
    )

    print(f"\nExtracted {table}: {df.count()} records")
    df.show(truncate=False)

    bronze_path = PROJECT_ROOT / "data_lake" / "bronze" / table.lower()

    df.write.mode("overwrite").parquet(str(bronze_path))

    print(f"Saved {table} to: {bronze_path}")

spark.stop()