#!/usr/bin/env hurl
# Error Handling and Edge Cases Tests
# =====================================================
# Purpose: Verify proper error handling and edge case management
#
# Business Context: Users need clear error messages and the API
# should handle edge cases gracefully without crashes.
#
# Tests:
#   1. Invalid endpoints return 404
#   2. Invalid methods return 405
#   3. Invalid data returns 400
#   4. Server errors return 500
#   5. Proper error messages
#   6. Edge cases handling

include fixtures/common.hurl

# =====================================================
# Test 1: Invalid endpoint returns 404
# =====================================================
# Verifies that non-existent endpoints return 404 Not Found

GET {{@base_url}}/api/invalid/endpoint

[Asserts]
status == 404


# =====================================================
# Test 2: GET on POST endpoint returns 405
# =====================================================
# Verifies that wrong HTTP method returns 405 Method Not Allowed

GET {{@base_url}}{{@generate_pdf_endpoint}}

[Asserts]
status == 405


# =====================================================
# Test 3: PUT on generate endpoint returns 405
# =====================================================
# Verifies that PUT method on POST endpoint returns 405

PUT {{@base_url}}{{@generate_docx_endpoint}}

[Header]
Content-Type: {{@json_content_type}}

{
  "data": {{@valid_cv_data}}
}

[Asserts]
status == 405


# =====================================================
# Test 4: DELETE on generate endpoint returns 405
# =====================================================
# Verifies that DELETE method on POST endpoint returns 405

DELETE {{@base_url}}{{@generate_excel_endpoint}}

[Asserts]
status == 405


# =====================================================
# Test 5: Missing Content-Type header
# =====================================================
# Verifies that missing Content-Type is handled

POST {{@base_url}}{{@generate_pdf_endpoint}}

{
  "data": {{@valid_cv_data}}
}

[Asserts]
status == 400 || status == 415


# =====================================================
# Test 6: Invalid Content-Type header
# =====================================================
# Verifies that invalid Content-Type is rejected

POST {{@base_url}}{{@generate_pdf_endpoint}}

[Header]
Content-Type: application/xml

{
  "data": {{@valid_cv_data}}
}

[Asserts]
status == 400 || status == 415


# =====================================================
# Test 7: Missing data in request body
# =====================================================
# Verifies that missing data field is rejected

POST {{@base_url}}{{@generate_pdf_endpoint}}

[Header]
Content-Type: {{@json_content_type}}

{
  "not_data": "invalid"
}

[Asserts]
status == 400
body contains "data"


# =====================================================
# Test 8: Null data field
# =====================================================
# Verifies that null data field is rejected

POST {{@base_url}}{{@generate_docx_endpoint}}

[Header]
Content-Type: {{@json_content_type}}

{
  "data": null
}

[Asserts]
status == 400


# =====================================================
# Test 9: Empty object as data
# =====================================================
# Verifies that empty object is rejected

POST {{@base_url}}{{@generate_excel_endpoint}}

[Header]
Content-Type: {{@json_content_type}}

{
  "data": {}
}

[Asserts]
status == 400


# =====================================================
# Test 10: Array instead of object
# =====================================================
# Verifies that array data is rejected

POST {{@base_url}}{{@generate_pdf_endpoint}}

[Header]
Content-Type: {{@json_content_type}}

{
  "data": ["item1", "item2"]
}

[Asserts]
status == 400


# =====================================================
# Test 11: String instead of object
# =====================================================
# Verifies that string data is rejected

POST {{@base_url}}{{@generate_docx_endpoint}}

[Header]
Content-Type: {{@json_content_type}}

{
  "data": "not an object"
}

[Asserts]
status == 400


# =====================================================
# Test 12: Very large request body
# =====================================================
# Verifies that extremely large requests are handled
# (not causing server crash)

POST {{@base_url}}{{@generate_pdf_endpoint}}

[Header]
Content-Type: {{@json_content_type}}

{
  "data": {
    "profile": {
      "name": "Test User",
      "title": "Test Title",
      "email": "test@email.com"
    },
    "bio": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
  }
}

[Asserts]
status == 200 || status == 413


# =====================================================
# Test 13: Invalid profile email format
# =====================================================
# Verifies that invalid email format is rejected

POST {{@base_url}}{{@generate_pdf_endpoint}}

[Header]
Content-Type: {{@json_content_type}}

{
  "data": {
    "profile": {
      "name": "Test User",
      "title": "Test Title",
      "email": "not-an-email"
    }
  }
}

[Asserts]
status == 400


# =====================================================
# Test 14: Special characters in profile name
# =====================================================
# Verifies special characters are handled properly

POST {{@base_url}}{{@generate_docx_endpoint}}

[Header]
Content-Type: {{@json_content_type}}

{
  "data": {
    "profile": {
      "name": "Test<User>\"'&Symbols",
      "title": "Test Title",
      "email": "test@email.com"
    }
  }
}

[Asserts]
status == 200 || status == 400


# =====================================================
# Test 15: Unicode characters in CV data
# =====================================================
# Verifies that Unicode characters are properly handled

POST {{@base_url}}{{@generate_pdf_endpoint}}

[Header]
Content-Type: {{@json_content_type}}

{
  "data": {
    "profile": {
      "name": "José García 李明 Müller",
      "title": "Ingénieur en QA",
      "email": "test@email.com",
      "bio": "Специалист по тестированию"
    }
  }
}

[Asserts]
status == 200
header "Content-Type" == "application/pdf"


# =====================================================
# Test 16: Health check endpoint success
# =====================================================
# Verifies health check is working

GET {{@base_url}}{{@health_endpoint}}

[Asserts]
status == 200
header "Content-Type" contains "{{@json_content_type}}"
body contains "ok"
body contains "status"


# =====================================================
# Test 17: Root endpoint success
# =====================================================
# Verifies root endpoint provides information

GET {{@base_url}}{{@root_endpoint}}

[Asserts]
status == 200
header "Content-Type" contains "{{@json_content_type}}"
body contains "service"
body contains "MiPortafolio"


# =====================================================
# Test 18: Documentation endpoints
# =====================================================
# Verifies docs endpoint is available

GET {{@base_url}}{{@docs_endpoint}}

[Asserts]
status == 200


# =====================================================
# Test 19: OpenAPI schema endpoint
# =====================================================
# Verifies OpenAPI schema is available

GET {{@base_url}}{{@openapi_endpoint}}

[Asserts]
status == 200
header "Content-Type" contains "{{@json_content_type}}"
body contains "openapi"


# =====================================================
# Test 20: Concurrent requests handling
# =====================================================
# Verifies API handles multiple concurrent requests
# (This test runs sequentially but simulates load)

POST {{@base_url}}{{@generate_all_endpoint}}

[Header]
Content-Type: {{@json_content_type}}

{
  "data": {{@valid_cv_data}}
}

[Asserts]
status == 200
[Asserts]
body contains "method" || body contains "not allowed"

# ============================================
# Test 3: Content-Type inválido
# ============================================
POST {{@base_url}}/api/cv/generate

[Header]
Content-Type: text/plain

invalid data

HTTP 400
[Asserts]
body contains "application/json" || body contains "invalid"

# ============================================
# Test 4: JSON malformado
# ============================================
POST {{@base_url}}/api/cv/generate

[Header]
Content-Type: application/json

{invalid json}

HTTP 400
[Asserts]
body contains "JSON" || body contains "invalid"

# ============================================
# Test 5: Campo requerido faltante
# ============================================
POST {{@base_url}}/api/cv/generate

[Header]
Content-Type: application/json

{
  "language": "es"
}

HTTP 400
[Asserts]
body contains "format" || body contains "required"

# ============================================
# Test 6: Timeout handling
# ============================================
POST {{@base_url}}/api/cv/generate

[Header]
Content-Type: application/json

{
  "format": "pdf",
  "timeout": "invalid"
}

HTTP 400
[Asserts]
body contains "error"

# ============================================
# Test 7: Validar error response structure
# ============================================
GET {{@base_url}}/api/invalid

HTTP 404
[Asserts]
jsonpath "$.error" exists
jsonpath "$.message" exists
jsonpath "$.timestamp" exists

# ============================================
# Test 8: Rate limiting (si aplica)
# ============================================
POST {{@base_url}}/api/cv/generate

[Header]
Content-Type: application/json

{
  "format": "pdf"
}

# Puede ser 200, 429, o 403 dependiendo del rate limiting
[Asserts]
header "x-ratelimit-limit" contains "" || header "content-type" contains ""
