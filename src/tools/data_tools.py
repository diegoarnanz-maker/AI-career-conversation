"""
Herramientas para el manejo de datos (leads, preguntas sin respuesta)
"""
import os
from src.config import Config

def record_user_details(email, name="Name not provided", notes="not provided"):
    """
    Registra un lead en el archivo de leads
    
    Args:
        email (str): Correo del usuario
        name (str): Nombre del usuario
        notes (str): Notas contextuales
        
    Returns:
        dict: Confirmación del registro
    """
    # Crear directorio data si no existe
    os.makedirs(os.path.dirname(Config.LEADS_FILE), exist_ok=True)
    
    with open(Config.LEADS_FILE, "a", encoding="utf-8") as f:
        f.write(f"{email} | {name} | {notes}\n")
    print(f"[INFO] Lead registrado: {email} | {name} | {notes}")
    return {"recorded": "ok"}

def record_unknown_question(question):
    """
    Registra preguntas que el asistente no supo responder
    
    Args:
        question (str): La pregunta sin respuesta
        
    Returns:
        dict: Confirmación del registro
    """
    # Crear directorio data si no existe
    os.makedirs(os.path.dirname(Config.UNKNOWN_QUESTIONS_FILE), exist_ok=True)
    
    with open(Config.UNKNOWN_QUESTIONS_FILE, "a", encoding="utf-8") as f:
        f.write(f"{question}\n")
    print(f"[INFO] Pregunta sin respuesta registrada: {question}")
    return {"recorded": "ok"} 