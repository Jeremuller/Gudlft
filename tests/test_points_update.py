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

    competition_name = "Spring Festival"
    club_name = "Simply Lift"
    initial_points = int(next(c for c in clubs if c["name"] == club_name)["points"])

    places_to_buy = 3
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
    assert int(updated_club["points"]) == initial_points - places_to_buy

