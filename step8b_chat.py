import redis
import sys
import threading
import time

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

HISTORY_KEY = "chat:history:{room}"      # List of last N messages per room
HISTORY_SIZE = 20                        # keep the last 20 messages

def room_channel(room):
    return f"chat:room:{room}"

def history_key(room):
    return f"chat:history:{room}"

def post_message(room, user, text):
    """Publish a message and store it in the room history."""
    msg = f"{user}: {text}"
    r.publish(room_channel(room), msg)
    # Keep a bounded list of the last N messages
    r.rpush(history_key(room), msg)
    r.ltrim(history_key(room), -HISTORY_SIZE, -1)
    return msg

def get_history(room, count=HISTORY_SIZE):
    return r.lrange(history_key(room), -count, -1)

def listen(room, username):
    """Subscribe to a room and print messages as they arrive."""
    pubsub = r.pubsub()
    pubsub.subscribe(room_channel(room))

    print(f"[{username}] Joined '{room}'. Recent history:")
    for h in get_history(room):
        print(f"  (history) {h}")

    # Run the listener in a background thread so we can also send
    def listener():
        for message in pubsub.listen():
            if message['type'] == 'message':
                print(f"  {message['data']}")

    t = threading.Thread(target=listener, daemon=True)
    t.start()
    return t, pubsub

def interactive(room, username):
    thread, pubsub = listen(room, username)
    try:
        while True:
            text = input()
            if text.strip() == "":
                continue
            if text == "/quit":
                break
            post_message(room, username, text)
    except (EOFError, KeyboardInterrupt):
        pass
    finally:
        pubsub.unsubscribe()
        pubsub.close()
        print(f"[{username}] Left '{room}'.")

# --- CLI entry point ---
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python step8b_chat.py <room> <username>")
        sys.exit(1)

    room = sys.argv[1]
    username = sys.argv[2]
    interactive(room, username)



    