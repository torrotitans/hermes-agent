# Data Quality Principles

## Mandatory Quality Dimensions
- **Accuracy**: Correct representation of real-world entities.
- **Completeness**: No missing critical fields.
- **Consistency**: No conflicts across sources.
- **Timeliness**: Updated within SLA.
- **Validity**: Conform to formats and domain rules.
- **Uniqueness**: No duplicated records within keys.

## Enforcement via dbt and DataHub
- **dbt**: Use built-in tests (`not_null`, `unique`, etc.) and custom SQL tests.
- **DataHub**: Use native assertions for freshness, volume, and field checks.
- **Ingestion**: Ingest dbt artifacts so results are visible as assertions in DataHub.

## Ownership & SLAs
Every dataset MUST have an explicit owner, SLA, and escalation path documented in its README.
