CREATE DATABASE RetailDB; 
USE RetailDB; 

CREATE TABLE Customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50), 
    city VARCHAR(50), 
    phone VARCHAR(15)
);

CREATE TABLE Productss (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(50), 
    category VARCHAR(50), 
    price DECIMAL(10,2)
); 

-- Drop the correct table
DROP TABLE IF EXISTS Productss;

CREATE TABLE Orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT, 
    order_date DATE, 
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
); 

CREATE TABLE OrderDetailss (
    orderDetail_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (product_id) REFERENCES Productss(product_id)  -- Fixed reference to Productss
);

-- Inserting data into Customers
INSERT INTO Customers (name, city, phone) VALUES
('Rahul', 'Mumbai', '9876543210'),
('Priya', 'Delhi', '9876501234'),
('Arjun', 'Bengaluru', '9876512345'),
('Neha', 'Hyderabad', '9876523456');

-- Inserting data into Productss
INSERT INTO Productss (product_name, category, price) VALUES
('Laptop', 'Electronics', 60000.00),
('Smartphone', 'Electronics', 30000.00),
('Headphones', 'Accessories', 2000.00),
('Shoes', 'Fashion', 3500.00),
('T-Shirt', 'Fashion', 1200.00);

-- Inserting data into Orders
INSERT INTO Orders (customer_id, order_date) VALUES
(1, '2025-09-01'),
(2, '2025-09-02'),
(3, '2025-09-03'),
(1, '2025-09-04');

-- Inserting data into OrderDetailss
INSERT INTO OrderDetailss (order_id, product_id, quantity) VALUES
(1, 1, 1),   -- Rahul bought 1 Laptop
(1, 3, 2),   -- Rahul bought 2 Headphones
(2, 2, 1),   -- Priya bought 1 Smartphone
(3, 4, 1),   -- Arjun bought 1 Shoes 
(4, 5, 3);   -- Rahul bought 3 T-Shirts
