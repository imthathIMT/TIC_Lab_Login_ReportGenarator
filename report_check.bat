@echo off
title Student Lab Usage Report System
cd /d "%~dp0"

echo.
echo Starting Student Lab Usage Report System...
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not added to PATH.
    pause
    exit /b
)

REM Install required Python packages
echo Installing required Python packages...
python -m pip install --upgrade pip >nul
python -m pip install tabulate pandas openpyxl >nul

if %errorlevel% neq 0 (
    echo Error: Failed to install one or more Python packages.
    pause
    exit /b
)

REM Run the Python script
echo Running report_generator.py...
echo.
python report_generator.py

if %errorlevel% neq 0 (
    echo.
    echo Error: Python script failed to run!
    pause
    exit /b
)

pause
