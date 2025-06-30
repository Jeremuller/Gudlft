import pytest

from server import clubs, app, competitions


@pytest.fixture
def client():
    """
    Fixture to provide a test client for the Flask application.
    Configures the application in testing mode.
    """
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_initialization_of_booking_tracking():
    """
    Test that the booking tracking is correctly initialized.
    """
    assert isinstance(booked_places, dict)
    assert len(booked_places) == 0


def test_track_places_booked_by_clubs(client):
    """
    Test that the system correctly tracks the number of places booked by a club for a competition.
    Performing two successive purchases to test if the datas are correctly tracked.
    """
    competition_name = "Spring Festival"
    club_name = "Simply Lift"

    # Initial setup
    club = next(c for c in clubs if c["name"] == club_name)
    # Sufficient points for testing
    club["points"] = "50"

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
