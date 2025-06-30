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


def test_initialization_of_booking_tracking():
    """
    Test that the booking tracking is correctly initialized.
    """
    assert isinstance(booked_places, dict)
    assert len(booked_places) == 0


