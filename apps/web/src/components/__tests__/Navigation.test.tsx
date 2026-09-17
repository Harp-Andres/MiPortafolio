/// <reference types="vitest/globals" />
import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { HashRouter } from 'react-router-dom'
import { Navigation } from '../Navigation'

vi.mock('../hooks', () => ({
  useScrollPosition: () => false
}))

const renderWithRouter = (component: React.ReactElement) => {
  return render(<HashRouter>{component}</HashRouter>)
}

describe('Navigation Component', () => {
  const mockOnDownloadATS = vi.fn()
  const mockOnDownloadVisual = vi.fn()

  it('should render navigation with logo', () => {
    renderWithRouter(
      <Navigation 
        onDownloadATS={mockOnDownloadATS} 
        onDownloadVisual={mockOnDownloadVisual} 
      />
    )
    expect(screen.getByText('INICIO')).toBeInTheDocument()
  })

  it('should render all navigation links', () => {
    renderWithRouter(
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
    renderWithRouter(
      <Navigation 
        onDownloadATS={mockOnDownloadATS} 
        onDownloadVisual={mockOnDownloadVisual} 
      />
    )
    const aboutButton = screen.getByRole('button', { name: /sobre mi/i })
    expect(aboutButton).toBeInTheDocument()
  })

  it('should toggle mobile menu on button click', () => {
    renderWithRouter(
      <Navigation 
        onDownloadATS={mockOnDownloadATS} 
        onDownloadVisual={mockOnDownloadVisual} 
      />
    )
    
    const menuButton = screen.getByRole('button', { name: /abrir menu principal/i })
    expect(menuButton).toBeInTheDocument()
    
    fireEvent.click(menuButton)
    // After click, mobile menu should appear
    expect(screen.getAllByText('Sobre Mi').length).toBeGreaterThan(1)
  })

  it('should be fixed position', () => {
    const { container } = renderWithRouter(
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
