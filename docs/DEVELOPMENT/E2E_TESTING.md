# 🧪 End-to-End Testing

## Overview

MiPortafolio has a comprehensive End-to-End (E2E) testing suite that validates both frontend and backend functionality using modern testing frameworks.

## Testing Frameworks

### Frontend E2E Testing with Playwright
- **Framework**: Playwright 1.63.0
- **Location**: `apps/web/tests/e2e/`
- **Coverage**: 56 tests
- **Features**:
  - Multi-browser testing (Chrome, Firefox, Safari)
  - Responsive design validation
  - WCAG 2.1 accessibility compliance
  - Automatic screenshots and video recordings

### Backend E2E Testing with Hurl
- **Framework**: Hurl (modern API testing tool)
- **Location**: `apps/api/tests/e2e/`
- **Coverage**: 26 tests
- **Features**:
  - DSL-based API testing
  - Performance assertions
  - Multi-environment support
  - HTML and JSON reporting

## Test Categories

### Web E2E Tests
1. **Navigation** (8 tests) - Route validation and section navigation
2. **CV Downloads** (9 tests) - PDF/DOCX generation and download
3. **Responsiveness** (27 tests) - Mobile, tablet, desktop layouts
4. **Accessibility** (12 tests) - WCAG 2.1 compliance

### API E2E Tests
1. **Health Checks** (4 tests) - API availability and documentation
2. **CV Generation** (7 tests) - All document formats
3. **Data Management** (7 tests) - CRUD operations
4. **Error Handling** (8 tests) - Error responses and edge cases

## Running Tests

### Frontend Tests
```bash
pnpm --filter @mportafolio/web test:e2e
```

### Backend Tests
```bash
hurl --test apps/api/tests/e2e/*.hurl
```

## Documentation

For complete setup instructions, best practices, and troubleshooting:
- **Detailed Guide**: See `.dev-docs/guides/E2E_TESTING_GUIDE.md`
- **Architecture**: See `.dev-docs/architecture/E2E_STRUCTURE.md`
- **Implementation Details**: See `.dev-docs/guides/E2E_IMPLEMENTATION_SUMMARY.md`
- **Web Tests**: See `apps/web/tests/e2e/README.md`
- **API Tests**: See `apps/api/tests/e2e/README.md`

## CI/CD Integration

E2E tests run automatically in GitHub Actions as part of the deployment pipeline. Test reports are uploaded as artifacts for review.

## Quality Metrics

| Layer | Tests | Framework | Coverage |
|-------|-------|-----------|----------|
| Web E2E | 56 | Playwright | 100% happy path |
| API E2E | 26 | Hurl | 100% endpoints |
| **Total** | **82** | | **Complete** |

---

**Last Updated**: 2026-09-14  
**Status**: ✅ Production Ready
