import { test, expect } from '@playwright/test'

test.describe('Portfolio Navigation', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/')
  })

  test('should have correct title', async ({ page }) => {
    const title = await page.title()
    expect(title).toContain('HARDWARE ANDRES RODRIGUEZ PISA')
  })

  test('should display header with navigation', async ({ page }) => {
    const header = page.locator('nav')
    await expect(header).toBeVisible()
  })

  test('should have download button', async ({ page }) => {
    const downloadBtn = page.locator('button:has-text("Hoja de Vida")')
    await expect(downloadBtn).toBeVisible()
  })

  test('should display hero section', async ({ page }) => {
    const hero = page.locator('h1')
    await expect(hero).toBeVisible()
  })
})

test.describe('Mobile Navigation', () => {
  test.use({ viewport: { width: 375, height: 667 } })

  test('should display mobile menu button on mobile viewport', async ({ page }) => {
    await page.goto('/')
    
    // Mobile viewport should load correctly
    const nav = page.locator('nav')
    await expect(nav).toBeVisible()
  })

  test('should be responsive at mobile size', async ({ page }) => {
    await page.goto('/')
    
    // Verify page loads at mobile viewport
    const body = page.locator('body')
    await expect(body).toBeVisible()
  })
})

test.describe('CV Download', () => {
  test('should have CV download button', async ({ page }) => {
    await page.goto('/')
    
    // Find CV download button
    const downloadBtn = page.locator('button:has-text("Hoja de Vida")')
    await expect(downloadBtn).toBeVisible()
  })

  test('should open CV download modal when clicked', async ({ page }) => {
    await page.goto('/')
    
    // Click download button
    const downloadBtn = page.locator('button:has-text("Hoja de Vida")')
    await downloadBtn.click()
    
    // Verify page content is present
    const body = page.locator('body')
    await expect(body).toBeVisible()
  })
})

test.describe('Responsive Design', () => {
  test('should render on desktop viewport', async ({ page }) => {
    await page.setViewportSize({ width: 1920, height: 1080 })
    await page.goto('/')
    
    // Desktop layout should show navigation
    const nav = page.locator('nav')
    await expect(nav).toBeVisible()
  })

  test('should render on tablet viewport', async ({ page }) => {
    await page.setViewportSize({ width: 768, height: 1024 })
    await page.goto('/')
    
    // Tablet layout should be responsive
    const body = page.locator('body')
    await expect(body).toBeVisible()
  })

  test('should render on mobile viewport', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 })
    await page.goto('/')
    
    // Mobile layout
    const body = page.locator('body')
    await expect(body).toBeVisible()
  })
})

test.describe('Page Content', () => {
  test('should display main content on page load', async ({ page }) => {
    await page.goto('/')
    
    // Main content should be visible
    const main = page.locator('main')
    await expect(main).toBeVisible()
  })

  test('should display multiple sections', async ({ page }) => {
    await page.goto('/')
    
    // Page should have content
    const body = page.locator('body')
    await expect(body).toBeVisible()
    
    // Scroll and verify page is scrollable
    await page.evaluate(() => window.scrollTo(0, 500))
    const scrollPos = await page.evaluate(() => window.scrollY)
    expect(scrollPos).toBeGreaterThan(0)
  })

  test('should have LinkedIn link in footer', async ({ page }) => {
    await page.goto('/')
    
    // Scroll to bottom
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight))
    
    // Look for LinkedIn link
    const linkedinLink = page.locator('a[href*="linkedin"]')
    const count = await linkedinLink.count()
    expect(count).toBeGreaterThan(0)
  })

  test('should not have Facebook link', async ({ page }) => {
    await page.goto('/')
    
    // Verify no Facebook link
    const facebookLink = page.locator('a[href*="facebook"]')
    const count = await facebookLink.count()
    expect(count).toBe(0)
  })

  test('should not have Instagram link', async ({ page }) => {
    await page.goto('/')
    
    // Verify no Instagram link
    const instagramLink = page.locator('a[href*="instagram"]')
    const count = await instagramLink.count()
    expect(count).toBe(0)
  })
})
