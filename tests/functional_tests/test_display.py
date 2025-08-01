import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Gudlft.server import app
from threading import Thread


@pytest.fixture(scope="module")
def driver():
    """
    Fixture to initialize and configure the Selenium WebDriver for Chrome.
    This will be used to automate the browser for testing.
    """
    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode, i.e., without a UI
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

    # Initialize WebDriver with the configured options
    driver = webdriver.Chrome(options=chrome_options)
    yield driver  # Provide the driver to the test and ensure it will be used within the test function
    driver.quit()  # Quit the driver after the test is completed


@pytest.fixture(scope="module")
def create_app():
    """
    Fixture to configure the Flask app for testing.
    """
    app.config['TESTING'] = True
    return app


def test_display_competitions(driver, create_app):
    """
    Test the display of competitions on the welcome page.
    """
    def run_app():
        create_app.run(port=5001)

    app_thread = Thread(target=run_app)
    app_thread.daemon = True
    app_thread.start()

    # Log in
    driver.get("http://localhost:5001/")
    email_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']"))
    )
    email_field.clear()
    email_field.send_keys("functional_test@club.co")

    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
    )
    submit_button.click()

    # Verify that competitions are displayed
    competition_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul li"))
    )
    assert len(competition_elements) > 0, "No competitions displayed"


def test_booking_and_display_update(driver, create_app):
    """
    Test booking places and verify the display is updated correctly.
    """
    def run_app():
        create_app.run(port=5001)

    app_thread = Thread(target=run_app)
    app_thread.daemon = True
    app_thread.start()

    # Log in
    driver.get("http://localhost:5001/")
    email_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']"))
    )
    email_field.clear()
    email_field.send_keys("functional_test@club.co")

    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
    )
    submit_button.click()

    # Record initial number of places for the first competition
    competition_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul li"))
    )
    initial_places_text = competition_elements[0].text.split('Number of Places: ')[1].split('\n')[0]
    initial_places = int(initial_places_text)

    # Book places for the first competition
    book_links = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.LINK_TEXT, "Book Places"))
    )
    book_links[0].click()

    places_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='places']"))
    )
    places_field.clear()
    places_field.send_keys("3")

    book_submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
    )
    book_submit_button.click()

    # Navigate back to the welcome page to verify the updated competition places
    driver.get("http://localhost:5001/showSummary")

    # Verify the updated number of places for the first competition
    updated_competition_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul li"))
    )
    updated_places_text = updated_competition_elements[0].text.split('Number of Places: ')[1].split('\n')[0]
    updated_places = int(updated_places_text)

    # Assert that the number of places has been correctly updated
    assert updated_places == initial_places - 3, "Number of places not updated correctly"
