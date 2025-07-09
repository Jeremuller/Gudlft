"""
Integration tests for the complete booking flow.
"""

from Python_Testing.server import clubs, competitions, booked_places


def test_complete_booking_flow(integration_client):
    """
    Test the full booking process from competition selection to confirmation.
    Verifies:
    - Competition and club data loading
    - Points verification
    - Places booking
    - Data updates
    """
    # Get initial data
    club = next(c for c in clubs if c["name"] == "Integration Club 1")
    competition = next(
        c for c in competitions if c["name"] == "Integration Competition 1"
    )

    initial_points = int(club["points"])
    initial_places = int(competition["numberOfPlaces"])

    # Test booking page access
    response = integration_client.get(f"/book/{competition['name']}/{club['name']}")
    assert response.status_code == 200
    assert b"Places available:" in response.data

    # Test actual booking
    response = integration_client.post(
        "/purchasePlaces",
        data={"competition": competition["name"], "club": club["name"], "places": "5"},
    )

    # Verify results
    assert response.status_code == 200
    assert int(club["points"]) == initial_points - 5
    assert int(competition["numberOfPlaces"]) == initial_places - 5
    assert b"Great-booking complete!" in response.data


def test_booking_failure_not_enough_points(integration_client):
    """
    Test booking failure when club doesn't have enough points.
    Verifies:
    - Error message is displayed
    - No points are deducted
    - No places are booked
    """
    # Setup - use a club with minimal points
    club = next(c for c in clubs if c["name"] == "Integration Club 2")
    competition = next(
        c for c in competitions if c["name"] == "Integration Competition 1"
    )

    initial_points = int(club["points"])
    initial_places = int(competition["numberOfPlaces"])

    # Try to book more points than available
    response = integration_client.post(
        "/purchasePlaces",
        data={
            "competition": competition["name"],
            "club": club["name"],
            "places": str(initial_points + 1),  # More than available points
        },
    )

    # Verify results
    assert response.status_code == 200
    assert int(club["points"]) == initial_points
    assert int(competition["numberOfPlaces"]) == initial_places
    assert b"Not enough points" in response.data


def test_booking_full_competition(integration_client):
    """
    Test booking when competition has no places left
    """

    # Setup - book all places first
    competition = next(
        c for c in competitions if c["name"] == "Integration Competition 2"
    )
    competition["numberOfPlaces"] = "0"

    response = integration_client.post(
        "/purchasePlaces",
        data={
            "competition": competition["name"],
            "club": "Integration Club 1",
            "places": "1",
        },
    )

    assert b"Not enough places available in the competition." in response.data


def test_booking_points_limit(integration_client):
    """
    Test that booking more than 12 places is rejected.
    """
    # Setup - club with enough points
    club = next(c for c in clubs if c["name"] == "Integration Club 1")
    competition = next(
        c for c in competitions if c["name"] == "Integration Competition 1"
    )

    # Try to book 13 places
    response = integration_client.post(
        "/purchasePlaces",
        data={"competition": competition["name"], "club": club["name"], "places": "13"},
    )

    # Verifications
    assert response.status_code == 200
    assert (
        b"A club cannot book more than 12 places in total for a competition."
        in response.data
    )
    assert int(club["points"]) == 20
    assert int(competition["numberOfPlaces"]) == int(competition["numberOfPlaces"])


def test_multiple_bookings(integration_client):
    """
    Test that multiple bookings maintain data consistency.
    """
    club1 = next(c for c in clubs if c["name"] == "Integration Club 1")
    club2 = next(c for c in clubs if c["name"] == "Integration Club 2")
    competition = next(
        c for c in competitions if c["name"] == "Integration Competition 1"
    )

    initial_places = int(competition["numberOfPlaces"])

    # First booking
    integration_client.post(
        "/purchasePlaces",
        data={"competition": competition["name"], "club": club1["name"], "places": "5"},
    )

    # Second booking
    integration_client.post(
        "/purchasePlaces",
        data={"competition": competition["name"], "club": club2["name"], "places": "3"},
    )

    # Verifications
    assert int(competition["numberOfPlaces"]) == initial_places - 8
    assert int(club1["points"]) == 20 - 5
    assert int(club2["points"]) == 30 - 3


def test_booking_missing_data(integration_client):
    """
    Test booking with missing form data.
    Verifies:
    - Server properly validates required fields
    - Returns appropriate error status
    - Maintains data integrity
    """
    # Get initial data for verification
    club = next(c for c in clubs if c["name"] == "Integration Club 1")
    competition = next(
        c for c in competitions if c["name"] == "Integration Competition 1"
    )
    initial_points = int(club["points"])
    initial_places = int(competition["numberOfPlaces"])

    # Send request with missing club data
    response = integration_client.post(
        "/purchasePlaces",
        data={
            "competition": competition["name"],
            # Missing club name intentionally
            "places": "5",
        },
    )

    # Verifications
    assert response.status_code == 400  # Bad Request
    # Verify no changes occurred
    assert int(club["points"]) == initial_points
    assert int(competition["numberOfPlaces"]) == initial_places


def test_booking_invalid_data(integration_client):
    """
    Test booking with invalid data types.
    Verifies:
    - Server properly validates data types
    - Returns specific error for invalid numbers
    - Prevents any data corruption
    """
    # Get initial data for verification
    club = next(c for c in clubs if c["name"] == "Integration Club 1")
    competition = next(
        c for c in competitions if c["name"] == "Integration Competition 1"
    )
    initial_points = int(club["points"])
    initial_places = int(competition["numberOfPlaces"])

    # Send request with invalid places data
    response = integration_client.post(
        "/purchasePlaces",
        data={
            "competition": competition["name"],
            "club": club["name"],
            "places": "abc",  # Invalid number
        },
    )

    # Verifications
    assert response.status_code == 200
    assert b"Please enter a valid number for places" in response.data
    # Verify no changes occurred
    assert int(club["points"]) == initial_points
    assert int(competition["numberOfPlaces"]) == initial_places


def test_booking_tracking(integration_client):
    """
    Test that booked places are properly tracked.
    """
    club = next(c for c in clubs if c["name"] == "Integration Club 1")
    competition = next(
        c for c in competitions if c["name"] == "Integration Competition 1"
    )

    # First booking
    integration_client.post(
        "/purchasePlaces",
        data={"competition": competition["name"], "club": club["name"], "places": "5"},
    )

    # Verify tracking
    key = (club["name"], competition["name"])
    assert booked_places.get(key, 0) == 5

    # Second booking
    integration_client.post(
        "/purchasePlaces",
        data={"competition": competition["name"], "club": club["name"], "places": "3"},
    )

    # Verify updated tracking
    assert booked_places.get(key, 0) == 8
