import pytest
import re
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


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_booking_and_display_update(driver, create_app):
    """
    Test booking places and verify the club points are updated correctly.
    """
    def run_app():
        create_app.run(port=5001)

    app_thread = Thread(target=run_app)
    app_thread.daemon = True
    app_thread.start()

    # Navigate to the login page
    driver.get("http://localhost:5001/")
    print("Page source after login:")
    print(driver.page_source)

    # Verify initial points of the Functional Test Club
    assert WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Functional Test Club - Points: 27")
    ), "Initial points are not as expected."

    # Log in
    email_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']"))
    )
    email_field.clear()
    email_field.send_keys("functional_test@club.co")

    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
    )
    submit_button.click()

    # Book places for the third competition
    book_links = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.LINK_TEXT, "Book Places"))
    )
    if len(book_links) >= 3:
        book_links[2].click()  # Select the third link (index 2)
    else:
        raise Exception("Not enough 'Book Places' links found.")

    places_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='places']"))
    )
    places_field.clear()
    places_field.send_keys("3")

    book_submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
    )
    book_submit_button.click()

    # Logout to return to the login page
    logout_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Logout"))
    )
    logout_link.click()

    # Verify the updated points of the Functional Test Club
    assert WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Functional Test Club - Points: 24")
    ), "Points not updated correctly after booking."
