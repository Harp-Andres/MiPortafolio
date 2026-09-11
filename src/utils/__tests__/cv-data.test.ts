import { describe, it, expect } from 'vitest'
import { CV_DATA } from '../cv-data'

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
    expect(CV_DATA.profile.length).toBeGreaterThan(50)
  })

  it('should have skills array with categories', () => {
    expect(Array.isArray(CV_DATA.skills)).toBe(true)
    expect(CV_DATA.skills.length).toBeGreaterThan(0)
    
    CV_DATA.skills.forEach(skill => {
      expect(skill).toHaveProperty('category')
      expect(skill).toHaveProperty('items')
      expect(skill.category).toBeTruthy()
      expect(skill.items).toBeTruthy()
    })
  })

  it('should have experience array with required fields', () => {
    expect(Array.isArray(CV_DATA.experience)).toBe(true)
    expect(CV_DATA.experience.length).toBeGreaterThan(0)
    
    CV_DATA.experience.forEach(exp => {
      expect(exp).toHaveProperty('company')
      expect(exp).toHaveProperty('role')
      expect(exp).toHaveProperty('period')
      expect(Array.isArray(exp.bullets)).toBe(true)
    })
  })

  it('should have education array', () => {
    expect(Array.isArray(CV_DATA.education)).toBe(true)
    expect(CV_DATA.education.length).toBeGreaterThan(0)
    
    CV_DATA.education.forEach(edu => {
      expect(edu).toHaveProperty('degree')
      expect(edu).toHaveProperty('institution')
      expect(edu).toHaveProperty('year')
    })
  })

  it('should have certifications by category', () => {
    expect(CV_DATA.certificatesByCategory).toBeDefined()
    expect(typeof CV_DATA.certificatesByCategory).toBe('object')
  })

  it('should have valid birth date format', () => {
    const dateRegex = /^\d{4}-\d{2}-\d{2}$/
    expect(CV_DATA.birthDate).toMatch(dateRegex)
  })

  it('should have all skills with non-empty items', () => {
    CV_DATA.skills.forEach(skill => {
      const items = skill.items.split(',').map(i => i.trim())
      expect(items.length).toBeGreaterThan(0)
      items.forEach(item => {
        expect(item.length).toBeGreaterThan(0)
      })
    })
  })

  it('should have experience with non-empty bullets', () => {
    CV_DATA.experience.forEach(exp => {
      expect(exp.bullets.length).toBeGreaterThan(0)
      exp.bullets.forEach(bullet => {
        expect(bullet.length).toBeGreaterThan(0)
      })
    })
  })

  it('should have consistent data types', () => {
    expect(typeof CV_DATA.name).toBe('string')
    expect(typeof CV_DATA.title).toBe('string')
    expect(typeof CV_DATA.email).toBe('string')
    expect(typeof CV_DATA.phone1).toBe('string')
    expect(typeof CV_DATA.location).toBe('string')
    expect(typeof CV_DATA.profile).toBe('string')
  })
})
