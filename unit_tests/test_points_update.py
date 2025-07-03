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


@pytest.mark.parametrize(
    "initial_points, competition_places, places_to_buy, expected_points, expected_comp_places, should_succeed",
    [
        # Normal cases
        (10, 10, 3, 7, 7, True),  # Normal purchase
        (10, 10, 5, 5, 5, True),  # Half purchase
        # Limit cases
        (10, 10, 10, 0, 0, True),  # Attempting to buy every places
        (3, 10, 3, 0, 7, True),  # Purchasing with all club points
        (10, 3, 3, 7, 0, True),  # Buying every available places
        # Fail cases
        (3, 10, 5, 3, 10, False),  # Not enough points
        (10, 3, 5, 10, 3, False),  # Not enough places
        (2, 3, 5, 2, 3, False),  # Not enough points and places
        (0, 10, 1, 0, 10, False),  # No point
        (10, 0, 1, 10, 0, False),  # No place
    ],
)
def test_parametrized_purchase_scenarios(
    client,
    setup_data,
    initial_points,
    competition_places,
    places_to_buy,
    expected_points,
    expected_comp_places,
    should_succeed,
):
    """
    Comprehensive parametrized test for all purchase scenarios.
    Tests combinations of club points and competition places.
    """
    competition_name = "Test Competition"
    club_name = "Test Club"

    # Get and update test club and competition
    club = next(c for c in clubs if c["name"] == club_name)
    competition = next(c for c in competitions if c["name"] == competition_name)

    # Set initial values
    club["points"] = str(initial_points)
    competition["numberOfPlaces"] = str(competition_places)

    # Make purchase
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competition_name,
            "club": club_name,
            "places": str(places_to_buy),
        },
    )

    # Verify response status
    assert response.status_code == 200

    # Get updated values
    updated_club = next(c for c in clubs if c["name"] == club_name)
    updated_competition = next(c for c in competitions if c["name"] == competition_name)

    # Verify results based on expected success
    if should_succeed:
        # For successful purchases
        assert int(updated_club["points"]) == expected_points
        assert int(updated_competition["numberOfPlaces"]) == expected_comp_places
    else:
        # For failed purchases (values should remain unchanged)
        assert int(updated_club["points"]) == initial_points
        assert int(updated_competition["numberOfPlaces"]) == competition_places


def test_club_points_cannot_go_below_zero(client, setup_data):
    """
    Test that a club cannot have negative points after purchasing places.
    Uses test data from setup_data fixture.
    """

    # Define competition and club for the test
    competition_name = "Test Competition"
    club_name = "Test Club"

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
