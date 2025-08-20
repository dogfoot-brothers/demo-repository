"""
LLM 통합 모듈 - OpenAI API와의 통신을 담당
"""

import openai
import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# OpenAI 클라이언트 초기화
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    logger.warning("OPENAI_API_KEY not found. LLM functionality will be limited.")
    client = None
else:
    client = openai.OpenAI(
        api_key=api_key,

    )

async def ask_llm(prompt: str, user_input: str, model: str = "gpt-3.5-turbo") -> str:
    """
    LLM에 프롬프트를 전송하고 응답을 받는 함수
    
    Args:
        prompt: 시스템 프롬프트
        user_input: 사용자 입력
        model: 사용할 모델명
        
    Returns:
        LLM 응답 문자열
    """
    try:
        if not client:
            # 환경변수가 없을 때는 더미 응답 반환 (테스트용)
            logger.warning("LLM client not available, returning dummy response")
            return f"테스트 응답: {user_input}에 대한 답변입니다."
        
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_input}
        ]
        
        logger.info(f"Sending request to LLM model: {model}")
        
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.3,  # 일관성 있는 응답을 위해 낮은 temperature
            max_tokens=500
        )
        
        result = response.choices[0].message.content.strip()
        logger.info(f"LLM response received: {result[:100]}...")
        
        return result
        
    except openai.APIConnectionError as e:
        logger.error(f"LLM connection error: {e}")
        return "죄송합니다. LLM 서비스에 연결할 수 없습니다. 네트워크 연결을 확인해주세요."
        
    except openai.APIStatusError as e:
        logger.error(f"LLM API error: {e.status_code} - {e.response}")
        return f"LLM 서비스 오류가 발생했습니다. (코드: {e.status_code})"
        
    except openai.AuthenticationError as e:
        logger.error(f"LLM authentication error: {e}")
        return "LLM 인증 오류가 발생했습니다. API 키를 확인해주세요."
        
    except Exception as e:
        logger.error(f"Unexpected LLM error: {e}")
        return "예상치 못한 오류가 발생했습니다. 잠시 후 다시 시도해주세요."

async def ask_llm_with_context(
    prompt: str, 
    user_input: str, 
    context: str = "", 
    model: str = "gpt-3.5-turbo"
) -> str:
    """
    컨텍스트 정보를 포함하여 LLM에 질문하는 함수
    
    Args:
        prompt: 시스템 프롬프트
        user_input: 사용자 입력
        context: 추가 컨텍스트 정보
        model: 사용할 모델명
        
    Returns:
        LLM 응답 문자열
    """
    try:
        messages = [
            {"role": "system", "content": prompt}
        ]
        
        if context:
            messages.append({"role": "system", "content": f"참고 정보: {context}"})
            
        messages.append({"role": "user", "content": user_input})
        
        logger.info(f"Sending contextual request to LLM model: {model}")
        
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.3,
            max_tokens=500
        )
        
        result = response.choices[0].message.content.strip()
        logger.info(f"LLM contextual response received: {result[:100]}...")
        
        return result
        
    except Exception as e:
        logger.error(f"Error in contextual LLM request: {e}")
        return "컨텍스트 기반 응답 생성 중 오류가 발생했습니다."

def get_available_models() -> list:
    """
    사용 가능한 OpenAI 모델 목록을 반환
    
    Returns:
        모델 목록
    """
    try:
        models = client.models.list()
        return [model.id for model in models.data]
    except Exception as e:
        logger.error(f"Error fetching models: {e}")
        return ["gpt-3.5-turbo", "gpt-4"]  # 기본값 반환

def test_llm_connection() -> dict:
    """
    LLM 연결 상태를 테스트
    
    Returns:
        테스트 결과 딕셔너리
    """
    try:
        # 간단한 테스트 요청
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10
        )
        
        return {
            "status": "success",
            "model": "gpt-3.5-turbo",
            "response": response.choices[0].message.content,
            "timestamp": "now"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "timestamp": "now"
        }
