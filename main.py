#!/usr/bin/env python3
"""
FastAPI service for Google Drive integration
Includes endpoints for creating Google Documents and Sheets
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# OAuth 2.0 scopes
SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/spreadsheets"
]

# Initialize FastAPI app
app = FastAPI(
    title="Google Drive Integration API",
    description="API for creating Google Documents and Sheets",
    version="1.0.0"
)

# Global services
drive_service = None
docs_service = None

class DocumentRequest(BaseModel):
    name: str = "Test Document"

class SheetRequest(BaseModel):
    name: str = "Test Sheet"

def authenticate_google_services():
    """Authenticate with Google services using OAuth 2.0."""
    global drive_service, docs_service
    
    if drive_service and docs_service:
        return drive_service, docs_service
    
    creds = None
    
    # Check if we have valid credentials
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # If no valid credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Check if we're in Railway (production) or local
            if os.environ.get('RAILWAY_ENVIRONMENT'):
                # Railway deployment - use environment variables
                client_id = os.environ.get('GOOGLE_OAUTH_CLIENT_ID')
                client_secret = os.environ.get('GOOGLE_OAUTH_CLIENT_SECRET')
                
                if not client_id or not client_secret:
                    raise HTTPException(
                        status_code=500,
                        detail="Missing Google OAuth environment variables in Railway"
                    )
                
                # For Railway, we'll need to handle OAuth differently
                # This is a simplified approach - you may need to implement
                # a proper OAuth flow for production
                raise HTTPException(
                    status_code=500,
                    detail="OAuth flow not yet implemented for Railway deployment"
                )
            else:
                # Local development - use oauth_credentials.json
                if not os.path.exists('oauth_credentials.json'):
                    raise HTTPException(
                        status_code=500, 
                        detail="oauth_credentials.json not found! Please ensure you have the OAuth credentials file."
                    )
                
                try:
                    # Use InstalledAppFlow for local development
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'oauth_credentials.json', SCOPES)
                    creds = flow.run_local_server(port=0)
                    
                    # Save the credentials for the next run
                    with open('token.pickle', 'wb') as token:
                        pickle.dump(creds, token)
                    
                except Exception as e:
                    raise HTTPException(
                        status_code=500, 
                        detail=f"OAuth authentication failed: {str(e)}"
                    )
    
    # Build services
    try:
        drive_service = build("drive", "v3", credentials=creds)
        docs_service = build("docs", "v1", credentials=creds)
        return drive_service, docs_service
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error building services: {str(e)}"
        )

@app.on_event("startup")
async def startup_event():
    """Initialize Google services on startup."""
    try:
        authenticate_google_services()
        print("✅ Google services initialized successfully!")
    except Exception as e:
        print(f"❌ Failed to initialize Google services: {e}")

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Google Drive Integration API",
        "version": "1.0.0",
        "endpoints": {
            "create_doc": "POST /create_doc - Create a Google Document",
            "create_sheet": "POST /create_sheet - Create a Google Sheet"
        }
    }

@app.post("/create_doc")
async def create_doc(request: DocumentRequest):
    """Create a Google Document in Drive."""
    try:
        # Ensure services are authenticated
        drive_service, docs_service = authenticate_google_services()
        
        # 1. Create the Google Doc file in Drive
        file_metadata = {
            "name": request.name,
            "mimeType": "application/vnd.google-apps.document",
            "parents": ["root"]  # or a folder ID if you want
        }
        
        file = drive_service.files().create(
            body=file_metadata,
            fields="id, webViewLink"
        ).execute()

        return JSONResponse(content={
            "success": True,
            "docId": file["id"],
            "link": file["webViewLink"],
            "name": request.name,
            "message": f"Google Document '{request.name}' created successfully!"
        })
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to create document: {str(e)}"
        )

@app.post("/create_sheet")
async def create_sheet(request: SheetRequest):
    """Create a Google Sheet in Drive."""
    try:
        # Ensure services are authenticated
        drive_service, docs_service = authenticate_google_services()
        
        # Create empty Google Sheet
        file_metadata = {
            'name': request.name,
            'mimeType': 'application/vnd.google-apps.spreadsheet'
        }
        
        file = drive_service.files().create(
            body=file_metadata,
            fields='id,name,webViewLink'
        ).execute()
        
        sheet_id = file.get('id')
        sheet_name = file.get('name')
        sheet_link = file.get('webViewLink')
        
        return JSONResponse(content={
            "success": True,
            "sheetId": sheet_id,
            "name": sheet_name,
            "link": sheet_link,
            "message": f"Google Sheet '{request.name}' created successfully!"
        })
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to create sheet: {str(e)}"
        )

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        # Test Google services
        authenticate_google_services()
        return {"status": "healthy", "google_services": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "google_services": "disconnected", "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 3333))
    uvicorn.run(app, host="0.0.0.0", port=port)
