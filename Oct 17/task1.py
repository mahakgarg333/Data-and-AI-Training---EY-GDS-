#CRUD + Database Module — Product & Customer Management
import sqlite3
import pandas as pd

# Connect to a new database
conn = sqlite3.connect('ordersystem.db')
cursor = conn.cursor()

# Create products table
cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    ProductID TEXT PRIMARY KEY,
    ProductName TEXT,
    Category TEXT,
    Price REAL
)
''')

# Create customers table
cursor.execute('''
CREATE TABLE IF NOT EXISTS customers (
    CustomerID TEXT PRIMARY KEY,
    Name TEXT,
    Email TEXT,
    Country TEXT
)
''')

conn.commit()

# Read data from CSV files
products = pd.read_csv(r"products.csv")
customers = pd.read_csv(r"customers.csv")

# Load data into the database
products.to_sql('products', conn, if_exists='replace', index=False)
customers.to_sql('customers', conn, if_exists='replace', index=False)

print("Initial data inserted successfully")

# 1. Add a new product
cursor.execute(
    "INSERT INTO products VALUES (?, ?, ?, ?)",
    ('P105', 'Smartwatch', 'Electronics', 150)
)
conn.commit()
print("New product added successfully")

# 2. Update product price
cursor.execute(
    "UPDATE products SET Price = ? WHERE ProductID = ?",
    (900, 'P101')
)
conn.commit()
print("Product price updated successfully")

# 3. Delete a customer
cursor.execute(
    "DELETE FROM customers WHERE CustomerID = ?",
    ('C002',)
)
conn.commit()
print("Customer deleted successfully")

# 4. List all customers from India
cursor.execute("SELECT * FROM customers WHERE Country = 'India'")
rows = cursor.fetchall()
print("\nCustomers from India:")
for row in rows:
    print(row)

# Display final data
print("\nProducts Table:")
print(pd.read_sql("SELECT * FROM products", conn))

print("\nCustomers Table:")
print(pd.read_sql("SELECT * FROM customers", conn))

# Close connection
conn.close()
