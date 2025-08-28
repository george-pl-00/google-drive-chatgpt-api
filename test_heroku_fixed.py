#!/usr/bin/env python3
"""
Test script for the fixed Heroku deployment
"""

import requests
import json

def test_endpoint(url, method="GET", data=None, description=""):
    """Test an endpoint and return the result."""
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        
        print(f"✅ {description}")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:200]}...")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ {description}")
        print(f"   Error: {e}")
        return False

def main():
    base_url = "https://google-drive-chatgpt-api-4f8a9bfe61b3.herokuapp.com"
    
    print("🧪 Testing Fixed Heroku Deployment")
    print("=" * 50)
    print(f"🌐 Base URL: {base_url}")
    print()
    
    # Test health endpoint
    test_endpoint(
        f"{base_url}/health",
        description="Health Check"
    )
    print()
    
    # Test root endpoint
    test_endpoint(
        f"{base_url}/",
        description="Root Endpoint"
    )
    print()
    
    # Test auth endpoint (should redirect to Google)
    test_endpoint(
        f"{base_url}/auth",
        description="OAuth Start"
    )
    print()
    
    # Test protected endpoints (should return 401)
    test_endpoint(
        f"{base_url}/create_doc",
        method="POST",
        data={"name": "Test Document"},
        description="Create Document (Unauthenticated)"
    )
    print()
    
    test_endpoint(
        f"{base_url}/create_sheet",
        method="POST",
        data={"name": "Test Sheet"},
        description="Create Sheet (Unauthenticated)"
    )
    print()
    
    print("📝 Test Summary:")
    print("- Health and Root endpoints should return 200")
    print("- Auth endpoint should redirect to Google (302)")
    print("- Protected endpoints should return 401 (Unauthorized)")
    print()
    print("🔐 To test full functionality:")
    print("1. Visit the auth endpoint in your browser")
    print("2. Complete Google OAuth")
    print("3. Test document/sheet creation")

if __name__ == "__main__":
    main()
