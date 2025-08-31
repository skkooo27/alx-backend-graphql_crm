# CRM Setup Guide

This guide provides comprehensive steps to set up and run the CRM application with Django, GraphQL, Celery, and Redis.

## Prerequisites
- Python 3.x
- Django
- Redis server
- Git (for cloning if needed)

## Installation Steps

1. **Clone the Repository** (if not already done):
   ```
   git clone <repository-url>
   cd alx-backend-graphql_crm
   ```

2. **Set Up Virtual Environment**:
   ```
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Python Dependencies**:
   ```
   pip install -r requirements.txt
   ```

4. **Set Environment Variables**:
   - Update `crm/settings.py` and replace `SECRET_KEY = 'your-secret-key-here'` with a secure key.
   - Optionally, set `DEBUG = False` for production.

5. **Run Django Migrations**:
   ```
   python manage.py migrate
   ```

6. **Create Superuser** (optional, for admin access):
   ```
   python manage.py createsuperuser
   ```

7. **Install and Start Redis**:
   - On Ubuntu/Debian: `sudo apt-get install redis-server`
   - On macOS: `brew install redis`
   - On Windows: Download from https://redis.io/download and follow installation instructions
   - Start Redis: `redis-server`

8. **Start Django Development Server**:
   ```
   python manage.py runserver
   ```
   The server will run on http://localhost:8000. GraphQL endpoint is available at http://localhost:8000/graphql.

## Running Celery

1. **Start Celery Worker** (in a separate terminal):
   ```
   celery -A crm worker -l info
   ```

2. **Start Celery Beat** (in a separate terminal):
   ```
   celery -A crm beat -l info
   ```

## Cron Jobs and Management Commands

1. **Run Management Command for Cleaning Inactive Customers**:
   ```
   python manage.py clean_inactive_customers
   ```

2. **Set Up Cron Jobs** (using the provided scripts):
   - For customer cleanup: Use `crm/cron_jobs/clean_inactive_customers.sh` or `crm/cron_jobs/customer_cleanup_crontab.txt`
   - For order reminders: Run `python crm/cron_jobs/send_order_reminders.py`

## Verification

- Access GraphQL at http://localhost:8000/graphql to query CRM data.
- The `generate_crm_report` task runs every Monday at 6:00 AM via Celery Beat.
- Check logs in `/tmp/crm_report_log.txt`, `/tmp/customer_cleanup_log.txt`, and `/tmp/order_reminders_log.txt`.
- Manually trigger tasks:
  ```
  celery -A crm call crm.tasks.generate_crm_report
  ```

## Notes
- Ensure Redis is running on `localhost:6379` (default).
- GraphQL queries can be tested using tools like GraphiQL or Postman.
- For production, configure proper environment variables and security settings.
- The application uses SQLite by default; update `DATABASES` in `settings.py` for other databases.
