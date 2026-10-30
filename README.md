# AI381 Lab 2 — Churn Prediction API

[![CI Pipeline](https://github.com/Sadeel948/lab2-AI381/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/Sadeel948/lab2-AI381/actions/workflows/ci.yml)

## Project Overview

This project packages a Machine Learning churn prediction model into a REST API using FastAPI and Docker.

The application loads a trained Scikit-learn model and predicts the probability of customer churn based on customer information.

## Project Structure

```text
lab2-AI381/
├── .github/
│   └── workflows/
│       └── ci.yml
├── data/
│   └── churn_v2.csv
├── models/
│   └── model.joblib
├── src/
│   ├── app/
│   │   └── main.py
│   └── train/
│       └── train.py
├── tests/
│   └── test_api.py
├── Dockerfile
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

## Technologies Used

- Python 3.11
- Scikit-learn
- Pandas
- FastAPI
- Pydantic
- Pytest
- Ruff
- Docker
- GitHub Actions
- Trivy
- GitHub Container Registry (GHCR)

## Running the Application

### Run using Docker (Recommended)

Pull and run the published image with one command:

```bash
docker run --rm -p 8000:8000 ghcr.io/sadeel948/lab2-ai381:2fef8517126a551d9831472a27ecafa2986d24dc
```

The API will be available at:

- Health check: http://localhost:8000/health
- Prediction: http://localhost:8000/predict
- Interactive API documentation: http://localhost:8000/docs

### Build locally

```bash
docker build -t churn-api .
docker run --rm -p 8000:8000 churn-api
```

## API Endpoints

### GET /health

Checks whether the API is running.

Example response:

```json
{
  "status": "ok"
}
```

### POST /predict

Accepts customer information and returns a churn probability.

Example request:

```json
{
  "tenure_months": 12,
  "monthly_fee": 75.5,
  "contract": "Month-to-month",
  "internet_service": "Fiber optic",
  "support_calls": 2
}
```

Example response:

```json
{
  "churn_probability": 0.735
}
```

The probability is a model prediction, not a guaranteed outcome.

## Testing

Install development dependencies:

```bash
pip install -r requirements-dev.txt
```

Run the tests:

```bash
python -m pytest -v
```

Run linting:

```bash
ruff check src tests
```

The test suite includes API health checks, prediction tests, input validation, edge cases, deterministic predictions, and model loading.

## Continuous Integration and Security

GitHub Actions automatically runs the following steps:

1. Install dependencies.
2. Run Ruff linting.
3. Run Pytest.
4. Build the Docker image.
5. Scan the image using Trivy.
6. Publish the image to GHCR when code is pushed to `main`.

The Trivy scan checks for HIGH and CRITICAL vulnerabilities with `ignore-unfixed` enabled.

## Docker Image

Published image:

```text
ghcr.io/sadeel948/lab2-ai381
```

Image tag:

```text
2fef8517126a551d9831472a27ecafa2986d24dc
```

Image digest:

```text
sha256:83c04a82eee31269134cd786b97e5b3d525d1309bc5572600cecf22e6024a7dc
```

## Author

AI381 — Machine Learning Operations  
Jordan University of Science and Technology (JUST)