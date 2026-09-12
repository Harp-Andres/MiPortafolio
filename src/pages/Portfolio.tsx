import { PROJECTS } from '@/types/projects'
import { ExternalLink, Code } from 'lucide-react'

export const Portfolio = () => {
  const featuredProjects = PROJECTS.filter(p => p.type === 'featured')
  const secondaryProjects = PROJECTS.filter(p => p.type === 'secondary')

  return (
    <div className="min-h-screen bg-white pt-20">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-slate-900 to-slate-800 text-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h1 className="text-4xl md:text-5xl font-bold mb-4 animate-slideUp">
            Portfolio de Proyectos
          </h1>
          <p className="text-xl text-slate-300 animate-slideUp" style={{ animationDelay: '0.1s' }}>
            Mis proyectos profesionales como SDET Senior | QA Automation Specialist
          </p>
          <div className="mt-4 flex gap-4 animate-slideUp" style={{ animationDelay: '0.2s' }}>
            <a
              href="https://github.com/Harp-Andres"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 bg-blue-600 hover:bg-blue-700 px-6 py-3 rounded-lg font-semibold transition-colors"
            >
              <Code size={20} />
              Ver en GitHub
            </a>
          </div>
        </div>
      </section>

      {/* Featured Projects */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold mb-12 text-gray-900">Proyectos Destacados</h2>

          <div className="grid gap-8 lg:grid-cols-1">
            {featuredProjects.map((project, index) => (
              <div
                key={project.id}
                className="bg-white rounded-xl shadow-lg hover:shadow-2xl transition-all duration-300 overflow-hidden animate-slideUp"
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                <div className="md:flex">
                  {/* Content */}
                  <div className="flex-1 p-8">
                    <div className="flex items-start justify-between mb-4">
                      <div>
                        <a
                          href={project.github}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="block"
                        >
                          <h3 className="text-2xl font-bold text-blue-600 hover:text-blue-800 transition-colors mb-2">
                            {project.name}
                          </h3>
                        </a>
                        <p className="text-lg text-blue-600 font-semibold">
                          {project.description}
                        </p>
                      </div>
                      {project.type === 'featured' && (
                        <span className="ml-4 px-4 py-2 bg-yellow-100 text-yellow-800 rounded-full text-sm font-semibold whitespace-nowrap">
                          ⭐ Featured
                        </span>
                      )}
                    </div>

                    <p className="text-gray-700 mb-6 leading-relaxed">
                      {project.longDescription}
                    </p>

                    {/* Highlights */}
                    <div className="mb-6">
                      <h4 className="text-sm font-semibold text-gray-900 mb-3">
                        Características destacadas:
                      </h4>
                      <ul className="grid grid-cols-1 md:grid-cols-2 gap-2">
                        {project.highlights.map((highlight, i) => (
                          <li key={i} className="flex items-start gap-2 text-gray-700">
                            <span className="text-blue-600 font-bold mt-1">✓</span>
                            <span>{highlight}</span>
                          </li>
                        ))}
                      </ul>
                    </div>

                    {/* Technologies */}
                    <div className="mb-6">
                      <h4 className="text-sm font-semibold text-gray-900 mb-3">
                        Tecnologías:
                      </h4>
                      <div className="flex flex-wrap gap-2">
                        {project.technologies.map((tech, i) => (
                          <span
                            key={i}
                            className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium"
                          >
                            {tech}
                          </span>
                        ))}
                      </div>
                    </div>

                    {/* Visit Link */}
                    {project.link && (
                      <div className="flex gap-4">
                        <a
                          href={project.link}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="inline-flex items-center gap-2 text-green-600 hover:text-green-800 font-semibold transition-colors"
                        >
                          <ExternalLink size={20} />
                          Ver Sitio en Vivo
                        </a>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Secondary Projects */}
      {secondaryProjects.length > 0 && (
        <section className="py-16 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 className="text-3xl font-bold mb-12 text-gray-900">Otros Proyectos</h2>

            <div className="grid gap-6 md:grid-cols-2">
              {secondaryProjects.map((project, index) => (
                <div
                  key={project.id}
                  className="bg-gradient-to-br from-slate-50 to-slate-100 rounded-lg shadow hover:shadow-lg transition-all p-6 animate-slideUp"
                  style={{ animationDelay: `${index * 0.1}s` }}
                >
                  <h3 className="text-xl font-bold text-gray-900 mb-2">
                    {project.name}
                  </h3>
                  <p className="text-gray-700 mb-4">
                    {project.description}
                  </p>

                  <div className="mb-4">
                    <div className="flex flex-wrap gap-2 mb-4">
                      {project.technologies.slice(0, 3).map((tech, i) => (
                        <span
                          key={i}
                          className="px-2 py-1 bg-slate-300 text-slate-800 rounded text-xs font-medium"
                        >
                          {tech}
                        </span>
                      ))}
                      {project.technologies.length > 3 && (
                        <span className="px-2 py-1 bg-slate-300 text-slate-800 rounded text-xs font-medium">
                          +{project.technologies.length - 3}
                        </span>
                      )}
                    </div>
                  </div>

                  <a
                    href={project.github}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-2 text-blue-600 hover:text-blue-800 font-semibold transition-colors"
                  >
                    <Code size={18} />
                    Ver en GitHub
                  </a>
                </div>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* CTA Section */}
      <section className="py-16 bg-gradient-to-br from-blue-600 to-blue-800 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold mb-6">¿Interesado en Colaborar?</h2>
          <p className="text-xl text-blue-100 mb-8 max-w-2xl mx-auto">
            Tengo experiencia en SDET, QA Automation, Testing y DevOps. Siempre abierto a nuevas oportunidades.
          </p>
          <a
            href="/#sobre-mi"
            className="inline-block bg-white text-blue-600 font-semibold px-8 py-3 rounded-lg hover:bg-blue-50 transition-colors"
          >
            Contactar
          </a>
        </div>
      </section>
    </div>
  )
}
