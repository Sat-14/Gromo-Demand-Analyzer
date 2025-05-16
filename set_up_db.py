# Simple file to set up the MongoDB database

from pymongo import MongoClient
import datetime
import random
import json

def initialize_database():
    """Initialize MongoDB database with required collections and sample data"""
    print("Initializing database...")
    
    # Connect to MongoDB
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client["gromo"]
        print("Connected to MongoDB successfully")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return
    
    # Create or clear collections
    collections = ["demand_prediction", "model_details", "model_evaluation", "sales_data", "uploaded_data"]
    for collection_name in collections:
        if collection_name in db.list_collection_names():
            db[collection_name].delete_many({})
            print(f"Cleared existing collection: {collection_name}")
        else:
            db.create_collection(collection_name)
            print(f"Created new collection: {collection_name}")
    
    # Create sample data for demand_prediction
    sample_regions = [
        {
            "region_id": 0,
            "pincodes": ["110001", "110002", "110003"],
            "total_demand": 500,
            "avg_demand_per_pincode": 166.67,
            "demand_rise_flag": True,
            "products": {
                "top_product": "loan",
                "distribution": {"loan": 0.55, "credit_card": 0.30, "insurance": 0.15}
            },
            "channels": {
                "top_channel": "online",
                "distribution": {"online": 0.65, "offline": 0.35}
            }
        },
        {
            "region_id": 1,
            "pincodes": ["400001", "400002"],
            "total_demand": 420,
            "avg_demand_per_pincode": 210.0,
            "demand_rise_flag": True,
            "products": {
                "top_product": "credit_card",
                "distribution": {"loan": 0.35, "credit_card": 0.45, "insurance": 0.20}
            },
            "channels": {
                "top_channel": "offline",
                "distribution": {"online": 0.40, "offline": 0.60}
            }
        }
    ]
    
    db["demand_prediction"].insert_many(sample_regions)
    print(f"Added {len(sample_regions)} sample regions to demand_prediction collection")
    
    # Create sample model details
    sample_model_details = [
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
            "training_date": datetime.datetime.now().isoformat()
        },
        {
            "model_type": "binary_classification",
            "target": "demand_rise",
            "hyperparameters": {
                "model__C": 1.0,
                "model__solver": "liblinear"
            },
            "metrics": {
                "accuracy": 0.92,
                "classification_report": {
                    "0": {"precision": 0.90, "recall": 0.88, "f1-score": 0.89},
                    "1": {"precision": 0.93, "recall": 0.95, "f1-score": 0.94}
                }
            },
            "training_date": datetime.datetime.now().isoformat()
        },
        {
            "model_type": "multi_class_classification",
            "target": "product_top",
            "hyperparameters": {
                "model__n_estimators": 100,
                "model__max_depth": 5
            },
            "metrics": {
                "accuracy": 0.87,
                "classification_report": {
                    "0": {"precision": 0.85, "recall": 0.88, "f1-score": 0.86},
                    "1": {"precision": 0.90, "recall": 0.87, "f1-score": 0.88},
                    "2": {"precision": 0.86, "recall": 0.85, "f1-score": 0.85}
                },
                "product_mapping": {"0": "loan", "1": "credit_card", "2": "insurance"}
            },
            "training_date": datetime.datetime.now().isoformat()
        }
    ]
    
    db["model_details"].insert_many(sample_model_details)
    print(f"Added {len(sample_model_details)} sample model details to model_details collection")
    
    # Create sample model evaluation
    sample_evaluation = {
        "timestamp": datetime.datetime.now().isoformat(),
        "dataset_size": 1000,
        "regression_metrics": {
            "mse": 150.25,
            "rmse": 12.26,
            "mae": 9.85,
            "r2": 0.85
        },
        "binary_classification_metrics": {
            "accuracy": 0.92,
            "report": {"0": {"f1-score": 0.89}, "1": {"f1-score": 0.94}}
        },
        "multi_classification_metrics": {
            "accuracy": 0.87,
            "report": {"0": {"f1-score": 0.86}, "1": {"f1-score": 0.88}, "2": {"f1-score": 0.85}}
        }
    }
    
    db["model_evaluation"].insert_one(sample_evaluation)
    print(f"Added sample evaluation to model_evaluation collection")
    
    # Create sample sales data
    products = ["loan", "credit_card", "insurance"]
    channels = ["online", "offline"]
    pincodes = ["110001", "110002", "110003", "400001", "400002", "400003", "600001", "600002"]
    cities = ["Delhi", "Mumbai", "Chennai"]
    
    # Generate random sales records
    sample_sales = []
    for _ in range(100):
        # Generate random date in the last year
        days_ago = random.randint(0, 365)
        date = datetime.datetime.now() - datetime.timedelta(days=days_ago)
        
        record = {
            "date": date,
            "pincode": random.choice(pincodes),
            "city": random.choice(cities),
            "product": random.choice(products),
            "channel": random.choice(channels),
            "agent_id": f"AG{random.randint(1000, 9999)}",
            "customer_age": random.randint(21, 60),
            "customer_income": random.randint(20000, 100000),
            "inserted_at": datetime.datetime.now()
        }
        sample_sales.append(record)
    
    db["sales_data"].insert_many(sample_sales)
    print(f"Added {len(sample_sales)} sample sales records to sales_data collection")
    
    print("\nDatabase initialization complete.")
    print(f"Collections: {db.list_collection_names()}")
    
    # Print collection counts
    for collection_name in db.list_collection_names():
        count = db[collection_name].count_documents({})
        print(f"Collection {collection_name}: {count} documents")

if __name__ == "__main__":
    initialize_database()