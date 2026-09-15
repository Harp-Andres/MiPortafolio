# 🧪 E2E Tests Structure - MiPortafolio

## 📂 Directory Structure

```
MiPortafolio/
├── apps/
│   ├── web/
│   │   ├── src/
│   │   │   ├── components/
│   │   │   │   ├── Skills.tsx
│   │   │   │   └── __tests__/           ← Unit tests (Vitest)
│   │   │   │       └── Skills.test.tsx
│   │   │   ├── utils/
│   │   │   │   └── cv-data.test.ts      ← Unit tests (Vitest)
│   │   │   └── hooks/
│   │   │       └── useNavigation.test.ts ← Unit tests (Vitest)
│   │   │
│   │   ├── tests/
│   │   │   └── e2e/                     ← E2E Tests (Playwright)
│   │   │       ├── 01-navigation.spec.ts
│   │   │       ├── 02-cv-download.spec.ts
│   │   │       ├── 03-responsiveness.spec.ts
│   │   │       ├── 04-accessibility.spec.ts
│   │   │       └── fixtures/
│   │   │           └── test-data.ts
│   │   │
│   │   ├── playwright.config.ts         ← E2E configuration
│   │   ├── vitest.config.ts             ← Unit test configuration
│   │   └── package.json
│   │
│   ├── api/
│   │   ├── src/
│   │   │   ├── mportafolio_backend/
│   │   │   │   └── __tests__/           ← Unit tests (pytest)
│   │   │   │       └── test_generators.py
│   │   │   │
│   │   ├── tests/
│   │   │   ├── test_generators.py       ← Existing unit tests
│   │   │   │
│   │   │   └── e2e/                     ← E2E Tests (Hurl)
│   │   │       ├── 01-health.hurl
│   │   │       ├── 02-cv-generation.hurl
│   │   │       ├── 03-cv-data.hurl
│   │   │       ├── 04-error-handling.hurl
│   │   │       └── fixtures/
│   │   │           └── common.hurl
│   │   │
│   │   └── pyproject.toml
│   │
│   └── README.md
│
├── tests/
│   └── E2E_TESTING_GUIDE.md             ← Complete E2E guide
│
└── README.md
```

## 🎯 Test Categorization

### Unit Tests (junto al código)
- **Purpose**: Test individual functions/components in isolation
- **Framework**: Vitest (Web), pytest (API)
- **Location**: `src/__tests__/` or co-located with source
- **Files**: `*.test.ts`, `*.test.tsx`, `test_*.py`
- **Run**: `pnpm test` or `pytest`

### E2E Tests (en carpeta `tests/e2e/`)
- **Purpose**: Test complete workflows end-to-end
- **Framework**: Playwright (Web), Hurl (API)
- **Location**: `tests/e2e/`
- **Files**: `*.spec.ts` (Playwright), `*.hurl` (Hurl)
- **Run**: `pnpm test:e2e` or `hurl --test`

---

## 🚀 Quick Start

### Web E2E Tests (Playwright)

```bash
# Navigate to web app
cd apps/web

# Install dependencies (if needed)
pnpm install

# Run all E2E tests
pnpm test:e2e

# Run with UI (visual test runner)
pnpm test:e2e:ui

# Run specific test
pnpm test:e2e -- 01-navigation.spec.ts

# Generate report
pnpm test:e2e
# View: playwright-report/index.html
```

### API E2E Tests (Hurl)

```bash
# Install Hurl (one-time setup)
# Windows: cargo install hurl
# macOS: brew install hurl

# Navigate to API
cd apps/api

# Start API server
python run.py

# In another terminal, run tests
hurl --test tests/e2e/*.hurl

# Run specific test
hurl --test tests/e2e/02-cv-generation.hurl

# Generate HTML report
hurl --test --html report.html tests/e2e/*.hurl
```

---

## 📋 Test Files Description

### apps/web/tests/e2e/

| File | Purpose | Coverage |
|------|---------|----------|
| `01-navigation.spec.ts` | Navigation and routing | 8 tests |
| `02-cv-download.spec.ts` | CV download functionality | 9 tests |
| `03-responsiveness.spec.ts` | Responsive design (Mobile/Tablet/Desktop) | 9 tests |
| `04-accessibility.spec.ts` | WCAG 2.1 accessibility compliance | 12 tests |
| **Total** | **Web E2E Tests** | **38 tests** |

### apps/api/tests/e2e/

| File | Purpose | Coverage |
|------|---------|----------|
| `01-health.hurl` | API health and documentation endpoints | 4 tests |
| `02-cv-generation.hurl` | CV generation (PDF, DOCX, Excel) | 7 tests |
| `03-cv-data.hurl` | CV data CRUD operations | 7 tests |
| `04-error-handling.hurl` | Error responses and edge cases | 8 tests |
| **Total** | **API E2E Tests** | **26 tests** |

---

## ⚙️ Configuration Files

### apps/web/playwright.config.ts
```typescript
{
  testDir: './tests/e2e',
  fullyParallel: true,
  retries: 2,
  workers: undefined,
  reporter: ['html', 'json', 'junit', 'list'],
  use: {
    baseURL: 'http://localhost:5173',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure'
  },
  projects: [
    { name: 'chromium', ... },
    { name: 'firefox', ... },
    { name: 'webkit', ... }
  ]
}
```

### apps/web/vitest.config.ts
Exclude pattern keeps E2E tests separate:
```typescript
exclude: [
  'node_modules/',
  'dist/',
  'tests/e2e/**',      // ← Exclude E2E
  '**/*.spec.ts'       // ← Exclude Playwright
]
```

### apps/api/tests/e2e/fixtures/common.hurl
Contains shared variables for all API tests:
- `@base_url`: API base URL
- `@timeout_*`: Timeout values
- `@valid_*`: Valid test data
- `@invalid_*`: Invalid test data

---

## 🔄 Workflow Integration

### Local Development
```bash
# Run unit tests continuously
pnpm --filter @mportafolio/web test --watch
pnpm --filter @mportafolio/api pytest --watch

# Run E2E tests before commit
pnpm --filter @mportafolio/web test:e2e
hurl --test apps/api/tests/e2e/*.hurl
```

### CI/CD Pipeline (.github/workflows/deploy.yml)
```yaml
- name: Run Playwright E2E Tests
  run: pnpm --filter @mportafolio/web test:e2e

- name: Run Hurl API E2E Tests
  run: hurl --test apps/api/tests/e2e/*.hurl

- name: Upload Test Reports
  if: always()
  uses: actions/upload-artifact@v3
  with:
    name: playwright-report
    path: apps/web/playwright-report/
```

---

## 🛡️ Best Practices Applied

### ✅ Separation of Concerns
- **Unit tests**: Test business logic, stay close to code
- **E2E tests**: Test complete workflows, in separate folder
- **No mixing**: E2E config excludes unit tests, vice versa

### ✅ Framework Choice
- **Playwright**: Industry standard for Web E2E (fast, reliable)
- **Hurl**: Modern API testing (2026 best practice, DSL-based)

### ✅ Organization
- **Unit tests**: Co-located with source (`src/__tests__/`)
- **E2E tests**: Centralized (`tests/e2e/`)
- **Fixtures**: Shared data in `fixtures/` folder

### ✅ Scalability
- **Multiple projects**: Each app has own test suite
- **Independent runs**: Web tests don't require API, vice versa
- **Parallel execution**: Tests can run in parallel

### ✅ Maintainability
- **Clear naming**: `01-*`, `02-*`, etc. for execution order
- **Documentation**: Comprehensive guide in `E2E_TESTING_GUIDE.md`
- **Fixtures**: Reusable test data and selectors
- **Comments**: Each test file has detailed descriptions

---

## 🚦 Test Execution Order (CI/CD)

```
┌─────────────────────────────────────────┐
│  1. Unit Tests (Fast)                   │
│     ├── pnpm test (Web)                 │
│     └── pytest (API)                    │
├─────────────────────────────────────────┤
│  2. E2E Tests (Medium)                  │
│     ├── pnpm test:e2e (Web)             │
│     └── hurl --test (API)               │
├─────────────────────────────────────────┤
│  3. Build & Deploy (Slow)               │
│     ├── pnpm build (Web)                │
│     └── GitHub Pages deployment         │
└─────────────────────────────────────────┘
```

---

## 📊 Test Coverage Goals

| Layer | Framework | Coverage Goal | Current |
|-------|-----------|----------------|---------|
| **Unit** | Vitest | 80%+ | TBD |
| **Unit** | pytest | 75%+ | TBD |
| **E2E Web** | Playwright | 100% happy path | 38 tests |
| **E2E API** | Hurl | 100% endpoints | 26 tests |

---

## 🔗 Related Documentation

- [E2E Testing Guide](./E2E_TESTING_GUIDE.md) - Complete guide with examples
- [Architecture Guide](./docs/MONOREPO_ARCHITECTURE.md) - Monorepo structure
- [Contributing Guide](./docs/CONTRIBUTING.md) - Development workflow

---

**Last Updated**: 2026-09-14  
**Version**: 1.0.0  
**Status**: ✅ Ready for use
