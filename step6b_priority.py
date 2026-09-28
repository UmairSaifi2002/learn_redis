import redis
import time

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
r.flushdb()

def enqueue(queue, task_name, priority):
    """
    priority: 1 (low) .. 10 (high)
    Same priority -> older first.
    """
    ts = time.time()
    # Composite score:
    #   Big part: priority (higher wins)
    #   Small part: inverse timestamp so older wins on tie
    score = priority * 10**12 + (10**12 - ts)
    member = f"{task_name}@{ts}"
    r.zadd(queue, {member: score})
    return member

def dequeue(queue):
    """Pop highest-priority task."""
    result = r.zpopmax(queue)
    if not result:
        return None
    member, score = result[0]
    # Decode priority back out (optional)
    return member

# Enqueue some tasks
enqueue('jobs', 'send-email',      priority=5)
time.sleep(0.1)
enqueue('jobs', 'resize-image',    priority=3)
time.sleep(0.1)
enqueue('jobs', 'process-payment', priority=10)
time.sleep(0.1)
enqueue('jobs', 'send-email',      priority=5)   # second email, same priority
time.sleep(0.1)
enqueue('jobs', 'cleanup-temp',    priority=1)

print("Job queue (highest score = highest priority):")
for member, score in r.zrevrange('jobs', 0, -1, withscores=True):
    print(f"  score={score:.2f}  {member}")

print("\nDequeuing in priority order:")
while True:
    task = dequeue('jobs')
    if task is None:
        break
    print(f"  -> {task}")



    