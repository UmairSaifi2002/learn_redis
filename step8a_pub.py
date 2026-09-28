import redis
import sys

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

msg = sys.argv[1] if len(sys.argv) > 1 else "Hello, world!"
receivers = r.publish('news', msg)
print(f"Published: '{msg}'  →  {receivers} subscriber(s) received it.")