import redis
import time
import sys

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

job_name = sys.argv[1] if len(sys.argv) > 1 else "job-default"

print(f"Producer: pushing '{job_name}' onto queue...")
r.rpush('jobs', job_name)
print("Producer: done.")

