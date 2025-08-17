from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import List, Dict, Optional
import json
import uuid
from datetime import datetime
from pydantic import BaseModel
import asyncio
import logging
from config import settings
from llm_service import llm_service

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.app_name, version=settings.app_version)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for demo purposes (in production, use a database)
chat_sessions: Dict[str, Dict] = {}
active_connections: Dict[str, WebSocket] = {}

class ChatMessage(BaseModel):
    session_id: str
    message: str
    sender: str
    timestamp: Optional[datetime] = None

    def dict(self, *args, **kwargs):
        # Convert datetime to ISO string for JSON serialization
        d = super().dict(*args, **kwargs)
        if d.get('timestamp'):
            d['timestamp'] = d['timestamp'].isoformat()
        return d

class ChatSession(BaseModel):
    session_id: str
    customer_name: str
    status: str = "active"
    created_at: datetime
    last_message_at: Optional[datetime] = None

    def dict(self, *args, **kwargs):
        # Convert datetime to ISO string for JSON serialization
        d = super().dict(*args, **kwargs)
        if d.get('created_at'):
            d['created_at'] = d['created_at'].isoformat()
        if d.get('last_message_at'):
            d['last_message_at'] = d['last_message_at'].isoformat()
        return d

class CreateSessionRequest(BaseModel):
    customer_name: str

@app.get("/")
async def root():
    return {"message": f"{settings.app_name} is running", "version": settings.app_version}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}

@app.post("/api/chat/session", response_model=ChatSession)
async def create_chat_session(request: CreateSessionRequest):
    """Create a new chat session for a customer"""
    session_id = str(uuid.uuid4())
    session = ChatSession(
        session_id=session_id,
        customer_name=request.customer_name,
        created_at=datetime.now()
    )
    chat_sessions[session_id] = {
        "session": session.dict(),
        "messages": []
    }
    logger.info(f"Created chat session: {session_id} for {request.customer_name}")
    return session

@app.get("/api/chat/sessions")
async def get_chat_sessions():
    """Get all active chat sessions"""
    return [session["session"] for session in chat_sessions.values()]

@app.get("/api/chat/session/{session_id}")
async def get_chat_session(session_id: str):
    """Get a specific chat session with messages"""
    if session_id not in chat_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return chat_sessions[session_id]

@app.websocket("/ws/chat/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """WebSocket endpoint for real-time chat communication with LLM integration"""
    await websocket.accept()
    logger.info(f"WebSocket connection accepted for session: {session_id}")
    
    if session_id not in chat_sessions:
        logger.error(f"Session not found: {session_id}")
        await websocket.close(code=4004, reason="Session not found")
        return
    
    # Store the connection
    active_connections[session_id] = websocket
    logger.info(f"WebSocket connection stored for session: {session_id}")
    
    try:
        while True:
            # Receive message from client
            logger.info(f"Waiting for message from session: {session_id}")
            data = await websocket.receive_text()
            logger.info(f"Received message from session {session_id}: {data}")
            
            message_data = json.loads(data)
            
            # Create message object
            message = ChatMessage(
                session_id=session_id,
                message=message_data["message"],
                sender=message_data["sender"],
                timestamp=datetime.now()
            )
            
            # Store message
            chat_sessions[session_id]["messages"].append(message.dict())
            chat_sessions[session_id]["session"]["last_message_at"] = message.timestamp.isoformat()
            logger.info(f"Stored message for session {session_id}: {message_data['message']}")
            
            # Broadcast message to all connections for this session
            await broadcast_message(session_id, message.dict())
            logger.info(f"Broadcasted message for session {session_id}")
            
            # If message is from customer, generate AI response
            if message_data["sender"] == "customer":
                logger.info(f"Generating AI response for session {session_id}")
                await generate_ai_response(session_id, message_data["message"])
            
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for session: {session_id}")
        # Remove connection when client disconnects
        if session_id in active_connections:
            del active_connections[session_id]
    except Exception as e:
        logger.error(f"Error in WebSocket for session {session_id}: {e}")
        if session_id in active_connections:
            del active_connections[session_id]

async def generate_ai_response(session_id: str, user_message: str):
    """Generate and send AI response for customer messages"""
    try:
        logger.info(f"Starting AI response generation for session {session_id}")
        # Get conversation history
        conversation_history = chat_sessions[session_id]["messages"]
        customer_name = chat_sessions[session_id]["session"]["customer_name"]
        
        # Generate AI response
        ai_response = await llm_service.generate_response(
            user_message=user_message,
            conversation_history=conversation_history,
            customer_name=customer_name
        )
        
        logger.info(f"AI response generated for session {session_id}: {ai_response[:50]}...")
        
        # Create AI message
        ai_message = ChatMessage(
            session_id=session_id,
            message=ai_response,
            sender="agent",
            timestamp=datetime.now()
        )
        
        # Store AI message
        chat_sessions[session_id]["messages"].append(ai_message.dict())
        chat_sessions[session_id]["session"]["last_message_at"] = ai_message.timestamp.isoformat()
        
        # Broadcast AI response
        await broadcast_message(session_id, ai_message.dict())
        logger.info(f"AI response broadcasted for session {session_id}")
        
    except Exception as e:
        logger.error(f"Error generating AI response for session {session_id}: {e}")
        # Send fallback message
        fallback_message = ChatMessage(
            session_id=session_id,
            message="I apologize, but I'm having trouble processing your request right now. Please try again or contact our human support team.",
            sender="agent",
            timestamp=datetime.now()
        )
        chat_sessions[session_id]["messages"].append(fallback_message.dict())
        await broadcast_message(session_id, fallback_message.dict())

async def broadcast_message(session_id: str, message: dict):
    """Broadcast message to all connections for a session"""
    if session_id in active_connections:
        try:
            await active_connections[session_id].send_text(json.dumps(message))
            logger.info(f"Message sent to session {session_id}")
        except Exception as e:
            logger.error(f"Error sending message to session {session_id}: {e}")
            # Remove broken connection
            del active_connections[session_id]

@app.post("/api/chat/message")
async def send_message(message: ChatMessage):
    """Send a message to a chat session (for non-WebSocket clients)"""
    if message.session_id not in chat_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    message.timestamp = datetime.now()
    chat_sessions[message.session_id]["messages"].append(message.dict())
    chat_sessions[message.session_id]["session"]["last_message_at"] = message.timestamp.isoformat()
    
    # Broadcast to WebSocket connections
    await broadcast_message(message.session_id, message.dict())
    
    # If message is from customer, generate AI response
    if message.sender == "customer":
        await generate_ai_response(message.session_id, message.message)
    
    return {"status": "sent", "message": message.dict()}

@app.get("/api/llm/test")
async def test_llm_response(query: str = "Hello"):
    """Test endpoint for LLM responses"""
    try:
        response = await llm_service.generate_response(query)
        return {"query": query, "response": response, "status": "success"}
    except Exception as e:
        return {"query": query, "error": str(e), "status": "error"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
