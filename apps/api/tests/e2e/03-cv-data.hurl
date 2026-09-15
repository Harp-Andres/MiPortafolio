# CV Data Management E2E Tests
# Testing CV data endpoints

@base_url=http://localhost:8000

# ============================================
# Test 1: Obtener CV data actual
# ============================================
GET {{@base_url}}/api/cv/data

HTTP 200
[Captures]
cv_id: body jsonpath "$.id"
cv_name: body jsonpath "$.personalInfo.fullName"

[Asserts]
header "content-type" contains "application/json"
body contains "personalInfo"
body contains "experience"
body contains "education"
body contains "skills"

# ============================================
# Test 2: Validar estructura de CV data
# ============================================
GET {{@base_url}}/api/cv/data

HTTP 200
[Asserts]
jsonpath "$.personalInfo" exists
jsonpath "$.personalInfo.fullName" exists
jsonpath "$.personalInfo.email" exists
jsonpath "$.experience" isArray
jsonpath "$.education" isArray
jsonpath "$.skills" isArray

# ============================================
# Test 3: Obtener sección específica - Experience
# ============================================
GET {{@base_url}}/api/cv/data/experience

HTTP 200
[Asserts]
jsonpath "$" isArray
jsonpath "$[0].company" exists
jsonpath "$[0].position" exists
jsonpath "$[0].startDate" exists

# ============================================
# Test 4: Obtener sección específica - Skills
# ============================================
GET {{@base_url}}/api/cv/data/skills

HTTP 200
[Asserts]
jsonpath "$" isArray
jsonpath "$[0].category" exists
jsonpath "$[0].items" exists

# ============================================
# Test 5: Obtener sección específica - Education
# ============================================
GET {{@base_url}}/api/cv/data/education

HTTP 200
[Asserts]
jsonpath "$" isArray
jsonpath "$[0].institution" exists
jsonpath "$[0].degree" exists

# ============================================
# Test 6: Actualizar CV data
# ============================================
PUT {{@base_url}}/api/cv/data

[Header]
Content-Type: application/json

{
  "personalInfo": {
    "fullName": "Test User",
    "email": "test@example.com",
    "phone": "+1234567890"
  },
  "experience": [],
  "education": [],
  "skills": []
}

HTTP 200
[Captures]
updated_at: body jsonpath "$.updatedAt"

[Asserts]
body contains "Test User"

# ============================================
# Test 7: Validar CV data integridad
# ============================================
GET {{@base_url}}/api/cv/data

HTTP 200
[Asserts]
jsonpath "$.personalInfo.fullName" isString
jsonpath "$.personalInfo.email" isString
jsonpath "$.experience" isArray
jsonpath "$.education" isArray
jsonpath "$.skills" isArray
