# Flask Enterprise Standards

## OpenAPI 3 & Thin Handlers
The `interface_*.py` files must strictly manage HTTP concerns.

- **APIBlueprint**: Use `flask-openapi3`.
- **Validation**: Use **Pydantic V2** `BaseModel`.
- **Method Encapsulation**: Routes must be in PascalCase classes using `@staticmethod`.
- **API Versioning**: Prefix all internal routes with `/api/v1/`.

## Standardized Endpoint Example
```python
class AssetInterface:
    @staticmethod
    @asset_bp.post('/', summary="Create an Asset", responses={201: AssetBaseResponse})
    @login_required
    def create_asset_v1(body: AssetCreateRequest):
        task = AssetCreateTask()
        result = task.run(body.model_dump())
        return response_result_process(result)
```

## Exception Handling (RFC 7807)
All API error responses MUST follow RFC 7807 Problem Details format.

```json
{
  "type": "https://torro.example.com/errors/validation-error",
  "title": "Validation Error",
  "status": 400,
  "detail": "The request contains invalid parameters.",
  "instance": "/api/v1/assets"
}
```

## Request Correlation
All API requests MUST include a correlation ID (`X-Request-ID`) for distributed tracing.
