CREATE DATABASE Office; 
Use Office;
-- Create Employees table
CREATE TABLE Employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    age INT,
    department VARCHAR(50),
    salary DECIMAL(10,2)
);

INSERT INTO Employees (name, age, department, salary)
VALUES ('Mahak Garg', 22, 'Engineering', 40000.00);

INSERT INTO Employees (name, age, department, salary)
VALUES ('Prabhat Choudhary', 24, 'Engineering', 40000.00);

INSERT INTO Employees (name, age, department, salary)
VALUES ('Sneha Kedia', 23, 'Engineering', 40000.00);

SELECT * FROM Employees;

SELECT * FROM Employees
WHERE id = 1;

SELECT * FROM Employees
WHERE department = 'Engineering';

UPDATE Employees
SET salary = 80000.00, department = 'Research and Development'
WHERE id = 1;

DELETE FROM Employees
WHERE id = 1;










