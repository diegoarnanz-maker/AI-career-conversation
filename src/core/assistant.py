"""
Clase principal del asistente personal
"""
import json
import re
from openai import OpenAI
from src.config import Config
from src.core.data_loader import DataLoader
from src.tools import send_email_to_me, record_user_details, record_unknown_question, get_all_tools

class PersonalAssistant:
    """Asistente personal conversacional con capacidades de email y registro de leads"""
    
    def __init__(self):
        self.openai = OpenAI()
        self.name = "Diego Arnanz Lozano"
        self.pending_email = None
        self.last_email_suggestion = False
        self.interaction_count = 0
        
        # Cargar datos del perfil
        self.data_loader = DataLoader()
        
        # Obtener herramientas disponibles
        self.tools = get_all_tools()
        
        print(f"[INFO] Asistente {self.name} inicializado correctamente")

    def infer_subject_from_context(self, message, history):
        """
        Infiere el asunto del email basado en el contexto de la conversación
        
        Args:
            message (str): Mensaje actual
            history (list): Historial de conversación
            
        Returns:
            str: Asunto inferido
        """
        keywords_map = {
            "trabajo": "Consulta sobre oportunidades laborales",
            "proyecto": "Propuesta de proyecto",
            "colaboración": "Propuesta de colaboración",
            "consultoría": "Consulta sobre servicios",
            "freelance": "Consulta sobre trabajo freelance",
            "contrato": "Consulta sobre contratación",
            "propuesta": "Nueva propuesta comercial",
            "presupuesto": "Solicitud de presupuesto",
            "servicio": "Consulta sobre servicios"
        }
        
        # Revisar el mensaje actual y el historial reciente
        full_context = message.lower()
        if history:
            # Tomar los últimos 3 mensajes para contexto
            recent_messages = history[-3:] if len(history) > 3 else history
            for msg in recent_messages:
                if isinstance(msg, dict) and msg.get("content"):
                    full_context += " " + msg["content"].lower()
        
        # Buscar coincidencias
        for keyword, subject in keywords_map.items():
            if keyword in full_context:
                return subject
        
        return "Nuevo mensaje desde el asistente web"

    def handle_tool_call(self, tool_calls):
        """
        Maneja las llamadas a herramientas
        
        Args:
            tool_calls: Lista de llamadas a herramientas de OpenAI
            
        Returns:
            list: Resultados de las herramientas
        """
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            print(f"[TOOL] Ejecutando herramienta: {tool_name}")

            if tool_name == "send_email_to_me":
                # Si no hay asunto, inferirlo del contexto
                if "subject" not in arguments or not arguments["subject"]:
                    arguments["subject"] = self.infer_subject_from_context(arguments.get("body", ""), [])
                
                self.pending_email = arguments
                confirmation_message = (
                    f"📧 Mensaje listo:\n"
                    f"De: {arguments['sender_email']}\n"
                    f"Asunto: {arguments['subject']}\n"
                    f"¿Enviar? (responde 'sí')"
                )
                results.append({
                    "role": "tool",
                    "content": json.dumps({"status": "esperando_confirmacion"}),
                    "tool_call_id": tool_call.id
                })
                results.append({
                    "role": "assistant",
                    "content": confirmation_message[:Config.MAX_RESPONSE_LENGTH]
                })
                return results

            # Mapear nombres de herramientas a funciones
            tool_functions = {
                "record_user_details": record_user_details,
                "record_unknown_question": record_unknown_question,
                "send_email_to_me": send_email_to_me
            }
            
            tool_function = tool_functions.get(tool_name)
            result = tool_function(**arguments) if tool_function else {}
            results.append({
                "role": "tool",
                "content": json.dumps(result),
                "tool_call_id": tool_call.id
            })
        return results

    def system_prompt(self):
        """
        Genera el prompt del sistema para el asistente
        
        Returns:
            str: Prompt del sistema
        """
        return (
            f"Eres {self.name}, y estás respondiendo en su página web. "
            f"Tu función es contestar preguntas sobre su carrera, formación, habilidades y experiencia. "
            f"Debes sonar profesional y auténtico, como si hablaras con un posible cliente o empleador. "
            f"Si no sabes responder, usa la herramienta 'record_unknown_question'. "
            f"Si el usuario parece interesado, pide su email y usa 'record_user_details'. "
            f"Cuando el usuario quiera enviarte un email, usa 'send_email_to_me' con un asunto apropiado basado en el contexto. "
            f"Responde siempre con menos de {Config.MAX_RESPONSE_LENGTH} caracteres.\n\n"
            f"## Resumen:\n{self.data_loader.get_summary_content()}\n\n"
            f"## Perfil de LinkedIn:\n{self.data_loader.get_linkedin_content()}\n\n"
            f"Con este contexto, chatea representando a {self.name} de forma fiel."
        )

    def chat(self, message, history):
        """
        Procesa un mensaje del usuario y genera una respuesta
        
        Args:
            message (str): Mensaje del usuario
            history (list): Historial de conversación
            
        Returns:
            str: Respuesta del asistente
        """
        # Incrementar contador de interacciones y resetear sugerencia cada N interacciones
        self.interaction_count += 1
        if self.interaction_count % Config.EMAIL_SUGGESTION_RESET_INTERVAL == 0:
            self.last_email_suggestion = False
        
        # Confirmación de envío pendiente
        if self.pending_email and message.strip().lower() in ["sí", "si", "enviar", "confirmar", "ok"]:
            result = send_email_to_me(**self.pending_email)
            self.pending_email = None
            self.last_email_suggestion = False  # Reset después de enviar
            if "Error" in result.get("status", ""):
                return f"❌ {result['status'][:140]}"
            else:
                return "✅ Correo enviado correctamente."

        # Detectar patrón simplificado: "Email: ... Mensaje: ..."
        email_pattern = r"(?:email|correo):\s*(\S+@\S+).*?(?:mensaje|message):\s*(.+)"
        match = re.search(email_pattern, message, re.IGNORECASE | re.DOTALL)
        if match:
            sender_email = match.group(1).strip()
            body = match.group(2).strip()
            subject = self.infer_subject_from_context(body, history)
            
            self.pending_email = {
                "sender_email": sender_email,
                "subject": subject,
                "body": body
            }
            return (
                f"📧 Mensaje listo:\n"
                f"De: {sender_email}\n"
                f"Asunto: {subject}\n"
                f"¿Enviar? (responde 'sí')"
            )[:Config.MAX_RESPONSE_LENGTH]

        # Detectar intención de contacto y pedir solo email y mensaje
        contact_triggers = [
            "quiero enviarte un mail", "escribirte", "mandarte un correo", 
            "tengo una propuesta", "puedo escribirte", "contactarte",
            "enviar email", "enviar correo"
        ]
        if any(trigger in message.lower() for trigger in contact_triggers):
            self.last_email_suggestion = True  # Marcamos que ya sugerimos
            return (
                "¡Perfecto! Solo necesito tu email y tu mensaje:\n\n"
                "📧 Formato:\n"
                "Email: tu@email.com\n"
                "Mensaje: Tu mensaje aquí"
            )[:Config.MAX_RESPONSE_LENGTH]

        # Construcción del mensaje normal a la API
        messages = [{"role": "system", "content": self.system_prompt()}] + history + [{"role": "user", "content": message}]
        done = False
        while not done:
            response = self.openai.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=messages,
                tools=self.tools
            )
            if response.choices[0].finish_reason == "tool_calls":
                message = response.choices[0].message
                tool_calls = message.tool_calls
                results = self.handle_tool_call(tool_calls)
                messages.append(message)
                messages.extend(results)
            else:
                done = True

        full_response = response.choices[0].message.content
        trimmed_response = full_response[:Config.MAX_RESPONSE_LENGTH].strip()

        # Solo agregar sugerencia de email si no hay email pendiente y no se sugirió recientemente
        if not self.pending_email and not self.last_email_suggestion:
            trimmed_response += "\n\n💬 También puedes escribirme por email si prefieres."
            self.last_email_suggestion = True
        
        return trimmed_response 