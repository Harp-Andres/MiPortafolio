#!/usr/bin/env hurl
# Data Validation and Integrity Tests
# =====================================================
# Purpose: Verify that CV data is validated correctly
# and maintains integrity across all operations
#
# Business Context: Data integrity is critical for professional CVs.
# Invalid data should be rejected, and updates must be consistent.
#
# Tests:
#   1. Valid data acceptance
#   2. Invalid data rejection
#   3. Required field validation
#   4. Data type validation
#   5. Data integrity after updates

include fixtures/common.hurl

# =====================================================
# Test 1: Accept valid complete CV data
# =====================================================
# Verifies that complete valid CV data is accepted

POST {{@base_url}}{{@generate_pdf_endpoint}}

[Header]
Content-Type: {{@json_content_type}}

{
  "data": {{@valid_cv_data}}
}

[Asserts]
status == 200
header "Content-Type" contains "application/pdf"


# =====================================================
# Test 2: Accept minimal valid CV data
# =====================================================
# Verifies that minimal valid CV data (profile only) is accepted

POST {{@base_url}}{{@generate_docx_endpoint}}

[Header]
Content-Type: {{@json_content_type}}

{
  "data": {{@minimal_cv_data}}
}

[Asserts]
status == 200
header "Content-Type" contains "wordprocessingml"


# =====================================================
# Test 3: Reject CV data with invalid profile
# =====================================================
# Verifies that CV data with invalid/missing profile is rejected

POST {{@base_url}}{{@generate_pdf_endpoint}}

[Header]
Content-Type: {{@json_content_type}}

{
  "data": {
    "invalid_section": "This is not a valid CV"
  }
}

[Asserts]
status == 400
header "Content-Type" contains "{{@json_content_type}}"
body contains "Invalid"


# =====================================================
# Test 4: Reject CV data with empty profile
# =====================================================
# Verifies that CV data with empty profile is rejected

POST {{@base_url}}{{@generate_docx_endpoint}}

[Header]
Content-Type: {{@json_content_type}}

{
  "data": {
    "profile": {}
  }
}

[Asserts]
status == 400
header "Content-Type" contains "{{@json_content_type}}"


# =====================================================
# Test 5: Reject CV data with missing email
# =====================================================
# Verifies that CV data without email is handled appropriately

POST {{@base_url}}{{@generate_excel_endpoint}}

[Header]
Content-Type: {{@json_content_type}}

{
  "data": {
    "profile": {
      "name": "Test User",
      "title": "Test Title"
    }
  }
}

[Asserts]
status == 400


# =====================================================
# Test 6: Validate profile name requirement
# =====================================================
# Verifies that profile name is required

POST {{@base_url}}{{@generate_pdf_endpoint}}

[Header]
Content-Type: {{@json_content_type}}

{
  "data": {
    "profile": {
      "email": "test@email.com",
      "title": "Test"
    }
  }
}

[Asserts]
status == 400
body contains "required"


# =====================================================
# Test 7: Validate profile title requirement
# =====================================================
# Verifies that profile title is required

POST {{@base_url}}{{@generate_docx_endpoint}}

[Header]
Content-Type: {{@json_content_type}}

{
  "data": {
    "profile": {
      "name": "Test User",
      "email": "test@email.com"
    }
  }
}

[Asserts]
status == 400
body contains "required"


# =====================================================
# Test 8: Accept CV data with extended experience
# =====================================================
# Verifies that valid experience data is accepted

POST {{@base_url}}{{@generate_pdf_endpoint}}

[Header]
Content-Type: {{@json_content_type}}

{
  "data": {
    "profile": {
      "name": "Test User",
      "title": "QA Engineer",
      "email": "qa@email.com"
    },
    "experience": [
      {
        "company": "Company A",
        "position": "Senior QA",
        "startDate": "2020-01",
        "endDate": "present",
        "description": "Leading QA initiatives"
      },
      {
        "company": "Company B",
        "position": "QA Engineer",
        "startDate": "2018-01",
        "endDate": "2019-12",
        "description": "Test automation"
      }
    ]
  }
}

[Asserts]
status == 200
header "Content-Type" == "application/pdf"


# =====================================================
# Test 9: Accept CV data with skills
# =====================================================
# Verifies that valid skills data is accepted

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
    "skills": [
      {
        "category": "Testing",
        "skills": [
          {"name": "Selenium", "level": "expert"},
          {"name": "Playwright", "level": "expert"}
        ]
      }
    ]
  }
}

[Asserts]
status == 200
header "Content-Type" contains "wordprocessingml"


# =====================================================
# Test 10: Accept CV data with education
# =====================================================
# Verifies that valid education data is accepted

POST {{@base_url}}{{@generate_excel_endpoint}}

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
        "institution": "University",
        "degree": "Bachelor's",
        "field": "Computer Science",
        "year": 2020
      }
    ]
  }
}

[Asserts]
status == 200
header "Content-Type" contains "spreadsheetml"


# =====================================================
# Test 11: Validate email format
# =====================================================
# Verifies that email format is validated (basic validation)

POST {{@base_url}}{{@generate_pdf_endpoint}}

[Header]
Content-Type: {{@json_content_type}}

{
  "data": {
    "profile": {
      "name": "Test User",
      "title": "Test Title",
      "email": "invalid-email-format"
    }
  }
}

[Asserts]
status == 400


# =====================================================
# Test 12: Accept valid email formats
# =====================================================
# Verifies that valid email formats are accepted

POST {{@base_url}}{{@generate_docx_endpoint}}

[Header]
Content-Type: {{@json_content_type}}

{
  "data": {
    "profile": {
      "name": "Test User",
      "title": "Test Title",
      "email": "valid.email+test@example.co.uk"
    }
  }
}

[Asserts]
status == 200


# =====================================================
# Test 13: Preserve data through update cycle
# =====================================================
# Verifies that updated CV data is properly stored

POST {{@base_url}}{{@generate_all_endpoint}}

[Header]
Content-Type: {{@json_content_type}}

{
  "data": {{@updated_cv_data}}
}

[Asserts]
status == 200
body contains "files"
jsonpath "$.files.docx" exists
jsonpath "$.files.pdf" exists
jsonpath "$.files.excel" exists


# =====================================================
# Test 14: Reject malformed JSON
# =====================================================
# Verifies that malformed JSON is rejected

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
    "extra_invalid_field": This is malformed
  }
}

[Asserts]
status == 400


# =====================================================
# Test 15: Accept CV with optional phone field
# =====================================================
# Verifies that optional fields like phone are handled

POST {{@base_url}}{{@generate_docx_endpoint}}

[Header]
Content-Type: {{@json_content_type}}

{
  "data": {
    "profile": {
      "name": "Test User",
      "title": "Test Title",
      "email": "test@email.com",
      "phone": "+57 320 123 4567",
      "location": "Bogotá, Colombia",
      "bio": "Professional profile",
      "github": "https://github.com/user",
      "linkedin": "https://linkedin.com/in/user",
      "portfolio": "https://portfolio.dev"
    }
  }
}

[Asserts]
status == 200
header "Content-Type" contains "wordprocessingml"
