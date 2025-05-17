# 🚀 Demand Prediction API

<div align="center">
  
  ![Demand Prediction Banner](https://user-images.githubusercontent.com/74038190/221352995-5ac18bdf-1a9e-4a6c-b455-f75a5a73c5ea.gif)
  
  <h3>A sophisticated Flask-based REST API for predicting product demand and sales trends using machine learning models</h3>

  [![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
  [![Flask Version](https://img.shields.io/badge/flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
  [![MongoDB](https://img.shields.io/badge/MongoDB-4.4+-darkgreen.svg)](https://www.mongodb.com/)
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  
</div>

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [System Architecture](#-system-architecture)
- [Installation](#-installation)
- [API Endpoints](#-api-endpoints)
- [Detailed Endpoint Guide](#-detailed-endpoint-guide)
- [Using the Client Library](#-using-the-client-library)
- [Data Format](#-data-format)
- [ML Pipeline](#-ml-pipeline)
- [Project Structure](#-project-structure)
- [Configuration](#-configuration)
- [Testing](#-testing)
- [Contributors](#-contributors)
- [License](#-license)

## 🔍 Overview

This project delivers a comprehensive API for financial product demand analysis and prediction, empowering businesses to make data-driven decisions about their product offerings across different geographical regions. Through advanced machine learning models, the system analyzes historical sales data to forecast demand trends, identify demand growth opportunities, and recommend optimal product offerings for specific markets.

The API is built on a modern stack utilizing Flask for the backend, MongoDB for data storage, and scikit-learn for machine learning capabilities. It offers a robust solution for financial institutions looking to optimize their product distribution strategies based on predictive analytics.

## ✨ Features

- **🧠 Intelligent Demand Prediction**: Forecast product demand across different regions with high accuracy
- **📈 Trend Analysis**: Identify regions with rising demand patterns
- **🏆 Product Recommendations**: Determine top-performing products for specific geographical areas
- **🌍 Geographical Clustering**: Group similar regions for targeted marketing strategies
- **📊 Data Visualization**: Generate insights through data visualization capabilities
- **📁 Flexible Data Input**: Support for multiple data formats (JSON, CSV, Excel)
- **📱 RESTful API Design**: Modern, stateless API following REST principles
- **📝 Interactive Documentation**: Built-in Swagger UI for easy API exploration
- **🔄 Real-time Processing**: Process and analyze data in real-time
- **🔍 Comprehensive Monitoring**: Health checks and usage statistics
- **🔌 Python Client Library**: Easily integrate with your applications using our Python client
- **💻 Command-line Interface**: Access all API functionality from the command line

## 🏗 System Architecture

```
┌─────────────┐      ┌─────────────┐      ┌─────────────────────┐
│ Client Apps │──────▶ Flask API   │──────▶ Prediction Services │
└─────────────┘      └──────┬──────┘      └──────────┬──────────┘
       ▲                    │                         │
       │              ┌──────▼──────┐           ┌──────▼──────┐
       └──────────────│   MongoDB   │◀──────────▶│   ML Models │
                      └─────────────┘           └─────────────┘
```

## 🚀 Installation

### Prerequisites

- Python 3.8+
- MongoDB 4.4+
- pip or conda package manager

### Setup Steps

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/demand-prediction-api.git
cd demand-prediction-api
```

2. **Create a virtual environment (recommended)**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install the required packages**

```bash
pip install -r requirements.txt
```

4. **Start MongoDB (if not already running)**

```bash
mongod --dbpath=/path/to/data/directory
```

5. **Initialize the database with sample data**

```bash
python setup_db.py
```

6. **Start the API server**

```bash
python app.py
```

The API will be available at http://localhost:5000

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information and documentation |
| `/regions` | GET | Get all region summaries |
| `/regions/<region_id>` | GET | Get a specific region summary |
| `/models` | GET | Get model details and evaluation metrics |
| `/predict/demand` | POST | Predict region demand |
| `/predict/demand-rise` | POST | Predict if demand will rise |
| `/predict/top-product` | POST | Predict top product for a region |
| `/predict/all` | POST | Run all three prediction models |
| `/upload/data` | POST | Upload data file (CSV, Excel, JSON) |
| `/sales/add` | POST | Add sales data records directly |
| `/generate-sample-data/<count>` | GET | Generate and add sample sales data |
| `/health` | GET | API health check |
| `/version` | GET | API version information |
| `/stats` | GET | API usage statistics |

## 📘 Detailed Endpoint Guide

### 🏠 Root Endpoint
**GET /**

Returns information about the API and available endpoints.

**Response:**
```json
{
  "status": "success",
  "message": "Demand Prediction API is running",
  "endpoints": {
    "GET /": "API information",
    "GET /regions": "Get all region summaries",
    ...
  }
}
```

### 🌍 Regions Endpoint
**GET /regions**

Returns summaries of all regions in the database.

**Response:**
```json
{
  "status": "success",
  "data": [
    {
      "region_id": 0,
      "pincodes": ["110001", "110002", "110003"],
      "total_demand": 500,
      "avg_demand_per_pincode": 166.67,
      "demand_rise_flag": true,
      "products": {
        "top_product": "loan",
        "distribution": {"loan": 0.55, "credit_card": 0.30, "insurance": 0.15}
      },
      "channels": {
        "top_channel": "online",
        "distribution": {"online": 0.65, "offline": 0.35}
      }
    },
    ...
  ]
}
```

### 🌆 Specific Region Endpoint
**GET /regions/{region_id}**

Returns details for a specific region.

**Response:**
```json
{
  "status": "success",
  "data": {
    "region_id": 1,
    "pincodes": ["400001", "400002"],
    "total_demand": 420,
    "avg_demand_per_pincode": 210.0,
    "demand_rise_flag": true,
    "products": {
      "top_product": "credit_card",
      "distribution": {"loan": 0.35, "credit_card": 0.45, "insurance": 0.20}
    },
    "channels": {
      "top_channel": "offline",
      "distribution": {"online": 0.40, "offline": 0.60}
    }
  }
}
```

### 🧠 Models Endpoint
**GET /models**

Returns details about the trained machine learning models.

**Response:**
```json
{
  "status": "success",
  "data": {
    "model_details": [
      {
        "model_type": "regression",
        "target": "region_total",
        "hyperparameters": {
          "model__n_estimators": 100,
          "model__learning_rate": 0.1,
          "model__max_depth": 3
        },
        "metrics": {
          "mse": 150.25,
          "rmse": 12.26,
          "mae": 9.85,
          "r2": 0.85
        },
        "training_date": "2025-05-17T00:12:34.726"
      },
      ...
    ],
    "evaluation": {...}
  }
}
```

### 📊 Demand Prediction Endpoint
**POST /predict/demand**

Predicts demand for products in specific regions.

**Request Body:**
```json
[
  {
    "pincode": "400001",
    "product": "loan",
    "channel": "online",
    "customer_age": 35,
    "customer_income": 75000
  }
]
```

**Response:**
```json
{
  "status": "success",
  "data": [
    {
      "pincode": "400001",
      "product": "loan",
      "channel": "online",
      "predicted_demand": 523.75,
      "confidence": 0.85
    }
  ]
}
```

### 📈 Demand Rise Prediction Endpoint
**POST /predict/demand-rise**

Predicts whether demand will rise for products in specific regions.

**Request Body:**
```json
[
  {
    "pincode": "400001",
    "product": "loan",
    "channel": "online",
    "customer_age": 35,
    "customer_income": 75000
  }
]
```

**Response:**
```json
{
  "status": "success",
  "data": [
    {
      "pincode": "400001",
      "product": "loan",
      "channel": "online",
      "demand_rise": true,
      "probability": 0.78
    }
  ]
}
```

### 🏆 Top Product Prediction Endpoint
**POST /predict/top-product**

Predicts the top-performing product for specific regions.

**Request Body:**
```json
[
  {
    "pincode": "400001",
    "channel": "online",
    "customer_age": 35,
    "customer_income": 75000
  }
]
```

**Response:**
```json
{
  "status": "success",
  "data": [
    {
      "pincode": "400001",
      "channel": "online",
      "top_product": "credit_card",
      "probability": 0.65,
      "all_products": {
        "loan": 0.25,
        "credit_card": 0.65,
        "insurance": 0.10
      }
    }
  ]
}
```

### 🔄 All Predictions Endpoint
**POST /predict/all**

Runs all three prediction models simultaneously.

**Request Body:**
```json
[
  {
    "pincode": "400001",
    "product": "loan",
    "channel": "online",
    "customer_age": 35,
    "customer_income": 75000
  }
]
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "demand": [...],
    "demand_rise": [...],
    "top_product": [...]
  }
}
```

### 📤 Upload Data Endpoint
**POST /upload/data**

Uploads data files for analysis.

**Request:**
```
FormData with 'file' field containing CSV, Excel, or JSON file
```

**Response:**
```json
{
  "status": "success",
  "message": "Data uploaded successfully",
  "data": {
    "rows": 100,
    "columns": ["date", "pincode", "city", "product", "channel", "agent_id", "customer_age", "customer_income"],
    "sample": [...]
  }
}
```

### 📝 Add Sales Data Endpoint
**POST /sales/add**

Adds sales data records directly to the database.

**Request Body:**
```json
[
  {
    "date": "2025-04-15T12:30:45",
    "pincode": "400001",
    "city": "Mumbai",
    "product": "loan",
    "channel": "online",
    "agent_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "customer_age": 35,
    "customer_income": 75000
  }
]
```

**Response:**
```json
{
  "status": "success",
  "message": "Successfully added 1 sales records",
  "data": {
    "inserted_count": 1,
    "invalid_records": null
  }
}
```

### 🧪 Generate Sample Data Endpoint
**GET /generate-sample-data/{count}**

Generates and adds sample sales data to the database.

**Response:**
```json
{
  "status": "success",
  "message": "Generated and inserted 100 sample records",
  "data": {
    "inserted_count": 100,
    "sample": {
      "date": "2025-02-15T09:45:30",
      "pincode": "110045",
      "city": "Delhi",
      "product": "loan",
      "channel": "online",
      "agent_id": "AG4875",
      "customer_age": 29,
      "customer_income": 65000,
      "inserted_at": "2025-05-17T00:12:34.726"
    }
  }
}
```

### ❤️ Health Check Endpoint
**GET /health**

Checks the health status of the API and its dependencies.

**Response:**
```json
{
  "status": "healthy",
  "checks": {
    "mongodb": "connected",
    "models": "available"
  }
}
```

### 🔢 Version Endpoint
**GET /version**

Returns the API version and model training information.

**Response:**
```json
{
  "status": "success",
  "data": {
    "api_version": "1.0.0",
    "models_last_trained": "2025-05-16T14:30:45.123"
  }
}
```

### 📊 Stats Endpoint
**GET /stats**

Returns usage statistics for the API.

**Response:**
```json
{
  "status": "success",
  "data": {
    "regions_count": 10,
    "models_count": 3,
    "uploads_count": 5,
    "sales_count": 1000
  }
}
```

## 🔌 Using the Client Library

The project includes a flexible Python client library (`client.py`) that provides both programmatic and command-line interfaces to the API.

### Command-Line Interface

The client library provides a convenient command-line interface for all API functionality:

```bash
# Check API status
python client.py status

# Get information about regions
python client.py regions
python client.py region --id 1

# Get model details
python client.py models

# Make predictions
python client.py predict-demand --file data.csv
python client.py predict-rise --file data.csv
python client.py predict-product --file data.csv
python client.py predict-all --file data.csv

# Work with data
python client.py upload --file sales_data.csv
python client.py add-sales --file new_sales.csv
python client.py generate-samples --count 500

# System information
python client.py health
python client.py version
python client.py stats
```

### Programmatic Usage

You can also use the client library in your Python code for seamless integration:

```python
from client import DemandPredictionClient

# Initialize client
client = DemandPredictionClient(base_url="http://localhost:5000")

# Check if API is available
health = client.check_health()
print(f"API health status: {health['status']}")

# Get region information
regions = client.get_all_regions()
region = client.get_region_by_id(region_id=1)

# The client supports multiple input formats for predictions:

# 1. Using a data file (CSV, Excel, or JSON)
predictions = client.predict_demand("customer_data.csv")

# 2. Using a pandas DataFrame
import pandas as pd
df = pd.DataFrame([
    {"pincode": "400001", "product": "loan", "channel": "online", "customer_age": 35},
    {"pincode": "400002", "product": "credit_card", "channel": "offline", "customer_age": 42}
])
predictions = client.predict_demand(df)

# 3. Using a list of dictionaries
data = [
    {"pincode": "400001", "product": "loan", "channel": "online", "customer_age": 35},
    {"pincode": "400002", "product": "credit_card", "channel": "offline", "customer_age": 42}
]
predictions = client.predict_demand(data)

# Run all prediction models at once
all_results = client.predict_all(df)
demand_predictions = all_results['demand']
rise_predictions = all_results['demand_rise']
product_predictions = all_results['top_product']

# Upload data and add sales records
client.upload_data("sales_data.csv")
client.add_sales_data("new_sales.csv")

# Generate sample data
client.generate_sample_data(count=500)

# Get system information
version = client.get_version()
stats = client.get_stats()
```

## 📋 Data Format

### Sales Data Schema

Our API processes financial product sales data with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| date | datetime | Date and time of the sale |
| pincode | string | Postal code where the sale occurred |
| city | string | City where the sale occurred |
| product | string | Product type (loan, credit_card, insurance) |
| channel | string | Sales channel (online, offline) |
| agent_id | string | Unique identifier for the sales agent |
| customer_age | integer | Age of the customer |
| customer_income | integer | Annual income of the customer |

### Sample Sales Record

```json
{
  "date": "2025-04-15T12:30:45",
  "pincode": "400001",
  "city": "Mumbai",
  "product": "loan",
  "channel": "online",
  "agent_id": "AG1234",
  "customer_age": 35,
  "customer_income": 75000
}
```

## 🔄 ML Pipeline

Our demand prediction system uses a sophisticated machine learning pipeline to transform raw sales data into actionable predictions:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Raw Data   │────▶│ Data Loading│────▶│Preprocessing│────▶│ Feature     │────▶│  Model      │
│ Collection  │     │             │     │& Validation │     │ Engineering │     │ Training    │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘     └─────┬───────┘
                                                                                      │
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────▼───────┐
│  API        │◀────│  Prediction │◀────│ Model       │◀────│  Model      │◀────│  Model      │
│  Endpoint   │     │  Service    │     │ Selection   │     │ Evaluation  │     │ Tuning      │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

### Pipeline Stages:

1. **Data Collection**: Sales data is gathered from multiple sources and stored in MongoDB
2. **Data Loading**: Raw data is loaded into the system, with automatic handling of various formats
3. **Preprocessing & Validation**: Data is cleaned, validated, and transformed into a suitable format
4. **Feature Engineering**: 
   - Geographical coordinates are assigned to pincodes
   - Regions are created through clustering algorithms
   - Time-based features are extracted from dates
   - Customer segments are created based on age and income
5. **Model Training**: Three types of models are trained:
   - Regression model for demand prediction
   - Binary classification for demand rise prediction
   - Multi-class classification for top product prediction
6. **Model Tuning**: Hyperparameters are optimized using GridSearchCV
7. **Model Evaluation**: Models are evaluated using appropriate metrics:
   - Regression: MSE, RMSE, MAE, R²
   - Classification: Accuracy, Precision, Recall, F1-score
8. **Model Selection**: The best performing models are selected for deployment
9. **Prediction Service**: Selected models are used to generate predictions
10. **API Endpoint**: Predictions are exposed through RESTful API endpoints

## 📁 Project Structure

```
demand-prediction-api/
├── app.py                  # Main Flask application
├── model.py                # Machine learning models and prediction logic
├── Dp.py                   # Data processing utilities
├── client.py               # Python client library with CLI
├── config.py               # Application configuration
├── setup_db.py             # Database initialization script
├── requirements.txt        # Project dependencies
├── tests/                  # Test scripts
│   ├── test_all_endpoints.py  # Endpoint test script
│   └── test_client.py      # Client library test script
└── docs/                   # Documentation
```

## ⚙️ Configuration

You can configure the API by modifying `config.py`:

```python
# API Configuration
API_HOST = '0.0.0.0'  # Listen on all interfaces
API_PORT = 5000       # Port to run the API on
DEBUG = False         # Set to True for development mode

# MongoDB Configuration
MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB = "gromo"

# Model Configuration
DEFAULT_CLUSTERS = 20  # Default number of clusters for pincode clustering
MODEL_PATH = "./models/"  # Path to save trained models
```

## 🧪 Testing

### Running Tests

```bash
python tests/test_all_endpoints.py
```

### Sample Test Script Output

```
======================================================
Testing: GET /
Description: Get API information and available endpoints
======================================================
Status Code: 200 (Expected: 200)
Response Time: 0.03 seconds
Response JSON: {
  "status": "success",
  "message": "Demand Prediction API is running",
  "endpoints": {
    "GET /": "API information",
    ...
  }
}
✅ TEST PASSED

...

============================================================
TEST SUMMARY
============================================================
root: ✅ PASSED
regions: ✅ PASSED
region_detail: ✅ PASSED
models: ✅ PASSED
predict_demand: ✅ PASSED
predict_rise: ✅ PASSED
predict_product: ✅ PASSED
predict_all: ✅ PASSED
add_sales: ✅ PASSED
generate_sample: ✅ PASSED
health: ✅ PASSED
version: ✅ PASSED
stats: ✅ PASSED

Overall: 13/13 tests passed (100.0%)
```

## 👥 Contributors

- [Your Name](https://github.com/yourusername)

## 📄 License

MIT License

---

<div align="center">
  
  <p>Built with ❤️ by Your Team</p>
  <p>Need help? <a href="mailto:your.email@example.com">Contact us</a></p>
  
</div>
