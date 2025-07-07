import pytest

from Python_Testing.server import clubs, app, competitions, booked_places


@pytest.fixture
def client():
    """
    Fixture to provide a test client for the Flask application.
    Configures the application in testing mode.
    """
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def setup_data():
    """Fixture to set up initial data for unit_tests."""

    # Copy from original datas to save them
    original_clubs = clubs.copy()
    original_competitions = competitions.copy()
    original_booked_places = booked_places.copy()

    # Add test datas for club and competition
    clubs.append({"name": "Test Club", "email": "test@club.com", "points": 10})
    competitions.append(
        {
            "name": "Test Competition",
            "date": "2026-12-01 10:00:00",
            "numberOfPlaces": 10,
        }
    )

    yield

    # Restore original datas
    clubs.clear()
    clubs.extend(original_clubs)
    competitions.clear()
    competitions.extend(original_competitions)
    booked_places.clear()
    booked_places.update(original_booked_places)


def test_show_summary_with_valid_email(client, setup_data):
    """
    Test the show_summary route with a valid email.
    Verifies that the response status code is 200 and the welcome message is present.
    """
    response = client.post("/showSummary", data={"email": "test@club.com"})
    data = response.data.decode()
    assert response.status_code == 200
    assert "Welcome, test@club.com" in data


def test_show_summary_with_invalid_email(client):
    """
    Test the show_summary route with an invalid email.
    Verifies that the response status code is 200 and the error message for invalid email is present.
    """
    response = client.post("/showSummary", data={"email": "invalid@example.com"})
    data = response.data.decode()
    assert response.status_code == 200
    assert "The email you entered isn&#39;t found, please try again." in data


def test_show_summary_with_missing_email(client):
    """
    Test the show_summary route with missing email data.
    Verifies that the response status code is 200 and the error message for missing email is present.
    """
    response = client.post("/showSummary", data={})
    data = response.data.decode()
    assert response.status_code == 200
    assert "Form isn&#39;t complete, please enter an email address." in data


def test_show_summary_with_booked_places(client, setup_data):
    """Test the show_summary route with booked places information."""
    # Add booked places for testing purpose
    booked_places[("Test Club", "Test Competition")] = 5

    response = client.post("/showSummary", data={"email": "test@club.com"})
    data = response.data.decode()

    # Verify the response contains the expected information
    assert response.status_code == 200
    assert "Welcome, test@club.com" in data
    assert "Test Competition" in data
    assert "Places already booked: 5 / 12" in data
