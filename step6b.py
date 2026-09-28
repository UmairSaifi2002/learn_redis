import redis

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
r.flushdb()

# Simulate 25 players with random-ish scores
players = {
    "alice": 1500, "bob": 1720, "carol": 1680, "dave": 1450, "eve": 1810,
    "frank": 1330, "grace": 1560, "heidi": 1290, "ivan": 1620, "judy": 1740,
    "karl": 1100, "liam": 1880, "mia": 1550, "noah": 1685, "olivia": 1770,
    "peter": 1400, "quinn": 1590, "rachel": 1650, "sam": 1350, "tom": 1490,
    "uma": 1710, "victor": 1230, "wendy": 1540, "xavier": 1440, "yara": 1860,
}
r.zadd('game:leaderboard', players)

def get_page(page_num, page_size=10):
    """Fetch a page of the leaderboard (1-indexed)."""
    start = (page_num - 1) * page_size
    end = start + page_size - 1
    rows = r.zrevrange('game:leaderboard', start, end, withscores=True)
    # Attach absolute rank
    return [(start + i + 1, name, score) for i, (name, score) in enumerate(rows)]

def get_my_stats(player):
    """Get a player's score, absolute rank, and percentile."""
    score = r.zscore('game:leaderboard', player)
    rank_zero = r.zrevrank('game:leaderboard', player)
    if score is None:
        return None
    total = r.zcard('game:leaderboard')
    rank_one = rank_zero + 1
    percentile = 100 * (1 - rank_zero / total)
    return {
        "player": player,
        "score": score,
        "rank": rank_one,
        "total": total,
        "percentile": round(percentile, 1),
    }

def get_neighbors(player, span=2):
    """Return players ranked just above and below `player`."""
    rank = r.zrevrank('game:leaderboard', player)
    if rank is None:
        return None
    start = max(0, rank - span)
    end = rank + span
    rows = r.zrevrange('game:leaderboard', start, end, withscores=True)
    return [(start + i + 1, name, score) for i, (name, score) in enumerate(rows)]

print("=== Page 1 ===")
for rank, name, score in get_page(1):
    print(f"  #{rank:>2}  {name:<8} {score}")

print("\n=== Page 2 ===")
for rank, name, score in get_page(2):
    print(f"  #{rank:>2}  {name:<8} {score}")

print("\n=== My stats (mia) ===")
print(get_my_stats("mia"))

print("\n=== Neighborhood around mia (±2 ranks) ===")
for rank, name, score in get_neighbors("mia", span=2):
    marker = " <-- you" if name == "mia" else ""
    print(f"  #{rank:>2}  {name:<8} {score}{marker}")



    