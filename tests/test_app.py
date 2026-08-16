from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    # Arrange
    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert "Chess Club" in response.json()


def test_signup_for_activity():
    # Arrange
    email = "teststudent@mergington.edu"
    activity = "Chess Club"

    # Act
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == (
        f"Signed up {email} for {activity}"
    )


def test_duplicate_signup_is_rejected():
    # Arrange
    email = "duplicate@mergington.edu"
    activity = "Programming Class"

    # Act
    first_response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email},
    )

    second_response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email},
    )

    # Assert
    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == (
        "Student is already signed up"
    )


def test_unregister_participant():
    # Arrange
    email = "remove@mergington.edu"
    activity = "Gym Class"

    client.post(
        f"/activities/{activity}/signup",
        params={"email": email},
    )

    # Act
    response = client.delete(
        f"/activities/{activity}/participants/{email}"
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == (
        f"Unregistered {email} from {activity}"
    )


def test_activity_not_found():
    # Arrange
    activity = "Nonexistent Activity"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert activity not in response.json()