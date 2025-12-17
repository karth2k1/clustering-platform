#!/bin/bash
# Setup script for Clustering Platform Backend

echo "Setting up Clustering Platform Backend..."

# Activate virtual environment
if [ -d "../venv" ]; then
    echo "Activating virtual environment..."
    source ../venv/bin/activate
else
    echo "Creating virtual environment..."
    python3 -m venv ../venv
    source ../venv/bin/activate
fi

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Initialize database
echo "Initializing database..."
python -c "from app.database import init_db; init_db(); print('Database initialized successfully')"

echo "Setup complete!"
echo ""
echo "To run the server:"
echo "  cd backend"
echo "  source ../venv/bin/activate"
echo "  python run.py"

