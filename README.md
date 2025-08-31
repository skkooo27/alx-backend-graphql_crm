# CRM Setup Guide

This guide provides the steps to set up and run the CRM application.

## Prerequisites

- Python 3.x
- Redis server
- Virtual environment (recommended)

## Setup Steps

### 1. Install Redis and Dependencies

First, install Redis on your system. On Windows, you can use Chocolatey or download from the official site. On Linux/Mac, use your package manager.

Then, install the Python dependencies including celery and django-celery-beat:

```bash
pip install -r requirements.txt
```

Make sure your `requirements.txt` includes:

```
celery
django-celery-beat
```

### 2. Update Django Settings

Add `django_celery_beat` to your `INSTALLED_APPS` in `crm/settings.py`:

```python
INSTALLED_APPS = [
    # other apps
    'django_celery_beat',
]
```

### 3. Run Migrations

Apply the database migrations including those for django-celery-beat:

```bash
python manage.py migrate
```

### 4. Configure Celery

Create `crm/celery.py` to initialize the Celery app with Redis as the broker:

```python
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')

app = Celery('crm')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

Update `crm/__init__.py` to load the Celery app:

```python
from .celery import app as celery_app

__all__ = ('celery_app',)
```

### 5. Define the Celery Task

In `crm/tasks.py`, define a task `generate_crm_report` that:

- Uses a GraphQL query to fetch:
  - Total number of customers
  - Total number of orders
  - Total revenue (sum of totalamount from orders)
- Logs the report to `/tmp/crm_report_log.txt` with a timestamp in the format `YYYY-MM-DD HH:MM:SS - Report: X customers, Y orders, Z revenue`

### 6. Schedule with Celery Beat

In `crm/settings.py`, configure the Celery beat schedule:

```python
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'generate-crm-report': {
        'task': 'crm.tasks.generate_crm_report',
        'schedule': crontab(day_of_week='mon', hour=6, minute=0),
    },
}
```

### 7. Start Celery Worker

Start the Celery worker to process background tasks:

```bash
celery -A crm worker -l info
```

### 8. Start Celery Beat

Start Celery Beat for scheduled tasks:

```bash
celery -A crm beat -l info
```

### 9. Verify Logs

Check the logs in the specified file to ensure everything is running correctly:

```bash
tail -f /tmp/crm_report_log.txt
```

## Running the Application

After completing the setup steps, you can run the Django development server:

```bash
python manage.py runserver
```


