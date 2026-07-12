@echo off
REM build.bat
REM Builds a standalone Windows executable for the 4D Object Rotation app.
REM Run this from the project root (where requirements.txt lives).
 
echo Installing dependencies...
pip install -r requirements.txt
 
echo Building executable...
pyinstaller --noconfirm --onefile --windowed ^
    --name "4D-Object-Rotation" ^
    --paths src ^
    src\main.py
 
echo.
echo Done. Find your executable in the "dist" folder: dist\4D-Object-Rotation.exe
pause
 