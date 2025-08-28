#!/usr/bin/env python3
"""
FastAPI service for Google Drive integration
Includes endpoints for creating Google Documents and Sheets
"""

from fastapi import FastAPI, HTTPException, Request, Response, Depends, Cookie
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel
from typing import Optional
import os
import pickle
import secrets
import jwt
from datetime import datetime, timedelta
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import json

# OAuth 2.0 scopes
SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/spreadsheets"
]

# JWT secret for session management
JWT_SECRET = os.environ.get('JWT_SECRET', secrets.token_urlsafe(32))

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

def create_session_token(creds_data: dict) -> str:
    """Create a JWT token for session management."""
    payload = {
        'creds': creds_data,
        'exp': datetime.utcnow() + timedelta(hours=1)  # 1 hour expiry
    }
    return jwt.encode(payload, JWT_SECRET, algorithm='HS256')

def verify_session_token(token: str) -> Optional[dict]:
    """Verify and decode a JWT session token."""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        return payload.get('creds')
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def get_oauth_flow():
    """Create OAuth flow for web application."""
    # Check if we're in production (Heroku) or local
    if os.environ.get('HEROKU_APP_NAME'):
        # Production - use environment variables
        client_id = os.environ.get('GOOGLE_OAUTH_CLIENT_ID')
        client_secret = os.environ.get('GOOGLE_OAUTH_CLIENT_SECRET')
        redirect_uri = f"https://{os.environ.get('HEROKU_APP_NAME')}.herokuapp.com/oauth2callback"
        
        # Create flow with production credentials
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [redirect_uri]
                }
            },
            SCOPES,
            redirect_uri=redirect_uri
        )
    else:
        # Local development - use oauth_credentials.json
        if not os.path.exists('oauth_credentials.json'):
            raise HTTPException(
                status_code=500, 
                detail="oauth_credentials.json not found! Please ensure you have the OAuth credentials file."
            )
        
        flow = Flow.from_client_secrets_file(
            'oauth_credentials.json', 
            SCOPES,
            redirect_uri='http://localhost:3333/oauth2callback'
        )
    
    return flow

def authenticate_google_services(request: Request, session_token: Optional[str] = Cookie(None)):
    """Authenticate with Google services using OAuth 2.0."""
    global drive_service, docs_service
    
    # Check if we have valid credentials in session token
    if session_token:
        creds_data = verify_session_token(session_token)
        if creds_data:
            try:
                # Try to use stored credentials
                from google.oauth2.credentials import Credentials
                
                creds = Credentials(
                    token=creds_data['token'],
                    refresh_token=creds_data.get('refresh_token'),
                    token_uri=creds_data['token_uri'],
                    client_id=creds_data['client_id'],
                    client_secret=creds_data.get('client_secret'),
                    scopes=creds_data['scopes']
                )
                
                # Check if credentials are valid
                if creds and creds.valid:
                    # Build services with valid credentials
                    drive_service = build("drive", "v3", credentials=creds)
                    docs_service = build("docs", "v1", credentials=creds)
                    return drive_service, docs_service
                elif creds and creds.expired and creds.refresh_token:
                    # Refresh expired credentials
                    creds.refresh(Request())
                    # Update session with new token
                    new_creds_data = {
                        'token': creds.token,
                        'refresh_token': creds.refresh_token,
                        'token_uri': creds.token_uri,
                        'client_id': creds.client_id,
                        'client_secret': creds.client_secret,
                        'scopes': creds.scopes
                    }
                    
                    # Build services with refreshed credentials
                    drive_service = build("drive", "v3", credentials=creds)
                    docs_service = build("docs", "v1", credentials=creds)
                    return drive_service, docs_service
                    
            except Exception as e:
                # Clear invalid credentials
                pass
    
    # No valid credentials - need to authenticate
    raise HTTPException(
        status_code=401,
        detail="Google authentication required. Please visit /auth to authenticate."
    )

@app.get("/auth")
async def start_oauth_flow():
    """Start OAuth 2.0 flow."""
    try:
        flow = get_oauth_flow()
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )
        
        return RedirectResponse(url=authorization_url)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to start OAuth flow: {str(e)}"
        )

@app.get("/oauth2callback")
async def oauth2_callback(code: str, state: str):
    """Handle OAuth 2.0 callback."""
    try:
        # Get the flow
        flow = get_oauth_flow()
        flow.fetch_token(code=code)
        
        # Get credentials
        creds = flow.credentials
        
        # Create session token
        creds_data = {
            'token': creds.token,
            'refresh_token': creds.refresh_token,
            'token_uri': creds.token_uri,
            'client_id': creds.client_id,
            'client_secret': creds.client_secret,
            'scopes': creds.scopes
        }
        
        session_token = create_session_token(creds_data)
        
        # Create response with cookie
        response = JSONResponse(content={
            "message": "Authentication successful!",
            "status": "authenticated"
        })
        
        # Set cookie with session token
        response.set_cookie(
            key="session_token",
            value=session_token,
            httponly=True,
            secure=os.environ.get('HEROKU_APP_NAME') is not None,  # HTTPS only in production
            max_age=3600  # 1 hour
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"OAuth callback failed: {str(e)}"
        )

@app.get("/logout")
async def logout():
    """Clear authentication session."""
    response = JSONResponse(content={"message": "Logged out successfully"})
    response.delete_cookie(key="session_token")
    return response

@app.on_event("startup")
async def startup_event():
    """Initialize FastAPI app on startup."""
    print("✅ FastAPI app started successfully!")
    print("🌐 OAuth web flow is ready for authentication")

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Google Drive Integration API",
        "version": "1.0.0",
        "endpoints": {
            "auth": "GET /auth - Start OAuth authentication",
            "oauth2callback": "GET /oauth2callback - OAuth callback (handled automatically)",
            "logout": "GET /logout - Clear authentication",
            "create_doc": "POST /create_doc - Create a Google Document",
            "create_sheet": "POST /create_sheet - Create a Google Sheet"
        }
    }

@app.post("/create_doc")
async def create_doc(request: DocumentRequest, http_request: Request = Depends()):
    """Create a Google Document in Drive."""
    try:
        # Ensure services are authenticated
        drive_service, docs_service = authenticate_google_services(http_request)
        
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
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to create document: {str(e)}"
        )

@app.post("/create_sheet")
async def create_sheet(request: SheetRequest, http_request: Request = Depends()):
    """Create a Google Sheet in Drive."""
    try:
        # Ensure services are authenticated
        drive_service, docs_service = authenticate_google_services(http_request)
        
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
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to create sheet: {str(e)}"
        )

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "API is running"}

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 3333))
    uvicorn.run(app, host="0.0.0.0", port=port)
