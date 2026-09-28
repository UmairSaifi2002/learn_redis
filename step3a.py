import redis

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
r.flushdb()

print("--- 1. Basic push and read ---")
r.rpush('mylist', 'a', 'b', 'c')
r.lpush('mylist', 'z')          # z goes to the front
print("List:", r.lrange('mylist', 0, -1))   # ['z', 'a', 'b', 'c']
print("Length:", r.llen('mylist'))          # 4

print("\n--- 2. Index and slice ---")
print("Index 0:", r.lindex('mylist', 0))    # 'z'
print("Index -1:", r.lindex('mylist', -1))  # 'c'
print("Slice 1..2:", r.lrange('mylist', 1, 2))  # ['a', 'b']

print("\n--- 3. Pop from both ends ---")
print("LPOP:", r.lpop('mylist'))  # 'z'
print("RPOP:", r.rpop('mylist'))  # 'c'
print("Remaining:", r.lrange('mylist', 0, -1))  # ['a', 'b']

print("\n--- 4. FIFO queue (push right, pop left) ---")
r.delete('queue')
r.rpush('queue', 'job1', 'job2', 'job3')
while r.llen('queue') > 0:
    job = r.lpop('queue')
    print("Processing:", job)

print("\n--- 5. LIFO stack (push left, pop left) ---")
r.delete('stack')
r.lpush('stack', 'page1', 'page2', 'page3')
while r.llen('stack') > 0:
    page = r.lpop('stack')
    print("Back to:", page)

print("\n--- 6. Capped list with LTRIM (keep last 3 items) ---")
r.delete('logs')
for i in range(1, 8):
    r.rpush('logs', f"log-{i}")
    r.ltrim('logs', -3, -1)   # keep only the last 3
print("Capped logs:", r.lrange('logs', 0, -1))



