import redis
import time
import threading

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
r.flushdb()

# Setup two accounts
r.set('account:alice', 100)
r.set('account:bob', 50)

def transfer(from_acc, to_acc, amount, max_retries=5):
    """
    Atomically move `amount` from `from_acc` to `to_acc`.
    Uses WATCH + MULTI/EXEC for safety.
    """
    from_key = f'account:{from_acc}'
    to_key = f'account:{to_acc}'

    for attempt in range(max_retries):
        try:
            with r.pipeline() as pipe:
                pipe.watch(from_key, to_key)   # start watching

                from_balance = int(pipe.get(from_key) or 0)
                if from_balance < amount:
                    pipe.unwatch()
                    raise ValueError(f"Insufficient funds in {from_acc}: {from_balance}")

                # Queue the transaction
                pipe.multi()
                pipe.decrby(from_key, amount)
                pipe.incrby(to_key, amount)
                pipe.execute()   # will fail if watched keys changed

                print(f"  [{attempt+1}] Transfer OK: {from_acc} -> {to_acc}  ({amount})")
                return True
        except redis.WatchError:
            print(f"  [{attempt+1}] Conflict detected, retrying...")
            time.sleep(0.05)
            continue

    print("  Transfer failed after retries.")
    return False

print("=== A. Simple transfer (no contention) ===")
transfer('alice', 'bob', 30)
print("Alice:", r.get('account:alice'))   # 70
print("Bob:  ", r.get('account:bob'))     # 80

print("\n=== B. Concurrent transfers with contention ===")
# Reset
r.set('account:alice', 100)
r.set('account:bob', 0)

def worker(name, amount):
    transfer('alice', 'bob', amount)

# Fire 10 transfers of 15 in parallel — total 150 from an account with 100
# Only some should succeed.
threads = [threading.Thread(target=worker, args=(f'w{i}', 15)) for i in range(10)]
for t in threads: t.start()
for t in threads: t.join()

print("\nFinal balances:")
print("Alice:", r.get('account:alice'))
print("Bob:  ", r.get('account:bob'))