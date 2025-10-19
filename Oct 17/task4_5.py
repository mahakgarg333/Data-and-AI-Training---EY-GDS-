import pandas as pd
import queue
import threading
import logging
import time

# ---------------- LOGGING CONFIGURATION ----------------
logging.basicConfig(
    filename="order_processing.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ---------------- QUEUE SETUP ----------------
order_queue = queue.Queue()

# ---------------- LOAD DATA ----------------
products = pd.read_csv("products.csv")
customers = pd.read_csv("customers.csv")
orders = pd.read_csv("orders.csv")

# ---------------- PRODUCER FUNCTION ----------------
def producer():
    for _, order in orders.iterrows():
        logging.info(f"New order received: {order['OrderID']}")
        order_queue.put(order)
        time.sleep(1)  # Simulate delay in receiving orders
    logging.info(" All orders pushed to queue.")

# ---------------- CONSUMER FUNCTION ----------------
def consumer():
    processed_orders = []

    while True:
        try:
            order = order_queue.get(timeout=5)
        except queue.Empty:
            logging.info("Queue empty. No more orders to process.")
            break

        try:
            # Validate ProductID
            product_row = products[products["ProductID"] == order["ProductID"]]
            if product_row.empty:
                logging.error(f" ProductID {order['ProductID']} not found for Order {order['OrderID']}")
                continue

            # Get product details
            price = float(product_row["Price"].values[0])
            total_price = order["Quantity"] * price

            # Enrich order data
            order_data = {
                "OrderID": order["OrderID"],
                "CustomerID": order["CustomerID"],
                "ProductID": order["ProductID"],
                "Quantity": order["Quantity"],
                "OrderDate": order["OrderDate"],
                "TotalPrice": total_price
            }

            processed_orders.append(order_data)
            logging.info(f" Processed Order {order['OrderID']} successfully with TotalPrice = {total_price}")

        except Exception as e:
            logging.error(f" Error processing order {order['OrderID']}: {str(e)}")

        order_queue.task_done()
        time.sleep(2)  # Simulate processing time

    # Save processed orders to CSV
    df = pd.DataFrame(processed_orders)
    if not df.empty:
        df.to_csv("processed_orders.csv", index=False)
        logging.info(f" Saved {len(df)} processed orders to processed_orders.csv")

# ---------------- RUN PRODUCER & CONSUMER ----------------
if __name__ == "__main__":
    start_time = time.time()
    logging.info(" Order processing started.")

    producer_thread = threading.Thread(target=producer)
    consumer_thread = threading.Thread(target=consumer)

    producer_thread.start()
    consumer_thread.start()

    producer_thread.join()
    consumer_thread.join()

    duration = round(time.time() - start_time, 2)
    logging.info(f" ETL process completed in {duration} seconds.")
    print(f"Order processing completed in {duration} seconds. Check 'order_processing.log' for details.")
