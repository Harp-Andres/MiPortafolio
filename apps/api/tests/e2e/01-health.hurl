# Health Check E2E Tests
# Verifica que la API está corriendo y responde correctamente

# ============================================
# Test 1: Health endpoint básico
# ============================================
GET http://localhost:8000/health

HTTP 200
[Asserts]
body contains "ok"

# ============================================
# Test 2: Endpoint raíz
# ============================================
GET http://localhost:8000

HTTP 200

# ============================================
# Test 3: Documentación Swagger
# ============================================
GET http://localhost:8000/docs

HTTP 200
[Asserts]
header "content-type" contains "text/html"

# ============================================
# Test 4: OpenAPI schema
# ============================================
GET http://localhost:8000/openapi.json

HTTP 200
[Asserts]
header "content-type" contains "application/json"
body contains "openapi"
body contains "paths"
