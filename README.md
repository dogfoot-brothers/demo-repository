# AI-Powered Customer Support Chat Platform

A modern, AI-powered customer support chat platform built with **Python FastAPI** backend and **React** frontend, featuring an intelligent AI assistant powered by OpenAI's GPT models and a beautiful floating chat widget.

## 🚀 Features

- **AI-Powered Chat**: Intelligent responses using OpenAI GPT models
- **Context-Aware Conversations**: AI remembers conversation history and provides relevant responses
- **Predefined Knowledge Base**: Comprehensive product information, policies, and troubleshooting guides
- **Real-time Chat**: WebSocket-based instant messaging with AI typing indicators
- **Floating Chat Widget**: Minimizable chat interface for customers
- **Modern UI**: Beautiful, responsive design with Tailwind CSS
- **RESTful API**: Complete API documentation with FastAPI
- **WebSocket Integration**: Real-time bidirectional communication

## 🏗️ Architecture

```
├── backend/                 # FastAPI backend
│   ├── main.py             # Main application with WebSocket & LLM support
│   ├── config.py           # Configuration and settings
│   ├── llm_service.py      # OpenAI integration service
│   └── context_data.py     # Predefined knowledge base
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   ├── pages/         # Page components
│   │   └── App.jsx        # Main application
│   └── package.json       # Frontend dependencies
├── requirements.txt        # Python dependencies
├── start_backend.py       # Backend startup script
├── start_frontend.sh      # Frontend startup script
└── test_llm.py           # LLM integration test script
```

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework
- **OpenAI GPT**: Advanced language model integration
- **WebSockets**: Real-time communication
- **Pydantic**: Data validation
- **Uvicorn**: ASGI server

### Frontend
- **React 18**: Modern UI library
- **Vite**: Fast build tool
- **Tailwind CSS**: Utility-first CSS framework
- **Lucide React**: Beautiful icons

## 🤖 AI Integration

### OpenAI GPT Models
- **Model**: GPT-3.5-turbo (configurable)
- **Context Length**: 4000 tokens
- **Temperature**: 0.7 (balanced creativity and accuracy)
- **System Prompt**: Customized for customer support

### Knowledge Base
The AI assistant has access to comprehensive information about:
- **Product Catalog**: Detailed product specifications and pricing
- **Service Policies**: Return, warranty, and shipping policies
- **Common Issues**: Troubleshooting guides and solutions
- **Company Information**: Contact details and business hours
- **FAQ Data**: Frequently asked questions and answers

### Context Awareness
- Remembers conversation history (last 10 messages)
- Provides personalized responses using customer names
- References relevant product and policy information
- Offers intelligent fallback responses

## 📦 Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn
- OpenAI API key

### Environment Setup
1. Copy the environment template:
```bash
cp env.example .env
```

2. Add your OpenAI API key to `.env`:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

### Backend Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Test LLM integration (optional)
python test_llm.py

# Start the backend server
python start_backend.py
```

The backend will be available at:
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **WebSocket**: ws://localhost:8000/ws/chat/{session_id}
- **LLM Test**: http://localhost:8000/api/llm/test

### Frontend Setup
```bash
# Start the frontend development server
./start_frontend.sh
```

The frontend will be available at:
- **Application**: http://localhost:3000
- **API Proxy**: http://localhost:3000/api → http://localhost:8000
- **WebSocket Proxy**: ws://localhost:3000/ws → ws://localhost:8000

## 🎯 Usage

### For Customers
1. Visit the homepage at http://localhost:3000
2. Click the floating AI chat widget (bottom-right corner)
3. Enter your name to start a conversation
4. Chat with the AI assistant in real-time
5. Get instant, intelligent responses to your questions

## 🔌 API Endpoints

### REST API
- `GET /` - Health check
- `GET /health` - System status
- `POST /api/chat/session` - Create new chat session
- `GET /api/chat/sessions` - List all sessions
- `GET /api/chat/session/{session_id}` - Get specific session
- `POST /api/chat/message` - Send message (non-WebSocket)
- `GET /api/llm/test` - Test LLM responses

### WebSocket
- `ws://localhost:8000/ws/chat/{session_id}` - Real-time chat connection

## 🎨 UI Components

### AI Chat Widget
- Floating, minimizable interface
- AI typing indicators
- Real-time message updates
- Smooth animations and transitions
- Responsive design

### Homepage
- Modern, responsive design
- AI feature highlights
- Clear call-to-action
- Beautiful animations

## 🔧 Development

### Backend Development
```bash
# Run with auto-reload
python start_backend.py

# Or directly with uvicorn
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development
```bash
cd frontend
npm install
npm run dev
```

### Testing LLM Integration
```bash
# Test LLM responses
python test_llm.py

# Test via API
curl "http://localhost:8000/api/llm/test?query=Hello"
```

### Building for Production
```bash
# Frontend build
cd frontend
npm run build

# Backend production
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 🚀 Deployment

### Backend Deployment
The FastAPI application can be deployed using:
- **Docker**: Containerized deployment
- **Heroku**: Cloud platform deployment
- **AWS/GCP**: Cloud infrastructure
- **VPS**: Traditional server deployment

### Frontend Deployment
The React application can be deployed to:
- **Vercel**: Zero-config deployment
- **Netlify**: Static site hosting
- **AWS S3**: Static website hosting
- **GitHub Pages**: Free hosting

## 🔒 Security Considerations

- CORS configuration for cross-origin requests
- Input validation with Pydantic
- WebSocket connection management
- Session isolation
- OpenAI API key security
- Rate limiting (recommended for production)

## 📈 Future Enhancements

- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] User authentication and authorization
- [ ] File upload support
- [ ] Chat history persistence
- [ ] Push notifications
- [ ] Analytics and reporting
- [ ] Multi-language support
- [ ] Mobile app development
- [ ] Advanced AI features (sentiment analysis, intent detection)
- [ ] Integration with other LLM providers
- [ ] Custom training data support

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the API documentation at http://localhost:8000/docs
- Review the code comments for implementation details
- Test the LLM integration with `python test_llm.py`

---

**Built with ❤️ using FastAPI, React, and OpenAI GPT**
