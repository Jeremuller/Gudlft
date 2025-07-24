def test_successful_booking_flow(driver):
    """
    Test the complete successful booking flow.
    Steps:
    1. Access home page
    2. Login with valid email
    3. Verify welcome page
    4. Access booking page
    5. Enter valid number of places
    6. Confirm booking
    7. Verify confirmation message
    8. Verify points deduction
    9. Verify competition places update
    """
    # Step 1: Access home page
    driver.get("http://localhost:5000/")
    assert "Welcome to the GUDLFT Registration Portal" in driver.page_source

    # Step 2: Login with valid email
    email_field = driver.find_element("name", "email")
    email_field.send_keys("club1@test.com")

    submit_button = driver.find_element("css selector", "button[type='submit']")
    submit_button.click()

    # Step 3: Verify welcome page with initial points
    assert "Welcome, club1@test.com" in driver.page_source
    assert "Points available: 20" in driver.page_source

    # Get initial points for later verification
    points_text = [
        t for t in driver.page_source.split("\n") if "Points available:" in t
    ][0]
    initial_points = int(points_text.split(":")[1].strip())

    # Verify competitions list
    assert "Competitions:" in driver.page_source

    # Step 4: Access booking page for first competition
    # Find the first "Book Places" link and click it
    book_link = driver.find_element("link text", "Book Places")
    book_link.click()

    # Step 5: Verify booking page for the competition
    booking_header = driver.find_element("css selector", "h2")
    assert "Booking for" in booking_header.text

    # Get available places for verification
    places_text = driver.find_element(
        "xpath", "//*[contains(text(), 'Places available:')]"
    ).text
    initial_places = int(places_text.split(":")[1].strip())

    # Step 6: Enter number of places to book and submit
    places_field = driver.find_element("name", "places")
    places_field.send_keys("5")

    # Step 7: Submit the booking
    book_button = driver.find_element("css selector", "button[type='submit']")
    book_button.click()

    # Step 8: Verify successful booking
    assert "Great-booking complete!" in driver.page_source

    # Step 9: Return to welcome page to verify updates
    driver.get("http://localhost:5000/")
    email_field = driver.find_element("name", "email")
    email_field.send_keys("club1@test.com")
    submit_button = driver.find_element("css selector", "button[type='submit']")
    submit_button.click()

    # Verify points deduction
    updated_points_text = driver.find_element(
        "xpath", "//*[contains(text(), 'Points available:')]"
    ).text
    updated_points = int(updated_points_text.split(":")[1].strip())
    assert updated_points == initial_points - 5
