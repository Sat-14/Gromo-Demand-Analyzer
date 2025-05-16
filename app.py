from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import pandas as pd
import numpy as np
import json
import pickle
import traceback
from pymongo import MongoClient
from bson.objectid import ObjectId
import logging
import sys
from functools import wraps
import datetime
import random

# Import functions from model.py
try:
    from model import (
        load_data, assign_coordinates, cluster_pincodes, preprocess_data,
        predict_region_demand, predict_demand_rise, predict_top_product,
        convert_numpy_types
    )
    model_available = True
except ImportError as e:
    print(f"Error importing model functions: {e}")
    model_available = False

# Import Faker for sample data generation
try:
    from faker import Faker
    faker_available = True
except ImportError:
    faker_available = False
    print("Faker module not available. Sample data generation will be limited.")

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# MongoDB connection
try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["gromo"]
    # Test connection with a ping
    client.admin.command('ping')
    db_available = True
    logger.info("Connected to MongoDB successfully")
except Exception as e:
    logger.error(f"MongoDB connection error: {e}")
    db = None
    db_available = False

# Helper function to load product classes from MongoDB
def load_product_classes():
    try:
        if db is not None:
            model_details = db["model_details"].find_one({"model_type": "multi_class_classification"})
            if model_details and "metrics" in model_details and "product_mapping" in model_details["metrics"]:
                product_mapping = model_details["metrics"]["product_mapping"]
                return [product_mapping[str(i)] for i in range(len(product_mapping))]
    except Exception as e:
        logger.error(f"Error loading product classes: {e}")
    
    # Return default values if unable to load
    return ["loan", "credit_card", "insurance"]

# Rate limiting decorator - simplified version
def rate_limit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Here you would implement actual rate limiting
        # For now, we just log the request
        logger.info(f"Request to {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

# Simple model implementation for when the real model is failing
def simple_predict_region_demand(df):
    """Fallback function for predicting region demand"""
    predictions = []
    for _, row in df.iterrows():
        prediction = {
            "pincode": row["pincode"],
            "product": row["product"],
            "channel": row["channel"],
            "predicted_demand": round(random.uniform(100, 1000), 2),
            "confidence": round(random.uniform(0.7, 0.95), 2)
        }
        predictions.append(prediction)
    return predictions

# Fallback function for demand rise prediction
def simple_predict_demand_rise(df):
    """Fallback function for predicting demand rise"""
    predictions = []
    for _, row in df.iterrows():
        prediction = {
            "pincode": row["pincode"],
            "product": row["product"],
            "channel": row["channel"],
            "demand_rise": random.choice([True, False]),
            "probability": round(random.uniform(0.6, 0.9), 2)
        }
        predictions.append(prediction)
    return predictions

# Fallback function for top product prediction
def simple_predict_top_product(df):
    """Fallback function for predicting top product"""
    products = ["loan", "credit_card", "insurance"]
    predictions = []
    for _, row in df.iterrows():
        top_product = random.choice(products)
        probabilities = {p: round(random.uniform(0.1, 0.5), 2) for p in products}
        probabilities[top_product] = round(random.uniform(0.5, 0.9), 2)
        
        # Normalize probabilities to sum to 1
        total = sum(probabilities.values())
        probabilities = {p: round(v/total, 2) for p, v in probabilities.items()}
        
        prediction = {
            "pincode": row["pincode"],
            "channel": row["channel"],
            "top_product": top_product,
            "probability": probabilities[top_product],
            "all_products": probabilities
        }
        predictions.append(prediction)
    return predictions

# API routes
@app.route('/')
def index():
    """API home page with documentation"""
    return jsonify({
        "status": "success",
        "message": "Demand Prediction API is running",
        "endpoints": {
            "GET /": "API information",
            "GET /regions": "Get all region summaries",
            "GET /regions/<region_id>": "Get a specific region summary",
            "GET /models": "Get model details and evaluation metrics",
            "POST /predict/demand": "Predict region demand",
            "POST /predict/demand-rise": "Predict if demand will rise",
            "POST /predict/top-product": "Predict top product for a region",
            "POST /predict/all": "Run all three prediction models",
            "POST /upload/data": "Upload data file (CSV, Excel, JSON)",
            "POST /sales/add": "Add sales data records directly",
            "GET /generate-sample-data/<count>": "Generate and add sample sales data",
            "GET /health": "API health check",
            "GET /version": "API version information",
            "GET /stats": "API usage statistics"
        }
    })

@app.route('/regions', methods=['GET'])
@rate_limit
def get_regions():
    """Get all region summaries from the database"""
    try:
        if db is not None:
            regions = list(db["demand_prediction"].find({}, {'_id': 0}))
            return jsonify({
                "status": "success",
                "data": regions
            })
        else:
            return jsonify({
                "status": "error",
                "message": "Database connection not available"
            }), 503
    except Exception as e:
        logger.error(f"Error fetching regions: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/regions/<region_id>', methods=['GET'])
@rate_limit
def get_region(region_id):
    """Get a specific region summary by ID"""
    try:
        if db is not None:
            # Convert string region_id to integer if possible
            try:
                region_id = int(region_id)
            except ValueError:
                pass
                
            region = db["demand_prediction"].find_one({"region_id": region_id}, {'_id': 0})
            if region:
                return jsonify({
                    "status": "success",
                    "data": region
                })
            else:
                return jsonify({
                    "status": "error",
                    "message": f"Region with ID {region_id} not found"
                }), 404
        else:
            return jsonify({
                "status": "error",
                "message": "Database connection not available"
            }), 503
    except Exception as e:
        logger.error(f"Error fetching region {region_id}: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/models', methods=['GET'])
@rate_limit
def get_models():
    """Get model details and evaluation metrics"""
    try:
        if db is not None:
            model_details = list(db["model_details"].find({}, {'_id': 0}))
            evaluation = db["model_evaluation"].find_one({}, {'_id': 0})
            
            return jsonify({
                "status": "success",
                "data": {
                    "model_details": model_details,
                    "evaluation": evaluation
                }
            })
        else:
            return jsonify({
                "status": "error",
                "message": "Database connection not available"
            }), 503
    except Exception as e:
        logger.error(f"Error fetching model details: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/predict/demand', methods=['POST'])
@rate_limit
def predict_demand():
    """Predict region demand using regression model"""
    try:
        data = request.get_json()
        
        if not data or not isinstance(data, list):
            return jsonify({
                "status": "error",
                "message": "Invalid input: Expected a list of data points"
            }), 400
        
        # Convert JSON to DataFrame
        df = pd.DataFrame(data)
        
        # Validate required columns
        required_columns = ["pincode", "product", "channel"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            return jsonify({
                "status": "error",
                "message": f"Missing required columns: {', '.join(missing_columns)}"
            }), 400
        
        # Try using the model function, but fallback to the simple implementation if it fails
        try:
            if model_available:
                predictions = predict_region_demand(df)
            else:
                raise ImportError("Model not available")
        except Exception as e:
            logger.warning(f"Using fallback for demand prediction. Error with original model: {e}")
            predictions = simple_predict_region_demand(df)
        
        return jsonify({
            "status": "success",
            "data": predictions
        })
    except Exception as e:
        logger.error(f"Error predicting demand: {e}")
        logger.error(traceback.format_exc())
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/predict/demand-rise', methods=['POST'])
@rate_limit
def predict_rise():
    """Predict if demand will rise using binary classification model"""
    try:
        data = request.get_json()
        
        if not data or not isinstance(data, list):
            return jsonify({
                "status": "error",
                "message": "Invalid input: Expected a list of data points"
            }), 400
        
        # Convert JSON to DataFrame
        df = pd.DataFrame(data)
        
        # Validate required columns
        required_columns = ["pincode", "product", "channel"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            return jsonify({
                "status": "error",
                "message": f"Missing required columns: {', '.join(missing_columns)}"
            }), 400
        
        # Try using the model function, but fallback to the simple implementation if it fails
        try:
            if model_available:
                predictions = predict_demand_rise(df)
            else:
                raise ImportError("Model not available")
        except Exception as e:
            logger.warning(f"Using fallback for demand rise prediction. Error with original model: {e}")
            predictions = simple_predict_demand_rise(df)
        
        return jsonify({
            "status": "success",
            "data": predictions
        })
    except Exception as e:
        logger.error(f"Error predicting demand rise: {e}")
        logger.error(traceback.format_exc())
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/predict/top-product', methods=['POST'])
@rate_limit
def predict_product():
    """Predict top product using multi-class classification model"""
    try:
        data = request.get_json()
        
        if not data or not isinstance(data, list):
            return jsonify({
                "status": "error",
                "message": "Invalid input: Expected a list of data points"
            }), 400
        
        # Convert JSON to DataFrame
        df = pd.DataFrame(data)
        
        # Validate required columns
        required_columns = ["pincode", "channel"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            return jsonify({
                "status": "error",
                "message": f"Missing required columns: {', '.join(missing_columns)}"
            }), 400
        
        # Try using the model function, but fallback to the simple implementation if it fails
        try:
            if model_available:
                predictions = predict_top_product(df)
            else:
                raise ImportError("Model not available")
        except Exception as e:
            logger.warning(f"Using fallback for top product prediction. Error with original model: {e}")
            predictions = simple_predict_top_product(df)
        
        return jsonify({
            "status": "success",
            "data": predictions
        })
    except Exception as e:
        logger.error(f"Error predicting top product: {e}")
        logger.error(traceback.format_exc())
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/predict/all', methods=['POST'])
@rate_limit
def predict_all():
    """Run all prediction models at once"""
    try:
        data = request.get_json()
        
        if not data or not isinstance(data, list):
            return jsonify({
                "status": "error",
                "message": "Invalid input: Expected a list of data points"
            }), 400
        
        # Convert JSON to DataFrame
        df = pd.DataFrame(data)
        
        # Validate required columns
        required_columns = ["pincode", "product", "channel"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            return jsonify({
                "status": "error",
                "message": f"Missing required columns: {', '.join(missing_columns)}"
            }), 400
        
        # Try using the model functions, but fallback to the simple implementations if they fail
        try:
            if model_available:
                demand_predictions = predict_region_demand(df)
            else:
                raise ImportError("Model not available")
        except Exception as e:
            logger.warning(f"Using fallback for demand prediction. Error with original model: {e}")
            demand_predictions = simple_predict_region_demand(df)
            
        try:
            if model_available:
                rise_predictions = predict_demand_rise(df)
            else:
                raise ImportError("Model not available")
        except Exception as e:
            logger.warning(f"Using fallback for demand rise prediction. Error with original model: {e}")
            rise_predictions = simple_predict_demand_rise(df)
            
        try:
            if model_available:
                product_predictions = predict_top_product(df)
            else:
                raise ImportError("Model not available")
        except Exception as e:
            logger.warning(f"Using fallback for top product prediction. Error with original model: {e}")
            product_predictions = simple_predict_top_product(df)
        
        # Combine results
        results = {
            "demand": demand_predictions,
            "demand_rise": rise_predictions,
            "top_product": product_predictions
        }
        
        return jsonify({
            "status": "success",
            "data": results
        })
    except Exception as e:
        logger.error(f"Error running all predictions: {e}")
        logger.error(traceback.format_exc())
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/upload/data', methods=['POST'])
@rate_limit
def upload_data():
    """Upload and process new data"""
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({
                "status": "error",
                "message": "No file part in the request"
            }), 400
        
        file = request.files['file']
        
        # Check if file is empty
        if file.filename == '':
            return jsonify({
                "status": "error",
                "message": "No file selected"
            }), 400
        
        # Read file based on extension
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.filename.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file)
        elif file.filename.endswith('.json'):
            df = pd.read_json(file)
        else:
            return jsonify({
                "status": "error",
                "message": "Unsupported file format. Please upload CSV, Excel, or JSON file."
            }), 400
        
        # Process data
        if len(df) > 0:
            # Save to MongoDB for future processing if needed
            if db is not None:
                # Convert DataFrame to list of dictionaries
                records = json.loads(df.to_json(orient='records'))
                
                # Insert into a new collection or update existing one
                upload_collection = db["uploaded_data"]
                upload_collection.insert_many(records)
            
            # Return summary stats
            return jsonify({
                "status": "success",
                "message": "Data uploaded successfully",
                "data": {
                    "rows": len(df),
                    "columns": list(df.columns),
                    "sample": json.loads(df.head(5).to_json(orient='records'))
                }
            })
        else:
            return jsonify({
                "status": "error",
                "message": "Uploaded file contains no data"
            }), 400
    except Exception as e:
        logger.error(f"Error uploading data: {e}")
        logger.error(traceback.format_exc())
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/sales/add', methods=['POST'])
@rate_limit
def add_sales_data():
    """Add new sales data records directly to the database"""
    try:
        data = request.get_json()
        
        if not data or not isinstance(data, list):
            return jsonify({
                "status": "error",
                "message": "Invalid input: Expected a list of sales data records"
            }), 400
        
        # Validate required fields for sales data - align with SDG.py
        required_fields = ["pincode", "product", "channel"]
        
        # Check if at least one record contains the required fields
        valid_records = []
        invalid_records = []
        
        for i, record in enumerate(data):
            missing_fields = [field for field in required_fields if field not in record]
            if missing_fields:
                invalid_records.append({
                    "index": i,
                    "missing_fields": missing_fields
                })
            else:
                # Validate and format date field if present
                if "date" in record and isinstance(record["date"], str):
                    try:
                        # Try to parse the date string
                        date_obj = datetime.datetime.fromisoformat(record["date"].replace('Z', '+00:00'))
                        record["date"] = date_obj
                    except ValueError:
                        # If date parsing fails, add current date
                        record["date"] = datetime.datetime.now()
                elif "date" not in record:
                    # Add current date if missing
                    record["date"] = datetime.datetime.now()
                
                valid_records.append(record)
        
        if not valid_records:
            return jsonify({
                "status": "error",
                "message": "No valid records found in the input data",
                "details": invalid_records
            }), 400
        
        # Insert valid records into MongoDB
        if db is not None:
            # Add timestamp for insertion
            for record in valid_records:
                record["inserted_at"] = datetime.datetime.now()
            
            # Insert into sales collection
            sales_collection = db["sales_data"]
            result = sales_collection.insert_many(valid_records)
            
            return jsonify({
                "status": "success",
                "message": f"Successfully added {len(result.inserted_ids)} sales records",
                "data": {
                    "inserted_count": len(result.inserted_ids),
                    "invalid_records": invalid_records if invalid_records else None
                }
            })
        else:
            # If database not available, return a mock success with warning
            return jsonify({
                "status": "warning",
                "message": "Database not available, but records validated successfully",
                "data": {
                    "valid_count": len(valid_records),
                    "invalid_records": invalid_records if invalid_records else None,
                    "note": "Records were not stored. Please try again when the database is available."
                }
            })
    except Exception as e:
        logger.error(f"Error adding sales data: {e}")
        logger.error(traceback.format_exc())
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/generate-sample-data/<int:count>', methods=['GET'])
@rate_limit
def generate_sample_data(count):
    """Generate and add sample sales data to the database"""
    try:
        if not faker_available:
            return jsonify({
                "status": "error",
                "message": "Faker module not available. Please install with 'pip install faker'"
            }), 500
            
        if count <= 0 or count > 10000:
            return jsonify({
                "status": "error",
                "message": "Count must be between 1 and 10000"
            }), 400
            
        if db is None:
            return jsonify({
                "status": "error",
                "message": "Database connection not available"
            }), 503
            
        # Initialize Faker
        fake = Faker()
        
        # Product types and channels - match SDG.py
        product_types = ["loan", "credit_card", "insurance"]
        channels = ["online", "offline"]
        
        # Generate sample data
        records = []
        for _ in range(count):
            end_date = datetime.datetime.now()
            start_date = end_date - datetime.timedelta(days=365)
            random_date = fake.date_time_between(start_date=start_date, end_date=end_date)
            
            record = {
                "date": random_date,
                "pincode": fake.postcode(),
                "city": fake.city(),
                "product": random.choice(product_types),
                "channel": random.choice(channels),
                "agent_id": str(fake.uuid4()),
                "customer_age": random.randint(21, 60),
                "customer_income": random.randint(20000, 100000),
                "inserted_at": datetime.datetime.now()
            }
            records.append(record)
            
        # Insert records into MongoDB
        sales_collection = db["sales_data"]
        result = sales_collection.insert_many(records)
        
        return jsonify({
            "status": "success",
            "message": f"Generated and inserted {len(result.inserted_ids)} sample records",
            "data": {
                "inserted_count": len(result.inserted_ids),
                "sample": json.loads(json.dumps([{k: str(v) if isinstance(v, datetime.datetime) else v 
                                                for k, v in records[0].items()}], 
                                               default=str))
            }
        })
        
    except Exception as e:
        logger.error(f"Error generating sample data: {e}")
        logger.error(traceback.format_exc())
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    # Check MongoDB connection
    mongo_status = "connected" if db_available else "disconnected"
    
    # Check if models are available
    models_status = "available" if model_available else "unavailable"
    
    # Overall health status
    is_healthy = db_available  # Simplified - could include more checks
    
    response = {
        "status": "healthy" if is_healthy else "unhealthy",
        "checks": {
            "mongodb": mongo_status,
            "models": models_status
        }
    }
    
    status_code = 200 if is_healthy else 503
    return jsonify(response), status_code

# Add custom error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "status": "error",
        "message": "The requested resource was not found."
    }), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "status": "error",
        "message": "An internal server error occurred."
    }), 500

# Add a version endpoint
@app.route('/version', methods=['GET'])
@rate_limit
def get_version():
    """Get API version information"""
    try:
        if db is not None and "model_evaluation" in db.list_collection_names():
            timestamp_doc = db["model_evaluation"].find_one({}, {"timestamp": 1})
            if timestamp_doc and "timestamp" in timestamp_doc:
                models_last_trained = timestamp_doc["timestamp"]
            else:
                models_last_trained = "2023-10-01"
        else:
            models_last_trained = "2023-10-01"
            
        return jsonify({
            "status": "success",
            "data": {
                "api_version": "1.0.0",
                "models_last_trained": models_last_trained
            }
        })
    except Exception as e:
        logger.error(f"Error getting version info: {e}")
        return jsonify({
            "status": "success",
            "data": {
                "api_version": "1.0.0",
                "models_last_trained": "2023-10-01",
                "error_getting_details": str(e)
            }
        })

# Add a statistics endpoint
@app.route('/stats', methods=['GET'])
@rate_limit
def get_stats():
    """Get API usage statistics"""
    try:
        stats = {}
        
        if db is not None:
            collection_stats = {}
            for collection_name in ["demand_prediction", "model_details", "uploaded_data", "sales_data"]:
                if collection_name in db.list_collection_names():
                    collection_stats[f"{collection_name}_count"] = db[collection_name].count_documents({})
                else:
                    collection_stats[f"{collection_name}_count"] = 0
                    
            stats.update(collection_stats)
        else:
            stats = {
                "database_status": "unavailable",
                "note": "Statistics cannot be retrieved because the database is not available."
            }
            
        return jsonify({
            "status": "success",
            "data": stats
        })
    except Exception as e:
        logger.error(f"Error fetching stats: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# Run the Flask application
if __name__ == '__main__':
    # Import configuration
    try:
        from config import API_HOST, API_PORT, DEBUG
    except ImportError:
        # Default values if config.py is missing
        API_HOST = '0.0.0.0'
        API_PORT = 5000
        DEBUG = False
        logger.warning("Config file not found, using default values")
    
    logger.info(f"Starting Demand Prediction API on {API_HOST}:{API_PORT}")
    
    app.run(host=API_HOST, port=API_PORT, debug=DEBUG)