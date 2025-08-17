#!/usr/bin/env python3
"""
Test script for LLM integration
"""
import asyncio
import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from llm_service import llm_service

async def test_llm_responses():
    """Test various LLM responses"""
    print("🤖 Testing LLM Integration...")
    print("=" * 50)
    
    test_queries = [
        "Hello, I need help with my laptop",
        "What's your return policy?",
        "How much does the TechPro Laptop cost?",
        "My computer is running slow, what should I do?",
        "Do you offer international shipping?",
        "What warranty do you provide?",
        "I can't reset my password",
        "Tell me about your products"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n📝 Test {i}: {query}")
        print("-" * 30)
        
        try:
            response = await llm_service.generate_response(query)
            print(f"🤖 AI Response: {response}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 30)
    
    print("\n✅ LLM testing completed!")

if __name__ == "__main__":
    asyncio.run(test_llm_responses())
