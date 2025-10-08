from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# ---test 1
def test_get_all_employees():
    response = client.get("/employees")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

from fastapi.testclient import TestClient
from main import app  # import your FastAPI app

client = TestClient(app)

# --------------------- TEST 2 ---------------------
def test_add_employee():
    new_emp = {
        "id": 2,
        "name": "Neha Verma",
        "department": "IT",
        "salary": 60000
    }

    response = client.post(url="/employees", json=new_emp)
    assert response.status_code == 201
    assert response.json()["employee"] == newemp


# --------------------- TEST 3 ---------------------
def test_get_employee_by_id():
    response = client.get("/employees/1")
    assert response.status_code == 200
    assert response.json()["name"] == "RaONE"


# --------------------- TEST 4 ---------------------
def test_get_employee_not_found():
    response = client.get("/employees/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Employee not found"


# Test 5
def test_update_employee():
    up_emp = {"id": 1, "name": "Meena", "dept": "AI", "salary": 50000.00}
    response = client.put("/employees/1", json=up_emp)
    assert response.status_code == 200
    assert response.json()["name"] == "Meena"


# Test 6
def test_delete_employee():
    response = client.delete("/employees/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Employee Deleted Successfully"


