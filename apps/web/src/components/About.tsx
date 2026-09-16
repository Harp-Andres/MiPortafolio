import { Mail, Phone, MapPin, Briefcase } from 'lucide-react'
import { useAge } from '../hooks'

interface AboutProps {
  email: string
  phone: string
  location: string
  linkedin: string
  birthDate: string
  about: string
}

export const About = ({ email, phone, location, linkedin, birthDate, about }: AboutProps) => {
  const age = useAge(birthDate)

  return (
    <section id="about" aria-labelledby="about-title" className="py-16 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid md:grid-cols-2 gap-12 items-center">
          
          {/* About Text */}
          <div className="animate-slideUp">
            <h2 id="about-title" className="text-3xl font-bold mb-6 text-gray-900">Sobre Mí</h2>
            <p className="text-gray-600 text-lg leading-relaxed mb-8">
              {about}
            </p>
          </div>

          {/* Contact Info */}
          <div className="card animate-slideUp" style={{ animationDelay: '0.2s' }}>
            <h3 className="text-2xl font-bold mb-6 text-gray-900">Información de Contacto</h3>
            <div className="space-y-4">
              <div className="flex items-center gap-4">
                <div className="flex items-center justify-center w-12 h-12 bg-blue-100 rounded-lg">
                  <Mail size={24} className="text-blue-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-500">Correo</p>
                  <a href={`mailto:${email}`} className="text-gray-900 font-medium hover:text-blue-600 transition-colors">
                    {email}
                  </a>
                </div>
              </div>

              <div className="flex items-center gap-4">
                <div className="flex items-center justify-center w-12 h-12 bg-blue-100 rounded-lg">
                  <Phone size={24} className="text-blue-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-500">Teléfono</p>
                  <p className="text-gray-900 font-medium">{phone}</p>
                </div>
              </div>

              <div className="flex items-center gap-4">
                <div className="flex items-center justify-center w-12 h-12 bg-blue-100 rounded-lg">
                  <MapPin size={24} className="text-blue-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-500">Ubicación</p>
                  <p className="text-gray-900 font-medium">{location}</p>
                </div>
              </div>

              <div className="flex items-center gap-4">
                <div className="flex items-center justify-center w-12 h-12 bg-blue-100 rounded-lg">
                  <Briefcase size={24} className="text-blue-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-500">LinkedIn</p>
                  <a 
                    href={linkedin} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="text-blue-600 font-medium hover:underline transition-colors"
                  >
                    Ver perfil
                  </a>
                </div>
              </div>

              <div className="pt-4 border-t">
                <p className="text-sm text-gray-500">Edad</p>
                <p className="text-2xl font-bold text-gray-900">{age} años</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
