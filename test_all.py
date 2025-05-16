import requests
import json
import time
import os

# Base URL for the API
BASE_URL = "http://localhost:5000"

def test_endpoint(method, endpoint, data=None, files=None, expected_status=200, description=None):
    """Generic function to test an endpoint"""
    url = f"{BASE_URL}{endpoint}"
    
    print(f"\n{'='*80}")
    print(f"Testing: {method} {endpoint}")
    if description:
        print(f"Description: {description}")
    print(f"{'='*80}")
    
    headers = {}
    if data and not files:
        headers["Content-Type"] = "application/json"
        data = json.dumps(data)
    
    start_time = time.time()
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers)
        elif method.upper() == "POST":
            response = requests.post(url, headers=headers, data=data, files=files)
        else:
            print(f"Unsupported method: {method}")
            return False
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"Status Code: {response.status_code} (Expected: {expected_status})")
        print(f"Response Time: {duration:.2f} seconds")
        
        try:
            response_json = response.json()
            print(f"Response JSON: {json.dumps(response_json, indent=2)[:500]}...")
            if len(json.dumps(response_json)) > 500:
                print("(Response truncated)")
        except:
            print(f"Response Text: {response.text[:500]}")
            if len(response.text) > 500:
                print("(Response truncated)")
        
        if response.status_code == expected_status:
            print("✅ TEST PASSED")
            return True
        else:
            print(f"❌ TEST FAILED: Expected status {expected_status}, got {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ TEST FAILED with exception: {str(e)}")
        return False

def run_all_tests():
    """Run tests for all endpoints"""
    test_results = {}
    
    # 1. Test root endpoint
    test_results["root"] = test_endpoint(
        "GET", "/", 
        description="Get API information and available endpoints"
    )
    
    # 2. Test regions endpoint
    test_results["regions"] = test_endpoint(
        "GET", "/regions", 
        description="Get all region summaries"
    )
    
    # 3. Test specific region endpoint (may fail if region_id doesn't exist)
    test_results["region_detail"] = test_endpoint(
        "GET", "/regions/1", 
        description="Get details for a specific region",
        expected_status=200  # Change to 404 if you expect the region not to exist
    )
    
    # 4. Test models endpoint
    test_results["models"] = test_endpoint(
        "GET", "/models", 
        description="Get model details and evaluation metrics"
    )
    
    # 5. Test predict demand endpoint
    predict_data = [{
        "pincode": "400001",
        "product": "loan",
        "channel": "online",
        "customer_age": 35,
        "customer_income": 75000
    }]
    test_results["predict_demand"] = test_endpoint(
        "POST", "/predict/demand", 
        data=predict_data,
        description="Predict region demand using regression model"
    )
    
    # 6. Test predict demand rise endpoint
    test_results["predict_rise"] = test_endpoint(
        "POST", "/predict/demand-rise", 
        data=predict_data,
        description="Predict if demand will rise using binary classification model"
    )
    
    # 7. Test predict top product endpoint
    predict_product_data = [{
        "pincode": "400001",
        "channel": "online",
        "customer_age": 35,
        "customer_income": 75000
    }]
    test_results["predict_product"] = test_endpoint(
        "POST", "/predict/top-product", 
        data=predict_product_data,
        description="Predict top product using multi-class classification model"
    )
    
    # 8. Test predict all endpoint
    test_results["predict_all"] = test_endpoint(
        "POST", "/predict/all", 
        data=predict_data,
        description="Run all three prediction models at once"
    )
    
    # 9. Test upload data endpoint (if you have a test file)
    # Uncomment and modify path if you want to test file upload
    """
    if os.path.exists("test_data.csv"):
        with open("test_data.csv", 'rb') as f:
            files = {'file': ('test_data.csv', f, 'text/csv')}
            test_results["upload_data"] = test_endpoint(
                "POST", "/upload/data", 
                files=files,
                description="Upload and process new data file"
            )
    else:
        print("\nSkipping file upload test - test_data.csv not found")
    """
    
    # 10. Test add sales data endpoint
    sales_data = [{
        "date": "2025-04-15T12:30:45",
        "pincode": "400001",
        "city": "Mumbai",
        "product": "loan",
        "channel": "online",
        "agent_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
        "customer_age": 35,
        "customer_income": 75000
    }]
    test_results["add_sales"] = test_endpoint(
        "POST", "/sales/add", 
        data=sales_data,
        description="Add sales data records directly to the database"
    )
    
    # 11. Test generate sample data endpoint
    test_results["generate_sample"] = test_endpoint(
        "GET", "/generate-sample-data/5", 
        description="Generate and add 5 sample sales data records"
    )
    
    # 12. Test health check endpoint
    test_results["health"] = test_endpoint(
        "GET", "/health", 
        description="Get API health status"
    )
    
    # 13. Test version endpoint
    test_results["version"] = test_endpoint(
        "GET", "/version", 
        description="Get API version information"
    )
    
    # 14. Test stats endpoint
    test_results["stats"] = test_endpoint(
        "GET", "/stats", 
        description="Get API usage statistics"
    )
    
    # Print summary
    print("\n\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    success_count = sum(1 for result in test_results.values() if result)
    total_count = len(test_results)
    
    for endpoint, success in test_results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{endpoint}: {status}")
    
    print(f"\nOverall: {success_count}/{total_count} tests passed ({success_count/total_count*100:.1f}%)")

if __name__ == "__main__":
    run_all_tests()