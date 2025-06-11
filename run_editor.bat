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

:: Clone the repository if not already cloned
if not exist sprite_sheet_editor (
    git clone https://github.com/softdrawart/sprite_sheet_editor
)

:: Change directory into the cloned repository
cd sprite_sheet_editor

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
