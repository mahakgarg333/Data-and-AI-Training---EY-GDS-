

#7 oct
from fastapi import FastAPI

#Create fastapi instance
app = FastAPI()

#root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}

#Path Parameter example
@app.get("/students/{student_id}")
def get_student(student_id: int):
    return {"student_id": student_id, "name":"rahul", "course":"AI"}


#GET
@app.get("/students")
def get_students():
    return {"This is a get request!"}


#POST
@app.post("/students")
def create_students():
    return {"This is a post request!"}

#PUT
@app.put("/students")
def update_students():
    return {"This is a put request!"}

#DELETE
@app.delete("/students")
def delete_students():
    return {"This is a delete request!"}
