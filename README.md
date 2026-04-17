# California Median Housing Price Prediction (End-to-End MLOps)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![Flask](https://img.shields.io/badge/Flask-Web%20API-black.svg)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-orange.svg)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-150458.svg)
![NumPy](https://img.shields.io/badge/NumPy-Numerical%20Computing-013243.svg)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED.svg)
![Gunicorn](https://img.shields.io/badge/Gunicorn-WSGI%20Server-499848.svg)

## Description

This project is an end-to-end machine learning workflow for estimating California median house prices from structured housing features. It covers exploratory data analysis (EDA), model experimentation with multiple regression algorithms, and deployment of a selected pre-trained model.

The application serves predictions through:

- A web interface for manual feature input and quick testing.
- A JSON API endpoint for programmatic integration.

At runtime, user-provided features are transformed using a persisted feature scaler and passed into a pre-trained Random Forest regressor to generate a price estimate.

## Architecture / Workflow

### High-Level Pipeline

1. Data exploration and analysis in `EDA.ipynb`.
2. Model experimentation (e.g., Linear Regression and Random Forest Regression).
3. Model selection and serialization of:
	 - `randomforest.pkl` (trained model)
	 - `scaler.pkl` (feature scaler)
4. Flask app loads serialized artifacts at startup.
5. Input features are validated/coerced to numeric values.
6. Features are scaled and passed to model inference.
7. Predicted median price is returned via HTML view or JSON response.

### Runtime Request Flow

```text
Client (Browser/API)
	 -> Flask Endpoint (/predict or /predict_api)
			-> Parse Input Features
			-> Apply scaler.pkl
			-> Predict with randomforest.pkl
	 -> Return estimated house price
```

## Prerequisites

- Python 3.10+ recommended
- `pip` (latest recommended)
- Git
- Optional (for deployment/packaging):
	- Docker
	- Gunicorn

Core Python dependencies are listed in `requirements.txt`:

- Flask
- scikit-learn
- pandas
- numpy
- matplotlib
- seaborn
- gunicorn

## Setup and Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd california_mediun_housing_prediction
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Verify required model artifacts exist

Ensure these files are present in the project root:

- `randomforest.pkl`
- `scaler.pkl`

### 5. Run the application

```bash
python app.py
```

The app should be available at:

```text
http://127.0.0.1:5000
```

## Usage

### Option A: Web Interface

1. Open `http://127.0.0.1:5000` in your browser.
2. Enter the housing feature values.
3. Submit the form to get an estimated price.

### Option B: JSON API

Endpoint:

```http
POST /predict_api
Content-Type: application/json
```

Example request:

```bash
curl -X POST http://127.0.0.1:5000/predict_api \
	-H "Content-Type: application/json" \
	-d '{
		"data": {
			"MedInc": 8.3252,
			"HouseAge": 41.0,
			"AveRooms": 6.984,
			"AveBedrms": 1.024,
			"Population": 322.0,
			"AveOccup": 2.555,
			"Latitude": 37.88,
			"Longitude": -122.23
		}
	}'
```

Example response:

```json
2.931
```

### Production-style run with Gunicorn

```bash
gunicorn --workers=4 --bind 0.0.0.0:5000 app:app
```

### Container run (optional)

```bash
docker build -t california-housing-ml .
docker run -p 5000:5000 -e PORT=5000 california-housing-ml
```

## Technologies Used

- Python
- Flask
- scikit-learn
- pandas
- numpy
- matplotlib
- seaborn
- Jinja2 (Flask templating)
- Gunicorn
- Docker
- Jupyter Notebook

## Project Structure

```text
.
|-- app.py
|-- EDA.ipynb
|-- randomforest.pkl
|-- scaler.pkl
|-- requirements.txt
|-- Dockerfile
|-- Procfile
|-- templates/
|   `-- home.html
`-- README.md
```

## Hosted on GitHub (Packages)

GitHub Pages does **not** support running server-side applications (like Python/Flask) directly. Instead, this project uses GitHub Actions to automatically build and host the finished Docker Image via **GitHub Container Registry (GHCR)**.

This setup prevents needing a third-party paid service simply to host the image. Any user or server can pull down the pre-built environment from GitHub without having to worry about missing PIP dependencies or incompatible environments.

### Automated CI/CD Setup

There is a CI/CD workflow at `.github/workflows/main.yaml` with two jobs:

- `ci`: installs dependencies and unconditionally runs the smoke testing framework (`python -m unittest discover -s tests -p "test_*.py"`) validation.
- `publish`: runs only on `main` branch pushes after a successful `ci` check. It logs into GHCR, builds the container image, and pushes it up as the latest release, accessible within the repository's `Packages` tab.

No external secrets or API keys are required; it natively relies on the `GITHUB_TOKEN` secret built into GitHub Actions.

### Deployment Behavior 

- Pull requests to `main`: run CI checks only (no Docker image publish)
- Pushes to `main`: run CI, then automatically publish the fresh artifact to GHCR
- Manual trigger: use **Actions -> CI and Publish to GHCR -> Run workflow**

### Local Smoke Test Command

```bash
python -m unittest discover -s tests -p "test_*.py"
```

