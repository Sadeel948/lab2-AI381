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
