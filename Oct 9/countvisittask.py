from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import traceback

app = FastAPI()

# Counter variable
page_hits = 0

# Middleware to count page hits
@app.middleware("http")
async def track_page_hits(req: Request, call_next):
    global page_hits
    page_hits += 1
    print(f"👉 Request number: {page_hits}")
    response = await call_next(req)
    return response

# Dummy student data
student_list = [
    {"id": 1, "name": "Rahul"},
    {"id": 2, "name": "Neha"}
]

@app.get("/students")
def list_students():
    return {"students": student_list}

@app.get("/hits")
def total_hits():
    return {"total_visits": page_hits}
