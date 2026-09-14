import React from 'react'
import ReactDOM from 'react-dom/client'
import { initializeApiClient } from '@mportafolio/api-client'
import App from './App'
import './index.css'

// Initialize API client with base URL from environment
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
initializeApiClient(apiBaseUrl)

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
