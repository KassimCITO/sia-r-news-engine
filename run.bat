@echo off
REM SIA-R News Engine - Startup Script (Windows)

title SIA-R News Engine - Starting

cls
echo ============================================================
echo           SIA-R News Engine - Starting Application
echo ============================================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔌 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/update requirements
echo 📚 Installing dependencies...
pip install -r requirements.txt --quiet

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  .env file not found
    echo 📝 Creating from .env.example...
    if exist ".env.example" (
        copy .env.example .env
        echo ✅ .env created. Please configure it with your values.
    ) else (
        echo ❌ .env.example not found
        exit /b 1
    )
)

REM Initialize database
echo 💾 Initializing database...
python -c "from storage.database import init_db; init_db(); print('✅ Database ready')" 2>nul

cls
echo ============================================================
echo                  Starting Application...
echo ============================================================
echo.
echo 🌍 Environment: development
echo 🔒 Debug Mode: True
echo 📍 Host: 0.0.0.0
echo 🔌 Port: 8000
echo.
echo 🚀 Application will be available at: http://localhost:8000
echo 🔐 Login page: http://localhost:8000/login
echo 📊 Dashboard: http://localhost:8000/dashboard
echo.
echo Press Ctrl+C to stop the application
echo.

REM Run the application
python app.py

pause
