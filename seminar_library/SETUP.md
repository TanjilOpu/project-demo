# MBSTU Seminar Library — Setup Guide

## 1. Install Python dependencies
```bash
pip install -r requirements.txt
```

## 2. Create MySQL database
Log into MySQL and run:
```sql
CREATE DATABASE seminar_library_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## 3. Configure settings
Open `seminar_library/settings.py` and update:
- `DATABASES['default']['PASSWORD']` → your MySQL password
- `EMAIL_HOST_USER` → your Gmail address
- `EMAIL_HOST_PASSWORD` → your Gmail App Password (not your normal password)
- `SITE_URL` → your server URL in production

## 4. Run migrations
```bash
python manage.py makemigrations accounts books
python manage.py migrate
```

## 5. Create a librarian account
```bash
python manage.py createsuperuser
```
Enter an email (any), name, and password.
Then in Django shell, set role to admin:
```bash
python manage.py shell
```
```python
from accounts.models import User
u = User.objects.get(email='it23044@mbstu.ac.bd')
u.role = 'admin'
u.is_verified = True
u.save()
```

## 6. Start the development server
```bash
python manage.py runserver
```

## 7. Start Redis (required for Celery)
```bash
redis-server
```

## 8. Start Celery worker (in a new terminal)
```bash
celery -A seminar_library worker --loglevel=info
```

## 9. Start Celery Beat scheduler (in another terminal)
```bash
celery -A seminar_library beat --loglevel=info
```

## URLs
- Public catalogue:     http://localhost:8000/
- Student login:        http://localhost:8000/accounts/login/
- Student register:     http://localhost:8000/accounts/register/
- Student borrows:      http://localhost:8000/books/my-borrows/
- Librarian dashboard:  http://localhost:8000/librarian/
- Librarian books:      http://localhost:8000/librarian/books/
- Librarian students:   http://localhost:8000/librarian/students/

## Gmail App Password setup
1. Go to your Google Account → Security
2. Enable 2-Step Verification
3. Go to App Passwords → Generate one for "Mail"
4. Use that 16-character password in EMAIL_HOST_PASSWORD
