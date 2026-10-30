
from pathlib import Path

import joblib
import pandas as pd
import sklearn


ROOT_DIR = Path(__file__).resolve().parents[2]

DATA_PATH = ROOT_DIR / "data" / "churn_v2.csv"
MODEL_PATH = ROOT_DIR / "models" / "model.joblib"

FEATURES = [
    "tenure_months",
    "monthly_fee",
    "support_calls",
    "contract",
    "internet_service",
]

TARGET = "churn"
EXPECTED_SKLEARN_VERSION = "1.9.1"


def load_dataset():
    """Load the dataset and validate its required columns."""
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    required_columns = FEATURES + [TARGET]
    missing = set(required_columns) - set(df.columns)

    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")

    if df.empty:
        raise ValueError("The dataset is empty.")

    if df[TARGET].isna().any():
        raise ValueError("The target column contains missing values.")

    if not df[TARGET].isin([0, 1]).all():
        raise ValueError("The target must contain only 0 and 1.")

    return df


def load_existing_model(df):
    """Load the saved model and verify that it makes predictions."""

    if sklearn.__version__ != EXPECTED_SKLEARN_VERSION:
        raise RuntimeError(
            f"Expected scikit-learn {EXPECTED_SKLEARN_VERSION}, "
            f"but found {sklearn.__version__}."
        )

    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

    model = joblib.load(MODEL_PATH)

    model_features = list(model.feature_names_in_)

    if model_features != FEATURES:
        raise ValueError(
            f"Model features do not match. Got: {model_features}"
        )

    sample = df[FEATURES].head(5)
    predictions = model.predict(sample)

    if len(predictions) != len(sample):
        raise ValueError("Unexpected number of predictions.")

    if not set(predictions).issubset({0, 1}):
        raise ValueError("The model returned unexpected labels.")

    return model

def main():
    """Load the dataset and validate the existing model."""
    df = load_dataset()
    model = load_existing_model(df)

    print(f"Dataset loaded: {len(df)} rows")
    print("Model loaded successfully.")
    print("Sample predictions:", model.predict(df[FEATURES].head(5)))


if __name__ == "__main__":
    main()
