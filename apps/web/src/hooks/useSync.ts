/**
 * useSync Hook
 *
 * Verifies CV data synchronization across all document formats
 * Polls for sync verification with configurable interval
 */

import { useState, useCallback, useEffect } from 'react'
import { getApiClient } from '@mportafolio/api-client'
import type { CVData, SyncVerifyResponse } from '@mportafolio/api-client'

export interface UseSyncState {
  report: SyncVerifyResponse | null
  isLoading: boolean
  error: string | null
  isVerified: boolean
}

export interface UseSyncReturn extends UseSyncState {
  verify: () => Promise<void>
  reset: () => void
}

/**
 * Hook that verifies CV data synchronization
 *
 * @param cvData - CV data to verify
 * @param pollInterval - Optional polling interval in milliseconds (default: no polling)
 *
 * @example
 * const { report, isLoading, error, isVerified, verify } = useSync(cvData)
 *
 * useEffect(() => {
 *   verify()
 * }, [verify])
 */
export const useSync = (cvData?: CVData, pollInterval?: number): UseSyncReturn => {
  const [report, setReport] = useState<SyncVerifyResponse | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [isVerified, setIsVerified] = useState(false)

  const reset = useCallback(() => {
    setReport(null)
    setIsLoading(false)
    setError(null)
    setIsVerified(false)
  }, [])

  const verify = useCallback(async () => {
    if (!cvData) {
      setError('CV data is required for synchronization verification')
      return
    }

    setIsLoading(true)
    setError(null)

    try {
      const client = getApiClient()
      const response = await client.verifySynchronization(cvData)

      if (response.error) {
        throw new Error(response.error.message || 'Synchronization verification failed')
      }

      if (!response.data) {
        throw new Error('Invalid response format')
      }

      setReport(response.data)

      // Check if all formats are synchronized
      const syncReport = response.data.sync_report
      const allFormatsSynced =
        syncReport.matched_formats.length >= 3 && syncReport.mismatches.length === 0

      setIsVerified(allFormatsSynced)
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error occurred'
      setError(errorMessage)
      setIsVerified(false)
    } finally {
      setIsLoading(false)
    }
  }, [cvData])

  // Poll for sync verification if interval is provided
  useEffect(() => {
    if (!pollInterval || !cvData) {
      return
    }

    const intervalId = setInterval(() => {
      verify()
    }, pollInterval)

    return () => clearInterval(intervalId)
  }, [cvData, pollInterval, verify])

  return {
    report,
    isLoading,
    error,
    isVerified,
    verify,
    reset,
  }
}
