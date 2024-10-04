import pytest
from flask import json
from unittest.mock import patch
from gatekeeper.app import app
from gatekeeper.models import db
from gatekeeper.tests.conf import SQLALCHEMY_DATABASE_URI, TESTING


@pytest.fixture(autouse=True)
def setup_database():
    app.config["TESTING"] = TESTING
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    with app.app_context():
        db.create_all()
        yield
        db.drop_all()


class TestGatekeeper:
    @pytest.fixture(autouse=True)
    def client(self):
        with app.test_client() as client:
            yield client

    def test_get_gate_status_default(self, client):
        response = client.get("/gate/status")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] is True
        assert "last_modified" in data

    def test_update_gate_status_valid(self, client):
        response = client.post("/gate/status", json={"status": False})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["message"] == "Gate status updated to False"
        assert data["status"] is False

    def test_update_gate_status_invalid(self, client):
        response = client.post("/gate/status", json={"status": "invalid"})
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data["error"] == "Invalid status"

    @patch("gatekeeper.models.GateStatus")
    def test_update_gate_status_when_no_gate_status_exists(
        self, mock_gate_status, client
    ):
        mock_gate_status.query.first.return_value = None

        response = client.post("/gate/status", json={"status": True})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["message"] == "Gate status updated to True"
        assert data["status"] is True
