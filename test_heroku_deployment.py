#!/usr/bin/env python3
"""
Test script for Heroku deployment
Replace YOUR_HEROKU_URL with your actual Heroku URL
"""

import requests
import json

# ⚠️  IMPORTANT: Replace this with your actual Heroku URL from the dashboard
# Go to Heroku → Your app → Settings → Domains → Copy the URL
HEROKU_URL = "YOUR_HEROKU_URL"  # e.g., "https://your-app-name.herokuapp.com"

def test_heroku_api():
    """Test the deployed Heroku API."""
    print(f"🚀 Testing Heroku API at: {HEROKU_URL}")
    print("=" * 50)
    
    # Test 1: Health check
    print("\n1️⃣ Testing health endpoint...")
    try:
        response = requests.get(f"{HEROKU_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed!")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
    
    # Test 2: Root endpoint
    print("\n2️⃣ Testing root endpoint...")
    try:
        response = requests.get(f"{HEROKU_URL}/")
        if response.status_code == 200:
            print("✅ Root endpoint working!")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
    
    # Test 3: Create document endpoint
    print("\n3️⃣ Testing create document endpoint...")
    try:
        doc_data = {"name": "Test Document from Heroku"}
        response = requests.post(
            f"{HEROKU_URL}/create_doc",
            json=doc_data,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            print("✅ Document creation working!")
            result = response.json()
            print(f"   Document ID: {result.get('docId')}")
            print(f"   Document Link: {result.get('link')}")
        else:
            print(f"❌ Document creation failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Document creation error: {e}")
    
    # Test 4: Create sheet endpoint
    print("\n4️⃣ Testing create sheet endpoint...")
    try:
        sheet_data = {"name": "Test Sheet from Heroku"}
        response = requests.post(
            f"{HEROKU_URL}/create_sheet",
            json=sheet_data,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            print("✅ Sheet creation working!")
            result = response.json()
            print(f"   Sheet ID: {result.get('sheetId')}")
            print(f"   Sheet Link: {result.get('link')}")
        else:
            print(f"❌ Sheet creation failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Sheet creation error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Heroku deployment test completed!")

if __name__ == "__main__":
    if HEROKU_URL == "YOUR_HEROKU_URL":
        print("❌ Please update HEROKU_URL with your actual Heroku URL!")
        print("   Go to Heroku dashboard → Your app → Settings → Domains")
        print("   Copy the URL and replace 'YOUR_HEROKU_URL' in this script")
        print("   Example: HEROKU_URL = 'https://my-app.herokuapp.com'")
    else:
        test_heroku_api()
