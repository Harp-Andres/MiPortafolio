/**
 * Test fixtures and shared data for E2E tests
 */

export const TEST_TIMEOUTS = {
  SHORT: 5000,
  MEDIUM: 10000,
  LONG: 30000
}

export const SECTIONS = {
  HERO: '[data-testid="hero-section"]',
  ABOUT: '[data-testid="about-section"]',
  SKILLS: '[data-testid="skills-section"]',
  EXPERIENCE: '[data-testid="experience-section"]',
  PROJECTS: '[data-testid="projects-section"]',
  EDUCATION: '[data-testid="education-section"]',
  CERTIFICATES: '[data-testid="certificates-section"]',
  CONTACT: '[data-testid="contact-section"]'
}

export const DOWNLOAD_SELECTORS = {
  BUTTON: '[data-testid="download-cv"]',
  PDF: '[data-testid="download-cv-pdf"]',
  DOCX: '[data-testid="download-cv-docx"]',
  LOADING: '[data-testid="download-loading"]',
  SUCCESS: '[data-testid="download-success"]',
  ERROR: '[data-testid="download-error"]'
}

export const NAVIGATION_SELECTORS = {
  LOGO: '[data-testid="logo"]',
  NAV: 'nav',
  NAV_LINKS: 'nav a',
  HAMBURGER: '[data-testid="hamburger-menu"]',
  CLOSE_MENU: '[data-testid="close-menu"]'
}

export const SKILL_CATEGORIES = [
  'Web Automation',
  'API Testing',
  'Mobile Testing',
  'Performance Testing',
  'CI/CD Integration'
]

export const PROJECTS = [
  {
    name: 'Playwright Automation',
    description: 'Modern web automation framework'
  },
  {
    name: 'API Testing Suite',
    description: 'Comprehensive REST API testing'
  },
  {
    name: 'E2E Testing Framework',
    description: 'End-to-end testing infrastructure'
  }
]

export const VIEWPORT_SIZES = {
  MOBILE: { width: 375, height: 667 },
  TABLET: { width: 768, height: 1024 },
  DESKTOP: { width: 1920, height: 1080 }
}

export const WAIT_ACTIONS = {
  NAVIGATION: async (page: any) => {
    await page.waitForLoadState('networkidle')
  },
  ANIMATION: async () => {
    await new Promise((resolve) => setTimeout(resolve, 500))
  },
  DOWNLOAD: async () => {
    await new Promise((resolve) => setTimeout(resolve, 2000))
  }
}
