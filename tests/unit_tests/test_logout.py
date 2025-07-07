from flask import request, url_for

from Python_Testing.server import app
import pytest


@pytest.fixture
def client():
    """
    Fixture to provide a test client for the Flask application.
    Configures the application in testing mode.
    """
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_logout_route(client):
    """Test logout route redirects to index"""
    # Exercise
    response = client.get("/logout", follow_redirects=True)

    # Verify response status code
    assert response.status_code == 200
    # Verify template used
    assert b"Welcome to the GUDLFT Registration Portal!" in response.data
    # Verify redirection
    assert request.path == url_for("index")
