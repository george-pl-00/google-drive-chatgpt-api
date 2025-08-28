#!/usr/bin/env python3
"""
Interactive Demo for ChatGPT Integration with Google Drive
Test the integration by typing natural language requests
"""

from chatgpt_integration import GoogleDriveChatGPTIntegration

def main():
    """Interactive demo of the ChatGPT integration."""
    print("🚀 ChatGPT + Google Drive Integration Demo")
    print("=" * 50)
    print("Type natural language requests to create Google Drive files!")
    print("Examples:")
    print("• 'Create a Google Document called Meeting Notes'")
    print("• 'Make me a spreadsheet for tracking expenses'")
    print("• 'New Google Sheet called Project Timeline'")
    print("• Type 'quit' to exit")
    print("=" * 50)
    
    # Initialize the integration
    integration = GoogleDriveChatGPTIntegration()
    
    # Check API health first
    print("🔧 Checking Google Drive API health...")
    health = integration.check_api_health()
    print(f"Status: {health['status']}")
    print(f"Message: {health['message']}")
    
    if health["status"] != "healthy":
        print("❌ API is not available. Please start the FastAPI service first.")
        print("Run: python main.py")
        return
    
    print("✅ API is ready! Start typing your requests...\n")
    
    while True:
        try:
            # Get user input
            user_input = input("🤖 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye! Thanks for testing the integration!")
                break
            
            if not user_input:
                continue
            
            print("🔄 Processing your request...")
            
            # Process the request
            response = integration.process_chatgpt_request(user_input)
            
            print(f"📝 Assistant: {response}")
            print("-" * 50)
            
        except KeyboardInterrupt:
            print("\n👋 Demo interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Please try again or type 'quit' to exit.")

if __name__ == "__main__":
    main()

