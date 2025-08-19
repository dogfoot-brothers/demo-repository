import { useState } from 'react'
import HomePage from './pages/HomePage'
import PromptOptimizationPage from './pages/PromptOptimizationPage'
import Navbar from './components/Navbar'
import ChatWidget from './components/ChatWidget'

function App() {
  const [currentPage, setCurrentPage] = useState('home')

  const renderPage = () => {
    switch (currentPage) {
      case 'home':
        return <HomePage onPageChange={setCurrentPage} />
      case 'prompt-optimization':
        return <PromptOptimizationPage />
      default:
        return <HomePage />
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar currentPage={currentPage} onPageChange={setCurrentPage} />
      <main className="container mx-auto px-4 py-8">
        {renderPage()}
      </main>
      <ChatWidget />
    </div>
  )
}

export default App
