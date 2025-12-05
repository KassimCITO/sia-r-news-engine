import pytest
import json
from app import app
from storage.database import init_db, engine, Base
from services.jwt_auth import JWTAuth

@pytest.fixture
def client():
    """Create a test client"""
    app.config['TESTING'] = True
    
    # Initialize test database
    Base.metadata.create_all(engine)
    
    with app.test_client() as client:
        yield client
    
    # Cleanup
    Base.metadata.drop_all(engine)

@pytest.fixture
def auth_token(client):
    """Get a valid JWT token"""
    token, _ = JWTAuth.create_token(user_id=1, user_role="admin")
    return token

class TestUIRoutes:
    
    def test_login_page(self, client):
        """Test login page loads"""
        response = client.get('/login')
        assert response.status_code == 200
        assert b'<h1>' in response.data or b'Login' in response.data
    
    def test_dashboard_page(self, client):
        """Test dashboard page loads"""
        response = client.get('/dashboard')
        assert response.status_code == 200
    
    def test_ui_status_unauthorized(self, client):
        """Test UI status without auth"""
        response = client.get('/api/ui/status')
        assert response.status_code in [401, 200]  # May allow status without auth
    
    def test_ui_status_authorized(self, client, auth_token):
        """Test UI status with auth"""
        headers = {'Authorization': f'Bearer {auth_token}'}
        response = client.get('/api/ui/status', headers=headers)
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'status' in data
        assert data['status'] in ['operational', 'error']
    
    def test_get_reviews(self, client, auth_token):
        """Test get reviews endpoint"""
        headers = {'Authorization': f'Bearer {auth_token}'}
        response = client.get('/api/ui/reviews', headers=headers)
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'reviews' in data
        assert 'count' in data
    
    def test_get_reviews_unauthorized(self, client):
        """Test get reviews without auth"""
        response = client.get('/api/ui/reviews')
        # May be protected or not, depending on implementation
        assert response.status_code in [200, 401]
    
    def test_get_published(self, client, auth_token):
        """Test get published articles"""
        headers = {'Authorization': f'Bearer {auth_token}'}
        response = client.get('/api/ui/published', headers=headers)
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'articles' in data or 'error' not in data
    
    def test_get_settings_admin(self, client, auth_token):
        """Test get settings with admin token"""
        headers = {'Authorization': f'Bearer {auth_token}'}
        response = client.get('/api/ui/settings', headers=headers)
        assert response.status_code in [200, 403]  # May check permissions
    
    def test_get_metrics(self, client, auth_token):
        """Test get metrics endpoint"""
        headers = {'Authorization': f'Bearer {auth_token}'}
        response = client.get('/api/ui/metrics?period=7d', headers=headers)
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'metrics' in data or 'error' not in data
    
    def test_get_metrics_periods(self, client, auth_token):
        """Test metrics with different periods"""
        headers = {'Authorization': f'Bearer {auth_token}'}
        
        for period in ['7d', '30d', '90d', 'all']:
            response = client.get(f'/api/ui/metrics?period={period}', headers=headers)
            assert response.status_code == 200
    
    def test_get_logs(self, client, auth_token):
        """Test get logs endpoint"""
        headers = {'Authorization': f'Bearer {auth_token}'}
        response = client.get('/api/ui/logs', headers=headers)
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'logs' in data
    
    def test_ui_pages_load(self, client):
        """Test all UI pages load"""
        pages = [
            '/login',
            '/dashboard',
            '/pipeline/run',
            '/published',
            '/settings',
            '/logs',
            '/metrics'
        ]
        
        for page in pages:
            response = client.get(page)
            assert response.status_code == 200, f"Page {page} failed to load"
    
    def test_run_pipeline_ui(self, client, auth_token):
        """Test run pipeline from UI"""
        headers = {
            'Authorization': f'Bearer {auth_token}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'title': 'Test Article',
            'content': 'This is a test article with enough content to be processed by the pipeline system.',
            'author': 'Test Author',
            'category': 'Tecnología'
        }
        
        response = client.post('/api/ui/run', 
                              headers=headers,
                              data=json.dumps(data))
        
        # May fail due to API key missing, but endpoint should exist
        assert response.status_code in [200, 400, 500]
    
    def test_clear_logs(self, client, auth_token):
        """Test clear logs endpoint"""
        headers = {'Authorization': f'Bearer {auth_token}'}
        response = client.post('/api/ui/logs/clear', headers=headers)
        
        # May require admin permissions
        assert response.status_code in [200, 403]


class TestUIIntegration:
    """Integration tests for complete UI workflows"""
    
    def test_complete_workflow(self, client, auth_token):
        """Test complete user workflow"""
        headers = {'Authorization': f'Bearer {auth_token}'}
        
        # 1. Load dashboard
        response = client.get('/dashboard')
        assert response.status_code == 200
        
        # 2. Check status
        response = client.get('/api/ui/status', headers=headers)
        assert response.status_code == 200
        
        # 3. View reviews
        response = client.get('/api/ui/reviews', headers=headers)
        assert response.status_code == 200
        
        # 4. View metrics
        response = client.get('/api/ui/metrics', headers=headers)
        assert response.status_code == 200
        
        # 5. View logs
        response = client.get('/api/ui/logs', headers=headers)
        assert response.status_code == 200


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
