@echo off
setlocal
cd /d "%~dp0"
set "VECTORCRAFT_CONFIG_DIR=%~dp0profile"
set "RUST_LOG=warn,vectorcraft*=info"
start "VectorCraft Live Repeat Test" "%~dp0VectorCraft-LiveRepeat.exe" --control 17979 --in-window-menus
