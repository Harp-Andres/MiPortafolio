import { Menu, X } from 'lucide-react'
import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useScrollPosition } from '../hooks'
import { CVDownloads } from './CVDownloads'

interface NavProps {
  onDownloadATS: () => void
  onDownloadVisual: () => void
}

export const Navigation = ({ onDownloadATS, onDownloadVisual }: NavProps) => {
  const [isOpen, setIsOpen] = useState(false)
  const isScrolled = useScrollPosition()

  const toggleMenu = () => setIsOpen(!isOpen)

  const navLinks = [
    { label: 'Sobre Mi', href: '/#about', isRoute: false },
    { label: 'Habilidades', href: '/#skills', isRoute: false },
    { label: 'Experiencia', href: '/#experience', isRoute: false },
    { label: 'Educacion', href: '/#education', isRoute: false },
    { label: 'Proyectos', href: '/portafolio', isRoute: true },
  ]

  return (
    <nav className={`fixed w-full z-50 transition-all duration-300 ${
      isScrolled ? 'bg-black shadow-lg' : 'bg-black'
    }`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          
          {/* Logo */}
          <div className="flex-shrink-0">
            <Link to="/" className="text-white font-bold text-xl">
              INICIO
            </Link>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            {navLinks.map(link => (
              link.isRoute ? (
                <Link
                  key={link.href}
                  to={link.href}
                  className="text-gray-300 hover:text-white transition-colors font-semibold"
                >
                  {link.label}
                </Link>
              ) : (
                <a
                  key={link.href}
                  href={link.href}
                  className="text-gray-300 hover:text-white transition-colors"
                >
                  {link.label}
                </a>
              )
            ))}
          </div>

          {/* Download Button Desktop - using CVDownloads component */}
          <div className="hidden lg:flex items-center">
            <CVDownloads onDownloadATS={onDownloadATS} onDownloadVisual={onDownloadVisual} />
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
                link.isRoute ? (
                  <Link
                    key={link.href}
                    to={link.href}
                    className="block px-3 py-2 text-gray-300 hover:text-white transition-colors font-semibold"
                    onClick={() => setIsOpen(false)}
                  >
                    {link.label}
                  </Link>
                ) : (
                  <a
                    key={link.href}
                    href={link.href}
                    className="block px-3 py-2 text-gray-300 hover:text-white transition-colors"
                    onClick={() => setIsOpen(false)}
                  >
                    {link.label}
                  </a>
                )
              ))}
              <div className="pt-4 px-3">
                <CVDownloads onDownloadATS={onDownloadATS} onDownloadVisual={onDownloadVisual} />
              </div>
            </div>
          </div>
        )}
      </div>
    </nav>
  )
}
