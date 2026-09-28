import redis

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
r.flushdb()

print("--- 1. Basic set operations ---")
r.sadd('fruits', 'apple', 'banana', 'cherry')
r.sadd('fruits', 'apple', 'date')      # 'apple' is a duplicate, ignored
print("Fruits:", r.smembers('fruits'))
print("Size:", r.scard('fruits'))       # 4

print("\n--- 2. Membership test ---")
print("Is 'banana' in fruits?", r.sismember('fruits', 'banana'))  # 1
print("Is 'kiwi' in fruits?", r.sismember('fruits', 'kiwi'))      # 0
print("Multiple:", r.smismember('fruits', ['apple', 'kiwi']))     # [1, 0]

print("\n--- 3. Remove a member ---")
r.srem('fruits', 'date')
print("After SREM date:", r.smembers('fruits'))
print("Size:", r.scard('fruits'))  # 3

print("\n--- 4. Set operations ---")

# Two users' friends
r.sadd('alice:friends', 'bob', 'carol', 'dave')
r.sadd('bob:friends',   'alice', 'carol', 'eve')

print("Alice's friends:", r.smembers('alice:friends'))
print("Bob's friends:  ", r.smembers('bob:friends'))

print("\nUnion (all unique friends of both):")
print(r.sunion('alice:friends', 'bob:friends'))

print("\nIntersection (mutual friends):")
print(r.sinter('alice:friends', 'bob:friends'))     # {'carol'}

print("\nDifference (Alice's friends minus Bob's):")
print(r.sdiff('alice:friends', 'bob:friends'))      # {'bob', 'dave'}

print("\n--- 5. Random members ---")
print("Random sample (SRANDMEMBER):", r.srandmember('fruits', 2))
print("Set unchanged:", r.smembers('fruits'))

print("\n--- 6. SPOP removes a random member ---")
popped = r.spop('fruits')
print("Popped:", popped)
print("Set now:", r.smembers('fruits'))
print("Size:", r.scard('fruits'))   # 2