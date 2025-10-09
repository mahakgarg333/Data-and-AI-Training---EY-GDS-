# main.py
import time
import asyncio
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse, HTMLResponse
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()


class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        response: Response = await call_next(request)
        elapsed = time.perf_counter() - start
        # Put elapsed seconds (float) in header
        response.headers["X-Process-Time"] = f"{elapsed:.6f}"
        return response


app.add_middleware(TimingMiddleware)

# Sample data: five students
STUDENTS = [
    {"id": 1, "name": "Asha Sharma", "age": 20, "class": "B.Tech"},
    {"id": 2, "name": "Ravi Kumar", "age": 21, "class": "B.Sc"},
    {"id": 3, "name": "Sana Verma", "age": 19, "class": "BCA"},
    {"id": 4, "name": "Vikram Singh", "age": 22, "class": "B.Tech"},
    {"id": 5, "name": "Neha Patel", "age": 20, "class": "B.A"},
]


@app.get("/students")
async def get_students():
    # simulate processing time (non-blocking)
    await asyncio.sleep(1)  # <-- "let it sleep for some time"
    return JSONResponse(content=STUDENTS)


# Simple HTML UI that calls /students (same origin)
INDEX_HTML = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <title>Students API Demo</title>
  <style>
    body { font-family: system-ui, -apple-system, "Segoe UI", Roboto, Arial; padding: 1.5rem; }
    #students { margin-top: 1rem; }
    .student { padding: .5rem; border-bottom: 1px solid #eee; }
    .header { display:flex; gap:1rem; align-items:center; }
    button { padding:.5rem 1rem; border-radius:6px; border:1px solid #ccc; cursor:pointer; }
    pre { background:#f8f8f8; padding: .75rem; border-radius:6px; overflow:auto; }
  </style>
</head>
<body>
  <h1>Students API — Demo</h1>
  <div class="header">
    <button id="loadBtn">Load students</button>
    <div><strong>Response time:</strong> <span id="time">—</span> seconds</div>
  </div>

  <div id="students"></div>

  <script>
    const btn = document.getElementById('loadBtn');
    const studentsDiv = document.getElementById('students');
    const timeEl = document.getElementById('time');

    async function loadStudents() {
      studentsDiv.innerHTML = 'Loading...';
      timeEl.textContent = '—';
      try {
        const res = await fetch('/students');
        const processTimeHeader = res.headers.get('X-Process-Time');
        if (processTimeHeader !== null) {
          timeEl.textContent = Number(processTimeHeader).toFixed(3);
        } else {
          timeEl.textContent = 'header missing';
        }

        if (!res.ok) {
          studentsDiv.innerHTML = `<div style="color:crimson">Error: ${res.status}</div>`;
          return;
        }
        const students = await res.json();
        if (!Array.isArray(students)) {
          studentsDiv.innerHTML = '<div>No students returned</div>';
          return;
        }
        studentsDiv.innerHTML = students.map(s => 
          `<div class="student"><strong>${s.name}</strong> (id: ${s.id}) — ${s.class}, age ${s.age}</div>`
        ).join('');
      } catch (err) {
        studentsDiv.innerHTML = `<div style="color:crimson">Fetch failed: ${err}</div>`;
      }
    }

    btn.addEventListener('click', loadStudents);

    // optional: auto-load once on open
    // loadStudents();
  </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def index():
    return HTMLResponse(content=INDEX_HTML, status_code=200)
