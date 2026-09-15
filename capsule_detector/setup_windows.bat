@echo off
python -m venv .venv
call .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
echo.
echo CapsuleSight is ready. Run: .venv\Scripts\activate then python manage.py runserver
