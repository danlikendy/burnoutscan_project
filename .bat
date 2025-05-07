@echo off
cd /d "%~dp0"

echo Запуск FastAPI backend...
start cmd /k "cd api && uvicorn main:app --reload"

timeout /t 3

echo Запуск одиночного Streamlit-прогноза...
start cmd /k "streamlit run apps/streamlit_app.py"

timeout /t 2

echo Запуск массового Streamlit-прогноза...
start cmd /k "streamlit run apps/bulk_prediction_app.py"