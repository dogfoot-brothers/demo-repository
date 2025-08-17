import { useState, useEffect } from 'react'
import { MessageCircle, X, Minimize2, Send, Bot } from 'lucide-react'

function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false)
  const [isMinimized, setIsMinimized] = useState(false)
  const [customerName, setCustomerName] = useState('')
  const [sessionId, setSessionId] = useState(null)
  const [messages, setMessages] = useState([])
  const [newMessage, setNewMessage] = useState('')
  const [ws, setWs] = useState(null)
  const [isAiTyping, setIsAiTyping] = useState(false)

  // Listen for custom event to open chat widget
  useEffect(() => {
    const handleOpenChatWidget = () => {
      setIsOpen(true)
      setIsMinimized(false)
    }

    window.addEventListener('openChatWidget', handleOpenChatWidget)

    return () => {
      window.removeEventListener('openChatWidget', handleOpenChatWidget)
    }
  }, [])

  const startChat = async () => {
    if (!customerName.trim()) return
    
    try {
      const response = await fetch('/api/chat/session', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ customer_name: customerName }),
      })
      
      if (response.ok) {
        const session = await response.json()
        setSessionId(session.session_id)
        setIsOpen(true)
        setIsMinimized(false)
        
        // Connect to WebSocket using the proxy
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
        const host = window.location.host
        const websocket = new WebSocket(`${protocol}//${host}/ws/chat/${session.session_id}`)
        
        websocket.onopen = () => {
          console.log('WebSocket connected')
        }
        
        websocket.onmessage = (event) => {
          const message = JSON.parse(event.data)
          
          // Only add messages from the server (AI responses), not echoed user messages
          if (message.sender === 'agent') {
            setMessages(prev => [...prev, message])
            setIsAiTyping(false)
          }
        }
        
        websocket.onclose = () => {
          console.log('WebSocket disconnected')
        }
        
        websocket.onerror = (error) => {
          console.error('WebSocket error:', error)
        }
        
        setWs(websocket)
      }
    } catch (error) {
      console.error('Error starting chat:', error)
    }
  }

  const sendMessage = () => {
    if (!newMessage.trim() || !ws) return
    
    const messageData = {
      message: newMessage,
      sender: 'customer'
    }
    
    // Add user message to local state immediately
    const userMessage = {
      message: newMessage,
      sender: 'customer',
      timestamp: new Date().toISOString()
    }
    setMessages(prev => [...prev, userMessage])
    
    // Send message to WebSocket
    ws.send(JSON.stringify(messageData))
    setNewMessage('')
    setIsAiTyping(true) // Show typing indicator when customer sends message
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  useEffect(() => {
    return () => {
      if (ws) {
        ws.close()
      }
    }
  }, [ws])

  if (!isOpen) {
    return (
      <div className="fixed bottom-4 right-4 z-50">
        <button
          onClick={() => setIsOpen(true)}
          className="bg-primary-600 hover:bg-primary-700 text-white p-4 rounded-full shadow-lg transition-all duration-200 hover:scale-110"
        >
          <MessageCircle className="h-6 w-6" />
        </button>
      </div>
    )
  }

  if (isMinimized) {
    return (
      <div className="fixed bottom-4 right-4 z-50">
        <div className="bg-white rounded-lg shadow-lg border p-3">
          <div className="flex items-center space-x-3">
            <div className="flex-1">
              <p className="text-sm font-medium text-gray-900">Chat with AI Support</p>
              <p className="text-xs text-gray-500">Click to expand</p>
            </div>
            <button
              onClick={() => setIsMinimized(false)}
              className="text-gray-400 hover:text-gray-600"
            >
              <Minimize2 className="h-4 w-4" />
            </button>
            <button
              onClick={() => setIsOpen(false)}
              className="text-gray-400 hover:text-gray-600"
            >
              <X className="h-4 w-4" />
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="fixed bottom-4 right-4 z-50 w-80 bg-white rounded-lg shadow-xl border">
      {/* Header */}
      <div className="bg-primary-600 text-white p-4 rounded-t-lg">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Bot className="h-5 w-5" />
            <span className="font-medium">AI Support</span>
          </div>
          <div className="flex items-center space-x-2">
            <button
              onClick={() => setIsMinimized(true)}
              className="text-white hover:text-gray-200 transition-colors"
            >
              <Minimize2 className="h-4 w-4" />
            </button>
            <button
              onClick={() => setIsOpen(false)}
              className="text-white hover:text-gray-200 transition-colors"
            >
              <X className="h-4 w-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Chat Area */}
      <div className="h-80 flex flex-col">
        {!sessionId ? (
          // Initial setup
          <div className="flex-1 p-4">
            <div className="text-center">
              <Bot className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">Start a conversation</h3>
              <p className="text-gray-600 mb-4">Our AI assistant is here to help! Enter your name to begin.</p>
              <input
                type="text"
                placeholder="Your name"
                value={customerName}
                onChange={(e) => setCustomerName(e.target.value)}
                className="input-field mb-4"
                onKeyPress={(e) => e.key === 'Enter' && startChat()}
              />
              <button
                onClick={startChat}
                disabled={!customerName.trim()}
                className="btn-primary w-full disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Start Chat
              </button>
            </div>
          </div>
        ) : (
          // Chat interface
          <>
            <div className="flex-1 p-4 overflow-y-auto space-y-3">
              {messages.length === 0 ? (
                <div className="text-center text-gray-500">
                  <p>Welcome! How can I help you today?</p>
                </div>
              ) : (
                messages.map((message, index) => (
                  <div
                    key={index}
                    className={`flex ${message.sender === 'customer' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`chat-bubble ${
                        message.sender === 'customer' ? 'chat-bubble-user' : 'chat-bubble-agent'
                      }`}
                    >
                      <div className="flex items-center space-x-2 mb-1">
                        {message.sender === 'agent' && <Bot className="h-3 w-3" />}
                        <span className="text-xs opacity-75">
                          {message.sender === 'agent' ? 'AI Assistant' : 'You'}
                        </span>
                      </div>
                      {message.message}
                    </div>
                  </div>
                ))
              )}
              
              {/* AI Typing Indicator */}
              {isAiTyping && (
                <div className="flex justify-start">
                  <div className="chat-bubble chat-bubble-agent">
                    <div className="flex items-center space-x-2 mb-1">
                      <Bot className="h-3 w-3" />
                      <span className="text-xs opacity-75">AI Assistant</span>
                    </div>
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                    </div>
                  </div>
                </div>
              )}
            </div>
            
            {/* Message Input */}
            <div className="p-4 border-t">
              <div className="flex space-x-2">
                <input
                  type="text"
                  placeholder="Type your message..."
                  value={newMessage}
                  onChange={(e) => setNewMessage(e.target.value)}
                  onKeyPress={handleKeyPress}
                  className="flex-1 input-field"
                  disabled={isAiTyping}
                />
                <button
                  onClick={sendMessage}
                  disabled={!newMessage.trim() || isAiTyping}
                  className="bg-primary-600 hover:bg-primary-700 text-white p-2 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  <Send className="h-4 w-4" />
                </button>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  )
}

export default ChatWidget
