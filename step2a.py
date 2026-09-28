import redis
import time

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Clean slate for this demo
r.flushdb()

print("--- 1. Basic SET / GET ---")
r.set('user:1:name', 'Alice')
r.set('user:1:city', 'Mumbai')
print("Name:", r.get('user:1:name'))
print("City:", r.get('user:1:city'))

print("\n--- 2. Multiple SET / GET ---")
r.mset({'user:2:name': 'Bob', 'user:2:city': 'Delhi'})
print("User 2:", r.mget('user:2:name', 'user:2:city'))

print("\n--- 3. SET with expiration (5 seconds) ---")
r.set('otp:12345', '987654', ex=5)
print("OTP value:", r.get('otp:12345'))
print("TTL (seconds left):", r.ttl('otp:12345'))

print("\n--- 4. Waiting 6 seconds... ---")
time.sleep(6)
print("OTP after 6s:", r.get('otp:12345'))     # None (expired)
print("TTL after expiry:", r.ttl('otp:12345'))  # -2 means key does not exist

print("\n--- 5. SETNX (only if not exists) ---")
print("First attempt:", r.set('lock', 'worker-A', nx=True))  # True
print("Second attempt:", r.set('lock', 'worker-B', nx=True)) # None
print("Lock value:", r.get('lock'))  # still 'worker-A'

print("\n--- 6. EXISTS & DELETE ---")
print("Exists user:1:name?", r.exists('user:1:name'))  # 1
r.delete('user:1:name')
print("After delete, exists?", r.exists('user:1:name'))  # 0

print("\n--- 7. PERSIST (remove expiration) ---")
r.set('temp', 'value', ex=100)
print("TTL before persist:", r.ttl('temp'))
r.persist('temp')
print("TTL after persist:", r.ttl('temp'))  # -1 means no expiration



