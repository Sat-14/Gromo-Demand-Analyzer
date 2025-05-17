# Gromo Demand Analyzer

A sophisticated machine learning-powered demand analysis system designed to help financial institutions optimize their product offerings and marketing strategies through data-driven insights.

## 🎯 Overview

Gromo Demand Analyzer is an advanced analytics platform that leverages machine learning to predict and analyze demand patterns for financial products across different regions. It helps financial institutions make data-driven decisions about product placement, marketing strategies, and resource allocation.

## 🌟 Key Features

### 1. Predictive Analytics
- **Regional Demand Forecasting**: Accurate predictions for product demand in specific regions
- **Trend Analysis**: Advanced algorithms to predict demand rise/fall patterns
- **Product Performance Prediction**: AI-powered recommendations for top-performing products
- **Geographical Clustering**: Smart grouping of regions based on similar demand patterns

### 2. Data Management
- **Multiple Data Input Methods**: Support for CSV, Excel, and JSON formats
- **Real-time Data Processing**: Immediate analysis of new data points
- **Sample Data Generation**: Built-in tools for testing and demonstration
- **Robust Data Validation**: Comprehensive input validation and error handling

### 3. System Features
- **RESTful API Architecture**: Clean and well-documented API endpoints
- **Fault Tolerance**: Graceful handling of failures with fallback mechanisms
- **Monitoring & Analytics**: Built-in health checks and usage statistics
- **Scalable Design**: Modular architecture supporting future expansion

## 💼 Use Cases

### 1. Financial Institutions
- Optimize product portfolio based on regional demand
- Identify emerging market opportunities
- Plan resource allocation efficiently
- Reduce risk through data-driven decisions

### 2. Marketing Teams
- Target marketing campaigns based on regional preferences
- Identify high-potential regions for specific products
- Optimize marketing budget allocation
- Track campaign effectiveness

### 3. Sales Teams
- Plan territory-wise sales strategies
- Set realistic sales targets based on demand predictions
- Identify cross-selling opportunities
- Optimize sales force deployment

### 4. Business Analysts
- Generate comprehensive market insights
- Track market trends and patterns
- Perform competitor analysis
- Create data-backed business strategies

## 🛠️ Technical Architecture

### Components
1. **API Layer** (`app.py`)
   - Flask-based RESTful API
   - CORS support
   - Rate limiting
   - Error handling

2. **ML Engine** (`model.py`)
   - Demand prediction models
   - Trend analysis
   - Product recommendation system
   - Geographic clustering

3. **Data Processing** (`Dp.py`)
   - Data validation
   - Preprocessing
   - Feature engineering
   - Data transformation

4. **Database Layer** (`set_up_db.py`)
   - MongoDB integration
   - Data persistence
   - Query optimization
   - Schema management

## 📊 API Endpoints

### Core Prediction Endpoints

#### 1. Demand Prediction
\`\`\`http
POST /predict/demand
\`\`\`
```json
// Request Body
[{
    "pincode": "400001",
    "product": "loan",
    "channel": "online",
    "customer_age": 35,
    "customer_income": 75000
}]
```
```json
// Response
{
    "status": "success",
    "data": [{
        "pincode": "400001",
        "product": "loan",
        "channel": "online",
        "predicted_demand": 856.45,
        "confidence": 0.89
    }]
}
```

#### 2. Demand Rise Prediction
\`\`\`http
POST /predict/demand-rise
\`\`\`
```json
// Response
{
    "status": "success",
    "data": [{
        "pincode": "400001",
        "product": "loan",
        "demand_rise": true,
        "probability": 0.85
    }]
}
```

#### 3. Top Product Prediction
\`\`\`http
POST /predict/top-product
\`\`\`
```json
// Response
{
    "status": "success",
    "data": [{
        "pincode": "400001",
        "top_product": "loan",
        "probability": 0.75,
        "all_products": {
            "loan": 0.75,
            "credit_card": 0.15,
            "insurance": 0.10
        }
    }]
}
```

### Data Management Endpoints

#### 1. Upload Data
\`\`\`http
POST /upload/data
\`\`\`
- Supports CSV, Excel, JSON formats
- Automatic data validation
- Batch processing capability

#### 2. Add Sales Data
\`\`\`http
POST /sales/add
\`\`\`
- Direct data entry
- Real-time processing
- Automatic validation

#### 3. Generate Sample Data
\`\`\`http
GET /generate-sample-data/{count}
\`\`\`
- Creates realistic test data
- Configurable data size
- Maintains data consistency

### Utility Endpoints

#### 1. Health Check
\`\`\`http
GET /health
\`\`\`
- System status monitoring
- Component health checks
- Performance metrics

#### 2. Statistics
\`\`\`http
GET /stats
\`\`\`
- Usage statistics
- System metrics
- Performance analytics

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

4. Configure the application
- Copy `config.py.example` to `config.py`
- Update configuration values

5. Initialize database
\`\`\`bash
python set_up_db.py
\`\`\`

6. Start the application
\`\`\`bash
python app.py
\`\`\`

## 📈 Advantages

1. **Data-Driven Decision Making**
   - Reduce guesswork in business decisions
   - Quantifiable results and predictions
   - Historical trend analysis

2. **Cost Optimization**
   - Better resource allocation
   - Reduced marketing waste
   - Optimized inventory management

3. **Risk Management**
   - Early trend detection
   - Market risk assessment
   - Demand fluctuation prediction

4. **Scalability**
   - Modular architecture
   - Easy integration
   - Extensible design

5. **User-Friendly**
   - Clean API design
   - Comprehensive documentation
   - Multiple data input methods

## 🔒 Security Features

1. **API Security**
   - Rate limiting
   - Input validation
   - Error handling

2. **Data Security**
   - Secure database connections
   - Data validation
   - Error logging

3. **Access Control**
   - API authentication
   - Role-based access
   - Request logging

## 📝 Testing

Run the comprehensive test suite:
\`\`\`bash
python -m pytest tests/
\`\`\`

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## 📞 Support

For support and queries, please create an issue in the repository or contact the maintainers.

## 🙏 Acknowledgments

- Flask community
- MongoDB team
- scikit-learn contributors
- All open-source contributors
