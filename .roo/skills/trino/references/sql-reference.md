# Trino SQL Reference

## Table of Contents

- [SQL Syntax Overview](#sql-syntax-overview)
- [Data Types](#data-types)
- [System Tables](#system-tables)
- [Window Functions](#window-functions)
- [CTEs and Subqueries](#ctes-and-subqueries)
- [JSON Functions](#json-functions)
- [Map & Array Functions](#map--array-functions)
- [Regular Expressions](#regular-expressions)
- [Time Travel Queries](#time-travel-queries)
- [DDL Statements](#ddl-statements)

## SQL Syntax Overview

Trino follows SQL:2016 standard with extensions. Key syntax:

```sql
SELECT [DISTINCT] select_expr [, ...]
FROM table_reference [, ...]
[WHERE where_condition]
[GROUP BY expression [, ...]]
[HAVING condition]
[ORDER BY expression [ASC|DESC] [, ...]]
[LIMIT count]
[OFFSET start]
```

## Data Types

### Primitive Types
| Type | Description |
|------|-------------|
| `BOOLEAN` | TRUE, FALSE, UNKNOWN |
| `TINYINT` | 1-byte signed integer |
| `SMALLINT` | 2-byte signed integer |
| `INTEGER` | 4-byte signed integer |
| `BIGINT` | 8-byte signed integer |
| `REAL` | 4-byte floating point |
| `DOUBLE` | 8-byte floating point |
| `DECIMAL(p,s)` | Exact numeric |
| `VARCHAR(n)` | Variable-length string |
| `CHAR(n)` | Fixed-length string |
| `VARBINARY` | Binary string |
| `DATE` | Calendar date |
| `TIME` | Time of day |
| `TIME WITH TIME ZONE` | Time with timezone |
| `TIMESTAMP` | Date and time |
| `TIMESTAMP WITH TIME ZONE` | Timestamp with timezone |
| `UUID` | Universally unique identifier |
| `JSON` | JSON data |

### Complex Types
| Type | Description |
|------|-------------|
| `ARRAY(T)` | Ordered collection of T |
| `MAP(K, V)` | Key-value pairs |
| `ROW(field1 T1, field2 T2, ...)` | Structured record |

### Type Casting
```sql
CAST(expression AS type)
expression::type  -- shorthand
```

## System Tables

### Runtime System
```sql
-- Active queries
SELECT * FROM runtime.queries;

-- Running tasks
SELECT * FROM runtime.tasks WHERE state != 'SUCCEEDED';

-- Cluster nodes
SELECT * FROM system.runtime.nodes;

-- Query plans
SELECT * FROM runtime.query_plans;

-- Resource groups
SELECT * FROM runtime.resource_groups;
```

### Memory System
```sql
-- Memory pool usage
SELECT * FROM memory.pools;

-- Task memory usage
SELECT * FROM memory.tasks;
```

### Scheduler System
```sql
-- Scheduler info
SELECT * FROM scheduler.info;
```

### Metadata System (per connector)
```sql
-- Tables in catalog/schema
SELECT * FROM hive.mydb.tables;
SELECT * FROM information_schema.tables;
SELECT * FROM information_schema.columns;

-- Schemas in catalog
SELECT * FROM information_schema.schemata;

-- Column statistics
SELECT * FROM hive.mydb.column_statistics;
```

## Window Functions

```sql
ROW_NUMBER() OVER (PARTITION BY col ORDER BY col2)
RANK() OVER (PARTITION BY col ORDER BY col2)
DENSE_RANK() OVER (PARTITION BY col ORDER BY col2)
NTILE(n) OVER (ORDER BY col)
LEAD(col, offset, default) OVER (...)
LAG(col, offset, default) OVER (...)
FIRST_VALUE(col) OVER (...)
LAST_VALUE(col) OVER (...)
SUM(col) OVER (PARTITION BY col2 ORDER BY col3 ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
```

## CTEs and Subqueries

```sql
-- Common Table Expression
WITH regional_sales AS (
    SELECT region, SUM(amount) AS total_sales
    FROM orders
    GROUP BY region
),
top_regions AS (
    SELECT region
    FROM regional_sales
    GROUP BY region
    HAVING SUM(total_sales) > (SELECT SUM(total_sales) * 0.10 FROM regional_sales)
)
SELECT region, product, SUM(quantity) AS product_units, SUM(amount) AS product_sales
FROM orders
WHERE region IN (SELECT region FROM top_regions)
GROUP BY region, product;

-- LATERIN subquery for unnesting
SELECT id, element
FROM my_table, UNNEST(array_column) AS t(element);
```

## JSON Functions

```sql
-- Parse JSON
SELECT json_parse('{"name": "John", "age": 30}');

-- Extract values
SELECT json_extract(json_col, '$.name') FROM table;
SELECT json_extract_scalar(json_col, '$.name') FROM table;

-- Array access
SELECT json_extract(json_col, '$.items[0]') FROM table;

-- Transform JSON
SELECT json_transform(json_col, '{"type":"object","properties":{"name":{"type":"string"}}}') FROM table;

-- Validate JSON
SELECT json_valid('{"valid": true}');
```

## Map & Array Functions

```sql
-- Array functions
ARRAY[1, 2, 3]
ARRAY_APPEND(arr, value)
ARRAY_CAT(arr1, arr2)
ARRAY_CONTAINS(arr, value)
ARRAY_EXCEPT(arr1, arr2)
ARRAY_INTERSECT(arr1, arr2)
ARRAY_UNIQUE_COUNT(arr)
CARDINALITY(arr)
FLATTEN(arr)
GENERATE_SER(start, stop, step)
ARRAY_SORT(arr)
ARRAY_SLICE(arr, start, length)

-- Map functions
MAP(keys, values)
MAP_FROM_ENTRIES(entries_array)
MAP_CONTAINS_KEY(map, key)
MAP_GET(map, key)
MAP_KEYS(map)
MAP_VALUES(map)
MAP_FILTER(map, predicate)
MAP_ZIP_WITH(map1, map2, combiner)
```

## Regular Expressions

```sql
REGEXP_LIKE(str, pattern)
REGEXP_EXTRACT(str, pattern, group)
REGEXP_EXTRACT_ALL(str, pattern)
REGEXP_REPLACE(str, pattern, replacement)
REGEXP_SPLIT(str, pattern)
```

## Time Travel Queries

### Iceberg
```sql
-- By timestamp
SELECT * FROM iceberg.db.table AT TIMESTAMP AS OF TIMESTAMP '2024-01-01 00:00:00';

-- By version
SELECT * FROM iceberg.db.table AT VERSION AS OF 123;
```

### Delta Lake
```sql
-- By timestamp
SELECT * FROM delta.db.table FOR TIME TRAVEL AS OF TIMESTAMP '2024-01-01 00:00:00';

-- By version
SELECT * FROM delta.db.table FOR TIME TRAVEL AS OF VERSION 123;
```

## DDL Statements

### Table Creation
```sql
-- Create table as select
CREATE TABLE hive.mydb.new_table AS SELECT * FROM source_table;

-- Create table with schema
CREATE TABLE hive.mydb.new_table (
    id INTEGER,
    name VARCHAR,
    amount DOUBLE
) WITH (
    format = 'PARQUET',
    partitioned_by = ARRAY['region']
);

-- External table
CREATE EXTERNAL TABLE hive.mydb.external_table (...) WITH (location = 's3://bucket/path');
```

### Schema Management
```sql
CREATE SCHEMA hive.mydb;
DROP SCHEMA hive.mydb CASCADE;
ALTER SCHEMA hive.old_name RENAME TO new_name;
```

### Table Management
```sql
DROP TABLE hive.mydb.table;
ALTER TABLE hive.mydb.table RENAME TO new_table;
ALTER TABLE hive.mydb.table ADD COLUMN new_col VARCHAR;
ALTER TABLE hive.mydb.table DROP COLUMN old_col;
ALTER TABLE hive.mydb.table SET PROPERTY format = 'ORC';
```

### View Management
```sql
CREATE VIEW hive.mydb.view_name AS SELECT ...;
DROP VIEW hive.mydb.view_name;
CREATE OR REPLACE VIEW hive.mydb.view_name AS SELECT ...;
```

## Query Hints

```sql
-- Distribution hints
SELECT /*+ DISTRIBUTE BY col */ * FROM table;
SELECT /*+ PARTITION DISTRIBUTE BY col */ * FROM table;
SELECT /*+ BROADCAST */ * FROM very_small_table;

-- Join hints
SELECT /*+ JOIN(s) */ * FROM t1 JOIN t2 ON t1.id = t2.id;
SELECT /*+ SHUFFLE_JOIN(t1, t2) */ * FROM t1 JOIN t2 ON t1.id = t2.id;
SELECT /*+ BROADCAST_JOIN(t1, t2) */ * FROM t1 JOIN t2 ON t1.id = t2.id;
```

## Session Properties

Common session properties for query control:

```sql
SET SESSION query_max_run_time = '2h';
SET SESSION query_priority = 1;  -- 1 (highest) to 1000 (lowest)
SET SESSION memory.heap_headroom_per_node = '4GB';
SET SESSION exchange.max_concurrent_tasks = 100;
SET SESSION optimizer.optimize_metadata_queries = true;
SET SESSION optimizer.optimize_annotated_queries = true;
SET SESSION optimizer.rewrite_anti_join = true;
SET SESSION optimizer.distributed_join = true;
```
