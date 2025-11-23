# Quick Railway Setup

## Your Railway Project ID
```
44b1a2ef-1f95-4d18-a5df-ad936f6fdd5c
```

## Installation Options

### Option 1: Standard Installation (Recommended)

Run in your terminal:
```bash
sudo curl -fsSL https://railway.com/install.sh | sh
railway link -p 44b1a2ef-1f95-4d18-a5df-ad936f6fdd5c
```

### Option 2: Manual Installation (No sudo)

Run the manual install script:
```bash
./install_railway_manual.sh
source ~/.bashrc
railway link -p 44b1a2ef-1f95-4d18-a5df-ad936f6fdd5c
```

### Option 3: Skip CLI - Use Web Dashboard

You don't need the CLI! You can:
1. Push to GitHub
2. Go to Railway web dashboard
3. Connect your repository
4. Set environment variables
5. Deploy!

## After Linking

Once linked, you can:

```bash
# View project info
railway status

# Set environment variable
railway variables set OPENROUTER_API_KEY=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

# View logs
railway logs

# Deploy
railway up
```

## Important: Set Environment Variable

Don't forget to set your OpenRouter API key in Railway:

**Via CLI:**
```bash
railway variables set OPENROUTER_API_KEY=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
```

**Via Web Dashboard:**
- Go to your Railway project
- Click "Variables" tab
- Add: `OPENROUTER_API_KEY` = `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`

## Next Steps

1. ✅ Install Railway CLI (or use web dashboard)
2. ✅ Link project: `railway link -p 44b1a2ef-1f95-4d18-a5df-ad936f6fdd5c`
3. ✅ Set environment variable
4. ✅ Push to GitHub
5. ✅ Deploy!

