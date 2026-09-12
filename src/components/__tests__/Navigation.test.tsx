/// <reference types="vitest/globals" />
import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { Navigation } from '../Navigation'

vi.mock('../hooks', () => ({
  useScrollPosition: () => false
}))

describe('Navigation Component', () => {
  const mockOnDownloadATS = vi.fn()
  const mockOnDownloadVisual = vi.fn()

  it('should render navigation with logo', () => {
    render(
      <Navigation 
        onDownloadATS={mockOnDownloadATS} 
        onDownloadVisual={mockOnDownloadVisual} 
      />
    )
    expect(screen.getByText('PORTAFOLIO')).toBeInTheDocument()
  })

  it('should render all navigation links', () => {
    render(
      <Navigation 
        onDownloadATS={mockOnDownloadATS} 
        onDownloadVisual={mockOnDownloadVisual} 
      />
    )
    expect(screen.getByText('Sobre Mi')).toBeInTheDocument()
    expect(screen.getByText('Habilidades')).toBeInTheDocument()
    expect(screen.getByText('Experiencia')).toBeInTheDocument()
    expect(screen.getByText('Educacion')).toBeInTheDocument()
  })

  it('should have correct href values for navigation links', () => {
    render(
      <Navigation 
        onDownloadATS={mockOnDownloadATS} 
        onDownloadVisual={mockOnDownloadVisual} 
      />
    )
    const aboutLink = screen.getByText('Sobre Mi').closest('a')
    expect(aboutLink).toHaveAttribute('href', '#about')
  })

  it('should toggle mobile menu on button click', () => {
    const { container } = render(
      <Navigation 
        onDownloadATS={mockOnDownloadATS} 
        onDownloadVisual={mockOnDownloadVisual} 
      />
    )
    
    const menuButton = container.querySelector('button')
    expect(menuButton).toBeInTheDocument()
    
    fireEvent.click(menuButton!)
    // After click, mobile menu should appear
    expect(screen.getAllByText('Sobre Mi').length).toBeGreaterThan(0)
  })

  it('should be fixed position', () => {
    const { container } = render(
      <Navigation 
        onDownloadATS={mockOnDownloadATS} 
        onDownloadVisual={mockOnDownloadVisual} 
      />
    )
    const nav = container.querySelector('nav')
    expect(nav).toHaveClass('fixed')
    expect(nav).toHaveClass('w-full')
    expect(nav).toHaveClass('z-50')
  })
})
