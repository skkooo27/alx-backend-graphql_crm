# TODO List for Cron Tasks Implementation

## Task 0: Schedule a Customer Cleanup Script
- [x] Create crm/cron_jobs/clean_inactive_customers.sh (shell script to delete inactive customers and log)
- [x] Create crm/cron_jobs/customer_cleanup_crontab.txt (crontab entry for Sunday 2:00 AM)
- [x] Make clean_inactive_customers.sh executable (chmod +x) - Note: On Windows, use bash environment like Git Bash or WSL

## Task 1: Schedule a GraphQL-Based Order Reminder Script
- [x] Create crm/cron_jobs/send_order_reminders.py (Python script to query GraphQL for pending orders and log)
- [x] Create crm/cron_jobs/order_reminders_crontab.txt (crontab entry for daily 8:00 AM)

## Task 2: Heartbeat Logger with django-crontab
- [x] Update requirements.txt to include django-crontab
- [x] Update crm/settings.py to add django_crontab to INSTALLED_APPS and configure CRONJOBS for heartbeat
- [x] Create crm/cron.py with log_crm_heartbeat function

## Task 3: Schedule a GraphQL Mutation for Product Stock Alerts
- [x] Update crm/schema.py to add UpdateLowStockProducts mutation
- [x] Update crm/cron.py to add update_low_stock function
- [x] Update crm/settings.py to add CRONJOBS for low-stock updates
- [x] Update requirements.txt to include gql library

## General
- [x] Ensure all files are created in correct directories
- [ ] Test scripts and cron jobs (user action)
- [ ] Install dependencies and run migrations if needed (user action)
- [ ] Update absolute paths in crontab files (user action)
