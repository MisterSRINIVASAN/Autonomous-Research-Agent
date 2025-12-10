@echo off
echo Starting Backend...
start cmd /k "cd backend && venv\Scripts\activate && python main.py"

echo Starting Frontend...
start cmd /k "cd frontend && npm run dev"

echo Both services started in separate windows!
