
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]

ORDER_PATH = PROJECT_ROOT / "data_lake" / "gold" / "order_sales"
PRODUCT_PATH = PROJECT_ROOT / "data_lake" / "gold" / "product_sales"

# Page configuration
st.set_page_config(
    page_title="Beauty Italia | Sales Analytics",
    page_icon="💄",
    layout="wide"
)

# Load Gold datasets
@st.cache_data
def load_data():
    orders = pd.read_parquet(ORDER_PATH)
    products = pd.read_parquet(PRODUCT_PATH)

    orders["OrderDate"] = pd.to_datetime(orders["OrderDate"])
    orders["TotalRevenue"] = pd.to_numeric(orders["TotalRevenue"])

    return orders, products


orders, products = load_data()

# Dashboard title
st.title("💄 Beauty Italia - Sales Analytics")
st.caption("Enterprise Data Integration Platform | Gold Layer")

# Sidebar filters
st.sidebar.header("Dashboard Filters")

channels = st.sidebar.multiselect(
    "Sales Channel",
    options=sorted(orders["OrderSource"].unique()),
    default=sorted(orders["OrderSource"].unique())
)

statuses = st.sidebar.multiselect(
    "Order Status",
    options=sorted(orders["OrderStatus"].unique()),
    default=sorted(orders["OrderStatus"].unique())
)

filtered_orders = orders[
    orders["OrderSource"].isin(channels)
    & orders["OrderStatus"].isin(statuses)
]

# KPI calculations
total_revenue = filtered_orders["TotalRevenue"].sum()
total_orders = filtered_orders["OrderID"].nunique()
total_units = filtered_orders["TotalQuantity"].sum()
average_order_value = (
    total_revenue / total_orders if total_orders else 0
)

# KPI cards
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"€{total_revenue:,.2f}")
col2.metric("Total Orders", f"{total_orders:,}")
col3.metric("Units Sold", f"{total_units:,}")
col4.metric("Average Order Value", f"€{average_order_value:,.2f}")

st.divider()

# Revenue by channel
channel_sales = (
    filtered_orders.groupby("OrderSource", as_index=False)
    ["TotalRevenue"].sum()
)

# Revenue by status
status_sales = (
    filtered_orders.groupby("OrderStatus", as_index=False)
    ["TotalRevenue"].sum()
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Revenue by Sales Channel")

    fig_channel = px.pie(
        channel_sales,
        names="OrderSource",
        values="TotalRevenue",
        hole=0.45
    )

    st.plotly_chart(fig_channel, use_container_width=True)

with col2:
    st.subheader("Revenue by Order Status")

    fig_status = px.bar(
        status_sales,
        x="OrderStatus",
        y="TotalRevenue",
        text_auto=".2f",
        title="Revenue (€)"
    )

    st.plotly_chart(fig_status, use_container_width=True)

# Product performance
st.subheader("Product Performance")

fig_product = px.bar(
    products.sort_values("TotalRevenue", ascending=True),
    x="TotalRevenue",
    y="ProductID",
    orientation="h",
    text_auto=".2f",
    labels={
        "TotalRevenue": "Revenue (€)",
        "ProductID": "Product ID"
    }
)

st.plotly_chart(fig_product, use_container_width=True)

# Order details
st.subheader("Order Details")

st.dataframe(
    filtered_orders[
        [
            "OrderID",
            "OrderSource",
            "OrderStatus",
            "OrderDate",
            "TotalQuantity",
            "TotalRevenue"
        ]
    ].sort_values("OrderDate", ascending=False),
    use_container_width=True,
    hide_index=True
)

st.caption("Data source: Beauty Italia Gold Layer | PySpark + Parquet")
