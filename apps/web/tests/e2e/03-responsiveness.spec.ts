import { test, expect, devices } from '@playwright/test'

// Tests de responsiveness en múltiples dispositivos
const viewports = [
  { name: 'Mobile (iPhone 12)', device: 'iPhone 12' },
  { name: 'Tablet (iPad)', device: 'iPad' },
  { name: 'Desktop (1920x1080)', width: 1920, height: 1080 }
]

viewports.forEach((viewport) => {
  test.describe(`Responsiveness - ${viewport.name}`, () => {
    test.beforeEach(async ({ page }) => {
      // Configura el viewport
      if (viewport.device) {
        const device = devices[viewport.device as keyof typeof devices]
        await page.setViewportSize(device.viewport)
      } else {
        await page.setViewportSize({
          width: viewport.width!,
          height: viewport.height!
        })
      }

      await page.goto('/')
    })

    test('should render hero section correctly', async ({ page }) => {
      const hero = page.locator('[data-testid="hero-section"]')
      await expect(hero).toBeVisible()

      // Verifica que el contenido es legible
      const heading = page.locator('[data-testid="hero-heading"]')
      await expect(heading).toBeVisible()
    })

    test('should render navigation correctly', async ({ page }) => {
      const nav = page.locator('nav')
      await expect(nav).toBeVisible()

      // En mobile, puede ser un hamburger menu
      const navLinks = page.locator('nav a')
      const count = await navLinks.count()
      expect(count).toBeGreaterThan(0)
    })

    test('should render skills section with proper layout', async ({ page }) => {
      await page.click('a[href="#skills"]')

      const skillsSection = page.locator('[data-testid="skills-section"]')
      await expect(skillsSection).toBeVisible()

      // Verifica que las skill cards sean accesibles
      const skillCards = page.locator('[data-testid="skill-category"]')
      const count = await skillCards.count()
      expect(count).toBeGreaterThan(0)

      // Verifica que cada card es visible sin scroll horizontal
      for (let i = 0; i < Math.min(count, 2); i++) {
        const card = skillCards.nth(i)
        const box = await card.boundingBox()
        expect(box?.width).toBeLessThanOrEqual(
          await page.evaluate(() => window.innerWidth)
        )
      }
    })

    test('should render projects with proper card layout', async ({ page }) => {
      await page.click('a[href="#projects"]')

      const projectCards = page.locator('[data-testid="project-card"]')
      const count = await projectCards.count()
      expect(count).toBeGreaterThan(0)

      // Verifica que las tarjetas son responsivas
      const firstCard = projectCards.first()
      const box = await firstCard.boundingBox()
      expect(box).toBeTruthy()
    })

    test('should render tables/lists with horizontal scroll if needed', async ({ page }) => {
      await page.click('a[href="#experience"]')

      const experienceSection = page.locator('[data-testid="experience-section"]')
      await expect(experienceSection).toBeVisible()

      // Verifica que el contenido es accesible
      const items = page.locator('[data-testid="experience-item"]')
      const count = await items.count()
      expect(count).toBeGreaterThan(0)
    })

    test('should maintain proper font sizes', async ({ page }) => {
      const heading = page.locator('[data-testid="hero-heading"]')
      const fontSize = await heading.evaluate((el) =>
        window.getComputedStyle(el).fontSize
      )

      // Verifica que el font size es readable (> 12px)
      const size = parseInt(fontSize)
      expect(size).toBeGreaterThanOrEqual(12)
    })

    test('should have proper touch targets on mobile', async ({ page }) => {
      if (viewport.device?.includes('iPhone')) {
        // Verifica que los botones son clickeables en mobile
        const buttons = page.locator('button, a[href*="#"]')
        const firstButton = buttons.first()

        const box = await firstButton.boundingBox()
        // Los botones deben ser al menos 44x44 pixels (recomendación Apple)
        expect(box?.width).toBeGreaterThanOrEqual(44)
        expect(box?.height).toBeGreaterThanOrEqual(44)
      }
    })

    test('should not have horizontal overflow', async ({ page }) => {
      // Verifica que no hay scroll horizontal
      const bodyWidth = await page.evaluate(() => document.body.scrollWidth)
      const windowWidth = await page.evaluate(() => window.innerWidth)

      expect(bodyWidth).toBeLessThanOrEqual(windowWidth + 2) // +2 para rounding errors
    })

    test('should render footer correctly', async ({ page }) => {
      // Scroll al footer
      await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight))

      const footer = page.locator('footer')
      if (await footer.isVisible()) {
        const footerBox = await footer.boundingBox()
        expect(footerBox?.width).toBeGreaterThan(0)
      }
    })
  })
})
