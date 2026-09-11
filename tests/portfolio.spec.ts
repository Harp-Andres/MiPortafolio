import { test, expect } from '@playwright/test'

test.describe('Portfolio Navigation', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/')
  })

  test('should have correct title', async ({ page }) => {
    const title = await page.title()
    expect(title).toContain('Portafolio Profesional')
  })

  test('should display header with navigation', async ({ page }) => {
    const header = page.locator('nav')
    await expect(header).toBeVisible()
    await expect(header).toContainText('PORTAFOLIO')
  })

  test('should have download buttons', async ({ page }) => {
    const downloadBtns = page.locator('button:has-text("ATS"), button:has-text("Visual")')
    const count = await downloadBtns.count()
    expect(count).toBeGreaterThan(0)
  })

  test('should navigate to sections via links', async ({ page }) => {
    await page.click('a:has-text("Sobre Mi")')
    const aboutSection = page.locator('#about')
    await expect(aboutSection).toBeVisible()
  })
})

test.describe('Mobile Navigation', () => {
  test.use({ viewport: { width: 375, height: 667 } })

  test('should display hamburger menu on mobile', async ({ page }) => {
    await page.goto('/')
    
    // Check if hamburger button is visible
    const hamburger = page.locator('button:has-text("Menu")')
    await expect(hamburger).toBeVisible({ timeout: 5000 })
  })

  test('should toggle mobile menu', async ({ page }) => {
    await page.goto('/')
    
    // Click hamburger
    const hamburger = page.locator('button').first()
    await hamburger.click()
    
    // Check if menu items appear
    const menuItem = page.locator('a:has-text("Sobre Mi")')
    await expect(menuItem).toBeVisible()
  })
})

test.describe('CV Download', () => {
  test('should download ATS CV', async ({ page }) => {
    await page.goto('/')
    
    // Find and click ATS download button
    const atsBtn = page.locator('button:has-text("ATS")').first()
    await expect(atsBtn).toBeVisible()
    
    // Listen for download
    const downloadPromise = page.waitForEvent('download')
    await atsBtn.click()
    
    const download = await downloadPromise
    expect(download.suggestedFilename()).toContain('HV_2026')
  })

  test('should download Visual CV', async ({ page }) => {
    await page.goto('/')
    
    // Find and click Visual download button
    const visualBtn = page.locator('button:has-text("Visual")').first()
    await expect(visualBtn).toBeVisible()
    
    // Listen for download
    const downloadPromise = page.waitForEvent('download')
    await visualBtn.click()
    
    const download = await downloadPromise
    expect(download.suggestedFilename()).toContain('HV_2026')
  })
})

test.describe('Responsive Design', () => {
  test('should be responsive on desktop', async ({ page }) => {
    await page.setViewportSize({ width: 1920, height: 1080 })
    await page.goto('/')
    
    // Desktop layout should show full menu
    const nav = page.locator('nav')
    await expect(nav).toBeVisible()
  })

  test('should be responsive on tablet', async ({ page }) => {
    await page.setViewportSize({ width: 768, height: 1024 })
    await page.goto('/')
    
    // Tablet layout
    const body = page.locator('body')
    await expect(body).toHaveCSS('background-color', 'rgb(255, 255, 255)')
  })

  test('should be responsive on mobile', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 })
    await page.goto('/')
    
    // Mobile layout
    const body = page.locator('body')
    await expect(body).toHaveCSS('background-color', 'rgb(255, 255, 255)')
  })
})

test.describe('Skills Section', () => {
  test('should display skills section', async ({ page }) => {
    await page.goto('/#skills')
    
    const skillsSection = page.locator('#skills')
    await expect(skillsSection).toBeVisible()
    await expect(skillsSection).toContainText('Habilidades')
  })

  test('should display skill categories', async ({ page }) => {
    await page.goto('/#skills')
    
    // Check if cards are visible
    const cards = page.locator('.card')
    const count = await cards.count()
    expect(count).toBeGreaterThan(0)
  })
})

test.describe('Experience Section', () => {
  test('should display experience section', async ({ page }) => {
    await page.goto('/#experience')
    
    const expSection = page.locator('#experience')
    await expect(expSection).toBeVisible()
    await expect(expSection).toContainText('Experiencia')
  })
})

test.describe('Education Section', () => {
  test('should display education section', async ({ page }) => {
    await page.goto('/#education')
    
    const eduSection = page.locator('#education')
    await expect(eduSection).toBeVisible()
    await expect(eduSection).toContainText('Educación')
  })
})

test.describe('Footer', () => {
  test('should display footer with contact info', async ({ page }) => {
    await page.goto('/')
    
    // Scroll to bottom
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight))
    
    const footer = page.locator('footer')
    await expect(footer).toBeVisible()
    await expect(footer).toContainText('LinkedIn')
  })

  test('should have LinkedIn link', async ({ page }) => {
    await page.goto('/')
    
    // Scroll to bottom
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight))
    
    const linkedinLink = page.locator('a[href*="linkedin"]')
    await expect(linkedinLink).toBeVisible()
  })
})

test.describe('No Facebook/Instagram', () => {
  test('should not have Facebook link', async ({ page }) => {
    await page.goto('/')
    
    const facebookLink = page.locator('a[href*="facebook"]')
    await expect(facebookLink).not.toBeVisible()
  })

  test('should not have Instagram link', async ({ page }) => {
    await page.goto('/')
    
    const instagramLink = page.locator('a[href*="instagram"]')
    await expect(instagramLink).not.toBeVisible()
  })
})
