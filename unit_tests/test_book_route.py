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


def test_book_route_missing_competition(client, setup_data):
    """
    Test booking route with non-existent competition.
    Should return welcome page with error message.
    """
    competition_name = "UnknownComp"  # This doesn't exist
    club_name = "Test Club"  # This exists

    response = client.get(f"/book/{competition_name}/{club_name}")

    # Verify response status code
    assert response.status_code == 200
    # Verify template content
    assert b"welcome.html" in response.data
    assert b"Something went wrong" in response.data


def test_book_route_missing_club(client, setup_data):
    """
    Test booking route with non-existent club.
    Should return welcome page with error message.
    """
    competition_name = "Test Competition"  # This exists
    club_name = "UnknownClub"  # This doesn't exist

    response = client.get(f"/book/{competition_name}/{club_name}")

    # Verify response status code
    assert response.status_code == 200
    # Verify template content
    assert b"welcome.html" in response.data
    assert b"Something went wrong" in response.data
