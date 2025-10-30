# 🚀 Streamlit Cloud Deployment Guide

Complete guide to deploy your AI Merchandising System to Streamlit Cloud.

## 📋 Prerequisites

1. ✅ GitHub account
2. ✅ Code pushed to GitHub repository
3. ✅ Streamlit Cloud account (free) - Sign up at https://share.streamlit.io

## 🎯 Quick Deploy (5 minutes)

### Step 1: Ensure Files Are Ready

Your repository should have:
- ✅ `streamlit_app.py` - Main Streamlit application
- ✅ `requirements_streamlit.txt` - Python dependencies
- ✅ `.streamlit/config.toml` - Streamlit configuration
- ✅ All code pushed to GitHub

### Step 2: Deploy to Streamlit Cloud

1. **Go to Streamlit Cloud**: https://share.streamlit.io
2. **Sign in** with your GitHub account
3. **Click "New app"**
4. **Fill in the form:**
   - **Repository:** Select `Naveed233/AI.MD` (or your repo)
   - **Branch:** `main`
   - **Main file path:** `streamlit_app.py`
   - **App URL:** Choose a unique name (e.g., `ai-merchandising`)
5. **Click "Deploy"**

### Step 3: Configure ML Service URL

After deployment:

1. **In Streamlit Cloud dashboard**, click on your app
2. **Go to "Settings" → "Secrets"**
3. **Add this secret:**
   ```
   ML_API_URL = "https://your-ml-service.run.app"
   ```
4. **Save and wait for app to restart**

## 🔧 Configuration Options

### Option 1: Use Environment Variable (Recommended)

In Streamlit Cloud Secrets, add:
```toml
ML_API_URL = "https://your-ml-service-url.run.app"
```

### Option 2: Use Sidebar Input

The app has a sidebar where users can manually enter the ML service URL if no environment variable is set.

### Option 3: Deploy ML Service First

**For full functionality, deploy ML service to:**
- **Google Cloud Run** (recommended)
- **Heroku**
- **AWS Lambda**
- **Azure Functions**

**Cloud Run Example:**
```bash
cd ml_service
gcloud run deploy ml-service \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080
```

Then use the Cloud Run URL in Streamlit Secrets.

## 📁 Required Files Structure

```
md-system/
├── streamlit_app.py              # ✅ Main app
├── requirements_streamlit.txt    # ✅ Dependencies
├── .streamlit/
│   ├── config.toml              # ✅ Streamlit config
│   └── secrets.toml.example     # Example secrets
└── ml_service/                   # ML service (deploy separately)
```

## 🔍 Testing Locally Before Deploy

1. **Install dependencies:**
   ```bash
   pip install -r requirements_streamlit.txt
   ```

2. **Set environment variable:**
   ```bash
   export ML_API_URL="http://localhost:8080"
   ```

3. **Run Streamlit:**
   ```bash
   streamlit run streamlit_app.py
   ```

4. **Test connection** using the sidebar button

## 🚨 Troubleshooting

### App won't start
- ✅ Check `streamlit_app.py` is in root or correct path
- ✅ Verify `requirements_streamlit.txt` exists
- ✅ Check Streamlit Cloud logs for errors

### Can't connect to ML service
- ✅ Verify ML service is deployed and accessible
- ✅ Check `ML_API_URL` in Streamlit Secrets
- ✅ Test ML service health: `curl https://your-service.run.app/health`
- ✅ Ensure CORS is enabled in ML service

### Slow predictions
- ✅ ML service might be cold (first request is slow)
- ✅ Check Cloud Run logs for errors
- ✅ Verify network connectivity

### Import errors
- ✅ Check `requirements_streamlit.txt` has all packages
- ✅ Review Streamlit Cloud logs for missing packages

## 📊 Monitoring

**Streamlit Cloud provides:**
- ✅ Real-time logs
- ✅ Usage statistics
- ✅ Error tracking
- ✅ Performance metrics

**Access via:** Streamlit Cloud dashboard → Your app → Logs

## 🔐 Security Best Practices

1. **Don't commit secrets** - Use Streamlit Secrets
2. **Use HTTPS** - Always use HTTPS URLs for ML service
3. **Rate limiting** - Consider adding rate limits in ML service
4. **API keys** - Store in Streamlit Secrets if needed

## 🎉 Success!

Once deployed, your app will be live at:
```
https://your-app-name.streamlit.app
```

Share this URL with anyone!

## 📚 Additional Resources

- **Streamlit Docs:** https://docs.streamlit.io
- **Streamlit Cloud:** https://docs.streamlit.io/streamlit-community-cloud
- **Cloud Run:** https://cloud.google.com/run/docs

---

**Need help?** Check the logs in Streamlit Cloud dashboard or review error messages in the app.

