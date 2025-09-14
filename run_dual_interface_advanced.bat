@echo off
REM Network Management Tool - Advanced Dual Interface Launcher
REM This script opens two terminals:
REM 1. One for the web UI interface
REM 2. One for manual CLI inputs with menu options

echo Network Management Tool - Advanced Dual Interface Launcher
echo ========================================================

REM Get the current directory (project root)
set PROJECT_DIR=%~dp0

echo Starting Network Management Tool interfaces...
echo.

REM Start the web interface in a new terminal window
echo [1/2] Starting Web Interface...
start "Network Management Tool - Web Interface" cmd /k "cd /d %PROJECT_DIR% && python run_web.py"

REM Wait a moment for the web interface to start
timeout /t 2 /nobreak >nul

REM Create a temporary batch file for the CLI interface with menu options
echo @echo off > "%PROJECT_DIR%\temp_cli_menu.bat"
echo echo Network Management Tool - CLI Interface >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo echo ====================================== >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo echo. >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo echo Web Interface is running at: http://localhost:5000 >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo echo. >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo :menu >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo echo Select an option: >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo echo ================== >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo echo 1. Scan local network >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo echo 2. Scan server network >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo echo 3. Scan web server >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo echo 4. Launch interactive dashboard >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo echo 5. Launch enhanced terminal dashboard >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo echo 6. Manage a specific device >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo echo 7. Show help >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo echo 8. Exit >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo echo. >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo set /p choice=Enter your choice (1-8):  >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo if "%%choice%%"=="1" goto scan_local >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo if "%%choice%%"=="2" goto scan_server >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo if "%%choice%%"=="3" goto scan_web >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo if "%%choice%%"=="4" goto dashboard >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo if "%%choice%%"=="5" goto enhanced_dashboard >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo if "%%choice%%"=="6" goto manage >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo if "%%choice%%"=="7" goto help >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo if "%%choice%%"=="8" goto exit >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo goto menu >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo. >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo :scan_local >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo echo Scanning local network... >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo python src\network_tool.py --scan local >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo echo. >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo pause >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo goto menu >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo. >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo :scan_server >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo echo Scanning server network... >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo python src\network_tool.py --scan server >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo echo. >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo pause >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo goto menu >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo. >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo :scan_web >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo echo Scanning web server... >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo python src\network_tool.py --scan web >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo echo. >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo pause >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo goto menu >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo. >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo :dashboard >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo echo Launching interactive dashboard... >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo python src\network_tool.py --dashboard >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo goto menu >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo. >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo :enhanced_dashboard >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo echo Launching enhanced terminal dashboard... >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo python src\network_tool.py --enhanced-dashboard >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo goto menu >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo. >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo :manage >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo set /p ip=Enter device IP address:  >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo python src\network_tool.py --manage %%ip%% >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo echo. >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo pause >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo goto menu >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo. >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo :help >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo python src\network_tool.py --help >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo echo. >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo pause >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo goto menu >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo. >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo :exit >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo del "%%~f0" >> "%PROJECT_DIR%\temp_cli_menu.bat"
echo exit >> "%PROJECT_DIR%\temp_cli_menu.bat"

REM Start the CLI interface with menu in a new terminal window
echo [2/2] Starting CLI Interface with Menu...
start "Network Management Tool - CLI Interface" cmd /k "cd /d %PROJECT_DIR% && temp_cli_menu.bat"

echo.
echo Both interfaces have been started:
echo - Web Interface: Check browser at http://localhost:5000
echo - CLI Interface: Use the menu for common operations
echo.
echo Press any key to close this launcher window (terminals will remain open)...
pause >nul