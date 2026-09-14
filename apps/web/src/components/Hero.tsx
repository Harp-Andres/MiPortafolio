interface HeroProps {
  name: string
  title: string
}

export const Hero = ({ name, title }: HeroProps) => {
  return (
    <div className="pt-24 pb-12 bg-gradient-to-br from-gray-50 to-gray-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center py-12 animate-slideUp">
          <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-4">
            {name}
          </h1>
          <h2 className="text-xl md:text-3xl text-blue-600 font-semibold mb-8">
            {title}
          </h2>
          <p className="text-gray-600 text-lg max-w-2xl mx-auto">
            Ingeniero de Calidad de Software especializado en Automatización de Pruebas
            con más de 8 años de experiencia
          </p>
        </div>
      </div>
    </div>
  )
}
