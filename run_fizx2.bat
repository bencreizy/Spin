@echo off
echo ===================================
echo FIZx2 SOVEREIGN LAUNCHER
echo ===================================
echo.
echo Checking Python installation...
py --version
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python from python.org
    pause
    exit /b
)
echo.
echo Checking Streamlit installation...
py -m pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo Streamlit not found. Installing...
    py -m pip install streamlit
)
echo.
echo Installing required packages...
py -m pip install numpy -q
echo.
echo ===================================
echo Launching FIZx2 Sovereign Interface...
echo Navigate to http://localhost:8501
echo Press Ctrl+C to stop the server
echo ===================================
echo.
py -m streamlit run fizx2_sovereign.py
pause
