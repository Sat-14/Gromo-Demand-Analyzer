import requests
import json
import pandas as pd
import argparse
import os

BASE_URL = "http://localhost:5000"

def test_api_status():
    """Test if the API is running"""
    response = requests.get(f"{BASE_URL}/")
    
    if response.status_code == 200:
        print("✅ API is running")
        print(f"Available endpoints: {json.dumps(response.json()['endpoints'], indent=2)}")
        return True
    else:
        print(f"❌ API is not responding. Status code: {response.status_code}")
        return False

def get_all_regions():
    """Fetch all region summaries"""
    response = requests.get(f"{BASE_URL}/regions")
    
    if response.status_code == 200:
        regions = response.json()['data']
        print(f"✅ Retrieved {len(regions)} regions")
        print("Sample region data:")
        print(json.dumps(regions[0] if regions else {}, indent=2))
        return regions
    else:
        print(f"❌ Failed to retrieve regions. Status code: {response.status_code}")
        print(response.text)
        return []

def get_region_by_id(region_id):
    """Fetch a specific region by ID"""
    response = requests.get(f"{BASE_URL}/regions/{region_id}")
    
    if response.status_code == 200:
        region = response.json()['data']
        print(f"✅ Retrieved data for region {region_id}")
        print(json.dumps(region, indent=2))
        return region
    else:
        print(f"❌ Failed to retrieve region {region_id}. Status code: {response.status_code}")
        print(response.text)
        return None

def get_model_details():
    """Fetch model details and evaluation metrics"""
    response = requests.get(f"{BASE_URL}/models")
    
    if response.status_code == 200:
        data = response.json()['data']
        print("✅ Retrieved model details and evaluation metrics")
        print(f"Found {len(data['model_details'])} models:")
        for model in data['model_details']:
            print(f"  - {model['model_type']}: {model['target']}")
        return data
    else:
        print(f"❌ Failed to retrieve model details. Status code: {response.status_code}")
        print(response.text)
        return None

def predict_demand(data_file):
    """Predict region demand using the API"""
    # Load data from file
    if not os.path.exists(data_file):
        print(f"❌ File not found: {data_file}")
        return None
    
    # Determine file type and load data
    if data_file.endswith('.csv'):
        df = pd.read_csv(data_file)
    elif data_file.endswith(('.xls', '.xlsx')):
        df = pd.read_excel(data_file)
    elif data_file.endswith('.json'):
        df = pd.read_json(data_file)
    else:
        print(f"❌ Unsupported file format: {data_file}")
        return None
    
    # Convert DataFrame to list of dictionaries for JSON
    data = df.to_dict(orient='records')
    
    # Make API request
    response = requests.post(
        f"{BASE_URL}/predict/demand",
        json=data,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        predictions = response.json()['data']
        print(f"✅ Successfully predicted demand for {len(data)} records")
        print("Sample predictions:")
        print(json.dumps(predictions, indent=2))
        return predictions
    else:
        print(f"❌ Failed to predict demand. Status code: {response.status_code}")
        print(response.text)
        return None

def predict_all(data_file):
    """Run all prediction models using the API"""
    # Load data from file
    if not os.path.exists(data_file):
        print(f"❌ File not found: {data_file}")
        return None
    
    # Determine file type and load data
    if data_file.endswith('.csv'):
        df = pd.read_csv(data_file)
    elif data_file.endswith(('.xls', '.xlsx')):
        df = pd.read_excel(data_file)
    elif data_file.endswith('.json'):
        df = pd.read_json(data_file)
    else:
        print(f"❌ Unsupported file format: {data_file}")
        return None
    
    # Convert DataFrame to list of dictionaries for JSON
    data = df.to_dict(orient='records')
    
    # Make API request
    response = requests.post(
        f"{BASE_URL}/predict/all",
        json=data,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        results = response.json()['data']
        print(f"✅ Successfully ran all predictions for {len(data)} records")
        print("Results include:")
        
        for model_type, predictions in results.items():
            print(f"  - {model_type}: predictions for {len(predictions['region_id'])} regions")
        
        return results
    else:
        print(f"❌ Failed to run predictions. Status code: {response.status_code}")
        print(response.text)
        return None

def upload_data(file_path):
    """Upload data file to the API"""
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return None
    
    # Check file type
    if not file_path.endswith(('.csv', '.xls', '.xlsx', '.json')):
        print(f"❌ Unsupported file format: {file_path}")
        return None
    
    # Upload file
    with open(file_path, 'rb') as file:
        response = requests.post(
            f"{BASE_URL}/upload/data",
            files={'file': file}
        )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Successfully uploaded data")
        print(f"  - Rows: {result['data']['rows']}")
        print(f"  - Columns: {', '.join(result['data']['columns'])}")
        return result
    else:
        print(f"❌ Failed to upload data. Status code: {response.status_code}")
        print(response.text)
        return None

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Demand Prediction API Client')
    parser.add_argument('action', choices=[
        'status', 'regions', 'region', 'models', 
        'predict-demand', 'predict-all', 'upload'
    ], help='Action to perform')
    parser.add_argument('--id', help='Region ID for specific region queries')
    parser.add_argument('--file', help='Data file path for predictions or uploads')
    
    args = parser.parse_args()
    
    # Execute requested action
    if args.action == 'status':
        test_api_status()
    elif args.action == 'regions':
        get_all_regions()
    elif args.action == 'region':
        if not args.id:
            print("❌ Region ID is required for this action")
            return
        get_region_by_id(args.id)
    elif args.action == 'models':
        get_model_details()
    elif args.action == 'predict-demand':
        if not args.file:
            print("❌ Data file is required for this action")
            return
        predict_demand(args.file)
    elif args.action == 'predict-all':
        if not args.file:
            print("❌ Data file is required for this action")
            return
        predict_all(args.file)
    elif args.action == 'upload':
        if not args.file:
            print("❌ Data file is required for this action")
            return
        upload_data(args.file)

if __name__ == '__main__':
    main()