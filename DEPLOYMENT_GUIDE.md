# 🚀 Deploy to Railway - Complete Guide

This guide will help you deploy your Google Drive API to Railway so ChatGPT can access it from the browser.

## 📋 **Prerequisites**

1. **GitHub Account** - to host your code
2. **Railway Account** - for hosting (free tier available)
3. **Google Cloud Console** - for OAuth credentials

## 🔧 **Step 1: Prepare Your Code**

### 1.1 Update Environment Variables
Create a `.env` file for local development:
```bash
GOOGLE_OAUTH_CREDENTIALS_FILE=oauth_credentials.json
RAILWAY_ENVIRONMENT=development
```

### 1.2 Test Locally
```bash
python main.py
```

## 🌐 **Step 2: Deploy to Railway**

### 2.1 Create Railway Account
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Create a new project

### 2.2 Deploy Your App
1. **Connect GitHub Repository**
   - Click "Deploy from GitHub repo"
   - Select your repository
   - Railway will auto-detect it's a Python app

2. **Configure Environment Variables**
   - Go to your project → Variables
   - Add these variables:
   ```
   GOOGLE_OAUTH_CREDENTIALS_FILE=oauth_credentials.json
   RAILWAY_ENVIRONMENT=production
   ```

3. **Upload OAuth Credentials**
   - In Railway dashboard, go to Files
   - Upload your `oauth_credentials.json`
   - This file will be available at runtime

4. **Deploy**
   - Railway will automatically build and deploy
   - Wait for deployment to complete

### 2.3 Get Your Public URL
- After deployment, Railway will give you a URL like:
  `https://your-app-name.railway.app`
- Copy this URL - you'll need it for ChatGPT integration

## 🔐 **Step 3: Update ChatGPT Integration**

### 3.1 Update the Integration Class
```python
# In chatgpt_integration.py, update the cloud URL:
integration = GoogleDriveChatGPTIntegration(
    api_base_url="https://your-app-name.railway.app"
)
```

### 3.2 Test the Deployed API
```bash
# Test health endpoint
curl https://your-app-name.railway.app/health

# Test document creation
curl -X POST "https://your-app-name.railway.app/create_doc" \
     -H "Content-Type: application/json" \
     -d '{"name": "Test Document"}'
```

## 🤖 **Step 4: Integrate with ChatGPT**

### 4.1 Create ChatGPT Plugin (Advanced)
1. Create a `plugin.json` file:
```json
{
  "schema_version": "v1",
  "name_for_human": "Google Drive Creator",
  "name_for_model": "google_drive_creator",
  "description_for_human": "Create Google Documents and Sheets automatically",
  "description_for_model": "Create Google Drive files through natural language requests",
  "auth": {
    "type": "none"
  },
  "api": {
    "type": "openapi",
    "url": "https://your-app-name.railway.app/openapi.json"
  }
}
```

2. Host this file publicly (GitHub Pages, etc.)

### 4.2 Use with ChatGPT API (Recommended)
```python
import openai
from chatgpt_integration import GoogleDriveChatGPTIntegration

# Initialize integration
integration = GoogleDriveChatGPTIntegration(
    api_base_url="https://your-app-name.railway.app"
)

# Use with ChatGPT
def create_file_via_chatgpt(user_request):
    response = integration.process_chatgpt_request(user_request)
    return response

# Example usage
result = create_file_via_chatgpt("Create a Google Document called Meeting Notes")
print(result)
```

## 🧪 **Step 5: Testing**

### 5.1 Test API Endpoints
```bash
# Health check
curl https://your-app-name.railway.app/health

# Create document
curl -X POST "https://your-app-name.railway.app/create_doc" \
     -H "Content-Type: application/json" \
     -d '{"name": "Test Document"}'

# Create sheet
curl -X POST "https://your-app-name.railway.app/create_sheet" \
     -H "Content-Type: application/json" \
     -d '{"name": "Test Sheet"}'
```

### 5.2 Test ChatGPT Integration
```python
python demo_chatgpt_integration.py
# Update the URL in the script to your Railway URL
```

## 🚨 **Troubleshooting**

### Common Issues

1. **"OAuth credentials not found"**
   - Ensure `oauth_credentials.json` is uploaded to Railway Files
   - Check environment variable path

2. **"Port binding error"**
   - Railway sets `PORT` environment variable automatically
   - Our code handles this with `os.environ.get("PORT", 3333)`

3. **"Google authentication failed"**
   - Check if OAuth credentials are valid
   - Verify Google Drive API is enabled

4. **"API not accessible"**
   - Check Railway deployment status
   - Verify the public URL is correct

### Debug Mode
```bash
# In Railway dashboard, check logs for errors
# Common log locations:
# - Build logs
# - Runtime logs
# - Environment variables
```

## 🔄 **Step 6: Continuous Deployment**

### 6.1 Automatic Updates
- Railway automatically redeploys when you push to GitHub
- Update your code locally, push to GitHub
- Railway will rebuild and redeploy automatically

### 6.2 Monitor Usage
- Check Railway dashboard for:
  - Request logs
  - Error rates
  - Resource usage
  - Cost (free tier limits)

## 🎯 **Next Steps After Deployment**

1. **Test all endpoints** with your Railway URL
2. **Update ChatGPT integration** with the new URL
3. **Create ChatGPT plugin** or use API integration
4. **Monitor performance** and usage
5. **Scale if needed** (Railway has paid plans)

## 💰 **Costs**

- **Railway Free Tier**: $5/month credit
- **Google Drive API**: Free (with quotas)
- **Total**: Essentially free for personal use

---

**🎉 Congratulations! Your API is now accessible to ChatGPT from anywhere in the world!**

