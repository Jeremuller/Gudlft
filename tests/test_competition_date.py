import pytest
import datetime

from server import clubs, app, get_current_date, competitions


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
    """Fixture to set up initial data for tests."""

    # Copy from original datas to save them
    original_clubs = clubs.copy()
    original_competitions = competitions.copy()

    # Add test datas for club and competition
    clubs.append({"name": "Test Club", "email": "test@club.com", "points": 10})
    # Add competitions with different dates for testing
    competitions.extend(
        [
            {
                "name": "Past Competition",
                "date": "2000-01-01 10:00:00",
                "numberOfPlaces": 10,
            },
            {
                "name": "Future Competition",
                "date": "2030-01-01 10:00:00",
                "numberOfPlaces": 10,
            },
        ]
    )

    yield

    # Restore original datas
    clubs.clear()
    clubs.extend(original_clubs)
    competitions.clear()
    competitions.extend(original_competitions)


def test_current_date():
    """Test that the program correctly identifies the current date."""
    assert get_current_date() == datetime.date.today()


def test_past_competitions_not_included(client, setup_data):
    """
    Test that past competitions are not included in the data returned by the show_summary function.
    Uses the setup_data fixture to ensure we have both past and future competitions.
    """
    response = client.post("/showSummary", data={"email": "test@club.com"})
    assert response.status_code == 200

    # Check that past competition is not displayed
    assert b"Past Competition" not in response.data


def test_upcoming_competitions_included(client, setup_data):
    """
    Test that future competitions are included in the data returned by the show_summary function.
    """
    response = client.post("/showSummary", data={"email": "test@club.com"})
    assert response.status_code == 200

    # Check that future competition is displayed
    assert b"Future Competition" in response.data


def test_added_past_competition_not_displayed(client):
    """
    Test that a past competition is not displayed.
    """
    # Create a past competition
    past_competition = {
        "name": "Past Competition",
        "date": "2020-01-01 10:00:00",
        "numberOfPlaces": "10",
    }

    # Add the past competition to the competitions list
    competitions.append(past_competition)

    # Assume "test@example.com" is an email associated with a valid club
    response = client.post("/showSummary", data={"email": "admin@irontemple.com"})
    assert response.status_code == 200

    # Check that the response does not contain the past competition name
    assert b"Past Competition" not in response.data


def test_added_future_competition_is_displayed(client):
    """
    Test that a future competition is displayed.
    """
    # Create a future competition
    future_competition = {
        "name": "Future Competition",
        "date": "2027-01-01 10:00:00",
        "numberOfPlaces": "10",
    }

    # Add the future competition to the competitions list
    competitions.append(future_competition)

    # Assume "test@example.com" is an email associated with a valid club
    response = client.post("/showSummary", data={"email": "admin@irontemple.com"})
    assert response.status_code == 200

    # Check that the response contains the future competition name
    assert b"Future Competition" in response.data
