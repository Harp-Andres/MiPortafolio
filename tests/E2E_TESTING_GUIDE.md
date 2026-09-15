# 🧪 E2E Testing Guide - MiPortafolio

## 📋 Overview

This project uses a modern approach to E2E testing with **two complementary frameworks**:

- **Playwright** for UI/Frontend E2E tests (Web applications)
- **Hurl** for API E2E tests (Backend services)

---

## 🎭 Playwright E2E Tests (Web Frontend)

### 📁 Location
```
apps/web/tests/e2e/
├── 01-navigation.spec.ts       # Navigation and routing
├── 02-cv-download.spec.ts      # CV download functionality
├── 03-responsiveness.spec.ts   # Responsive design validation
├── 04-accessibility.spec.ts    # WCAG accessibility compliance
└── fixtures/
    └── test-data.ts            # Shared test data and selectors
```

### 🚀 Running Tests

```bash
# Run all E2E tests
pnpm --filter @mportafolio/web test:e2e

# Run specific test file
pnpm --filter @mportafolio/web test:e2e -- 01-navigation.spec.ts

# Run with UI mode (visual test runner)
pnpm --filter @mportafolio/web test:e2e:ui

# Generate HTML report
pnpm --filter @mportafolio/web test:e2e
# Report will be in: apps/web/playwright-report/
```

### 📝 Test Categories

#### 1. Navigation Tests (`01-navigation.spec.ts`)
- ✅ Homepage loads successfully
- ✅ Navigate to all sections (About, Skills, Experience, etc.)
- ✅ Scroll-to-top functionality
- ✅ Link structure validation

#### 2. CV Download Tests (`02-cv-download.spec.ts`)
- ✅ Download button availability
- ✅ PDF generation and download
- ✅ DOCX generation and download
- ✅ Loading states
- ✅ Success messages

#### 3. Responsiveness Tests (`03-responsiveness.spec.ts`)
- ✅ Mobile (iPhone 12)
- ✅ Tablet (iPad)
- ✅ Desktop (1920x1080)
- ✅ Proper layout on each viewport
- ✅ Touch target sizes
- ✅ No horizontal overflow

#### 4. Accessibility Tests (`04-accessibility.spec.ts`)
- ✅ Proper heading hierarchy
- ✅ Image alt text
- ✅ Color contrast
- ✅ Keyboard navigation
- ✅ Button semantics
- ✅ Form labels
- ✅ ARIA landmarks
- ✅ Focus management

### 🎯 Best Practices

#### Use Data Test IDs
```tsx
// In components
<section data-testid="hero-section">
  <button data-testid="download-cv">Download</button>
</section>

// In tests
await page.locator('[data-testid="download-cv"]').click()
```

#### Wait for Elements Properly
```typescript
// ❌ Don't use arbitrary waits
await page.waitForTimeout(1000)

// ✅ Do use Playwright's built-in methods
await expect(element).toBeVisible()
await page.waitForLoadState('networkidle')
```

#### Use Fixtures for Common Data
```typescript
import { SECTIONS, DOWNLOAD_SELECTORS } from './fixtures/test-data'

// Use predefined selectors
await page.click(SECTIONS.ABOUT)
await page.click(DOWNLOAD_SELECTORS.PDF)
```

---

## 🔌 Hurl E2E Tests (Backend API)

### 📁 Location
```
apps/api/tests/e2e/
├── 01-health.hurl              # Health check endpoints
├── 02-cv-generation.hurl       # CV generation endpoints
├── 03-cv-data.hurl             # CV data management
├── 04-error-handling.hurl      # Error handling scenarios
└── fixtures/
    └── common.hurl             # Common variables and data
```

### 🚀 Running Tests

#### Install Hurl
```bash
# macOS
brew install hurl

# Windows (using Cargo)
cargo install hurl

# Or download from: https://hurl.dev
```

#### Run Tests
```bash
# Run all API E2E tests
hurl --test apps/api/tests/e2e/*.hurl

# Run specific test file
hurl --test apps/api/tests/e2e/02-cv-generation.hurl

# Run with verbose output
hurl --test --verbose apps/api/tests/e2e/*.hurl

# Generate HTML report
hurl --test --html report.html apps/api/tests/e2e/*.hurl

# Run against specific environment
hurl --variable base_url=https://staging-api.dev --test apps/api/tests/e2e/*.hurl

# Run with multiple workers
hurl --test --parallel 4 apps/api/tests/e2e/*.hurl
```

### 📝 Hurl Syntax Guide

#### Basic GET Request
```hurl
GET http://localhost:8000/api/cv/data

HTTP 200
[Asserts]
header "content-type" contains "application/json"
body contains "personalInfo"
```

#### POST with JSON
```hurl
POST http://localhost:8000/api/cv/generate

[Header]
Content-Type: application/json

{
  "format": "pdf",
  "language": "es"
}

HTTP 200
[Asserts]
header "content-type" contains "application/pdf"
header "content-length" > 0
```

#### Capture Values for Reuse
```hurl
[Captures]
response_time: header "x-response-time"
cv_id: body jsonpath "$.id"
```

#### Use Variables
```hurl
@base_url=http://localhost:8000
@format=pdf

POST {{@base_url}}/api/cv/generate

[Header]
Content-Type: application/json

{
  "format": "{{@format}}"
}
```

#### Assertions
```hurl
[Asserts]
status == 200                                    # Status code
header "content-type" contains "application/json"  # Header contains
body contains "success"                          # Body contains
jsonpath "$.id" exists                          # JSON path exists
jsonpath "$.data" isArray                       # Is array
jsonpath "$[0].name" isString                   # Is string
response_time < "1000"                          # Response time < 1s
```

### 📝 Test Categories

#### 1. Health Checks (`01-health.hurl`)
- ✅ API health endpoint
- ✅ Root endpoint
- ✅ Swagger documentation
- ✅ OpenAPI schema

#### 2. CV Generation (`02-cv-generation.hurl`)
- ✅ Generate PDF CV
- ✅ Generate DOCX CV
- ✅ Generate Excel CV
- ✅ Invalid format handling
- ✅ Performance validation (< 5s)
- ✅ Multi-language support

#### 3. CV Data Management (`03-cv-data.hurl`)
- ✅ Get CV data
- ✅ Validate data structure
- ✅ Get specific sections (Experience, Skills, Education)
- ✅ Update CV data
- ✅ Validate data integrity

#### 4. Error Handling (`04-error-handling.hurl`)
- ✅ 404 Not Found
- ✅ 405 Method Not Allowed
- ✅ 400 Bad Request
- ✅ Invalid JSON
- ✅ Missing required fields
- ✅ Error response structure

### 🎯 Best Practices

#### Use Variables for Reusability
```hurl
@base_url=http://localhost:8000
@cv_format_pdf=pdf
@cv_format_docx=docx

# Use in requests
POST {{@base_url}}/api/cv/generate
```

#### Capture and Reuse Responses
```hurl
# Capture from first request
[Captures]
auth_token: body jsonpath "$.token"

# Use in subsequent requests
[Header]
Authorization: Bearer {{auth_token}}
```

#### Validate Performance
```hurl
[Asserts]
response_time < "5000"  # Must respond in < 5 seconds
header "x-response-time" < "3000"
```

#### Test Error Cases
```hurl
POST http://localhost:8000/api/cv/generate

[Header]
Content-Type: application/json

{}  # Missing required format field

HTTP 400
[Asserts]
body contains "format"
body contains "required"
```

---

## 🔄 CI/CD Integration

### GitHub Actions

The project includes automated E2E testing in CI/CD:

```yaml
# See .github/workflows/deploy.yml

- name: Install Playwright browsers
  run: npx playwright install --with-deps

- name: Run Playwright E2E tests
  run: pnpm --filter @mportafolio/web test:e2e

- name: Run Hurl API E2E tests
  run: hurl --test apps/api/tests/e2e/*.hurl
```

### Local Testing Before Commit

```bash
# Test everything before pushing
pnpm --filter @mportafolio/web test:e2e
hurl --test apps/api/tests/e2e/*.hurl

# If all pass, safe to commit
git add .
git commit -m "feat: add feature with E2E coverage"
```

---

## 🛠️ Troubleshooting

### Playwright Issues

#### Tests timeout
```bash
# Increase timeout in playwright.config.ts
test: {
  timeout: 30000  // 30 seconds
}
```

#### Browser not found
```bash
# Install Playwright browsers
npx playwright install
```

#### Port already in use
```bash
# Kill the process using port 5173
# macOS/Linux
lsof -ti:5173 | xargs kill -9

# Windows
netstat -ano | findstr :5173
taskkill /PID <PID> /F
```

### Hurl Issues

#### API not responding
```bash
# Check if API is running
curl http://localhost:8000/health

# Start API if needed
cd apps/api
python run.py
```

#### Variable not found
```bash
# Ensure variables are defined in common.hurl
# Or pass via command line
hurl --variable base_url=http://localhost:8000 --test 01-health.hurl
```

#### Parse errors
```bash
# Validate Hurl syntax
hurl --check 02-cv-generation.hurl

# Run with verbose output
hurl --test --verbose 02-cv-generation.hurl
```

---

## 📊 Test Coverage

### Frontend (Playwright)
- **Navigation**: 100% of main sections
- **Downloads**: PDF, DOCX formats
- **Responsiveness**: 3 viewports (Mobile, Tablet, Desktop)
- **Accessibility**: WCAG 2.1 Level AA
- **Current Coverage**: ~30+ test cases

### Backend (Hurl)
- **Health Checks**: API availability
- **CV Generation**: All formats
- **Data Management**: CRUD operations
- **Error Handling**: 400, 404, 405 status codes
- **Performance**: Response time validation
- **Current Coverage**: ~20+ test cases

---

## 📚 References

### Playwright
- [Official Documentation](https://playwright.dev)
- [Best Practices](https://playwright.dev/docs/best-practices)
- [API Reference](https://playwright.dev/docs/api/class-page)

### Hurl
- [Official Website](https://hurl.dev)
- [Documentation](https://hurl.dev/docs/tutorial)
- [GitHub Repository](https://github.com/Orange-OpenSource/hurl)

---

## 🚀 Next Steps

1. **Add data-testid attributes** to all interactive components
2. **Expand Playwright tests** with more complex scenarios
3. **Create API contract tests** using Hurl
4. **Set up performance monitoring** in CI/CD
5. **Add visual regression tests** with Playwright
6. **Create test reporting dashboard** in GitHub Actions

---

**Last Updated**: 2026-09-14  
**Maintained By**: Portfolio QA Team
