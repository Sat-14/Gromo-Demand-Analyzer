import requests
import json
import pandas as pd
import argparse
import os
import sys
from typing import Dict, List, Union, Optional, Any

# Default base URL for the API
BASE_URL = "http://localhost:5000"

class DemandPredictionClient:
    """
    Client for interacting with the Demand Prediction API.
    
    This client provides a simple interface to access all endpoints of the
    Demand Prediction API, handling request formatting, error handling, and
    response parsing.
    """
    
    def __init__(self, base_url: str = BASE_URL, timeout: int = 10):
        """
        Initialize the Demand Prediction API client.
        
        Args:
            base_url: Base URL of the API, defaults to http://localhost:5000
            timeout: Request timeout in seconds, defaults to 10
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
    
    def _handle_response(self, response: requests.Response) -> Dict:
        """
        Handle API response, checking for errors and returning parsed JSON.
        
        Args:
            response: Response object from requests
            
        Returns:
            Parsed JSON response
            
        Raises:
            Exception: If the response indicates an error
        """
        try:
            data = response.json()
            
            if response.status_code >= 400 or (isinstance(data, dict) and data.get('status') == 'error'):
                error_message = data.get('message', 'Unknown error') if isinstance(data, dict) else 'Unknown error'
                raise Exception(f"API Error ({response.status_code}): {error_message}")
                
            return data
        except json.JSONDecodeError:
            raise Exception(f"Failed to parse API response as JSON: {response.text}")
    
    def check_api_status(self) -> Dict:
        """
        Test if the API is running and return available endpoints.
        
        Returns:
            API status information including available endpoints
        """
        response = requests.get(f"{self.base_url}/", timeout=self.timeout)
        return self._handle_response(response)
    
    def get_all_regions(self) -> List[Dict]:
        """
        Fetch all region summaries.
        
        Returns:
            List of region summaries
        """
        response = requests.get(f"{self.base_url}/regions", timeout=self.timeout)
        result = self._handle_response(response)
        return result.get('data', [])
    
    def get_region_by_id(self, region_id: Union[int, str]) -> Dict:
        """
        Fetch a specific region by ID.
        
        Args:
            region_id: ID of the region to retrieve
            
        Returns:
            Region details
        """
        response = requests.get(f"{self.base_url}/regions/{region_id}", timeout=self.timeout)
        result = self._handle_response(response)
        return result.get('data', {})
    
    def get_model_details(self) -> Dict:
        """
        Fetch model details and evaluation metrics.
        
        Returns:
            Model details and evaluation metrics
        """
        response = requests.get(f"{self.base_url}/models", timeout=self.timeout)
        result = self._handle_response(response)
        return result.get('data', {})
    
    def predict_demand(self, data: Union[List[Dict], str, pd.DataFrame]) -> List[Dict]:
        """
        Predict region demand using the API.
        
        Args:
            data: Either a list of dictionaries, a DataFrame, or a file path
            
        Returns:
            List of demand predictions
            
        Raises:
            ValueError: If the input data format is invalid
            FileNotFoundError: If the specified file does not exist
        """
        # Process input data based on type
        processed_data = self._process_input_data(data)
        
        # Make API request
        response = requests.post(
            f"{self.base_url}/predict/demand",
            json=processed_data,
            headers={"Content-Type": "application/json"},
            timeout=self.timeout
        )
        
        result = self._handle_response(response)
        return result.get('data', [])
    
    def predict_demand_rise(self, data: Union[List[Dict], str, pd.DataFrame]) -> List[Dict]:
        """
        Predict if demand will rise using the API.
        
        Args:
            data: Either a list of dictionaries, a DataFrame, or a file path
            
        Returns:
            List of demand rise predictions
            
        Raises:
            ValueError: If the input data format is invalid
            FileNotFoundError: If the specified file does not exist
        """
        # Process input data based on type
        processed_data = self._process_input_data(data)
        
        # Make API request
        response = requests.post(
            f"{self.base_url}/predict/demand-rise",
            json=processed_data,
            headers={"Content-Type": "application/json"},
            timeout=self.timeout
        )
        
        result = self._handle_response(response)
        return result.get('data', [])
    
    def predict_top_product(self, data: Union[List[Dict], str, pd.DataFrame]) -> List[Dict]:
        """
        Predict top product using the API.
        
        Args:
            data: Either a list of dictionaries, a DataFrame, or a file path
            
        Returns:
            List of top product predictions
            
        Raises:
            ValueError: If the input data format is invalid
            FileNotFoundError: If the specified file does not exist
        """
        # Process input data based on type
        processed_data = self._process_input_data(data)
        
        # Make API request
        response = requests.post(
            f"{self.base_url}/predict/top-product",
            json=processed_data,
            headers={"Content-Type": "application/json"},
            timeout=self.timeout
        )
        
        result = self._handle_response(response)
        return result.get('data', [])
    
    def predict_all(self, data: Union[List[Dict], str, pd.DataFrame]) -> Dict:
        """
        Run all prediction models using the API.
        
        Args:
            data: Either a list of dictionaries, a DataFrame, or a file path
            
        Returns:
            Dictionary containing results from all prediction models
            
        Raises:
            ValueError: If the input data format is invalid
            FileNotFoundError: If the specified file does not exist
        """
        # Process input data based on type
        processed_data = self._process_input_data(data)
        
        # Make API request
        response = requests.post(
            f"{self.base_url}/predict/all",
            json=processed_data,
            headers={"Content-Type": "application/json"},
            timeout=self.timeout
        )
        
        result = self._handle_response(response)
        return result.get('data', {})
    
    def upload_data(self, file_path: str) -> Dict:
        """
        Upload data file to the API.
        
        Args:
            file_path: Path to the data file
            
        Returns:
            Upload results
            
        Raises:
            FileNotFoundError: If the specified file does not exist
            ValueError: If the file format is unsupported
        """
        # Check if file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Check file type
        if not file_path.endswith(('.csv', '.xls', '.xlsx', '.json')):
            raise ValueError(f"Unsupported file format: {file_path}")
        
        # Upload file
        with open(file_path, 'rb') as file:
            response = requests.post(
                f"{self.base_url}/upload/data",
                files={'file': file},
                timeout=self.timeout
            )
        
        return self._handle_response(response)
    
    def add_sales_data(self, data: Union[List[Dict], str, pd.DataFrame]) -> Dict:
        """
        Add sales data records directly to the database.
        
        Args:
            data: Either a list of dictionaries, a DataFrame, or a file path
            
        Returns:
            Summary of added records
        """
        # Process input data based on type
        processed_data = self._process_input_data(data)
        
        # Make API request
        response = requests.post(
            f"{self.base_url}/sales/add",
            json=processed_data,
            headers={"Content-Type": "application/json"},
            timeout=self.timeout
        )
        
        return self._handle_response(response)
    
    def generate_sample_data(self, count: int = 100) -> Dict:
        """
        Generate and add sample sales data to the database.
        
        Args:
            count: Number of records to generate, defaults to 100
            
        Returns:
            Summary of generated records
            
        Raises:
            ValueError: If count is not between 1 and 10000
        """
        if count <= 0 or count > 10000:
            raise ValueError("Count must be between 1 and 10000")
            
        response = requests.get(
            f"{self.base_url}/generate-sample-data/{count}",
            timeout=self.timeout
        )
        
        return self._handle_response(response)
    
    def check_health(self) -> Dict:
        """
        Check the health status of the API.
        
        Returns:
            Health status information
        """
        response = requests.get(f"{self.base_url}/health", timeout=self.timeout)
        return self._handle_response(response)
    
    def get_version(self) -> Dict:
        """
        Get API version information.
        
        Returns:
            API version and model training information
        """
        response = requests.get(f"{self.base_url}/version", timeout=self.timeout)
        result = self._handle_response(response)
        return result.get('data', {})
    
    def get_stats(self) -> Dict:
        """
        Get API usage statistics.
        
        Returns:
            Usage statistics
        """
        response = requests.get(f"{self.base_url}/stats", timeout=self.timeout)
        result = self._handle_response(response)
        return result.get('data', {})
    
    def _process_input_data(self, data: Union[List[Dict], str, pd.DataFrame]) -> List[Dict]:
        """
        Process input data based on its type.
        
        Args:
            data: Either a list of dictionaries, a DataFrame, or a file path
            
        Returns:
            List of dictionaries ready for API submission
            
        Raises:
            ValueError: If the input data format is invalid
            FileNotFoundError: If the specified file does not exist
        """
        # If data is already a list of dictionaries, use it directly
        if isinstance(data, list) and all(isinstance(item, dict) for item in data):
            return data
        
        # If data is a DataFrame, convert to list of dictionaries
        elif isinstance(data, pd.DataFrame):
            return data.to_dict(orient='records')
        
        # If data is a file path, load the file
        elif isinstance(data, str):
            # Check if file exists
            if not os.path.exists(data):
                raise FileNotFoundError(f"File not found: {data}")
            
            # Determine file type and load data
            if data.endswith('.csv'):
                df = pd.read_csv(data)
            elif data.endswith(('.xls', '.xlsx')):
                df = pd.read_excel(data)
            elif data.endswith('.json'):
                df = pd.read_json(data)
            else:
                raise ValueError(f"Unsupported file format: {data}")
            
            # Convert DataFrame to list of dictionaries
            return df.to_dict(orient='records')
        
        # Invalid input type
        else:
            raise ValueError(f"Invalid input data type: {type(data)}")


def test_api_status():
    """Test if the API is running"""
    client = DemandPredictionClient()
    try:
        result = client.check_api_status()
        print("✅ API is running")
        print(f"Available endpoints: {json.dumps(result['endpoints'], indent=2)}")
        return True
    except Exception as e:
        print(f"❌ API is not responding: {e}")
        return False

def get_all_regions():
    """Fetch all region summaries"""
    client = DemandPredictionClient()
    try:
        regions = client.get_all_regions()
        print(f"✅ Retrieved {len(regions)} regions")
        print("Sample region data:")
        print(json.dumps(regions[0] if regions else {}, indent=2))
        return regions
    except Exception as e:
        print(f"❌ Failed to retrieve regions: {e}")
        return []

def get_region_by_id(region_id):
    """Fetch a specific region by ID"""
    client = DemandPredictionClient()
    try:
        region = client.get_region_by_id(region_id)
        print(f"✅ Retrieved data for region {region_id}")
        print(json.dumps(region, indent=2))
        return region
    except Exception as e:
        print(f"❌ Failed to retrieve region {region_id}: {e}")
        return None

def get_model_details():
    """Fetch model details and evaluation metrics"""
    client = DemandPredictionClient()
    try:
        data = client.get_model_details()
        print("✅ Retrieved model details and evaluation metrics")
        print(f"Found {len(data['model_details'])} models:")
        for model in data['model_details']:
            print(f"  - {model['model_type']}: {model['target']}")
        return data
    except Exception as e:
        print(f"❌ Failed to retrieve model details: {e}")
        return None

def predict_demand(data_file):
    """Predict region demand using the API"""
    client = DemandPredictionClient()
    try:
        predictions = client.predict_demand(data_file)
        print(f"✅ Successfully predicted demand for {len(predictions)} records")
        print("Sample predictions:")
        sample_count = min(3, len(predictions))
        print(json.dumps(predictions[:sample_count], indent=2))
        return predictions
    except Exception as e:
        print(f"❌ Failed to predict demand: {e}")
        return None

def predict_all(data_file):
    """Run all prediction models using the API"""
    client = DemandPredictionClient()
    try:
        results = client.predict_all(data_file)
        print(f"✅ Successfully ran all predictions")
        print("Results include:")
        
        for model_type, predictions in results.items():
            print(f"  - {model_type}: {len(predictions)} predictions")
        
        return results
    except Exception as e:
        print(f"❌ Failed to run predictions: {e}")
        return None

def upload_data(file_path):
    """Upload data file to the API"""
    client = DemandPredictionClient()
    try:
        result = client.upload_data(file_path)
        print(f"✅ Successfully uploaded data")
        print(f"  - Rows: {result['data']['rows']}")
        print(f"  - Columns: {', '.join(result['data']['columns'])}")
        return result
    except Exception as e:
        print(f"❌ Failed to upload data: {e}")
        return None

def add_sales_data(data_file):
    """Add sales data records directly to the database"""
    client = DemandPredictionClient()
    try:
        result = client.add_sales_data(data_file)
        print(f"✅ Successfully added sales data")
        print(f"  - Inserted count: {result['data']['inserted_count']}")
        if result['data'].get('invalid_records'):
            print(f"  - Invalid records: {len(result['data']['invalid_records'])}")
        return result
    except Exception as e:
        print(f"❌ Failed to add sales data: {e}")
        return None

def generate_sample_data(count):
    """Generate sample sales data"""
    client = DemandPredictionClient()
    try:
        result = client.generate_sample_data(count)
        print(f"✅ Successfully generated sample data")
        print(f"  - Generated {result['data']['inserted_count']} records")
        return result
    except Exception as e:
        print(f"❌ Failed to generate sample data: {e}")
        return None

def check_health():
    """Check the health status of the API"""
    client = DemandPredictionClient()
    try:
        result = client.check_health()
        print(f"✅ API health: {result['status']}")
        print(f"  - MongoDB: {result['checks']['mongodb']}")
        print(f"  - Models: {result['checks']['models']}")
        return result
    except Exception as e:
        print(f"❌ Failed to check API health: {e}")
        return None

def get_version():
    """Get API version information"""
    client = DemandPredictionClient()
    try:
        version = client.get_version()
        print(f"✅ API version: {version['api_version']}")
        print(f"  - Models last trained: {version['models_last_trained']}")
        return version
    except Exception as e:
        print(f"❌ Failed to get API version: {e}")
        return None

def get_stats():
    """Get API usage statistics"""
    client = DemandPredictionClient()
    try:
        stats = client.get_stats()
        print(f"✅ API statistics:")
        for key, value in stats.items():
            print(f"  - {key}: {value}")
        return stats
    except Exception as e:
        print(f"❌ Failed to get API statistics: {e}")
        return None

def main():
    """Main function to handle command line arguments and execute actions"""
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Demand Prediction API Client')
    parser.add_argument('action', choices=[
        'status', 'regions', 'region', 'models', 
        'predict-demand', 'predict-rise', 'predict-product', 'predict-all', 
        'upload', 'add-sales', 'generate-samples', 'health', 'version', 'stats'
    ], help='Action to perform')
    parser.add_argument('--id', help='Region ID for specific region queries')
    parser.add_argument('--file', help='Data file path for predictions or uploads')
    parser.add_argument('--count', type=int, default=100, help='Number of sample records to generate')
    parser.add_argument('--url', default=BASE_URL, help='Base URL for the API')
    
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
    elif args.action == 'predict-rise':
        if not args.file:
            print("❌ Data file is required for this action")
            return
        client = DemandPredictionClient()
        try:
            predictions = client.predict_demand_rise(args.file)
            print(f"✅ Successfully predicted demand rise for {len(predictions)} records")
            print("Sample predictions:")
            sample_count = min(3, len(predictions))
            print(json.dumps(predictions[:sample_count], indent=2))
        except Exception as e:
            print(f"❌ Failed to predict demand rise: {e}")
    elif args.action == 'predict-product':
        if not args.file:
            print("❌ Data file is required for this action")
            return
        client = DemandPredictionClient()
        try:
            predictions = client.predict_top_product(args.file)
            print(f"✅ Successfully predicted top product for {len(predictions)} records")
            print("Sample predictions:")
            sample_count = min(3, len(predictions))
            print(json.dumps(predictions[:sample_count], indent=2))
        except Exception as e:
            print(f"❌ Failed to predict top product: {e}")
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
    elif args.action == 'add-sales':
        if not args.file:
            print("❌ Data file is required for this action")
            return
        add_sales_data(args.file)
    elif args.action == 'generate-samples':
        generate_sample_data(args.count)
    elif args.action == 'health':
        check_health()
    elif args.action == 'version':
        get_version()
    elif args.action == 'stats':
        get_stats()

if __name__ == '__main__':
    main()
