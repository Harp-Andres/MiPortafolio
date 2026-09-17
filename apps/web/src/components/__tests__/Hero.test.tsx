/// <reference types="vitest/globals" />
import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { Hero } from '../Hero'

describe('Hero Component', () => {
  it('should render hero section with name and title', () => {
    render(
      <Hero 
        name="John Doe" 
        title="Senior QA Engineer"
      />
    )
    expect(screen.getByText('John Doe')).toBeInTheDocument()
    expect(screen.getByText('Senior QA Engineer')).toBeInTheDocument()
  })

  it('should display description text', () => {
    render(
      <Hero 
        name="John Doe" 
        title="Senior QA Engineer"
      />
    )
    expect(screen.getByText(/Ingeniero de Calidad de Software/)).toBeInTheDocument()
  })

  it('should have proper heading hierarchy', () => {
    render(
      <Hero 
        name="John Doe" 
        title="Senior QA Engineer"
      />
    )
    const heading1 = screen.getByRole('heading', { level: 1 })
    const heading2 = screen.getByRole('heading', { level: 2 })
    
    expect(heading1).toHaveTextContent('John Doe')
    expect(heading2).toHaveTextContent('Senior QA Engineer')
  })

  it('should have animation class', () => {
    const { container } = render(
      <Hero 
        name="John Doe" 
        title="Senior QA Engineer"
      />
    )
    const animated = container.querySelector('.animate-slideUp')
    expect(animated).toBeInTheDocument()
  })

  it('should have gradient background', () => {
    const { container } = render(
      <Hero 
        name="John Doe" 
        title="Senior QA Engineer"
      />
    )
    const section = container.querySelector('section')
    expect(section).toHaveClass('bg-gradient-to-br')
  })
})
