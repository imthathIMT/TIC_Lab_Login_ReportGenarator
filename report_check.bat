@echo off
title Student Lab Usage Report System
cd /d "%~dp0"
echo Starting Student Lab Usage Report System...
echo.
python report_generator.py
if %errorlevel% neq 0 (
    echo.
    echo Error: Python not found or script failed!
    echo Make sure Python is installed and added to PATH.
    echo.
)
pause