@echo off
cd /d "%~dp0"
echo ========================================
echo Iniciando Waitress para KOOK
echo ========================================
waitress-serve --host=127.0.0.1 --port=8000 app:app
pause
