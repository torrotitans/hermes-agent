---
name: trino
description: Query, optimize, and administer Trino (formerly PrestoSQL) distributed SQL engine. Use for: writing Trino SQL queries, configuring connectors (Hive, Iceberg, Delta Lake, PostgreSQL, MySQL, Kafka, Snowflake, BigQuery, etc.), performance tuning, query execution analysis, catalog management, connector development, cluster administration, data federation across sources, EXPLAIN ANALYZE, session properties, resource groups, troubleshooting query failures, and integrating Trino with data pipelines.
---

# Trino Distributed SQL Engine

When to use this skill:
- Writing SQL queries across multiple data sources (federation/joins across connectors)
- Configuring and troubleshooting Trino connectors (catalog properties)
- Performance tuning with EXPLAIN ANALYZE, session properties, and resource groups
- Developing custom Trino connectors or plugins (Java/SPI)
- Administering Trino clusters (coordinator/worker configuration)
- Querying data lakes (Iceberg, Delta Lake, Hudi) or data warehouses
- Integrating Trino with dbt, Airflow, or BI tools

When NOT to use this skill:
- Single-database queries (use the appropriate database skill directly)
- PostgreSQL/MySQL native operations (use those database skills)
- Non-SQL data processing (use Spark, Pandas, or similar)

## Inputs Required

1. **Task type**: query-writing, connector-config, performance-tuning, cluster-admin, or connector-dev
2. **Target connector(s)**: e.g., hive, iceberg, postgresql, snowflake
3. **Query or configuration** (if applicable)

## Workflow

### 1. Identify the Task Category

Select the appropriate reference file based on your task:

| Task | Read |
|------|------|
| Writing SQL queries | [`references/sql-reference.md`](references/sql-reference.md) |
| Configuring connectors | [`references/connectors.md`](references/connectors.md) |
| Performance tuning | [`references/performance.md`](references/performance.md) |
| Cluster administration | [`references/cluster-config.md`](references/cluster-config.md) |
| Developing connectors (Java/SPI) | [`references/connector-dev.md`](references/connector-dev.md) |

### 2. Connector Configuration

For catalog setup, create `<catalog_name>.properties` in `etc/catalog/`:

```properties
connector.name=<connector-name>
# connector-specific properties
```

Common connectors:
- **hive**: HDFS/Hadoop data lakes
- **iceberg**: Apache Iceberg tables
- **delta**: Delta Lake tables
- **postgresql/mysql/sqlserver**: RDBMS sources
- **snowflake**: Snowflake data warehouse
- **kafka**: Streaming data
- **memory**: In-memory queries
- **blackhole**: Testing/empty tables

### 3. Query Federation

Join data across connectors in a single query:

```sql
SELECT h.customer_name, i.total_sales
FROM hive.mydb.customers h
JOIN iceberg.analytics.sales i ON h.id = i.customer_id
```

### 4. Session Properties

Modify query behavior with session commands:

```sql
SET SESSION hive.iterative_partitioned_pruning = true;
SET SESSION memory.heap_headroom_per_node = 4GB;
SET SESSION query_max_run_time = '2h';
```

### 5. Performance Analysis

```sql
-- View execution plan
EXPLAIN SELECT ...;

-- View execution plan with stats
EXPLAIN ANALYZE SELECT ...;

-- Query runtime info
SELECT * FROM runtime.queries;
SELECT * FROM runtime.nodes;
SELECT * FROM runtime.tasks WHERE state != 'SUCCEEDED';
```

## CLI Usage

```bash
# Start CLI
./trino-cli --server localhost:8080 --catalog hive --schema default

# Run query from command line
./trino-cli --server localhost:8080 --execute "SELECT 1"

# Connect to specific catalog/schema
./trino-cli --server localhost:8080 --catalog iceberg --schema analytics
```

## Examples

### Cross-Source Join
```sql
SELECT p.product_name, h.reviews_count
FROM postgresql.shop.products p
JOIN hive.data_lake.reviews h ON p.sku = h.sku
```

### Iceberg Time Travel
```sql
SELECT * FROM iceberg.db.table AT TIMESTAMP AS OF TIMESTAMP '2024-01-01 00:00:00';
SELECT * FROM iceberg.db.table AT VERSION AS OF 123;
```

### Delta Lake Operations
```sql
DESCRIBE HISTORY delta.mydb.mytable;
SELECT * FROM delta.mydb.mytable FOR TIME TRAVEL AS OF '2024-01-01';
```

## Troubleshooting

| Issue | Check |
|-------|-------|
| Connector not found | Verify `<connector>.jar` in plugin directory |
| Query OOM | Increase `memory.heap_headroom_per_node`, check EXPLAIN |
| Catalog not loading | Check `etc/catalog/<catalog>.properties` syntax |
| Slow queries | Run EXPLAIN ANALYZE, check partition pruning, join ordering |
| Authentication failure | Verify `config.properties` auth settings (LDAP, OAuth, etc.) |

For connector-specific issues, see [`references/connectors.md`](references/connectors.md).
