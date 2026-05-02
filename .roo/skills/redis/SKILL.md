---
name: redis
description: Configure and operate Redis (v7.x+) including data structures, persistence, replication, clustering, and Python client integration for caching, session management, and message brokering
license: MIT
compatibility:
  - redis-7.0+
  - python-3.9+
  - redis-py-5.0+
metadata:
  version: 1.0.0
  author: Torro Team
  source: https://github.com/redis/redis
---

# Redis Skill

## When to Use This Skill

Use this skill when you need to:
- Configure Redis server (redis.conf) for production or development
- Implement Redis data structures (strings, lists, sets, hashes, sorted sets, streams)
- Set up Redis persistence (RDB snapshots, AOF append-only file)
- Configure Redis replication (master-replica) or clustering
- Use Redis for caching with eviction policies
- Implement distributed session management
- Build message queues or pub/sub systems with Redis
- Integrate Redis with Python applications using redis-py
- Optimize Redis performance and memory usage
- Debug Redis connectivity or performance issues

## When NOT to Use This Skill

Do NOT use this skill when:
- Working with Redis 3.x or older (significantly different API)
- Building non-cache, non-data-structure use cases (use database skills instead)
- Configuring cloud-managed Redis (use cloud provider skills)
- Implementing complex data transformations (use Airflow or database skills)

## Inputs Required

Before starting, ensure you have:
1. Redis version (default: v7.x+)
2. Use case (caching, session store, queue, etc.)
3. Deployment type (standalone, replication, cluster)
4. Python environment with redis-py installed

## Workflow

### Step 1: Install and Start Redis

```bash
# Using Docker (recommended for development)
docker run -d -p 6379:6379 --name redis-server redis:latest

# With persistence
docker run -d -p 6379:6379 \
  -v $(pwd)/data:/data \
  -v $(pwd)/redis.conf:/usr/local/etc/redis/redis.conf \
  redis:latest redis-server /usr/local/etc/redis/redis.conf

# Start with custom config
redis-server /path/to/redis.conf
```

### Step 2: Configure redis.conf

Key configuration from the official redis.conf:

```conf
# Network
bind 127.0.0.1 -::1
port 6379
protected-mode yes

# Persistence - RDB Snapshots
save 900 1      # Save after 900s if at least 1 key changed
save 300 10     # Save after 300s if at least 10 keys changed
save 60 10000   # Save after 60s if at least 10000 keys changed
dbfilename dump.rdb
dir /data

# Persistence - AOF
appendonly yes
appendfilename "appendonly.aof"
appendfsync everysec

# Memory Management
maxmemory 2gb
maxmemory-policy allkeys-lru

# Security
requirepass your-strong-password
rename-command FLUSHDB ""
rename-command FLUSHALL ""
rename-command DEBUG ""
```

### Step 3: Python Client Integration (redis-py)

```python
import redis

# Basic connection
r = redis.Redis(
    host='localhost',
    port=6379,
    db=0,
    password='your-password',
    decode_responses=True,  # Return strings instead of bytes
    max_connections=10,
    socket_connect_timeout=5,
    socket_timeout=5,
)

# Test connection
r.ping()  # Returns True
```

### Step 4: Use String Operations

```python
# Basic string operations
r.set('user:1001:name', 'John Doe')
r.set('user:1001:email', 'john@example.com')
r.setex('session:abc123', 3600, 'session-data')  # Expire in 1 hour

# Get values
name = r.get('user:1001:name')
print(name)  # 'John Doe'

# Increment/decrement counters
r.set('counter:page_views', 0)
r.incr('counter:page_views')      # 1
r.incrby('counter:page_views', 10)  # 11
r.decr('counter:page_views')      # 10

# Pipeline for batch operations
pipe = r.pipeline()
pipe.set('key1', 'value1')
pipe.set('key2', 'value2')
pipe.incr('counter')
results = pipe.execute()  # Returns [True, True, 1]
```

### Step 5: Use Hash Data Structures

```python
# Hash operations (like a dictionary)
r.hset('user:1001', mapping={
    'name': 'John Doe',
    'email': 'john@example.com',
    'age': '30',
    'role': 'admin',
})

# Get single field
name = r.hget('user:1001', 'name')

# Get multiple fields
user_data = r.hmget('user:1001', 'name', 'email')

# Get all fields
all_data = r.hgetall('user:1001')
# {'name': 'John Doe', 'email': 'john@example.com', ...}

# Check field exists
has_email = r.hexists('user:1001', 'email')

# Delete fields
r.hdel('user:1001', 'role')
```

### Step 6: Use Lists (Queues)

```python
# List operations - FIFO queue
r.lpush('tasks:queue', 'task_1', 'task_2', 'task_3')

# Pop from queue (blocking)
task = r.brpop('tasks:queue', timeout=10)
# ('tasks:queue', 'task_3')

# Peek at queue without removing
last_task = r.lindex('tasks:queue', -1)

# Get queue length
queue_size = r.llen('tasks:queue')

# Trim list (keep only last 1000 items)
r.ltrim('logs:app', -1000, -1)
```

### Step 7: Use Sorted Sets (Leaderboards)

```python
# Add members with scores
r.zadd('leaderboard', {
    'player1': 1500,
    'player2': 2300,
    'player3': 1800,
})

# Get rank (0-based)
rank = r.zrank('leaderboard', 'player2')

# Get score
score = r.zscore('leaderboard', 'player1')

# Get top 3
top_players = r.zrevrange('leaderboard', 0, 2, withscores=True)
# [('player2', 2300.0), ('player3', 1800.0), ('player1', 1500.0)]

# Increment score
r.zincrby('leaderboard', 500, 'player1')  # player1 now has 2000
```

### Step 8: Use Sets

```python
# Set operations
r.sadd('users:online', 'user1', 'user2', 'user3')
r.sadd('users:offline', 'user4', 'user5')

# Get all members
online_users = r.smembers('users:online')

# Check membership
is_online = r.sismember('users:online', 'user1')

# Set operations
r.sadd('users:premium', 'user1', 'user2', 'user6')

# Intersection (premium AND online)
premium_online = r.sinter('users:online', 'users:premium')

# Union
all_users = r.sunion('users:online', 'users:offline')

# Difference (online but not premium)
free_online = r.sdiff('users:online', 'users:premium')
```

### Step 9: Implement Pub/Sub

```python
# Publisher
pubsub = r.pubsub()
pubsub.subscribe('channel:notifications')

# Subscribe (in separate thread/process)
for message in pubsub.listen():
    if message['type'] == 'message':
        print(f"Received: {message['data']}")

# Publish
r.publish('channel:notifications', 'New notification!')
```

### Step 10: Implement Streams (Message Broker)

```python
# Produce messages to stream
r.xadd('orders:stream', {
    'order_id': '12345',
    'customer': 'user1',
    'amount': '99.99',
})

# Consume from stream (blocking)
messages = r.xread({'orders:stream': '$'}, count=10, block=5000)

# Read with consumer group
r.xgroup_create('orders:stream', 'workers', id='0', mkstream=True)
pending = r.xreadgroup('workers', 'consumer1', {'orders:stream': '>'}, count=10)

# Acknowledge processing
r.xack('orders:stream', 'workers', *message_ids)
```

### Step 11: Implement Caching Pattern

```python
import json
import time

def get_with_cache(r, key, fetch_func, ttl=300):
    """Cache-aside pattern."""
    cached = r.get(key)
    if cached:
        return json.loads(cached)
    
    # Cache miss - fetch from source
    data = fetch_func()
    
    # Store in cache with TTL
    r.setex(key, ttl, json.dumps(data))
    
    return data

# Usage
def fetch_user(user_id):
    # Expensive database query
    return {'id': user_id, 'name': 'John'}

user = get_with_cache(r, f'user:{1001}', lambda: fetch_user(1001))
```

### Step 12: Implement Distributed Lock

```python
import uuid

def acquire_lock(r, resource, ttl=30):
    """Acquire distributed lock using SET NX."""
    lock_id = str(uuid.uuid4())
    acquired = r.set(resource, lock_id, nx=True, ex=ttl)
    return lock_id if acquired else None

def release_lock(r, resource, lock_id):
    """Safely release lock using Lua script."""
    lua_script = """
    if redis.call("get", KEYS[1]) == ARGV[1] then
        return redis.call("del", KEYS[1])
    else
        return 0
    end
    """
    r.eval(lua_script, 1, resource, lock_id)

# Usage
lock_id = acquire_lock(r, 'resource:critical', ttl=30)
if lock_id:
    try:
        # Critical section
        pass
    finally:
        release_lock(r, 'resource:critical', lock_id)
```

## Files Reference

| File | Purpose |
|------|---------|
| `redis.conf` | Server configuration |
| `src/commands/` | Command definitions (JSON) |
| `tests/` | Test suite |

## Troubleshooting

### Issue: Connection Refused

**Symptom**: `ConnectionRefusedError: Connection refused`

**Solution**:
- Verify Redis is running: `redis-cli ping` (should return PONG)
- Check bind address in redis.conf
- Verify port is not blocked by firewall
- Check protected-mode setting

### Issue: OOM (Out of Memory)

**Symptom**: `OOM command not allowed when used memory > 'maxmemory'`

**Solution**:
- Increase maxmemory: `maxmemory 4gb`
- Change eviction policy: `maxmemory-policy allkeys-lru`
- Identify large keys: `redis-cli --bigkeys`
- Use memory analysis: `redis-cli memory doctor`

### Issue: Slow Queries

**Symptom**: High latency on Redis operations

**Solution**:
- Enable slow log: `slowlog-log-slower-than 10000` (10ms)
- Check slow log: `slowlog get 10`
- Avoid KEYS pattern: use SCAN instead
- Use pipelines for batch operations
- Monitor with `INFO commandstats`

## Examples

### Example 1: Session Store

```python
import json
import uuid

def create_session(r, user_id):
    session_id = str(uuid.uuid4())
    session_data = {
        'user_id': user_id,
        'created_at': time.time(),
    }
    r.setex(f'session:{session_id}', 86400, json.dumps(session_data))
    return session_id

def get_session(r, session_id):
    data = r.get(f'session:{session_id}')
    return json.loads(data) if data else None
```

### Example 2: Rate Limiter

```python
def is_rate_limited(r, key, max_requests, window_seconds):
    """Sliding window rate limiter."""
    current = r.llen(f'rate:{key}')
    if current and current < max_requests:
        r.lpush(f'rate:{key}', time.time())
        r.ltrim(f'rate:{key}', 0, max_requests - 1)
        return False
    r.lpush(f'rate:{key}', time.time())
    r.ltrim(f'rate:{key}', 0, max_requests - 1)
    r.expire(f'rate:{key}', window_seconds)
    return current >= max_requests
```

## Related Resources

- [Redis Documentation](https://redis.io/docs/)
- [Redis Commands Reference](https://redis.io/commands/)
- [redis-py Documentation](https://redis-py.readthedocs.io/)
- [Redis Modules API](https://redis.io/docs/latest/develop/reference/modules/)
