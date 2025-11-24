#!/bin/bash

# Hebrew Speech Correction System - Setup Script
# This script helps set up the environment and dependencies

echo "=================================="
echo "Hebrew Speech Correction System"
echo "Setup Script"
echo "=================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo "Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}✓ Python3 found: $PYTHON_VERSION${NC}"
else
    echo -e "${RED}✗ Python3 not found. Please install Python 3.8 or higher.${NC}"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Virtual environment created${NC}"
    else
        echo -e "${RED}✗ Failed to create virtual environment${NC}"
        exit 1
    fi
else
    echo -e "${YELLOW}! Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
echo "This may take several minutes..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Dependencies installed successfully${NC}"
else
    echo -e "${RED}✗ Failed to install some dependencies${NC}"
    echo "You may need to install system dependencies first:"
    echo "  Ubuntu/Debian: sudo apt-get install portaudio19-dev python3-pyaudio ffmpeg"
    echo "  macOS: brew install portaudio ffmpeg"
fi

# Create necessary directories
echo ""
echo "Creating project directories..."
mkdir -p data/recordings
mkdir -p data/syllables
mkdir -p data/training_data
mkdir -p models

echo -e "${GREEN}✓ Directories created${NC}"

# Check for audio devices
echo ""
echo "Checking audio devices..."
python3 -c "
import sounddevice as sd
print('Available audio devices:')
print(sd.query_devices())
" 2>/dev/null

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Audio devices detected${NC}"
else
    echo -e "${YELLOW}! Could not detect audio devices. Make sure your microphone is connected.${NC}"
fi

# Setup complete
echo ""
echo "=================================="
echo -e "${GREEN}Setup Complete!${NC}"
echo "=================================="
echo ""
echo "To run the application:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run the application: python main.py"
echo ""
echo "For more information, see README.md"
echo ""
