#!/bin/bash

# Clean Build Script for Stage 2 GUI
# Removes all cached build data to fix container issues

echo "🧹 Cleaning Stage 2 GUI build cache..."
echo ""

# Remove Derived Data
echo "1. Removing Xcode Derived Data..."
rm -rf ~/Library/Developer/Xcode/DerivedData/BPMKeyDetector-* 2>/dev/null
echo "✓ Derived Data removed"

# Try to remove container (may fail due to permissions)
echo ""
echo "2. Attempting to remove app container..."
if rm -rf ~/Library/Containers/com.gentech.BPMKeyDetector 2>/dev/null; then
    echo "✓ Container removed successfully"
else
    echo "⚠️  Container removal failed (protected)"
    echo "   Please manually delete in Finder:"
    echo "   ~/Library/Containers/com.gentech.BPMKeyDetector"
    echo ""
    echo "   Or try with sudo:"
    echo "   sudo rm -rf ~/Library/Containers/com.gentech.BPMKeyDetector"
fi

echo ""
echo "3. Checking Python backend..."
if [ -f "python-backend/venv/bin/python3" ]; then
    echo "✓ Python backend exists"
else
    echo "⚠️  Python backend not found"
    echo "   Run: cd python-backend && ./setup.sh"
fi

echo ""
echo "✅ Cleanup complete!"
echo ""
echo "Next steps:"
echo "1. In Xcode: Product → Clean Build Folder (⇧⌘K)"
echo "2. Close Xcode completely"
echo "3. Reopen and rebuild (⌘B)"
echo "4. Run (⌘R)"
echo ""
