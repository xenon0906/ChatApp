#!/bin/bash
# Build and publish to PyPI

set -e

echo "================================================"
echo "  Publishing ChattingWorld to PyPI"
echo "================================================"

# Install build tools
echo "[1/6] Installing build tools..."
pip install --upgrade build twine

# Clean previous builds
echo "[2/6] Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info

# Build the package
echo "[3/6] Building package..."
python -m build

# Check the package
echo "[4/6] Checking package..."
python -m twine check dist/*

# Display contents
echo "[5/6] Package contents:"
ls -lh dist/

echo ""
echo "================================================"
echo "  Ready to publish!"
echo "================================================"
echo ""
echo "Test on TestPyPI first (recommended):"
echo "  python -m twine upload --repository testpypi dist/*"
echo ""
echo "Or publish to PyPI:"
echo "  python -m twine upload dist/*"
echo ""
echo "You'll need:"
echo "  - PyPI account: https://pypi.org/account/register/"
echo "  - API token: https://pypi.org/manage/account/token/"
echo ""
echo "[6/6] Waiting for your confirmation..."
read -p "Publish to PyPI now? (y/N): " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📤 Publishing to PyPI..."
    python -m twine upload dist/*
    echo ""
    echo "================================================"
    echo "✅ Published successfully!"
    echo "================================================"
    echo ""
    echo "Users can now install with:"
    echo "  pip install chattingworld"
    echo ""
else
    echo "❌ Cancelled. Package not published."
    echo "Files ready in dist/ directory"
fi
