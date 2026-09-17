import { useState, useEffect } from 'react'

export const useAge = (birthDate: string): number => {
  const [age, setAge] = useState(0)

  useEffect(() => {
    const today = new Date()
    const birth = new Date(birthDate)
    let calculatedAge = today.getFullYear() - birth.getFullYear()
    const monthDiff = today.getMonth() - birth.getMonth()

    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
      calculatedAge--
    }

    setAge(calculatedAge)
  }, [birthDate])

  return age
}

export const useScrollPosition = (): boolean => {
  const [isScrolled, setIsScrolled] = useState(false)

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 50)
    }

    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  return isScrolled
}

// Re-export API-related hooks
export { useDocuments } from './useDocuments'
export type { UseDocumentsState, UseDocumentsReturn } from './useDocuments'

export { useSync } from './useSync'
export type { UseSyncState, UseSyncReturn } from './useSync'

export { useSectionNavigation } from './useSectionNavigation'
