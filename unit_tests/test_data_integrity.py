import pytest
from server import clubs, competitions, load_clubs, load_competitions


@pytest.fixture(scope="module")
def original_data():
    """Fixture to store original values of critical fields."""
    # Store only the essential fields we want to protect
    return {
        "clubs_points": {club["name"]: club["points"] for club in clubs},
        "competitions_places": {
            comp["name"]: comp["numberOfPlaces"] for comp in competitions
        },
    }


def test_critical_fields_integrity(original_data):
    """
    Test that verifies only critical fields (points and places) haven't been modified.
    Compares current values with original values for these specific fields.
    """
    # Reload original data to get clean reference
    original_clubs = load_clubs()
    original_competitions = load_competitions()

    # Verify club points haven't changed
    for club in clubs:
        assert (
            club["points"] == original_data["clubs_points"][club["name"]]
        ), f"Club {club['name']} points were modified"

    # Verify competition places haven't changed
    for comp in competitions:
        assert (
            comp["numberOfPlaces"] == original_data["competitions_places"][comp["name"]]
        ), f"Competition {comp['name']} places were modified"

        # Additional verification with freshly loaded data
        for club in original_clubs:
            current_club = next(c for c in clubs if c["name"] == club["name"])
            assert (
                club["points"] == current_club["points"]
            ), f"Club {club['name']} points changed during tests"

        for competition in original_competitions:
            current_comp = next(c for c in competitions if c["name"] == competition["name"])
            assert (
                competition["numberOfPlaces"] == current_comp["numberOfPlaces"]
            ), f"Competition {competition['name']} places changed during tests"
