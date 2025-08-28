# 🚀 ChatGPT + Google Drive Integration

This system allows ChatGPT to automatically create Google Documents and Sheets in your Google Drive through natural language requests.

## ✨ Features

- **Natural Language Processing**: Understands requests like "Create a Google Document called Meeting Notes"
- **Automatic File Creation**: Creates files directly in your Google Drive
- **Real-time Links**: Provides direct links to created files
- **Smart Pattern Matching**: Recognizes various ways to request file creation
- **Health Monitoring**: Checks API status and Google services connectivity

## 🏗️ Architecture

```
User Request → ChatGPT Integration → FastAPI Service → Google Drive API → File Created
```

## 📋 Prerequisites

1. **Google OAuth Setup**: `oauth_credentials.json` file
2. **Python Dependencies**: All packages in `requirements.txt`
3. **Google Drive API**: Enabled in Google Cloud Console

## 🚀 Quick Start

### 1. Start the Google Drive API Service

```bash
python main.py
```

The service will run on `http://localhost:3333` and authenticate with Google.

### 2. Test the Integration

```bash
python demo_chatgpt_integration.py
```

This starts an interactive demo where you can type natural language requests.

## 💬 How to Use

### Natural Language Examples

**Create Google Documents:**
- "Create a Google Document called Project Notes"
- "Make me a document for meeting minutes"
- "New Google Document called Daily Journal"

**Create Google Sheets:**
- "Create a Google Sheet called Budget Tracker"
- "Make me a spreadsheet for tracking expenses"
- "New Google Sheet called Project Timeline"

### API Endpoints

- **POST** `/create_doc` - Create Google Documents
- **POST** `/create_sheet` - Create Google Sheets
- **GET** `/health` - Check API status
- **GET** `/` - API information

## 🔧 Integration with ChatGPT

### Method 1: Direct API Calls

ChatGPT can call the API endpoints directly:

```python
import requests

# Create a document
response = requests.post("http://localhost:3333/create_doc", 
                        json={"name": "Meeting Notes"})

# Create a sheet
response = requests.post("http://localhost:3333/create_sheet", 
                        json={"name": "Budget Tracker"})
```

### Method 2: Use the Integration Class

```python
from chatgpt_integration import GoogleDriveChatGPTIntegration

integration = GoogleDriveChatGPTIntegration()

# Process natural language requests
response = integration.process_chatgpt_request(
    "Create a Google Document called Project Notes"
)
print(response)
```

## 📁 File Structure

```
├── main.py                          # FastAPI service
├── chatgpt_integration.py          # ChatGPT integration logic
├── demo_chatgpt_integration.py     # Interactive demo
├── google_drive_integration.py     # Google Drive API functions
├── requirements.txt                 # Python dependencies
├── oauth_credentials.json          # Google OAuth credentials
└── token.pickle                    # Stored authentication token
```

## 🧪 Testing

### Test API Health
```bash
curl http://localhost:3333/health
```

### Test Document Creation
```bash
curl -X POST "http://localhost:3333/create_doc" \
     -H "Content-Type: application/json" \
     -d '{"name": "Test Document"}'
```

### Test Sheet Creation
```bash
curl -X POST "http://localhost:3333/create_sheet" \
     -H "Content-Type: application/json" \
     -d '{"name": "Test Sheet"}'
```

## 🔐 Authentication

The system uses OAuth 2.0 for Google Drive access:

1. **First Run**: Browser opens for Google authentication
2. **Subsequent Runs**: Uses stored `token.pickle` file
3. **Token Refresh**: Automatically handles expired tokens

## 🚨 Troubleshooting

### Common Issues

1. **"uvicorn not found"**
   ```bash
   python -m pip install uvicorn[standard]
   ```

2. **"Google services not connected"**
   - Check `oauth_credentials.json` exists
   - Verify Google Drive API is enabled
   - Check internet connection

3. **"Port 3333 already in use"**
   ```bash
   # Kill existing process
   netstat -ano | findstr :3333
   taskkill /PID <PID> /F
   ```

### Debug Mode

Start the service with debug logging:
```bash
python -m uvicorn main:app --reload --port 3333 --log-level debug
```

## 🔄 Advanced Usage

### Custom File Names

The system extracts file names from natural language:
- "Create a document called **My Project**" → File: "My Project"
- "Make me a sheet for **Budget 2025**" → File: "Budget 2025"

### Pattern Matching

Supports various request formats:
- "Create a Google Document called..."
- "Make me a spreadsheet for..."
- "New Google Sheet called..."
- "Google Document called..."

### Error Handling

- API connectivity issues
- Google authentication problems
- Invalid file names
- Rate limiting

## 📈 Future Enhancements

- [ ] File content population
- [ ] Folder organization
- [ ] File sharing settings
- [ ] Template support
- [ ] Batch file creation
- [ ] File modification capabilities

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

If you encounter issues:

1. Check the troubleshooting section
2. Verify all prerequisites are met
3. Check the API logs for errors
4. Ensure Google Drive API is enabled

---

**Happy file creating! 🎉**

