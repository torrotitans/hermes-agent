# Trino Cluster Configuration Reference

## Table of Contents

- [Cluster Architecture](#cluster-architecture)
- [Node Configuration](#node-configuration)
- [Security Configuration](#security-configuration)
- [EventListener Plugins](#eventlistener-plugins)
- [Node Properties](#node-properties)
- [Log Configuration](#log-configuration)
- [High Availability](#high-availability)
- [Deployment Considerations](#deployment-considerations)

## Cluster Architecture

Trino follows a master-worker architecture:

```
                    ┌─────────────────┐
                    │   Coordinator   │
                    │  (Query Mgmt)   │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
        ┌─────▼─────┐ ┌─────▼─────┐ ┌─────▼─────┐
        │  Worker 1  │ │  Worker 2  │ │  Worker 3  │
        └───────────┘ └───────────┘ └───────────┘
```

- **Coordinator**: Accepts queries, plans execution, assigns tasks
- **Worker**: Executes query tasks, processes data
- A node can be both coordinator and worker

## Node Configuration

### config.properties (Coordinator)
```properties
# Node identification
node.environment=production
node.id=node-1
node.data-dir=/var/trino/data

# HTTP
http-server.http.port=8080
http-server.http.max-request-header-size=10MB

# Discovery (uses discovery instead of HTTP for node discovery)
discovery.uri=http://coordinator-host:8080
discovery-server.enabled=true

# Query settings
query.max-memory=50GB
query.max-memory-per-node=2GB
query.max-plan-size=50000000
query.max-run-time=3h
query.max-workers=1000

# JMX
jmx.rmiregistry.port=161
jmx.rmiserver.port=162
```

### config.properties (Worker)
```properties
node.environment=production
node.id=node-2
node.data-dir=/var/trino/data

http-server.http.port=8080
discovery.uri=http://coordinator-host:8080

query.max-memory-per-node=2GB
query.max-workers=500
```

### jvm.config
```
-server
-Xmx16G
-Xms16G
-XX:MaxDirectMemorySize=16G
-XX:+UseG1GC
-XX:G1HeapRegionSize=32M
-XX:+UseGCOverheadLimit
-XX:+ExplicitGCInvokesConcurrent
-XX:+HeapDumpOnOutOfMemoryError
-XX:+ExitOnOutOfMemoryError
-XX:ReservedCodeCacheSize=512M
-XX:+TrustFinalNonStaticFields
-XX:DeterministicRandomNumberGenerator=1
--add-modules=jdk.incubator.vector
```

### node.properties
```properties
node.environment=production
node.id=uuid-or-manual-id
node.data-dir=/data/trino
```

## Security Configuration

### Authentication

#### None (Development)
```properties
http-server.authentication.allow-insecure-over-http=true
http-server.authentication.type=NONE
```

#### LDAP
```properties
http-server.authentication.type=LDAP
ldap.config-file=etc/ldap.properties
```

**etc/ldap.properties:**
```properties
ldap.environment=production
ldap.url=ldaps://ldap.example.com:636
ldap.base-dn=dc=example,dc=com
ldap.user-search-filter=sAMAccountName={user}
ldap.group-search-filter=member={dn}
ldap.group-base-dn=ou=groups,dc=example,dc=com
```

#### OAuth2
```properties
http-server.authentication.type=OAUTH2
http-server.authentication.oauth2.provider=Google
http-server.authentication.oauth2.client-id=client_id
http-server.authentication.oauth2.client-secret=client_secret
http-server.authentication.oauth2.redirect-uri-base-url=https://trino.example.com
```

#### Kerberos
```properties
http-server.authentication.type=KERBEROS
http-server.kerberos.principal=trino/_HOST@EXAMPLE.COM
http-server.kerberos.keytab=/etc/trino/trino.keytab
```

### Authorization

#### Access Control Types
- **ALLOW_ALL**: Default, all operations allowed
- **File-based**: `etc/access-control.properties`
- **Ranger**: Via `trino-ranger` plugin
- **OPA**: Via `trino-opa` plugin

**etc/access-control.properties:**
```properties
access-control.name=file
```

### SSL/TLS
```properties
http-server.https.enabled=true
http-server.https.port=8443
http-server.https.certIFICATE=/path/to/cert.pem
http-server.https.key=/path/to/key.pem
```

## EventListener Plugins

### HTTP Event Listener
```properties
connector.name=http-event-listener
http-event-listener.url=http://collector:8080/trino
```

### OPA Integration
```properties
connector.name=opa
opa.config-file=etc/opa/config.json
```

### OpenLineage
```properties
connector.name=openlineage
openlineage.url=http://lineage:5000
openlineage.api-key=your-api-key
```

## Node Properties

### File-Based Discovery (Recommended)
```properties
# config.properties
discovery.uri=
discovery.file-enabled=true

# etc/discovery.properties
discovery.uri=http://coordinator:8080
```

### HTTP-Based Discovery (Legacy)
```properties
# config.properties
discovery.uri=http://coordinator:8080
```

## Log Configuration

### etc/log.properties
```properties
# Log levels by package
io.trino=INFO
io.trino.server=DEBUG
io.trino.execution=WARN
io.trino.operator=INFO
io.trino.sql=DEBUG
io.trino.spi=INFO
io.trino.transaction=INFO
com.facebook.airlift=INFO
```

## High Availability

### Coordinator HA with Proxy
```
                    ┌─────────────┐
                    │   Proxy/ LB  │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
        ┌─────▼─────┐ ┌───▼────┐ ┌────▼─────┐
        │ Coord 1   │ │Coord 2 │ │Coord 3  │
        └───────────┘ └────────┘ └──────────┘
```

### Multi-Cluster Federation
```properties
# Each cluster has its own coordinator
# Use federated catalog to query across clusters
connector.name=federated
federated.catalogs=cluster1,hive,iceberg
```

## Deployment Considerations

### Sizing Guidelines

| Cluster Size | Workers | RAM/Worker | CPUs/Worker |
|--------------|---------|------------|-------------|
| Small | 3-5 | 16-32 GB | 4-8 |
| Medium | 6-15 | 32-64 GB | 8-16 |
| Large | 16-50 | 64-128 GB | 16-32 |
| XL | 50+ | 128-256 GB | 32-64 |

### Disk Requirements
- **node.data-dir**: SSD/NVMe recommended for local spilling
- **Minimum**: 100 GB for metadata and spilling
- **Recommended**: 500 GB+ for production workloads

### Network Requirements
- **Internal**: 10 Gbps minimum between coordinator and workers
- **Data sources**: High bandwidth to data lakes (S3, HDFS)
- **Latency**: < 1ms between coordinator and workers

### Resource Group JSON Example
```json
[
  {
    "id": 1,
    "name": "interactive",
    "softMemoryLimit": "60%",
    "softCpuLimit": "60%",
    "maxQueued": 100,
    "schedulingPolicy": "fair",
    "userMaxQueries": 10,
    "userConcurrencyLimit": 5,
    "queryMaxMemory": "16GB",
    "queryMaxRunTime": "30m",
    "selector": [
      { "attribute": "user", "value": "admin" },
      { "attribute": "source", "value": "bi-tool" }
    ]
  },
  {
    "id": 2,
    "name": "batch",
    "softMemoryLimit": "40%",
    "softCpuLimit": "40%",
    "maxQueued": 1000,
    "schedulingPolicy": "fair",
    "userMaxQueries": 50,
    "queryMaxMemory": "32GB",
    "queryMaxRunTime": "12h"
  }
]
```
