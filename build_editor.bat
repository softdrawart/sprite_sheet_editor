@echo off
call myenv\Scripts\activate.bat
pip install pyinstaller
pyinstaller --onefile --noconsole run.py
pause