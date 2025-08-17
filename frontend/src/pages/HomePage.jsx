import { MessageCircle, Users, Clock, Shield, Bot, Zap, Brain } from 'lucide-react'

function HomePage() {
  const openChatWidget = () => {
    // Dispatch a custom event to open the chat widget
    window.dispatchEvent(new CustomEvent('openChatWidget'));
  }

  return (
    <div className="max-w-6xl mx-auto">
      {/* Hero Section */}
      <div className="text-center py-16 px-4">
        <div className="mb-8">
          <div className="flex justify-center mb-6">
            <div className="relative">
              <MessageCircle className="h-16 w-16 text-primary-600" />
              <Bot className="h-8 w-8 text-green-600 absolute -top-2 -right-2" />
            </div>
          </div>
          <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
            Autopromtix
            <span className="text-primary-600"> AI Support</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Experience the future of customer service with our intelligent AI assistant. 
            Get instant, accurate responses powered by advanced language models and comprehensive knowledge base.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button 
              onClick={openChatWidget}
              className="btn-primary text-lg px-8 py-3"
            >
              Try AI Chat
            </button>
            <button className="btn-secondary text-lg px-8 py-3">
              Learn More
            </button>
          </div>
        </div>
      </div>

      {/* AI Features Section */}
      <div className="py-16 px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            Powered by Advanced AI
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Our AI assistant understands context, remembers conversations, and provides intelligent responses
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          <div className="text-center p-6 bg-white rounded-lg shadow-sm border">
            <Bot className="h-12 w-12 text-primary-600 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">AI Assistant</h3>
            <p className="text-gray-600">
              Intelligent chatbot powered by OpenAI's GPT models for natural conversations
            </p>
          </div>

          <div className="text-center p-6 bg-white rounded-lg shadow-sm border">
            <Brain className="h-12 w-12 text-primary-600 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Context Aware</h3>
            <p className="text-gray-600">
              Remembers conversation history and provides relevant, contextual responses
            </p>
          </div>

          <div className="text-center p-6 bg-white rounded-lg shadow-sm border">
            <Zap className="h-12 w-12 text-primary-600 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Instant Responses</h3>
            <p className="text-gray-600">
              Real-time AI responses with typing indicators for natural conversation flow
            </p>
          </div>

          <div className="text-center p-6 bg-white rounded-lg shadow-sm border">
            <Shield className="h-12 w-12 text-primary-600 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Knowledge Base</h3>
            <p className="text-gray-600">
              Access to comprehensive product information, policies, and troubleshooting guides
            </p>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="py-16 px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            Why Choose Autopromtix AI Support?
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Built with modern technology to provide the best customer experience
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          <div className="text-center p-6 bg-white rounded-lg shadow-sm border">
            <MessageCircle className="h-12 w-12 text-primary-600 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Real-time Chat</h3>
            <p className="text-gray-600">
              WebSocket-based instant messaging with AI-powered responses
            </p>
          </div>

          <div className="text-center p-6 bg-white rounded-lg shadow-sm border">
            <Users className="h-12 w-12 text-primary-600 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Multi-session Support</h3>
            <p className="text-gray-600">
              Handle multiple customer conversations simultaneously with AI assistance
            </p>
          </div>

          <div className="text-center p-6 bg-white rounded-lg shadow-sm border">
            <Clock className="h-12 w-12 text-primary-600 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">24/7 Availability</h3>
            <p className="text-gray-600">
              AI assistant available round-the-clock to help your customers
            </p>
          </div>

          <div className="text-center p-6 bg-white rounded-lg shadow-sm border">
            <Shield className="h-12 w-12 text-primary-600 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Secure & Reliable</h3>
            <p className="text-gray-600">
              Built with security best practices and reliable infrastructure
            </p>
          </div>
        </div>
      </div>

      {/* How It Works Section */}
      <div className="py-16 px-4 bg-white rounded-lg shadow-sm border">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            How Autopromtix AI Support Works
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Get instant AI assistance in just a few simple steps
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8 max-w-4xl mx-auto">
          <div className="text-center">
            <div className="bg-primary-100 text-primary-600 rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-4 font-bold text-lg">
              1
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Click Chat Widget</h3>
            <p className="text-gray-600">
              Click the floating chat widget in the bottom-right corner to start a conversation
            </p>
          </div>

          <div className="text-center">
            <div className="bg-primary-100 text-primary-600 rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-4 font-bold text-lg">
              2
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">AI Responds Instantly</h3>
            <p className="text-gray-600">
              Our AI assistant analyzes your query and provides intelligent, contextual responses
            </p>
          </div>

          <div className="text-center">
            <div className="bg-primary-100 text-primary-600 rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-4 font-bold text-lg">
              3
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Get Help Anytime</h3>
            <p className="text-gray-600">
              Get answers to your questions 24/7 with our intelligent AI assistant
            </p>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="py-16 px-4 text-center">
        <div className="bg-gradient-to-r from-primary-600 to-primary-700 rounded-lg p-12 text-white">
          <h2 className="text-3xl font-bold mb-4">
            Ready to Experience Autopromtix AI Support?
          </h2>
          <p className="text-xl mb-8 opacity-90">
            Click the chat widget and start talking to our AI assistant now!
          </p>
          <button 
            onClick={openChatWidget}
            className="bg-white text-primary-600 hover:bg-gray-100 font-medium py-3 px-8 rounded-lg transition-colors duration-200"
          >
            Start Chatting
          </button>
        </div>
      </div>
    </div>
  )
}

export default HomePage
