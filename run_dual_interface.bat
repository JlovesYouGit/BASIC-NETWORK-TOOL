@echo off
REM Network Management Tool - Dual Interface Launcher
REM This script opens two terminals:
REM 1. One for the web UI interface
REM 2. One for manual CLI inputs

echo Network Management Tool - Dual Interface Launcher
echo =================================================

REM Get the current directory (project root)
set PROJECT_DIR=%~dp0

echo Starting Network Management Tool interfaces...
echo.

REM Start the web interface in a new terminal window
echo [1/2] Starting Web Interface...
start "Network Management Tool - Web Interface" cmd /k "cd /d %PROJECT_DIR% && python run_web.py"

REM Wait a moment for the web interface to start
timeout /t 2 /nobreak >nul

REM Start the CLI interface in a new terminal window
echo [2/2] Starting CLI Interface...
start "Network Management Tool - CLI Interface" cmd /k "cd /d %PROJECT_DIR% && python src\network_tool.py --help"

echo.
echo Both interfaces have been started:
echo - Web Interface: Check browser at http://localhost:5000
echo - CLI Interface: Use this terminal for manual commands
echo.
echo To scan your local network, in the CLI terminal run:
echo   python src\network_tool.py --scan local
echo.
echo To launch the interactive dashboard, in the CLI terminal run:
echo   python src\network_tool.py --dashboard
echo.
echo To launch the enhanced terminal dashboard, in the CLI terminal run:
echo   python src\network_tool.py --enhanced-dashboard
echo.
echo Press any key to close this launcher window (terminals will remain open)...
pause >nul