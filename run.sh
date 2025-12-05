#!/bin/bash

# SIA-R News Engine - Startup Script (Linux/Mac)

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║           SIA-R News Engine - Starting Application           ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install/update requirements
echo "📚 Installing dependencies..."
pip install -r requirements.txt --quiet

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found"
    echo "📝 Creating from .env.example..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✅ .env created. Please configure it with your values."
    else
        echo "❌ .env.example not found"
        exit 1
    fi
fi

# Initialize database
echo "💾 Initializing database..."
python3 -c "from storage.database import init_db; init_db(); print('✅ Database ready')" 2>/dev/null || true

# Get configuration
source .env

echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                  Starting Application...                     ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "🌍 Environment: ${FLASK_ENV:-development}"
echo "🔒 Debug Mode: ${DEBUG:-False}"
echo "📍 Host: ${HOST:-0.0.0.0}"
echo "🔌 Port: ${PORT:-8000}"
echo ""
echo "🚀 Application will be available at: http://localhost:${PORT:-8000}"
echo "🔐 Login page: http://localhost:${PORT:-8000}/login"
echo "📊 Dashboard: http://localhost:${PORT:-8000}/dashboard"
echo ""
echo "Press Ctrl+C to stop the application"
echo ""

# Run the application
python3 app.py
