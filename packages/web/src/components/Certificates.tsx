interface Certificate {
  title: string
  filePath: string | null
  hours?: number
}

interface CertificateCategory {
  [key: string]: Certificate[] | string[]
}

interface OfficialCertification {
  title: string
  issuer: string
  color: string
  icon: string
}

interface CertificatesProps {
  items?: (Certificate | string)[]
  byCategory?: CertificateCategory
  learningPaths?: Certificate[]
  officialCertifications?: OfficialCertification[]
}

const isCertificateObject = (cert: unknown): cert is Certificate => {
  return typeof cert === 'object' && cert !== null && 'title' in cert
}

export const Certificates = ({ byCategory, learningPaths = [], officialCertifications = [] }: CertificatesProps) => {
  const categories = byCategory || {}
  
  const handleDownload = (filePath: string | null) => {
    if (!filePath) return
    // The file path is relative to public, so we can use it directly
    const link = document.createElement('a')
    link.href = filePath
    link.download = filePath.split('/').pop() || 'certificado'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

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

        {/* CERTIFICACIONES OFICIALES */}
        {officialCertifications.length > 0 && (
          <div className="mb-16">
            <h3 className="text-2xl font-bold mb-8 text-gray-900">Certificaciones Oficiales</h3>
            <div className="grid grid-cols-2 gap-6">
              {officialCertifications.map((cert, index) => (
                <div
                  key={index}
                  className={`border-l-4 rounded-lg p-6 flex flex-col items-start ${cert.color}`}
                >
                  <div className="flex items-center gap-3 mb-3">
                    <span className="text-3xl">{cert.icon}</span>
                    <div>
                      <h4 className="text-lg font-bold text-gray-900">{cert.title}</h4>
                      <p className="text-sm text-gray-600">Emisor: {cert.issuer}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* RUTAS DE APRENDIZAJE */}
        {learningPaths.length > 0 && (
          <div className="mb-16">
            <h3 className="text-2xl font-bold mb-8 text-gray-900">Rutas de Aprendizaje</h3>
            <p className="text-gray-600 mb-6 text-sm italic">Programas formales y de mayor duración</p>
            <div className="grid grid-cols-1 gap-6">
              {learningPaths.map((cert, index) => {
                const hasFile = cert.filePath !== null
                return (
                  <div
                    key={index}
                    className="border-l-4 border-indigo-500 bg-indigo-50 rounded-lg p-6 flex flex-col sm:flex-row sm:items-center sm:justify-between"
                  >
                    <div className="flex-1">
                      {hasFile ? (
                        <button
                          onClick={() => handleDownload(cert.filePath)}
                          className="text-left text-lg font-semibold text-blue-600 hover:text-blue-800 hover:underline transition-colors cursor-pointer"
                          title="Clic para descargar"
                        >
                          {cert.title}
                          <span className="ml-2 text-sm">📥</span>
                        </button>
                      ) : (
                        <h4 className="text-lg font-semibold text-gray-900">{cert.title}</h4>
                      )}
                    </div>
                    {cert.hours && (
                      <div className="mt-3 sm:mt-0 sm:ml-4 flex items-center gap-2 bg-white rounded-full px-4 py-2 text-sm font-semibold text-indigo-700">
                        <span>⏱️</span>
                        <span>{cert.hours} horas</span>
                      </div>
                    )}
                  </div>
                )
              })}
            </div>
          </div>
        )}

        {/* CURSOS DE FORMACIÓN */}
        <div>
          <h3 className="text-2xl font-bold mb-8 text-gray-900">Cursos de Formación</h3>
          <div className="grid grid-cols-3 gap-4 auto-rows-fr">
            {Object.entries(categories).map(([category, certs]) => (
              <div
                key={category}
                className={`border-l-4 rounded-lg p-6 min-h-56 flex flex-col ${categoryColors[category] || 'border-gray-300 bg-gray-50'}`}
              >
                <div className="flex items-center gap-2 mb-4">
                  <span className="text-2xl">{categoryIcons[category] || '📌'}</span>
                  <h4 className="text-lg font-bold text-gray-900">{category}</h4>
                </div>
                <ul className="space-y-3">
                  {certs.map((cert, index) => {
                    const isObject = isCertificateObject(cert)
                    const title = isObject ? cert.title : cert
                    const filePath = isObject ? cert.filePath : null
                    const hours = isObject ? cert.hours : undefined
                    const hasFile = isObject && cert.filePath !== null

                    return (
                      <li key={index} className="flex flex-col gap-1">
                        <div className="flex items-start gap-2">
                          <span className="text-blue-600 font-bold mt-1">•</span>
                          {hasFile ? (
                            <button
                              onClick={() => handleDownload(filePath)}
                              className="text-left text-blue-600 hover:text-blue-800 hover:underline transition-colors cursor-pointer text-sm"
                              title="Clic para descargar"
                            >
                              {title}
                              <span className="ml-1 text-xs">📥</span>
                            </button>
                          ) : (
                            <span className="text-gray-700 text-sm">{title}</span>
                          )}
                        </div>
                        {hours && (
                          <span className="text-xs text-gray-500 ml-5">⏱️ {hours} horas</span>
                        )}
                      </li>
                    )
                  })}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}
