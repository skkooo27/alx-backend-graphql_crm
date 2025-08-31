from celery import shared_task
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import datetime

@shared_task
def generate_crm_report():
    # GraphQL endpoint
    transport = RequestsHTTPTransport(url='http://localhost:8000/graphql', verify=True, retries=3)
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # GraphQL query to get total customers, orders, revenue
    query = gql(
        """
        query {
            totalCustomers
            totalOrders
            totalRevenue
        }
        """
    )

    try:
        result = client.execute(query)
        total_customers = result.get('totalCustomers', 0)
        total_orders = result.get('totalOrders', 0)
        total_revenue = result.get('totalRevenue', 0.0)

        # Log the report
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        report = f"{timestamp} - Report: {total_customers} customers, {total_orders} orders, {total_revenue} revenue"
        with open('/tmp/crm_report_log.txt', 'a') as f:
            f.write(report + '\n')
    except Exception as e:
        # Log error
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open('/tmp/crm_report_log.txt', 'a') as f:
            f.write(f"{timestamp} - Error generating report: {e}\n")
