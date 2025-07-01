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


def test_display_all_club_names_and_points(client):
    """
    Test that all clubs and their points are correctly displayed on the welcome page.
    """
    response = client.post("/showSummary", data={"email": "admin@irontemple.com"})
    assert response.status_code == 200

    for club in clubs:
        expected_display = f"{club['name']} - Points: {club['points']}"
        assert expected_display.encode() in response.data
