import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    FLASK_PORT = int(
        os.getenv('CDSW_APP_PORT') or
        os.getenv('FLASK_PORT', 5001)
    )
    
    # LLM Configuration
    LLM_MODEL = "claude-sonnet-4-20250514"
    LLM_TEMPERATURE = 0.2
    LLM_MAX_TOKENS = 4096