from server import app, competitions, clubs
import pytest


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


def test_book_route_success(client, setup_data):
    """Test successful booking page rendering"""
    competition_name = "Test Competition"
    club_name = "Test Club"

    # Make GET request to book route with test data
    response = client.get(f"/book/{competition_name}/{club_name}")

    # Verify response status code
    assert response.status_code == 200
    # Verify template content
    assert b"Places available" in response.data
    assert competition_name.encode() in response.data
    assert club_name.encode() in response.data



