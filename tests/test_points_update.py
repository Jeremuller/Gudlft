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


def test_booking_places_update_club_points(client):
    """
    Test the purchase of places and verify the club points are correctly updated.
    """

    # Define competition and club for the test
    competition_name = "Spring Festival"
    club_name = "Simply Lift"

    # Set initial points and places for the test
    club = next(c for c in clubs if c["name"] == club_name)
    # Sufficient points for the purchase
    club["points"] = "10"
    competition = next(c for c in competitions if c["name"] == competition_name)
    # Sufficient places for the purchase
    competition["numberOfPlaces"] = "10"

    # Reset the booked places for this specific club and competition
    booked_places[(club_name, competition_name)] = 0

    # Retrieve initial points of the club and define the number of places to buy
    initial_points = int(club["points"])
    places_to_buy = 3

    # Simulate a POST request to purchase places
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competition_name,
            "club": club_name,
            "places": str(places_to_buy),
        },
    )

    # Verify the response status code is successful
    assert response.status_code == 200

    # Retrieve the updated club details
    updated_club = next(c for c in clubs if c["name"] == club_name)

    #  Verify the club points are correctly updated after purchase
    assert int(updated_club["points"]) == initial_points - places_to_buy


def test_club_points_cannot_go_below_zero(client):
    """
    Test that a club cannot have negative points after purchasing places.
    """

    # Define competition and club for the test
    competition_name = "Spring Festival"
    club_name = "Simply Lift"

    # Set the club's points to a low value for testing
    club = next(c for c in clubs if c["name"] == club_name)
    club["points"] = "3"

    # Attempt to purchase more places than the club has points for
    places_to_buy = 5
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competition_name,
            "club": club_name,
            "places": str(places_to_buy),
        },
    )

    # Verify the response status code is successful
    assert response.status_code == 200

    # Verify that the club's points have not changed (should still be 3)
    updated_club = next(c for c in clubs if c["name"] == club_name)
    # Points should remain unchanged
    assert int(updated_club["points"]) == 3


def test_successful_purchase_with_enough_points(client):
    """
    Test that a purchase is successful when the club has enough points.
    """
    # Define competition and club for the test
    competition_name = "Spring Festival"
    club_name = "Simply Lift"

    # Reset the booked places for this specific club and competition
    booked_places[(club_name, competition_name)] = 0

    club = next(c for c in clubs if c["name"] == club_name)
    # Set initial points to a sufficient value
    club["points"] = "10"

    # Attempt to purchase
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
    updated_club = next(c for c in clubs if c["name"] == club_name)
    # Points should be deducted
    assert int(updated_club["points"]) == 5


def test_successful_purchase_without_enough_points(client):
    """
    Test that a purchase is successful when the club has enough points.
    """
    # Define competition and club for the test
    competition_name = "Spring Festival"
    club_name = "Simply Lift"

    # Reset the booked places for this specific club and competition
    booked_places[(club_name, competition_name)] = 0

    club = next(c for c in clubs if c["name"] == club_name)
    # Set initial points to a low value
    club["points"] = "3"

    # Attempt to purchase
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
    updated_club = next(c for c in clubs if c["name"] == club_name)
    # Points should be deducted
    assert int(updated_club["points"]) == 3


def test_successful_purchase_with_enough_places(client):
    """
    Test that a purchase is successful when there are enough places available.
    """
    competition_name = "Spring Festival"
    club_name = "Simply Lift"

    # Reset the booked places for this specific club and competition
    booked_places[(club_name, competition_name)] = 0

    # Set initial points and places for the test
    club = next(c for c in clubs if c["name"] == club_name)
    # Sufficient points
    club["points"] = "10"

    competition = next(c for c in competitions if c["name"] == competition_name)
    # Sufficient places
    competition["numberOfPlaces"] = "10"

    # Debug print before purchase
    print("Before purchase - Club points:", club["points"])
    print("Before purchase - Competition places:", competition["numberOfPlaces"])

    places_to_buy = 5
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competition_name,
            "club": club_name,
            "places": str(places_to_buy),
        },
    )

    # Debug print after purchase
    updated_competition = next(c for c in competitions if c["name"] == competition_name)
    updated_club = next(c for c in clubs if c["name"] == club_name)
    print("After purchase - Club points:", updated_club["points"])
    print("After purchase - Competition places:", updated_competition["numberOfPlaces"])

    assert response.status_code == 200
    updated_competition = next(c for c in competitions if c["name"] == competition_name)
    # Places should be deducted
    assert int(updated_competition["numberOfPlaces"]) == 5
    updated_club = next(c for c in clubs if c["name"] == club_name)
    # Points should be deducted
    assert int(updated_club["points"]) == 5


def test_purchase_with_insufficient_places(client):
    """
    Test that a purchase fails when there are not enough places available.
    """
    competition_name = "Spring Festival"
    club_name = "Simply Lift"

    # Set initial points and places for the test
    club = next(c for c in clubs if c["name"] == club_name)
    # Sufficient points
    club["points"] = "10"
    competition = next(c for c in competitions if c["name"] == competition_name)
    # Insufficient places
    competition["numberOfPlaces"] = "3"

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
    updated_competition = next(c for c in competitions if c["name"] == competition_name)
    # Places should remain unchanged
    assert int(updated_competition["numberOfPlaces"]) == 3
    updated_club = next(c for c in clubs if c["name"] == club_name)
    # Points should remain unchanged
    assert int(updated_club["points"]) == 10
