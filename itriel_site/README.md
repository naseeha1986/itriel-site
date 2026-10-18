# ITRIEL CONSULTING – Django site

    python -m venv venv
    venv\Scripts\activate          # macOS/Linux: source venv/bin/activate
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py seed_content  # loads all 10 pages of PDF content
    python manage.py createsuperuser   # optional, for /admin/
    python manage.py runserver

Open http://127.0.0.1:8000/
