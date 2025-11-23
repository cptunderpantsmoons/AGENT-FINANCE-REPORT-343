#!/bin/bash
# Manual Railway CLI installation script

echo "Installing Railway CLI to ~/.local/bin..."

# Create directory
mkdir -p ~/.local/bin

# Detect OS and architecture
OS="$(uname -s | tr '[:upper:]' '[:lower:]')"
ARCH="$(uname -m)"

# Map architecture
case "$ARCH" in
    x86_64) ARCH="x64" ;;
    aarch64|arm64) ARCH="arm64" ;;
    *) echo "Unsupported architecture: $ARCH"; exit 1 ;;
esac

# Download Railway CLI
echo "Downloading Railway CLI for $OS/$ARCH..."
RAILWAY_VERSION="3.0.0"  # Update to latest version
URL="https://github.com/railwayapp/cli/releases/download/v${RAILWAY_VERSION}/railway-${OS}-${ARCH}"

curl -L -o ~/.local/bin/railway "$URL"
chmod +x ~/.local/bin/railway

# Add to PATH
if ! grep -q '~/.local/bin' ~/.bashrc 2>/dev/null; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
fi

echo "✅ Railway CLI installed to ~/.local/bin/railway"
echo "📝 Added ~/.local/bin to PATH in ~/.bashrc"
echo ""
echo "To use Railway CLI:"
echo "  source ~/.bashrc"
echo "  railway --version"
echo ""
echo "Then link your project:"
echo "  railway link -p 44b1a2ef-1f95-4d18-a5df-ad936f6fdd5c"

