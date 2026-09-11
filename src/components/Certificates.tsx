interface CertificateCategory {
  [key: string]: string[]
}

interface CertificatesProps {
  items: string[]
  byCategory?: CertificateCategory
  microsoftStudies?: string[]
}

export const Certificates = ({ byCategory, microsoftStudies = [] }: CertificatesProps) => {
  const categories = byCategory || {}
  const categoryColors: { [key: string]: string } = {
    'DevOps & Cloud': 'border-orange-500 bg-orange-50',
    'Calidad & QA': 'border-blue-500 bg-blue-50',
    'Automatización Web & Mobile': 'border-green-500 bg-green-50',
    'Playwright & API Testing': 'border-purple-500 bg-purple-50',
    'Otros Frameworks & Herramientas': 'border-pink-500 bg-pink-50',
    'IA & Productividad': 'border-red-500 bg-red-50',
    'Programación & Desarrollo': 'border-indigo-500 bg-indigo-50',
  }

  const categoryIcons: { [key: string]: string } = {
    'DevOps & Cloud': '☁️',
    'Calidad & QA': '✅',
    'Automatización Web & Mobile': '🔧',
    'Playwright & API Testing': '🎭',
    'Otros Frameworks & Herramientas': '⚙️',
    'IA & Productividad': '🤖',
    'Programación & Desarrollo': '💻',
  }

  return (
    <section id="certificates" className="py-16 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="text-3xl font-bold mb-12 text-gray-900">Certificaciones & Formación</h2>

        {/* CERTIFICACIONES POR CATEGORÍA */}
        <div className="mb-16">
          <h3 className="text-2xl font-bold mb-8 text-gray-900">Certificaciones Profesionales</h3>
          <div className="grid md:grid-cols-2 gap-4 auto-rows-fr">
            {Object.entries(categories).map(([category, certs]) => (
              <div
                key={category}
                className={`border-l-4 rounded-lg p-6 ${categoryColors[category] || 'border-gray-300 bg-gray-50'}`}
              >
                <div className="flex items-center gap-2 mb-4">
                  <span className="text-2xl">{categoryIcons[category] || '📌'}</span>
                  <h4 className="text-lg font-bold text-gray-900">{category}</h4>
                </div>
                <ul className="space-y-3">
                  {certs.map((cert, index) => (
                    <li key={index} className="flex items-start gap-2">
                      <span className="text-blue-600 font-bold mt-1">•</span>
                      <span className="text-gray-700">{cert}</span>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>

        {/* ESTUDIOS MICROSOFT */}
        {microsoftStudies.length > 0 && (
          <div>
            <h3 className="text-2xl font-bold mb-8 text-gray-900">Capacitación Microsoft</h3>
            <div className="border-l-4 border-green-500 bg-green-50 rounded-lg p-6">
              <div className="flex items-center gap-2 mb-4">
                <span className="text-2xl">📚</span>
                <h4 className="text-lg font-bold text-gray-900">Microsoft Learning</h4>
              </div>
              <ul className="space-y-3">
                {microsoftStudies.map((study, index) => (
                  <li key={index} className="flex items-start gap-2">
                    <span className="text-green-600 font-bold mt-1">•</span>
                    <span className="text-gray-700">{study}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        )}
      </div>
    </section>
  )
}
