import { useState } from 'react'
import {
  Navigation,
  Hero,
  About,
  Skills,
  Experience,
  Education,
  Certificates,
  Footer,
} from './components'
import { CV_DATA } from './utils/cv-data'
import { downloadCV } from './utils/download-cv'

function App() {
  const [isLoading, setIsLoading] = useState(false)

  const handleDownloadATS = async () => {
    setIsLoading(true)
    try {
      await downloadCV('ats')
    } finally {
      setIsLoading(false)
    }
  }

  const handleDownloadVisual = async () => {
    setIsLoading(true)
    try {
      await downloadCV('visual')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-white">
      <Navigation onDownloadATS={handleDownloadATS} onDownloadVisual={handleDownloadVisual} />
      
      <main>
        <Hero name={CV_DATA.name} title={CV_DATA.title} />
        <About
          email={CV_DATA.email}
          phone={`${CV_DATA.phone1} - ${CV_DATA.phone2}`}
          location={CV_DATA.location}
          linkedin={CV_DATA.linkedin}
          birthDate={CV_DATA.birthDate}
          about={CV_DATA.profile}
        />
        <Skills categories={CV_DATA.skills} />
        <Experience items={CV_DATA.experience} />
        <Education items={CV_DATA.education} />
        <Certificates 
          byCategory={CV_DATA.certificatesByCategory}
          officialCertifications={CV_DATA.officialCertifications}
          items={CV_DATA.certificates} 
          microsoftStudies={CV_DATA.microsoftStudies} 
        />
      </main>

      <Footer />

      {isLoading && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-8">
            <div className="animate-spin w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full mx-auto"></div>
            <p className="mt-4 text-gray-900 font-medium text-center">
              Descargando CV...
            </p>
          </div>
        </div>
      )}
    </div>
  )
}

export default App
