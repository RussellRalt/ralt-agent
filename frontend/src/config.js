// Configuración de la aplicación
export const config = {
  // URL base de la API
  API_BASE_URL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:5001',
  
  // Configuración de desarrollo
  isDevelopment: import.meta.env.DEV,
  
  // Configuración de agentes
  DEFAULT_AGENT: 'general',
  
  // Configuración de UI
  THEME: {
    primary: '#8B5CF6',
    secondary: '#EC4899',
    background: '#0F172A',
    surface: '#1E293B'
  }
}

export default config

