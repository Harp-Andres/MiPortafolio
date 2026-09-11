interface SkillCategoryProps {
  category: string
  items: string
}

const SkillCategory = ({ category, items }: SkillCategoryProps) => {
  // Parsear items separados por comas
  const skillsList = items.split(',').map(item => item.trim())
  
  return (
    <div className="card">
      <h4 className="text-lg font-bold mb-4 text-blue-600">{category}</h4>
      <div className="space-y-2">
        {skillsList.map((item, i) => (
          <p key={i} className="text-gray-700 flex items-center gap-2">
            <span className="w-2 h-2 bg-blue-600 rounded-full flex-shrink-0" />
            {item}
          </p>
        ))}
      </div>
    </div>
  )
}

interface SkillsProps {
  categories: Array<{
    category: string
    items: string
  }>
}

export const Skills = ({ categories }: SkillsProps) => {
  return (
    <section id="skills" className="py-16 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="text-3xl font-bold mb-12 text-gray-900">Habilidades Profesionales</h2>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {categories.map((category, index) => (
            <div
              key={index}
              className="animate-slideUp"
              style={{ animationDelay: `${index * 0.05}s` }}
            >
              <SkillCategory {...category} />
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
