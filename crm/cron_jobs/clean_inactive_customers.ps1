# PowerShell script to run the customer cleanup management command
# Run with: .\clean_inactive_customers.ps1

# Change to the project directory
Set-Location "C:\Users\Administrator\Desktop\sharline\alx-backend-graphql_crm"

# Run the Django management command
& python manage.py clean_inactive_customers
