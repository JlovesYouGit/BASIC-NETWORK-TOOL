@echo off
echo Adding Nmap to PATH...
setx PATH "%PATH%;%~dp0..\break"
echo Nmap has been added to your PATH. You may need to restart your terminal for changes to take effect.
echo Testing Nmap installation...
nmap --version
if %errorlevel% == 0 (
    echo Nmap is successfully installed and accessible!
) else (
    echo There was an issue accessing Nmap. Please check the installation.
)
pause