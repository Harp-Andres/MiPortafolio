import { ArrowRight, FolderGit2 } from 'lucide-react'
import { Link } from 'react-router-dom'
import { CV_DATA } from '../utils/cv-data'

export const Footer = () => {
  const currentYear = new Date().getFullYear()

  return (
    <footer className="bg-black text-white py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid md:grid-cols-3 gap-8 mb-8">
          
          {/* Brand */}
          <div>
            <h3 className="text-2xl font-bold mb-2">HOJA DE VIDA</h3>
            <p className="text-gray-400">
              SDET Senior | QA Automation Engineer
            </p>
          </div>

          {/* Proyectos */}
          <div className="flex flex-col items-start">
            <h4 className="text-lg font-semibold mb-4">Proyectos</h4>
            <p className="text-gray-400 mb-4">
              Explora los proyectos y casos de estudio de automatización que he desarrollado.
            </p>
            <Link
              to="/portafolio"
              className="inline-flex items-center gap-2 text-blue-400 hover:text-blue-300 font-semibold transition-colors"
            >
              <FolderGit2 size={18} />
              Ver Proyectos
              <ArrowRight size={16} />
            </Link>
          </div>

          {/* Contact */}
          <div>
            <h4 className="text-lg font-semibold mb-4">Contacto</h4>
            <ul className="space-y-2 text-gray-400">
              <li><a href="mailto:andresrdrgzps05@gmail.com" className="hover:text-white transition-colors">andresrdrgzps05@gmail.com</a></li>
              <li><p>{CV_DATA.phone1} - {CV_DATA.phone2}</p></li>
              <li className="pt-2">
                <a 
                  href="https://www.linkedin.com/in/AndresRodriguezPisa-CalidadDeSoftware" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="text-blue-400 hover:text-blue-300 transition-colors"
                >
                  LinkedIn
                </a>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-gray-700 pt-8 mt-8">
          <p className="text-center text-gray-400">
            © {currentYear} Andrés Rodríguez Pisa. Todos los derechos reservados.
          </p>
        </div>
      </div>
    </footer>
  )
}
