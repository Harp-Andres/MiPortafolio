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
    const nav = page.getByRole('navigation', { name: /navegacion principal/i })
    await nav.getByRole('button', { name: /sobre mi/i }).click()
    await expect(page.getByRole('heading', { level: 2, name: /sobre m[ií]/i })).toBeInViewport()
  })

  test('should navigate to Skills section', async ({ page }) => {
    const nav = page.getByRole('navigation', { name: /navegacion principal/i })
    await nav.getByRole('button', { name: /habilidades/i }).click()
    await expect(page.getByRole('heading', { level: 2, name: /habilidades profesionales/i })).toBeInViewport()
  })

  test('should navigate to Experience section', async ({ page }) => {
    const nav = page.getByRole('navigation', { name: /navegacion principal/i })
    await nav.getByRole('button', { name: /experiencia/i }).click()
    await expect(page.getByRole('heading', { level: 2, name: /experiencia profesional/i })).toBeInViewport()
  })

  test('should navigate to Projects section', async ({ page }) => {
    const nav = page.getByRole('navigation', { name: /navegacion principal/i })
    await nav.getByRole('link', { name: /proyectos/i }).click()
    await expect(page).toHaveURL(/#\/portafolio/)
    await expect(page.getByRole('heading', { level: 1, name: /portfolio de proyectos/i })).toBeVisible()
  })

  test('should navigate to Education section', async ({ page }) => {
    const nav = page.getByRole('navigation', { name: /navegacion principal/i })
    await nav.getByRole('button', { name: /educacion/i }).click()
    await expect(page.getByRole('heading', { level: 2, name: /educaci[oó]n/i })).toBeInViewport()
  })

  test('should scroll to top when clicking logo/home', async ({ page }) => {
    const nav = page.getByRole('navigation', { name: /navegacion principal/i })
    await nav.getByRole('button', { name: /experiencia/i }).click()
    await expect(page.getByRole('heading', { level: 2, name: /experiencia profesional/i })).toBeInViewport()

    await nav.getByRole('link', { name: /inicio/i }).click()
    await expect(page.getByRole('heading', { level: 1 })).toBeInViewport()
  })

  test('should have proper navigation links structure', async ({ page }) => {
    const nav = page.getByRole('navigation', { name: /navegacion principal/i })
    await expect(nav.getByRole('button', { name: /sobre mi/i })).toBeVisible()
    await expect(nav.getByRole('button', { name: /habilidades/i })).toBeVisible()
    await expect(nav.getByRole('button', { name: /experiencia/i })).toBeVisible()
    await expect(nav.getByRole('button', { name: /educacion/i })).toBeVisible()
    await expect(nav.getByRole('link', { name: /proyectos/i })).toBeVisible()
  })
})
