import pandas as pd
from datetime import datetime

# Step 1: Extract - Load all three CSV files
products_df = pd.read_csv("products.csv")
customers_df = pd.read_csv("customers.csv")
orders_df = pd.read_csv("orders.csv")

# Optional: Clean column names in case of extra spaces
customers_df.columns = customers_df.columns.str.strip()
orders_df.columns = orders_df.columns.str.strip()
products_df.columns = products_df.columns.str.strip()

# Step 2: Transform - Join datasets
orders_customers = pd.merge(orders_df, customers_df, on="CustomerID", how="inner")
full_data = pd.merge(orders_customers, products_df, on="ProductID", how="inner")

# Add TotalAmount and OrderMonth columns
full_data["TotalAmount"] = full_data["Quantity"] * full_data["Price"]
full_data["OrderMonth"] = pd.to_datetime(full_data["OrderDate"]).dt.month

# Filter: Quantity >= 2 and Country in ["India", "UAE"]
filtered_data = full_data[(full_data["Quantity"] >= 2) & (full_data["Country"].isin(["India", "UAE"]))]

# Step 3: Group and aggregate
category_summary = filtered_data.groupby("Category")["TotalAmount"].sum().reset_index()
segment_summary = filtered_data.groupby("Segment")["TotalAmount"].sum().reset_index()

# Step 4: Sorting & Ranking - Total revenue per customer
customer_revenue = filtered_data.groupby(["CustomerID", "Name"])["TotalAmount"].sum().reset_index()
customer_revenue_sorted = customer_revenue.sort_values(by="TotalAmount", ascending=False)

# Step 5: Load - Save outputs
filtered_data.to_csv("processed_orders.csv", index=False)
category_summary.to_csv("category_summary.csv", index=False)
segment_summary.to_csv("segment_summary.csv", index=False)

# Completion message
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"Sales pipeline completed at {timestamp}")
