--done in sql
-- Create Database
CREATE DATABASE RetailSystem;
USE RetailSystem;

-- Create Products Table
CREATE TABLE products (
    ProductID VARCHAR(10) PRIMARY KEY,
    ProductName VARCHAR(100),
    Category VARCHAR(50),
    Price DECIMAL(10,2)
);

-- Create Customers Table
CREATE TABLE customers (
    CustomerID VARCHAR(10) PRIMARY KEY,
    Name VARCHAR(100),
    Email VARCHAR(100),
    Country VARCHAR(50)
);

-- Insert Initial Data
INSERT INTO products VALUES
('P101', 'Laptop', 'Electronics', 800),
('P102', 'Mouse', 'Accessories', 20),
('P103', 'Keyboard', 'Accessories', 35),
('P104', 'Headphones', 'Audio', 50);

INSERT INTO customers VALUES
('C001', 'Neha', 'neha@example.com', 'India'),
('C002', 'Ali', 'ali@example.com', 'UAE'),
('C003', 'Sophia', 'sophia@example.com', 'UK');

-- CRUD Operations

-- 1. Add a new product
INSERT INTO products VALUES ('P105', 'Smartwatch', 'Electronics', 120);

-- 2. Update product price
UPDATE products SET Price = 850 WHERE ProductID = 'P101';

-- 3. Delete a customer
DELETE FROM customers WHERE CustomerID = 'C002';

-- 4. List all customers from India
SELECT * FROM customers WHERE Country = 'India';
