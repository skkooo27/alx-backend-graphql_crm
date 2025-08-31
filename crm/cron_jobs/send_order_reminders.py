import datetime
import logging
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# Configure logging
logging.basicConfig(filename='/tmp/order_reminders_log.txt', level=logging.INFO, format='%(asctime)s %(message)s')

def main():
    # GraphQL endpoint
    transport = RequestsHTTPTransport(url='http://localhost:8000/graphql', verify=True, retries=3)
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # Calculate date 7 days ago
    seven_days_ago = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%d')

    # GraphQL query to get orders with order_date within last 7 days
    query = gql(
        """
        query getRecentOrders($date: Date!) {
            orders(orderDate_Gte: $date) {
                id
                customer {
                    email
                }
            }
        }
        """
    )

    params = {"date": seven_days_ago}

    try:
        result = client.execute(query, variable_values=params)
        orders = result.get('orders', [])
        for order in orders:
            order_id = order['id']
            customer_email = order['customer']['email']
            log_msg = f"Order ID: {order_id}, Customer Email: {customer_email}"
            logging.info(log_msg)
        print("Order reminders processed!")
    except Exception as e:
        logging.error(f"Error fetching orders: {e}")
        print("Failed to process order reminders.")

if __name__ == "__main__":
    main()
