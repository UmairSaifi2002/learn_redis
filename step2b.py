import redis
import time

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
r.flushdb()

print("--- 1. Basic counters ---")
r.set('page:views', 0)
r.incr('page:views')
r.incr('page:views')
r.incrby('page:views', 10)
print("Views:", r.get('page:views'))   # 12

r.decr('page:views')
r.decrby('page:views', 5)
print("After decrement:", r.get('page:views'))  # 6

print("\n--- 2. INCR on a non-existent key ---")
r.delete('fresh_counter')
r.incr('fresh_counter')      # starts from 0 → 1
r.incr('fresh_counter')
print("Fresh counter:", r.get('fresh_counter'))  # 2

print("\n--- 3. INCRBYFLOAT ---")
r.set('price', '10.50')
r.incrbyfloat('price', 0.75)
print("Price:", r.get('price'))  # 11.25

print("\n--- 4. INCR on a non-numeric value (this will fail) ---")
r.set('notanumber', 'hello')
try:
    r.incr('notanumber')
except redis.exceptions.ResponseError as e:
    print("Redis error (expected):", e)

print("\n--- 5. Real-world pattern: Rate Limiter ---")

def is_rate_limited(user_id, limit=5, window_seconds=60):
    """
    Allow at most `limit` requests per `window_seconds` per user.
    Returns True if the user is over the limit.
    """
    key = f"ratelimit:{user_id}"
    # Atomically increment. If the key is new, this returns 1.
    current = r.incr(key)
    # Only set expiry when the key is first created (current == 1)
    if current == 1:
        r.expire(key, window_seconds)
    return current > limit

# Simulate 7 requests from the same user
for i in range(1, 8):
    limited = is_rate_limited("alice", limit=5, window_seconds=60)
    print(f"Request {i}: limited = {limited}")

print("\nTTL on alice's counter:", r.ttl("ratelimit:alice"))

print("\n--- 6. Proving INCR is atomic (concurrent) ---")
import threading

r.delete('atomic_test')

def hammer():
    for _ in range(1000):
        r.incr('atomic_test')

threads = [threading.Thread(target=hammer) for _ in range(5)]
for t in threads: t.start()
for t in threads: t.join()

print("Final value (should be 5000):", r.get('atomic_test'))



