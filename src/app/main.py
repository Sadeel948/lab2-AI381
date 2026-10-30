from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel


ROOT_DIR = Path(__file__).resolve().parents[2]
MODEL_PATH = ROOT_DIR / "models" / "model.joblib"

FEATURES = [
    "tenure_months",
    "monthly_fee",
    "contract",
    "internet_service",
    "support_calls",
]

class Customer(BaseModel):
    tenure_months: int
    monthly_fee: float
    contract: str
    internet_service: str
    support_calls: int

app = FastAPI(title="AI381 Lab 1 churn API")
model = joblib.load(MODEL_PATH)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(customer: Customer):
    X = pd.DataFrame([customer.model_dump()])[FEATURES]

    probability = float(model.predict_proba(X)[0, 1])

    return {
        "churn_probability": round(probability, 3)
    }

