import pytest
from fastapi.testclient import TestClient
from courses_api import app

client = TestClient(app)


# Task 1 — Test Course Creation (Positive Case)
def test_create_course_success():
    new_course = {
        "id": 2,
        "title": "Machine Learning",
        "duration": 40,
        "fee": 8000,
        "is_active": True
    }
    response = client.post("/courses", json=new_course)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 2
    assert data["title"] == "Machine Learning"


# Task 2 — Duplicate Course ID Handling
@pytest.mark.parametrize("duplicate_id", [1, 2])
def test_duplicate_course_id(duplicate_id):
    duplicate_course = {
        "id": duplicate_id,
        "title": "Duplicate Course",
        "duration": 20,
        "fee": 2000,
        "is_active": True
    }
    response = client.post("/courses", json=duplicate_course)
    assert response.status_code == 400
    assert response.json()["detail"] == "Course ID already exists"


# Task 3 — Validation Error Testing
def test_course_validation_errors():
    # Title must have at least 3 characters, so we use "AIM" to only test numbers
    invalid_course = {
        "id": 3,
        "title": "AIM",
        "duration": 0,   # invalid (must be >0)
        "fee": -500,     # invalid (must be >0)
        "is_active": True
    }
    response = client.post("/courses", json=invalid_course)
    assert response.status_code == 422
    body = response.text
    # Pydantic v2 uses "greater_than" for this kind of error
    assert "greater_than" in body


# Task 4 — Test GET Returns Correct Format
def test_get_courses_format():
    response = client.get("/courses")
    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert all(isinstance(course, dict) for course in data)
    for course in data:
        assert "id" in course
        assert "title" in course
        assert "duration" in course
        assert "fee" in course
        assert "is_active" in course
