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


def test_booking_places_update_club_points(client):
    """
    Test the purchase of places and verify the club points are correctly updated.
    """

    # Define competition and club for the test
    competition_name = "Spring Festival"
    club_name = "Simply Lift"

    # Retrieve initial points of the club and define the number of places to buy
    initial_points = int(next(c for c in clubs if c["name"] == club_name)["points"])
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

    # Set initial points and places for the test
    club = next(c for c in clubs if c["name"] == club_name)
    # Sufficient points
    club["points"] = "10"
    competition = next(c for c in competitions if c["name"] == competition_name)
    # Sufficient places
    competition["numberOfPlaces"] = "10"

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
    # Places should be deducted
    assert int(updated_competition["numberOfPlaces"]) == 5
    updated_club = next(c for c in clubs if c["name"] == club_name)
    # Points should be deducted
    assert int(updated_club["points"]) == 5
