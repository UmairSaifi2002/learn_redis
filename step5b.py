import redis

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
r.flushdb()

# Suppose we have 5 posts, each tagged with multiple tags
posts_tags = {
    'post:1': ['python', 'redis'],
    'post:2': ['python', 'django'],
    'post:3': ['redis', 'caching'],
    'post:4': ['python', 'redis', 'performance'],
    'post:5': ['javascript', 'nodejs'],
}

# Index them: for each tag, build a set of posts that have that tag
for post, tags in posts_tags.items():
    for tag in tags:
        r.sadd(f"tag:{tag}", post)

print("All tags and their posts:")
for tag in ['python', 'redis', 'django', 'caching', 'performance', 'javascript', 'nodejs']:
    print(f"  {tag}: {r.smembers(f'tag:{tag}')}")

print("\n--- Query: posts tagged 'python' AND 'redis' ---")
result = r.sinter('tag:python', 'tag:redis')
print(result)   # {'post:1', 'post:4'}

print("\n--- Query: posts tagged 'python' OR 'redis' ---")
result = r.sunion('tag:python', 'tag:redis')
print(result)   # {'post:1', 'post:2', 'post:3', 'post:4'}

print("\n--- Query: posts tagged 'redis' but NOT 'python' ---")
result = r.sdiff('tag:redis', 'tag:python')
print(result)   # {'post:3'}