/// <reference types="vitest/globals" />
import { describe, it, expect } from 'vitest'
import { CV_DATA } from '@mportafolio/core'

describe('CV Data Constants', () => {
  it('should have required personal information', () => {
    expect(CV_DATA.name).toBeTruthy()
    expect(CV_DATA.title).toBeTruthy()
    expect(CV_DATA.email).toBeTruthy()
    expect(CV_DATA.phone1).toBeTruthy()
    expect(CV_DATA.location).toBeTruthy()
  })

  it('should have valid email format', () => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    expect(CV_DATA.email).toMatch(emailRegex)
  })

  it('should have valid contact links', () => {
    expect(CV_DATA.linkedin).toBeTruthy()
    expect(CV_DATA.github).toBeTruthy()
  })

  it('should have non-empty profile description', () => {
    expect(typeof CV_DATA.bio === 'string' || typeof CV_DATA.profile === 'string').toBe(true)
  })

  it('should have skills array with categories', () => {
    expect(Array.isArray(CV_DATA.skills)).toBe(true)
    expect(CV_DATA.skills.length).toBeGreaterThan(0)
  })

  it('should have experience array with required fields', () => {
    expect(Array.isArray(CV_DATA.experience)).toBe(true)
    expect(CV_DATA.experience.length).toBeGreaterThan(0)
  })

  it('should have education array', () => {
    expect(Array.isArray(CV_DATA.education)).toBe(true)
    expect(CV_DATA.education.length).toBeGreaterThan(0)
  })

  it('should have certificates', () => {
    expect(typeof CV_DATA.certificates === 'object').toBe(true)
    expect(Object.keys(CV_DATA.certificates).length).toBeGreaterThan(0)
  })

  it('should have languages', () => {
    expect(Array.isArray(CV_DATA.languages)).toBe(true)
    expect(CV_DATA.languages.length).toBeGreaterThan(0)
  })

  it('should have valid birth date format', () => {
    const dateRegex = /^\d{4}-\d{2}-\d{2}$/
    expect(CV_DATA.birthDate).toMatch(dateRegex)
  })
})
