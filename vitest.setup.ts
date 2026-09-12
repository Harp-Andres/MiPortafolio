/// <reference types="vitest/globals" />
/// <reference types="@testing-library/jest-dom" />
import '@testing-library/jest-dom'
import { vi, beforeEach } from 'vitest'

// Mock de window.matchMedia para tests de responsive
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  }))
})

// Configuración global para tests
beforeEach(() => {
  vi.clearAllMocks()
})
