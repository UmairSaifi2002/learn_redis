import redis
import sys

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
pubsub = r.pubsub()

# Subscribe to every channel that starts with "user:"
pubsub.psubscribe('user:*')

print("Listening on pattern 'user:*'. Waiting for messages... (Ctrl+C to exit)")

for message in pubsub.listen():
    if message['type'] != 'pmessage':
        # 'pmessage' = message delivered via pattern subscription
        # 'message'  = message delivered via direct subscription
        continue
    print(f"[PATTERN {message['pattern']}] "
          f"channel={message['channel']}  data={message['data']}")



          