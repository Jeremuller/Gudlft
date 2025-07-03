import json
import pytest
import copy

from server import clubs, competitions, load_clubs, load_competitions


@pytest.fixture(scope="module")
def original_data():
    """Fixture to load and store original JSON data."""
    # Créer des copies profondes des données originales
    return {"clubs": copy.deepcopy(clubs), "competitions": copy.deepcopy(competitions)}


def test_data_integrity(original_data):
    """
    Test that verifies user data hasn't been modified by tests.
    Compares current data with original data loaded at the beginning.
    """
    # Recharger les données originales depuis les fichiers
    original_clubs = load_clubs()
    original_competitions = load_competitions()

    # Comparer avec les données actuelles
    assert clubs == original_clubs, "Clubs data was modified by tests"
    assert competitions == original_competitions, "Competitions data was modified by tests"

    # Optionnel: comparaison plus détaillée avec les copies de la fixture
    assert clubs == original_data['clubs'], "Clubs data changed during tests"
    assert competitions == original_data['competitions'], "Competitions data changed during tests"
