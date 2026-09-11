import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import { About } from '../About'

// Mock del hook useAge
vi.mock('../../hooks', () => ({
  useAge: vi.fn(() => 31)
}))

describe('About Component', () => {
  const mockProps = {
    email: 'test@example.com',
    phone: '(+57) 320 324 5988',
    location: 'Bogotá, Colombia',
    linkedin: 'https://linkedin.com/in/test',
    birthDate: '1994-04-05',
    about: 'Ingeniero especializado en QA Automation'
  }

  it('should render about section with correct heading', () => {
    render(<About {...mockProps} />)
    expect(screen.getByText('Sobre Mí')).toBeInTheDocument()
  })

  it('should render contact information heading', () => {
    render(<About {...mockProps} />)
    expect(screen.getByText('Información de Contacto')).toBeInTheDocument()
  })

  it('should display email correctly', () => {
    render(<About {...mockProps} />)
    const emailLink = screen.getByText(mockProps.email)
    expect(emailLink).toHaveAttribute('href', `mailto:${mockProps.email}`)
  })

  it('should display phone number', () => {
    render(<About {...mockProps} />)
    expect(screen.getByText(mockProps.phone)).toBeInTheDocument()
  })

  it('should display location', () => {
    render(<About {...mockProps} />)
    expect(screen.getByText(mockProps.location)).toBeInTheDocument()
  })

  it('should display LinkedIn link with correct href', () => {
    render(<About {...mockProps} />)
    const linkedinLink = screen.getByText('Ver perfil')
    expect(linkedinLink).toHaveAttribute('href', mockProps.linkedin)
    expect(linkedinLink).toHaveAttribute('target', '_blank')
    expect(linkedinLink).toHaveAttribute('rel', 'noopener noreferrer')
  })

  it('should display about text', () => {
    render(<About {...mockProps} />)
    expect(screen.getByText(mockProps.about)).toBeInTheDocument()
  })

  it('should display age label', () => {
    render(<About {...mockProps} />)
    expect(screen.getByText('Edad')).toBeInTheDocument()
  })

  it('should display a numeric age value', () => {
    render(<About {...mockProps} />)
    const { container } = render(<About {...mockProps} />)
    const ageValue = container.querySelector('.text-2xl.font-bold')
    expect(ageValue).toBeInTheDocument()
  })

  it('should have responsive grid layout', () => {
    const { container } = render(<About {...mockProps} />)
    const gridContainer = container.querySelector('.grid')
    expect(gridContainer).toHaveClass('md:grid-cols-2')
  })

  it('should have animation classes', () => {
    const { container } = render(<About {...mockProps} />)
    const animated = container.querySelectorAll('.animate-slideUp')
    expect(animated.length).toBeGreaterThan(0)
  })

  it('should have contact icons', () => {
    const { container } = render(<About {...mockProps} />)
    const iconContainers = container.querySelectorAll('.bg-blue-100')
    expect(iconContainers.length).toBeGreaterThan(0)
  })
})
