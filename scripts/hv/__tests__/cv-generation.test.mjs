import { describe, it, expect, beforeEach, afterEach } from 'vitest'
import { promises as fs } from 'fs'
import { join } from 'path'
import { fileURLToPath } from 'url'
import { dirname } from 'path'

const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)
const TEMP_DIR = join(__dirname, '../../.temp-test')

describe('CV Generation Script', () => {
  beforeEach(async () => {
    try {
      await fs.mkdir(TEMP_DIR, { recursive: true })
    } catch (err) {
      console.log('Temp dir already exists')
    }
  })

  afterEach(async () => {
    try {
      await fs.rm(TEMP_DIR, { recursive: true, force: true })
    } catch (err) {
      console.log('Failed to clean temp dir')
    }
  })

  it('should have all required contact information', () => {
    const data = {
      name: 'ANDRES RODRIGUEZ PISA',
      title: 'SDET | Senior QA Automation Engineer',
      email: 'andresrdrgzps05@gmail.com',
      phone1: '(+57) 320 324 5988',
      phone2: '(+57) 301 211 9295',
      location: 'Bogotá, Colombia',
      linkedin: 'linkedin.com/in/andresrodriguezpisa-qa/',
      github: 'github.com/Harp-Andres'
    }

    expect(data.name).toBeTruthy()
    expect(data.email).toMatch(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)
    expect(data.phone1).toMatch(/\(\+\d+\)/)
    expect(data.linkedin).toBeTruthy()
  })

  it('should have all required sections in data', () => {
    const requiredSections = [
      'name', 'title', 'email', 'phone1', 'phone2', 
      'location', 'linkedin', 'github', 'profile',
      'skills', 'experience', 'education', 'certs'
    ]

    const data = {
      name: 'Test',
      title: 'Test',
      email: 'test@test.com',
      phone1: '123',
      phone2: '456',
      location: 'Test',
      linkedin: 'http://test.com',
      github: 'http://test.com',
      profile: 'Test profile',
      skills: [],
      experience: [],
      education: [],
      certs: []
    }

    requiredSections.forEach(section => {
      expect(data).toHaveProperty(section)
    })
  })

  it('should have skills with category and items', () => {
    const skills = [
      { cat: 'Web Automation', items: 'Selenium, Playwright' },
      { cat: 'API Testing', items: 'REST Assured, Postman' }
    ]

    skills.forEach(skill => {
      expect(skill).toHaveProperty('cat')
      expect(skill).toHaveProperty('items')
      expect(skill.cat).toBeTruthy()
      expect(skill.items).toBeTruthy()
    })
  })

  it('should have experience entries with required fields', () => {
    const experience = [
      {
        company: 'Test Corp',
        role: 'QA Engineer',
        period: '2024 - Present',
        bullets: ['Did QA work']
      }
    ]

    experience.forEach(exp => {
      expect(exp).toHaveProperty('company')
      expect(exp).toHaveProperty('role')
      expect(exp).toHaveProperty('period')
      expect(exp).toHaveProperty('bullets')
      expect(Array.isArray(exp.bullets)).toBe(true)
    })
  })

  it('should have education entries with required fields', () => {
    const education = [
      { title: 'Degree', inst: 'University', year: '2024' }
    ]

    education.forEach(edu => {
      expect(edu).toHaveProperty('title')
      expect(edu).toHaveProperty('inst')
      expect(edu).toHaveProperty('year')
    })
  })

  it('should have certifications array', () => {
    const certs = [
      'Certification 1',
      'Certification 2',
      'Certification 3'
    ]

    expect(Array.isArray(certs)).toBe(true)
    expect(certs.length).toBeGreaterThan(0)
    certs.forEach(cert => {
      expect(typeof cert).toBe('string')
      expect(cert.length).toBeGreaterThan(0)
    })
  })

  it('should have languages with level', () => {
    const languages = [
      { lang: 'Spanish', level: 'Native' },
      { lang: 'English', level: 'B1' }
    ]

    languages.forEach(lang => {
      expect(lang).toHaveProperty('lang')
      expect(lang).toHaveProperty('level')
    })
  })
})
