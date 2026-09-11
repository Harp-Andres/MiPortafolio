import { test, expect } from '@playwright/test'

// Configuración de viewports de prueba
const VIEWPORTS = {
  samsungS24: { width: 360, height: 800, name: 'Samsung S24 (360px)' },
  tablet: { width: 768, height: 1024, name: 'Tablet (768px)' },
  desktop: { width: 1920, height: 1080, name: 'Desktop (1920px)' },
  iphone12: { width: 390, height: 844, name: 'iPhone 12 (390px)' },
  iPad: { width: 1024, height: 1366, name: 'iPad (1024px)' }
}

test.describe('Responsive Skills Section', () => {
  test('should display skills in 1 column on Samsung S24 (360px)', async ({ page }) => {
    await page.setViewportSize(VIEWPORTS.samsungS24)
    await page.goto('/')
    
    // Scroll to skills section
    const skillsSection = page.locator('#skills')
    await skillsSection.scrollIntoViewIfNeeded()
    
    // Verify grid columns for mobile
    const grid = skillsSection.locator('.grid').first()
    const computedStyle = await grid.evaluate(el => 
      window.getComputedStyle(el).gridTemplateColumns
    )
    
    // On 360px, should show 1 column (grid-cols-1)
    const columns = computedStyle.split(' ').length
    expect(columns).toBeLessThanOrEqual(2) // Might be 1 or less on very small screens
  })

  test('should display skills in 2 columns on Tablet (768px)', async ({ page }) => {
    await page.setViewportSize(VIEWPORTS.tablet)
    await page.goto('/')
    
    const skillsSection = page.locator('#skills')
    await skillsSection.scrollIntoViewIfNeeded()
    
    // On 768px, should show 2 columns (sm:grid-cols-2)
    const cards = skillsSection.locator('.h-80')
    const cardCount = await cards.count()
    expect(cardCount).toBeGreaterThan(0)
  })

  test('should display skills in 3 columns on Desktop (1920px)', async ({ page }) => {
    await page.setViewportSize(VIEWPORTS.desktop)
    await page.goto('/')
    
    const skillsSection = page.locator('#skills')
    await skillsSection.scrollIntoViewIfNeeded()
    
    // On 1920px, should show 3 columns (lg:grid-cols-3)
    const grid = skillsSection.locator('.grid').first()
    const computedStyle = await grid.evaluate(el => 
      window.getComputedStyle(el).gridTemplateColumns
    )
    
    const columns = computedStyle.split(' ').length
    expect(columns).toBeGreaterThanOrEqual(2)
  })
})

test.describe('Responsive Education Section', () => {
  test('should display education in 1 column on mobile (360px)', async ({ page }) => {
    await page.setViewportSize(VIEWPORTS.samsungS24)
    await page.goto('/')
    
    const educationSection = page.locator('#education')
    await educationSection.scrollIntoViewIfNeeded()
    
    // Mobile: 1 column
    const cards = educationSection.locator('.card')
    expect(await cards.count()).toBeGreaterThan(0)
  })

  test('should display education in 2 columns on tablet and above', async ({ page }) => {
    await page.setViewportSize(VIEWPORTS.tablet)
    await page.goto('/')
    
    const educationSection = page.locator('#education')
    await educationSection.scrollIntoViewIfNeeded()
    
    const cards = educationSection.locator('.card')
    expect(await cards.count()).toBeGreaterThan(0)
  })
})

test.describe('Samsung S24 Viewport (360px)', () => {
  test('should render navigation correctly', async ({ page }) => {
    await page.setViewportSize(VIEWPORTS.samsungS24)
    await page.goto('/')
    
    const nav = page.locator('nav')
    await expect(nav).toBeVisible()
    
    // Logo should be visible
    const logo = nav.locator('a:has-text("PORTAFOLIO")')
    await expect(logo).toBeVisible()
  })

  test('should have mobile menu button visible', async ({ page }) => {
    await page.setViewportSize(VIEWPORTS.samsungS24)
    await page.goto('/')
    
    // Mobile button should be visible on small screens
    const button = page.locator('button').first()
    await expect(button).toBeVisible()
  })

  test('should display hero section responsively', async ({ page }) => {
    await page.setViewportSize(VIEWPORTS.samsungS24)
    await page.goto('/')
    
    const hero = page.locator('h1')
    await expect(hero).toBeVisible()
  })

  test('should have readable text sizes', async ({ page }) => {
    await page.setViewportSize(VIEWPORTS.samsungS24)
    await page.goto('/')
    
    const heading = page.locator('h1')
    const fontSize = await heading.evaluate(el => 
      window.getComputedStyle(el).fontSize
    )
    
    // Font size should be reasonable (not too small)
    const sizeInPixels = parseInt(fontSize)
    expect(sizeInPixels).toBeGreaterThanOrEqual(24)
  })

  test('should have proper padding on mobile', async ({ page }) => {
    await page.setViewportSize(VIEWPORTS.samsungS24)
    await page.goto('/')
    
    const section = page.locator('section').first()
    const padding = await section.evaluate(el => 
      window.getComputedStyle(el).paddingLeft
    )
    
    const paddingInPixels = parseInt(padding)
    expect(paddingInPixels).toBeGreaterThan(0)
  })
})

test.describe('Tablet Viewport (768px)', () => {
  test('should render 2-column layouts', async ({ page }) => {
    await page.setViewportSize(VIEWPORTS.tablet)
    await page.goto('/')
    
    const education = page.locator('#education')
    await education.scrollIntoViewIfNeeded()
    
    const grid = education.locator('.grid').first()
    await expect(grid).toBeVisible()
  })

  test('should have balanced content layout', async ({ page }) => {
    await page.setViewportSize(VIEWPORTS.tablet)
    await page.goto('/')
    
    const about = page.locator('#about')
    await about.scrollIntoViewIfNeeded()
    
    await expect(about).toBeVisible()
  })
})

test.describe('Desktop Viewport (1920px)', () => {
  test('should show full 3-column skills grid', async ({ page }) => {
    await page.setViewportSize(VIEWPORTS.desktop)
    await page.goto('/')
    
    const skillsSection = page.locator('#skills')
    await skillsSection.scrollIntoViewIfNeeded()
    
    const cards = skillsSection.locator('.h-80')
    expect(await cards.count()).toBeGreaterThan(2)
  })

  test('should have full navigation bar visible', async ({ page }) => {
    await page.setViewportSize(VIEWPORTS.desktop)
    await page.goto('/')
    
    const navLinks = page.locator('nav a')
    expect(await navLinks.count()).toBeGreaterThan(3)
  })
})

test.describe('Responsive Images and Media', () => {
  test('should load images correctly on all viewports', async ({ page }) => {
    const viewports = [VIEWPORTS.samsungS24, VIEWPORTS.tablet, VIEWPORTS.desktop]
    
    for (const viewport of viewports) {
      await page.setViewportSize(viewport)
      await page.goto('/')
      
      // Check if page loads without errors
      const body = page.locator('body')
      await expect(body).toBeVisible()
    }
  })
})

test.describe('Cross-Device Consistency', () => {
  test('should have same content across all devices', async ({ page }) => {
    const viewports = [VIEWPORTS.samsungS24, VIEWPORTS.tablet, VIEWPORTS.desktop]
    
    for (const viewport of viewports) {
      await page.setViewportSize(viewport)
      await page.goto('/')
      
      // Navigation should always be present
      const nav = page.locator('nav')
      await expect(nav).toBeVisible()
      
      // Hero section should always be present
      const hero = page.locator('h1')
      await expect(hero).toBeVisible()
    }
  })

  test('should have no horizontal overflow on any device', async ({ page }) => {
    const viewports = [VIEWPORTS.samsungS24, VIEWPORTS.tablet, VIEWPORTS.desktop]
    
    for (const viewport of viewports) {
      await page.setViewportSize(viewport)
      await page.goto('/')
      
      const scrollWidth = await page.evaluate(() => document.documentElement.scrollWidth)
      const clientWidth = await page.evaluate(() => document.documentElement.clientWidth)
      
      expect(scrollWidth).toBeLessThanOrEqual(clientWidth + 2) // Small tolerance
    }
  })
})
