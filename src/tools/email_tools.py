"""
Herramientas para el manejo de emails
"""
import smtplib
from email.message import EmailMessage
from src.config import Config

def send_email_to_me(sender_email, subject, body):
    """
    Envía un correo real a Diego usando la configuración SMTP
    
    Args:
        sender_email (str): Email del remitente
        subject (str): Asunto del correo
        body (str): Contenido del mensaje
        
    Returns:
        dict: Estado del envío
    """
    if not Config.validate_smtp_config():
        error_msg = "Configuración SMTP incompleta. Faltan variables de entorno."
        print(f"[ERROR] {error_msg}")
        return {"status": f"Error: {error_msg}"}

    msg = EmailMessage()
    msg["From"] = Config.SMTP_EMAIL
    msg["To"] = Config.SMTP_EMAIL
    msg["Subject"] = f"[Mensaje desde asistente web] {subject}"
    msg["Reply-To"] = sender_email  # Responder irá al email del remitente

    # Incluir el remitente dentro del cuerpo del mensaje
    full_body = f"Remitente: {sender_email}\n\n{body}"
    msg.set_content(full_body)

    try:
        with smtplib.SMTP(Config.SMTP_HOST, int(Config.SMTP_PORT)) as server:
            server.starttls()
            server.login(Config.SMTP_EMAIL, Config.SMTP_PASSWORD)
            server.send_message(msg)
        print(f"[INFO] Email enviado correctamente desde {sender_email}")
        return {"status": "Correo enviado correctamente"}
    except Exception as e:
        error_msg = f"Error al enviar correo: {type(e).__name__} - {str(e)}"
        print(f"[ERROR] {error_msg}")
        return {"status": f"Error: {error_msg}"} 