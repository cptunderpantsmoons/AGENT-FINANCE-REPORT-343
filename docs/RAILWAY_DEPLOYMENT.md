# Railway Deployment Guide

## Overview

This guide will help you deploy the AASB Financial Statement Generator to Railway.

## Prerequisites

1. GitHub account
2. Railway account (sign up at https://railway.app)
3. OpenRouter API key (provided)

## Step-by-Step Deployment

### 1. Prepare Repository

Ensure your repository has:
- ✅ All source files
- ✅ `requirements.txt`
- ✅ `Procfile` (for Railway)
- ✅ `railway.json` (optional, for Railway config)
- ✅ `.gitignore` (excludes unnecessary files)

### 2. Push to GitHub

```bash
# Initialize git if not already done
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - AASB Financial Statement Generator"

# Add remote (replace with your repo URL)
git remote add origin https://github.com/yourusername/your-repo-name.git

# Push to GitHub
git push -u origin main
```

### 3. Deploy on Railway

1. **Log into Railway**: https://railway.app
2. **New Project**: Click "New Project"
3. **Deploy from GitHub**: Select "Deploy from GitHub repo"
4. **Select Repository**: Choose your repository
5. **Railway will automatically detect** the project and start building

### 4. Configure Environment Variables

In Railway dashboard, go to your project → Variables tab, add:

```
OPENROUTER_API_KEY=your-api-key-here
PORT=8501
```

**Important**: Railway automatically sets `PORT`, but you can override if needed.

### 5. Deploy Settings

Railway will automatically:
- Detect Python project
- Install dependencies from `requirements.txt`
- Run the command from `Procfile`

### 6. Access Your App

Once deployed:
- Railway provides a public URL (e.g., `https://your-app.railway.app`)
- Click on the URL in Railway dashboard
- Your app should be live!

## Configuration Files

### Procfile
```
web: streamlit run gui_app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true
```

### railway.json
Contains Railway-specific configuration for deployment.

### runtime.txt
Specifies Python version (3.11.0).

## Environment Variables

### Required
- `OPENROUTER_API_KEY`: Your OpenRouter API key for AI features

### Optional
- `PORT`: Server port (Railway sets this automatically)
- `RAILWAY_ENVIRONMENT`: Automatically set by Railway

## Troubleshooting

### Build Fails

**Issue**: Build errors during deployment

**Solutions**:
1. Check `requirements.txt` has all dependencies
2. Verify Python version in `runtime.txt` is supported
3. Check Railway build logs for specific errors
4. Ensure all files are committed to GitHub

### App Won't Start

**Issue**: App deploys but won't start

**Solutions**:
1. Check `Procfile` command is correct
2. Verify `PORT` environment variable is set
3. Check Railway logs for startup errors
4. Ensure Streamlit is in `requirements.txt`

### Port Issues

**Issue**: Port binding errors

**Solutions**:
1. Railway automatically sets `PORT` - don't hardcode
2. Use `$PORT` in Procfile
3. Streamlit reads `PORT` from environment

### Environment Variables Not Working

**Issue**: API key not recognized

**Solutions**:
1. Check variables are set in Railway dashboard
2. Verify variable names match exactly
3. Restart deployment after adding variables
4. Check variable visibility (public/private)

## Monitoring

### View Logs

In Railway dashboard:
- Go to your project
- Click "View Logs"
- See real-time application logs

### Metrics

Railway provides:
- CPU usage
- Memory usage
- Network traffic
- Request metrics

## Updating Deployment

### Automatic Updates

Railway automatically redeploys when you push to GitHub:
```bash
git add .
git commit -m "Update application"
git push
```

### Manual Redeploy

In Railway dashboard:
- Go to your project
- Click "Redeploy"
- Select deployment to redeploy

## Custom Domain

To add a custom domain:

1. Go to Railway project settings
2. Click "Domains"
3. Add your custom domain
4. Follow DNS configuration instructions

## Cost Considerations

Railway pricing:
- **Hobby Plan**: Free tier available
- **Pro Plan**: Pay-as-you-go
- Check Railway pricing for current rates

**Tips to reduce costs**:
- Use free tier for development
- Monitor resource usage
- Set up auto-sleep for non-production apps

## Security

### API Keys

- ✅ Store in Railway environment variables
- ✅ Never commit to GitHub
- ✅ Use Railway's secret management
- ❌ Don't hardcode in source code

### Best Practices

1. Use environment variables for all secrets
2. Enable Railway's built-in security features
3. Regularly rotate API keys
4. Monitor access logs

## Support

### Railway Support

- Documentation: https://docs.railway.app
- Discord: Railway Discord community
- Email: support@railway.app

### Application Issues

- Check Railway logs
- Review application logs
- Test locally first
- Check GitHub issues

## Quick Reference

### Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Repository connected to Railway
- [ ] Environment variables set
- [ ] Build successful
- [ ] App accessible via Railway URL
- [ ] Test file uploads
- [ ] Test PDF generation
- [ ] Verify AI features work (if enabled)

### Common Commands

```bash
# Local testing
streamlit run gui_app.py

# Check Railway status
# (via Railway dashboard)

# View logs
# (via Railway dashboard)
```

## Next Steps

After successful deployment:

1. **Test the application**: Upload sample files
2. **Share the URL**: With your team/users
3. **Monitor usage**: Check Railway metrics
4. **Set up alerts**: For errors or downtime
5. **Custom domain**: Add your own domain (optional)

## Your Deployment Info

**OpenRouter API Key**: See `SECRETS.md` (not committed to GitHub for security)

**Set this in Railway environment variables as**: `OPENROUTER_API_KEY`

Your app will be available at: `https://your-app-name.railway.app`

Happy deploying! 🚂

