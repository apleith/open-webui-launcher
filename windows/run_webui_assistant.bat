@echo off
cd /d "%~dp0"
powershell -WindowStyle Hidden -Command "Start-Process python -WindowStyle Hidden '../common/splash_screen.py'"
exit
