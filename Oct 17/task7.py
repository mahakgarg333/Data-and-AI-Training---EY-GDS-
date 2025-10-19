import pandas as pd
import schedule
import time
import os
from datetime import datetime
def run_daily_etl():
   try:
       # Ensure reports folder exists
       os.makedirs("reports", exist_ok=True)

       # Step 1: Read input CSVs
       products = pd.read_csv("products.csv")
       customers = pd.read_csv("customers.csv")
       orders = pd.read_csv("orders.csv")

       # Step 2: Join DataFrames
       merged = orders.merge(products, on="ProductID", how="left")
       merged = merged.merge(customers, on="CustomerID", how="left")

       # Step 3: Transformations
       merged["TotalPrice"] = merged["Quantity"] * merged["Price"]
       merged["OrderDate"] = pd.to_datetime(merged["OrderDate"])
       merged["OrderMonth"] = merged["OrderDate"].dt.month

       # Step 4: Save output with timestamp
       today = datetime.now().strftime("%Y_%m_%d")
       filename = f"reports/daily_orders_report_{today}.csv"
       merged.to_csv(filename, index=False)
       print(f" ETL completed and saved to: {filename}")
   except Exception as e:
       print(f"Error during ETL: {str(e)}")


# Uncomment this line below to test the ETL immediately (runs once instantly)
run_daily_etl()

# Schedule ETL daily at 7 AM
#schedule.every().day.at("07:00").do(run_daily_etl)
print("ETL Scheduler started. Waiting for 7:00 AM to run daily...")
while True:
   schedule.run_pending()
   time.sleep(60)

