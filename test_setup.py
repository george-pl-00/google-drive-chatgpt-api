#!/usr/bin/env python3
"""
Test script for Google Drive Chat Application
Verifies that all components are properly configured
"""

import os
import sys
import importlib

def test_imports():
    """Test if all required modules can be imported."""
    print("🔍 Testing imports...")
    
    required_modules = [
        'flask',
        'flask_cors', 
        'google_auth_oauthlib',
        'google.auth.transport.requests',
        'googleapiclient.discovery',
        'openai',
        'dotenv'
    ]
    
    failed_imports = []
    
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n❌ Failed to import: {', '.join(failed_imports)}")
        print("Please run: pip install -r requirements.txt")
        return False
    
    print("✅ All imports successful!")
    return True

def test_configuration():
    """Test configuration files and settings."""
    print("\n🔍 Testing configuration...")
    
    # Check .env file
    if os.path.exists(".env"):
        print("✅ .env file exists")
        
        # Test loading environment variables
        try:
            from dotenv import load_dotenv
            load_dotenv()
            
            openai_key = os.getenv("OPENAI_API_KEY")
            if openai_key and not openai_key.startswith("sk-your"):
                print("✅ OpenAI API key configured")
            else:
                print("❌ OpenAI API key not properly configured")
                return False
                
        except Exception as e:
            print(f"❌ Error loading .env file: {e}")
            return False
    else:
        print("❌ .env file not found")
        print("   Copy env_example.txt to .env and configure your API keys")
        return False
    
    # Check OAuth credentials
    if os.path.exists("oauth_credentials.json"):
        print("✅ OAuth credentials file exists")
    else:
        print("❌ OAuth credentials file not found")
        print("   Please download from Google Cloud Console")
        return False
    
    # Check main application file
    if os.path.exists("webdrive.py"):
        print("✅ Main application file exists")
    else:
        print("❌ Main application file not found")
        return False
    
    # Check HTML template
    if os.path.exists("templates/chat.html"):
        print("✅ HTML template exists")
    else:
        print("❌ HTML template not found")
        return False
    
    print("✅ Configuration looks good!")
    return True

def test_google_auth():
    """Test Google authentication setup."""
    print("\n🔍 Testing Google authentication...")
    
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build
        
        # Test if we can read OAuth credentials
        if os.path.exists("oauth_credentials.json"):
            print("✅ OAuth credentials file readable")
            
            # Test if we can create a flow (without running it)
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'oauth_credentials.json', 
                    ['https://www.googleapis.com/auth/drive']
                )
                print("✅ OAuth flow can be created")
            except Exception as e:
                print(f"❌ OAuth flow creation failed: {e}")
                return False
        else:
            print("❌ OAuth credentials file not found")
            return False
            
    except Exception as e:
        print(f"❌ Google authentication test failed: {e}")
        return False
    
    print("✅ Google authentication setup looks good!")
    return False

def main():
    """Run all tests."""
    print("🚀 Google Drive Chat - Setup Test")
    print("=" * 40)
    print()
    
    tests = [
        ("Import Test", test_imports),
        ("Configuration Test", test_configuration),
        ("Google Auth Test", test_google_auth)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name}...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with error: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 40)
    print("📊 Test Results Summary:")
    print("=" * 40)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your setup is ready.")
        print("Run 'python webdrive.py' to start the application.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please fix the issues above.")
        print("Check the README.md for setup instructions.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
