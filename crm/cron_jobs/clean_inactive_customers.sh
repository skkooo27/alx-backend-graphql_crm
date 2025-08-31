#!/bin/bash

# Script to clean inactive customers (no orders in the last year)
# Run with: ./clean_inactive_customers.sh

# Get the directory of the script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")/.."  # Assuming crm is in project root

# Change to project directory
cd "$PROJECT_DIR"

# Execute Django shell command to delete inactive customers
count=$(python manage.py shell -c "
from crm.models import Customer
from datetime import datetime, timedelta
cutoff = datetime.now() - timedelta(days=365)
deleted = Customer.objects.filter(order__isnull=True, created_at__lt=cutoff).delete()
print(deleted[0])
")

# Log the result
echo "$(date '+%Y-%m-%d %H:%M:%S') - Deleted $count inactive customers" >> /tmp/customer_cleanup_log.txt

echo "Customer cleanup completed. Deleted $count customers."
