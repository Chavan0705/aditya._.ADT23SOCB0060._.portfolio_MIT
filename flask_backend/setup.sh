#!/bin/bash

# Comment Moderation System Setup Script
# This script sets up the environment and runs the application

echo "=========================================="
echo "Comment Moderation System Setup"
echo "=========================================="
echo ""

# Check Python version
echo "[1/5] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✓ Found Python $PYTHON_VERSION"
echo ""

# Create virtual environment
echo "[2/5] Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "[3/5] Activating virtual environment..."
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null
echo "✓ Virtual environment activated"
echo ""

# Install dependencies
echo "[4/5] Installing dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
echo "✓ Dependencies installed"
echo ""

# Load sample data
echo "[5/5] Loading sample data..."
python load_sample_data.py 50 > /dev/null 2>&1
echo "✓ Sample data loaded (50 comments)"
echo ""

echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Starting application..."
echo ""
echo "Access the application at:"
echo "  Dashboard:  http://localhost:5000/"
echo "  Analyzer:   http://localhost:5000/analyzer"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run the application
python run.py
