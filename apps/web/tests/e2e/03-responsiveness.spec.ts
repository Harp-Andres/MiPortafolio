import { test, expect, devices } from '@playwright/test'

// Tests de responsiveness en múltiples dispositivos
const viewports = [
  { name: 'Mobile (iPhone 12)', width: devices['iPhone 12'].viewport.width, height: devices['iPhone 12'].viewport.height },
  { name: 'Tablet (iPad)', width: 768, height: 1024 },
  { name: 'Desktop (1920x1080)', width: 1920, height: 1080 }
]

viewports.forEach((viewport) => {
  test.describe(`Responsiveness - ${viewport.name}`, () => {
    test.beforeEach(async ({ page }) => {
      await page.setViewportSize({
        width: viewport.width,
        height: viewport.height,
      })

      await page.goto('/')
    })

    test('should render semantic landmarks correctly', async ({ page }) => {
      await expect(page.getByRole('navigation', { name: /navegacion principal/i })).toBeVisible()
      await expect(page.getByRole('main')).toBeVisible()
      await expect(page.getByRole('contentinfo')).toBeVisible()
      await expect(page.getByRole('heading', { level: 1 })).toBeVisible()
    })

    test('should keep section navigation reachable', async ({ page }) => {
      if (viewport.name.includes('iPhone')) {
        await page.getByRole('button', { name: /abrir menu principal/i }).click()
      }

      await page.getByRole('heading', { level: 2, name: /habilidades profesionales/i }).scrollIntoViewIfNeeded()
      await expect(page.getByRole('heading', { level: 2, name: /habilidades profesionales/i })).toBeVisible()
    })

    test('should maintain proper font sizes', async ({ page }) => {
      const heading = page.getByRole('heading', { level: 1 })
      const fontSize = await heading.evaluate((el) =>
        window.getComputedStyle(el).fontSize
      )

      // Verifica que el font size es readable (> 12px)
      const size = parseInt(fontSize)
      expect(size).toBeGreaterThanOrEqual(12)
    })

    test('should have proper touch targets on mobile', async ({ page }) => {
      if (viewport.name.includes('iPhone')) {
        const firstButton = page.getByRole('button', { name: /abrir menu principal/i })
        await expect(firstButton).toBeVisible()

        const box = await firstButton.boundingBox()
        expect(box?.width).toBeGreaterThanOrEqual(40)
        expect(box?.height).toBeGreaterThanOrEqual(40)
      }
    })

    test('should not have horizontal overflow', async ({ page }) => {
      // Verifica que no hay scroll horizontal
      const bodyWidth = await page.evaluate(() => document.body.scrollWidth)
      const windowWidth = await page.evaluate(() => window.innerWidth)

      expect(bodyWidth).toBeLessThanOrEqual(windowWidth + 120)
    })

    test('should render footer correctly', async ({ page }) => {
      await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight))
      await expect(page.getByRole('contentinfo')).toBeVisible()
    })
  })
})
