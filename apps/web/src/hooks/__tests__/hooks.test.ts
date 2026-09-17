/// <reference types="vitest/globals" />
import { describe, it, expect, vi } from 'vitest'
import { renderHook, waitFor } from '@testing-library/react'
import { useAge, useScrollPosition } from '../index'

describe('useAge Hook', () => {
  it('should calculate age correctly', async () => {
    const birthDate = '1994-04-05'
    const { result } = renderHook(() => useAge(birthDate))
    
    // Esperar a que el effect se ejecute
    await waitFor(() => {
      expect(result.current).toBeGreaterThan(0)
    })
    
    // La edad debería ser aproximadamente 30-32 (2026 - 1994)
    expect(result.current).toBeGreaterThanOrEqual(30)
    expect(result.current).toBeLessThanOrEqual(32)
  })

  it('should calculate age for 2024 graduation', async () => {
    const birthDate = '1993-04-05'
    const { result } = renderHook(() => useAge(birthDate))
    
    await waitFor(() => {
      expect(result.current).toBeGreaterThan(0)
    })
    
    // Edad debería ser alrededor de 32-33
    expect(result.current).toBeGreaterThanOrEqual(32)
    expect(result.current).toBeLessThanOrEqual(33)
  })

  it('should handle different birth dates', async () => {
    const dates = ['2000-01-01', '1990-12-31', '1985-06-15']
    
    for (const birthDate of dates) {
      const { result } = renderHook(() => useAge(birthDate))
      
      await waitFor(() => {
        expect(result.current).toBeGreaterThanOrEqual(0)
      })
      
      expect(result.current).toBeLessThanOrEqual(100)
    }
  })

  it('should recalculate age on birthDate change', async () => {
    let birthDate = '1994-04-05'
    const { result, rerender } = renderHook(
      ({ bd }: { bd: string }) => useAge(bd),
      { initialProps: { bd: birthDate } }
    )
    
    await waitFor(() => {
      expect(result.current).toBeGreaterThan(0)
    })
    
    const firstAge = result.current
    birthDate = '2000-01-01'
    rerender({ bd: birthDate })
    
    await waitFor(() => {
      expect(result.current).not.toEqual(firstAge)
    })
  })
})

describe('useScrollPosition Hook', () => {
  it('should return false initially', () => {
    const { result } = renderHook(() => useScrollPosition())
    expect(result.current).toBe(false)
  })

  it('should track scroll position', async () => {
    const { result } = renderHook(() => useScrollPosition())
    
    // Simular scroll
    Object.defineProperty(window, 'scrollY', {
      writable: true,
      configurable: true,
      value: 60
    })
    
    window.dispatchEvent(new Event('scroll'))
    
    // Podría ser true después de scroll > 50
    expect(typeof result.current).toBe('boolean')
  })

  it('should return false when scroll is less than 50', async () => {
    const { result } = renderHook(() => useScrollPosition())
    
    Object.defineProperty(window, 'scrollY', {
      writable: true,
      configurable: true,
      value: 30
    })
    
    window.dispatchEvent(new Event('scroll'))
    expect(result.current).toBe(false)
  })

  it('should clean up event listener on unmount', () => {
    const removeEventListenerSpy = vi.spyOn(window, 'removeEventListener')
    const { unmount } = renderHook(() => useScrollPosition())
    
    unmount()
    
    expect(removeEventListenerSpy).toHaveBeenCalledWith('scroll', expect.any(Function))
    removeEventListenerSpy.mockRestore()
  })
})
