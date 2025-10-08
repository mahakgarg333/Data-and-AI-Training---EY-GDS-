from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# Create FastAPI instance
app = FastAPI()

# Course model with validation
class Course(BaseModel):
    id: int
    title: str = Field(..., min_length=3, max_length=50)
    duration: int = Field(..., gt=0, description="Duration in hours")
    fee: float = Field(..., gt=0)
    is_active: bool = True

# In-memory database (list of courses)
courses = [
    {"id": 1, "title": "Python Basics", "duration": 30, "fee": 3000, "is_active": True},
]

# GET all courses
@app.get("/courses")
def get_all_courses():
    return courses

# POST add new course
@app.post("/courses", status_code=201)
def add_course(course: Course):
    for c in courses:
        if c["id"] == course.id:
            raise HTTPException(status_code=400, detail="Course ID already exists")
    courses.append(course.dict())
    return course
