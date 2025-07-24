"""
Functional tests configuration file.
This file contains fixtures and configurations specific to functional tests using Selenium.
"""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from Python_Testing.server import app, clubs, competitions, booked_places


@pytest.fixture(scope="module")
def driver():
    """
    Selenium WebDriver fixture for functional tests.
    Configures and provides a Chrome WebDriver instance for testing.
    Runs in headless mode for CI compatibility.
    Yields the driver instance and ensures proper cleanup after tests.
    """
    # Configure Chrome options for headless testing
    chrome_options = Options()
    # Run without GUI
    chrome_options.add_argument("--headless")
    # Bypass OS security model
    chrome_options.add_argument("--no-sandbox")
    # Overcome limited resource problems
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Initialize the WebDriver with configured options
    driver = webdriver.Chrome(options=chrome_options)

    # Set basic configurations for tests
    driver.implicitly_wait(10)
    driver.maximize_window()

    # Provide the driver to tests
    yield driver

    # Cleanup after tests complete
    driver.quit()


@pytest.fixture(scope="module")
def flask_app():
    """
    Flask application fixture for functional tests.
    Configures the Flask application in testing mode.
    Yields the configured app instance.
    """
    # Set testing configuration
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing

    # Provide the configured app to tests
    yield app


@pytest.fixture(scope="module")
def client(flask_app):
    """
    Flask test client fixture.
    Provides a test client for making requests to the Flask application.
    """
    # Create and provide a test client
    with flask_app.test_client() as client:
        yield client


@pytest.fixture(scope="function")
def app_context(flask_app):
    """
    Flask application context fixture.
    Provides an application context for tests that need it.
    """
    # Create and provide an application context
    with flask_app.app_context():
        yield


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
