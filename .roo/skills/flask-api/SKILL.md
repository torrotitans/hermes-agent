---
name: flask-api
description: Build, maintain, and refactor Flask API endpoints following Torro architecture standards including layered structure, SQLModel integration, OpenAPI documentation, and agentic documentation patterns.
license: MIT
compatibility:
  - python-3.12+
metadata:
  version: 1.1.0
  author: Torro Team
---

# Flask API Development Skill

## When to Use This Skill

Use this skill when you need to:
- Create new Flask API endpoints or routes
- Refactor existing Flask API code to follow Torro standards
- Add OpenAPI documentation or improve endpoint discoverability
- Implement authentication/authorization for API routes
- Structure API responses following enterprise patterns
- Use flask-openapi3 for automatic OpenAPI spec generation

## When NOT to Use This Skill

Do NOT use this skill when:
- Working on frontend/UI components (use `nextjs-enterprise` or `component-publisher` skills)
- Writing database models directly (use `backend-architecture` skill)
- Creating standalone scripts without HTTP interface
- Working on non-Flask web frameworks

## Inputs Required

Before starting, ensure you have:
1. Clear understanding of the API endpoint's purpose and data flow
2. Access to relevant SQLModel models (if database interaction is needed)
3. Knowledge of authentication requirements for the endpoint

## Workflow

### Step 1: Plan the Endpoint Structure

Identify the following before writing code:
- HTTP method (GET, POST, PUT, DELETE)
- Route path (follow REST conventions)
- Request schema (input validation)
- Response schema (output structure)
- Authentication requirements
- OpenAPI tags and summary for documentation

### Step 2: Create the API Interface File

Follow the naming convention: `interface_<entity>.py`

**Option A: Standard Flask Blueprint Pattern**

```python
"""
FN:interface_user.py
API interface for user-related HTTP endpoints.

Classes:
- UserApi: Handles user-related HTTP requests and responses

Functions:
- FN:list_users: Retrieve all users (lines 45-60)
- FN:get_user_by_id: Retrieve user by ID (lines 62-75)
- FN:create_user: Create new user (lines 77-95)
"""

from flask import Blueprint, jsonify, request
from sqlmodel import Session
from engine.db.models.user import User, UserCreate, UserPublic
from engine.db.core import get_session
from engine.common.common_response_process import process_response

user_api = Blueprint('user_api', __name__)

@user_api.route('/users', methods=['GET'])
def list_users(session: Session = None):
    """FN:list_users Retrieve all users from the database."""
    # Implementation follows in subsequent steps
    pass

@user_api.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id: int, session: Session = None):
    """FN:get_user_by_id Retrieve a specific user by ID."""
    pass

@user_api.route('/users', methods=['POST'])
def create_user(session: Session = None):
    """FN:create_user Create a new user in the database."""
    pass
```

**Option B: Flask-OpenAPI3 Pattern (Recommended for New Projects)**

```python
"""
FN:interface_user.py
API interface with OpenAPI documentation for user endpoints.

Classes:
- UserApi: Handles user-related HTTP requests with OpenAPI spec

Functions:
- FN:list_users: Retrieve all users (lines 45-60)
- FN:get_user_by_id: Retrieve user by ID (lines 62-75)
- FN:create_user: Create new user (lines 77-95)
"""

from flask_openapi3 import Blueprint, Tag
from sqlmodel import Session
from engine.db.models.user import User, UserCreate, UserPublic
from engine.db.core import get_session
from engine.common.common_response_process import process_response

# Define OpenAPI tags
user_tag = Tag(name="user", description="User management operations")

# Create blueprint with OpenAPI support
user_api = Blueprint('user_api', __name__, url_prefix='/api')

@user_api.get('/users', summary="List all users", tags=[user_tag])
def list_users(session: Session = None):
    """FN:list_users Retrieve all users from the database.
    
    Returns a list of all users in the system.
    """
    pass

@user_api.get('/users/<int:user_id>', summary="Get user by ID", tags=[user_tag])
def get_user_by_id(user_id: int, session: Session = None):
    """FN:get_user_by_id Retrieve a specific user by ID."""
    pass

@user_api.post('/users', summary="Create a new user", tags=[user_tag])
def create_user(session: Session = None):
    """FN:create_user Create a new user in the database."""
    pass
```

### Step 3: Implement Business Logic in DB Manager

Create or update the domain DB manager: `engine/db/<domain>/db_<domain>_mgr.py`

```python
"""
FN:db_user_mgr.py
Database manager for user-related operations.

Classes:
- UserDatabaseManager: Handles user data persistence and retrieval

Functions:
- FN:create_user: Creates a new user in the database (lines 45-60)
- FN:get_user_by_id: Retrieves user by ID (lines 62-75)
- FN:list_users: Lists all users (lines 77-90)
"""

from sqlmodel import Session, select
from engine.db.models.user import User, UserCreate

class UserDatabaseManager:
    """FN:UserDatabaseManager Database operations for user domain."""
    
    @staticmethod
    def create_user(session: Session, payload: UserCreate) -> User:
        """FN:create_user Create a new user in the database."""
        obj = User.model_validate(payload)
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj
    
    @staticmethod
    def get_user_by_id(session: Session, user_id: int) -> User | None:
        """FN:get_user_by_id Retrieve user by ID from the database."""
        return session.exec(select(User).where(User.id == user_id)).first()
    
    @staticmethod
    def list_users(session: Session) -> list[User]:
        """FN:list_users Retrieve all users from the database."""
        return session.exec(select(User)).all()
```

### Step 4: Wire Up the API Handler

Connect the API interface to the DB manager:

**Option A: Standard Flask Pattern**

```python
from flask import Blueprint, jsonify, request, current_app
from sqlmodel import Session
from engine.db.core import get_session
from engine.db.user.db_user_mgr import UserDatabaseManager
from engine.common.common_response_process import process_response
from engine.db.models.user import UserCreate, UserPublic

user_api = Blueprint('user_api', __name__)

@user_api.route('/users', methods=['GET'])
def list_users(session: Session = None):
    """FN:list_users Retrieve all users from the database."""
    try:
        users = UserDatabaseManager.list_users(session)
        return process_response(
            data=[user.model_dump() for user in users],
            message="Users retrieved successfully",
            status_code=200
        )
    except Exception as e:
        current_app.logger.error(f"FN:list_users Error: {str(e)}")
        return process_response(
            data=None,
            message="Failed to retrieve users",
            status_code=500
        )

@user_api.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id: int, session: Session = None):
    """FN:get_user_by_id Retrieve a specific user by ID."""
    try:
        user = UserDatabaseManager.get_user_by_id(session, user_id)
        if not user:
            return process_response(
                data=None,
                message="User not found",
                status_code=404
            )
        return process_response(
            data=user.model_dump(),
            message="User retrieved successfully",
            status_code=200
        )
    except Exception as e:
        current_app.logger.error(f"FN:get_user_by_id Error: {str(e)}")
        return process_response(
            data=None,
            message="Failed to retrieve user",
            status_code=500
        )

@user_api.route('/users', methods=['POST'])
def create_user(session: Session = None):
    """FN:create_user Create a new user in the database."""
    try:
        data = request.get_json()
        payload = UserCreate(**data)
        user = UserDatabaseManager.create_user(session, payload)
        return process_response(
            data=user.model_dump(),
            message="User created successfully",
            status_code=201
        )
    except Exception as e:
        current_app.logger.error(f"FN:create_user Error: {str(e)}")
        return process_response(
            data=None,
            message="Failed to create user",
            status_code=500
        )
```

### Step 5: Register the Blueprint

**Option A: Standard Flask Pattern**

In your main application file or API module's `main.py`:

```python
from flask import Flask
from engine.api.user.interface_user import user_api

def create_app():
    """FN:create_app Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Register blueprints
    app.register_blueprint(user_api, url_prefix='/api')
    
    return app
```

**Option B: Flask-OpenAPI3 Pattern**

```python
from flask_openapi3 import OpenAPI, Info
from engine.api.user.interface_user import user_api

# Define OpenAPI info
info = Info(title="Torro API", version="1.0.0", description="Torro Data Platform API")

# Create OpenAPI-enabled app
app = OpenAPI(__name__, info=info)

# Register blueprints
app.register_blueprint(user_api)

# Access OpenAPI spec at /openapi
# Access Swagger UI at /swagger
# Access Redoc at /redoc
```

### Step 6: Add Agentic Documentation

Update the `__init__.py` file with RAG anchor:

```python
"""
FN:__init__.py
Package: engine/api/user
Summary: User management API endpoints for CRUD operations.

Structure:
- interface_user.py (main API routes)
- main.py (blueprint registration)
- tasks/ (complex business logic if >200 lines)

Entry Points:
- interface_user.user_api (Flask Blueprint)
- interface_user.UserApi (API handler class)

Flow:
- UI -> engine/api/user/interface_user.py -> engine/db/user/db_user_mgr.py -> DB

Read First:
- interface_user.py
- engine/db/user/db_user_mgr.py
- engine/common/common_response_process.py
"""

from .interface_user import user_api, UserApi

__all__ = ['user_api', 'UserApi']
```

### Step 7: Write Unit Tests

Create test file in `tests/integration/api/`:

```python
"""
FN:test_user_api.py
Integration tests for user API endpoints.

Test Classes:
- TestUserApi: Tests for user CRUD operations

Test Functions:
- FN:test_create_user: Test user creation (lines 45-60)
- FN:test_get_user: Test user retrieval (lines 62-80)
- FN:test_list_users: Test user listing (lines 82-100)
"""

import pytest
from engine.api.user.interface_user import user_api

class TestUserApi:
    """FN:TestUserApi Test suite for user API endpoints."""
    
    def test_create_user(self, client, test_session):
        """FN:test_create_user Test creating a new user."""
        response = client.post('/api/users', json={
            'email': 'test@example.com',
            'full_name': 'Test User'
        })
        assert response.status_code == 201
        data = response.get_json()
        assert data['email'] == 'test@example.com'
    
    def test_get_user(self, client, test_session, test_user):
        """FN:test_get_user Test retrieving a user by ID."""
        response = client.get(f'/api/users/{test_user.id}')
        assert response.status_code == 200
        data = response.get_json()
        assert data['id'] == test_user.id
    
    def test_list_users(self, client, test_session, test_users):
        """FN:test_list_users Test listing all users."""
        response = client.get('/api/users')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == len(test_users)
```

## Files Reference

| File | Purpose |
|------|---------|
| `engine/api/<entity>/interface_<entity>.py` | API route definitions |
| `engine/db/<domain>/db_<domain>_mgr.py` | Database operations |
| `engine/api/<entity>/main.py` | Blueprint registration |
| `engine/api/<entity>/__init__.py` | Package RAG anchor |
| `tests/integration/api/test_<entity>_api.py` | Integration tests |

## Troubleshooting

### Issue: Circular Import Error

**Symptom**: `ImportError: cannot import name 'X' from partially initialized module`

**Solution**:
- Check import order in your files
- Move imports inside functions if needed
- Ensure DB layer doesn't import from API layer

### Issue: Session Not Available

**Symptom**: `RuntimeError: Working outside of request context`

**Solution**:
- Ensure session is injected via dependency injection
- Use `current_app` for accessing app context
- Check that blueprint is properly registered

### Issue: SQLModel Validation Error

**Symptom**: `pydantic.ValidationError` on request

**Solution**:
- Verify request schema matches SQLModel definition
- Check field types and required fields
- Add proper error handling for validation failures

## Examples

### Example 1: Simple GET Endpoint

```python
@user_api.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id: int, session: Session = None):
    """FN:get_user_by_id Retrieve user by ID."""
    user = UserDatabaseManager.get_user_by_id(session, user_id)
    if not user:
        return process_response(data=None, message="Not found", status_code=404)
    return process_response(data=user.model_dump(), status_code=200)
```

### Example 2: POST with Validation

```python
@user_api.route('/users', methods=['POST'])
def create_user(session: Session = None):
    """FN:create_user Create new user with validation."""
    data = request.get_json()
    payload = UserCreate(**data)  # Pydantic validation happens here
    user = UserDatabaseManager.create_user(session, payload)
    return process_response(data=user.model_dump(), status_code=201)
```

### Example 3: Error Handling Pattern

```python
from flask import current_app

@user_api.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id: int, session: Session = None):
    """FN:update_user Update user with error handling."""
    try:
        data = request.get_json()
        payload = UserUpdate(**data)
        user = UserDatabaseManager.update_user(session, user_id, payload)
        return process_response(data=user.model_dump(), status_code=200)
    except ValueError as e:
        current_app.logger.error(f"FN:update_user Validation error: {e}")
        return process_response(data=None, message=str(e), status_code=400)
    except Exception as e:
        current_app.logger.error(f"FN:update_user Unexpected error: {e}")
        return process_response(data=None, message="Server error", status_code=500)
```
