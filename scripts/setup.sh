#!/bin/bash
# Setup script for Lumina environment

echo "Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "Installing backend dependencies..."
pip install -r backend/requirements.txt

echo "Installing frontend dependencies..."
cd frontend
npm install
cd ..

echo "Setup complete. You can now run the backend and frontend."
