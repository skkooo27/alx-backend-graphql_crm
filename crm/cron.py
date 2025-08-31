import datetime
import logging
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def log_crm_heartbeat():
    # Log heartbeat message
    timestamp = datetime.datetime.now().strftime('%d/%m/%Y-%H:%M:%S')
    message = f"{timestamp} CRM is alive"
    with open('/tmp/crm_heartbeat_log.txt', 'a') as f:
        f.write(message + '\n')

    # Optionally, query GraphQL hello field
    try:
        transport = RequestsHTTPTransport(url='http://localhost:8000/graphql', verify=True, retries=3)
        client = Client(transport=transport, fetch_schema_from_transport=True)
        query = gql(
            """
            query {
                hello
            }
            """
        )
        result = client.execute(query)
        if result.get('hello'):
            with open('/tmp/crm_heartbeat_log.txt', 'a') as f:
                f.write(f"{timestamp} GraphQL endpoint is responsive\n")
    except Exception as e:
        with open('/tmp/crm_heartbeat_log.txt', 'a') as f:
            f.write(f"{timestamp} Error checking GraphQL endpoint: {e}\n")

def update_low_stock():
    # Execute UpdateLowStockProducts mutation
    transport = RequestsHTTPTransport(url='http://localhost:8000/graphql', verify=True, retries=3)
    client = Client(transport=transport, fetch_schema_from_transport=True)

    mutation = gql(
        """
        mutation {
            updateLowStockProducts {
                success
                message
                updatedProducts {
                    id
                    name
                    stock
                }
            }
        }
        """
    )

    try:
        result = client.execute(mutation)
        mutation_result = result.get('updateLowStockProducts', {})
        if mutation_result.get('success'):
            updated_products = mutation_result.get('updatedProducts', [])
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open('/tmp/low_stock_updates_log.txt', 'a') as f:
                f.write(f"{timestamp} - Updated products:\n")
                for product in updated_products:
                    f.write(f"  {product['name']}: new stock {product['stock']}\n")
        else:
            logging.error(f"Mutation failed: {mutation_result.get('message')}")
    except Exception as e:
        logging.error(f"Error executing mutation: {e}")
