export interface Project {
  id: string
  name: string
  description: string
  longDescription: string
  technologies: string[]
  github: string
  link?: string
  highlights: string[]
  type: 'featured' | 'secondary' | 'supporting'
  image?: string
  stats?: {
    stars?: number
    watchers?: number
    forks?: number
  }
}

export const PROJECTS: Project[] = [
  {
    id: 'automation-test-reports-hub',
    name: 'Automation Test Reports Hub',
    description: 'Centralized CI/CD test reporting platform for multiple projects',
    longDescription: 'Enterprise-grade centralized platform for aggregating test reports from multiple automation projects (Allure, Cucumber, Serenity). Integrated with GitHub Actions for automated report generation and distribution.',
    technologies: ['GitHub Actions', 'Allure Reports', 'Cucumber', 'Serenity', 'CI/CD', 'DevOps'],
    github: 'https://github.com/Harp-Andres/automation-test-reports-hub',
    highlights: [
      'Multi-project test report aggregation',
      'Automated GitHub Actions integration',
      'Allure, Cucumber & Serenity report support',
      'Enterprise-scale reporting solution'
    ],
    type: 'featured'
  },
  {
    id: 'buscar-cruceros',
    name: 'Buscar Cruceros - E2E Automation',
    description: 'Frontend automation with Playwright and JavaScript',
    longDescription: 'End-to-end automation testing project demonstrating modern automation practices using Playwright. Includes comprehensive test scenarios for web-based cruise search and booking workflows.',
    technologies: ['Playwright', 'JavaScript', 'E2E Testing', 'Web Automation', 'POM Pattern'],
    github: 'https://github.com/Harp-Andres/Buscar_Cruceros',
    highlights: [
      'Playwright E2E automation framework',
      'Page Object Model pattern',
      'Cross-browser testing',
      'Real-world application testing'
    ],
    type: 'featured'
  },
  {
    id: 'portfolio-site',
    name: 'Professional Portfolio (This Site)',
    description: 'Modern portfolio site with React 18, TypeScript, and comprehensive testing',
    longDescription: 'Full-stack portfolio application built with React 18 and TypeScript, featuring component-level testing with Vitest and E2E testing with Playwright. Demonstrates CI/CD practices with GitHub Actions and deployment to GitHub Pages.',
    technologies: ['React 18', 'TypeScript', 'Tailwind CSS', 'Vitest', 'Playwright', 'GitHub Actions', 'GitHub Pages'],
    github: 'https://github.com/Harp-Andres/MiPortafolio',
    link: 'https://harp-andres.github.io/MiPortafolio/',
    highlights: [
      '65+ unit tests with 100% pass rate',
      '30+ E2E tests with Playwright',
      'Responsive design (mobile-first)',
      'CI/CD pipeline with GitHub Actions',
      'React components with TypeScript'
    ],
    type: 'featured'
  },
  {
    id: 'literalura',
    name: 'Literalura - Java Backend',
    description: 'Full-stack application with Spring Boot, API integration & Database',
    longDescription: 'Comprehensive Java application demonstrating backend development skills. Uses Spring Boot framework for REST API development, integrates external APIs, and implements database operations with proper error handling.',
    technologies: ['Java', 'Spring Boot', 'REST APIs', 'Database', 'Exception Handling'],
    github: 'https://github.com/Harp-Andres/Literalura',
    highlights: [
      'Spring Boot REST API development',
      'External API integration',
      'Database operations',
      'Advanced exception handling'
    ],
    type: 'secondary'
  }
]
