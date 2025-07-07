import pytest

from Python_Testing.server import (
    clubs,
    app,
    competitions,
    get_booked_places,
    booked_places,
)


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


def test_initialization_of_booking_tracking(setup_data):
    """
    Test that the booking tracking is correctly initialized.
    """
    assert isinstance(booked_places, dict)
    assert len(booked_places) == 0


def test_track_places_booked_by_clubs(client, setup_data):
    """
    Test that the system correctly tracks the number of places booked by a club for a competition.
    Performing two successive purchases to test if the datas are correctly tracked.
    """
    competition_name = "Test Competition"
    club_name = "Test Club"

    # First booking
    places_to_buy = 5
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competition_name,
            "club": club_name,
            "places": str(places_to_buy),
        },
    )
    assert response.status_code == 200

    # Check if the booking is tracked correctly
    assert get_booked_places(club_name, competition_name) == places_to_buy

    # Second booking
    additional_places_to_buy = 3
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competition_name,
            "club": club_name,
            "places": str(additional_places_to_buy),
        },
    )
    assert response.status_code == 200

    # Check if the total booking is tracked correctly
    assert (
        get_booked_places(club_name, competition_name)
        == places_to_buy + additional_places_to_buy
    )


@pytest.mark.parametrize(
    "initial_places, places_to_buy, expected_total",
    [
        (0, 10, 10),  # Test successful purchase within limit
        (10, 2, 12),  # Test purchase reaching the limit
        (12, 1, 12),  # Test purchase exceeding the limit
    ],
)
def test_purchase_places_limits(
    client, setup_data, initial_places, places_to_buy, expected_total
):
    """
    Parametrized test for different purchase scenarios.
    Tests successful purchases, reaching the limit, and exceeding the limit.
    """
    competition_name = "Test Competition"
    club_name = "Test Club"

    # Set initial points and places
    club = next(c for c in clubs if c["name"] == club_name)
    # Sufficient points for testing
    club["points"] = "50"

    competition = next(c for c in competitions if c["name"] == competition_name)
    # Sufficient places for testing
    competition["numberOfPlaces"] = 50

    # Set initial booked places if needed
    if initial_places > 0:
        booked_places[(club_name, competition_name)] = initial_places

    # Attempt to book places
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competition_name,
            "club": club_name,
            "places": str(places_to_buy),
        },
    )
    assert response.status_code == 200
    assert get_booked_places(club_name, competition_name) == expected_total
