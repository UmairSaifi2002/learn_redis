import redis

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
r.flushdb()

print("--- 1. Create a user profile ---")
r.hset('user:1', mapping={
    'name': 'Alice',
    'email': 'alice@example.com',
    'age': 30,
    'city': 'Mumbai'
})
print("Created user:1")

print("\n--- 2. Read a single field ---")
print("Name:", r.hget('user:1', 'name'))

print("\n--- 3. Read multiple fields ---")
print("Name + city:", r.hmget('user:1', 'name', 'city'))

print("\n--- 4. Read ALL fields ---")
print("Full profile:", r.hgetall('user:1'))

print("\n--- 5. Field-level operations ---")
print("Field count (HLEN):", r.hlen('user:1'))
print("Field names (HKEYS):", r.hkeys('user:1'))
print("Field values (HVALS):", r.hvals('user:1'))
print("Does 'email' exist?", r.hexists('user:1', 'email'))
print("Does 'phone' exist?", r.hexists('user:1', 'phone'))

print("\n--- 6. Update a single field ---")
r.hset('user:1', 'city', 'Delhi')
print("Updated city:", r.hget('user:1', 'city'))

print("\n--- 7. Increment a numeric field ---")
r.hincrby('user:1', 'age', 1)
print("Age after birthday:", r.hget('user:1', 'age'))

print("\n--- 8. Delete a field ---")
r.hdel('user:1', 'city')
print("After HDEL city:", r.hgetall('user:1'))

print("\n--- 9. HSETNX: only set field if it doesn't exist ---")
print("Set 'name' with HSETNX:", r.hsetnx('user:1', 'name', 'Bob'))     # 0 (already exists)
print("Set 'phone' with HSETNX:", r.hsetnx('user:1', 'phone', '99999')) # 1 (new field)
print("Name unchanged:", r.hget('user:1', 'name'))  # still 'Alice'
print("Phone added:", r.hget('user:1', 'phone'))

print("\n--- 10. Delete the whole hash ---")
r.delete('user:1')
print("After delete, exists?", r.exists('user:1'))  # 0



