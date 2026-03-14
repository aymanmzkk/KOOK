@echo off
cd /d C:\Users\Lenovo\KOOK
echo ========================================
echo Iniciando Waitress para KOOK
echo ========================================
waitress-serve --host=127.0.0.1 --port=8000 wsgi:app
pause