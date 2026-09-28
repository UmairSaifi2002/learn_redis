import redis
import time

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

print("Consumer: waiting for jobs (timeout 10s per pop, Ctrl+C to exit)...")

while True:
    # BLPOP blocks until an item is available or timeout hits
    result = r.blpop('jobs', timeout=10)
    if result is None:
        print("Consumer: timeout, no job arrived. Still waiting...")
        continue
    # result is a tuple: (key, value)
    queue_name, job = result
    print(f"Consumer: picked up '{job}' from '{queue_name}'")
    # Simulate work
    time.sleep(1)
    print(f"Consumer: finished '{job}'")


    