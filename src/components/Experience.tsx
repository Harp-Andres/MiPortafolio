interface ExperienceItemProps {
  position: string
  company: string
  duration: string
  technologies: string[]
}

const ExperienceItem = ({ position, company, duration, technologies }: ExperienceItemProps) => (
  <div className="card">
    <div className="flex justify-between items-start mb-2">
      <div>
        <h3 className="text-xl font-bold text-gray-900">{position}</h3>
        <p className="text-blue-600 font-medium">{company}</p>
      </div>
      <span className="text-sm text-gray-600 bg-gray-100 px-3 py-1 rounded">{duration}</span>
    </div>
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
  return (
    <section id="experience" className="py-16 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="text-3xl font-bold mb-12 text-gray-900">Experiencia Profesional</h2>
        
        <div className="space-y-6">
          {items.map((item, index) => (
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
