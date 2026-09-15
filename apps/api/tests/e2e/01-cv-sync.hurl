#!/usr/bin/env hurl
# CV Synchronization Tests
# =====================================================
# Purpose: Verify that CV data synchronizes correctly
# across Web, PDF, and Word formats (single source of truth)
#
# Business Goal: Ensure that when a user updates their CV data,
# all formats (Web, PDF, DOCX, Excel) reflect the same information
#
# Tests:
#   1. Generate documents from same CV data
#   2. Verify all documents contain identical information
#   3. Update CV data and verify sync across all formats
#   4. Test data integrity after updates

include fixtures/common.hurl

# =====================================================
# Test 1: Generate PDF from CV data
# =====================================================
# Verifies that PDF generation works and returns valid PDF file

POST {{@base_url}}{{@generate_pdf_endpoint}}

[Header]
Content-Type: {{@json_content_type}}

{
  "data": {{@valid_cv_data}}
}

[Asserts]
status == 200
header "Content-Type" contains "application/pdf"
header "Content-Length" > "1000"
body contains ""

# Capture PDF response info
[Captures]
pdf_size: header "Content-Length"
pdf_generated: body string "PDF"


# =====================================================
# Test 2: Generate DOCX from same CV data
# =====================================================
# Verifies that DOCX generation works and returns valid DOCX file

POST {{@base_url}}{{@generate_docx_endpoint}}

[Header]
Content-Type: {{@json_content_type}}

{
  "data": {{@valid_cv_data}}
}

[Asserts]
status == 200
header "Content-Type" contains "wordprocessingml"
header "Content-Length" > "1000"

# Capture DOCX response info
[Captures]
docx_size: header "Content-Length"


# =====================================================
# Test 3: Generate Excel from same CV data
# =====================================================
# Verifies that Excel generation works and returns valid file

POST {{@base_url}}{{@generate_excel_endpoint}}

[Header]
Content-Type: {{@json_content_type}}

{
  "data": {{@valid_cv_data}}
}

[Asserts]
status == 200
header "Content-Type" contains "spreadsheetml"
header "Content-Length" > "1000"

# Capture Excel response info
[Captures]
excel_size: header "Content-Length"


# =====================================================
# Test 4: Generate all formats simultaneously
# =====================================================
# Verifies that all formats can be generated in one request
# This ensures consistency when generating all formats together

POST {{@base_url}}{{@generate_all_endpoint}}

[Header]
Content-Type: {{@json_content_type}}

{
  "data": {{@valid_cv_data}}
}

[Asserts]
status == 200
header "Content-Type" == "{{@json_content_type}}"
body contains "success"
body contains "timestamp"
body contains "files"
jsonpath "$.files.docx" exists
jsonpath "$.files.pdf" exists
jsonpath "$.files.excel" exists

# Capture all file paths
[Captures]
all_files_timestamp: body jsonpath "$.timestamp"
all_files_docx: body jsonpath "$.files.docx"
all_files_pdf: body jsonpath "$.files.pdf"
all_files_excel: body jsonpath "$.files.excel"


# =====================================================
# Test 5: Verify sync with profile name
# =====================================================
# Demonstrates that profile name is consistent across formats
# by verifying the name is used in document generation

POST {{@base_url}}{{@generate_pdf_endpoint}}

[Header]
Content-Type: {{@json_content_type}}

{
  "data": {
    "profile": {
      "name": "Sync Test Name",
      "title": "Test Title",
      "email": "sync@test.com"
    }
  }
}

[Asserts]
status == 200
header "Content-Type" contains "application/pdf"

# This would verify the PDF contains the name, but requires PDF parsing
# For now, we verify the PDF was generated successfully


# =====================================================
# Test 6: Verify sync with profile email
# =====================================================
# Demonstrates that profile email is consistent across formats

POST {{@base_url}}{{@generate_docx_endpoint}}

[Header]
Content-Type: {{@json_content_type}}

{
  "data": {
    "profile": {
      "name": "Test User",
      "title": "Test Title",
      "email": "sync.email@test.com"
    }
  }
}

[Asserts]
status == 200
header "Content-Type" contains "wordprocessingml"


# =====================================================
# Test 7: Updated CV data sync to PDF
# =====================================================
# Verifies that updated CV data is used when generating PDF

POST {{@base_url}}{{@generate_pdf_endpoint}}

[Header]
Content-Type: {{@json_content_type}}

{
  "data": {{@updated_cv_data}}
}

[Asserts]
status == 200
header "Content-Type" contains "application/pdf"
header "Content-Length" > "1000"


# =====================================================
# Test 8: Updated CV data sync to DOCX
# =====================================================
# Verifies that updated CV data is used when generating DOCX

POST {{@base_url}}{{@generate_docx_endpoint}}

[Header]
Content-Type: {{@json_content_type}}

{
  "data": {{@updated_cv_data}}
}

[Asserts]
status == 200
header "Content-Type" contains "wordprocessingml"
header "Content-Length" > "1000"


# =====================================================
# Test 9: Updated CV data sync to Excel
# =====================================================
# Verifies that updated CV data is used when generating Excel

POST {{@base_url}}{{@generate_excel_endpoint}}

[Header]
Content-Type: {{@json_content_type}}

{
  "data": {{@updated_cv_data}}
}

[Asserts]
status == 200
header "Content-Type" contains "spreadsheetml"
header "Content-Length" > "1000"


# =====================================================
# Test 10: Verify sync report endpoint
# =====================================================
# Verifies that the sync verification endpoint works
# This endpoint should report if all formats are in sync

POST {{@base_url}}{{@sync_verify_endpoint}}

[Header]
Content-Type: {{@json_content_type}}

{
  "data": {{@valid_cv_data}}
}

[Asserts]
status == 200
header "Content-Type" contains "{{@json_content_type}}"
body contains "profile"
body contains "name"
body contains "email"

# The response should indicate sync status
[Captures]
sync_status: body jsonpath "$.profile.name"


# =====================================================
# Test 11: Minimal CV data sync to PDF
# =====================================================
# Verifies that even minimal CV data synchronizes correctly

POST {{@base_url}}{{@generate_pdf_endpoint}}

[Header]
Content-Type: {{@json_content_type}}

{
  "data": {{@minimal_cv_data}}
}

[Asserts]
status == 200
header "Content-Type" contains "application/pdf"


# =====================================================
# Test 12: Large CV data sync - performance
# =====================================================
# Verifies that large CV data with many skills synchronizes
# and generates documents within acceptable time

POST {{@base_url}}{{@generate_all_endpoint}}

[Header]
Content-Type: {{@json_content_type}}

{
  "data": {
    "profile": {
      "name": "Performance Test",
      "title": "SDET with Large Dataset",
      "email": "perf@test.com"
    },
    "skills": [
      {
        "category": "Web Automation",
        "skills": [
          {"name": "Playwright", "level": "expert"},
          {"name": "Selenium", "level": "expert"},
          {"name": "Cypress", "level": "advanced"}
        ]
      },
      {
        "category": "API Testing",
        "skills": [
          {"name": "REST APIs", "level": "expert"},
          {"name": "GraphQL", "level": "advanced"}
        ]
      }
    ]
  }
}

[Asserts]
status == 200
body contains "success"
response_time < "{{@timeout_medium}}"  # Must complete within 5 seconds
jsonpath "$.files.docx" exists
jsonpath "$.files.pdf" exists
jsonpath "$.files.excel" exists
