@echo off 
echo Network Management Tool - CLI Interface 
echo ====================================== 
echo. 
echo Web Interface is running at: http://localhost:5000 
echo. 
:menu 
echo Select an option: 
echo ================== 
echo 1. Scan local network 
echo 2. Scan server network 
echo 3. Scan web server 
echo 4. Launch interactive dashboard 
echo 5. Launch enhanced terminal dashboard 
echo 6. Manage a specific device 
echo 7. Show help 
echo 8. Exit 
echo. 
set /p choice=Enter your choice (1-8):  
if "%choice%"=="1" goto scan_local 
if "%choice%"=="2" goto scan_server 
if "%choice%"=="3" goto scan_web 
if "%choice%"=="4" goto dashboard 
if "%choice%"=="5" goto enhanced_dashboard 
if "%choice%"=="6" goto manage 
if "%choice%"=="7" goto help 
if "%choice%"=="8" goto exit 
goto menu 
 
:scan_local 
echo Scanning local network... 
python src\network_tool.py --scan local 
echo. 
pause 
goto menu 
 
:scan_server 
echo Scanning server network... 
python src\network_tool.py --scan server 
echo. 
pause 
goto menu 
 
:scan_web 
echo Scanning web server... 
python src\network_tool.py --scan web 
echo. 
pause 
goto menu 
 
:dashboard 
echo Launching interactive dashboard... 
python src\network_tool.py --dashboard 
goto menu 
 
:enhanced_dashboard 
echo Launching enhanced terminal dashboard... 
python src\network_tool.py --enhanced-dashboard 
goto menu 
 
:manage 
set /p ip=Enter device IP address:  
python src\network_tool.py --manage %ip% 
echo. 
pause 
goto menu 
 
:help 
python src\network_tool.py --help 
echo. 
pause 
goto menu 
 
:exit 
del "%~f0" 
exit 
