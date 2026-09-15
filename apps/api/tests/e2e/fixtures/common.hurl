# Shared variables and fixtures for all API E2E tests
# This file is included by all test files to provide common data and configuration
# Purpose: Ensure CV synchronization across Web, PDF, and Word formats

# ============================================
# Base Configuration
# ============================================

# Base URL - cambiar según ambiente
@base_url=http://localhost:8000

# API Endpoints
@health_endpoint=/health
@root_endpoint=/
@docs_endpoint=/docs
@openapi_endpoint=/api/docs/openapi.json

# Document generation endpoints
@generate_pdf_endpoint=/api/generate/pdf
@generate_docx_endpoint=/api/generate/docx
@generate_excel_endpoint=/api/generate/excel
@generate_all_endpoint=/api/generate/all

# Sync verification endpoint
@sync_verify_endpoint=/api/sync/verify

# ============================================
# Timeouts (milliseconds)
# ============================================

@timeout_quick=2000
@timeout_medium=5000
@timeout_long=10000

# ============================================
# Content-Type Headers
# ============================================

@json_content_type=application/json
@content_type_pdf=application/pdf
@content_type_docx=application/vnd.openxmlformats-officedocument.wordprocessingml.document
@content_type_xlsx=application/vnd.openxmlformats-officedocument.spreadsheetml.sheet

# ============================================
# Test Data - Complete CV Data for Sync Testing
# ============================================
# This represents the single source of truth for CV data
# When updated, should sync to Web, PDF, and Word formats

@valid_cv_data={
  "profile": {
    "name": "Andrés Rodríguez Pisa",
    "title": "SDET Senior | QA Automation Engineer",
    "email": "test@email.com",
    "phone": "(+57) 320 324 5988",
    "location": "Bogotá, Colombia",
    "bio": "Experienced SDET Senior with 8+ years in software testing and automation.",
    "github": "https://github.com/Harp-Andres",
    "linkedin": "https://linkedin.com/in/harp-andres",
    "portfolio": "https://Harp-Andres.github.io/MiPortafolio/"
  },
  "skills": [
    {
      "category": "Web Automation",
      "skills": [
        {"name": "Playwright", "level": "expert"},
        {"name": "Selenium", "level": "expert"}
      ]
    },
    {
      "category": "API & Backend",
      "skills": [
        {"name": "REST APIs", "level": "expert"}
      ]
    }
  ],
  "experience": [
    {
      "company": "TechCorp",
      "position": "SDET Senior",
      "startDate": "2020-01",
      "endDate": "present",
      "description": "Leading QA automation initiatives"
    }
  ],
  "education": [
    {
      "institution": "University",
      "degree": "Bachelor's",
      "field": "Computer Science",
      "year": 2018
    }
  ]
}

# ============================================
# Test Data - Updated CV (for sync validation)
# ============================================

@updated_cv_data={
  "profile": {
    "name": "Andrés Rodríguez Pisa",
    "title": "SDET Senior | QA Automation Engineer - UPDATED",
    "email": "updated@email.com",
    "phone": "(+57) 320 324 5988",
    "location": "Bogotá, Colombia",
    "bio": "UPDATED: Experienced SDET Senior with 10+ years in software testing.",
    "github": "https://github.com/Harp-Andres",
    "linkedin": "https://linkedin.com/in/harp-andres",
    "portfolio": "https://Harp-Andres.github.io/MiPortafolio/"
  },
  "skills": [
    {
      "category": "Web Automation",
      "skills": [
        {"name": "Playwright", "level": "expert"},
        {"name": "Selenium", "level": "expert"},
        {"name": "Cypress", "level": "advanced"}
      ]
    }
  ]
}

# ============================================
# Test Data - Minimal CV Data
# ============================================

@minimal_cv_data={
  "profile": {
    "name": "Test User",
    "title": "Test Title",
    "email": "test@test.com"
  }
}

# ============================================
# Test Data - Invalid Data
# ============================================

@invalid_format={
  "format": "invalid"
}

@missing_format={}

@empty_request=

# ============================================
# Response Validation Templates
# ============================================

# Success response pattern
# [Asserts]
# status == 200
# header "content-type" contains "application/json"

# Error response pattern
# [Asserts]
# status >= 400
# body contains "error"
# jsonpath "$.message" exists

# ============================================
# Environment-specific values
# ============================================

# Development
# @dev_url=http://localhost:8000

# Staging
# @staging_url=https://staging-api.mportafolio.dev

# Production
# @prod_url=https://api.mportafolio.dev
