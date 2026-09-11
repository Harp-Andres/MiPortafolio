import { Menu, X, Download } from 'lucide-react'
import { useState } from 'react'
import { useScrollPosition } from '../hooks'

interface NavProps {
  onDownloadATS: () => void
  onDownloadVisual: () => void
}

export const Navigation = ({ onDownloadATS, onDownloadVisual }: NavProps) => {
  const [isOpen, setIsOpen] = useState(false)
  const isScrolled = useScrollPosition()

  const toggleMenu = () => setIsOpen(!isOpen)

  const navLinks = [
    { label: 'Sobre Mi', href: '#about' },
    { label: 'Habilidades', href: '#skills' },
    { label: 'Experiencia', href: '#experience' },
    { label: 'Educacion', href: '#education' },
  ]

  return (
    <nav className={`fixed w-full z-50 transition-all duration-300 ${
      isScrolled ? 'bg-black shadow-lg' : 'bg-black'
    }`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          
          {/* Logo */}
          <div className="flex-shrink-0">
            <a href="#" className="text-white font-bold text-xl">
              PORTAFOLIO
            </a>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            {navLinks.map(link => (
              <a
                key={link.href}
                href={link.href}
                className="text-gray-300 hover:text-white transition-colors"
              >
                {link.label}
              </a>
            ))}
          </div>

          {/* Download Buttons Desktop */}
          <div className="hidden lg:flex items-center space-x-4">
            <button
              onClick={onDownloadATS}
              className="flex items-center gap-2 px-4 py-2 bg-white text-black rounded hover:bg-gray-200 transition-colors"
              title="Descargar CV en formato ATS"
            >
              <Download size={18} />
              <span className="text-sm">ATS</span>
            </button>
            <button
              onClick={onDownloadVisual}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
              title="Descargar CV Visual"
            >
              <Download size={18} />
              <span className="text-sm">Visual</span>
            </button>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button
              onClick={toggleMenu}
              className="text-gray-300 hover:text-white"
            >
              {isOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isOpen && (
          <div className="md:hidden pb-4">
            <div className="space-y-2">
              {navLinks.map(link => (
                <a
                  key={link.href}
                  href={link.href}
                  className="block px-3 py-2 text-gray-300 hover:text-white transition-colors"
                  onClick={() => setIsOpen(false)}
                >
                  {link.label}
                </a>
              ))}
              <div className="flex gap-2 pt-4 px-3">
                <button
                  onClick={() => {
                    onDownloadATS()
                    setIsOpen(false)
                  }}
                  className="flex-1 flex items-center justify-center gap-2 px-3 py-2 bg-white text-black rounded hover:bg-gray-200 transition-colors text-sm"
                >
                  <Download size={16} />
                  ATS
                </button>
                <button
                  onClick={() => {
                    onDownloadVisual()
                    setIsOpen(false)
                  }}
                  className="flex-1 flex items-center justify-center gap-2 px-3 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors text-sm"
                >
                  <Download size={16} />
                  Visual
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </nav>
  )
}
