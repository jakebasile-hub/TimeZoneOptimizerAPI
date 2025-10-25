import pytest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from fastapi.testclient import TestClient
from main import app
from auth import auth_manager


class TestAPI:
    def setup_method(self):
        self.client = TestClient(app)
        # Create a test API key
        self.test_api_key = auth_manager.create_api_key("test_user")
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = self.client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "uptime" in data
        assert data["uptime"] >= 0
    
    def test_optimize_endpoint_missing_api_key(self):
        """Test optimize endpoint without API key"""
        request_data = {
            "participants": [
                {"name": "Alice", "location": "New York, USA"},
                {"name": "Bob", "location": "London, UK"}
            ],
            "duration_minutes": 60,
            "num_alternatives": 2
        }
        
        response = self.client.post("/optimize", json=request_data)
        assert response.status_code == 401
        assert "API key required" in response.json()["error"]
    
    def test_optimize_endpoint_invalid_api_key(self):
        """Test optimize endpoint with invalid API key"""
        request_data = {
            "participants": [
                {"name": "Alice", "location": "New York, USA"},
                {"name": "Bob", "location": "London, UK"}
            ],
            "duration_minutes": 60,
            "num_alternatives": 2
        }
        
        headers = {"X-API-Key": "invalid_key"}
        response = self.client.post("/optimize", json=request_data, headers=headers)
        assert response.status_code == 401
        assert "Invalid API key" in response.json()["error"]
    
    def test_optimize_endpoint_valid_request(self):
        """Test optimize endpoint with valid request"""
        request_data = {
            "participants": [
                {"name": "Alice", "location": "New York, USA"},
                {"name": "Bob", "location": "London, UK"}
            ],
            "duration_minutes": 60,
            "num_alternatives": 2
        }
        
        headers = {"X-API-Key": self.test_api_key}
        response = self.client.post("/optimize", json=request_data, headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert "best_meeting_time_utc" in data
        assert "local_times" in data
        assert "alternatives" in data
        
        # Check local times
        assert len(data["local_times"]) == 2
        assert data["local_times"][0]["name"] == "Alice"
        assert data["local_times"][1]["name"] == "Bob"
        
        # Check alternatives
        assert len(data["alternatives"]) <= 2
        for alt in data["alternatives"]:
            assert "utc_time" in alt
            assert "fairness_score" in alt
    
    def test_optimize_endpoint_validation(self):
        """Test request validation"""
        # Test with invalid duration
        request_data = {
            "participants": [{"name": "Alice", "location": "New York, USA"}],
            "duration_minutes": 5,  # Too short
            "num_alternatives": 1
        }
        
        headers = {"X-API-Key": self.test_api_key}
        response = self.client.post("/optimize", json=request_data, headers=headers)
        assert response.status_code == 422  # Validation error
    
    def test_create_api_key_endpoint(self):
        """Test API key creation endpoint"""
        response = self.client.post("/create-key", params={"user_id": "new_user"})
        assert response.status_code == 200
        
        data = response.json()
        assert "api_key" in data
        assert "message" in data
        assert data["message"] == "API key created successfully"
    
    def test_usage_endpoint(self):
        """Test usage stats endpoint"""
        headers = {"X-API-Key": self.test_api_key}
        response = self.client.get("/usage", headers=headers)
        assert response.status_code == 200
