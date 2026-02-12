import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert all('description' in v for v in data.values())

def test_signup_and_unregister():
    # Use a unique email for test isolation
    email = "pytestuser@mergington.edu"
    activity = next(iter(client.get("/activities").json().keys()))

    # Sign up
    signup = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup.status_code == 200
    assert "signed up" in signup.json().get("message", "").lower()

    # Duplicate signup should fail
    dup = client.post(f"/activities/{activity}/signup?email={email}")
    assert dup.status_code == 400

    # Unregister
    unregister = client.post(f"/activities/{activity}/unregister?email={email}")
    assert unregister.status_code == 200
    assert "removed" in unregister.json().get("message", "").lower() or "unregistered" in unregister.json().get("message", "").lower()

    # Unregister again should fail
    unregister2 = client.post(f"/activities/{activity}/unregister?email={email}")
    assert unregister2.status_code == 400
