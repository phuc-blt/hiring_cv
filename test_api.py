#!/usr/bin/env python3
"""
Simple API test script to verify the API endpoints work correctly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.api import app
from fastapi.testclient import TestClient

def test_api_endpoints():
    """Test all API endpoints"""
    client = TestClient(app)
    
    print("🧪 Testing API Endpoints...")
    
    # Test health check
    print("\n1. Testing health check...")
    response = client.get("/api/health")
    if response.status_code == 200:
        print("✅ Health check passed")
        print(f"Response: {response.json()}")
    else:
        print(f"❌ Health check failed: {response.status_code}")
    
    # Test JD creation
    print("\n2. Testing JD creation...")
    jd_data = {
        "jobTitle": "Frontend Developer",
        "department": "Technology",
        "location": "Hanoi",
        "jobType": "full-time",
        "experience": "mid",
        "salary": "20-30 million VND",
        "description": "We are looking for a skilled frontend developer...",
        "requirements": ["React", "TypeScript", "3+ years experience"],
        "benefits": ["Health insurance", "Flexible working hours"],
        "platforms": ["linkedin", "indeed"]
    }
    
    response = client.post("/api/jd/create", json=jd_data)
    if response.status_code == 200:
        print("✅ JD creation passed")
        print(f"Response: {response.json()}")
    else:
        print(f"❌ JD creation failed: {response.status_code}")
        print(f"Error: {response.text}")
    
    # Test application submission (simulated)
    print("\n3. Testing application submission...")
    # Note: This would normally include file upload, but we'll test the structure
    from io import BytesIO
    
    # Create a mock file
    mock_file = BytesIO(b"mock cv content")
    mock_file.name = "test_cv.pdf"
    mock_file.content_type = "application/pdf"
    
    files = {"cvFile": ("test_cv.pdf", mock_file, "application/pdf")}
    data = {
        "fullName": "John Doe",
        "email": "john@example.com",
        "phone": "0912345678",
        "address": "Hanoi, Vietnam",
        "position": "Frontend Developer",
        "experience": "3-5",
        "coverLetter": "I am a skilled frontend developer with 3 years of experience...",
        "portfolio": "https://johndoe.dev",
        "expectedSalary": "20-25 million VND",
        "availability": "1 month"
    }
    
    response = client.post("/api/apply/submit", files=files, data=data)
    if response.status_code == 200:
        print("✅ Application submission passed")
        print(f"Response: {response.json()}")
    else:
        print(f"❌ Application submission failed: {response.status_code}")
        print(f"Error: {response.text}")
    
    # Test CV evaluation
    print("\n4. Testing CV evaluation...")
    cv_data = {
        "cv_content": "John Doe - Frontend Developer with 3 years experience in React, TypeScript, and Node.js...",
        "role": "Frontend Developer",
        "company_context": "Technology company looking for mid-level frontend developer"
    }
    
    response = client.post("/api/evaluate/cv", json=cv_data)
    if response.status_code == 200:
        print("✅ CV evaluation passed")
        result = response.json()
        print(f"Skills analysis: {list(result.keys())}")
    else:
        print(f"❌ CV evaluation failed: {response.status_code}")
        print(f"Error: {response.text}")
    
    # Test candidates list
    print("\n5. Testing candidates list...")
    response = client.get("/api/candidates/list")
    if response.status_code == 200:
        print("✅ Candidates list passed")
        candidates = response.json()
        print(f"Found {len(candidates)} candidates")
    else:
        print(f"❌ Candidates list failed: {response.status_code}")
    
    print("\n🎉 API testing completed!")

if __name__ == "__main__":
    test_api_endpoints()
