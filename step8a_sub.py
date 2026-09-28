import redis

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
pubsub = r.pubsub()

pubsub.subscribe('news')
print("Subscribed to 'news'. Waiting for messages... (Ctrl+C to exit)")

for message in pubsub.listen():
    print(f"[RECEIVED] {message}")