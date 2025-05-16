# Modified model.py with cluster_pincodes fix to handle small datasets

import pandas as pd
import numpy as np
import json
import random
import datetime
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Cache for coordinates to avoid duplicate calculation
coordinate_cache = {}

def load_data():
    """Load data for model training"""
    # This is a stub function that will be replaced by actual data loading
    # In the actual implementation, this would load data from MongoDB
    try:
        from pymongo import MongoClient
        client = MongoClient("mongodb://localhost:27017/")
        db = client["gromo"]
        collection = db["sales_data"]
        
        # Get data from MongoDB
        cursor = collection.find({})
        data = list(cursor)
        
        # Convert to DataFrame
        if data:
            df = pd.DataFrame(data)
            print(f"Loaded {len(df)} records from MongoDB")
            return df
        else:
            print("No data found in MongoDB, returning dummy data")
            return pd.DataFrame({
                'pincode': ['110001', '110002', '110003', '600001', '600002'],
                'product': ['loan', 'credit_card', 'insurance', 'loan', 'credit_card'],
                'channel': ['online', 'offline', 'online', 'offline', 'online'],
                'customer_age': [35, 42, 28, 39, 45],
                'customer_income': [75000, 50000, 90000, 65000, 80000]
            })
    except Exception as e:
        print(f"Error loading data from MongoDB: {e}")
        return pd.DataFrame({
            'pincode': ['110001', '110002', '110003', '600001', '600002'],
            'product': ['loan', 'credit_card', 'insurance', 'loan', 'credit_card'],
            'channel': ['online', 'offline', 'online', 'offline', 'online'],
            'customer_age': [35, 42, 28, 39, 45],
            'customer_income': [75000, 50000, 90000, 65000, 80000]
        })

def assign_coordinates(df):
    """Assign geographic coordinates to pincodes in a dataframe"""
    # Clone the dataframe to avoid modifying the original
    result_df = df.copy()
    
    # Create a mapping of pincodes to coordinates
    pincodes = result_df['pincode'].unique().tolist()
    coordinates = {}
    
    # Use cached values if available
    for pincode in pincodes:
        if pincode in coordinate_cache:
            coordinates[pincode] = coordinate_cache[pincode]
        else:
            # Generate random coordinates within India
            lat = random.uniform(8.0, 37.0)  # Latitude range for India
            lon = random.uniform(68.0, 97.0)  # Longitude range for India
            coordinates[pincode] = (lat, lon)
            # Cache the coordinates
            coordinate_cache[pincode] = (lat, lon)
    
    # Add latitude and longitude columns to the dataframe
    result_df['latitude'] = result_df['pincode'].map(lambda p: coordinates[p][0])
    result_df['longitude'] = result_df['pincode'].map(lambda p: coordinates[p][1])
    
    return result_df

def cluster_pincodes(df, n_clusters=5):
    """
    Cluster pincodes based on coordinates
    
    Parameters:
    -----------
    df : pandas DataFrame
        Dataframe containing pincode, latitude, and longitude columns
    n_clusters : int, default=5
        Number of clusters to create
        
    Returns:
    --------
    df_with_regions : pandas DataFrame
        Dataframe with an additional region_id column
    """
    # Make sure the dataframe has coordinates
    if 'latitude' not in df.columns or 'longitude' not in df.columns:
        df = assign_coordinates(df)
    
    # Extract coordinates
    coords = df[['latitude', 'longitude']].values
    
    # Scale the coordinates
    scaler = StandardScaler()
    coords_scaled = scaler.fit_transform(coords)
    
    # Determine the appropriate number of clusters based on data size
    unique_pincodes = df['pincode'].nunique()
    actual_n_clusters = min(n_clusters, unique_pincodes)
    
    # Fix: Ensure we have at least 1 cluster but not more than the number of samples
    actual_n_clusters = max(1, min(actual_n_clusters, len(coords_scaled)))
    
    # Perform clustering
    kmeans = KMeans(n_clusters=actual_n_clusters, random_state=42, n_init=10)
    df['region_id'] = kmeans.fit_predict(coords_scaled)
    
    return df

def preprocess_data(df):
    """
    Preprocess data for model input
    
    Parameters:
    -----------
    df : pandas DataFrame
        Dataframe to preprocess
        
    Returns:
    --------
    processed_df : pandas DataFrame
        Preprocessed dataframe
    """
    # Clone the dataframe to avoid modifying the original
    result_df = df.copy()
    
    # Ensure proper data types
    if 'customer_age' in result_df.columns:
        result_df['customer_age'] = pd.to_numeric(result_df['customer_age'], errors='coerce')
        # Fill missing values with median
        result_df['customer_age'].fillna(result_df['customer_age'].median(), inplace=True)
    
    if 'customer_income' in result_df.columns:
        result_df['customer_income'] = pd.to_numeric(result_df['customer_income'], errors='coerce')
        # Fill missing values with median
        result_df['customer_income'].fillna(result_df['customer_income'].median(), inplace=True)
    
    # If region_id is not present, add it using clustering
    if 'region_id' not in result_df.columns:
        result_df = cluster_pincodes(result_df)
    
    # One-hot encode categorical variables
    if 'product' in result_df.columns:
        product_dummies = pd.get_dummies(result_df['product'], prefix='product')
        result_df = pd.concat([result_df, product_dummies], axis=1)
    
    if 'channel' in result_df.columns:
        channel_dummies = pd.get_dummies(result_df['channel'], prefix='channel')
        result_df = pd.concat([result_df, channel_dummies], axis=1)
    
    return result_df

def predict_region_demand(df):
    """
    Predict region demand using regression model
    
    Parameters:
    -----------
    df : pandas DataFrame
        Dataframe containing pincode, product, and channel columns
        
    Returns:
    --------
    predictions : list of dict
        List of dictionaries with pincode, predicted_demand, and confidence
    """
    try:
        # Preprocess the data
        new_data = preprocess_data(df)
        
        # In a real implementation, this would use a trained model
        # For now, generate random predictions
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
    except Exception as e:
        print(f"Error in predict_region_demand: {e}")
        raise e

def predict_demand_rise(df):
    """
    Predict if demand will rise using binary classification model
    
    Parameters:
    -----------
    df : pandas DataFrame
        Dataframe containing pincode, product, and channel columns
        
    Returns:
    --------
    predictions : list of dict
        List of dictionaries with pincode, demand_rise, and probability
    """
    try:
        # Preprocess the data
        new_data = preprocess_data(df)
        
        # In a real implementation, this would use a trained model
        # For now, generate random predictions
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
    except Exception as e:
        print(f"Error in predict_demand_rise: {e}")
        raise e

def predict_top_product(df):
    """
    Predict top product using multi-class classification model
    
    Parameters:
    -----------
    df : pandas DataFrame
        Dataframe containing pincode and channel columns
        
    Returns:
    --------
    predictions : list of dict
        List of dictionaries with pincode, top_product, and probability
    """
    try:
        # Preprocess the data
        new_data = preprocess_data(df)
        
        # In a real implementation, this would use a trained model
        # For now, generate random predictions
        products = ["loan", "credit_card", "insurance"]
        
        predictions = []
        for _, row in df.iterrows():
            # Generate random probabilities for each product
            probs = {p: round(random.uniform(0.1, 0.9), 2) for p in products}
            
            # Normalize probabilities to sum to 1
            total = sum(probs.values())
            probs = {p: round(v/total, 2) for p, v in probs.items()}
            
            # Find top product
            top_product = max(probs, key=probs.get)
            
            prediction = {
                "pincode": row["pincode"],
                "channel": row["channel"],
                "top_product": top_product,
                "probability": probs[top_product],
                "all_products": probs
            }
            predictions.append(prediction)
        
        return predictions
    except Exception as e:
        print(f"Error in predict_top_product: {e}")
        raise e

def convert_numpy_types(obj):
    """
    Convert NumPy types to native Python types for MongoDB compatibility
    
    Parameters:
    -----------
    obj : object
        Object containing NumPy types
        
    Returns:
    --------
    converted : object
        Object with NumPy types converted to native Python types
    """
    if isinstance(obj, dict):
        return {k: convert_numpy_types(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(v) for v in obj]
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return convert_numpy_types(obj.tolist())
    elif isinstance(obj, datetime.datetime):
        return obj.isoformat()
    else:
        return obj