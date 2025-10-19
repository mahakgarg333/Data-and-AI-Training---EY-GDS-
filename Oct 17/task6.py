import pandas as pd, os

os.makedirs("reports", exist_ok=True)
data = pd.read_csv("processed_orders.csv")

# Total revenue by category
rev_category = data.groupby("Category")["TotalPrice"].sum()

# Top 3 customers by spending
top_customers = data.groupby("Name")["TotalPrice"].sum().nlargest(3)

# Monthly revenue trends
monthly = data.groupby("OrderMonth")["TotalPrice"].sum()

# Save reports
rev_category.to_csv("reports/revenue_by_category.csv")
top_customers.to_csv("reports/top_customers.csv")
monthly.to_csv("reports/monthly_trends.csv")

print(" Reports generated inside /reports/")

