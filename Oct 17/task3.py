#ETL Module — Order Processing & Analytics
import pandas as pd 

# Load data
products = pd.read_csv("products.csv")
customers = pd.read_csv("customers.csv")
orders = pd.read_csv("orders.csv")

# Merge all tables
merged = orders.merge(customers, on="CustomerID", how="left").merge(products, on="ProductID", how="left")

# Add TotalPrice and OrderMonth
merged["TotalPrice"] = merged["Quantity"] * merged["Price"]
merged["OrderMonth"] = pd.to_datetime(merged["OrderDate"]).dt.month

# Save processed data
merged.to_csv("processed_orders.csv", index=False)
print(" ETL completed and saved as processed_orders.csv")


