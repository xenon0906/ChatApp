#!/bin/bash
# Build Debian package for chattingworld

set -e

echo "================================================"
echo "  Building Debian Package for ChattingWorld"
echo "================================================"

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "❌ Error: Debian packages can only be built on Linux"
    echo "💡 Try using: WSL, Docker, or a Linux VM"
    exit 1
fi

# Install build dependencies
echo "[1/5] Installing build dependencies..."
sudo apt-get update
sudo apt-get install -y python3-stdeb python3-all dh-python debhelper

# Clean previous builds
echo "[2/5] Cleaning previous builds..."
rm -rf deb_dist/ dist/ *.egg-info

# Build the Debian package
echo "[3/5] Building Debian package..."
python3 setup.py --command-packages=stdeb.command bdist_deb

# Find the built package
DEB_FILE=$(find deb_dist -name "*.deb" | head -n 1)

if [ -z "$DEB_FILE" ]; then
    echo "❌ Error: No .deb file found!"
    exit 1
fi

echo "[4/5] Package built successfully!"
echo "📦 Location: $DEB_FILE"

# Test installation (optional)
echo "[5/5] Testing installation..."
echo "To install, run:"
echo "  sudo dpkg -i $DEB_FILE"
echo ""
echo "To test:"
echo "  chattingworld"

echo ""
echo "================================================"
echo "✅ Debian package created successfully!"
echo "================================================"
echo ""
echo "Share this file with users:"
echo "  $DEB_FILE"
echo ""
echo "Users can install with:"
echo "  sudo dpkg -i $(basename $DEB_FILE)"
echo "  sudo apt-get install -f  # Install dependencies"
echo ""
