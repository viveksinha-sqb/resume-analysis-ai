import os
from dotenv import load_dotenv

# Load .env from project root
load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    # Model Configurations
    GEMINI_MODEL = "gemini-2.5-pro" 


    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

config = Config()
