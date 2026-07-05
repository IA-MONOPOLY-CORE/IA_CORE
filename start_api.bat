@echo off
title SAAOP API Server
echo ========================================
echo  S.A.A.O.P. API Server
echo ========================================
echo.
echo Starting FastAPI server on http://localhost:8000
echo Press Ctrl+C to stop
echo.

cd /d "%~dp0"

if exist venv\Scripts\activate (
    call venv\Scripts\activate
    echo Virtual environment activated
) else (
    echo WARNING: Virtual environment not found at venv\
    echo Please ensure venv is set up correctly
)

echo.
echo Starting uvicorn...
python -m uvicorn api:app --host 0.0.0.0 --port 8000 --reload

pause
