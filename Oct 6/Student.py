from pydantic import BaseModel

#define a model(named schema)
class Student(BaseModel):
    name : str
    age :int
    email : str
    is_active: bool= True

data = {"name": "Ali", "age": 20, "email": "ali@gmail.com"}
student = Student(**data)
print(student.name)
