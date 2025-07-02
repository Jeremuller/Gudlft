import pytest

from server import clubs, app, competitions, booked_places


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

    # Copy from original datas
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


def test_display_all_club_names_and_points(client):
    """
    Test that all clubs and their points are correctly displayed on the welcome page.
    """
    response = client.get("/")
    assert response.status_code == 200

    for club in clubs:
        expected_display = f"{club['name']} - Points: {club['points']}"
        assert expected_display.encode() in response.data
