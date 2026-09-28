import redis

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
r.flushdb()

print("--- 1. Add members with scores ---")
r.zadd('leaderboard', {'Alice': 100, 'Bob': 85, 'Carol': 92, 'Dave': 78})
print("Leaderboard created.")
print("Cardinality (ZCARD):", r.zcard('leaderboard'))   # 4

print("\n--- 2. Get a member's score ---")
print("Alice's score:", r.zscore('leaderboard', 'Alice'))  # 100.0
print("Bob's score:", r.zscore('leaderboard', 'Bob'))      # 85.0

print("\n--- 3. Get the top 3 (by highest score) ---")
top3 = r.zrevrange('leaderboard', 0, 2, withscores=True)
for rank, (name, score) in enumerate(top3):
    print(f"  #{rank + 1}: {name} -> {score}")

print("\n--- 4. Get the bottom 3 (ascending) ---")
bottom3 = r.zrange('leaderboard', 0, 2, withscores=True)
print(bottom3)

print("\n--- 5. Rank of a specific member ---")
print("Alice's rank (from top):", r.zrevrank('leaderboard', 'Alice'))   # 0
print("Alice's rank (from bottom):", r.zrank('leaderboard', 'Alice'))   # 3
print("Bob's rank (from top):", r.zrevrank('leaderboard', 'Bob'))       # 3

print("\n--- 6. Atomic score update (ZINCRBY) ---")
r.zincrby('leaderboard', 20, 'Bob')      # Bob: 85 + 20 = 105
print("Bob's new score:", r.zscore('leaderboard', 'Bob'))
print("Top 3 after update:")
for name, score in r.zrevrange('leaderboard', 0, 2, withscores=True):
    print(f"  {name}: {score}")

print("\n--- 7. Add or update (ZADD overwrites the score) ---")
r.zadd('leaderboard', {'Carol': 200})
print("Carol's new score:", r.zscore('leaderboard', 'Carol'))

print("\n--- 8. Score range queries ---")
print("Members with score between 90 and 150:")
print(r.zrangebyscore('leaderboard', 90, 150, withscores=True))

print("Members with score > 100 (exclusive):")
print(r.zrangebyscore('leaderboard', '(100', '+inf', withscores=True))

print("Count with score in [80, 150]:", r.zcount('leaderboard', 80, 150))

print("\n--- 9. Remove members ---")
r.zrem('leaderboard', 'Dave')
print("After ZREM Dave:", r.zcard('leaderboard'))

print("\n--- 10. Remove by score range ---")
# Remove everyone with score below 100
r.zremrangebyscore('leaderboard', '-inf', '(100')
print("After removing scores < 100:")
for name, score in r.zrevrange('leaderboard', 0, -1, withscores=True):
    print(f"  {name}: {score}")

print("\n--- 11. Pop the top scorer (ZPOPMAX) ---")
top = r.zpopmax('leaderboard')
print("Popped:", top)       # [('Carol', 200.0)]
print("Remaining:", r.zrange('leaderboard', 0, -1, withscores=True))