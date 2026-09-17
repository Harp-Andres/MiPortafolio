import { useCallback } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'

/**
 * Navigates to an in-page section by id. Works both when already on the
 * home route (scrolls directly) and from any other route (navigates home
 * first, then Home.tsx scrolls once mounted using the navigation state).
 */
export const useSectionNavigation = () => {
  const location = useLocation()
  const navigate = useNavigate()

  const goToSection = useCallback(
    (sectionId: string) => (event: React.MouseEvent) => {
      event.preventDefault()
      if (location.pathname === '/') {
        document.getElementById(sectionId)?.scrollIntoView({ behavior: 'smooth' })
      } else {
        navigate('/', { state: { scrollTo: sectionId } })
      }
    },
    [location.pathname, navigate]
  )

  return { goToSection }
}
