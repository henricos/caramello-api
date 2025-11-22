from fastapi.testclient import TestClient
from caramello.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Caramello API"}

def test_routers_registered():
    # Check if routes are registered
    routes = [route.path for route in app.routes]
    assert "/users/" in routes
    assert "/family/" in routes
    assert "/family_members/" in routes
    assert "/family_invitations/" in routes
