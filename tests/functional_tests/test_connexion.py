import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
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


def test_valid_login(driver, create_app):
    """
    Test login with a valid email.
    """
    def run_app():
        create_app.run(port=5001)

    app_thread = Thread(target=run_app)
    app_thread.daemon = True
    app_thread.start()

    driver.get("http://localhost:5001/")

    email_field = driver.find_element("css selector", "input[name='email']")
    email_field.clear()
    email_field.send_keys("functional_test@club.co")

    submit_button = driver.find_element("css selector", "button[type='submit']")
    submit_button.click()

    assert "Welcome, functional_test@club.co" in driver.page_source

def test_invalid_login(driver, create_app):
    """
    Test login with an invalid email.
    """
    def run_app():
        create_app.run(port=5001)

    app_thread = Thread(target=run_app)
    app_thread.daemon = True
    app_thread.start()

    driver.get("http://localhost:5001/")

    email_field = driver.find_element("css selector", "input[name='email']")
    email_field.clear()
    email_field.send_keys("invalid_email@club.co")

    submit_button = driver.find_element("css selector", "button[type='submit']")
    submit_button.click()

    assert "The email you entered isn't found" in driver.page_source

def test_logout(driver, create_app):
    """
    Test logout functionality.
    """
    def run_app():
        create_app.run(port=5001)

    app_thread = Thread(target=run_app)
    app_thread.daemon = True
    app_thread.start()

    driver.get("http://localhost:5001/")

    email_field = driver.find_element("css selector", "input[name='email']")
    email_field.clear()
    email_field.send_keys("functional_test@club.co")

    submit_button = driver.find_element("css selector", "button[type='submit']")
    submit_button.click()
    assert "Welcome, functional_test@club.co" in driver.page_source


    logout_link = driver.find_element("link text", "Logout")
    logout_link.click()

    assert "Welcome to the GUDLFT Registration Portal!" in driver.page_source
