import redis

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
r.flushdb()

def create_user(user_id, name, email):
    key = f"user:{user_id}"
    if r.exists(key):
        print(f"User {user_id} already exists.")
        return
    r.hset(key, mapping={'id': user_id, 'name': name, 'email': email})
    print(f"Created user {user_id}: {name}")

def get_user(user_id):
    data = r.hgetall(f"user:{user_id}")
    return data if data else None

def update_user(user_id, **fields):
    key = f"user:{user_id}"
    if not r.exists(key):
        print(f"User {user_id} not found.")
        return
    r.hset(key, mapping=fields)
    print(f"Updated user {user_id}: {fields}")

def delete_user(user_id):
    removed = r.delete(f"user:{user_id}")
    print(f"Deleted user {user_id}." if removed else f"User {user_id} not found.")

def list_all_users():
    # Note: KEYS is fine for learning; in production use SCAN
    keys = r.keys("user:*")
    print(f"Total users: {len(keys)}")
    for k in keys:
        print(f"  {k} -> {r.hgetall(k)}")

# Demo
create_user(1, "Alice", "alice@example.com")
create_user(2, "Bob", "bob@example.com")
create_user(3, "Carol", "carol@example.com")

print("\nFetch user 2:", get_user(2))

update_user(2, email="bob.new@example.com", city="Bangalore")
print("After update:", get_user(2))

print()
list_all_users()

print()
delete_user(3)
list_all_users()


