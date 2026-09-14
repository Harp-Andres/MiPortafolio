/// <reference types="vitest/globals" />
import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { Skills } from '../Skills'

describe('Skills Component', () => {
  const mockCategories = [
    {
      category: 'Web Automation',
      items: 'Selenium WebDriver, Playwright, Cypress'
    },
    {
      category: 'API Testing',
      items: 'REST Assured, Postman, SoapUI'
    }
  ]

  it('should render the section with correct heading', () => {
    render(<Skills categories={mockCategories} />)
    const heading = screen.getByRole('heading', { name: /Habilidades Profesionales/i })
    expect(heading).toBeInTheDocument()
  })

  it('should render all skill categories', () => {
    render(<Skills categories={mockCategories} />)
    expect(screen.getByText('Web Automation')).toBeInTheDocument()
    expect(screen.getByText('API Testing')).toBeInTheDocument()
  })

  it('should display all skill items correctly', () => {
    render(<Skills categories={mockCategories} />)
    expect(screen.getByText(/Selenium WebDriver/)).toBeInTheDocument()
    expect(screen.getByText(/Playwright/)).toBeInTheDocument()
    expect(screen.getByText(/REST Assured/)).toBeInTheDocument()
  })

  it('should have responsive grid classes', () => {
    const { container } = render(<Skills categories={mockCategories} />)
    const gridContainer = container.querySelector('.grid')
    expect(gridContainer).toHaveClass('grid-cols-1')
    expect(gridContainer).toHaveClass('sm:grid-cols-2')
    expect(gridContainer).toHaveClass('lg:grid-cols-3')
  })

  it('should parse comma-separated items correctly', () => {
    render(<Skills categories={mockCategories} />)
    const items = screen.getAllByText(/WebDriver|Playwright|Cypress|Assured|Postman|SoapUI/)
    expect(items.length).toBeGreaterThan(0)
  })

  it('should apply animation delay to cards', () => {
    const { container } = render(<Skills categories={mockCategories} />)
    const cards = container.querySelectorAll('.animate-slideUp')
    expect(cards.length).toBe(mockCategories.length)
    
    cards.forEach((card, index) => {
      expect(card).toHaveStyle(`animation-delay: ${index * 0.05}s`)
    })
  })

  it('should handle empty categories', () => {
    const { container } = render(<Skills categories={[]} />)
    const gridContainer = container.querySelector('.grid')
    expect(gridContainer?.children.length).toBe(0)
  })

  it('should sort categories by item count (largest first)', () => {
    const categories = [
      { category: 'Small', items: 'Item1, Item2' },
      { category: 'Large', items: 'Item1, Item2, Item3, Item4, Item5' },
      { category: 'Medium', items: 'Item1, Item2, Item3' }
    ]
    render(<Skills categories={categories} />)
    
    // La primera tarjeta debe ser "Large" (5 items)
    const cards = screen.getAllByRole('heading', { level: 4 })
    expect(cards[0]).toHaveTextContent('Large')
  })
})
