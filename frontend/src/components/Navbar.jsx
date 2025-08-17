import { MessageCircle, Home, Bot } from 'lucide-react'

function Navbar() {
  return (
    <nav className="bg-white shadow-sm border-b">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center space-x-2">
            <MessageCircle className="h-8 w-8 text-primary-600" />
            <Bot className="h-6 w-6 text-green-600" />
            <span className="text-xl font-bold text-gray-900">Autopromtix</span>
          </div>
          
          <div className="flex items-center space-x-6">
            <div className="flex items-center space-x-1 text-gray-600">
              <Home className="h-4 w-4" />
              <span>Home</span>
            </div>
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navbar
