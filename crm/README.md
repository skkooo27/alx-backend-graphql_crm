# CRM Celery Setup Guide

This guide provides steps to set up and run Celery with Redis for the CRM application.

## Prerequisites
- Python 3.x
- Django
- Redis server

## Installation Steps

1. **Install Redis**:
   - On Ubuntu/Debian: `sudo apt-get install redis-server`
   - On macOS: `brew install redis`
   - On Windows: Download from https://redis.io/download and follow installation instructions
   - Start Redis: `redis-server`

2. **Install Python Dependencies**:
   ```
   pip install -r requirements.txt
   ```

3. **Run Django Migrations**:
   ```
   python manage.py migrate
   ```

## Running Celery

1. **Start Celery Worker**:
   ```
   celery -A crm worker -l info
   ```

2. **Start Celery Beat** (in a separate terminal):
   ```
   celery -A crm beat -l info
   ```

## Verification

- The `generate_crm_report` task is scheduled to run every Monday at 6:00 AM.
- Check the logs in `/tmp/crm_report_log.txt` for the generated reports.
- You can also manually trigger the task for testing:
  ```
  celery -A crm call crm.tasks.generate_crm_report
  ```

## Notes
- Ensure Redis is running on `localhost:6379` (default).
- The task uses GraphQL queries to fetch CRM data.
- Logs are appended to `/tmp/crm_report_log.txt`.
