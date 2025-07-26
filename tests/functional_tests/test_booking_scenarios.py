import pytest
from selenium.webdriver.common.by import By


def test_homepage_loads(test_base):
    """
    Test basique : vérifie que la page d'accueil se charge correctement.
    """
    # Vérifie que le titre de la page est correct
    assert "Welcome to the GUDLFT Registration Portal" in test_base.driver.title

    # Vérifie qu'un élément spécifique est présent
    email_field = test_base.driver.find_element(By.NAME, "email")
    assert email_field is not None
