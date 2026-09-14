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

          {/* Links */}
          <div>
            <h4 className="text-lg font-semibold mb-4">Enlaces Rápidos</h4>
            <ul className="space-y-2 text-gray-400">
              <li><a href="/#about" className="hover:text-white transition-colors">Sobre Mí</a></li>
              <li><a href="/#skills" className="hover:text-white transition-colors">Habilidades</a></li>
              <li><a href="/#experience" className="hover:text-white transition-colors">Experiencia</a></li>
              <li><a href="/#education" className="hover:text-white transition-colors">Educación</a></li>
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h4 className="text-lg font-semibold mb-4">Contacto</h4>
            <ul className="space-y-2 text-gray-400">
              <li><a href="mailto:andresrdrgzps05@gmail.com" className="hover:text-white transition-colors">andresrdrgzps05@gmail.com</a></li>
              <li><p>(+57) 3012119295</p></li>
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
