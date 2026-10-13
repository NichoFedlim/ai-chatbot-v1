"""
Test cases for API endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from app.models import ChatMessage

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    """Create test client."""
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as test_client:
        yield test_client
    Base.metadata.drop_all(bind=engine)

def test_root(client):
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_chat_endpoint(client):
    """Test chat endpoint."""
    response = client.post("/api/chat", json={"message": "Hello"})
    assert response.status_code == 200
    assert "message" in response.json()

def test_chat_validation(client):
    """Test chat endpoint validation."""
    # Test empty message
    response = client.post("/api/chat", json={"message": ""})
    assert response.status_code == 422
    
    # Test missing message field
    response = client.post("/api/chat", json={})
    assert response.status_code == 422

def test_get_history(client):
    """Test get history endpoint."""
    # First, add some messages
    client.post("/api/chat", json={"message": "Test message 1"})
    client.post("/api/chat", json={"message": "Test message 2"})
    
    # Then get history
    response = client.get("/api/history")
    assert response.status_code == 200
    assert response.json()["total_count"] >= 2

def test_delete_message(client):
    """Test delete message endpoint."""
    # Add a message
    response = client.post("/api/chat", json={"message": "Delete me"})
    assert response.status_code == 200
    
    # Get history to find message ID
    history_response = client.get("/api/history")
    messages = history_response.json()["messages"]
    
    if messages:
        message_id = messages[0]["id"]
        
        # Delete the message
        delete_response = client.delete(f"/api/history/{message_id}")
        assert delete_response.status_code == 200
        assert delete_response.json()["success"] == True

def test_clear_history(client):
    """Test clear history endpoint."""
    # Add some messages
    client.post("/api/chat", json={"message": "Message to clear 1"})
    client.post("/api/chat", json={"message": "Message to clear 2"})
    
    # Clear history
    response = client.post("/api/clear")
    assert response.status_code == 200
    assert response.json()["success"] == True
    
    # Verify history is empty
    history_response = client.get("/api/history")
    assert history_response.json()["total_count"] == 0

def test_rate_limiting(client):
    """Test rate limiting."""
    # Make multiple rapid requests
    responses = []
    for i in range(35):  # More than rate limit
        response = client.post("/api/chat", json={"message": f"Rate limit test {i}"})
        responses.append(response.status_code)
    
    # Check if any request was rate limited
    assert 429 in responses
    