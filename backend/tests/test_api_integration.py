import requests
import os

# Assuming backend is running on localhost:8000
BASE_URL = "http://localhost:8000/api/v1"

def test_health():
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("Health Check: PASSED")
        else:
            print(f"Health Check: FAILED {response.status_code}")
    except Exception as e:
        print(f"Health Check: FAILED {e}")

def test_analyze_text():
    print("\nTesting Text Analysis...")
    try:
        # Simple non-medical text to trigger relevance check
        payload = {"text": "What is the capital of France?"}
        response = requests.post(f"{BASE_URL}/analyze", data=payload)
        
        data = response.json()
        if not data.get("is_relevant"):
            print("Irrelevant Text Check: PASSED (Correctly identified as irrelevant)")
        else:
            print("Irrelevant Text Check: FAILED (Should be irrelevant)")

        # Medical text
        payload_med = {"text": "Patient presents with persistent cough and hemoptysis for 3 weeks."}
        response_med = requests.post(f"{BASE_URL}/analyze", data=payload_med)
        data_med = response_med.json()
        
        if data_med.get("is_relevant"):
            print("Relevant Text Check: PASSED")
            if data_med.get("analysis"):
               print("Analysis Content: PASSED (Received analysis)")
            else:
               print("Analysis Content: FAILED (No analysis text)")
        else:
            print(f"Relevant Text Check: FAILED {data_med.get('reason')}")

    except Exception as e:
        print(f"Text Analysis Test: FAILED {e}")

if __name__ == "__main__":
    print("Starting Integration Tests...")
    test_health()
    test_analyze_text()
    # Note: Image test requires a physical file, skipping for automated script unless available.
