# SQLModel Enterprise Foundation

## SQLModel Standard (MANDATORY)
SQLModel is the **EXCLUSIVE** standard for all database interactions.

### Raw SQL PROHIBITION
Raw SQL is **FORBIDDEN** except in extreme cases. It requires:
1. Agent Approval.
2. Encapsulation with `FN:` prefix.
3. Justification comments.
4. Security review.

## CRUD Layer Rules
- **Session First**: Every CRUD function MUST have `session: Session` as the FIRST parameter.
- **Use `select()`**: No deprecated `session.query()`.
- **Use `model_validate()`**: Convert request schemas to table instances.
- **No Business Logic**: CRUD handle ONLY database operations.

```python
def create_entity(session: Session, payload: EntityCreate) -> Entity:
    obj = Entity.model_validate(payload)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj
```

## Refactoring Protocol
1. Identify Legacy Code (`session.execute`, `session.query`).
2. Move logic to domain DB managers leveraging `db_core_crud.py`.
3. Update API to call DB Manager.
4. Run compliance checks.
