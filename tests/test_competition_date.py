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

