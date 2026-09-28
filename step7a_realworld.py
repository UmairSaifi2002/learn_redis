import redis
import time

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
r.flushdb()

# Preload 500 user records as hashes
pipe = r.pipeline()
for i in range(500):
    pipe.hset(f'user:{i}', mapping={'id': i, 'name': f'user{i}', 'score': i * 10})
pipe.execute()

# Now fetch 200 random users
import random
random.seed(42)
ids = random.sample(range(500), 200)

# --- Naive ---
start = time.time()
results = []
for i in ids:
    results.append(r.hgetall(f'user:{i}'))
print(f"Naive HGETALL x200: {time.time() - start:.3f}s")

# --- With pipeline ---
start = time.time()
pipe = r.pipeline()
for i in ids:
    pipe.hgetall(f'user:{i}')
results = pipe.execute()
print(f"Pipelined HGETALL x200: {time.time() - start:.3f}s")

# Compare contents
print("First record (naive):", results[0])


