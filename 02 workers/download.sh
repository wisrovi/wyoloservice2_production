#!/bin/bash
# NeuralForgeAI - Remote Worker Downloader
# Author: William Rodriguez - wisrovi
#
# This script downloads only the necessary installation files for the GPU Worker Invoker
# directly from the GitHub repository, without needing to clone the entire project.

echo "=========================================================="
echo "  NeuralForgeAI - Worker Node Downloader"
echo "=========================================================="
echo "Downloading installation files from GitHub..."

# Create an isolated directory for the installer
TARGET_DIR="wyolo_worker_setup"
mkdir -p "$TARGET_DIR"
cd "$TARGET_DIR" || exit 1

# Download the tarball and extract ONLY the 'workers' directory
# We use standard tools (curl and tar) so it works on any bare Linux machine
if curl -sSL https://github.com/wisrovi/wyoloservice2_production/archive/refs/heads/main.tar.gz | tar -xz --strip-components=2 "wyoloservice2_production-main/workers"; then
    echo "✅ Download complete!"
    echo "Files have been saved to: $(pwd)"
    echo ""
    echo "----------------------------------------------------------"
    echo "To install the worker node, run the following commands:"
    echo "----------------------------------------------------------"
    echo "cd $TARGET_DIR"
    echo "sudo chmod +x install.sh"
    echo "sudo ./install.sh"
    echo "=========================================================="
else
    echo "❌ Error: Failed to download files. Please check your internet connection and ensure tar/curl are installed."
    # Clean up on failure
    cd ..
    rm -rf "$TARGET_DIR"
    exit 1
fi
