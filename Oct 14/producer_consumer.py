import threading
import queue
import time
import random

# Create a shared queue
q = queue.Queue()

# Producer function
def producer():
    for i in range(5):
        item = f"Task-{i}"
        print(f"Producer: producing {item}")
        q.put(item)  # Add item to queue
        time.sleep(random.uniform(0.5, 1.5))
    q.put(None)  # Sentinel to signal consumer to stop
    print("Producer: finished producing\n")

# Consumer function
def consumer():
    while True:
        item = q.get()  # Wait for item
        if item is None:
            print("Consumer: no more items, exiting\n")
            break
        print(f"Consumer: processing {item}")
        time.sleep(random.uniform(1, 2))
        q.task_done()

# Create threads
producer_thread = threading.Thread(target=producer)
consumer_thread = threading.Thread(target=consumer)

# Start threads
producer_thread.start()
consumer_thread.start()

# Wait for threads to finish
producer_thread.join()
consumer_thread.join()

print("All work completed.")
