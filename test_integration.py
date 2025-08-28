#!/usr/bin/env python3
"""
Simple test script to verify OAuth setup and Google Drive access.
"""

from google_drive_integration import authenticate_google_services

def test_basic_functionality():
    """Test basic OAuth and Google Drive functionality."""
    print("🧪 Testing Google Drive API Integration")
    print("=" * 45)
    
    # Test authentication
    print("🔧 Testing authentication...")
    drive_service, docs_service = authenticate_google_services()
    
    if not drive_service or not docs_service:
        print("❌ Authentication failed!")
        return False
    
    print("✅ Authentication successful!")
    
    # Test Drive access
    try:
        print("\n📁 Testing Google Drive access...")
        about = drive_service.about().get(fields="user").execute()
        user_info = about.get("user", {})
        
        print(f"👤 Connected as: {user_info.get('displayName', 'Unknown')}")
        print(f"📧 Email: {user_info.get('emailAddress', 'Unknown')}")
        
        # List a few files
        files = drive_service.files().list(pageSize=3, fields="files(id,name,mimeType)").execute()
        file_list = files.get("files", [])
        
        if file_list:
            print(f"\n📄 Found {len(file_list)} files in Drive:")
            for file in file_list:
                print(f"   • {file.get('name', 'Unknown')}")
        else:
            print("\n📄 No files found in Drive (this is normal)")
        
        print("\n🎉 All tests passed! Your integration is ready.")
        return True
        
    except Exception as e:
        print(f"❌ Drive access test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Google Drive Integration Test")
    print("=" * 35)
    
    success = test_basic_functionality()
    
    if success:
        print("\n✨ Ready to create documents!")
        print("💡 Run: python google_drive_integration.py")
    else:
        print("\n❌ Setup incomplete. Please check your OAuth configuration.")
