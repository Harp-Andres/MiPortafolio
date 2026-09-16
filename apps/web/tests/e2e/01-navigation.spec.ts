import { test, expect } from '@playwright/test'

test.describe('Navigation E2E Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/')
  })

  test('should load the homepage successfully', async ({ page }) => {
    await expect(page).toHaveTitle(/Hoja de Vida/)
    await expect(page.getByRole('navigation', { name: /navegacion principal/i })).toBeVisible()
    await expect(page.getByRole('main')).toBeVisible()
    await expect(page.getByRole('heading', { level: 1 })).toBeVisible()
  })

  test('should navigate to About section', async ({ page }) => {
    await page.getByRole('heading', { level: 2, name: /sobre m[ií]/i }).scrollIntoViewIfNeeded()
    await expect(page.getByRole('heading', { level: 2, name: /sobre m[ií]/i })).toBeVisible()
  })

  test('should navigate to Skills section', async ({ page }) => {
    await page.getByRole('heading', { level: 2, name: /habilidades profesionales/i }).scrollIntoViewIfNeeded()
    await expect(page.getByRole('heading', { level: 2, name: /habilidades profesionales/i })).toBeVisible()
  })

  test('should navigate to Experience section', async ({ page }) => {
    await page.getByRole('heading', { level: 2, name: /experiencia profesional/i }).scrollIntoViewIfNeeded()
    await expect(page.getByRole('heading', { level: 2, name: /experiencia profesional/i })).toBeVisible()
  })

  test('should navigate to Projects section', async ({ page }) => {
    await page.getByRole('link', { name: /proyectos/i }).first().click()
    await expect(page).toHaveURL(/#\/portafolio/)
    await expect(page.getByRole('heading', { level: 1, name: /portfolio de proyectos/i })).toBeVisible()
  })

  test('should navigate to Education section', async ({ page }) => {
    await page.getByRole('heading', { level: 2, name: /educaci[oó]n/i }).scrollIntoViewIfNeeded()
    await expect(page.getByRole('heading', { level: 2, name: /educaci[oó]n/i })).toBeVisible()
  })

  test('should scroll to top when clicking logo/home', async ({ page }) => {
    await page.getByRole('heading', { level: 2, name: /experiencia profesional/i }).scrollIntoViewIfNeeded()
    let scrollTop = await page.evaluate(() => window.scrollY)
    expect(scrollTop).toBeGreaterThan(0)

    await page.getByRole('link', { name: /inicio/i }).first().click()
    scrollTop = await page.evaluate(() => window.scrollY)
    expect(scrollTop).toBeLessThan(100)
  })

  test('should have proper navigation links structure', async ({ page }) => {
    const nav = page.getByRole('navigation', { name: /navegacion principal/i })
    const navLinks = nav.getByRole('link').filter({ hasText: /sobre mi|habilidades|experiencia|educacion|proyectos/i })
    const count = await navLinks.count()
    expect(count).toBeGreaterThan(0)

    for (let i = 0; i < count; i++) {
      const href = await navLinks.nth(i).getAttribute('href')
      expect(href).toBeTruthy()
    }
  })
})
