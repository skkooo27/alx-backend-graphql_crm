from django.core.management.base import BaseCommand
from crm.models import Customer
from datetime import timedelta
from django.utils import timezone
import os

class Command(BaseCommand):
    help = 'Delete inactive customers (no orders in the last year)'

    def handle(self, *args, **options):
        # Calculate cutoff date (1 year ago)
        cutoff = timezone.now() - timedelta(days=365)

        # Delete inactive customers
        deleted_count = Customer.objects.filter(
            order__isnull=True,
            created_at__lt=cutoff
        ).delete()[0]

        # Log the result
        timestamp = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"{timestamp} - Deleted {deleted_count} inactive customers"

        # Ensure log directory exists
        log_dir = '/tmp'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Append to log file
        with open('/tmp/customer_cleanup_log.txt', 'a') as f:
            f.write(log_message + '\n')

        self.stdout.write(
            self.style.SUCCESS(f'Successfully deleted {deleted_count} inactive customers')
        )
