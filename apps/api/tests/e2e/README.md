# 🧪 API E2E Tests with Hurl

## 📋 Overview

This directory contains end-to-end tests for the MiPortafolio Backend API using [Hurl](https://hurl.dev), a modern CLI tool for testing HTTP APIs.

**Business Focus**: These tests verify that CV data synchronizes correctly across Web, PDF, and Word formats (single source of truth).

## 🎯 Test Categories

### 01-cv-sync.hurl (12 tests)
**Purpose**: Verify CV synchronization across all formats

Tests that when CV data is updated, all generated documents (PDF, DOCX, Excel) contain the same information:
- Generate PDF, DOCX, Excel from same CV data
- Generate all formats simultaneously
- Verify sync with profile name and email
- Test updated CV data sync
- Verify sync report endpoint
- Performance testing with large CV data

**Key Objective**: Ensure Web, PDF, and Word CV are always in sync

### 02-document-generation.hurl (15 tests)
**Purpose**: Verify documents are generated correctly

Tests that documents are properly created with correct format and content:
- PDF generation with complete and minimal CV
- DOCX generation with complete and minimal CV
- Excel generation with complete and minimal CV
- Verify document filenames follow expected format
- Test performance (documents generated within acceptable time)
- Verify content handling (special characters, accents)

**Key Objective**: Reliable document generation in all formats

### 03-data-validation.hurl (15 tests)
**Purpose**: Verify CV data validation

Tests that valid data is accepted and invalid data is rejected:
- Accept valid complete CV data
- Accept minimal valid CV data
- Reject invalid data
- Validate required fields (name, title, email)
- Test optional fields (phone, location, bio, social links)
- Verify email format validation
- Test data integrity through update cycles

**Key Objective**: Maintain data quality and consistency

### 04-error-handling.hurl (20 tests)
**Purpose**: Verify error handling and edge cases

Tests that the API handles errors gracefully:
- 404 for invalid endpoints
- 405 for invalid HTTP methods
- 400 for invalid data
- Proper error messages
- Special characters and Unicode support
- Health check and documentation endpoints

**Key Objective**: Robust error handling and reliability

---

## 🚀 Installation

### macOS

```bash
# Using Homebrew (recommended)
brew install hurl

# Or compile from source
cargo install hurl
```

### Windows

```powershell
# Using Cargo (Rust package manager)
cargo install hurl

# Or download pre-built binary from GitHub
# https://github.com/Orange-OpenSource/hurl/releases
# Then add to PATH
```

### Linux (Ubuntu/Debian)

```bash
# Using package manager
sudo apt-get install hurl

# Or using Cargo
cargo install hurl
```

### Docker

```bash
docker run -v $PWD:$PWD -w $PWD ghcr.io/orange-opensource/hurl:latest \
  --test tests/e2e/*.hurl
```

---

## 🔍 Verify Installation

```bash
# Check version
hurl --version

# Run help
hurl --help

# Test basic functionality
echo 'GET https://httpbin.org/get' | hurl
```

---

## 🎯 Quick Start

### 1. Navigate to API folder

```bash
cd apps/api
```

### 2. Start API server

```bash
# Start in one terminal
python run.py

# Or using UV (if installed)
uv run run.py
```

### 3. Run E2E tests

```bash
# Run all E2E tests
hurl --test tests/e2e/*.hurl

# Run with verbose output
hurl --test --verbose tests/e2e/*.hurl

# Generate HTML report
hurl --test --html report.html tests/e2e/*.hurl

# Run in parallel (4 workers)
hurl --test --parallel 4 tests/e2e/*.hurl

# Run specific test file
hurl --test tests/e2e/01-health.hurl
```

---

## 📝 Hurl File Structure

### Basic Test File

```hurl
# Health Check E2E Tests
# This is a comment

# 1. Basic GET request
GET http://localhost:8000/api/health

HTTP 200
[Asserts]
body contains "ok"

---

# 2. POST with JSON
POST http://localhost:8000/api/cv/generate

[Header]
Content-Type: application/json

{
  "format": "pdf"
}

HTTP 200
[Asserts]
header "content-type" contains "application/pdf"
```

### Key Concepts

**Sections** (in order):
1. **Request Line**: `GET`, `POST`, `PUT`, `DELETE`, `PATCH`
2. **Headers** (optional): `[Header]` block
3. **Body** (optional): JSON, form data, etc.
4. **Response**: `HTTP <status>` expected status
5. **Captures** (optional): `[Captures]` extract values
6. **Asserts** (optional): `[Asserts]` validate response

---

## 🔄 Advanced Features

### Variables

```hurl
# Define variables
@base_url=http://localhost:8000
@format=pdf

# Use in requests
POST {{@base_url}}/api/cv/generate

[Header]
Content-Type: application/json

{
  "format": "{{@format}}"
}
```

### Capture and Reuse

```hurl
# Capture response value
POST http://localhost:8000/api/cv/generate
...
[Captures]
response_time: header "x-response-time"
download_url: body jsonpath "$.url"

---

# Use captured value in next request
GET {{@download_url}}

HTTP 200
```

### Conditional Logic

```hurl
# Run test only on specific environment
[Env]
base_url=http://localhost:8000

GET {{@base_url}}/api/health

HTTP 200
```

### Request Options

```hurl
POST http://localhost:8000/api/upload

[Header]
Authorization: Bearer token123

# Add query parameters
?format=json&verbose=true

# Multipart form data
[MultipartFormData]
file: @/path/to/file.pdf
name: "Test File"

HTTP 200
```

---

## ✅ Assertions

### Status Code

```hurl
HTTP 200              # Exact match
HTTP 2xx              # Range match
```

### Headers

```hurl
[Asserts]
header "content-type" contains "application/json"
header "x-api-version" == "v1"
header "cache-control" exists
```

### Body

```hurl
[Asserts]
body contains "success"
body starts with "{"
body ends with "}"
```

### JSON Path

```hurl
[Asserts]
jsonpath "$.id" exists
jsonpath "$.data" isArray
jsonpath "$.name" isString
jsonpath "$.count" > 0
jsonpath "$[0].email" == "test@example.com"
```

### Response Time

```hurl
[Asserts]
response_time < "1000"     # milliseconds
response_time < "5s"       # seconds
header "x-response-time" < "3000"
```

---

## 🏃 Running Tests

### All Tests

```bash
hurl --test tests/e2e/*.hurl
```

### Specific Test

```bash
hurl --test tests/e2e/02-cv-generation.hurl
```

### Dry Run (No execution)

```bash
hurl --dry-run tests/e2e/01-health.hurl
```

### Verbose Output

```bash
hurl --test --verbose tests/e2e/*.hurl
```

### With Report

```bash
hurl --test --html report.html tests/e2e/*.hurl
# Open report.html in browser
```

### Parallel Execution

```bash
# Run 4 tests in parallel
hurl --test --parallel 4 tests/e2e/*.hurl

# Run 8 tests in parallel (faster)
hurl --test --parallel 8 tests/e2e/*.hurl
```

### Environment-Specific

```bash
# Override variables
hurl --variable base_url=https://staging-api.dev \
     --test tests/e2e/*.hurl

# Multiple variables
hurl --variable base_url=http://localhost:8000 \
     --variable api_key=secret123 \
     --test tests/e2e/*.hurl
```

---

## 📊 Reports

### Generate HTML Report

```bash
hurl --test --html report.html tests/e2e/*.hurl
```

### JSON Report

```bash
hurl --test --json report.json tests/e2e/*.hurl
```

### TAP Report (for CI)

```bash
hurl --test --tap report.tap tests/e2e/*.hurl
```

### Multiple Formats

```bash
hurl --test \
  --html report.html \
  --json report.json \
  tests/e2e/*.hurl
```

---

## 🔧 Configuration

### .hurl Config File (Optional)

Create `hurl.toml` in project root:

```toml
[test]
timeout = 10000
retry = 2

[report]
html = "test-reports/hurl-report.html"
json = "test-reports/hurl-results.json"

[ssl]
insecure = false
```

### Environment Variables

```bash
# Pass via environment
export BASE_URL=http://localhost:8000
export API_KEY=secret123

# Use in Hurl files
@base_url={{env.BASE_URL}}
@api_key={{env.API_KEY}}
```

---

## 🚨 Troubleshooting

### Connection Refused

```
Error: Connection refused

# Solution: Ensure API is running
python run.py

# Or check if port is correct
hurl --variable base_url=http://localhost:8000 --test tests/e2e/01-health.hurl
```

### SSL Certificate Error

```
Error: certificate verify failed

# Solution: For development only
hurl --insecure --test tests/e2e/*.hurl

# Or add to hurl file
[Options]
insecure: true
```

### Timeout Error

```
Error: Connection timeout

# Solution: Increase timeout
hurl --connect-timeout 30000 --max-time 60000 --test tests/e2e/*.hurl
```

### Parse Error

```
Error: Parse error

# Solution: Validate syntax
hurl --check tests/e2e/02-cv-generation.hurl

# Run with verbose to see issue
hurl --test --verbose tests/e2e/02-cv-generation.hurl
```

### Variable Not Found

```
Error: Variable '{{@base_url}}' not found

# Solution: Check common.hurl is included
# Or pass via command line
hurl --variable base_url=http://localhost:8000 --test tests/e2e/*.hurl
```

---

## 📚 Hurl File Examples

### Example 1: Health Check

```hurl
GET http://localhost:8000/health

HTTP 200
[Asserts]
body contains "ok"
response_time < "1000"
```

### Example 2: Create and Use

```hurl
# Create resource
POST http://localhost:8000/api/cv/generate

[Header]
Content-Type: application/json

{
  "format": "pdf"
}

HTTP 200
[Captures]
cv_id: body jsonpath "$.id"

---

# Use created resource
GET http://localhost:8000/api/cv/{{@cv_id}}

HTTP 200
[Asserts]
jsonpath "$.format" == "pdf"
```

### Example 3: Error Handling

```hurl
# Missing required field
POST http://localhost:8000/api/cv/generate

[Header]
Content-Type: application/json

{}

HTTP 400
[Asserts]
body contains "format"
body contains "required"
jsonpath "$.error.field" == "format"
```

### Example 4: Performance Testing

```hurl
POST http://localhost:8000/api/cv/generate

[Header]
Content-Type: application/json

{
  "format": "pdf"
}

HTTP 200
[Asserts]
response_time < "5000"        # Must be under 5 seconds
header "x-response-time" < "3000"  # Server response time
header "content-length" > "1000"   # File size > 1KB
```

---

## 🔗 Integration with CI/CD

### GitHub Actions

```yaml
name: API E2E Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Install Hurl
        run: |
          sudo apt-get update
          sudo apt-get install hurl
      
      - name: Start API
        run: |
          cd apps/api
          python -m pip install -r requirements.txt
          python run.py &
          sleep 5  # Wait for API to start
      
      - name: Run Hurl Tests
        run: |
          hurl --test --html report.html apps/api/tests/e2e/*.hurl
      
      - name: Upload Report
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: hurl-report
          path: report.html
```

### Local Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Running Hurl E2E tests..."
cd apps/api

# Ensure API is running
python run.py &
API_PID=$!

sleep 3

# Run tests
hurl --test tests/e2e/*.hurl
TEST_RESULT=$?

# Kill API
kill $API_PID

exit $TEST_RESULT
```

---

## 🎓 Learning Resources

- **Official Docs**: https://hurl.dev/docs
- **GitHub Repo**: https://github.com/Orange-OpenSource/hurl
- **Examples**: https://github.com/Orange-OpenSource/hurl/tree/master/docs/samples
- **Tutorial**: https://hurl.dev/docs/tutorial
- **Community**: https://github.com/Orange-OpenSource/hurl/discussions

---

## ✨ Pro Tips

1. **Use fixtures**: Define common variables in `fixtures/common.hurl`
2. **Order matters**: Tests in file execute sequentially
3. **Parallel testing**: Use `--parallel` for faster runs
4. **Capture values**: Save response data for next request
5. **Descriptive comments**: Add meaningful comments for documentation
6. **Performance baseline**: Set response time expectations early
7. **Test edge cases**: Include error scenarios in tests
8. **Version control**: Commit test files, not reports

---

**Last Updated**: 2026-09-14  
**Version**: 1.0.0
