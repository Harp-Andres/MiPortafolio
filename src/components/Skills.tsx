interface SkillBarProps {
  name: string
  level: number
}

const SkillBar = ({ name, level }: SkillBarProps) => {
  return (
    <div className="mb-6">
      <div className="flex justify-between mb-2">
        <span className="font-medium text-gray-900">{name}</span>
        <span className="text-sm text-gray-600">{level}/10</span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-2">
        <div
          className="bg-blue-600 h-2 rounded-full transition-all duration-500"
          style={{ width: `${level * 10}%` }}
        />
      </div>
    </div>
  )
}

interface SkillsProps {
  categories: Array<{
    category: string
    items: string[]
  }>
}

export const Skills = ({ categories }: SkillsProps) => {
  const skillsWithLevels = [
    { name: 'Diseño Casos De Prueba', level: 10 },
    { name: 'Selenium', level: 7 },
    { name: 'Cucumber', level: 9 },
    { name: 'Playwright', level: 8 },
    { name: 'Java', level: 7 },
    { name: 'Python', level: 8 },
    { name: 'JavaScript/TypeScript', level: 8 },
    { name: 'Postman', level: 8 },
  ]

  return (
    <section id="skills" className="py-16 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="text-3xl font-bold mb-12 text-gray-900">Habilidades Profesionales</h2>
        
        <div className="grid md:grid-cols-2 gap-8">
          {skillsWithLevels.map((skill, index) => (
            <div
              key={index}
              className="card animate-slideUp"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <SkillBar name={skill.name} level={skill.level} />
            </div>
          ))}
        </div>

        {/* Tech Categories */}
        <div className="mt-12">
          <h3 className="text-2xl font-bold mb-8 text-gray-900">Tecnologías por Categoría</h3>
          <div className="grid md:grid-cols-3 gap-6">
            {categories.map((category, index) => (
              <div key={index} className="card animate-slideUp" style={{ animationDelay: `${index * 0.1}s` }}>
                <h4 className="text-xl font-bold mb-4 text-blue-600">{category.category}</h4>
                <div className="space-y-2">
                  {category.items.map((item, i) => (
                    <p key={i} className="text-gray-600 flex items-center gap-2">
                      <span className="w-2 h-2 bg-blue-600 rounded-full" />
                      {item}
                    </p>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}
