import config from '../config.js'

class ApiService {
  constructor() {
    this.baseURL = config.API_BASE_URL
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`
    
    const defaultOptions = {
      headers: {
        'Content-Type': 'application/json',
      },
    }

    const mergedOptions = {
      ...defaultOptions,
      ...options,
      headers: {
        ...defaultOptions.headers,
        ...options.headers,
      },
    }

    try {
      const response = await fetch(url, mergedOptions)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error('API request failed:', error)
      throw error
    }
  }

  // Métodos específicos de la API
  async sendMessage(message, agentType, context = []) {
    return this.request('/api/chat', {
      method: 'POST',
      body: JSON.stringify({
        message,
        agent_type: agentType,
        context
      })
    })
  }

  async getAgents() {
    return this.request('/api/agents')
  }

  async getAgentCapabilities(agentType) {
    return this.request(`/api/agent/${agentType}/capabilities`)
  }

  async getStatus() {
    return this.request('/api/status')
  }

  async healthCheck() {
    return this.request('/api/health')
  }
}

export default new ApiService()

