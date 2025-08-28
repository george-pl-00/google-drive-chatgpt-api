#!/usr/bin/env python3
"""
Test script for Heroku deployment with OAuth flow
Replace YOUR_HEROKU_URL with your actual Heroku URL
"""

import requests
import json

# ⚠️  IMPORTANT: Replace this with your actual Heroku URL from the dashboard
# Go to Heroku → Your app → Settings → Domains → Copy the URL
HEROKU_URL = "https://google-drive-chatgpt-api-4f8a9bfe61b3.herokuapp.com"  # e.g., "https://your-app-name.herokuapp.com"

def test_heroku_api():
    """Test the deployed Heroku API with OAuth flow."""
    print(f"🚀 Testing Heroku API at: {HEROKU_URL}")
    print("=" * 50)
    
    # Test 1: Root endpoint (should work without auth)
    print("\n1️⃣ Testing root endpoint...")
    try:
        response = requests.get(f"{HEROKU_URL}/")
        if response.status_code == 200:
            print("✅ Root endpoint working!")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
    
    # Test 2: Health check (should show unauthenticated)
    print("\n2️⃣ Testing health endpoint...")
    try:
        response = requests.get(f"{HEROKU_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check working!")
            print(f"   Status: {data.get('status')}")
            print(f"   Google Services: {data.get('google_services')}")
            if 'error' in data:
                print(f"   Error: {data.get('error')}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
    
    # Test 3: OAuth start endpoint
    print("\n3️⃣ Testing OAuth start endpoint...")
    try:
        response = requests.get(f"{HEROKU_URL}/auth", allow_redirects=False)
        if response.status_code in [302, 303, 307, 308]:
            print("✅ OAuth redirect working!")
            print(f"   Redirect to: {response.headers.get('Location', 'Unknown')}")
        else:
            print(f"❌ OAuth redirect failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ OAuth start error: {e}")
    
    # Test 4: Protected endpoints (should require auth)
    print("\n4️⃣ Testing protected endpoints (should require auth)...")
    try:
        doc_data = {"name": "Test Document from Heroku"}
        response = requests.post(
            f"{HEROKU_URL}/create_doc",
            json=doc_data,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 401:
            print("✅ Authentication required (correct behavior)!")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Unexpected response: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Protected endpoint test error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Heroku deployment test completed!")
    print("\n📋 Next Steps:")
    print("1. Visit: " + HEROKU_URL + "/auth")
    print("2. Complete Google OAuth authentication")
    print("3. Test document/sheet creation endpoints")

if __name__ == "__main__":
    # Check if URL is still placeholder
    if "YOUR_HEROKU_URL" in HEROKU_URL:
        print("❌ Please update HEROKU_URL with your actual Heroku URL!")
        print("   Go to Heroku dashboard → Your app → Settings → Domains")
        print("   Copy the URL and replace 'YOUR_HEROKU_URL' in this script")
        print("   Example: HEROKU_URL = 'https://my-app.herokuapp.com'")
    else:
        test_heroku_api()
