import pytest

from server import clubs, app


@pytest.fixture
def client():
    """
    Fixture to provide a test client for the Flask application.
    Configures the application in testing mode.
    """
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_show_summary_with_valid_email(client):
    """
    Test the show_summary route with a valid email.
    Verifies that the response status code is 200 and the welcome message is present.
    """
    response = client.post("/showSummary", data={"email": "john@simplylift.co"})
    data = response.data.decode()
    assert response.status_code == 200
    assert "Welcome, john@simplylift.co" in data


def test_show_summary_with_invalid_email(client):
    """
    Test the show_summary route with an invalid email.
    Verifies that the response status code is 200 and the error message for invalid email is present.
    """
    response = client.post("/showSummary", data={"email": "invalid@example.com"})
    data = response.data.decode()
    assert response.status_code == 200
    assert "The email you entered isn&#39;t found, please try again." in data


def test_show_summary_with_missing_email(client):
    """
    Test the show_summary route with missing email data.
    Verifies that the response status code is 200 and the error message for missing email is present.
    """
    response = client.post("/showSummary", data={})
    data = response.data.decode()
    assert response.status_code == 200
    assert "Form isn&#39;t complete, please enter an email address." in data
