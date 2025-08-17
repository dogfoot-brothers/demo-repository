import openai
import asyncio
from typing import List, Dict, Optional
from .config import settings
from .context_data import get_context_for_query

class LLMService:
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model
        self.system_prompt = settings.system_prompt
        self.max_context_length = settings.max_context_length
    
    async def generate_response(
        self, 
        user_message: str, 
        conversation_history: List[Dict] = None,
        customer_name: str = "Customer"
    ) -> str:
        """
        Generate an AI response based on user message and conversation history
        """
        try:
            # Get relevant context for the query
            context = get_context_for_query(user_message)
            
            # Build conversation messages
            messages = [
                {
                    "role": "system",
                    "content": f"{self.system_prompt}\n\nCompany Context:\n{context}\n\nCustomer Name: {customer_name}"
                }
            ]
            
            # Add conversation history if available
            if conversation_history:
                for msg in conversation_history[-10:]:  # Keep last 10 messages for context
                    if msg.get('sender') == 'customer':
                        messages.append({
                            "role": "user",
                            "content": msg.get('message', '')
                        })
                    elif msg.get('sender') == 'agent':
                        messages.append({
                            "role": "assistant",
                            "content": msg.get('message', '')
                        })
            
            # Add current user message
            messages.append({
                "role": "user",
                "content": user_message
            })
            
            # Generate response using OpenAI
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=self.model,
                messages=messages,
                max_tokens=500,
                temperature=0.7,
                presence_penalty=0.1,
                frequency_penalty=0.1
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            # Add fallback if response is too short or generic
            if len(ai_response) < 10:
                ai_response = self._get_fallback_response(user_message, context)
            
            return ai_response
            
        except Exception as e:
            print(f"Error generating LLM response: {e}")
            return self._get_fallback_response(user_message, context)
    
    def _get_fallback_response(self, user_message: str, context: str) -> str:
        """
        Provide a fallback response when LLM fails
        """
        user_message_lower = user_message.lower()
        
        # Check for common patterns and provide appropriate responses
        if any(word in user_message_lower for word in ['hello', 'hi', 'hey']):
            return "Hello! I'm here to help you with any questions about our products and services. How can I assist you today?"
        
        elif any(word in user_message_lower for word in ['price', 'cost', 'how much']):
            return "I'd be happy to help you with pricing information. Could you please specify which product you're interested in?"
        
        elif any(word in user_message_lower for word in ['return', 'refund']):
            return "Our return policy allows returns within 30 days of purchase, provided the item is in its original condition with packaging. Would you like me to help you with a return?"
        
        elif any(word in user_message_lower for word in ['warranty', 'guarantee']):
            return "Most of our products come with a 1-year standard warranty. Extended warranty options are also available. What specific product are you asking about?"
        
        elif any(word in user_message_lower for word in ['shipping', 'delivery']):
            return "We offer free shipping on orders over $50. Standard shipping takes 3-5 business days, and express shipping is available for 1-2 business days."
        
        elif any(word in user_message_lower for word in ['help', 'support', 'problem']):
            return "I'm here to help! For technical support, you can call us at 1-800-TECH-HELP or email support@techcompany.com. What specific issue are you experiencing?"
        
        else:
            return "Thank you for your message. I'm here to help with any questions about our products, services, or policies. Could you please provide more details about what you need assistance with?"

# Global LLM service instance
llm_service = LLMService()
