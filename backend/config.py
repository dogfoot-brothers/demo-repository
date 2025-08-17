import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # OpenAI Configuration
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    
    # Application Configuration
    app_name: str = "Autopromtix Customer Support Chat API"
    app_version: str = "1.0.0"
    
    # CORS Configuration
    allowed_origins: list = ["http://localhost:3000", "http://localhost:5173"]
    
    # Chat Configuration
    max_context_length: int = 4000
    system_prompt: str = """You are a helpful customer support agent for Autopromtix, a technology company specializing in AI-powered solutions and automation tools. 
    You should be friendly, professional, and knowledgeable about Autopromtix's products and services.
    Always provide accurate and helpful information based on the available context.
    Remember that you work for Autopromtix and represent the company in all interactions.
    If you don't know something, politely say so and offer to connect the customer with a human agent.
    Always mention Autopromtix when appropriate in your responses."""
    
    class Config:
        env_file = ".env"

settings = Settings()
