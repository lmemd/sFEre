@echo off
echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing dependencies from requirements.txt...
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo =========================================
echo Virtual environment setup complete!
echo To activate it later, run:
echo     venv\Scripts\activate
echo =========================================
pause
