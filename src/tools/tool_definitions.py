"""
Definiciones JSON de las herramientas para OpenAI
"""

# Definición de la herramienta para registrar leads
record_user_details_json = {
    "name": "record_user_details",
    "description": "Registra el interés de un usuario que proporciona su email",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {"type": "string", "description": "Correo del usuario"},
            "name": {"type": "string", "description": "Nombre del usuario"},
            "notes": {"type": "string", "description": "Notas contextuales"}
        },
        "required": ["email"],
        "additionalProperties": False
    }
}

# Definición de la herramienta para registrar preguntas sin respuesta
record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Registra preguntas que el asistente no supo responder",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {"type": "string", "description": "La pregunta sin respuesta"},
        },
        "required": ["question"],
        "additionalProperties": False
    }
}

# Definición de la herramienta para enviar emails
send_email_to_me_json = {
    "name": "send_email_to_me",
    "description": "Permite al usuario enviar un correo a Diego. El asunto se infiere automáticamente del contexto.",
    "parameters": {
        "type": "object",
        "properties": {
            "sender_email": {"type": "string", "description": "Correo del remitente"},
            "subject": {"type": "string", "description": "Asunto inferido del contexto"},
            "body": {"type": "string", "description": "Contenido del mensaje"}
        },
        "required": ["sender_email", "body"],
        "additionalProperties": False
    }
}

def get_all_tools():
    """
    Retorna todas las herramientas disponibles en el formato requerido por OpenAI
    
    Returns:
        list: Lista de herramientas formateadas para OpenAI
    """
    return [
        {"type": "function", "function": record_user_details_json},
        {"type": "function", "function": record_unknown_question_json},
        {"type": "function", "function": send_email_to_me_json}
    ] 