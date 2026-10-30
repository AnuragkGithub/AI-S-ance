"""Lightweight smoke checks; run from the project root with pytest."""
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json()['ok'] is True

def test_homepage_served():
    response = client.get('/')
    assert response.status_code == 200
    assert 'REPO SÉANCE' in response.text

def test_github_url_validation_rejects_non_github():
    response = client.post('/api/repositories/clone', json={'url':'https://example.com/owner/repo'})
    assert response.status_code == 400
