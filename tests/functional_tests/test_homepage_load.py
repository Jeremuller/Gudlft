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


def test_login(driver):
    """
    Test the login functionality of the web application.
    This test checks if a user can log in successfully using valid credentials.
    """
    # Start the Flask application in a separate thread
    def run_app():
        app.run(port=5001)

    app_thread = Thread(target=run_app)
    app_thread.daemon = True  # Daemonize thread to ensure it exits when the main program exits
    app_thread.start()

    # Navigate to the login page
    driver.get("http://localhost:5001/")

    # Find the email input field and enter an email
    email_field = driver.find_element("css selector", "input[name='email']")
    email_field.clear()  # Clear the field in case there is any default text
    email_field.send_keys("functional_test@club.co")  # Enter the test email

    # Submit the form
    submit_button = driver.find_element("css selector", "button[type='submit']")
    submit_button.click()

    # Assert that the login was successful by checking for a welcome message or a specific element on the dashboard
    assert "Welcome, functional_test@club.co" in driver.page_source
