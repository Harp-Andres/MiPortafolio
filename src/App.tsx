import { useState } from 'react'
import { HashRouter, Routes, Route } from 'react-router-dom'
import { Navigation, Footer } from './components'
import { Home, Portfolio } from './pages'
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
    <HashRouter>
      <div className="min-h-screen bg-white">
        <Navigation onDownloadATS={handleDownloadATS} onDownloadVisual={handleDownloadVisual} />
        
        <Routes>
          <Route path="/" element={<Home onDownloadATS={handleDownloadATS} onDownloadVisual={handleDownloadVisual} />} />
          <Route path="/portafolio" element={<Portfolio />} />
        </Routes>

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
    </HashRouter>
  )
}

export default App
