import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Textarea } from '@/components/ui/textarea.jsx'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Brain, Eye, Globe, Code, Search, Palette, Sparkles, Send, Settings, User, MessageSquare } from 'lucide-react'
import apiService from './services/api.js'
import './App.css'

function App() {
  const [selectedAgent, setSelectedAgent] = useState('general')
  const [userInput, setUserInput] = useState('')
  const [messages, setMessages] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [agentStatus, setAgentStatus] = useState('ready')

  const agentTypes = [
    { 
      id: 'general', 
      name: 'General Chat', 
      icon: MessageSquare, 
      description: 'Conversación general y asistencia',
      color: 'bg-blue-500',
      capabilities: ['chat', 'qa', 'general_assistance']
    },
    { 
      id: 'vision', 
      name: 'Vision Agent', 
      icon: Eye, 
      description: 'Análisis de imágenes y contenido visual',
      color: 'bg-purple-500',
      capabilities: ['image_analysis', 'ocr', 'visual_qa']
    },
    { 
      id: 'web', 
      name: 'Web Navigator', 
      icon: Globe, 
      description: 'Navegación y automatización web',
      color: 'bg-green-500',
      capabilities: ['web_scraping', 'automation', 'research']
    },
    { 
      id: 'code', 
      name: 'Code Assistant', 
      icon: Code, 
      description: 'Programación y desarrollo',
      color: 'bg-orange-500',
      capabilities: ['code_generation', 'debugging', 'review']
    },
    { 
      id: 'research', 
      name: 'Research Agent', 
      icon: Search, 
      description: 'Investigación profunda y análisis',
      color: 'bg-indigo-500',
      capabilities: ['deep_research', 'data_analysis', 'synthesis']
    },
    { 
      id: 'creative', 
      name: 'Creative Agent', 
      icon: Palette, 
      description: 'Contenido creativo y multimedia',
      color: 'bg-pink-500',
      capabilities: ['content_creation', 'design', 'storytelling']
    }
  ]

  const outputTypes = [
    { id: 'quality', name: 'Quality', icon: '⭐', color: 'bg-yellow-500' },
    { id: 'image', name: 'Image', icon: '🖼️', color: 'bg-red-500' },
    { id: 'slides', name: 'Slides', icon: '📊', color: 'bg-teal-500' },
    { id: 'webpage', name: 'Webpage', icon: '🌐', color: 'bg-blue-500' },
    { id: 'visualization', name: 'Visualization', icon: '📈', color: 'bg-green-500' },
    { id: 'playbook', name: 'Playbook', icon: '📋', color: 'bg-amber-500' },
    { id: 'video', name: 'Video', icon: '🎥', color: 'bg-purple-500' },
    { id: 'audio', name: 'Audio', icon: '🎵', color: 'bg-cyan-500' }
  ]

  const categories = [
    { id: 'recommend', name: 'Recommend', count: 24 },
    { id: 'featured', name: 'Featured', count: 18 },
    { id: 'research', name: 'Research', count: 32 },
    { id: 'data', name: 'Data', count: 28 },
    { id: 'edu', name: 'Edu', count: 15 },
    { id: 'productivity', name: 'Productivity', count: 22 },
    { id: 'programming', name: 'Programming', count: 31 }
  ]

  const selectedAgentData = agentTypes.find(agent => agent.id === selectedAgent)

  const handleSendMessage = async () => {
    if (!userInput.trim()) return

    setIsLoading(true)
    setAgentStatus('processing')

    const newMessage = {
      id: Date.now(),
      type: 'user',
      content: userInput,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, newMessage])
    setUserInput('')

    try {
      // Llamada real a la API
      const response = await apiService.sendMessage(userInput, selectedAgent, messages)
      
      const agentMessage = {
        id: Date.now() + 1,
        type: 'agent',
        content: response.response,
        agent: selectedAgent,
        timestamp: new Date(),
        metadata: response.metadata,
        model_used: response.model_used,
        capabilities_used: response.capabilities_used
      }
      setMessages(prev => [...prev, agentMessage])
      
    } catch (error) {
      console.error('Error sending message:', error)
      const errorMessage = {
        id: Date.now() + 1,
        type: 'error',
        content: `Error: ${error.message}. Verifica que el backend esté ejecutándose en http://localhost:5001`,
        timestamp: new Date()
      }
      setMessages(prev => [...prev, errorMessage])
    }

    setIsLoading(false)
    setAgentStatus('ready')
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <div className="container mx-auto p-4 max-w-7xl">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg">
              <Brain className="h-8 w-8 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-white">RALT Agent</h1>
              <p className="text-slate-300">Agente Multimodal Profesional</p>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <Badge variant="outline" className="text-green-400 border-green-400">
              {agentStatus === 'ready' ? 'Listo' : 'Procesando...'}
            </Badge>
            <Button variant="outline" size="sm">
              <Settings className="h-4 w-4" />
            </Button>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Sidebar - Agent Selection */}
          <div className="lg:col-span-1 space-y-4">
            <Card className="bg-slate-800/50 border-slate-700">
              <CardHeader>
                <CardTitle className="text-white flex items-center space-x-2">
                  <User className="h-5 w-5" />
                  <span>Seleccionar Agente</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                {agentTypes.map((agent) => {
                  const IconComponent = agent.icon
                  return (
                    <div
                      key={agent.id}
                      className={`p-3 rounded-lg cursor-pointer transition-all duration-200 ${
                        selectedAgent === agent.id
                          ? `${agent.color} text-white shadow-lg`
                          : 'bg-slate-700/50 text-slate-300 hover:bg-slate-700'
                      }`}
                      onClick={() => setSelectedAgent(agent.id)}
                    >
                      <div className="flex items-center space-x-2 mb-2">
                        <IconComponent className="h-5 w-5" />
                        <span className="font-medium">{agent.name}</span>
                      </div>
                      <p className="text-xs opacity-80">{agent.description}</p>
                      <div className="flex flex-wrap gap-1 mt-2">
                        {agent.capabilities.slice(0, 2).map((cap) => (
                          <Badge key={cap} variant="secondary" className="text-xs">
                            {cap}
                          </Badge>
                        ))}
                      </div>
                    </div>
                  )
                })}
              </CardContent>
            </Card>

            {/* Output Types */}
            <Card className="bg-slate-800/50 border-slate-700">
              <CardHeader>
                <CardTitle className="text-white text-sm">Tipos de Salida</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 gap-2">
                  {outputTypes.map((type) => (
                    <Button
                      key={type.id}
                      variant="outline"
                      size="sm"
                      className="text-xs border-slate-600 text-slate-300 hover:bg-slate-700"
                    >
                      <span className="mr-1">{type.icon}</span>
                      {type.name}
                    </Button>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Main Chat Area */}
          <div className="lg:col-span-3">
            <Card className="bg-slate-800/50 border-slate-700 h-[600px] flex flex-col">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    {selectedAgentData && (
                      <>
                        <div className={`p-2 ${selectedAgentData.color} rounded-lg`}>
                          <selectedAgentData.icon className="h-5 w-5 text-white" />
                        </div>
                        <div>
                          <CardTitle className="text-white">{selectedAgentData.name}</CardTitle>
                          <p className="text-slate-400 text-sm">{selectedAgentData.description}</p>
                        </div>
                      </>
                    )}
                  </div>
                  <Badge variant="outline" className="text-blue-400 border-blue-400">
                    {messages.length} mensajes
                  </Badge>
                </div>
              </CardHeader>

              {/* Messages Area */}
              <CardContent className="flex-1 overflow-y-auto space-y-4">
                {messages.length === 0 ? (
                  <div className="flex items-center justify-center h-full">
                    <div className="text-center">
                      <Sparkles className="h-12 w-12 text-purple-400 mx-auto mb-4" />
                      <h3 className="text-xl font-semibold text-white mb-2">
                        ¡Hola! Soy tu agente RALT
                      </h3>
                      <p className="text-slate-400">
                        Selecciona un agente y comienza a chatear. Puedo ayudarte con tareas multimodales.
                      </p>
                    </div>
                  </div>
                ) : (
                  messages.map((message) => (
                    <div
                      key={message.id}
                      className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                      <div
                        className={`max-w-[80%] p-3 rounded-lg ${
                          message.type === 'user'
                            ? 'bg-blue-600 text-white'
                            : message.type === 'error'
                            ? 'bg-red-600/20 text-red-300 border border-red-600/30'
                            : 'bg-slate-700 text-slate-100'
                        }`}
                      >
                        <p className="whitespace-pre-wrap">{message.content}</p>
                        <p className="text-xs opacity-70 mt-1">
                          {message.timestamp.toLocaleTimeString()}
                        </p>
                      </div>
                    </div>
                  ))
                )}
                {isLoading && (
                  <div className="flex justify-start">
                    <div className="bg-slate-700 text-slate-100 p-3 rounded-lg">
                      <div className="flex items-center space-x-2">
                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-purple-400"></div>
                        <span>Procesando...</span>
                      </div>
                    </div>
                  </div>
                )}
              </CardContent>

              {/* Input Area */}
              <div className="p-4 border-t border-slate-700">
                <div className="flex space-x-2">
                  <Textarea
                    value={userInput}
                    onChange={(e) => setUserInput(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Escribe tu mensaje aquí..."
                    className="flex-1 bg-slate-700 border-slate-600 text-white placeholder-slate-400 resize-none"
                    rows={2}
                  />
                  <Button
                    onClick={handleSendMessage}
                    disabled={!userInput.trim() || isLoading}
                    className="bg-purple-600 hover:bg-purple-700"
                  >
                    <Send className="h-4 w-4" />
                  </Button>
                </div>
                <div className="flex flex-wrap gap-1 mt-2">
                  {categories.map((category) => (
                    <Badge
                      key={category.id}
                      variant="outline"
                      className="text-xs cursor-pointer border-slate-600 text-slate-400 hover:bg-slate-700"
                    >
                      {category.name} {category.count}
                    </Badge>
                  ))}
                </div>
              </div>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App

