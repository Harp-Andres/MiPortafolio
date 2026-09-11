import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { Education } from '../Education'

describe('Education Component', () => {
  const mockEducation = [
    {
      degree: 'Ingeniero de Sistemas',
      institution: 'Universidad Nacional Abierta y a Distancia (UNAD)',
      year: '2024'
    },
    {
      degree: 'Tecnólogo en Gestión de Redes de Datos',
      institution: 'SENA',
      year: '2018'
    }
  ]

  it('should render the section with correct heading', () => {
    render(<Education items={mockEducation} />)
    const heading = screen.getByRole('heading', { name: /Educación/i })
    expect(heading).toBeInTheDocument()
  })

  it('should render all education items', () => {
    render(<Education items={mockEducation} />)
    expect(screen.getByText('Ingeniero de Sistemas')).toBeInTheDocument()
    expect(screen.getByText('Tecnólogo en Gestión de Redes de Datos')).toBeInTheDocument()
  })

  it('should display institution names', () => {
    render(<Education items={mockEducation} />)
    expect(screen.getByText(/Universidad Nacional/)).toBeInTheDocument()
    expect(screen.getByText('SENA')).toBeInTheDocument()
  })

  it('should display graduation years', () => {
    render(<Education items={mockEducation} />)
    expect(screen.getByText('2024')).toBeInTheDocument()
    expect(screen.getByText('2018')).toBeInTheDocument()
  })

  it('should have responsive grid classes', () => {
    const { container } = render(<Education items={mockEducation} />)
    const gridContainer = container.querySelector('.grid')
    expect(gridContainer).toHaveClass('grid-cols-1')
    expect(gridContainer).toHaveClass('md:grid-cols-2')
  })

  it('should apply animation delay to items', () => {
    const { container } = render(<Education items={mockEducation} />)
    const items = container.querySelectorAll('.animate-slideUp')
    expect(items.length).toBe(mockEducation.length)
    
    items.forEach((item, index) => {
      expect(item).toHaveStyle(`animation-delay: ${index * 0.1}s`)
    })
  })

  it('should handle empty education list', () => {
    const { container } = render(<Education items={[]} />)
    const gridContainer = container.querySelector('.grid')
    expect(gridContainer?.children.length).toBe(0)
  })

  it('should have proper card styling', () => {
    const { container } = render(<Education items={mockEducation} />)
    const cards = container.querySelectorAll('.card')
    expect(cards.length).toBe(mockEducation.length)
  })
})
