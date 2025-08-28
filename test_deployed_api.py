#!/usr/bin/env python3
"""
Test script for deployed Railway API
Run this after deployment to verify everything works
"""

import requests
import json
import sys

def test_deployed_api(base_url):
    """Test all endpoints of the deployed API."""
    print(f"🧪 Testing deployed API at: {base_url}")
    print("=" * 50)
    
    # Test 1: Health endpoint
    print("1️⃣ Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health check passed!")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False
    
    # Test 2: Root endpoint
    print("\n2️⃣ Testing root endpoint...")
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            print("✅ Root endpoint working!")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
    
    # Test 3: Create document
    print("\n3️⃣ Testing document creation...")
    try:
        payload = {"name": "Test Document from Deployed API"}
        response = requests.post(
            f"{base_url}/create_doc",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Document created successfully!")
            print(f"   Document ID: {result.get('docId')}")
            print(f"   Link: {result.get('link')}")
            print(f"   Name: {result.get('name')}")
        else:
            print(f"❌ Document creation failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Document creation error: {e}")
        return False
    
    # Test 4: Create sheet
    print("\n4️⃣ Testing sheet creation...")
    try:
        payload = {"name": "Test Sheet from Deployed API"}
        response = requests.post(
            f"{base_url}/create_sheet",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Sheet created successfully!")
            print(f"   Sheet ID: {result.get('sheetId')}")
            print(f"   Link: {result.get('link')}")
            print(f"   Name: {result.get('name')}")
        else:
            print(f"❌ Sheet creation failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Sheet creation error: {e}")
        return False
    
    print("\n🎉 All tests passed! Your API is working correctly!")
    return True

def main():
    """Main test function."""
    if len(sys.argv) != 2:
        print("Usage: python test_deployed_api.py <your-railway-url>")
        print("Example: python test_deployed_api.py https://my-app.railway.app")
        sys.exit(1)
    
    base_url = sys.argv[1].rstrip('/')
    
    # Validate URL format
    if not base_url.startswith(('http://', 'https://')):
        print("❌ Please provide a valid URL starting with http:// or https://")
        sys.exit(1)
    
    print("🚀 Testing Deployed Railway API")
    print("=" * 40)
    
    success = test_deployed_api(base_url)
    
    if success:
        print("\n✅ Your API is ready for ChatGPT integration!")
        print(f"🔗 Use this URL in your ChatGPT integration: {base_url}")
        print("\n📝 Next steps:")
        print("1. Update chatgpt_integration.py with the new URL")
        print("2. Test with ChatGPT API or create a plugin")
        print("3. Enjoy creating Google Drive files from anywhere!")
    else:
        print("\n❌ Some tests failed. Please check your deployment.")
        print("📚 See QUICK_DEPLOY.md for troubleshooting steps")

if __name__ == "__main__":
    main()


