import { useState } from 'react'
import { Download, X } from 'lucide-react'

interface CVDownloadsProps {
  onDownloadATS: () => void
  onDownloadVisual: () => void
  isLoading?: boolean
}

export const CVDownloads = ({ onDownloadATS, onDownloadVisual, isLoading = false }: CVDownloadsProps) => {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <>
      {/* Botón para abrir modal */}
      <button
        onClick={() => setIsOpen(true)}
        className="flex items-center gap-2 px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors"
      >
        <Download size={18} />
        Hoja de Vida Descargable
      </button>

      {/* Modal */}
      {isOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-8 max-w-lg w-full mx-4">
            {/* Header */}
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-2xl font-bold text-gray-900">Descargar Hoja de Vida</h3>
              <button
                onClick={() => setIsOpen(false)}
                disabled={isLoading}
                className="text-gray-500 hover:text-gray-900 disabled:opacity-50"
              >
                <X size={24} />
              </button>
            </div>

            {/* Descripción */}
            <p className="text-gray-600 mb-6">
              Selecciona el formato que prefieres para descargar tu hoja de vida:
            </p>

            {/* Opciones de descarga lado a lado */}
            <div className="grid grid-cols-2 gap-4">
              {/* Opción ATS */}
              <button
                onClick={() => {
                  onDownloadATS()
                  setIsOpen(false)
                }}
                disabled={isLoading}
                className="flex flex-col items-center gap-3 p-4 border-2 border-blue-600 rounded-lg hover:bg-blue-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <Download className="text-blue-600" size={32} />
                <div className="text-center">
                  <p className="font-bold text-gray-900">[ATS]</p>
                  <p className="text-sm text-gray-600">Formato optimizado</p>
                  <p className="text-xs text-gray-500">para sistemas ATS</p>
                </div>
              </button>

              {/* Opción Visual */}
              <button
                onClick={() => {
                  onDownloadVisual()
                  setIsOpen(false)
                }}
                disabled={isLoading}
                className="flex flex-col items-center gap-3 p-4 border-2 border-purple-600 rounded-lg hover:bg-purple-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <Download className="text-purple-600" size={32} />
                <div className="text-center">
                  <p className="font-bold text-gray-900">[Visual]</p>
                  <p className="text-sm text-gray-600">Diseño elegante</p>
                  <p className="text-xs text-gray-500">con colores y formato</p>
                </div>
              </button>
            </div>

            {/* Footer */}
            <p className="text-xs text-gray-500 mt-6 text-center">
              Los archivos se descargarán en formato PDF
            </p>
          </div>
        </div>
      )}
    </>
  )
}
