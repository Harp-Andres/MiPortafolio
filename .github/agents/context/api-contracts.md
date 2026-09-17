# API Contracts Index

Expected sources:
- OpenAPI definitions for backend endpoints
- Authentication and authorization expectations
- Request/response examples and error shapes

Minimum verification:
- Endpoint path exists
- Method and schema match tests
- Error contracts are asserted in API tests

If missing:
- generate baseline OpenAPI from FastAPI app
- track gaps in testing-matrix.md
