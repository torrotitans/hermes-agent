# Trino Performance Tuning Reference

## Table of Contents

- [Query Analysis](#query-analysis)
- [Session Properties](#session-properties)
- [Join Optimization](#join-optimization)
- [Partition Pruning](#partition-pruning)
- [Memory Management](#memory-management)
- [Parallelism & Scheduling](#parallelism--scheduling)
- [Resource Groups](#resource-groups)
- [Common Performance Patterns](#common-performance-patterns)
- [Troubleshooting Slow Queries](#troubleshooting-slow-queries)

## Query Analysis

### EXPLAIN
```sql
-- Logical execution plan
EXPLAIN SELECT ...;

-- Physical execution plan with cost estimates
EXPLAIN (TYPE DISTRIBUTED) SELECT ...;

-- Full execution plan with stats
EXPLAIN ANALYZE SELECT ...;

-- Compare plans
EXPLAIN (FORMAT TEXT) SELECT ...;
EXPLAIN (FORMAT GRAPHVIZ) SELECT ...;
```

### Query Inspection
```sql
-- Find slow queries
SELECT query_id, query, state, user, query_text
FROM runtime.queries
WHERE state = 'RUNNING'
  AND elapsed_time > INTERVAL '5 minutes'
ORDER BY elapsed_time DESC;

-- Query statistics
SELECT user,
       COUNT(*) AS query_count,
       SUM(total_driver_time) AS total_time,
       AVG(total_driver_time) AS avg_time
FROM runtime.tasks
GROUP BY user
ORDER BY total_time DESC;

-- Find bottlenecks
SELECT node_id, state, processed_rows,
       elapsed_time, user_time, system_time
FROM runtime.tasks
WHERE state = 'RUNNING'
ORDER BY elapsed_time DESC
LIMIT 20;
```

## Session Properties

### General Query Settings
| Property | Default | Description |
|----------|---------|-------------|
| `query_max_run_time` | 3h | Maximum query execution time |
| `query_priority` | 100 | Query priority (1-1000) |
| `query_max_memory` | auto | Max memory per query |
| `query_max_plan_size` | 50000 | Max plan nodes |
| `max_warning_count` | 256 | Max warnings per query |

### Optimizer Settings
| Property | Default | Description |
|----------|---------|-------------|
| `optimizer.optimize_metadata_queries` | true | Push down metadata-only queries |
| `optimizer.optimize_annotated_queries` | true | Optimize queries with annotations |
| `optimizer.rewrite_anti_join` | true | Rewrite NOT IN as anti-join |
| `optimizer.distributed_join` | true | Use distributed joins |
| `optimizer.push_join_filter_through_join` | true | Push filters through joins |
| `optimizer.optimize_null_aware_anti_join` | true | Optimize null-aware anti-joins |
| `optimizer.enable_hash_generation` | true | Enable hash generation optimization |
| `optimizer.max_optimization_rounds` | 20 | Max optimizer iterations |

### Hive-Specific
| Property | Default | Description |
|----------|---------|-------------|
| `hive.iterative_partitioned_pruning` | true | Iterative partition pruning |
| `hive.optimize_bucket_join` | false | Bucket-aware join optimization |
| `hive.optimize_bucketing` | false | Bucketed table optimization |
| `hive.parquet.use_column_names` | true | Use column names in Parquet |
| `hive.parquet.reader.type` | native | Parquet reader type |
| `hive.pushdown_aggregation_limit` | 100000 | Aggregation pushdown limit |

### Join Settings
| Property | Default | Description |
|----------|---------|-------------|
| `join_distribution_type` | AUTO | AUTO, BROADCAST, DISTRIBUTE, PARTITIONED |
| `optimize_position_join` | true | Optimize position-based joins |
| `auto_join_join_selection_strategy` | best-estimates | Use best cost estimates |

## Join Optimization

### Join Distribution Strategies

```sql
-- Force broadcast join (small table)
SET SESSION join_distribution_type = 'BROADCAST';
SELECT /*+ BROADCAST(t2) */ * FROM t1 JOIN t2 ON t1.id = t2.id;

-- Force distributed join
SET SESSION join_distribution_type = 'DISTRIBUTE';
SELECT /*+ DISTRIBUTE_JOIN(t1, t2) */ * FROM t1 JOIN t2 ON t1.id = t2.id;

-- Force partitioned join
SET SESSION join_distribution_type = 'PARTITIONED';
SELECT /*+ PARTITIONED_JOIN(t1, t2) */ * FROM t1 JOIN t2 ON t1.id = t2.id;
```

### Join Best Practices

1. **Join order**: Place largest tables first in FROM clause
2. **Broadcast small tables**: Use `/*+ BROADCAST(small_table) */` hint
3. **Filter early**: Apply WHERE filters before JOINs
4. **Bucketed joins**: Ensure both tables are bucketed on join key
5. **Avoid cartesian products**: Always provide JOIN conditions

## Partition Pruning

### Enable Partition Pruning
```sql
-- Hive partition pruning
SET SESSION hive.iterative_partitioned_pruning = true;
SET SESSION hive.statisticsonsource = true;

-- Check partition info
SELECT * FROM hive.mydb.table_partitions WHERE table_name = 'my_table';
```

### Partition Pruning Patterns
```sql
-- Direct partition filter (optimal)
SELECT * FROM hive.mydb.table WHERE dt = '2024-01-01';

-- Range partition filter
SELECT * FROM hive.mydb.table WHERE dt BETWEEN '2024-01-01' AND '2024-01-31';

-- Multiple partition columns
SELECT * FROM hive.mydb.table WHERE dt = '2024-01-01' AND region = 'us-east';
```

## Memory Management

### Heap Configuration
```properties
# config.properties (coordinator & workers)
http-server.http.port=8080
jvm.config:
-server
-Xmx16G
-Xms16G
-XX:+UseG1GC
-XX:G1HeapRegionSize=32M
-XX:+UseGCOverheadLimit
-XX:+ExplicitGCInvokesConcurrent
-XX:+HeapDumpOnOutOfMemoryError
-XX:+ExitOnOutOfMemoryError
```

### Query Memory Settings
```sql
-- Per-query memory
SET SESSION memory.heap_headroom_per_node = '4GB';
SET SESSION memory.max_memory_per_node = '8GB';
SET SESSION memory.max_total_memory_per_node = '32GB';

-- Spill to disk
SET SESSION spilling_enabled = true;
SET SESSION io.tmp-dir = /tmp/trino-io;
```

### Memory Monitoring
```sql
-- Check memory pool usage
SELECT pool, used_memory, queued_memory, max_memory
FROM memory.pools;

-- Check task memory
SELECT task_id, user, state, processed_memory
FROM memory.tasks
ORDER BY processed_memory DESC
LIMIT 20;
```

## Parallelism & Scheduling

### Task Parallelism
```sql
-- Adjust concurrent tasks
SET SESSION exchange.max_concurrent_tasks = 50;
SET SESSION http.client.max-requests-per-node = 500;
SET SESSION http.client.max-idle-connection = 500;

-- Adjust splits
SET SESSION hive.splits-per-node = 100;
```

### Worker Configuration
```properties
# config.properties
coordinator=true
node-scheduler.include-coordinator=false
http-server.http.port=8080
query.max-workers=1000
query.max-task-per-node=8
query.min-worker-tasks=16
```

## Resource Groups

### Resource Group Configuration
```properties
# etc/resource-groups.json
[
  {
    "id": 1,
    "name": "interactive",
    "softMemoryLimit": "80%",
    "softCpuLimit": "80%",
    "maxQueued": 100,
    "schedulingPolicy": "fair",
    "userMaxQueries": 10,
    "userConcurrencyLimit": 5,
    "queryMaxMemory": "16GB",
    "queryMaxRunTime": "1h"
  },
  {
    "id": 2,
    "name": "batch",
    "softMemoryLimit": "50%",
    "softCpuLimit": "50%",
    "maxQueued": 1000,
    "schedulingPolicy": "fair"
  }
]
```

### Resource Group Queries
```sql
-- View resource groups
SELECT * FROM runtime.resource_groups;

-- View group usage
SELECT group_id, user, query_id, state, queued_time
FROM runtime.resource_groups
ORDER BY queued_time DESC;
```

## Common Performance Patterns

### Anti-Patterns to Avoid

```sql
-- BAD: Function on column prevents index usage
SELECT * FROM table WHERE UPPER(name) = 'JOHN';

-- GOOD: Use case-insensitive collation or stored lowercase
SELECT * FROM table WHERE name = 'john' COLLATE "en-x-icu:lower";

-- BAD: Implicit type conversion
SELECT * FROM table WHERE varchar_column = 123;

-- GOOD: Explicit cast
SELECT * FROM table WHERE varchar_column = CAST(123 AS VARCHAR);

-- BAD: SELECT * in large joins
SELECT * FROM large_table JOIN small_table ON ...;

-- GOOD: Select only needed columns
SELECT col1, col2, col3 FROM large_table JOIN small_table ON ...;
```

### Optimization Patterns

```sql
-- Use EXISTS instead of IN for large subqueries
SELECT * FROM t1 WHERE EXISTS (SELECT 1 FROM t2 WHERE t1.id = t2.id);

-- Use UNION ALL instead of UNION when duplicates impossible
SELECT col FROM t1 UNION ALL SELECT col FROM t2;

-- Pre-aggregate before joining
WITH agg AS (
    SELECT key, SUM(value) as total
    FROM large_table
    GROUP BY key
)
SELECT a.*, b.total FROM dim_table a JOIN agg b ON a.key = b.key;
```

## Troubleshooting Slow Queries

### Diagnostic Steps

1. **Run EXPLAIN ANALYZE** - Identify the slowest stage
2. **Check runtime.tasks** - Find rows/stage bottlenecks
3. **Verify partition pruning** - Check if partitions are being skipped
4. **Check join distribution** - Ensure optimal join strategy
5. **Monitor memory** - Check for spilling

### Common Issues

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| One task takes forever | Data skew | Use `/*+ DISTRIBUTE */` hint |
| Query fails with OOM | Insufficient memory | Increase heap_headroom |
| Many small splits | Too many small files | Increase hive.splits-per-node |
| High queuing time | Resource contention | Check resource groups |
| Slow metadata queries | Large table count | Enable metadata query optimization |

### Skew Detection
```sql
-- Find skewed tasks
SELECT stage_id, task_id, processed_rows, elapsed_time
FROM runtime.tasks
WHERE stage_id = <problematic_stage>
ORDER BY processed_rows DESC
LIMIT 10;
```
