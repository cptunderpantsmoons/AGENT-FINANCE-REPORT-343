# Railway CLI Installation

## Installation Methods

### Method 1: Standard Installation (Requires sudo)

Run this command in your terminal:

```bash
curl -fsSL https://railway.com/install.sh | sh
```

This will install Railway CLI to `/usr/local/bin/railway`.

**Note**: You'll need to enter your password when prompted for sudo.

### Method 2: Manual Installation (No sudo required)

If you don't have sudo access, you can install Railway CLI manually:

```bash
# Download Railway CLI
curl -fsSL https://railway.com/install.sh -o install-railway.sh

# Review the script (optional but recommended)
cat install-railway.sh

# Run with custom install path (no sudo needed)
mkdir -p ~/.local/bin
export PATH="$HOME/.local/bin:$PATH"
bash install-railway.sh --install-dir ~/.local/bin
```

Then add to your `~/.bashrc` or `~/.zshrc`:
```bash
export PATH="$HOME/.local/bin:$PATH"
```

### Method 3: Using npm (if you have Node.js)

```bash
npm install -g @railway/cli
```

### Method 4: Using Homebrew (macOS/Linux)

```bash
brew install railway
```

## Verify Installation

After installation, verify it works:

```bash
railway --version
```

You should see something like:
```
railway version 3.x.x
```

## Login to Railway

Once installed, login to your Railway account:

```bash
railway login
```

This will open a browser window for authentication.

## Alternative: Use Railway Web Dashboard

You don't actually need the CLI to deploy! You can:

1. **Push to GitHub** (as planned)
2. **Use Railway Web Dashboard** to:
   - Connect your GitHub repository
   - Set environment variables
   - Deploy your app

The CLI is optional but useful for:
- Managing projects from command line
- Viewing logs
- Running commands
- Advanced deployment options

## For Your Deployment

Since you're deploying via GitHub → Railway web dashboard, you can skip CLI installation for now and install it later if needed.

## Quick Reference

```bash
# Install Railway CLI
curl -fsSL https://railway.com/install.sh | sh

# Login
railway login

# Link to project (if using CLI)
railway link

# View logs
railway logs

# Set environment variable
railway variables set OPENROUTER_API_KEY=your-key

# Deploy
railway up
```

## Troubleshooting

### Permission Denied

If you get permission errors:
- Use Method 2 (manual installation to ~/.local/bin)
- Or use `sudo` with Method 1

### Command Not Found

After installation, if `railway` command not found:
- Add installation directory to PATH
- Restart your terminal
- Check installation location

### Already Installed

If Railway CLI is already installed:
```bash
railway --version  # Check version
railway update     # Update to latest
```

## Next Steps

1. **Install CLI** (optional): Use one of the methods above
2. **Or skip CLI**: Use Railway web dashboard instead
3. **Deploy**: Push to GitHub and deploy via Railway web interface

For your use case (GitHub → Railway web dashboard), the CLI is optional!

