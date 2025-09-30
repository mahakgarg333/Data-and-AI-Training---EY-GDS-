CREATE DATABASE Hospital;
USE Hospital;

CREATE TABLE Patients(
patient_id INT PRIMARY KEY,
name VARCHAR(50),
age INT,
gender CHAR(1),
city VARCHAR(50) 
); 


CREATE TABLE Doctors(
doctor_id INT PRIMARY KEY,
name VARCHAR(50),
specialization VARCHAR(50),
experience INT
); 


CREATE TABLE Appointments(
appointment_id INT PRIMARY KEY,
patient_id INT ,
doctor_id INT ,
appointment_date DATE,
status VARCHAR(20), 
FOREIGN KEY (patient_id) REFERENCES Patients(patient_id),
FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id)
); 

CREATE TABLE MedicalRecords(
record_id INT PRIMARY KEY,
patient_id INT ,
doctor_id INT ,
diagnosis VARCHAR(100),
treatment VARCHAR(100),
date DATE, 
FOREIGN KEY (patient_id) REFERENCES Patients(patient_id),
FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id)
); 

CREATE TABLE Billing(
bill_id INT PRIMARY KEY,
patient_id INT ,
amount DECIMAL(10,2),
bill_date DATE,
status VARCHAR(20), 
FOREIGN KEY (patient_id) REFERENCES Patients(patient_id)
); 


-- Patients
INSERT INTO Patients VALUES
(1, 'Amit Sharma', 30, 'M', 'Delhi'),
(2, 'Priya Singh', 25, 'F', 'Mumbai'),
(3, 'Rajesh Kumar', 40, 'M', 'Bangalore'),
(4, 'Sneha Patel', 35, 'F', 'Ahmedabad'),
(5, 'Karan Mehta', 28, 'M', 'Chennai'),
(6, 'Anjali Gupta', 32, 'F', 'Hyderabad'),
(7, 'Vikram Joshi', 45, 'M', 'Pune'),
(8, 'Neha Reddy', 22, 'F', 'Kolkata'),
(9, 'Rohit Verma', 38, 'M', 'Surat'),
(10, 'Sonal Kapoor', 29, 'F', 'Jaipur');

-- Doctors
INSERT INTO Doctors VALUES
(1, 'Dr. Ashok Rao', 'Cardiology', 15),
(2, 'Dr. Meera Iyer', 'Orthopedics', 10),
(3, 'Dr. Rakesh Singh', 'Pediatrics', 12),
(4, 'Dr. Kavita Sharma', 'Neurology', 20),
(5, 'Dr. Sanjay Patel', 'General Medicine', 8);

-- Appointments
INSERT INTO Appointments VALUES
(1, 1, 1, '2025-10-01', 'Scheduled'),
(2, 2, 2, '2025-10-03', 'Completed'),
(3, 3, 3, '2025-10-05', 'Cancelled'),
(4, 4, 1, '2025-10-07', 'Scheduled'),
(5, 5, 4, '2025-10-08', 'Completed'),
(6, 6, 5, '2025-10-10', 'Scheduled'),
(7, 7, 2, '2025-10-11', 'Completed'),
(8, 8, 3, '2025-10-12', 'Scheduled'),
(9, 9, 4, '2025-10-13', 'Scheduled'),
(10, 10, 5, '2025-10-14', 'Completed');

-- Medical Records
INSERT INTO MedicalRecords VALUES
(1, 1, 1, 'Hypertension', 'Medication', '2025-10-01'),
(2, 2, 2, 'Fracture', 'Cast application', '2025-10-03'),
(3, 3, 3, 'Flu', 'Rest and fluids', '2025-10-05'),
(4, 4, 1, 'Arrhythmia', 'Medication', '2025-10-07'),
(5, 5, 4, 'Migraine', 'Painkillers', '2025-10-08');

-- Billing
INSERT INTO Billing VALUES
(1, 1, 5000.00, '2025-10-02', 'Paid'),
(2, 2, 12000.00, '2025-10-04', 'Unpaid'),
(3, 3, 1500.00, '2025-10-06', 'Paid'),
(4, 4, 7000.00, '2025-10-08', 'Paid'),
(5, 5, 3500.00, '2025-10-09', 'Unpaid');

-- List all patients assigned to a cardiologist. 
SELECT DISTINCT p.patient_id, p.name, p.age, p.gender, p.city
FROM Patients p
JOIN Appointments a ON p.patient_id = a.patient_id
JOIN Doctors d ON a.doctor_id = d.doctor_id
WHERE d.specialization = 'Cardiology';

-- Find all the appointments of a doctor 
SELECT appointment_id, patient_id, appointment_date, status
FROM Appointments
WHERE doctor_id = 1;

-- Show unpaid bills of patients
SELECT b.bill_id, b.patient_id, p.name, b.amount, b.bill_date, b.status
FROM Billing b
JOIN Patients p ON b.patient_id = p.patient_id
WHERE b.status = 'Unpaid';

-- Procedures 
DELIMITER $$

CREATE PROCEDURE GetPatientHistory(IN p_patient_id INT)
BEGIN
    SELECT 
        mr.record_id,
        mr.date AS visit_date,
        d.name AS doctor_name,
        mr.diagnosis,
        mr.treatment
    FROM MedicalRecords mr
    JOIN Doctors d ON mr.doctor_id = d.doctor_id
    WHERE mr.patient_id = p_patient_id
    ORDER BY mr.date DESC;
END $$

DELIMITER ;

-- Procedures 



DELIMITER $$

CREATE PROCEDURE GetDoctorAppointments(IN p_doctor_id INT)
BEGIN
    SELECT 
        a.appointment_id,
        p.name AS patient_name,
        a.appointment_date,
        a.status
    FROM Appointments a
    JOIN Patients p ON a.patient_id = p.patient_id
    WHERE a.doctor_id = p_doctor_id
    ORDER BY a.appointment_date DESC;
END $$

DELIMITER ;


