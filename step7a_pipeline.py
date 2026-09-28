import redis
import time

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
r.flushdb()

N = 1000

print(f"Running {N} SET operations...\n")

# --- Approach 1: No pipeline (one round-trip per command) ---
start = time.time()
for i in range(N):
    r.set(f'plain:{i}', i)
plain_time = time.time() - start
print(f"Without pipeline: {plain_time:.3f} seconds")

# --- Approach 2: With pipeline ---
r.flushdb()
start = time.time()
pipe = r.pipeline()
for i in range(N):
    pipe.set(f'pipe:{i}', i)
pipe.execute()
pipe_time = time.time() - start
print(f"With pipeline:    {pipe_time:.3f} seconds")

print(f"\nSpeedup: {plain_time / pipe_time:.1f}x faster")