interface EducationItemProps {
  degree: string
  institution: string
  year: string
}

const EducationItem = ({ degree, institution, year }: EducationItemProps) => (
  <div className="card">
    <div className="flex justify-between items-start">
      <div>
        <h3 className="text-xl font-bold text-gray-900">{degree}</h3>
        <p className="text-blue-600 font-medium">{institution}</p>
      </div>
      <span className="text-sm text-gray-600 bg-gray-100 px-3 py-1 rounded">{year}</span>
    </div>
  </div>
)

interface EducationProps {
  items: EducationItemProps[]
}

export const Education = ({ items }: EducationProps) => {
  return (
    <section id="education" className="py-16 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="text-3xl font-bold mb-12 text-gray-900">Educación</h2>
        
        <div className="grid md:grid-cols-2 gap-6">
          {items.map((item, index) => (
            <div
              key={index}
              className="animate-slideUp"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <EducationItem {...item} />
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
