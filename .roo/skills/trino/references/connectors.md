# Trino Connectors Reference

## Table of Contents

- [Connector Architecture](#connector-architecture)
- [Built-in Connectors](#built-in-connectors)
- [Data Lake Connectors](#data-lake-connectors)
- [RDBMS Connectors](#rdbms-connectors)
- [Streaming Connectors](#streaming-connectors)
- [Cloud Connectors](#cloud-connectors)
- [Custom Connector Development](#custom-connector-development)

## Connector Architecture

Trino connectors implement the `Connector` SPI. Each connector:
- Exposes catalogs with schemas and tables
- Supports read/write operations based on capabilities
- Provides session properties for tuning
- Integrates with Trino's distributed query engine

Catalog configuration goes in `etc/catalog/<name>.properties`:
```properties
connector.name=<connector-name>
# connector-specific properties
```

## Built-in Connectors

### Memory Connector
In-memory data source for testing and temporary tables.
```properties
connector.name=memory
memory.max-data-per-node=4GB
```

### Blackhole Connector
Empty table connector for testing query execution.
```properties
connector.name=blackhole
```

### TPCH Connector
Synthetic TPC-H benchmark data generator.
```properties
connector.name=tpch
tpch.splits-per-node=4
```

### TPCDS Connector
Synthetic TPC-DS benchmark data generator.
```properties
connector.name=tpcds
tpcds.splits-per-node=4
```

## Data Lake Connectors

### Hive Connector
Access HDFS, S3, GCS, Azure Blob via Hive Metastore.
```properties
connector.name=hive
hive.metastore.uri=thrift://metastore:9083
hive.config.resources=/etc/hadoop/core-site.xml,/etc/hadoop/hdfs-site.xml
```

**Key Session Properties:**
- `hive.insert_existing_partitions_behavior` (append/error)
- `hive.parquet.reader.type` (native/direct)
- `hive.statisticsonsource` (true/false for stats-based pruning)

### Iceberg Connector
Native Apache Iceberg support with time travel.
```properties
connector.name=iceberg
hive.metastore.uri=thrift://metastore:9083
```

**Iceberg Features:**
- Time travel: `AT TIMESTAMP AS OF`, `AT VERSION AS OF`
- Schema evolution
- Merge into: `MERGE INTO table USING source ON ... WHEN MATCHED THEN UPDATE`
- Snapshot management

### Delta Lake Connector
Delta Lake support with ACID transactions.
```properties
connector.name=delta
hive.metastore.uri=thrift://metastore:9083
```

**Delta Features:**
- Time travel: `FOR TIME TRAVEL AS OF`
- VACUUM, DESCRIBE HISTORY
- Merge operations

### Hudi Connector
Apache Hudi support for streaming upserts.
```properties
connector.name=hudi
hive.metastore.uri=thrift://metastore:9083
```

## RDBMS Connectors

### PostgreSQL Connector
```properties
connector.name=postgresql
jdbc.url=jdbc:postgresql://host:5432/db
connection.user=username
connection.password=password
```

### MySQL Connector
```properties
connector.name=mysql
jdbc.url=jdbc:mysql://host:3306/db
connection.user=username
connection.password=password
```

### SQL Server Connector
```properties
connector.name=sqlserver
jdbc.url=jdbc:sqlserver://host:1433;databaseName=db
connection.user=username
connection.password=password
```

### Oracle Connector
```properties
connector.name=oracle
jdbc.url=jdbc:oracle:thin:@host:1521:service
connection.user=username
connection.password=password
```

### MariaDB Connector
```properties
connector.name=mariadb
jdbc.url=jdbc:mariadb://host:3306/db
connection.user=username
connection.password=password
```

### SingleStore Connector
```properties
connector.name=singlestore
jdbc.url=jdbc:mysql://host:3306/db
connection.user=username
connection.password=password
```

### MongoDB Connector
```properties
connector.name=mongodb
mongodb.seeds=host1:27017,host2:27017
```

### Druid Connector
```properties
connector.name=druid
druid coordinator.host=druid-coordinator
druid broker.host=druid-broker
```

## Streaming Connectors

### Kafka Connector
```properties
connector.name=kafka
kafka.nodes=kafka1:9092,kafka2:9092
kafka.table-names=topic1,topic2
kafka.hidden-tables=internal_topic
```

### Prometheus Connector
Query Prometheus metrics via SQL.
```properties
connector.name=prometheus
prometheus.http-server.address=http://prometheus:9090
```

### JMX Connector
Query JVM JMX metrics.
```properties
connector.name=jmx
```

## Cloud Connectors

### Snowflake Connector
```properties
connector.name=snowflake
jdbc.url=jdbc:snowflake://account.snowflakecomputing.com
connection.user=username
connection.password=password
```

### BigQuery Connector
```properties
connector.name=bigquery
bigquery.project-id=my-project
bigquery.default-project=my-project
bigquery.json-key-file=/path/to/key.json
```

### Google Sheets Connector
```properties
connector.name=google-sheets
google.service.json=/path/to/service-account.json
```

### Amazon Redshift Connector
```properties
connector.name=redshift
jdbc.url=jdbc:redshift://cluster.region.redshift.amazonaws.com:5439/db
connection.user=username
connection.password=password
```

### Elasticsearch/OpenSearch Connector
```properties
connector.name=elasticsearch
elasticsearch.hosts=http://es-host:9200
elasticsearch.index-pattern=*
```

### ClickHouse Connector
```properties
connector.name=clickhouse
clickhouse.host=host
clickhouse.port=8123
clickhouse.user=username
clickhouse.password=password
```

### Loki Connector
Query Grafana Loki logs via SQL.
```properties
connector.name=loki
loki.url=http://loki:3100
```

## Connector Development (Java/SPI)

For custom connectors, implement these SPI interfaces:

| Interface | Purpose |
|-----------|---------|
| `Connector` | Factory for connector components |
| `ConnectorFactory` | Creates connector instances |
| `ConnectorSession` | Connector-specific session properties |
| `ConnectorHandleResolver` | Resolves handle types |
| `TableHandle` | Represents a table |
| `ColumnHandle` | Represents a column |
| `ConnectorReadRecordHandle` | Record-level read handle |
| `ConnectorOutputTableHandle` | Write target handle |

### Minimal Connector Skeleton

```java
@ConnectorFactory("myconnector")
public class MyConnectorFactory implements ConnectorFactory {
    @Override
    public String getName() {
        return "myconnector";
    }

    @Override
    public Connector create(Config config, ConnectorContext context) {
        return new MyConnector(config, context);
    }
}
```

### Testing Connectors

Use Trino's `QueryRunner` base class for connector tests:
```java
public class MyQueryRunner {
    private static final TestQueryRunner QUERY_RUNNER = new TestQueryRunner();

    @BeforeClass
    public static void startQueryRunner() {
        QUERY_RUNNER.initialize();
    }

    @AfterClass
    public static void stopQueryRunner() {
        QUERY_RUNNER.close();
    }
}
```

## Authentication & Authorization

### Authentication Methods
- None (development)
- LDAP
- OAuth2
- Kerberos
- Custom (via `PasswordAuthenticator` SPI)

### Authorization
- Access control via `AccessControl` SPI
- Ranger integration via `trino-ranger` plugin
- OPA integration via `trino-opa` plugin

## Common Connector Issues

| Issue | Resolution |
|-------|------------|
| `Catalog property not found` | Check `etc/catalog/<name>.properties` syntax |
| `Connection refused` | Verify JDBC URL, host, port |
| `Authentication failed` | Check credentials, SSL config |
| `Table not found` | Verify schema name, case sensitivity |
| `Out of memory` | Increase heap, check partition pruning |
