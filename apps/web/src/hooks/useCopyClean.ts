import { useEffect } from 'react'

/**
 * Hook que limpia el texto cuando se copia desde la página
 * Remueve caracteres especiales y espacios extras
 */
export const useCopyClean = () => {
  useEffect(() => {
    const handleCopy = (e: ClipboardEvent) => {
      const selectedText = window.getSelection()?.toString() || ''
      
      // Limpiar el texto copiado
      const cleanText = selectedText
        .replace(/[\u200B-\u200D\uFEFF]/g, '') // Remover caracteres invisibles (zero-width)
        .trim()
      
      if (cleanText && cleanText !== selectedText) {
        e.preventDefault()
        e.clipboardData?.setData('text/plain', cleanText)
      }
    }

    document.addEventListener('copy', handleCopy)
    return () => document.removeEventListener('copy', handleCopy)
  }, [])
}
