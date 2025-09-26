CREATE DATABASE SchoolDB;

USE SchoolDB;

CREATE TABLE Students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    age INT,
    course VARCHAR(50),
    marks INT
);
INSERT INTO Students (name, age, course, marks)
VALUES ('Rahul', 21, 'AI', 85);

INSERT INTO Students (name, age, course, marks)
VALUES
    ('Priya', 22, 'ML', 90),
    ('Arjun', 20, 'Data Science', 78);

SELECT * FROM Students;

# CRUD -- Create, Read, Update & Delete 
-- Select all 
Select * from Students; 
-- Select specific columns 
Select name, age from Students; 

Select name from Students Where marks >90;

UPDATE students 
SET marks = 95 , course = 'Advanced AI' 
WHERE id = 4;

DELETE FROM Students WHERE id =3;



