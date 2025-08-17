#!/bin/bash

echo "🚀 Starting React Customer Support Chat Frontend..."
echo "📍 Frontend will be available at: http://localhost:3000"
echo "🔗 Backend API proxy: http://localhost:3000/api -> http://localhost:8000"
echo "🔌 WebSocket proxy: ws://localhost:3000/ws -> ws://localhost:8000"
echo ""
echo "="*50

cd frontend
npm install
npm run dev
