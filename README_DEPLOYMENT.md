# Quick Deployment Guide

## Railway Deployment (5 Minutes)

### Step 1: Push to GitHub

```bash
git add .
git commit -m "Ready for Railway deployment"
git push origin main
```

### Step 2: Deploy on Railway

1. Go to https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Railway will auto-detect and build

### Step 3: Set Environment Variable

In Railway dashboard → Variables tab, add:

```
OPENROUTER_API_KEY=your-api-key-here
```

### Step 4: Access Your App

Railway provides a public URL. Click it to access your app!

## That's It! 🎉

Your AASB Financial Statement Generator is now live on Railway.

For detailed instructions, see [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md)

