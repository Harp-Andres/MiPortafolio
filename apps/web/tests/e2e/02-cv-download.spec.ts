import { test, expect } from '@playwright/test'
import path from 'path'

test.describe('CV Download E2E Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/')
  })

  test('should have download CV button', async ({ page }) => {
    // Busca el botón de descargar CV
    const downloadButton = page.locator('[data-testid="download-cv"]')
    await expect(downloadButton).toBeVisible()
    await expect(downloadButton).toBeEnabled()
  })

  test('should download PDF CV successfully', async ({ page, context }) => {
    // Promete para esperar a la descarga
    const downloadPromise = context.waitForEvent('download')

    // Click en el botón de descargar PDF
    const pdfButton = page.locator('[data-testid="download-cv-pdf"]')
    await pdfButton.click()

    // Espera a que se complete la descarga
    const download = await downloadPromise
    expect(download.suggestedFilename()).toContain('.pdf')

    // Verifica que el archivo fue descargado
    const filePath = await download.path()
    expect(filePath).toBeTruthy()
  })

  test('should download DOCX CV successfully', async ({ page, context }) => {
    // Promete para esperar a la descarga
    const downloadPromise = context.waitForEvent('download')

    // Click en el botón de descargar DOCX
    const docxButton = page.locator('[data-testid="download-cv-docx"]')
    await docxButton.click()

    // Espera a que se complete la descarga
    const download = await downloadPromise
    expect(download.suggestedFilename()).toContain('.docx')
  })

  test('should show loading state during download', async ({ page }) => {
    // Click en descargar
    const downloadButton = page.locator('[data-testid="download-cv"]')
    await downloadButton.click()

    // Verifica que hay un loading state
    const loadingState = page.locator('[data-testid="download-loading"]')
    await expect(loadingState).toBeVisible({ timeout: 5000 })
  })

  test('should have multiple format options', async ({ page }) => {
    // Busca los botones de descarga
    const downloadButtons = page.locator('[data-testid^="download-cv-"]')

    // Verifica que hay al menos 2 opciones (PDF y DOCX)
    const count = await downloadButtons.count()
    expect(count).toBeGreaterThanOrEqual(2)
  })

  test('should show download success message', async ({ page }) => {
    // Click en descargar
    const downloadButton = page.locator('[data-testid="download-cv"]')
    await downloadButton.click()

    // Espera por el mensaje de éxito
    const successMessage = page.locator('[data-testid="download-success"]')
    await expect(successMessage).toBeVisible({ timeout: 10000 })
  })

  test('should maintain download history', async ({ page }) => {
    // Descarga múltiples veces
    const downloadButton = page.locator('[data-testid="download-cv"]')

    for (let i = 0; i < 3; i++) {
      await downloadButton.click()
      await page.waitForTimeout(500)
    }

    // Verifica que el botón sigue funcionando
    await expect(downloadButton).toBeEnabled()
  })

  test('should have download button in hero section', async ({ page }) => {
    // Verifica que el botón está visible sin scroll
    const heroDownloadButton = page.locator('[data-testid="hero-download-btn"]')
    await expect(heroDownloadButton).toBeVisible()
    await expect(heroDownloadButton).toBeInViewport()
  })

  test('should have download button in About section', async ({ page }) => {
    // Navega a About
    await page.click('a[href="#about"]')

    // Verifica que el botón está disponible
    const aboutDownloadButton = page.locator('[data-testid="about-download-btn"]')
    await expect(aboutDownloadButton).toBeVisible()
  })
})
