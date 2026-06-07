from copy import deepcopy

from fastapi.testclient import TestClient

from src import app as application

original_activities = deepcopy(application.activities)

client = TestClient(application.app)


def setup_function():
    application.activities = deepcopy(original_activities)


def test_get_activities_returns_activity_list():
    # Arrange
    url = "/activities"

    # Act
    response = client.get(url)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert data["Chess Club"]["schedule"] == "Fridays, 3:30 PM - 5:00 PM"


def test_signup_for_activity_returns_success_message():
    # Arrange
    activity_name = "Chess Club"
    email = "teststudent@mergington.edu"
    url = f"/activities/{activity_name}/signup?email={email}"

    # Act
    response = client.post(url)

    # Assert
    assert response.status_code == 200
    result = response.json()
    assert result["message"] == f"Signed up {email} for {activity_name}"
    assert email in application.activities[activity_name]["participants"]


def test_signup_for_missing_activity_returns_404():
    # Arrange
    activity_name = "Nonexistent Club"
    email = "teststudent@mergington.edu"
    url = f"/activities/{activity_name}/signup?email={email}"

    # Act
    response = client.post(url)

    # Assert
    assert response.status_code == 404
    error = response.json()
    assert error["detail"] == "Activity not found"
