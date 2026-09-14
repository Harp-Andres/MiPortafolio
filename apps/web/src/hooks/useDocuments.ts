/**
 * useDocuments Hook
 *
 * Manages document generation and download state
 * Handles loading, error, and success states for DOCX, PDF, and Excel formats
 */

import { useState, useCallback } from 'react'
import { getApiClient } from '@mportafolio/api-client'
import type { CVData, DocumentFormat } from '@mportafolio/api-client'

export interface UseDocumentsState {
  isLoading: boolean
  error: string | null
  success: boolean
  lastFileName: string | null
}

export interface UseDocumentsReturn extends UseDocumentsState {
  downloadDocx: (cvData: CVData, filename?: string) => Promise<void>
  downloadPdf: (cvData: CVData, filename?: string) => Promise<void>
  downloadExcel: (cvData: CVData, filename?: string) => Promise<void>
  resetState: () => void
}

/**
 * Hook that manages document download state
 *
 * @example
 * const { isLoading, error, success, downloadDocx } = useDocuments()
 *
 * const handleDownload = async () => {
 *   try {
 *     await downloadDocx(cvData)
 *   } catch (err) {
 *     console.error('Download failed:', err)
 *   }
 * }
 */
export const useDocuments = (): UseDocumentsReturn => {
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState(false)
  const [lastFileName, setLastFileName] = useState<string | null>(null)

  const resetState = useCallback(() => {
    setIsLoading(false)
    setError(null)
    setSuccess(false)
    setLastFileName(null)
  }, [])

  const handleDownload = useCallback(
    async (format: DocumentFormat, cvData: CVData, filename?: string) => {
      resetState()
      setIsLoading(true)

      try {
        const client = getApiClient()
        const response = await client.generateDocument(format, cvData)

        if (response.error) {
          throw new Error(response.error.message || 'Failed to generate document')
        }

        if (!response.data || !(response.data instanceof Blob)) {
          throw new Error('Invalid response format')
        }

        // Determine filename
        const fileExtensions: Record<string, string> = {
          docx: 'CV.docx',
          pdf: 'CV.pdf',
          excel: 'CV.xlsx',
        }
        const finalFilename = filename || fileExtensions[format] || 'document'

        // Trigger download
        const url = window.URL.createObjectURL(response.data)
        const link = document.createElement('a')
        link.href = url
        link.download = finalFilename
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        window.URL.revokeObjectURL(url)

        setLastFileName(finalFilename)
        setSuccess(true)
      } catch (err) {
        const errorMessage = err instanceof Error ? err.message : 'Unknown error occurred'
        setError(errorMessage)
        setSuccess(false)
      } finally {
        setIsLoading(false)
      }
    },
    [resetState]
  )

  const downloadDocx = useCallback(
    (cvData: CVData, filename?: string) => handleDownload('docx', cvData, filename),
    [handleDownload]
  )

  const downloadPdf = useCallback(
    (cvData: CVData, filename?: string) => handleDownload('pdf', cvData, filename),
    [handleDownload]
  )

  const downloadExcel = useCallback(
    (cvData: CVData, filename?: string) => handleDownload('excel', cvData, filename),
    [handleDownload]
  )

  return {
    isLoading,
    error,
    success,
    lastFileName,
    downloadDocx,
    downloadPdf,
    downloadExcel,
    resetState,
  }
}
