from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from typing import List, Dict, Optional
import json
import uuid
from datetime import datetime
from pydantic import BaseModel
import asyncio
import logging
from config import settings

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI-Powered Customer Support & Prompt Optimization Platform", 
    version="2.0.0",
    description="통합된 고객 지원 채팅 및 프롬프트 최적화 플랫폼"
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 한글 인코딩을 위한 미들웨어
@app.middleware("http")
async def add_charset_header(request: Request, call_next):
    response = await call_next(request)
    if "application/json" in response.headers.get("content-type", ""):
        response.headers["content-type"] = "application/json; charset=utf-8"
    return response

# In-memory storage for demo purposes (in production, use a database)
chat_sessions: Dict[str, Dict] = {}
active_connections: Dict[str, WebSocket] = {}

# ============================================================================
# CHAT SYSTEM MODELS AND ENDPOINTS
# ============================================================================

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
    return {
        "message": f"{settings.app_name} is running", 
        "version": "2.0.0",
        "features": ["Customer Support Chat", "Prompt Optimization"],
        "endpoints": {
            "chat": "/api/chat/*",
            "prompt_optimization": "/api/prompt-optimization/*",
            "docs": "/docs"
        }
    }

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
        from llm import ask_llm
        ai_response = await ask_llm(
            f"고객 지원: {user_message}",
            f"고객 {customer_name}님의 문의에 대해 도움이 되는 답변을 제공해라."
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
        from llm import ask_llm
        response = await ask_llm("테스트", query)
        return {"query": query, "response": response, "status": "success"}
    except Exception as e:
        return {"query": query, "error": str(e), "status": "error"}

# ============================================================================
# PROMPT OPTIMIZATION SYSTEM MODELS AND ENDPOINTS
# ============================================================================

class OptimizeRequest(BaseModel):
    user_input: str
    expected_output: str = ""  # 선택적, 빈 문자열이면 기본값
    product_name: str
    exclude_keywords: List[str]
    custom_mutators: List[str] = []

class PromptOptimizeResult(BaseModel):
    best_prompt: str
    best_output: str
    best_score: float
    all_trials: List[Dict]

@app.post("/api/prompt-optimization/optimize", response_model=PromptOptimizeResult)
async def optimize_prompt_api(req: OptimizeRequest):
    """AutoPromptix Simple: 간단하고 효과적인 프롬프트 최적화 API"""
    try:
        # 한글 인코딩 디버깅
        logger.info(f"=== 입력 데이터 디버깅 ===")
        logger.info(f"사용자 요청 (raw): {repr(req.user_input)}")
        logger.info(f"기대 결과 (raw): {repr(req.expected_output)}")
        logger.info(f"제품명 (raw): {repr(req.product_name)}")
        logger.info(f"제외 키워드 (raw): {repr(req.exclude_keywords)}")
        
        # 인코딩 문제가 있는 경우 기본값으로 대체
        if not req.user_input or req.user_input.strip() == "":
            req.user_input = "프로젝트 계획서 만들기"
            logger.warning("사용자 요청이 비어있어 기본값으로 대체")
        
        # 기대 결과가 비어있으면 기본값 설정
        if not req.expected_output or req.expected_output.strip() == "":
            req.expected_output = "구체적이고 실용적인 답변으로, 요청사항에 맞는 상세한 내용을 포함"
            logger.warning("기대 결과가 비어있어 기본값으로 대체")
        
        from autopromptix_efficient import optimize_prompt_simple
        
        result = await optimize_prompt_simple(
            user_input=req.user_input,
            expected_output=req.expected_output,
            product_name=req.product_name,
            exclude_keywords=req.exclude_keywords,
            custom_mutators=req.custom_mutators
        )
        
        logger.info(f"=== 최적화 결과 ===")
        logger.info(f"최고 점수: {result['best_score']}")
        logger.info(f"개선 폭: {result['score_improvement']}")
        
        return result
        
    except Exception as e:
        logger.error(f"프롬프트 최적화 실패: {str(e)}")
        raise HTTPException(status_code=500, detail=f"프롬프트 최적화 중 오류가 발생했습니다: {str(e)}")

@app.get("/api/prompt-optimization/examples")
async def get_optimization_examples():
    """프롬프트 최적화 예시 데이터 반환 (확장된 버전)"""
    examples = [
        {
            "title": "고객 사과 메일",
            "description": "애매한 요청을 구체적이고 효과적인 프롬프트로 변환",
            "data": {
                "user_input": "고객에게 사과 메일 써줘",
                "expected_output": "정중하고 구체적인 사과 메일로, 사과 이유, 해결책, 재발 방지책을 포함",
                "product_name": "고객서비스",
                "forbidden_words": ["절대", "전혀", "아예"],
                "custom_mutators": [
                    "정중하고 공손한 어조로 작성",
                    "구체적인 해결책과 일정 포함"
                ]
            }
        },
        {
            "title": "회사 소개서 작성",
            "description": "간단한 요청을 전문적이고 구조화된 프롬프트로 개선",
            "data": {
                "user_input": "회사 소개서 작성",
                "expected_output": "전문적이고 매력적인 회사 소개서로, 비전, 미션, 핵심 가치를 포함",
                "product_name": "회사",
                "forbidden_words": ["거짓", "과장"],
                "custom_mutators": [
                    "전문적이고 신뢰할 수 있는 톤",
                    "구체적인 수치와 성과 포함"
                ]
            }
        },
        {
            "title": "프로젝트 계획서",
            "description": "애매한 요청을 실행 가능한 구체적 지시사항으로 변환",
            "data": {
                "user_input": "프로젝트 계획서 만들기",
                "expected_output": "구체적이고 실행 가능한 프로젝트 계획서로, 목표, 일정, 리소스를 포함",
                "product_name": "프로젝트",
                "forbidden_words": ["불가능", "어려움"],
                "custom_mutators": [
                    "실행 가능한 구체적 단계 포함",
                    "일정과 담당자 명시"
                ]
            }
        },
        {
            "title": "마케팅 전략 수립",
            "description": "추상적인 요청을 구체적인 실행 계획으로 변환",
            "data": {
                "user_input": "마케팅 전략 좀 제안해줘",
                "expected_output": "데이터 기반의 구체적인 마케팅 전략으로, 타겟 고객, 채널, 예산, KPI를 포함",
                "product_name": "마케팅",
                "forbidden_words": ["모든", "무조건"],
                "custom_mutators": [
                    "구체적인 수치와 일정 포함",
                    "실행 가능한 액션 아이템 제시"
                ]
            }
        },
        {
            "title": "기술 문서 작성",
            "description": "기술적 요청을 명확하고 체계적인 문서로 변환",
            "data": {
                "user_input": "API 사용법 문서 써줘",
                "expected_output": "개발자가 쉽게 이해할 수 있는 API 문서로, 인증, 엔드포인트, 예시 코드를 포함",
                "product_name": "API",
                "forbidden_words": ["복잡", "어려움"],
                "custom_mutators": [
                    "단계별로 따라할 수 있게 구성",
                    "실제 사용 예시 포함"
                ]
            }
        },
        {
            "title": "비즈니스 제안서",
            "description": "비즈니스 아이디어를 구체적이고 설득력 있는 제안서로 변환",
            "data": {
                "user_input": "새로운 서비스 아이디어 제안서 작성",
                "expected_output": "투자자와 고객을 설득할 수 있는 제안서로, 시장 기회, 수익 모델, 실행 계획을 포함",
                "product_name": "서비스",
                "forbidden_words": ["불확실", "모름"],
                "custom_mutators": [
                    "구체적인 시장 규모와 수익 예측",
                    "실행 가능한 로드맵 제시"
                ]
            }
        }
    ]
    return {"examples": examples}

@app.get("/api/prompt-optimization/status")
async def get_optimization_status():
    """프롬프트 최적화 시스템 상태 확인"""
    return {
        "status": "active",
        "version": "1.0.0",
        "features": [
            "자동 프롬프트 변이",
            "다중 평가 메트릭",
            "LLM 통합",
            "실시간 최적화"
        ],
        "endpoints": {
            "optimize": "/api/prompt-optimization/optimize",
            "examples": "/api/prompt-optimization/examples",
            "status": "/api/prompt-optimization/status"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
