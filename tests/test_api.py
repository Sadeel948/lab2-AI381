from pathlib import Path

import joblib
from fastapi.testclient import TestClient

from src.app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_predict():
    customer = {
        "tenure_months": 24,
        "monthly_fee": 75.5,
        "contract": "one-year",
        "internet_service": "fiber",
        "support_calls": 3
    }

    response = client.post("/predict", json=customer)

    assert response.status_code == 200

    result = response.json()

    assert "churn_probability" in result
    assert 0 <= result["churn_probability"] <= 1

def test_invalid_input_schema():
    customer = {
        "tenure_months": 24,
        "monthly_fee": 75.5,
        "contract": "one-year",
        "internet_service": "fiber"
        # support_calls is missing
    }

    response = client.post("/predict", json=customer)

    assert response.status_code == 422

def test_negative_tenure():
    customer = {
        "tenure_months": -10,
        "monthly_fee": 75.5,
        "contract": "one-year",
        "internet_service": "fiber",
        "support_calls": 3
    }

    response = client.post("/predict", json=customer)

    assert response.status_code == 422

def test_deterministic_prediction():
    customer = {
        "tenure_months": 24,
        "monthly_fee": 75.5,
        "contract": "one-year",
        "internet_service": "fiber",
        "support_calls": 3
    }

    response1 = client.post("/predict", json=customer)
    response2 = client.post("/predict", json=customer)

    assert response1.status_code == 200
    assert response2.status_code == 200

    assert (
        response1.json()["churn_probability"]
        == response2.json()["churn_probability"]
    )

def test_model_loads():
    model_path = (
        Path(__file__).resolve().parents[1]
        / "models"
        / "model.joblib"
    )

    model = joblib.load(model_path)

    assert model is not None