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


def test_display_club_points(client):
    """
    Test that the points of other clubs are displayed when logged in as Iron Temple.
    """
    # Assume "iron_temple@example.com" is the email associated with Iron Temple
    response = client.post("/showSummary", data={"email": "admin@irontemple.com"})
    assert response.status_code == 200

    # Check that the response contains the points of Simply Lift and She Lifts
    assert b"Simply Lift" in response.data
    assert b"She Lifts" in response.data
