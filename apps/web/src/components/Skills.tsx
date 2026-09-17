interface SkillCategoryProps {
  category: string
  items: string
}

const SkillCard = ({ category, items }: SkillCategoryProps) => {
  // Parsear items separados por comas
  const skillsList = items.split(',').map(item => item.trim())
  
  return (
    <div className="h-80 border-2 border-blue-200 rounded-lg p-6 bg-gradient-to-br from-blue-50 to-white hover:shadow-lg transition-shadow duration-300 flex flex-col">
      <h4 className="text-lg font-bold mb-4 text-blue-700 flex-shrink-0">{category}</h4>
      <div className="space-y-2 flex-1 overflow-y-auto scrollbar-hide">
        {skillsList.map((item, i) => (
          <p key={i} className="text-gray-700 flex items-start gap-2 text-sm leading-tight">
            <span className="text-blue-600 font-bold mt-1 flex-shrink-0">▸</span>
            <span>{item}</span>
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
  // Organizar categorías: primero las más grandes
  const sortedCategories = [...categories].sort((a, b) => {
    const aCount = a.items.split(',').length
    const bCount = b.items.split(',').length
    return bCount - aCount
  })

  return (
    <section id="skills" aria-labelledby="skills-title" className="py-16 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 id="skills-title" className="text-3xl font-bold mb-12 text-gray-900">Habilidades Profesionales</h2>
        
        {/* Responsive Grid: 1 col móvil (360px), 2 col tablet (768px), 3 col desktop (1024px+) */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 auto-rows-fr">
          {sortedCategories.map((category, index) => (
            <div
              key={index}
              className="animate-slideUp"
              style={{ animationDelay: `${index * 0.05}s` }}
            >
              <SkillCard {...category} />
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
