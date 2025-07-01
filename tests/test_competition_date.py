import pytest, datetime

from server import clubs, app, get_current_date


@pytest.fixture
def client():
    """
    Fixture to provide a test client for the Flask application.
    Configures the application in testing mode.
    """
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_current_date():
    """Test that the program correctly identifies the current date."""
    assert get_current_date() == datetime.date.today()


def test_past_competition_not_displayed(client):
    """
    Test that past competitions are not displayed by the book function.
    """
    competition_name = "2020 Spring Festival"  # This competition is in the past
    club_name = "Simply Lift"

    response = client.get(f"/book/{competition_name}/{club_name}")

    # Check that the response redirects or shows an error message
    assert response.status_code == 200
    assert b"Something went wrong" in response.data

    competition_name = "2020 Fall Classic"

    response = client.get(f"/book/{competition_name}/{club_name}")

    # Check that the response redirects or shows an error message
    assert response.status_code == 200
    assert b"Something went wrong" in response.data
