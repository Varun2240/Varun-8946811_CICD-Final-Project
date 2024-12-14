from app import app
from backend.app import app
def test_health_check():
    with app.test_client() as client:
        response = client.get('/api/health-check')
        assert response.status_code == 200
        assert response.json['status'] == 'ok'
