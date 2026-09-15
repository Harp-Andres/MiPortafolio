#!/usr/bin/env hurl
# Document Generation Tests
# =====================================================
# Purpose: Verify that documents (PDF, DOCX, Excel) are generated
# correctly with all required data and proper formatting
#
# Business Context: Users need reliable document generation
# to download their professional CV in multiple formats
#
# Tests:
#   1. PDF generation with various data sizes
#   2. DOCX generation with formatting preservation
#   3. Excel generation with structured data
#   4. Performance validation for large datasets

include fixtures/common.hurl

# =====================================================
# Test 1: PDF generation with complete CV
# =====================================================
# Verifies PDF file is generated with proper format

POST {{@base_url}}{{@generate_pdf_endpoint}}

[Header]
Content-Type: {{@json_content_type}}

{
  "data": {{@valid_cv_data}}
}

[Asserts]
status == 200
header "Content-Type" == "application/pdf"
header "Content-Disposition" contains "filename="
header "Content-Length" exists
header "Content-Length" > "5000"  # PDF should be sizeable

[Captures]
pdf_file_size: header "Content-Length"


# =====================================================
# Test 2: DOCX generation with complete CV
# =====================================================
# Verifies DOCX file is generated with proper Office format

POST {{@base_url}}{{@generate_docx_endpoint}}

[Header]
Content-Type: {{@json_content_type}}

{
  "data": {{@valid_cv_data}}
}

[Asserts]
status == 200
header "Content-Type" == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
header "Content-Disposition" contains "filename="
header "Content-Length" exists
header "Content-Length" > "5000"  # DOCX should be sizeable

[Captures]
docx_file_size: header "Content-Length"


# =====================================================
# Test 3: Excel generation with complete CV
# =====================================================
# Verifies Excel file is generated with proper spreadsheet format

POST {{@base_url}}{{@generate_excel_endpoint}}

[Header]
Content-Type: {{@json_content_type}}

{
  "data": {{@valid_cv_data}}
}

[Asserts]
status == 200
header "Content-Type" == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
header "Content-Disposition" contains "filename="
header "Content-Length" exists
header "Content-Length" > "5000"  # Excel should be sizeable

[Captures]
excel_file_size: header "Content-Length"


# =====================================================
# Test 4: PDF generation with profile only
# =====================================================
# Tests minimal profile data in PDF generation

POST {{@base_url}}{{@generate_pdf_endpoint}}

[Header]
Content-Type: {{@json_content_type}}

{
  "data": {
    "profile": {
      "name": "John Doe",
      "title": "Software Engineer",
      "email": "john@example.com"
    }
  }
}

[Asserts]
status == 200
header "Content-Type" == "application/pdf"
header "Content-Length" > "1000"


# =====================================================
# Test 5: DOCX generation with extended experience
# =====================================================
# Tests DOCX generation with rich experience data

POST {{@base_url}}{{@generate_docx_endpoint}}

[Header]
Content-Type: {{@json_content_type}}

{
  "data": {
    "profile": {
      "name": "Test User",
      "title": "Test Title",
      "email": "test@email.com"
    },
    "experience": [
      {
        "company": "Company A",
        "position": "Senior Role",
        "startDate": "2020-01",
        "endDate": "present",
        "description": "Leading team and projects"
      },
      {
        "company": "Company B",
        "position": "Mid-level Role",
        "startDate": "2018-06",
        "endDate": "2019-12",
        "description": "Developing features and automation"
      }
    ]
  }
}

[Asserts]
status == 200
header "Content-Type" contains "wordprocessingml"
header "Content-Length" > "1000"


# =====================================================
# Test 6: Excel generation with skills data
# =====================================================
# Tests Excel generation with structured skills

POST {{@base_url}}{{@generate_excel_endpoint}}

[Header]
Content-Type: {{@json_content_type}}

{
  "data": {
    "profile": {
      "name": "Test User",
      "title": "QA Engineer",
      "email": "qa@email.com"
    },
    "skills": [
      {
        "category": "Testing",
        "skills": [
          {"name": "Selenium", "level": "expert"},
          {"name": "Playwright", "level": "expert"}
        ]
      },
      {
        "category": "Programming",
        "skills": [
          {"name": "Python", "level": "advanced"},
          {"name": "JavaScript", "level": "advanced"}
        ]
      }
    ]
  }
}

[Asserts]
status == 200
header "Content-Type" contains "spreadsheetml"
header "Content-Length" > "1000"


# =====================================================
# Test 7: PDF generation with education data
# =====================================================
# Tests PDF generation with education records

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
    "education": [
      {
        "institution": "University A",
        "degree": "Bachelor's",
        "field": "Computer Science",
        "year": 2020
      }
    ]
  }
}

[Asserts]
status == 200
header "Content-Type" == "application/pdf"
header "Content-Length" > "1000"


# =====================================================
# Test 8: PDF filename format
# =====================================================
# Verifies PDF filename follows expected format (CV_YYYYMMDD_HHMMSS.pdf)

POST {{@base_url}}{{@generate_pdf_endpoint}}

[Header]
Content-Type: {{@json_content_type}}

{
  "data": {{@valid_cv_data}}
}

[Asserts]
status == 200
header "Content-Disposition" contains "CV_"
header "Content-Disposition" contains ".pdf"


# =====================================================
# Test 9: DOCX filename format
# =====================================================
# Verifies DOCX filename follows expected format

POST {{@base_url}}{{@generate_docx_endpoint}}

[Header]
Content-Type: {{@json_content_type}}

{
  "data": {{@valid_cv_data}}
}

[Asserts]
status == 200
header "Content-Disposition" contains "CV_"
header "Content-Disposition" contains ".docx"


# =====================================================
# Test 10: Excel filename format
# =====================================================
# Verifies Excel filename follows expected format

POST {{@base_url}}{{@generate_excel_endpoint}}

[Header]
Content-Type: {{@json_content_type}}

{
  "data": {{@valid_cv_data}}
}

[Asserts]
status == 200
header "Content-Disposition" contains "CV_"
header "Content-Disposition" contains ".xlsx"


# =====================================================
# Test 11: PDF generation response time
# =====================================================
# Verifies PDF generation completes within acceptable time

POST {{@base_url}}{{@generate_pdf_endpoint}}

[Header]
Content-Type: {{@json_content_type}}

{
  "data": {{@valid_cv_data}}
}

[Asserts]
status == 200
header "Content-Type" == "application/pdf"
response_time < "{{@timeout_long}}"  # Must complete within 10 seconds


# =====================================================
# Test 12: DOCX generation response time
# =====================================================
# Verifies DOCX generation completes within acceptable time

POST {{@base_url}}{{@generate_docx_endpoint}}

[Header]
Content-Type: {{@json_content_type}}

{
  "data": {{@valid_cv_data}}
}

[Asserts]
status == 200
header "Content-Type" contains "wordprocessingml"
response_time < "{{@timeout_long}}"  # Must complete within 10 seconds


# =====================================================
# Test 13: Excel generation response time
# =====================================================
# Verifies Excel generation completes within acceptable time

POST {{@base_url}}{{@generate_excel_endpoint}}

[Header]
Content-Type: {{@json_content_type}}

{
  "data": {{@valid_cv_data}}
}

[Asserts]
status == 200
header "Content-Type" contains "spreadsheetml"
response_time < "{{@timeout_long}}"  # Must complete within 10 seconds


# =====================================================
# Test 14: All formats generation performance
# =====================================================
# Verifies generating all formats together completes on time

POST {{@base_url}}{{@generate_all_endpoint}}

[Header]
Content-Type: {{@json_content_type}}

{
  "data": {{@valid_cv_data}}
}

[Asserts]
status == 200
response_time < "{{@timeout_long}}"  # Must complete within 10 seconds
body contains "files"


# =====================================================
# Test 15: PDF with special characters
# =====================================================
# Tests PDF generation with special characters (accents, etc.)

POST {{@base_url}}{{@generate_pdf_endpoint}}

[Header]
Content-Type: {{@json_content_type}}

{
  "data": {
    "profile": {
      "name": "Andrés Rodríguez García",
      "title": "Ingeniero en QA - Especialista",
      "email": "andres@test.com",
      "bio": "Especializado en pruebas: UI, API y Performance"
    }
  }
}

[Asserts]
status == 200
header "Content-Type" == "application/pdf"
