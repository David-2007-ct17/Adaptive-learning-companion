import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration settings for the Learning Companion"""
    
    # Gemini API Configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    MODEL_NAME = "gemini-2.5-flash-exp"  # Updated for Gemini 2.5
    
    # Memory Configuration
    MEMORY_FILE = "data/learning_memory.json"
    MAX_SESSIONS = 100
    
    # Agent Configuration
    MAX_RETRIES = 3
    RATE_LIMIT_CALLS_PER_MINUTE = 15
    
    # UI Configuration
    MAX_DISPLAY_WIDTH = 70
    
    # Flask Configuration
    FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-secret-key-change-in-production")
    
    @classmethod
    def validate_config(cls):
        """Validate that required configuration is present"""
        if not cls.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY not found. "
                "Please create a .env file with your API key. "
                "See README.md for setup instructions."
            )