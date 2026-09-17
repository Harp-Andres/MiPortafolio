# 🧪 Playwright E2E Tests - Web Frontend

## 📁 Structure

```
apps/web/tests/e2e/
├── 01-navigation.spec.ts       # Navigation and routing tests
├── 02-cv-download.spec.ts      # CV download functionality
├── 03-responsiveness.spec.ts   # Responsive design validation
├── 04-accessibility.spec.ts    # WCAG accessibility compliance
└── fixtures/
    └── test-data.ts            # Shared test data and selectors
```

---

## 🚀 Running Tests

### Install Dependencies

```bash
# From project root
pnpm install

# Or from apps/web
cd apps/web
pnpm install
```

### Run All E2E Tests

```bash
# From project root
pnpm --filter @mportafolio/web test:e2e

# From apps/web
cd apps/web
pnpm test:e2e
```

### Run Tests in UI Mode

Visual test runner with live browser:

```bash
pnpm --filter @mportafolio/web test:e2e:ui
```

### Run Specific Test File

```bash
pnpm --filter @mportafolio/web test:e2e -- 01-navigation.spec.ts
```

### Run Specific Test

```bash
pnpm --filter @mportafolio/web test:e2e -- 01-navigation.spec.ts -g "should load"
```

### Run with Debug

```bash
# Headed mode (show browser)
npx playwright test --headed

# Debug mode (step-by-step)
npx playwright test --debug

# Pause on failure
npx playwright test --pause-on-failure
```

---

## 📊 Test Categories

### 01-navigation.spec.ts (8 tests)
✅ Homepage loads successfully  
✅ Navigate to About section  
✅ Navigate to Skills section  
✅ Navigate to Experience section  
✅ Navigate to Projects section  
✅ Navigate to Education section  
✅ Navigate to Certificates section  
✅ Scroll to top functionality  
✅ Proper navigation links structure  

```bash
pnpm test:e2e -- 01-navigation.spec.ts
```

### 02-cv-download.spec.ts (9 tests)
✅ Download CV button exists  
✅ Download PDF successfully  
✅ Download DOCX successfully  
✅ Show loading state  
✅ Multiple format options  
✅ Download success message  
✅ Maintain download history  
✅ Button in hero section  
✅ Button in about section  

```bash
pnpm test:e2e -- 02-cv-download.spec.ts
```

### 03-responsiveness.spec.ts (9 tests per viewport = 27 total)
Tests for **3 viewports**: Mobile, Tablet, Desktop

✅ Hero section renders correctly  
✅ Navigation renders correctly  
✅ Skills section with proper layout  
✅ Projects with proper card layout  
✅ Experience section accessible  
✅ Maintain proper font sizes  
✅ Touch targets (mobile)  
✅ No horizontal overflow  
✅ Footer renders correctly  

```bash
pnpm test:e2e -- 03-responsiveness.spec.ts
```

### 04-accessibility.spec.ts (12 tests)
✅ Proper heading hierarchy  
✅ Image alt text  
✅ Color contrast  
✅ Keyboard navigation  
✅ Button semantics  
✅ Link semantics  
✅ Keyboard shortcuts  
✅ Form labels  
✅ Announce dynamic updates  
✅ Focus visible styles  
✅ No keyboard traps  
✅ ARIA landmarks  

```bash
pnpm test:e2e -- 04-accessibility.spec.ts
```

---

## 📝 Test Data & Fixtures

### Using Test Data

```typescript
import {
  SECTIONS,
  DOWNLOAD_SELECTORS,
  NAVIGATION_SELECTORS,
  VIEWPORT_SIZES,
  SKILL_CATEGORIES,
  PROJECTS
} from './fixtures/test-data'

test('example', async ({ page }) => {
  // Use predefined selectors
  await page.click(SECTIONS.ABOUT)
  await page.click(DOWNLOAD_SELECTORS.PDF)
  
  // Use predefined data
  expect(SKILL_CATEGORIES).toContain('Web Automation')
  expect(VIEWPORT_SIZES.MOBILE).toEqual({ width: 375, height: 667 })
})
```

---

## 🎯 Writing New Tests

### Basic Test Template

```typescript
import { test, expect } from '@playwright/test'

test.describe('Feature Name', () => {
  test.beforeEach(async ({ page }) => {
    // Setup before each test
    await page.goto('/')
  })

  test('should do something', async ({ page }) => {
    // Arrange
    const element = page.locator('[data-testid="element"]')

    // Act
    await element.click()

    // Assert
    await expect(element).toHaveText('Expected text')
  })

  test('should handle error case', async ({ page }) => {
    // Test error scenario
    const errorMessage = page.locator('[data-testid="error"]')
    await expect(errorMessage).toBeVisible()
  })
})
```

### Best Practices

1. **Use data-testid attributes**
   ```tsx
   <button data-testid="download-cv">Download</button>
   ```

2. **Wait properly**
   ```typescript
   // ✅ Good
   await expect(element).toBeVisible()
   await page.waitForLoadState('networkidle')

   // ❌ Bad
   await page.waitForTimeout(1000)
   ```

3. **Use meaningful names**
   ```typescript
   // ✅ Good
   test('should download PDF when user clicks button', async () => {})

   // ❌ Bad
   test('test 1', async () => {})
   ```

4. **Cleanup after tests**
   ```typescript
   test.afterEach(async ({ page }) => {
     // Close dialogs, clear state
   })
   ```

5. **Test user behavior**
   ```typescript
   // ✅ User-centric
   await page.click('button:has-text("Download")')

   // ❌ Implementation detail
   await page.dispatchEvent('[id="xyz"]', 'click')
   ```

---

## 🔧 Configuration

### playwright.config.ts

```typescript
export default defineConfig({
  testDir: './tests/e2e',           // Where tests are located
  fullyParallel: true,              // Run tests in parallel
  forbidOnly: !!process.env.CI,     // Fail in CI if test.only()
  retries: process.env.CI ? 2 : 0,  // Retry failed tests in CI
  workers: process.env.CI ? 1 : undefined,  // Workers in CI
  reporter: [
    ['html', { outputFolder: 'playwright-report' }],
    ['json', { outputFile: 'playwright-report/results.json' }],
    ['junit', { outputFile: 'playwright-report/results.xml' }],
    ['list']
  ],
  use: {
    baseURL: 'http://localhost:5173',
    trace: 'on-first-retry',      // Trace only on first retry
    screenshot: 'only-on-failure', // Screenshot on failure
  },
  webServer: {
    command: 'pnpm dev',           // Start dev server
    url: 'http://localhost:5173',
    reuseExistingServer: !process.env.CI
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } }
  ]
})
```

---

## 📊 Reports

### HTML Report

```bash
pnpm test:e2e
# View: apps/web/playwright-report/index.html
```

### View Test Report Online

```bash
# Serve report
npx playwright show-report

# Opens http://localhost:3000
```

### Screenshots & Videos

- Stored in: `test-results/`
- Automatically captured on failure
- Included in HTML report

---

## 🔗 Selectors Guide

### Finding Elements

```typescript
// By test ID (recommended)
page.locator('[data-testid="download-cv"]')

// By text
page.locator('button:has-text("Download")')

// By role (most accessible)
page.locator('role=button[name="Download"]')

// By CSS selector
page.locator('.btn-download')

// By XPath
page.locator('//button[@class="btn-download"]')

// Multiple
page.locator('nav a')
```

### Element Interactions

```typescript
// Click
await element.click()

// Type
await input.fill('text')

// Select option
await select.selectOption('value')

// Check/uncheck
await checkbox.check()
await checkbox.uncheck()

// Hover
await element.hover()

// Focus
await element.focus()

// Scroll into view
await element.scrollIntoViewIfNeeded()
```

---

## 🛡️ Assertions

```typescript
// Visibility
await expect(element).toBeVisible()
await expect(element).toBeHidden()

// Content
await expect(element).toHaveText('Expected')
await expect(element).toContainText('Part of text')

// Attributes
await expect(element).toHaveAttribute('href', '/about')

// Classes
await expect(element).toHaveClass('active')

// State
await expect(element).toBeEnabled()
await expect(element).toBeDisabled()
await expect(element).toBeChecked()

// Page
await expect(page).toHaveTitle('Expected Title')
await expect(page).toHaveURL('http://localhost:5173/')
```

---

## 🐛 Debugging

### Debug Mode

```bash
# Step through tests
npx playwright test --debug

# Or add pause in test
test('example', async ({ page }) => {
  await page.pause()  // Browser will pause here
  // Continue in console or DevTools
})
```

### Inspector

```bash
# Open Playwright Inspector
PWDEBUG=1 pnpm test:e2e -- 01-navigation.spec.ts
```

### View Trace

```bash
# Generate trace
npx playwright test --trace on

# View trace
npx playwright show-trace trace.zip
```

### Logs

```bash
# Run with verbose logging
npx playwright test --reporter=list --verbose

# See HTTP requests/responses
page.on('request', request => console.log('→', request.method(), request.url()))
page.on('response', response => console.log('←', response.status(), response.url()))
```

---

## 🔄 Continuous Integration

### GitHub Actions

See `.github/workflows/deploy.yml`:

```yaml
- name: Install Playwright browsers
  run: npx playwright install --with-deps

- name: Run Playwright E2E tests
  run: pnpm --filter @mportafolio/web test:e2e

- name: Upload test report
  if: always()
  uses: actions/upload-artifact@v3
  with:
    name: playwright-report
    path: apps/web/playwright-report/
    retention-days: 30
```

---

## ⚠️ Troubleshooting

### Tests timeout

```bash
# Increase timeout in config
test: {
  timeout: 30000  // 30 seconds
}

# Or for specific test
test.setTimeout(30000)
test('slow test', async () => {
  // ...
})
```

### Browser not found

```bash
# Install browsers
npx playwright install

# Or with system deps
npx playwright install --with-deps
```

### Port already in use

```bash
# Kill process on port 5173
# macOS/Linux
lsof -ti:5173 | xargs kill -9

# Windows PowerShell
netstat -ano | findstr :5173
taskkill /PID <PID> /F
```

### Connection refused

```bash
# Start dev server manually
cd apps/web
pnpm dev

# In another terminal, run tests
pnpm test:e2e
```

### Flaky tests

```typescript
// Increase timeout for this test
test('flaky test', async ({ page }, testInfo) => {
  testInfo.setTimeout(30000)
  // ...
}, { timeout: 30000 })

// Or use retries
test.describe.configure({ retries: 2 })
```

---

## 🚀 Performance Tips

1. **Parallel execution**: Already enabled, don't disable
2. **Headless mode**: Default in CI, faster execution
3. **Worker pool**: Adjust workers based on CPU cores
4. **Minimize waits**: Use waitForLoadState strategically
5. **Reuse sessions**: Keep cookies between tests if possible

---

## 📚 Resources

- [Playwright Docs](https://playwright.dev)
- [Best Practices](https://playwright.dev/docs/best-practices)
- [API Reference](https://playwright.dev/docs/api/class-page)
- [Debugging](https://playwright.dev/docs/debug)
- [CI/CD](https://playwright.dev/docs/ci)

---

**Last Updated**: 2026-09-14  
**Version**: 1.0.0  
**Status**: ✅ Ready for use
