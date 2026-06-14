# 📈 Stock Prediction MLOps System

**Live Dashboard:** [https://stockpredictionmlops-jxahbuhq2jqqu464mgqyul.streamlit.app/](https://stockpredictionmlops-jxahbuhq2jqqu464mgqyul.streamlit.app/)

**API Endpoint:** [https://stockpredictionmlops-production-83a6.up.railway.app/](https://stockpredictionmlops-production-83a6.up.railway.app/)

**Experiment Tracking:** [https://api.wandb.ai/links/hanseeka-dhingana-sukkur-iba-university/vgs0jzg2](https://api.wandb.ai/links/hanseeka-dhingana-sukkur-iba-university/vgs0jzg2)

---

## 📋 Table of Contents

* [Project Overview](#-project-overview)
* [System Architecture](#️-system-architecture)
* [Key Features](#-key-features)
* [Technology Stack](#️-technology-stack)
* [Installation & Setup](#-installation--setup)
* [Project Structure](#-project-structure)
* [MLOps Pipelines (CI/CD/CT)](#-mlops-pipelines-cicdct)
* [API Documentation](#-api-documentation)
* [Performance & Results](#-performance--results)

---

## 🎯 Project Overview

**Stock Prediction MLOps** is an end-to-end Machine Learning system designed to predict the next day's stock price using historical market data. Unlike static notebooks, this project implements a full **MLOps lifecycle**: automated data ingestion, a centralized feature store, continuous training (CT), and automated deployment.

### 🏆 Objectives Achieved

* ✅ **Automated Data Pipeline:** Live data fetching from Yahoo Finance (`yfinance`).
* ✅ **Feature Store:** Centralized storage of engineered features using **MongoDB Atlas**.
* ✅ **Experiment Tracking:** Model metrics and artifacts tracked via **Weights & Biases (WandB)**.
* ✅ **Continuous Training (CT):** Weekly automated retraining via GitHub Actions to adapt to new market trends.
* ✅ **Continuous Integration (CI):** Automated unit testing with `pytest`.
* ✅ **Continuous Deployment (CD):** Auto-deployment to **Railway** (Backend) and **Streamlit** (Frontend).

---

## 🏗️ System Architecture

### High-Level Data Flow

```ascii
┌──────────────┐     ┌──────────────────┐     ┌─────────────────┐
│ Yahoo Finance│────▶│  Data Ingestion  │────▶│  Feature Store  │
│     API      │     │   & Processing   │     │ (MongoDB Atlas) │
└──────────────┘     └──────────────────┘     └─────────────────┘
                                                       │
                                                       ▼
┌──────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Streamlit   │◀───▶│ FastAPI Service  │◀────│ Model Training  │
│  Dashboard   │     │    (Railway)     │     │    (GitHub)     │
└──────────────┘     └──────────────────┘     └─────────────────┘
                                                       │
                                                       ▼
                                              ┌─────────────────┐
                                              │ Experiment Logs │
                                              │     (WandB)     │
                                              └─────────────────┘

```

### Component Details

1. **Data Layer:** Fetches raw stock data, calculates Technical Indicators (SMA, Volatility), and pushes them to **MongoDB**.
2. **ML Layer:** An Ensemble Model (Linear Regression + Random Forest + XGBoost) trained on data pulled from the Feature Store.
3. **Ops Layer:** GitHub Actions handles the "Self-Learning" loop (Retraining) and "Quality Gate" (Testing).
4. **Serving Layer:** FastAPI provides a REST endpoint for predictions; Streamlit consumes this API for the UI.

---

## ✨ Key Features

### 1. 🧠 Automated Data Pipeline (Continuous Training)

The system doesn't just sit there. Every **Sunday at Midnight**, a GitHub Action:

1. Wakes up and downloads fresh data from Yahoo Finance.
2. Updates the Feature Store (MongoDB).
3. Retrains the Ensemble Model.
4. Commits the new model back to the repository.

### 2. 🗄️ MongoDB Feature Store

Instead of relying on static CSVs, processed features (`SMA_10`, `SMA_50`, `Volatility`) are stored in MongoDB. This ensures training and inference always use the exact same feature definitions.

### 3. 🧪 Robust CI/CD Pipeline

* **CI (Continuous Integration):** Every code push triggers `pytest` to ensure the API and Model logic aren't broken.
* **CD (Continuous Deployment):** If tests pass, Railway automatically builds and deploys the new API version.

---

## 🛠️ Technology Stack

| Category | Technologies |
| --- | --- |
| **Language** | Python 3.12 |
| **Machine Learning** | Linear Regression, Random Forest, XGBoost, Ensemble Learning (Voting Regressor), Scikit-Learn, Pandas, NumPy |
| **Backend API** | FastAPI, Uvicorn, Pydantic |
| **Frontend** | Streamlit|
| **Database** | MongoDB Atlas (Feature Store) |
| **MLOps Tools** | GitHub Actions, Weights & Biases (WandB), Docker |
| **Deployment** | Railway (API), Streamlit Cloud (UI) |

---

## 📦 Installation & Setup

### Prerequisites

* Python 3.10+
* MongoDB Atlas Account
* WandB Account

### Step 1: Clone Repository

```bash
git clone https://github.com/Hanseeka-Dhingana/stock_prediction_mlops.git
cd stock_prediction_mlops

```

### Step 2: Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt

```

### Step 4: Configure Environment (`.env`)

Create a `.env` file in the root directory:

```ini
MONGO_URI="mongodb+srv://<username>:<password>@cluster.mongodb.net/..."
WANDB_API_KEY="wd-..."

```

### Step 5: Run Locally

**1. Run the Pipeline (Ingest -> Train):**

```bash
python src/pipeline/train_pipeline.py

```

**2. Start the API:**

```bash
uvicorn api.main:app --reload

```

**3. Start the Dashboard:**

```bash
streamlit run frontend/app.py

```

---

## 📁 Project Structure

```text
stock_prediction_mlops/
├── .github/workflows/       # The Brains (Automation)
│   ├── ci.yml               # Runs Tests on every push
│   └── retrain.yml          # Weekly Self-Learning Robot
├── api/                     # Backend
│   ├── main.py              # FastAPI endpoints
│   └── __init__.py
├── data/                    # csv files of dataset
├── frontend/                # Frontend
│   └── app.py               # Streamlit Dashboard
├── models/               # Local storage for Models
├── notebook/                # perform EDA and train model
|   ├── EDA_stock_prediction.ipynb
|   └── model_training.ipynb
├── src/                     # Core Logic
|   ├── __init__.py 
│   ├── components/
|   |   ├── __init__.py 
│   │   ├── data_ingestion.py      # Yahoo Finance -> CSV
│   │   ├── data_transformation.py # CSV -> MongoDB Features
│   │   └── model_trainer.py       # MongoDB -> Models
│   ├── pipeline/
|   |   ├── __init__.py 
│   │   └── train_pipeline.py      # Orchestrator
|   ├── exception.py
|   ├── logger.py
|   ├── tunning.py           # train models on different hyperparameters
|   └── utils.py
├── tests/                   # Unit Tests
|   ├── __init__.py 
│   └── test_api.py
├── Dockerfile
├── gitignore
├── export_results.py
├── setup.py
├── sweep_results.csv
├── requirements.txt
└── README.md

```

---

## 🔄 MLOps Pipelines (CI/CD/CT)

### 1. Continuous Integration (CI)

* **Trigger:** Push to `main`.
* **Job:** Runs unit tests (`pytest`). Checks if API endpoints return 200 OK.
* **File:** `.github/workflows/ci.yml`

### 2. Continuous Training (CT)

* **Trigger:** Schedule (Every Sunday 00:00) OR Manual Dispatch.
* **Job:**  Fetches new data.
* Retrains model.
* Logs performance to **WandB**.
* **Commits** the new `model.pkl` to the repo.


* **File:** `.github/workflows/retrain.yml`

### 3. Continuous Deployment (CD)

* **Trigger:** When `model.pkl` is updated in the repo.
* **Job:** Railway detects the change, rebuilds the Docker container, and updates the live API.

---

## 📡 API Documentation

**Base URL:** `https://your-railway-app-url.app`

### 1. Health Check

`GET /`
Returns status of the API.

```json
{ "status": "active", "model": "v1.0" }

```

### 2. Predict Price

`POST /predict`
Predicts the next day's closing price.

**Request:**

```json
{
  "Close": 150.5,
  "SMA_10": 148.2,
  "SMA_50": 145.0,
  "Volatility": 2.1
}

```

**Response:**

```json
{
  "status": "success",
  "predicted_price": 152.34
}

```

---

## 📊 Performance & Results

We optimized our model using **Weights & Biases Sweeps**, achieving a **21.2% reduction in error**.

* **Baseline Model (Untuned):** MAE ~27.72
* **Final Production Model (Ensemble):** MAE **~21.83** *(Lower is better)*

* **Key Improvement:** Reduced prediction error by **$5.89 per share** compared to the baseline.

*Check the [WandB Dashboard](https://api.wandb.ai/links/hanseeka-dhingana-sukkur-iba-university/vgs0jzg2) for the full sweep comparison.*


---

### 👤 Author

**Hanseeka Dhingana**