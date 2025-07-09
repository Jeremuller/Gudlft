"""
Integration tests configuration file.
This file contains fixtures and configurations specific to integration tests.
"""

import pytest

from Python_Testing.server import clubs, competitions, app, booked_places


@pytest.fixture(scope="function")
def integration_client():
    """
    Flask test client configured for integration tests.
    Sets up a test client with appropriate configuration for integration testing.
    """
    # Configure the app for testing
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False  # Disable CSRF for testing

    # Provide the test client
    with app.test_client() as client:
        yield client


@pytest.fixture(scope="function", autouse=True)
def integration_data():
    """
    Test data setup for integration tests.
    Automatically used by all tests in this directory.
    Adds realistic test data and ensures clean state before/after tests.
    """
    # Save original data
    original_clubs = clubs.copy()
    original_competitions = competitions.copy()
    original_booked_places = booked_places.copy()

    # Reset test datas
    clubs.clear()
    competitions.clear()
    booked_places.clear()

    # Add integration-specific test data
    clubs.extend(
        [
            {"name": "Integration Club 1", "email": "club1@test.com", "points": "20"},
            {"name": "Integration Club 2", "email": "club2@test.com", "points": "30"},
        ]
    )

    competitions.extend(
        [
            {
                "name": "Integration Competition 1",
                "date": "2025-12-01 10:00:00",
                "numberOfPlaces": "25",
                "booked_places": 0,
            },
            {
                "name": "Integration Competition 2",
                "date": "2025-11-15 14:00:00",
                "numberOfPlaces": "15",
                "booked_places": 0,
            },
        ]
    )

    # This is where the test runs
    yield

    # Restore original data after tests complete
    clubs.clear()
    clubs.extend(original_clubs)
    competitions.clear()
    competitions.extend(original_competitions)
    booked_places.clear()
    booked_places.update(original_booked_places)
