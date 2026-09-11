interface CertificatesProps {
  items: string[]
  microsoftStudies?: string[]
}

export const Certificates = ({ items, microsoftStudies = [] }: CertificatesProps) => {
  return (
    <section id="certificates" className="py-16 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="text-3xl font-bold mb-12 text-gray-900">Certificaciones & Formación</h2>
        
        <div className="grid md:grid-cols-2 gap-6">
          {/* Certificaciones */}
          <div className="card">
            <h3 className="text-2xl font-bold mb-6 text-blue-600">Certificaciones Profesionales</h3>
            <ul className="space-y-3">
              {items.map((cert, index) => (
                <li key={index} className="flex items-start gap-3">
                  <span className="w-2 h-2 bg-blue-600 rounded-full mt-2 flex-shrink-0" />
                  <span className="text-gray-700">{cert}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Microsoft Studies */}
          {microsoftStudies.length > 0 && (
            <div className="card">
              <h3 className="text-2xl font-bold mb-6 text-blue-600">Capacitación Microsoft</h3>
              <ul className="space-y-3">
                {microsoftStudies.map((study, index) => (
                  <li key={index} className="flex items-start gap-3">
                    <span className="w-2 h-2 bg-green-600 rounded-full mt-2 flex-shrink-0" />
                    <span className="text-gray-700">{study}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    </section>
  )
}
