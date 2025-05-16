# Gromo-Demand-Analyzer
Demand Prediction API
A Flask-based REST API for predicting product demand and sales trends using machine learning models.

Overview
This project provides a powerful API for analyzing sales data and making predictions about:

Regional demand for various products
Whether demand will rise in specific regions
Top-performing products in different areas
The application uses machine learning models (regression, binary classification, and multi-class classification) to analyze patterns in sales data and provide actionable insights.

Features
Data Analysis: Upload and analyze sales data
Demand Prediction: Predict demand for different products across regions
Trend Analysis: Determine if demand is likely to rise
Product Recommendations: Identify top-performing products for specific regions
Geographical Clustering: Group similar geographic areas based on sales patterns
Interactive API Documentation: Built-in Swagger UI documentation
Installation
Prerequisites
Python 3.8+
MongoDB
pip or conda
Steps
Clone the repository:
bash
git clone https://github.com/yourusername/demand-prediction-api.git
cd demand-prediction-api
Install the required packages:
bash
pip install -r requirements.txt
Start MongoDB (if not already running):
bash
mongod --dbpath=/path/to/data/directory
Initialize the database with sample data:
bash
python setup_db.py
Start the API server:
bash
python app.py
API Endpoints
Endpoint	Method	Description
/	GET	API information and documentation
/regions	GET	Get all region summaries
/regions/<region_id>	GET	Get a specific region summary
/models	GET	Get model details and evaluation metrics
/predict/demand	POST	Predict region demand
/predict/demand-rise	POST	Predict if demand will rise
/predict/top-product	POST	Predict top product for a region
/predict/all	POST	Run all three prediction models
/upload/data	POST	Upload data file (CSV, Excel, JSON)
/sales/add	POST	Add sales data records directly
/generate-sample-data/<count>	GET	Generate and add sample sales data
/health	GET	API health check
/version	GET	API version information
/stats	GET	API usage statistics
Usage Examples
Predict Demand for a Product
bash
curl -X POST http://localhost:5000/predict/demand \
  -H "Content-Type: application/json" \
  -d '[{
    "pincode": "400001",
    "product": "loan",
    "channel": "online",
    "customer_age": 35,
    "customer_income": 75000
  }]'
Add Sales Data
bash
curl -X POST http://localhost:5000/sales/add \
  -H "Content-Type: application/json" \
  -d '[{
    "date": "2025-04-15T12:30:45",
    "pincode": "400001",
    "city": "Mumbai",
    "product": "loan",
    "channel": "online",
    "agent_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "customer_age": 35,
    "customer_income": 75000
  }]'
Generate Sample Data
bash
curl http://localhost:5000/generate-sample-data/100
Data Format
Sales Data
json
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
Prediction Input
json
{
  "pincode": "400001",
  "product": "loan",
  "channel": "online",
  "customer_age": 35,
  "customer_income": 75000
}
Project Structure
demand-prediction-api/
├── app.py                  # Main Flask application
├── model.py                # Machine learning models and prediction logic
├── Dp.py                   # Data processing utilities
├── config.py               # Application configuration
├── setup_db.py             # Database initialization script
├── requirements.txt        # Project dependencies
├── tests/                  # Test scripts
│   └── test_all_endpoints.py  # Endpoint test script
└── docs/                   # Documentation
Machine Learning Models
The API uses three types of models:

Regression Model: Predicts the actual demand value for a region
Binary Classification Model: Predicts whether demand will rise (1) or not (0)
Multi-class Classification Model: Predicts the top product for a region from available product categories
Configuration
You can configure the API by modifying config.py:

python
# API Configuration
API_HOST = '0.0.0.0'  # Listen on all interfaces
API_PORT = 5000       # Port to run the API on
DEBUG = False         # Set to True for development mode

# MongoDB Configuration
MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB = "gromo"
Testing
Run the test script to verify all endpoints are working:

bash
python tests/test_all_endpoints.py
Dependencies
Flask & Flask-CORS: Web framework and CORS support
pymongo: MongoDB client
pandas & numpy: Data manipulation
scikit-learn: Machine learning models
Faker: Generating sample data
See requirements.txt for a complete list of dependencies.

License
MIT License

Contributors
Satwik Rai
Acknowledgments
Thanks to the Flask and scikit-learn communities for the excellent documentation and resources.
