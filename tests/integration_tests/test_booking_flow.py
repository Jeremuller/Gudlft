"""
Integration tests for the complete booking flow.
"""

from Python_Testing.server import clubs, competitions, booked_places


def test_complete_booking_flow(integration_client):
    """
    Test the full booking process from competition selection to confirmation.
    Verifies:
    - Successful loading with valid email
    - Competition and club data loading
    - Access to booking page
    - Points verification
    - Places booking
    - Data updates
    - Success message display
    """

    # Step 1: Login with valid email
    response = integration_client.post(
        "/showSummary",
        data={"email": "club1@test.com"},  # Club with 20 points
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Welcome" in response.data
    assert b"club1@test.com" in response.data
    assert b"Points available:" in response.data

    # Step 2: Get initial data
    club = next(c for c in clubs if c["name"] == "Integration Club 1")
    competition = next(
        c for c in competitions if c["name"] == "Integration Competition 1"
    )

    initial_points = int(club["points"])
    initial_places = int(competition["numberOfPlaces"])

    # Step 3: Test booking page access
    response = integration_client.get(f"/book/{competition['name']}/{club['name']}")
    assert response.status_code == 200
    assert b"Places available:" in response.data

    # Step 4: Test actual booking
    response = integration_client.post(
        "/purchasePlaces",
        data={"competition": competition["name"], "club": club["name"], "places": "5"},
    )

    # Step 5: Verify results
    assert response.status_code == 200
    assert int(club["points"]) == initial_points - 5
    assert int(competition["numberOfPlaces"]) == initial_places - 5
    assert b"Great-booking complete!" in response.data


def test_booking_failure_not_enough_points(integration_client):
    """
    Test complete booking flow with insufficient points scenario.
    Verifies:
    - Successful login with valid email
    - Access to booking page
    - Error handling when not enough points
    - Error message display
    - Data integrity (no points deducted, no places booked)
    - User stays on booking page
    """
    # Step 1: Login with valid email
    response = integration_client.post(
        "/showSummary",
        data={"email": "club2@test.com"},  # Club with 30 points
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Welcome" in response.data
    assert b"club2@test.com" in response.data
    assert b"Points available:" in response.data

    # Step 2: Get initial data
    club = next(c for c in clubs if c["name"] == "Integration Club 2")
    competition = next(
        c for c in competitions if c["name"] == "Integration Competition 1"
    )
    initial_points = int(club["points"])

    # Step 3: Access booking page
    response = integration_client.get(f"/book/{competition['name']}/{club['name']}")
    assert response.status_code == 200
    assert b"Places available:" in response.data
    assert str.encode(competition["name"]) in response.data
    assert str.encode(club["name"]) in response.data

    # Step 4: Attempt booking with insufficient points
    response = integration_client.post(
        "/purchasePlaces",
        data={
            "competition": competition["name"],
            "club": club["name"],
            "places": str(initial_points + 1),  # More than available points
        },
        follow_redirects=True,
    )

    # Step 5: Verify results
    assert response.status_code == 200
    assert b"Not enough points" in response.data
    # Verify we're still on booking page
    assert b"Integration Competition 1" in response.data


def test_booking_full_competition(integration_client):
    """
    Test complete booking flow when competition has no places left.
    Verifies:
    - Successful login
    - Access to booking page for full competition
    - Error handling when no places available
    - Proper error message display
    - Data integrity (no points deducted, no places booked)
    - User stays on booking page
    """
    # Step 1: Login with valid email
    response = integration_client.post(
        "/showSummary", data={"email": "club1@test.com"}, follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Welcome" in response.data
    assert b"club1@test.com" in response.data

    # Step 2: Get competition and set it to full
    competition = next(
        c for c in competitions if c["name"] == "Integration Competition 2"
    )
    competition["numberOfPlaces"] = "0"  # Set competition to full

    # Step 3: Access booking page
    response = integration_client.get(
        f"/book/{competition['name']}/Integration Club 1", follow_redirects=True
    )
    assert response.status_code == 200
    assert str.encode(competition["name"]) in response.data
    assert b"Places available: 0" in response.data  # Verify no places available

    # Step 4: Attempt to book a place
    response = integration_client.post(
        "/purchasePlaces",
        data={
            "competition": competition["name"],
            "club": "Integration Club 1",
            "places": "1",
        },
        follow_redirects=True,
    )

    # Step 5: Verify error handling
    assert response.status_code == 200
    assert b"Not enough places available in the competition" in response.data
    assert b"Integration Competition 2" in response.data  # Still on booking page
    assert str.encode(competition["name"]) in response.data


def test_booking_points_limit(integration_client):
    """
    Test complete booking flow when exceeding 12 places limit.
    Verifies:
    - Successful login
    - Access to booking page
    - Error handling when exceeding 12 places limit
    - Proper error message display
    - Data integrity (no points deducted, no places booked)
    - User stays on booking page
    """
    # Step 1: Login with valid email
    response = integration_client.post(
        "/showSummary", data={"email": "club1@test.com"}, follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Welcome" in response.data
    assert b"club1@test.com" in response.data
    assert b"Points available: 20" in response.data

    # Step 2: Get club and competition data
    club = next(c for c in clubs if c["name"] == "Integration Club 1")
    competition = next(
        c for c in competitions if c["name"] == "Integration Competition 1"
    )
    initial_points = int(club["points"])
    initial_places = int(competition["numberOfPlaces"])

    # Step 3: Access booking page
    response = integration_client.get(
        f"/book/{competition['name']}/{club['name']}", follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Integration Competition 1" in response.data
    assert str.encode(competition["name"]) in response.data
    assert str.encode(club["name"]) in response.data
    assert int(competition["numberOfPlaces"]) == initial_places
    assert int(club["points"]) == initial_points

    # Step 4: Attempt to book 13 places (exceeding limit)
    response = integration_client.post(
        "/purchasePlaces",
        data={
            "competition": competition["name"],
            "club": club["name"],
            "places": "13",
        },
        follow_redirects=True,
    )

    # Step 5: Verify error handling
    assert response.status_code == 200
    assert (
        b"A club cannot book more than 12 places in total for a competition"
        in response.data
    )
    # Still on booking page
    assert b"Integration Competition 1" in response.data
    assert str.encode(competition["name"]) in response.data


def test_multiple_bookings(integration_client):
    """
    Test complete flow of multiple bookings by different clubs.
    Verifies:
    - Successful login for both clubs
    - Sequential booking process
    - Points deduction for each club
    - Places reduction in competition
    - Booking tracking for each club
    - Data consistency throughout the process
    """
    # Step 1: Login with first club
    response = integration_client.post(
        "/showSummary",
        data={"email": "club1@test.com"},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Welcome" in response.data
    assert b"club1@test.com" in response.data

    # Get initial data
    club1 = next(c for c in clubs if c["name"] == "Integration Club 1")
    club2 = next(c for c in clubs if c["name"] == "Integration Club 2")
    competition = next(c for c in competitions if c["name"] == "Integration Competition 1")
    initial_places = int(competition["numberOfPlaces"])
    initial_points_club1 = int(club1["points"])
    initial_points_club2 = int(club2["points"])

    # Step 2: First booking by club1
    response = integration_client.get(
        f"/book/{competition['name']}/{club1['name']}",
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Places available:" in response.data

    response = integration_client.post(
        "/purchasePlaces",
        data={
            "competition": competition["name"],
            "club": club1["name"],
            "places": "5"
        },
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data
    assert int(club1["points"]) == initial_points_club1 - 5
    assert int(competition["numberOfPlaces"]) == initial_places - 5

    # Verify first booking tracking
    key1 = (club1["name"], competition["name"])
    assert booked_places.get(key1, 0) == 5

    # Step 3: Login with second club
    response = integration_client.post(
        "/showSummary",
        data={"email": "club2@test.com"},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Welcome" in response.data
    assert b"club2@test.com" in response.data

    # Step 4: Second booking by club2
    response = integration_client.get(
        f"/book/{competition['name']}/{club2['name']}",
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Places available" in response.data

    response = integration_client.post(
        "/purchasePlaces",
        data={
            "competition": competition["name"],
            "club": club2["name"],
            "places": "3"
        },
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data
    assert int(club2["points"]) == initial_points_club2 - 3
    assert int(competition["numberOfPlaces"]) == initial_places - 8

    # Verify second booking tracking
    key2 = (club2["name"], competition["name"])
    assert booked_places.get(key2, 0) == 3

    # Step 5: Final verifications
    assert int(competition["numberOfPlaces"]) == initial_places - 8
    assert int(club1["points"]) == initial_points_club1 - 5
    assert int(club2["points"]) == initial_points_club2 - 3


def test_booking_missing_data(integration_client):
    """
    Test complete booking flow with missing form data.
    Verifies:
    - Successful login
    - Access to booking page
    - Server properly validates required fields
    - Returns appropriate error status
    - Maintains data integrity
    """
    # Step 1: Login with valid email
    response = integration_client.post(
        "/showSummary",
        data={"email": "club1@test.com"},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Welcome" in response.data
    assert b"club1@test.com" in response.data

    # Step 2: Get initial data for verification
    club = next(c for c in clubs if c["name"] == "Integration Club 1")
    competition = next(c for c in competitions if c["name"] == "Integration Competition 1")
    initial_points = int(club["points"])
    initial_places = int(competition["numberOfPlaces"])

    # Step 3: Access booking page
    response = integration_client.get(
        f"/book/{competition['name']}/{club['name']}",
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Places available:" in response.data

    # Step 4: Send request with missing club data
    response = integration_client.post(
        "/purchasePlaces",
        data={
            "competition": competition["name"],
            # Missing club name intentionally
            "places": "5",
        },
        follow_redirects=True
    )

    # Step 5: Verifications
    assert response.status_code == 400  # Bad Request

    # Verify no changes occurred
    assert int(club["points"]) == initial_points
    assert int(competition["numberOfPlaces"]) == initial_places

    # Verify no booking was tracked
    key = (club["name"], competition["name"])
    assert booked_places.get(key, 0) == 0


def test_booking_invalid_data(integration_client):
    """
    Test complete booking flow with invalid data types.
    Verifies:
    - Successful login
    - Access to booking page
    - Server properly validates data types
    - Returns specific error for invalid numbers
    - Displays error message
    - Maintains data integrity
    - User gets back on welcome
    """
    # Step 1: Login with valid email
    response = integration_client.post(
        "/showSummary",
        data={"email": "club1@test.com"},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Welcome" in response.data
    assert b"club1@test.com" in response.data

    # Step 2: Get initial data for verification
    club = next(c for c in clubs if c["name"] == "Integration Club 1")
    competition = next(c for c in competitions if c["name"] == "Integration Competition 1")
    initial_points = int(club["points"])
    initial_places = int(competition["numberOfPlaces"])

    # Step 3: Access booking page
    response = integration_client.get(
        f"/book/{competition['name']}/{club['name']}",
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Places available:" in response.data

    # Step 4: Send request with invalid places data
    response = integration_client.post(
        "/purchasePlaces",
        data={
            "competition": competition["name"],
            "club": club["name"],
            "places": "abc",  # Invalid number
        },
        follow_redirects=True
    )

    # Step 5: Verifications
    assert response.status_code == 200
    assert b"Please enter a valid number for places" in response.data

    # Verify no changes occurred
    assert int(club["points"]) == initial_points
    assert int(competition["numberOfPlaces"]) == initial_places

    # Verify no booking was tracked
    key = (club["name"], competition["name"])
    assert booked_places.get(key, 0) == 0
    # Check user is properly on welcome page
    assert b"Welcome, club1@test.com" in response.data


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
