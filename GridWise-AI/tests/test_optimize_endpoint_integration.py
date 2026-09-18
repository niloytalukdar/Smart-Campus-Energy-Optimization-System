import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)

@patch('app.services.llm_interpreter.openai.OpenAI')
def test_optimize_energy_integration(mock_openai):
    mock_client = MagicMock()
    mock_openai.return_value = mock_client
    
    mock_response = MagicMock()
    mock_message = MagicMock(content='[{"directive_type": "no_charge_window", "hours": [14, 15], "factor": null}]')
    mock_response.choices = [MagicMock(message=mock_message)]
    mock_client.chat.completions.create.return_value = mock_response
    
    req = {
        "scenario_id": "GRID-101",
        "operator_notes": ["Do not charge between 2 PM and 4 PM"],
        "battery": {
            "capacity_kwh": 100.0,
            "initial_energy_kwh": 50.0,
            "max_charge_rate_kwh": 25.0,
            "max_discharge_rate_kwh": 25.0,
            "charge_efficiency": 0.95,
            "discharge_efficiency": 0.95
        },
        "hours": [
            {
                "hour": h,
                "demand_kwh": 20.0,
                "solar_kwh": 10.0 if 8 <= h <= 17 else 0.0,
                "price": 0.1 if h < 12 else 0.5
            }
            for h in range(24)
        ]
    }
    
    response = client.post("/optimize-energy", json=req)
    assert response.status_code == 200
    data = response.json()
    assert data["scenario_id"] == "GRID-101"
    assert data["status"] == "ok"
    assert len(data["hourly_plan"]) == 24
    assert len(data["directive_interpretation"]) == 1

def test_optimize_energy_malformed_request():
    req = {
        "scenario_id": "GRID-102",
        "operator_notes": [],
        "battery": {
            "capacity_kwh": 100.0,
            "initial_energy_kwh": 150.0 
        },
        "hours": []
    }
    response = client.post("/optimize-energy", json=req)
    assert response.status_code == 422
