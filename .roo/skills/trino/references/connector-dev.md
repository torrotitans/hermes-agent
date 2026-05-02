# Trino Connector Development Reference

## Table of Contents

- [Development Setup](#development-setup)
- [SPI Overview](#spi-overview)
- [Connector Factory](#connector-factory)
- [Connector Metadata](#connector-metadata)
- [Connector HandleResolver](#connector-handleresolver)
- [Connector RecordCursor](#connector-recordcursor)
- [Connector Output](#connector-output)
- [Testing Connectors](#testing-connectors)
- [Building & Deploying](#building--deploying)

## Development Setup

### Prerequisites
- Java 25 (JEP 508 Vector API available)
- Maven 3.8+
- IntelliJ IDEA recommended

### Build Commands
```bash
# Build without tests
./mvnw clean install -DskipTests

# Build specific connector
./mvnw clean install -pl plugin/trino-my-connector

# Run checks before PR
./mvnw validate

# Format code (IntelliJ preferred)
mcp__idea__reformat_file
```

### Code Style Rules
- No wildcard imports
- Braces required for all control structures
- Use `TrinoException(errorCode)` for categorized errors
- Prefer AssertJ for assertions
- No mocking libraries - hand-write test mocks
- Avoid `var` - use explicit types
- Prefer Guava immutable collections

## SPI Overview

### Core SPI Interfaces

| Interface | Module | Purpose |
|-----------|--------|---------|
| `ConnectorFactory` | core | Creates connector instances |
| `Connector` | core | Factory for connector components |
| `ConnectorMetadata` | core | Schema/table metadata |
| `ConnectorSession` | core | Connector-specific session |
| `ConnectorHandleResolver` | core | Resolves handle types |
| `RecordCursor` | core | Reads data rows |
| `ConnectorRecordReader` | core | Reads records |
| `ConnectorRecordWriter` | core | Writes records |
| `ConnectorSplitSource` | core | Provides splits |
| `ConnectorSplit` | core | Data split for tasks |
| `ConnectorOutputTableHandle` | core | Write target handle |

### Handle Types Pattern

Handles represent logical objects and are serialized across cluster:

```java
// Handle interfaces must be serializable
public interface TableHandle extends Handle {
    CatalogHandle getCatalogHandle();
    String getTableName();
}

public interface ColumnHandle extends Handle {
    String getColumnName();
    Type getType();
}
```

## Connector Factory

```java
@ConnectorFactory("myconnector")
public class MyConnectorFactory implements ConnectorFactory {
    private static final Logger log = Logger.get(MyConnectorFactory.class);

    @Inject
    private MyConfigProvider configProvider;

    @Override
    public String getName() {
        return "myconnector";
    }

    @Override
    public Connector create(Config config, ConnectorContext context) {
        log.info("Creating myconnector");
        return new MyConnector(config, context);
    }
}
```

### Config Interface
```java
public interface Config {
    @Config("myconnector.property")
    @ConfigDocumentation("Description of property", "100MB")
    void setProperty(String property);

    String getProperty();
}
```

## Connector Metadata

```java
public class MyConnectorMetadata implements ConnectorMetadata {
    private final MyClient client;

    @Override
    public List<String> listSchemaNames(Session session) {
        return client.listSchemas();
    }

    @Override
    public Optional<TableHandle> getTableHandle(Session session, SchemaTableName table) {
        if (client.tableExists(table.getSchemaName(), table.getTableName())) {
            return Optional.of(new MyTableHandle(
                new CatalogHandle(session.getCatalogName()),
                table.getSchemaName(),
                table.getTableName()
            ));
        }
        return Optional.empty();
    }

    @Override
    public TableInfo getTableInfo(Session session, TableHandle tableHandle) {
        return new TableInfo(false); // false = not partitioned
    }

    @Override
    public List<ColumnHandle> getTableColumns(Session session, TableHandle tableHandle) {
        MyTable table = client.getTable(
            tableHandle.getSchemaName(),
            tableHandle.getTableName()
        );
        return table.getColumns().stream()
            .map(col -> new MyColumnHandle(col.getName(), col.getType()))
            .collect(toImmutableList());
    }

    @Override
    public Map<String, ColumnHandle> getColumnNames(Session session, TableHandle tableHandle) {
        return getTableColumns(session, tableHandle).stream()
            .collect(toImmutableMap(
                ColumnHandle::getName,
                identity()
            ));
    }
}
```

## Connector HandleResolver

```java
public class MyHandleResolver implements ConnectorHandleResolver {
    @Override
    public Class<? extends Handle> getHandleType(boolean output) {
        return MyHandle.class;
    }

    @Override
    public boolean isHandleType(Class<? extends Handle> handleClass, boolean output) {
        return MyTableHandle.class.isAssignableFrom(handleClass) ||
               MyColumnHandle.class.isAssignableFrom(handleClass) ||
               MySplit.class.isAssignableFrom(handleClass);
    }

    @Override
    public Handle readHandle(JsonCodec<Handle> codec, String serializedHandle) {
        return codec.fromJson(serializedHandle);
    }
}
```

## Connector RecordCursor

```java
public class MyRecordCursor implements RecordCursor {
    private final MyIterator iterator;
    private MyRow currentRow;
    private int currentColumn;

    @Override
    public Type getType(int column) {
        return schema.getColumns().get(column).getType();
    }

    @Override
    public boolean advanceNextPosition() {
        if (iterator.hasNext()) {
            currentRow = iterator.next();
            return true;
        }
        return false;
    }

    @Override
    public Object getLong(int column) {
        return currentRow.getLong(column);
    }

    @Override
    public Object getDouble(int column) {
        return currentRow.getDouble(column);
    }

    @Override
    public Object getSlice(int column) {
        return currentRow.getSlice(column);
    }

    @Override
    public Object getVarchar(int column, Type type) {
        return currentRow.getVarchar(column, type);
    }

    @Override
    public boolean isColumnSet(int column) {
        return currentRow.isColumnSet(column);
    }

    @Override
    public boolean isNull(int column) {
        return currentRow.isNull(column);
    }

    @Override
    public void close() {
        iterator.close();
    }
}
```

## Connector Split Source

```java
public class MySplitSource implements ConnectorSplitSource {
    private final Iterator<ConnectorSplit> splits;

    @Override
    public boolean isSplitDone() {
        return !splits.hasNext();
    }

    @Override
    public ConnectorSplitBatch getSplits(int limit, NodeProvider nodeProvider) {
        List<ConnectorSplit> batch = new ArrayList<>();
        int i = 0;
        while (splits.hasNext() && i < limit) {
            batch.add(splits.next());
            i++;
        }
        return new ConnectorSplitBatch(
            batch,
            isSplitDone() ? Optional.empty() : Optional.of(this)
        );
    }
}
```

## Connector Output

```java
public class MyConnectorOutputHandle implements ConnectorOutputTableHandle {
    private final SchemaTableName table;
    private final OutputFormatCodec<OutputFormat> outputFormatCodec;

    @Override
    public SchemaTableName getTableName() {
        return table;
    }
}

public class MyRecordWriter implements ConnectorRecordWriter {
    private final OutputFormat outputFormat;

    @Override
    public void writeRow(Object[] row) {
        MyRecord record = convertToRecord(row);
        try {
            outputFormat.write(record);
        } catch (IOException e) {
            throw new TrinoException(MY_CONNECTOR_WRITE_ERROR, e);
        }
    }

    @Override
    public ConnectorOutputMetadata getOutputMetadata() {
        return new MyConnectorOutputMetadata(table);
    }

    @Override
    public long getWrittenRows() {
        return outputFormat.getWrittenRows();
    }

    @Override
    public void close() throws IOException {
        outputFormat.close();
    }
}
```

## Testing Connectors

### QueryRunner Base
```java
public class MyQueryRunner {
    private static TestQueryRunner queryRunner;

    @BeforeClass
    public static void startQueryRunner() throws IOException {
        Multimap<String, Property> extraProperties = ArrayListMultimap.create();
        extraProperties.put("catalog", "my");
        extraProperties.put("my.catalog", "test");

        queryRunner = new TestQueryRunner();
        queryRunner.addConnector("my", extraProperties);
        queryRunner.initialize();
    }

    @AfterClass
    public static void stopQueryRunner() {
        if (queryRunner != null) {
            queryRunner.close();
        }
    }

    @Test
    public void testSimpleQuery() {
        queryRunner.execute("SELECT * FROM my.db.test_table");
        QueryResult result = queryRunner.getQueryResults();
        assertEquals(result.getColumns().size(), 3);
    }
}
```

### Integration Test Pattern
```java
public class MyConnectorTest extends AbstractTestQueryFramework {
    @Test
    public void testTableExists() {
        assertQueryReturns(
            "SELECT table_name FROM information_schema.tables WHERE table_catalog = 'my'",
            "VALUES 'test_table'"
        );
    }

    @Test
    public void testSimpleSelect() {
        assertQueryReturns(
            "SELECT id, name FROM my.db.test_table ORDER BY id",
            "VALUES 1, 'one'" + System.lineSeparator() +
            "VALUES 2, 'two'"
        );
    }
}
```

## Building & Deploying

### Build Plugin JAR
```bash
./mvnw clean package -pl plugin/trino-my-connector -am -DskipTests
```

### Deploy to Cluster
```bash
# Copy JAR to plugins directory
cp plugin/trino-my-connector/target/trino-my-connector-450.jar \
   /etc/trino/plugins/trino-my-connector/trino-my-connector-450.jar

# Restart Trino
systemctl restart trino
```

### Plugin Directory Structure
```
etc/trino/plugins/
└── trino-my-connector/
    ├── trino-my-connector-450.jar
    └── pom.xml  (optional, for dependency resolution)
```

### SPI Registration
Register the factory in `src/main/resources/META-INF/services/io.trino.spi.connector.ConnectorFactory`:
```
com.example.MyConnectorFactory
```

## Connector Testing Checklist

- [ ] `listSchemaNames` returns expected schemas
- [ ] `getTableHandle` returns handle for existing tables
- [ ] `getTableHandle` returns empty for non-existing tables
- [ ] `getTableColumns` returns correct column types
- [ ] Simple SELECT queries execute successfully
- [ ] WHERE clause filtering works
- [ ] Aggregation queries work (SUM, COUNT, AVG)
- [ ] JOIN queries work with other connectors
- [ ] Error handling returns appropriate TrinoException codes
- [ ] Code passes checkstyle and modernizer checks
- [ ] No wildcard imports
- [ ] All exceptions categorized with error codes
