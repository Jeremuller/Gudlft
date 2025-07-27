def test_login_with_test_data(driver):
    """
    Test login using test data.
    """
    # Use the test application port
    driver.get("http://localhost:5001/")

    # Use test email from test data
    email_field = driver.find_element("css selector", "input[name='email']")
    email_field.clear()
    email_field.send_keys("john@simplylift.co")  # Email from test data

    submit_button = driver.find_element("css selector", "button[type='submit']")
    submit_button.click()

    assert "Welcome, john@simplylift.co" in driver.page_source
