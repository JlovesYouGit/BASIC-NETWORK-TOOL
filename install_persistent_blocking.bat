@echo off
REM Install persistent blocking service for Windows

echo Installing persistent blocking service...

REM Create the service using sc command
sc create NetworkBlockerService binPath= "%~dp0restore_blocked_ips.py" start= auto

if %errorlevel% == 0 (
    echo Service installed successfully
    echo Starting the service...
    sc start NetworkBlockerService
    if %errorlevel% == 0 (
        echo Service started successfully
    ) else (
        echo Failed to start service
    )
) else (
    echo Failed to install service
    echo Please run this script as Administrator
)

pause