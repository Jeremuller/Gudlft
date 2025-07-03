import pytest
import datetime

from server import clubs, app, get_current_date, competitions


@pytest.fixture
def client():
    """
    Fixture to provide a test client for the Flask application.
    Configures the application in testing mode.
    """
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def setup_data():
    """Fixture to set up initial data for unit_tests."""

    # Copy from original datas to save them
    original_clubs = clubs.copy()
    original_competitions = competitions.copy()

    # Add test datas for club and competition
    clubs.append({"name": "Test Club", "email": "test@club.com", "points": 10})

    yield

    # Restore original datas
    clubs.clear()
    clubs.extend(original_clubs)
    competitions.clear()
    competitions.extend(original_competitions)


def test_current_date():
    """Test that the program correctly identifies the current date."""
    assert get_current_date() == datetime.date.today()


@pytest.mark.parametrize("date_offset, expected_display", [
    (-1, False),  # Past competition (1 day ago)
    (0, True),   # Today's competition
    (1, True),   # Tomorrow's competition
    (30, True)   # Future competition (30 days from now)
])
def test_competition_display_based_on_date(client, setup_data, date_offset, expected_display):
    """
    Parametrized test to check competition display based on date.
    Tests various date offsets to verify display logic.
    """
    # Add a competition with the specific date offset
    test_date = (datetime.datetime.now() + datetime.timedelta(days=date_offset)).strftime("%Y-%m-%d %H:%M:%S")
    test_name = f"Test Competition {date_offset}"

    competitions.append({
        "name": test_name,
        "date": test_date,
        "numberOfPlaces": 10
    })

    response = client.post("/showSummary", data={"email": "test@club.com"})
    assert response.status_code == 200

    if expected_display:
        assert test_name.encode() in response.data
    else:
        assert test_name.encode() not in response.data

    # Clean up - remove the test competition we just added
    competitions[:] = [c for c in competitions if c["name"] != test_name]
