# Beauty Italia – Enterprise Data Integration & Analytics Platform

An end-to-end Data Engineering project demonstrating data ingestion, integration, transformation, data quality, and business intelligence using Python, SQL Server, PySpark, Parquet, and Streamlit.

## Project Overview

Beauty Italia is a simulated Italian beauty retailer operating across e-commerce and physical retail stores.

The objective of this project is to build a centralized data platform that integrates operational data from different business systems and transforms it into reliable, analytics-ready datasets.

The platform demonstrates how data from ERP, e-commerce, CRM, retail, and warehouse systems can be consolidated to support business reporting and decision-making.

**Main business objectives:**
- Integrate data from multiple operational systems.
- Build reliable and reusable data ingestion processes.
- Implement data validation and transformation.
- Organize data using the Medallion Architecture.
- Generate business-ready sales and product analytics.
- Visualize KPIs through an interactive dashboard.

## Architecture

```text
                 SOURCE SYSTEMS
                       |
             +---------+---------+
             |                   |
          SQL Server       External Systems
          (Operational)   (Future integrations)
             |
             v
       PYTHON + JDBC
       Data Ingestion
             |
             v
       BRONZE LAYER
       Raw Parquet Data
             |
             v
       SILVER LAYER
       Validation & Cleaning
             |
             v
        GOLD LAYER
       Business Aggregations
             |
             v
      STREAMLIT DASHBOARD
       Business Analytics
```

The project follows the Medallion Architecture, separating raw, validated, and business-ready data.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Data engineering and integration |
| SQL Server | Operational relational database |
| Docker | Local SQL Server environment |
| PySpark | Distributed data processing |
| JDBC | SQL Server connectivity |
| Parquet | Columnar data storage |
| Pandas | Dashboard data loading |
| Streamlit | Interactive dashboard |
| Plotly | Data visualization |
| Git | Version control |

## Project Structure

```text
beauty-italia-data-platform/
│
├── dashboard/
│   └── app.py
│
├── data_lake/
│   ├── bronze/
│   │   ├── orders/
│   │   └── orderitems/
│   │
│   ├── silver/
│   │   ├── orders/
│   │   ├── orderitems/
│   │   ├── rejected_orders/
│   │   └── rejected_orderitems/
│   │
│   ├── gold/
│   │   ├── order_sales/
│   │   └── product_sales/
│   │
│   └── transformations/
│       ├── sqlserver_to_bronze.py
│       ├── bronze_to_silver.py
│       └── silver_to_gold.py
│
├── database/
│
├── integration/
│
├── source_systems/
│
├── tests/
│
├── logs/
│
├── drivers/
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

*Note: The integration and source-system folders are reserved for the next development phase.*

## Data Pipeline

### 1. SQL Server – Operational Database

The project uses a local SQL Server instance running inside Docker.

The database is named `BeautyItaliaDB`.

Main tables:

- Customers
- Products
- Stores
- Orders
- OrderItems
- Inventory

The current pipeline extracts Orders and OrderItems.

### 2. Bronze Layer – Raw Data Ingestion

Data is extracted from SQL Server using Python, PySpark, and the Microsoft JDBC driver.

The extracted datasets are stored in Parquet format.

Implemented datasets:

- Orders: 8 records
- OrderItems: 12 records

The Bronze layer preserves the source data before applying business transformations.

### 3. Silver Layer – Data Quality and Transformation

The Silver layer applies data validation and standardization.

Implemented operations:

- Null-value validation on required fields.
- Standardization of order sources and statuses.
- Validation of order quantities and unit prices.
- Duplicate removal using business identifiers.
- Processing timestamp addition.
- Separation of valid and rejected records.

Current validation results:

| Dataset | Bronze | Silver | Rejected |
|---|---:|---:|---:|
| Orders | 8 | 8 | 0 |
| OrderItems | 12 | 12 | 0 |

### 4. Gold Layer – Business Analytics

The Gold layer generates business-ready datasets using PySpark.

**Order Sales**

Contains:
- Order ID
- Sales channel
- Order status
- Order date
- Total quantity
- Number of order items
- Total order revenue

**Product Sales**

Contains:
- Product ID
- Units sold
- Total revenue

Revenue is calculated using:

```python
LineRevenue = Quantity * UnitPrice
```

Order-level revenue is calculated by aggregating order items and joining the results to the Orders dataset.

## Business Results

Based on the current sample dataset:

| KPI | Result |
|---|---:|
| Total Revenue | €523.80 |
| Total Orders | 8 |
| Units Sold | 20 |
| Average Order Value | €65.48 |

**Revenue by sales channel:**

| Channel | Revenue |
|---|---:|
| E-commerce | €303.90 |
| Retail | €219.90 |

**Top-performing product:**

Product ID 104 generated the highest revenue, with €159.98.

These results demonstrate how operational data can be transformed into actionable business insights.

## Interactive Dashboard

The project includes a Streamlit dashboard built on top of the Gold datasets.

Dashboard features:

- Total revenue KPI.
- Total orders KPI.
- Units sold KPI.
- Average order value.
- Revenue by sales channel.
- Revenue by order status.
- Product revenue comparison.
- Order-level details.
- Interactive channel and order-status filters.

### Run the Dashboard

```bash
streamlit run dashboard/app.py
```

Open:

```text
http://localhost:8501
```

## Installation and Setup

### Prerequisites

- Python 3.11 or another compatible Python version.
- Docker Desktop.
- SQL Server running in Docker.
- Java installation compatible with your PySpark version.
- Microsoft SQL Server JDBC driver.

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/beauty-italia-data-platform.git

cd beauty-italia-data-platform
```

### 2. Create a virtual environment

```bash
python3 -m venv venv

source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
DB_HOST=localhost
DB_PORT=1433
DB_NAME=BeautyItaliaDB
DB_USER=sa
DB_PASSWORD=YOUR_LOCAL_SQL_SERVER_PASSWORD
```

Never commit your `.env` file or database credentials to GitHub.

### 5. Configure the JDBC driver

Download the Microsoft SQL Server JDBC driver from:

https://learn.microsoft.com/en-us/sql/connect/jdbc/download-microsoft-jdbc-driver-for-sql-server

Place the compatible JAR file inside:

```text
drivers/
```

The ingestion script expects:

```text
drivers/mssql-jdbc-13.6.0.jre11.jar
```

### 6. Run the pipeline

Execute the scripts from the project root, in this order:

**Step 1 – SQL Server to Bronze**

```bash
python data_lake/transformations/sqlserver_to_bronze.py
```

**Step 2 – Bronze to Silver**

```bash
python data_lake/transformations/bronze_to_silver.py
```

**Step 3 – Silver to Gold**

```bash
python data_lake/transformations/silver_to_gold.py
```

**Step 4 – Launch the dashboard**

```bash
streamlit run dashboard/app.py
```

## Microsoft Fabric and Azure – Future Architecture

The current implementation runs locally. The architecture is designed to demonstrate concepts that can be applied to Microsoft Fabric and Azure-based data platforms.

| Current implementation | Potential Microsoft equivalent |
|---|---|
| Local Parquet storage | OneLake |
| PySpark transformations | Fabric Notebooks |
| Local medallion architecture | Fabric Lakehouse |
| SQL Server | Azure SQL / SQL Server |
| Python ingestion | Fabric Data Factory / Azure integration services |
| Streamlit dashboard | Power BI |

These are architectural mappings. A cloud deployment has not yet been implemented.

## Future Improvements

Planned development:

- FastAPI-based integration services.
- REST API integration between ERP, CRM, and e-commerce systems.
- Authentication and API error handling.
- Incremental data ingestion.
- Idempotent pipeline execution.
- Automated data quality tests.
- Pipeline logging and monitoring.
- CI/CD and GitHub Actions.
- Microsoft Fabric and Power BI deployment.
- AI-assisted business analytics.

## Project Scope and Disclaimer

Beauty Italia is a fictional business scenario created for technical demonstration and portfolio development.

The current implementation uses a local development environment and sample operational data. It is not a production deployment and does not claim an existing integration with Microsoft Dynamics 365 Business Central or Microsoft Fabric.

The project demonstrates practical experience with SQL Server, Python, PySpark, JDBC, data transformation, analytical data modeling, and dashboard development.

---

**Project:** Beauty Italia – Enterprise Data Integration & Analytics Platform  
**Architecture:** Medallion (Bronze / Silver / Gold)  
**Environment:** Local development on macOS  
**Status:** Core data pipeline and dashboard implemented; integration services planned.