# 📍 Documentation Moved

All End-to-End testing documentation has been reorganized for better project structure.

## 📚 Development Documentation

For developers working on testing infrastructure:

- **[E2E Testing Guide](./../.dev-docs/guides/E2E_TESTING_GUIDE.md)** - Complete guide for E2E testing
  - Playwright configuration and examples
  - Hurl syntax and API testing
  - CI/CD integration
  - Troubleshooting

- **[E2E Architecture](./../.dev-docs/architecture/E2E_STRUCTURE.md)** - Project structure and organization
  - Directory structure explanation
  - Test categorization (Unit vs E2E)
  - Configuration details
  - Workflow integration

- **[Implementation Summary](./../.dev-docs/guides/E2E_IMPLEMENTATION_SUMMARY.md)** - Overview of what was implemented
  - Test coverage details
  - Architecture decisions
  - CI/CD integration
  - Best practices applied

## 📖 Project Documentation

For stakeholders and general overview:

- **[E2E Testing](./../docs/E2E_TESTING.md)** - High-level overview for non-developers
  - Testing frameworks overview
  - Test categories
  - Running tests
  - Quality metrics

## 🏗️ Test Files

Actual test implementations:

- **Frontend E2E**: `apps/web/tests/e2e/` - Playwright tests (56 tests)
  - [Web E2E README](../apps/web/tests/e2e/README.md)

- **Backend E2E**: `apps/api/tests/e2e/` - Hurl tests (26 tests)
  - [API E2E README](../apps/api/tests/e2e/README.md)

---

**This folder now serves as a navigation hub only.**  
**All development documentation is in `.dev-docs/`**  
**All project documentation is in `docs/`**
