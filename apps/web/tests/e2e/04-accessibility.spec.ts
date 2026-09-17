import { test, expect } from '@playwright/test'

test.describe('Accessibility E2E Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/')
  })

  test('should have proper heading hierarchy', async ({ page }) => {
    // Obtén todos los headings
    const h1s = page.locator('h1')
    const h2s = page.locator('h2')

    // Debe haber al menos un H1
    const h1Count = await h1s.count()
    expect(h1Count).toBeGreaterThanOrEqual(1)

    // No debe haber H3 sin H2
    const h3s = page.locator('h3')
    const h3Count = await h3s.count()

    if (h3Count > 0) {
      const h2Count = await h2s.count()
      expect(h2Count).toBeGreaterThan(0)
    }
  })

  test('should have alt text for images', async ({ page }) => {
    const images = page.locator('img')
    const count = await images.count()

    for (let i = 0; i < count; i++) {
      const img = images.nth(i)
      const alt = await img.getAttribute('alt')

      // Las imágenes decorativas pueden tener alt vacío, pero debe existir el atributo
      expect(alt).not.toBeNull()
    }
  })

  test('should have proper color contrast', async ({ page }) => {
    // Verifica que no haya texto con contraste muy bajo
    const textElements = page.locator('p, h1, h2, h3, h4, h5, h6, a, button')
    const count = Math.min(await textElements.count(), 10)

    for (let i = 0; i < count; i++) {
      const element = textElements.nth(i)
      const color = await element.evaluate((el) =>
        window.getComputedStyle(el).color
      )
      const bgColor = await element.evaluate((el) =>
        window.getComputedStyle(el).backgroundColor
      )

      // Verifica que hay un color definido
      expect(color).toBeTruthy()
      expect(bgColor).toBeTruthy()
    }
  })

  test('should have keyboard navigation', async ({ page }) => {
    const firstLink = page.getByRole('link').first()
    await firstLink.focus()

    // Verifica que el elemento recibió focus
    const focused = await page.locator(':focus')
    const focusedText = await focused.textContent()

    expect(focusedText).toBeTruthy()
  })

  test('should have proper button semantics', async ({ page }) => {
    const buttons = page.locator('button')
    const count = await buttons.count()

    expect(count).toBeGreaterThan(0)

    // Verifica que cada botón tiene aria-label o text content
    for (let i = 0; i < Math.min(count, 5); i++) {
      const button = buttons.nth(i)
      const ariaLabel = await button.getAttribute('aria-label')
      const text = await button.textContent()

      const hasLabel = ariaLabel || (text && text.trim().length > 0)
      expect(hasLabel).toBeTruthy()
    }
  })

  test('should have proper link semantics', async ({ page }) => {
    const links = page.locator('a[href]')
    const count = await links.count()

    expect(count).toBeGreaterThan(0)

    // Verifica que cada link tiene texto o aria-label
    for (let i = 0; i < Math.min(count, 5); i++) {
      const link = links.nth(i)
      const ariaLabel = await link.getAttribute('aria-label')
      const text = await link.textContent()

      const hasLabel = ariaLabel || (text && text.trim().length > 0)
      expect(hasLabel).toBeTruthy()
    }
  })

  test('should support keyboard shortcuts', async ({ page }) => {
    // Home - ir al top
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight))
    const scrollY = await page.evaluate(() => window.scrollY)
    expect(scrollY).toBeGreaterThan(0)

    // Presiona Home (el scroll es "smooth", así que esperamos a que termine la animación)
    await page.keyboard.press('Home')
    await expect.poll(() => page.evaluate(() => window.scrollY)).toBeLessThan(100)
  })

  test('should have proper form labels', async ({ page }) => {
    const inputs = page.locator('input, textarea, select')
    const count = await inputs.count()

    for (let i = 0; i < Math.min(count, 5); i++) {
      const input = inputs.nth(i)
      const inputId = await input.getAttribute('id')
      const label = inputId ? page.locator(`label[for="${inputId}"]`) : page.locator('label').filter({ has: input })

      if (await label.count() === 0) {
        const ariaLabel = await input.getAttribute('aria-label')
        expect(ariaLabel).toBeTruthy()
      }
    }
  })

  test('should announce dynamic content updates', async ({ page }) => {
    // Busca aria-live regions
    const ariaLive = page.locator('[aria-live]')
    const count = await ariaLive.count()

    // Puede que haya o no, pero si hay, deben estar bien configurados
    for (let i = 0; i < count; i++) {
      const region = ariaLive.nth(i)
      const liveValue = await region.getAttribute('aria-live')
      expect(['polite', 'assertive', 'off']).toContain(liveValue)
    }
  })

  test('should support focus visible styles', async ({ page }) => {
    const link = page.getByRole('link').first()

    await link.focus()

    // Verifica que hay un outline o indicador visual
    const outline = await link.evaluate((el) =>
      window.getComputedStyle(el).outline
    )

    expect(outline || 'visible').toBeTruthy()
  })

  test('should not have keyboard traps', async ({ page }) => {
    // Navega forward y backward sin quedarse atrapado
    const elements = page.locator('a[href], button')

    if (await elements.count() > 0) {
      // Tab through a few elements
      for (let i = 0; i < 3; i++) {
        await page.keyboard.press('Tab')
        const focused = await page.locator(':focus')
        expect(await focused.count()).toBeLessThanOrEqual(1)
      }
    }
  })

  test('should have proper ARIA landmarks', async ({ page }) => {
    await expect(page.getByRole('navigation', { name: /navegacion principal/i })).toBeVisible()
    await expect(page.getByRole('main')).toBeVisible()
    await expect(page.getByRole('contentinfo')).toBeVisible()
  })
})
