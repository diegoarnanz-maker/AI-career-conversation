"""
Configuración centralizada del asistente personal
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv(override=True)

class Config:
    """Configuración principal del asistente"""
    
    # OpenAI
    OPENAI_MODEL = "gpt-4o-mini"
    
    # SMTP Configuration
    SMTP_EMAIL = os.getenv("SMTP_EMAIL")
    SMTP_HOST = os.getenv("SMTP_HOST")
    SMTP_PORT = os.getenv("SMTP_PORT")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
    
    # Archivos de datos
    LEADS_FILE = "data/leads.txt"
    UNKNOWN_QUESTIONS_FILE = "data/unknown_questions.txt"
    LINKEDIN_PDF = "data/me/linkedin.pdf"
    
    # Configuración del asistente
    MAX_RESPONSE_LENGTH = 400
    EMAIL_SUGGESTION_RESET_INTERVAL = 3
    
    @classmethod
    def validate_smtp_config(cls):
        """Valida que la configuración SMTP esté completa"""
        return all([cls.SMTP_EMAIL, cls.SMTP_HOST, cls.SMTP_PORT, cls.SMTP_PASSWORD]) 