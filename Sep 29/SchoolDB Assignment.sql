CREATE DATABASE SchooolDB; 
USE SchooolDB; 

CREATE TABLE Teachers(
    teacher_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    subject_id INT
); 

CREATE TABLE Subjects(
    subject_id INT AUTO_INCREMENT PRIMARY KEY,
    subject_name VARCHAR(50)
);

INSERT INTO Subjects (subject_name) VALUES
('Mathematics'),   -- id = 1
('Science'),       -- id = 2
('English'),       -- id = 3
('History'),       -- id = 4
('Geography');     -- id = 5 (no teacher yet) 

INSERT INTO Teachers (name, subject_id) VALUES
('Rahul Sir', 1),   -- Mathematics
('Priya Madam', 2), -- Science
('Arjun Sir', NULL),-- No subject assigned
('Neha Madam', 3);  -- English 

select t.name, t.subject_id, s.subject_name
from Teachers t
inner join Subjects s
on t.subject_id= s.subject_id;
 
 
select t.name, t.subject_id, s.subject_name
from Teachers t
left join Subjects s
on t.subject_id= s.subject_id;
 
 
select t.name, t.subject_id, s.subject_name
from Teachers t
right join Subjects s
on t.subject_id= s.subject_id;
 
 
-- full join
select t.name, t.subject_id, s.subject_name
from Teachers t
left join Subjects s
on t.subject_id= s.subject_id 
union
select t.name, t.subject_id, s.subject_name
from Teachers t
right join Subjects s
on t.subject_id= s.subject_id;
    

