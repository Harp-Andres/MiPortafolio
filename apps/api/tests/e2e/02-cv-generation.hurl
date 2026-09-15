# CV Generation E2E Tests with Hurl
# Testing document generation endpoints

# ============================================
# Setup: Cargar datos de prueba
# ============================================

# Variables de prueba
@base_url=http://localhost:8000
@cv_format_pdf=pdf
@cv_format_docx=docx
@cv_format_excel=excel

# ============================================
# Test 1: Generar CV en PDF
# ============================================
POST {{@base_url}}/api/cv/generate

[Header]
Content-Type: application/json

{
  "format": "{{@cv_format_pdf}}",
  "includeProfilePhoto": true,
  "language": "es"
}

HTTP 200
[Captures]
pdf_response_time: header "x-response-time"

[Asserts]
header "content-type" contains "application/pdf"
header "content-length" > 0
header "content-disposition" contains "attachment"

# ============================================
# Test 2: Generar CV en DOCX
# ============================================
POST {{@base_url}}/api/cv/generate

[Header]
Content-Type: application/json

{
  "format": "{{@cv_format_docx}}",
  "includeProfilePhoto": true,
  "language": "es"
}

HTTP 200
[Asserts]
header "content-type" contains "vnd.openxmlformats-officedocument.wordprocessingml"
header "content-disposition" contains "attachment"

# ============================================
# Test 3: Generar CV en Excel
# ============================================
POST {{@base_url}}/api/cv/generate

[Header]
Content-Type: application/json

{
  "format": "{{@cv_format_excel}}",
  "language": "es"
}

HTTP 200
[Asserts]
header "content-type" contains "spreadsheetml"

# ============================================
# Test 4: Validar entrada inválida
# ============================================
POST {{@base_url}}/api/cv/generate

[Header]
Content-Type: application/json

{
  "format": "invalid_format"
}

HTTP 400
[Asserts]
body contains "error" || body contains "invalid"

# ============================================
# Test 5: Generar CV sin datos obligatorios
# ============================================
POST {{@base_url}}/api/cv/generate

[Header]
Content-Type: application/json

{}

HTTP 400
[Asserts]
body contains "format" || body contains "required"

# ============================================
# Test 6: Validar performance - PDF < 5s
# ============================================
POST {{@base_url}}/api/cv/generate

[Header]
Content-Type: application/json

{
  "format": "{{@cv_format_pdf}}"
}

HTTP 200
[Asserts]
header "x-response-time" < "5000"

# ============================================
# Test 7: Validar múltiples idiomas
# ============================================
POST {{@base_url}}/api/cv/generate

[Header]
Content-Type: application/json

{
  "format": "{{@cv_format_pdf}}",
  "language": "en"
}

HTTP 200
[Asserts]
header "content-type" contains "pdf"
