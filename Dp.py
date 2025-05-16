# data_processing.py

import pandas as pd
from faker import Faker
from pymongo import MongoClient
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

fake = Faker()
client = MongoClient("mongodb://localhost:27017/")
db = client["gromo"]
collection = db["sales_data"]

def load_data():
    data = list(collection.find({}, {"_id": 0}))
    return pd.DataFrame(data)

def assign_coordinates(df):
    unique_pins = df["pincode"].unique()
    pin_coord_map = {
        pin: (fake.latitude(), fake.longitude()) for pin in unique_pins
    }
    df["latitude"] = df["pincode"].map(lambda x: pin_coord_map[x][0])
    df["longitude"] = df["pincode"].map(lambda x: pin_coord_map[x][1])
    return df

def cluster_pincodes(df, n_clusters=20):
    coords = df[["latitude", "longitude"]]
    scaler = StandardScaler()
    coords_scaled = scaler.fit_transform(coords)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df["region_id"] = kmeans.fit_predict(coords_scaled)
    return df

def preprocess_data(df):
    # date is already datetime.datetime object from MongoDB
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["day_of_week"] = df["date"].dt.dayofweek
    
    # Drop columns not used in modeling
    df.drop(columns=["date", "city", "agent_id", "latitude", "longitude"], inplace=True)

    # Define features
    categorical_cols = ["product", "channel", "region_id"]
    numeric_cols = ["customer_age", "customer_income", "year", "month", "day_of_week"]

    # Create transformation pipeline
    preprocessor = ColumnTransformer(transformers=[
        ("num", StandardScaler(), numeric_cols),
        ("cat", OneHotEncoder(sparse_output=False, handle_unknown='ignore'), categorical_cols)
    ])

    X_processed = preprocessor.fit_transform(df)

    # Extract column names for result
    cat_features = preprocessor.named_transformers_["cat"].get_feature_names_out(categorical_cols)
    feature_names = numeric_cols + list(cat_features)

    return pd.DataFrame(X_processed, columns=feature_names)

if __name__ == "__main__":
    df = load_data()
    df = assign_coordinates(df)
    df = cluster_pincodes(df)
    processed_df = preprocess_data(df)

    print(processed_df.head())
