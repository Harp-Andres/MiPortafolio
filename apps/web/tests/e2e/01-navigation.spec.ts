import { test, expect } from '@playwright/test'

test.describe('Navigation E2E Tests', () => {
  test.beforeEach(async ({ page }) => {
    // Navega a la página principal
    await page.goto('/')
  })

  test('should load the homepage successfully', async ({ page }) => {
    // Verifica que el título esté presente
    await expect(page).toHaveTitle(/Hoja de Vida/)

    // Verifica que el hero está visible
    const hero = page.locator('[data-testid="hero-section"]')
    await expect(hero).toBeVisible()
  })

  test('should navigate to About section', async ({ page }) => {
    // Click en el link de About
    await page.click('a[href="#about"]')

    // Espera a que la sección About sea visible
    const aboutSection = page.locator('[data-testid="about-section"]')
    await expect(aboutSection).toBeVisible()
  })

  test('should navigate to Skills section', async ({ page }) => {
    // Click en el link de Skills
    await page.click('a[href="#skills"]')

    // Verifica que se muestren las categorías de skills
    const skillsSection = page.locator('[data-testid="skills-section"]')
    await expect(skillsSection).toBeVisible()

    // Verifica que hay categorías de habilidades
    const skillCategories = page.locator('[data-testid="skill-category"]')
    await expect(skillCategories).toHaveCount(3)
  })

  test('should navigate to Experience section', async ({ page }) => {
    // Click en el link de Experience
    await page.click('a[href="#experience"]')

    // Verifica que la sección sea visible
    const experienceSection = page.locator('[data-testid="experience-section"]')
    await expect(experienceSection).toBeVisible()
  })

  test('should navigate to Projects section', async ({ page }) => {
    // Click en el link de Projects
    await page.click('a[href="#projects"]')

    // Verifica que la sección sea visible
    const projectsSection = page.locator('[data-testid="projects-section"]')
    await expect(projectsSection).toBeVisible()

    // Verifica que hay tarjetas de proyectos
    const projectCards = page.locator('[data-testid="project-card"]')
    const count = await projectCards.count()
    expect(count).toBeGreaterThan(0)
  })

  test('should navigate to Education section', async ({ page }) => {
    // Click en el link de Education
    await page.click('a[href="#education"]')

    // Verifica que la sección sea visible
    const educationSection = page.locator('[data-testid="education-section"]')
    await expect(educationSection).toBeVisible()
  })

  test('should navigate to Certificates section', async ({ page }) => {
    // Click en el link de Certificates
    await page.click('a[href="#certificates"]')

    // Verifica que la sección sea visible
    const certificatesSection = page.locator('[data-testid="certificates-section"]')
    await expect(certificatesSection).toBeVisible()
  })

  test('should scroll to top when clicking logo/home', async ({ page }) => {
    // Navega a una sección
    await page.click('a[href="#projects"]')

    // Verifica que estamos más abajo en la página
    let scrollTop = await page.evaluate(() => window.scrollY)
    expect(scrollTop).toBeGreaterThan(0)

    // Click en el logo/home
    await page.click('[data-testid="logo"]')

    // Verifica que volvemos al top
    scrollTop = await page.evaluate(() => window.scrollY)
    expect(scrollTop).toBeLessThan(100)
  })

  test('should have proper navigation links structure', async ({ page }) => {
    // Verifica que todos los links de navegación están presentes
    const navLinks = page.locator('nav a')
    const count = await navLinks.count()
    expect(count).toBeGreaterThan(0)

    // Verifica que cada link tiene href
    for (let i = 0; i < count; i++) {
      const href = await navLinks.nth(i).getAttribute('href')
      expect(href).toBeTruthy()
    }
  })
})
