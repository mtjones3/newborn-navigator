@echo off
cd /d "%~dp0"
start "" http://127.0.0.1:3000/my-updates/f7e7ff7656d9481684cea6b54f735d17?week=5
venv\Scripts\python -m uvicorn app.main:app --host 127.0.0.1 --port 3000
