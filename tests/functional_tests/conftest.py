import pytest
from flask_testing import LiveServerTestCase
from selenium import webdriver
from Python_Testing.server import app


class TestBase(LiveServerTestCase):
    """Classe de base pour les tests fonctionnels."""

    def create_app(self):
        """Crée et configure l'application pour les tests."""
        app.config["TESTING"] = True
        app.config["LIVESERVER_PORT"] = 5001
        app.config["WTF_CSRF_ENABLED"] = False  # Désactive CSRF pour les tests
        return app

    def setUp(self):
        """Configuration avec Chrome."""
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Optionnel : mode sans interface
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(self.get_server_url())

    def tearDown(self):
        """Nettoyage après chaque test."""
        self.driver.quit()


@pytest.fixture(scope="module")
def test_base():
    """Fixture pour la classe de base de test."""
    return TestBase()
