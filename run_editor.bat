@echo off
setlocal

:: Check if Python is installed
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo Python is not installed. Please install Python first.
    pause
    exit /b
)

:: Create virtual environment
python -m venv myenv
if errorlevel 1 (
    echo Failed to create virtual environment.
    pause
    exit /b
)

:: Activate virtual environment
call myenv\Scripts\activate.bat
if errorlevel 1 (
    echo Failed to activate virtual environment.
    pause
    exit /b
)

:: Install requirements
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install requirements.
    pause
    exit /b
)

:: Run the application
python run.py

endlocal
pause
