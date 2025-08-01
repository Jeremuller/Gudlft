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


def test_successful_booking(driver, create_app):
    """
    Test a successful booking of competition places.
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

    # Find all "Book Places" links and select the third one (corresponding to test competition)
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

    assert WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Great-booking complete!")
    )


def test_invalid_data_booking(driver, create_app):
    """
    Test booking with invalid data.
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

    # Find all "Book Places" links and select the third one (corresponding to test competition)
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
    places_field.send_keys("invalid")

    book_submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
    )
    book_submit_button.click()

    assert WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Please enter a valid number for places")
    )


def test_insufficient_points_booking(driver, create_app):
    """
    Test booking with insufficient points.
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

    # Find all "Book Places" links and select the third one (corresponding to test competition)
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
    places_field.send_keys("40")  # Assuming the user doesn't have this many points

    book_submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
    )
    book_submit_button.click()

    assert WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "body"),
                                         "Not enough points to book the required number of places.")
    )


def test_limit_places_booking(driver, create_app):
    """
    Test booking with insufficient competition places.
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

    # Find all "Book Places" links and select the third one (corresponding to test competition)
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
    places_field.send_keys("15")  # Assuming there aren't this many places available

    book_submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
    )
    book_submit_button.click()

    # Wait for the flash message to be present in the DOM
    flash_message = WebDriverWait(driver, 20).until(
        EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".flash-messages"),
                                         "A club cannot book more than 12 places in total for a competition.")
    )
    assert flash_message


def test_insufficient_places_booking(driver, create_app):
    """
    Test booking with insufficient competition places.
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

    # Find all "Book Places" links and select the third one
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
    places_field.send_keys("21")  # Assuming there aren't this many places available

    book_submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
    )
    book_submit_button.click()

    # Wait for the flash message to be present in the DOM
    try:
        flash_message = WebDriverWait(driver, 20).until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".flash-messages"),
                                             "Not enough places available in the competition.")
        )
        print("Flash message found:", flash_message)
    except Exception as e:
        print("Flash message not found. Page source:", driver.page_source)
        raise e

    assert flash_message
