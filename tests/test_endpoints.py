import pytest
from transplant.app import create_app

@pytest.fixture
def app():
    """Needed for pytest-flask."""
    app = create_app()
    return app

def test_autoland_response(client):
    response = client.post('/autoland')
    assert response.status_code == 200
    assert response.json == {'request_id': 1}
