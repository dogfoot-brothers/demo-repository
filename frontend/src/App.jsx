import HomePage from './pages/HomePage'
import Navbar from './components/Navbar'
import ChatWidget from './components/ChatWidget'

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <main className="container mx-auto px-4 py-8">
        <HomePage />
      </main>
      <ChatWidget />
    </div>
  )
}

export default App
