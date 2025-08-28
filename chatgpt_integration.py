#!/usr/bin/env python3
"""
ChatGPT Integration with Google Drive API
Allows ChatGPT to create Google Documents and Sheets via natural language
"""

import requests
import re
import os
from typing import Dict, Any, Optional

class GoogleDriveChatGPTIntegration:
    """
    Integration class for ChatGPT to interact with Google Drive API
    Automatically detects local vs cloud deployment
    """
    
    def __init__(self):
        """Initialize the integration with automatic URL detection."""
        # Check if we're in Railway (cloud) or local
        railway_url = os.environ.get('RAILWAY_URL')
        if railway_url:
            self.api_base_url = railway_url
            print(f"🌐 Using Railway deployment: {railway_url}")
        else:
            # Local development
            self.api_base_url = "http://localhost:3333"
            print(f"🏠 Using local development: {self.api_base_url}")
    
    def check_api_health(self) -> bool:
        """Check if the API is healthy and accessible."""
        try:
            response = requests.get(f"{self.api_base_url}/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ API Health: {data.get('status', 'unknown')}")
                print(f"🔗 Google Services: {data.get('google_services', 'unknown')}")
                return True
            else:
                print(f"❌ API Health Check Failed: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ API Connection Error: {e}")
            return False
    
    def create_google_document(self, name: str) -> Dict[str, Any]:
        """Create a Google Document via the API."""
        try:
            response = requests.post(
                f"{self.api_base_url}/create_doc",
                json={"name": name},
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Document created successfully!")
                print(f"📄 Name: {result.get('name')}")
                print(f"🔗 Link: {result.get('link')}")
                print(f"🆔 ID: {result.get('docId')}")
                return result
            else:
                print(f"❌ Failed to create document: {response.status_code}")
                print(f"📝 Response: {response.text}")
                return {"success": False, "error": response.text}
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
            return {"success": False, "error": str(e)}
    
    def create_google_sheet(self, name: str) -> Dict[str, Any]:
        """Create a Google Sheet via the API."""
        try:
            response = requests.post(
                f"{self.api_base_url}/create_sheet",
                json={"name": name},
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Sheet created successfully!")
                print(f"📊 Name: {result.get('name')}")
                print(f"🔗 Link: {result.get('link')}")
                print(f"🆔 ID: {result.get('sheetId')}")
                return result
            else:
                print(f"❌ Failed to create sheet: {response.status_code}")
                print(f"📝 Response: {response.text}")
                return {"success": False, "error": response.text}
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
            return {"success": False, "error": str(e)}
    
    def parse_user_request(self, user_message: str) -> Optional[Dict[str, Any]]:
        """
        Parse natural language user request to determine action.
        Returns action details or None if no action detected.
        """
        user_message = user_message.lower().strip()
        
        # Patterns for creating Google Documents
        doc_patterns = [
            r"create\s+(?:a\s+)?(?:google\s+)?(?:doc|document)(?:\s+called\s+|\s+named\s+|\s+titled\s+)?['\"]?([^'\"]+)['\"]?",
            r"make\s+(?:me\s+)?(?:a\s+)?(?:google\s+)?(?:doc|document)(?:\s+called\s+|\s+named\s+|\s+titled\s+)?['\"]?([^'\"]+)['\"]?",
            r"new\s+(?:google\s+)?(?:doc|document)(?:\s+called\s+|\s+named\s+|\s+titled\s+)?['\"]?([^'\"]+)['\"]?",
            r"generate\s+(?:a\s+)?(?:google\s+)?(?:doc|document)(?:\s+called\s+|\s+named\s+|\s+titled\s+)?['\"]?([^'\"]+)['\"]?"
        ]
        
        # Patterns for creating Google Sheets
        sheet_patterns = [
            r"create\s+(?:a\s+)?(?:google\s+)?(?:sheet|spreadsheet)(?:\s+called\s+|\s+named\s+|\s+titled\s+)?['\"]?([^'\"]+)['\"]?",
            r"make\s+(?:me\s+)?(?:a\s+)?(?:google\s+)?(?:sheet|spreadsheet)(?:\s+called\s+|\s+named\s+|\s+titled\s+)?['\"]?([^'\"]+)['\"]?",
            r"new\s+(?:google\s+)?(?:sheet|spreadsheet)(?:\s+called\s+|\s+named\s+|\s+titled\s+)?['\"]?([^'\"]+)['\"]?",
            r"generate\s+(?:a\s+)?(?:google\s+)?(?:sheet|spreadsheet)(?:\s+called\s+|\s+named\s+|\s+titled\s+)?['\"]?([^'\"]+)['\"]?"
        ]
        
        # Check for document creation requests
        for pattern in doc_patterns:
            match = re.search(pattern, user_message)
            if match:
                doc_name = match.group(1).strip()
                return {
                    "action": "create_document",
                    "name": doc_name,
                    "type": "Google Document"
                }
        
        # Check for sheet creation requests
        for pattern in sheet_patterns:
            match = re.search(pattern, user_message)
            if match:
                sheet_name = match.group(1).strip()
                return {
                    "action": "create_sheet",
                    "name": sheet_name,
                    "type": "Google Sheet"
                }
        
        return None
    
    def process_chat_request(self, user_message: str) -> str:
        """
        Process a chat request and return a response.
        This is the main method ChatGPT would call.
        """
        print(f"🤖 Processing request: {user_message}")
        
        # Check API health first
        if not self.check_api_health():
            return "❌ Sorry, the Google Drive API is currently unavailable. Please try again later."
        
        # Parse the user request
        action = self.parse_user_request(user_message)
        
        if not action:
            return "❓ I didn't understand that request. Try saying something like 'Create a Google Document called Meeting Notes' or 'Make me a spreadsheet for tracking expenses'."
        
        # Execute the action
        if action["action"] == "create_document":
            result = self.create_google_document(action["name"])
            if result.get("success"):
                return f"✅ I've created a Google Document called '{action['name']}' for you!\n🔗 You can access it here: {result.get('link')}"
            else:
                return f"❌ Sorry, I couldn't create the document. Error: {result.get('error', 'Unknown error')}"
        
        elif action["action"] == "create_sheet":
            result = self.create_google_sheet(action["name"])
            if result.get("success"):
                return f"✅ I've created a Google Sheet called '{action['name']}' for you!\n🔗 You can access it here: {result.get('link')}"
            else:
                return f"❌ Sorry, I couldn't create the sheet. Error: {result.get('error', 'Unknown error')}"
        
        return "❓ Something went wrong. Please try again."

# Example usage for testing
if __name__ == "__main__":
    integration = GoogleDriveChatGPTIntegration()
    
    # Test the integration
    test_requests = [
        "Create a Google Document called Test Document",
        "Make me a spreadsheet for tracking expenses",
        "New Google Sheet called Project Timeline"
    ]
    
    for request in test_requests:
        print(f"\n🧪 Testing: {request}")
        response = integration.process_chat_request(request)
        print(f"📝 Response: {response}")
        print("-" * 50)
