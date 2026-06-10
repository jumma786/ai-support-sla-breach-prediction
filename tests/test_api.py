"""Tests for API endpoints."""

import pytest
from fastapi.testclient import TestClient

from src.api.app import create_app


@pytest.fixture
def client():
    app = create_app()
    with TestClient(app) as test_client:  # triggers lifespan (model loading)
        yield test_client


PAYLOAD = {
    "customer_segment": "Enterprise",
    "priority_initial": "Critical",
    "issue_category": "service_outage",
    "agent_queue_length_at_submit": 50,
    "backlog_age_hours": 18.0,
    "negative_sentiment_flag": 1,
    "message_has_deadline": 1,
}


class TestAPIEndpoints:
    def test_health_check(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_predict(self, client):
        response = client.post("/predict", json=PAYLOAD)
        assert response.status_code in (200, 503)  # 503 if model file absent
        if response.status_code == 200:
            data = response.json()
            assert data["prediction"] in (0, 1)
            assert 0.0 <= data["probability"] <= 1.0
            assert data["risk_factors"]

    def test_predict_validation_error(self, client):
        response = client.post("/predict", json={"customer_segment": "Enterprise"})
        assert response.status_code == 422

    def test_predict_batch(self, client):
        response = client.post("/predict-batch", json={"records": [PAYLOAD, PAYLOAD]})
        assert response.status_code in (200, 503)
        if response.status_code == 200:
            assert response.json()["total_records"] == 2
