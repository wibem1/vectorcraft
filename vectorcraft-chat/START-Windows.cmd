@echo off
cd /d "%~dp0"
py -3 vectorcraft_chat.py
if errorlevel 1 pause
