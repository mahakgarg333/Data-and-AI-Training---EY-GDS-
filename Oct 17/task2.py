from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd

app = FastAPI()

# Load initial data
products = pd.read_csv("products.csv").to_dict(orient="records")
customers = pd.read_csv("customers.csv").to_dict(orient="records")

class Product(BaseModel):
    ProductID: str
    ProductName: str
    Category: str
    Price: float

class Customer(BaseModel):
    CustomerID: str
    Name: str
    Email: str
    Country: str

# ---------------- PRODUCTS -----------------
#get - fetch
@app.get("/products")
def get_products():
    return products

#post - add
@app.post("/products")
def add_product(product: Product):
    products.append(product.dict())
    return {"message": "Product added successfully"}

#put - update
@app.put("/products/{product_id}")
def update_product(product_id: str, updated_product: Product):
    for p in products:
        if p["ProductID"] == product_id:
            p.update(updated_product.dict())
            return {"message": "Product updated successfully"}
    raise HTTPException(status_code=404, detail="Product not found")

@app.delete("/products/{product_id}")
def delete_product(product_id: str):
    global products
    products = [p for p in products if p["ProductID"] != product_id]
    return {"message": "Product deleted successfully"}

# ---------------- CUSTOMERS -----------------
@app.get("/customers")
def get_customers():
    return customers

@app.post("/customers")
def add_customer(customer: Customer):
    customers.append(customer.dict())
    return {"message": "Customer added successfully"}

@app.put("/customers/{customer_id}")
def update_customer(customer_id: str, updated_customer: Customer):
    for c in customers:
        if c["CustomerID"] == customer_id:
            c.update(updated_customer.dict())
            return {"message": "Customer updated successfully"}
    raise HTTPException(status_code=404, detail="Customer not found")

@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: str):
    global customers
    customers = [c for c in customers if c["CustomerID"] != customer_id]
    return {"message": "Customer deleted successfully"}
