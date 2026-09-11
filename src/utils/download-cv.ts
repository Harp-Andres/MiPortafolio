/**
 * Utilidad para descargar el CV en diferentes formatos
 * Integra con el generador de HV centralizado
 */

interface DownloadOptions {
  format: 'ats' | 'visual'
}

export const downloadCV = async (format: 'ats' | 'visual'): Promise<void> => {
  try {
    // Rutas a los PDFs generados
    const cvPath = format === 'ats' 
      ? '/cv/HV_2026_2_ATS_AndesRodriguez.pdf'
      : '/cv/HV_2026_2_Visual_AndresRodriguez.pdf'

    const filename = format === 'ats'
      ? 'HV_2026_ATS_AndesRodriguez.pdf'
      : 'HV_2026_Visual_AndresRodriguez.pdf'

    // Crear elemento de descarga
    const link = document.createElement('a')
    link.href = cvPath
    link.download = filename
    link.target = '_blank'
    
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)

    console.log(`CV ${format} descargado exitosamente`)
  } catch (error) {
    console.error('Error descargando CV:', error)
    throw new Error(`No se pudo descargar el CV en formato ${format}`)
  }
}

/**
 * Genera el CV en el servidor (llamar desde backend si es necesario)
 */
export const generateCV = async (options: DownloadOptions): Promise<Blob> => {
  try {
    const response = await fetch('/api/generate-cv', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(options),
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    return await response.blob()
  } catch (error) {
    console.error('Error generando CV:', error)
    throw error
  }
}
