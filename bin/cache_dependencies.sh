#!/bin/bash
# Script to download and cache external dependencies locally

set -e

# Create vendor directory if it doesn't exist
VENDOR_DIR="$(dirname "$0")/../vendor"
mkdir -p "$VENDOR_DIR"

MDL_VERSION="1.3.0"
BASE_URL="https://cdnjs.cloudflare.com/ajax/libs/material-design-lite/${MDL_VERSION}"

# Material Design Lite color schemes to cache
COLOR_SCHEMES=(
    "deep_orange-blue"
    "indigo-pink"
    "blue-red"
    "light_blue-pink"
    "purple-pink"
    "deep_purple-pink"
)

echo "Caching Material Design Lite v${MDL_VERSION}..."

# Download the main JavaScript file
if [ ! -f "$VENDOR_DIR/material.min.js" ]; then
    echo "Downloading material.min.js..."
    curl -sL "${BASE_URL}/material.min.js" -o "$VENDOR_DIR/material.min.js"
    echo "✓ Downloaded material.min.js"
else
    echo "✓ material.min.js already cached"
fi

# Download CSS files for each color scheme
for scheme in "${COLOR_SCHEMES[@]}"; do
    css_file="material.${scheme}.min.css"
    if [ ! -f "$VENDOR_DIR/$css_file" ]; then
        echo "Downloading $css_file..."
        curl -sL "${BASE_URL}/$css_file" -o "$VENDOR_DIR/$css_file"
        echo "✓ Downloaded $css_file"
    else
        echo "✓ $css_file already cached"
    fi
done

echo ""
echo "All dependencies cached in: $VENDOR_DIR"
echo "Available color schemes:"
for scheme in "${COLOR_SCHEMES[@]}"; do
    echo "  - $scheme"
done
