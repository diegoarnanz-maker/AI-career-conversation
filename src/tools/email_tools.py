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

    # Crear mensaje
    msg = EmailMessage()
    msg["From"] = Config.SMTP_EMAIL
    msg["To"] = Config.SMTP_EMAIL
    msg["Subject"] = f"[Asistente Web] {subject}"
    msg["Reply-To"] = sender_email
    
    # Incluir información del remitente en el cuerpo
    full_body = f"📧 NUEVO MENSAJE DESDE EL ASISTENTE WEB\n\n"
    full_body += f"👤 Remitente: {sender_email}\n"
    full_body += f"📝 Asunto: {subject}\n"
    full_body += f"📅 Enviado desde: Asistente Personal\n\n"
    full_body += f"💬 Mensaje:\n{body}\n\n"
    full_body += f"---\n"
    full_body += f"Para responder, usa Reply-To: {sender_email}"
    
    msg.set_content(full_body)

    try:
        with smtplib.SMTP(Config.SMTP_HOST, int(Config.SMTP_PORT)) as server:
            server.starttls()
            server.login(Config.SMTP_EMAIL, Config.SMTP_PASSWORD)
            server.send_message(msg)
            
        print(f"[INFO] ✅ Email enviado correctamente desde {sender_email}")
        return {"status": "Correo enviado correctamente"}
        
    except smtplib.SMTPAuthenticationError as e:
        error_msg = f"Error de autenticación SMTP: {str(e)}"
        print(f"[ERROR] {error_msg}")
        return {"status": f"Error de autenticación: {error_msg}"}
        
    except smtplib.SMTPRecipientsRefused as e:
        error_msg = f"Destinatario rechazado: {str(e)}"
        print(f"[ERROR] {error_msg}")
        return {"status": f"Error de destinatario: {error_msg}"}
        
    except Exception as e:
        error_msg = f"Error al enviar correo: {type(e).__name__} - {str(e)}"
        print(f"[ERROR] {error_msg}")
        return {"status": f"Error: {error_msg}"} 