"""
Functional tests configuration with proper test data isolation.
"""
import pytest
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from Python_Testing.server import app as flask_app
from threading import Thread


# Configuration pour le serveur de test
TEST_PORT = 5001
TEST_HOST = 'localhost'


def load_test_data():
    """Load test data from JSON files."""
    try:
        with open("test_clubs.json") as c:
            clubs = json.load(c)["clubs"]
        with open("test_competitions.json") as comps:
            competitions = json.load(comps)["competitions"]
        return clubs, competitions
    except FileNotFoundError as e:
        print(f"Error loading test data: {e}")
        raise


@pytest.fixture(scope="function", autouse=True)
def test_data():
    """Fixture providing test data for the entire test session."""
    return load_test_data()


@pytest.fixture(scope="function", autouse=True)
def test_app(test_data):
    """
    Fixture providing a configured Flask test application.
    Uses test data and runs on a separate port.
    """
    clubs, competitions = test_data

    # Configure the test application
    test_app = flask_app
    test_app.config['TESTING'] = True
    test_app.config['WTF_CSRF_ENABLED'] = False
    test_app.config['CLUBS'] = clubs
    test_app.config['COMPETITIONS'] = competitions

    # Use test data instead of production data
    def get_test_clubs():
        return test_app.config['CLUBS']

    def get_test_competitions():
        return test_app.config['COMPETITIONS']

    return test_app


@pytest.fixture(scope="function", autouse=True)
def driver(test_app):
    """
    Fixture providing a Selenium WebDriver and running the test application.
    """
    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Start the test application in a separate thread
    def run_app():
        test_app.run(host=TEST_HOST, port=TEST_PORT)

    app_thread = Thread(target=run_app)
    app_thread.daemon = True
    app_thread.start()

    # Initialize WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)

    yield driver

    # Cleanup
    driver.quit()
