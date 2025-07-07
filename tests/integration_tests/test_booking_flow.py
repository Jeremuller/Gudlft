"""
Integration tests for the complete booking flow.
"""

from Python_Testing.server import clubs, competitions


def test_complete_booking_flow(integration_client):
    """
    Test the full booking process from competition selection to confirmation.
    Verifies:
    - Competition and club data loading
    - Points verification
    - Places booking
    - Data updates
    """
    # 1. Get initial data
    club = next(c for c in clubs if c["name"] == "Integration Club 1")
    competition = next(c for c in competitions if c["name"] == "Integration Competition 1")

    initial_points = int(club["points"])
    initial_places = int(competition["numberOfPlaces"])

    # 2. Test booking page access
    response = integration_client.get(f"/book/{competition['name']}/{club['name']}")
    assert response.status_code == 200
    assert b"Places available:" in response.data

    # 3. Test actual booking
    response = integration_client.post("/purchasePlaces", data={
        "competition": competition["name"],
        "club": club["name"],
        "places": "5"
    })

    # 4. Verify results
    assert response.status_code == 200
    assert int(club["points"]) == initial_points - 5
    assert int(competition["numberOfPlaces"]) == initial_places - 5
    assert b"Great-booking complete!" in response.data
