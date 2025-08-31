# CRM Setup Guide

This guide provides the steps to set up and run the CRM application.

## Prerequisites

- Python 3.x
- Redis server
- Virtual environment (recommended)

## Setup Steps

### 1. Install Redis and Dependencies

First, install Redis on your system. On Windows, you can use Chocolatey or download from the official site. On Linux/Mac, use your package manager.

Then, install the Python dependencies:

```bash
pip install -r requirements.txt
```

### 2. Run Migrations

Apply the database migrations:

```bash
python manage.py migrate
```

### 3. Start Celery Worker

Start the Celery worker to process background tasks:

```bash
celery -A crm worker -l info
```

### 4. Start Celery Beat

Start Celery Beat for scheduled tasks:

```bash
celery -A crm beat -l info
```

### 5. Verify Logs

Check the logs in the specified file to ensure everything is running correctly:

```bash
tail -f /tmp/crm_report_log.txt
```

## Running the Application

After completing the setup steps, you can run the Django development server:

```bash
python manage.py runserver
```

Ensure all services (Redis, Celery worker, Celery beat) are running in the background.
