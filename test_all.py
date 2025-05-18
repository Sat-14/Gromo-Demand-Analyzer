import requests
import json
import time
import os
import datetime
import base64
from pathlib import Path

# Base URL for the API
BASE_URL = "http://localhost:5000"

# Create output directory if it doesn't exist
OUTPUT_DIR = "output"
Path(OUTPUT_DIR).mkdir(exist_ok=True)

# Create a log file with timestamp
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
LOG_FILE = os.path.join(OUTPUT_DIR, f"api_test_log_{timestamp}.txt")
RESPONSE_DIR = os.path.join(OUTPUT_DIR, f"responses_{timestamp}")
Path(RESPONSE_DIR).mkdir(exist_ok=True)

def write_to_log(message):
    """Write message to log file"""
    with open(LOG_FILE, 'a', encoding='utf-8') as log_file:
        log_file.write(message + '\n')
    print(message)

def save_response_content(endpoint_name, response):
    """Save response content to files based on content type"""
    try:
        # Try to parse as JSON first
        response_data = response.json()
        
        # Save JSON response
        json_path = os.path.join(RESPONSE_DIR, f"{endpoint_name}_response.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(response_data, f, indent=2)
        
        # Check for any base64 encoded images in the response
        if isinstance(response_data, dict):
            for key, value in response_data.items():
                if isinstance(value, str) and value.startswith(('data:image', 'data:application/octet-stream')):
                    try:
                        # Extract image data
                        img_format = 'png'  # default
                        if 'image/jpeg' in value:
                            img_format = 'jpg'
                        elif 'image/png' in value:
                            img_format = 'png'
                        
                        # Remove header and decode
                        img_data = value.split(',', 1)[1]
                        img_bytes = base64.b64decode(img_data)
                        
                        # Save image
                        img_path = os.path.join(RESPONSE_DIR, f"{endpoint_name}_{key}.{img_format}")
                        with open(img_path, 'wb') as img_file:
                            img_file.write(img_bytes)
                        write_to_log(f"  - Saved image to: {img_path}")
                    except Exception as e:
                        write_to_log(f"  - Failed to save image data: {str(e)}")
    except ValueError:
        # If not JSON, save as text
        text_path = os.path.join(RESPONSE_DIR, f"{endpoint_name}_response.txt")
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(response.text)
    except Exception as e:
        write_to_log(f"  - Error saving response content: {str(e)}")

def test_endpoint(method, endpoint, data=None, files=None, expected_status=200, description=None):
    """Generic function to test an endpoint"""
    url = f"{BASE_URL}{endpoint}"
    
    # Get a clean endpoint name for file naming
    endpoint_name = endpoint.strip('/').replace('/', '_')
    if not endpoint_name:
        endpoint_name = "root"
    
    separator = '=' * 80
    write_to_log(f"\n{separator}")
    write_to_log(f"Testing: {method} {endpoint}")
    if description:
        write_to_log(f"Description: {description}")
    write_to_log(separator)
    
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
            write_to_log(f"Unsupported method: {method}")
            return False
        
        end_time = time.time()
        duration = end_time - start_time
        
        write_to_log(f"Status Code: {response.status_code} (Expected: {expected_status})")
        write_to_log(f"Response Time: {duration:.2f} seconds")
        
        # Save full response content
        save_response_content(endpoint_name, response)
        
        try:
            response_json = response.json()
            truncated_response = json.dumps(response_json, indent=2)[:500]
            write_to_log(f"Response JSON: {truncated_response}...")
            if len(json.dumps(response_json)) > 500:
                write_to_log("(Response truncated in log, full response saved to file)")
        except:
            truncated_text = response.text[:500]
            write_to_log(f"Response Text: {truncated_text}")
            if len(response.text) > 500:
                write_to_log("(Response truncated in log, full response saved to file)")
        
        if response.status_code == expected_status:
            write_to_log("✅ TEST PASSED")
            return True
        else:
            write_to_log(f"❌ TEST FAILED: Expected status {expected_status}, got {response.status_code}")
            return False
            
    except Exception as e:
        write_to_log(f"❌ TEST FAILED with exception: {str(e)}")
        return False

def run_all_tests():
    """Run tests for all endpoints"""
    # Write header to log file
    write_to_log(f"API Test Results - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    write_to_log(f"Base URL: {BASE_URL}")
    write_to_log(f"Output Directory: {OUTPUT_DIR}")
    write_to_log(f"Response Files: {RESPONSE_DIR}")
    write_to_log("=" * 80)
    
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
    if os.path.exists("test_data.csv"):
        with open("test_data.csv", 'rb') as f:
            files = {'file': ('test_data.csv', f, 'text/csv')}
            test_results["upload_data"] = test_endpoint(
                "POST", "/upload/data", 
                files=files,
                description="Upload and process new data file"
            )
    else:
        write_to_log("\nSkipping file upload test - test_data.csv not found")
    
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
    
    # Print and save summary
    summary = "\n\n" + "="*80 + "\n"
    summary += "TEST SUMMARY\n"
    summary += "="*80 + "\n"
    
    success_count = sum(1 for result in test_results.values() if result)
    total_count = len(test_results)
    
    for endpoint, success in test_results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        summary += f"{endpoint}: {status}\n"
    
    summary += f"\nOverall: {success_count}/{total_count} tests passed ({success_count/total_count*100:.1f}%)\n"
    write_to_log(summary)
    
    # Save summary to a separate file for quick reference
    summary_file = os.path.join(OUTPUT_DIR, f"test_summary_{timestamp}.txt")
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(summary)
    
    write_to_log(f"Summary saved to: {summary_file}")
    write_to_log(f"All test outputs saved to: {OUTPUT_DIR}")
    write_to_log(f"API responses saved to: {RESPONSE_DIR}")

if __name__ == "__main__":
    run_all_tests()
