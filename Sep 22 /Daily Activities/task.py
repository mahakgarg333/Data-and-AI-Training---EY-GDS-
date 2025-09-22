import pandas as pd
import matplotlib.pyplot as plt
 
# Sample sales dataset
data = {
    "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "Product": ["Laptop", "Laptop", "Laptop", "Mobile", "Mobile", "Mobile"],
    "Units_Sold": [120, 135, 150, 200, 220, 210],
    "Revenue": [600000, 675000, 750000, 300000, 330000, 315000]
}
 
df = pd.DataFrame(data)
df
import matplotlib.pyplot as plt 
plt.figure(figsize=(10,5)) 
for product in df["Product"].unique():
    product_data = df[df["Product"] == product] 
    plt.bar(product_data["Month"], product_data["Revenue"], label = product) 

plt.title("Revenue per month")
plt.xlabel("Month")
plt.ylabel("Revenue ")
plt.show()
