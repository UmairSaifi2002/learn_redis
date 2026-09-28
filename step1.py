import redis

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

print("Ping:", r.ping())

r.set('greeting', 'Hello, Redis!')
print("Greeting:", r.get('greeting'))

info = r.info()
print("Redis version:", info['redis_version'])
print("Connected clients:", info['connected_clients'])
print("Used memory (bytes):", info['used_memory'])



