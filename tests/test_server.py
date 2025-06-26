import pytest

from server import clubs, app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_show_summary_with_valid_email(client):
    response = client.post("/showSummary", data={"email": "john@simplylift.co"})
    data = response.data.decode()
    assert response.status_code == 200
    assert "Welcome, john@simplylift.co" in data


def test_show_summary_with_invalid_email(client):
    response = client.post("/showSummary", data={"email": "invalid@example.com"})
    data = response.data.decode()
    assert response.status_code == 200
    assert "index.html" in data
    assert "The email you entered isn't found, please try again." in data
