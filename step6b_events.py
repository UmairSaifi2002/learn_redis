import redis
import time

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
r.flushdb()

def log_event(event_type, payload):
    """Log an event with the current timestamp as its score."""
    ts = time.time()
    # Member must be unique; include a nanosecond suffix to avoid collisions
    member = f"{event_type}:{int(ts * 1000)}:{payload}"
    r.zadd('events', {member: ts})
    return ts

def recent_events(seconds=60):
    """Events in the last `seconds`."""
    now = time.time()
    rows = r.zrangebyscore('events', now - seconds, now, withscores=True)
    return [(m, round(now - s, 2)) for m, s in rows]   # (event, age in seconds)

def cleanup_old(seconds=3600):
    """Remove events older than `seconds`."""
    cutoff = time.time() - seconds
    removed = r.zremrangebyscore('events', '-inf', cutoff)
    return removed

# Log a bunch of events
print("Logging events...")
log_event('login', 'user1')
time.sleep(0.3)
log_event('view', 'user1:pageA')
log_event('view', 'user2:pageB')
time.sleep(0.3)
log_event('purchase', 'user1:item42')
log_event('logout', 'user2')

print("\nAll events in order (oldest first):")
for member, score in r.zrange('events', 0, -1, withscores=True):
    print(f"  ts={round(score, 3)}  {member}")

print("\nLast 1 second of events:")
for event, age in recent_events(1):
    print(f"  {event}  (age: {age}s)")

print("\nMost recent event only:")
print(" ", r.zrevrange('events', 0, 0))

print("\nCleanup events older than 0.5 seconds:")
removed = cleanup_old(0.5)
print(f"  Removed {removed} events")
print("  Remaining:", r.zcard('events'))