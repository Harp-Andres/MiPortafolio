import { test, expect } from '@playwright/test'
import { promises as fs } from 'node:fs'
import path from 'node:path'

test.describe('CV Download E2E Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/')
  })

  test('should expose semantic download trigger and dialog', async ({ page }) => {
    const trigger = page.getByRole('button', { name: /hoja de vida descargable/i }).first()
    await expect(trigger).toBeVisible()
    await expect(trigger).toBeEnabled()

    await trigger.click()

    const dialog = page.getByRole('dialog', { name: /descargar hoja de vida/i })
    await expect(dialog).toBeVisible()
    await expect(dialog.getByText(/selecciona el formato/i)).toBeVisible()
  })

  test('should download PDF CV successfully', async ({ page }) => {
    await page.getByRole('button', { name: /hoja de vida descargable/i }).first().click()
    const atsLink = page.getByRole('link', { name: /formato ats pdf/i })
    await expect(atsLink).toHaveAttribute('download', /\.pdf$/i)

    const href = await atsLink.getAttribute('href')
    expect(href).toBeTruthy()
    expect(href).toMatch(/^\/cv\/.*\.pdf$/i)
    await atsLink.click()

    const localPath = path.join(process.cwd(), 'public', href!.replace(/^\//, ''))
    const stat = await fs.stat(localPath)
    expect(stat.size).toBeGreaterThan(0)

    const body = await fs.readFile(localPath)
    expect(body.byteLength).toBeGreaterThan(0)
    expect(body.subarray(0, 4).toString()).toBe('%PDF')
  })

  test('should download visual PDF CV successfully', async ({ page }) => {
    await page.getByRole('button', { name: /hoja de vida descargable/i }).first().click()

    const visualLink = page.getByRole('link', { name: /formato visual pdf/i })
    await expect(visualLink).toHaveAttribute('download', /\.pdf$/i)

    const href = await visualLink.getAttribute('href')
    expect(href).toBeTruthy()
    expect(href).toMatch(/^\/cv\/.*\.pdf$/i)
    await visualLink.click()

    const localPath = path.join(process.cwd(), 'public', href!.replace(/^\//, ''))
    const stat = await fs.stat(localPath)
    expect(stat.size).toBeGreaterThan(0)

    const body = await fs.readFile(localPath)
    expect(body.byteLength).toBeGreaterThan(0)
    expect(body.subarray(0, 4).toString()).toBe('%PDF')
  })

  test('should expose both semantic format options in dialog', async ({ page }) => {
    await page.getByRole('button', { name: /hoja de vida descargable/i }).first().click()

    const dialog = page.getByRole('dialog', { name: /descargar hoja de vida/i })
    await expect(dialog.getByRole('link', { name: /formato ats pdf/i })).toBeVisible()
    await expect(dialog.getByRole('link', { name: /formato visual pdf/i })).toBeVisible()
  })

  test('should close download dialog with close semantic button', async ({ page }) => {
    await page.getByRole('button', { name: /hoja de vida descargable/i }).first().click()

    const dialog = page.getByRole('dialog', { name: /descargar hoja de vida/i })
    await expect(dialog).toBeVisible()

    await page.getByRole('button', { name: /cerrar dialogo de descarga/i }).click()
    await expect(dialog).toBeHidden()
  })
})
