@echo off
cd /d "%~dp0.."
py -3 -m venv .venv
call .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r backend\requirements.txt
pip install -r windows\requirements-desktop.txt
pause
