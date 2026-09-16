interface ExperienceItemProps {
  company: string
  role: string
  period: string
  technologies: string[]
  bullets?: string[]
}

const ExperienceItem = ({ company, role, period, technologies, bullets }: ExperienceItemProps) => (
  <div className="card">
    <div className="flex justify-between items-start mb-3">
      <div>
        <h3 className="text-xl font-bold text-gray-900">{role}</h3>
        <p className="text-blue-600 font-medium">{company}</p>
      </div>
      <span className="text-sm text-gray-600 bg-gray-100 px-3 py-1 rounded whitespace-nowrap">{period}</span>
    </div>
    
    {bullets && bullets.length > 0 && (
      <ul className="list-disc list-inside text-gray-700 text-sm mb-4 space-y-1">
        {bullets.slice(0, 3).map((bullet, i) => (
          <li key={i}>{bullet}</li>
        ))}
      </ul>
    )}
    
    <div className="flex flex-wrap gap-2 mt-4">
      {technologies.map((tech, i) => (
        <span key={i} className="text-xs bg-blue-100 text-blue-700 px-3 py-1 rounded-full">
          {tech}
        </span>
      ))}
    </div>
  </div>
)

interface ExperienceProps {
  items: ExperienceItemProps[]
}

export const Experience = ({ items }: ExperienceProps) => {
  // Mostrar solo las últimas 4 experiencias
  const recentItems = items.slice(0, 4)
  
  return (
    <section id="experience" aria-labelledby="experience-title" className="py-16 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 id="experience-title" className="text-3xl font-bold mb-12 text-gray-900">Experiencia Profesional</h2>
        
        <div className="space-y-6">
          {recentItems.map((item, index) => (
            <div
              key={index}
              className="animate-slideUp"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <ExperienceItem {...item} />
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
