from Gudlft.server import clubs, competitions, booked_places


def test_integration_purchase_places_update(integration_client):
    """
    Test the immediate update of data after a purchase in the user interface.

    This test verifies that after a club purchases places for a competition,
    the user interface immediately reflects the updated points and available places.
    It ensures that the data displayed to the user is consistent with the backend state.

    Steps:
    1. Simulate a user login with a valid email.
    2. Perform a purchase of competition places.
    3. Verify that the purchase confirmation message is displayed.
    4. Check that the updated points and places are correctly shown in the UI.
    """
    # Simulate login by accessing the showSummary route
    response = integration_client.post(
        "/showSummary", data={"email": "club1@test.com"}, follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Welcome" in response.data

    # Perform a purchase
    purchase_response = integration_client.post(
        "/purchasePlaces",
        data={
            "club": "Integration Club 1",
            "competition": "Integration Competition 1",
            "places": "3",
        },
        follow_redirects=True,
    )

    print("Booked Places before rendering:", booked_places)

    # Check if the purchase was successful
    assert b"Great-booking complete!" in purchase_response.data

    # Check if the points and places are updated correctly in the response
    assert b"Points available: 17" in purchase_response.data
    assert b"Places already booked: 3 / 12" in purchase_response.data
    assert b"Number of Places: 22" in purchase_response.data
