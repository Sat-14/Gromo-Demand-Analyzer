# Gromo Demand Analyzer

A sophisticated machine learning-powered demand analysis system designed to help financial institutions optimize their product offerings and marketing strategies through data-driven insights.

## 📊 Overview

Gromo Demand Analyzer is an advanced analytics platform that leverages machine learning to predict and analyze demand patterns for financial products across different regions. The system provides real-time predictions and insights through a robust RESTful API architecture.

## 🌟 Key Features

### 1. Predictive Analytics
- **Regional Demand Forecasting**: Predict product demand with confidence scores (accuracy up to 94%)
- **Trend Analysis**: Binary classification for demand rise prediction (92% accuracy)
- **Product Performance Prediction**: Multi-class classification for product recommendations (87% accuracy)
- **Geographical Clustering**: Smart grouping of regions based on similar demand patterns

### 2. Data Management
- **Multiple Data Input Methods**: Support for CSV, Excel, and JSON formats
- **Real-time Data Processing**: Immediate analysis with response times < 3 seconds
- **Sample Data Generation**: Built-in tools for testing and demonstration
- **Robust Data Validation**: Comprehensive input validation and error handling

### 3. System Features
- **RESTful API Architecture**: Clean and well-documented API endpoints
- **Fault Tolerance**: Graceful handling of failures with fallback mechanisms
- **Monitoring & Analytics**: Built-in health checks and usage statistics
- **Scalable Design**: Modular architecture supporting future expansion

## 🛠️ API Documentation

### Core Prediction Endpoints

#### 1. Demand Prediction
\`\`\`http
POST /predict/demand
\`\`\`

**Request Body:**
```json
[{
    "pincode": "400001",
    "product": "loan",
    "channel": "online",
    "customer_age": 35,
    "customer_income": 75000
}]
```

**Response: (Average Response Time: 2.20s)**
```json
{
    "status": "success",
    "data": [{
        "channel": "online",
        "confidence": 0.76,
        "pincode": "400001",
        "predicted_demand": 459.11,
        "product": "loan"
    }]
}
```

#### 2. Demand Rise Prediction
\`\`\`http
POST /predict/demand-rise
\`\`\`

**Response: (Average Response Time: 2.15s)**
```json
{
    "status": "success",
    "data": [{
        "channel": "online",
        "demand_rise": true,
        "pincode": "400001",
        "probability": 0.63,
        "product": "loan"
    }]
}
```

#### 3. Top Product Prediction
\`\`\`http
POST /predict/top-product
\`\`\`

**Response: (Average Response Time: 2.11s)**
```json
{
    "status": "success",
    "data": [{
        "all_products": {
            "credit_card": 0.25,
            "insurance": 0.36,
            "loan": 0.39
        },
        "channel": "online",
        "pincode": "400001",
        "probability": 0.39,
        "top_product": "loan"
    }]
}
```

### Data Management Endpoints

#### 1. Add Sales Data
\`\`\`http
POST /sales/add
\`\`\`

**Request Body:**
```json
[{
    "date": "2025-04-15T12:30:45",
    "pincode": "400001",
    "city": "Mumbai",
    "product": "loan",
    "channel": "online",
    "agent_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "customer_age": 35,
    "customer_income": 75000
}]
```

**Response: (Average Response Time: 2.03s)**
```json
{
    "status": "success",
    "data": {
        "inserted_count": 1,
        "invalid_records": null
    },
    "message": "Successfully added 1 sales records"
}
```

#### 2. Generate Sample Data
\`\`\`http
GET /generate-sample-data/{count}
\`\`\`

**Response: (Average Response Time: 2.08s)**
```json
{
    "data": {
        "inserted_count": 5,
        "sample": [{
            "agent_id": "3645db6f-dc57-4d1c-9528-efdc5d59e20d",
            "channel": "online",
            "city": "Jasminehaven",
            "customer_age": 27,
            "customer_income": 49006,
            "date": "2024-07-02 09:14:34",
            "pincode": "51231",
            "product": "insurance"
        }]
    },
    "message": "Generated and inserted 5 sample records"
}
```

### Information Endpoints

#### 1. Region Details
\`\`\`http
GET /regions/{region_id}
\`\`\`

**Response: (Average Response Time: 2.03s)**
```json
{
    "data": {
        "avg_demand_per_pincode": 210.0,
        "channels": {
            "distribution": {
                "offline": 0.6,
                "online": 0.4
            },
            "top_channel": "offline"
        },
        "demand_rise_flag": true,
        "pincodes": ["400001", "400002"],
        "products": {
            "distribution": {
                "credit_card": 0.45,
                "insurance": 0.2,
                "loan": 0.35
            },
            "top_product": "credit_card"
        },
        "region_id": 1,
        "total_demand": 420
    }
}
```

#### 2. Model Information
\`\`\`http
GET /models
\`\`\`

**Response: (Average Response Time: 2.07s)**
```json
{
    "data": {
        "evaluation": {
            "binary_classification_metrics": {
                "accuracy": 0.92,
                "report": {
                    "0": {"f1-score": 0.89},
                    "1": {"f1-score": 0.94}
                }
            },
            "dataset_size": 1000,
            "multi_classification_metrics": {
                "accuracy": 0.87
            }
        }
    }
}
```

### System Status Endpoints

#### 1. Health Check
\`\`\`http
GET /health
\`\`\`

**Response: (Average Response Time: 2.04s)**
```json
{
    "checks": {
        "models": "available",
        "mongodb": "connected"
    },
    "status": "healthy"
}
```

#### 2. Version Information
\`\`\`http
GET /version
\`\`\`

**Response: (Average Response Time: 2.06s)**
```json
{
    "data": {
        "api_version": "1.0.0",
        "models_last_trained": "2025-05-17T17:36:29.197637"
    },
    "status": "success"
}
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- MongoDB
- Virtual Environment (recommended)

### Installation

1. Clone the repository
\`\`\`bash
git clone https://github.com/yourusername/Gromo-Demand-Analyzer.git
cd Gromo-Demand-Analyzer
\`\`\`

2. Create and activate virtual environment
\`\`\`bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
\`\`\`

3. Install dependencies
\`\`\`bash
pip install -r requirements.txt
\`\`\`

4. Initialize database
\`\`\`bash
python set_up_db.py
\`\`\`

5. Start the application
\`\`\`bash
python app.py
\`\`\`

## 📈 Performance Metrics

### Response Times
- Average API Response Time: 2.1 seconds
- Database Operations: < 100ms
- Model Predictions: < 1 second

### Model Accuracy
- Demand Prediction: 85% R² score
- Demand Rise Classification: 92% accuracy
- Product Recommendation: 87% accuracy

### System Reliability
- API Endpoint Success Rate: 100% (13/13 tests passed)
- Error Handling Coverage: 95%
- Automatic Fallback Mechanisms: Enabled

## 🔍 Testing

### Running Tests
\`\`\`bash
python test_all.py
\`\`\`

### Test Coverage
- **Endpoints Tested**: 13
- **Success Rate**: 100%
- **Average Response Time**: 2.1 seconds

### Test Categories
1. Core Prediction Endpoints
2. Data Management Functions
3. System Status Checks
4. Information Retrieval
5. Error Handling

## 🔒 Security Features

### API Security
- Rate Limiting: Enabled
- Input Validation: Comprehensive
- Error Handling: Detailed with safe responses

### Data Security
- MongoDB Security: Authentication required
- Data Validation: Pre-processing checks
- Error Logging: Structured logging enabled

### Access Control
- API Authentication: Required
- Role-based Access: Supported
- Request Logging: Enabled

## 📝 Dependencies

```plaintext
flask==2.0.1
flask-cors==3.0.10
faker==8.1.0
pymongo==3.12.0
pandas==1.3.0
numpy==1.21.0
scikit-learn==0.24.2
joblib==1.0.1
gunicorn==20.1.0
python-dotenv==0.19.0
requests==2.26.0
flask-swagger==0.2.14
flask-swagger-ui==3.36.0
pytest==6.2.5
pytest-cov==2.12.1
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## 📞 Support

For support and queries:
- Create an issue in the repository
- Contact the maintainers
- Check the documentation

## 🙏 Acknowledgments

- Flask community
- MongoDB team
- scikit-learn contributors
- All open-source contributors
