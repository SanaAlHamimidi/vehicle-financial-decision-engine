# Vehicle Financial Decision Engine
### CS163 Senior Project · Group 20 · San José State University · Spring 2026
**Team:** Nyi Wai Yan Tun, Sana Al Hamimidi

🌐 **Live Website:** [https://cs163seniorproject.uw.r.appspot.com](https://cs163seniorproject.uw.r.appspot.com)

---

## What Is This Repo?

A data-driven resale value and depreciation analysis tool for the California used car market. Our project combines 50,000+ Craigslist vehicle listings, 3.6 million California DMV registration records, and an XGBoost model to predict used car resale prices and analyze how geography, fuel type, and vehicle characteristics influence vehicle's long-term financial value.

The system answers three research questions:
1. Which vehicle features have the most impact on depreciation/appreciation the most?
2. How does geography in California affect resale value?
3. Does selling the same vehicle across different California regions yield different resale prices?

---

## Repository Structure

```
vehicle-financial-decision-engine/
├── notebooks/
│   ├── CS163_Vehicle.ipynb        # EDA, preprocessing, registration data analysis
│   └── CS163_Notebook2.ipynb      # Feature engineering, demand score, XGBoost, K-Means
├── api/
│   ├── app.py                     # Flask REST API — prediction endpoint
│   ├── Dockerfile                 # Container definition
│   └── requirements.txt           # Python dependencies
├── website/
│   ├── index.html                 # Landing page with prediction form
│   ├── objectives.html            # Project objectives and data sources
│   ├── methods.html               # Analytical methods and system architecture
│   ├── findings.html              # Major findings with interactive chart
│   └── app.yaml                   # Google App Engine configuration
└── README.md
```

---

## Analysis Pipeline

```
Raw Data (8 datasets)
        │
        ▼
Preprocessing & Cleaning
(outlier removal, null handling, standardization)
        │
        ▼
Feature Engineering
├── Demand Score: ZIP → Region mapping via pgeocode
│   Aggregate registrations by region + make + fuel (2019–2024)
│   Normalize to 0–1 score
└── Depreciation Rate: (avg_msrp − price) / avg_msrp
        │
        ▼
Model Training
├── XGBoost Regressor → predicts resale price
└── K-Means Clustering (K=5) → depreciation tier profiles
        │
        ▼
Deployment
├── Flask API → Docker → Google Cloud Run
├── Model artifacts → Google Cloud Storage
└── Website → Google App Engine
```

---

## Setup Instructions

### Prerequisites
- Python 3.10+
- Google Cloud SDK (`gcloud`)
- Docker Desktop

### Running the API Locally

```bash
# Clone the repo
git clone https://github.com/SanaAlHamimidi/vehicle-financial-decision-engine.git
cd vehicle-financial-decision-engine/api

# Install dependencies
pip install -r requirements.txt

# Run Flask app
python app.py
```

### Running the Notebooks

Open notebooks in Google Colab. Update the file paths to point to your Google Drive folder containing the datasets.

**Required datasets:**
- `vehicles.csv` — Craigslist used car listings
- `vehicle-fuel-type-count-*.csv` (×6) — California DMV registration data 2019–2024
- `car_data.csv` — Vehicle MSRP reference data

---

## Inference Service

**Location:** `api/` directory

**Service URL:** `https://depreciation-api-680233638391.us-west1.run.app`

The inference service is a Flask REST API containerized with Docker and deployed on Google Cloud Run. It loads the trained XGBoost model and supporting files from Google Cloud Storage on startup.

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/predict` | Predict resale price for a vehicle |
| GET | `/health` | Health check |

### POST /predict

**Input (JSON):**
```json
{
  "manufacturer": "toyota",
  "year": 2018,
  "odometer": 50000,
  "condition": "good",
  "fuel": "gas",
  "type": "sedan",
  "region": "los angeles"
}
```

**Output (JSON):**
```json
{
  "predicted_price": 21876.29,
  "demand_score": 1.0
}
```

The demand score is automatically calculated from the region, manufacturer, and fuel type using the pre-computed lookup table. Users do not need to provide it.

### Docker

```bash
# Build
docker build -t depreciation-api .

# Run locally
docker run -p 8080:8080 depreciation-api
```

---

## Data Stored in the Cloud

**Storage:** Google Cloud Storage bucket — `gs://cs163-vehicle-depreciation/`

| File | Description | Size |
|------|-------------|------|
| `xgboost_model.pkl` | Trained XGBoost regressor | 453 KB |
| `label_encoders.pkl` | Fitted label encoders for categorical features | 2.3 KB |
| `demand_lookup.csv` | Pre-computed demand scores by region, make, fuel type | 229 KB |

The Flask API loads all three files from Cloud Storage on startup using the `google-cloud-storage` Python client. This separates model artifacts from application code, enables model updates without container rebuilds, and satisfies the cloud database requirement.

---

## System Design

```
┌─────────────────────────────────────────────────────┐
│                   User's Browser                     │
│         https://cs163seniorproject.uw.r.appspot.com  │
└──────────────────────┬──────────────────────────────┘
                       │ HTTP request
                       ▼
┌─────────────────────────────────────────────────────┐
│              Google App Engine                       │
│         Static website (HTML/CSS/JS)                 │
│  index.html, objectives.html, methods.html,          │
│  findings.html                                       │
└──────────────────────┬──────────────────────────────┘
                       │ POST /predict (JavaScript fetch)
                       ▼
┌─────────────────────────────────────────────────────┐
│              Google Cloud Run                        │
│         Flask API (Docker container)                 │
│    - Receives car details                            │
│    - Looks up demand score                           │
│    - Encodes categorical features                    │
│    - Runs XGBoost prediction                         │
│    - Returns predicted price                         │
└──────────────────────┬──────────────────────────────┘
                       │ Load model artifacts on startup
                       ▼
┌─────────────────────────────────────────────────────┐
│           Google Cloud Storage                       │
│    gs://cs163-vehicle-depreciation/                  │
│    - xgboost_model.pkl                               │
│    - label_encoders.pkl                              │
│    - demand_lookup.csv                               │
└─────────────────────────────────────────────────────┘
```

### Scalability

**Google Cloud Run** automatically scales the inference service from 0 to N instances based on incoming request volume. Each container instance handles requests independently with no shared state — all state lives in Cloud Storage. This means the system can handle sudden traffic spikes (e.g., many students visiting at once) without manual intervention.

**Google App Engine** serves the static website with Google's global CDN infrastructure, ensuring fast load times regardless of user location.

**Google Cloud Storage** is globally replicated and highly available. Model files are loaded once at container startup and cached in memory for the lifetime of the instance, minimizing latency per prediction request.

---

## Key Results

| Metric | Value |
|--------|-------|
| R² Score | 0.779 |
| RMSE | $5,891 |
| Training samples | 37,991 |
| Top predictor | Fuel type (27% importance) |
| Highest depreciation region | Siskiyou County (61%) |
| Lowest depreciation region | Imperial County (-10%, appreciating) |
| Best value retention brand | Tesla (0.08 depreciation rate) |
| Largest regional price gap | $28,550 (same truck, Imperial County vs LA) |

---

## References

- California DMV Open Data Portal — Vehicle Registration by Fuel Type
- Craigslist Used Vehicle Listings Dataset (Kaggle)
- scikit-learn: Machine Learning in Python — Pedregosa et al., JMLR 2011
