import redis
import sys

name = sys.argv[1] if len(sys.argv) > 1 else "sub"
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
pubsub = r.pubsub()

pubsub.subscribe('news', 'sports')
print(f"[{name}] Subscribed to 'news' and 'sports'. Waiting...")

for message in pubsub.listen():
    if message['type'] != 'message':
        continue
    print(f"[{name}] {message['channel']}: {message['data']}")


    