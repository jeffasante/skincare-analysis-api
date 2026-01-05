"""
Simple test script for the Skincare Analysis API
"""
import requests
import json

API_URL = "http://localhost:8000"
API_KEY = "dev-api-key-12345"

def test_health():
    """Test health endpoint (no auth required)"""
    print("🔍 Testing health endpoint...")
    response = requests.get(f"{API_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_upload_and_analyze(image_path):
    """Test upload and analysis endpoints"""
    headers = {"X-API-Key": API_KEY}
    
    # Upload image
    print(f"Uploading image: {image_path}")
    try:
        with open(image_path, "rb") as f:
            files = {"file": f}
            response = requests.post(
                f"{API_URL}/upload",
                headers=headers,
                files=files
            )
        
        if response.status_code == 200:
            upload_data = response.json()
            print(f"Upload successful!")
            print(f"Response: {json.dumps(upload_data, indent=2)}\n")
            
            # Analyze image
            image_id = upload_data["image_id"]
            print(f"🔬 Analyzing image with ID: {image_id}")
            
            analyze_response = requests.post(
                f"{API_URL}/analyze",
                headers=headers,
                json={"image_id": image_id}
            )
            
            if analyze_response.status_code == 200:
                analysis_data = analyze_response.json()
                print(f"Analysis successful!")
                print(f"Response: {json.dumps(analysis_data, indent=2)}\n")
            else:
                print(f"Analysis failed: {analyze_response.status_code}")
                print(f"Error: {analyze_response.text}\n")
        else:
            print(f"Upload failed: {response.status_code}")
            print(f"Error: {response.text}\n")
            
    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}\n")
    except Exception as e:
        print(f"Error: {str(e)}\n")

if __name__ == "__main__":
    print("=" * 60)
    print("Skincare Analysis API - Test Script")
    print("=" * 60 + "\n")
    
    # Test health
    test_health()
    
    # Test upload and analyze with test image
    test_image = "/Users/jeff/Desktop/veefyed-backend/test_images/test_skin_medium.jpg"
    test_upload_and_analyze(test_image)
