import redis

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
r.flushdb()

print("--- 1. A simple transaction ---")
# In redis-py, pipeline(transaction=True) is the DEFAULT.
# So r.pipeline() IS a transaction.
pipe = r.pipeline()   # transaction=True by default
pipe.set('a', 1)
pipe.incr('a')
pipe.incr('a')
pipe.get('a')
results = pipe.execute()
print("Results:", results)   # [True, 2, 3, '3']
print("Final value of a:", r.get('a'))

print("\n--- 2. Same thing, explicitly marked ---")
pipe = r.pipeline(transaction=True)
pipe.set('b', 10)
pipe.incrby('b', 5)
pipe.get('b')
print(pipe.execute())   # [True, 15, '15']

print("\n--- 3. Pipeline WITHOUT transaction ---")
# No MULTI/EXEC wrapping. Just batching.
pipe = r.pipeline(transaction=False)
pipe.set('c', 100)
pipe.incr('c')
pipe.get('c')
print(pipe.execute())   # [True, 101, '101']

print("\n--- 4. What happens if a queued command is invalid? ---")
pipe = r.pipeline()
pipe.set('str', 'hello')
pipe.incr('str')          # This will fail at EXEC time (not queue time)
pipe.set('after', 'ok')
try:
    results = pipe.execute()
    print("Results:", results)
except redis.exceptions.ResponseError as e:
    print("Error during EXEC:", e)

print("\nDid 'after' still get set?")
print("  after =", r.get('after'))
print("  str   =", r.get('str'))



