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
        self.waiting_for_message = None  # Para recordar email cuando esperamos mensaje
        
        # Cargar datos del perfil
        self.data_loader = DataLoader()
        
        # Obtener herramientas disponibles
        self.tools = get_all_tools()
        
        print(f"[INFO] Asistente {self.name} inicializado correctamente")

    def infer_subject_from_context(self, message, history):
        """
        Infiere el asunto del email usando IA basándose en el contexto de la conversación
        
        Args:
            message (str): Mensaje actual
            history (list): Historial de conversación
            
        Returns:
            str: Asunto generado por IA
        """
        try:
            # Construir contexto completo
            full_context = message
            if history:
                # Tomar los últimos 3 mensajes para contexto
                recent_messages = history[-3:] if len(history) > 3 else history
                context_messages = []
                for msg in recent_messages:
                    if isinstance(msg, dict) and msg.get("content"):
                        context_messages.append(msg["content"])
                if context_messages:
                    full_context = "\n".join(context_messages) + "\n" + message
            
            # Prompt para generar el asunto
            subject_prompt = f"""
Eres un asistente que genera asuntos de email profesionales y concisos.

Basándote en el siguiente mensaje que alguien quiere enviar a Diego Arnanz Lozano (desarrollador/consultor), genera un asunto de email profesional de máximo 8 palabras.

Mensaje:
{full_context}

Genera SOLO el asunto del email, sin comillas ni explicaciones adicionales. Debe ser profesional y describir claramente el propósito del mensaje.
"""
            
            # Llamar a la IA para generar el asunto
            response = self.openai.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[{"role": "user", "content": subject_prompt}],
                max_tokens=50,
                temperature=0.3
            )
            
            generated_subject = response.choices[0].message.content.strip()
            
            # Limpiar el asunto (remover comillas si las hay)
            generated_subject = generated_subject.strip('"\'')
            
            # Validar que no esté vacío y no sea muy largo
            if generated_subject and len(generated_subject) <= 100:
                print(f"[INFO] Asunto generado por IA: {generated_subject}")
                return generated_subject
            else:
                print(f"[WARNING] Asunto generado inválido, usando fallback")
                return "Nuevo mensaje desde el asistente web"
                
        except Exception as e:
            print(f"[ERROR] Error generando asunto con IA: {e}")
            # Fallback a sistema de palabras clave
            return self._fallback_subject_inference(message, history)
    
    def _fallback_subject_inference(self, message, history):
        """
        Sistema de fallback para generar asuntos basado en palabras clave
        
        Args:
            message (str): Mensaje actual
            history (list): Historial de conversación
            
        Returns:
            str: Asunto basado en palabras clave
        """
        keywords_map = {
            "trabajo": "Consulta sobre oportunidades laborales",
            "oferta laboral": "Consulta sobre oportunidades laborales",
            "oferta": "Consulta sobre oportunidades laborales",
            "empleo": "Consulta sobre oportunidades laborales",
            "proyecto": "Propuesta de proyecto",
            "colaboración": "Propuesta de colaboración",
            "consultoría": "Consulta sobre servicios",
            "freelance": "Consulta sobre trabajo freelance",
            "contrato": "Consulta sobre contratación",
            "contratar": "Consulta sobre contratación",
            "contratarte": "Consulta sobre contratación",
            "propuesta": "Nueva propuesta comercial",
            "presupuesto": "Solicitud de presupuesto",
            "servicio": "Consulta sobre servicios"
        }
        
        # Revisar el mensaje actual y el historial reciente
        full_context = message.lower()
        if history:
            recent_messages = history[-3:] if len(history) > 3 else history
            for msg in recent_messages:
                if isinstance(msg, dict) and msg.get("content"):
                    full_context += " " + msg["content"].lower()
        
        # Buscar coincidencias
        for keyword, subject in keywords_map.items():
            if keyword in full_context:
                return subject
        
        return "Nuevo mensaje desde el asistente web"

    def _adapt_long_response(self, original_response, max_length):
        """
        Adapta una respuesta larga usando IA para que quepa en el límite de caracteres
        
        Args:
            original_response (str): Respuesta original completa
            max_length (int): Máximo número de caracteres permitidos
            
        Returns:
            str: Respuesta adaptada que cabe en el límite
        """
        try:
            adaptation_prompt = f"""
Tienes una respuesta que es demasiado larga y necesitas adaptarla para que quepa en exactamente {max_length} caracteres o menos.

Respuesta original:
{original_response}

INSTRUCCIONES ESPECÍFICAS:
1. MANTÉN: El argumento principal y la lógica persuasiva de la respuesta
2. PRIORIZA: Beneficios concretos, valor añadido, diferenciadores clave
3. CONSERVA: El tono profesional y la estructura argumentativa
4. ABREVIA: Términos técnicos cuando sea necesario ("Desarrollo de Aplicaciones Web" → "DAW")
5. ELIMINA: Redundancias y palabras de relleno, pero NO el hilo argumentativo
6. CONECTA: Las ideas con conectores apropiados para mantener fluidez
7. TERMINA: Con una conclusión clara y llamada a la acción si la había
8. La respuesta debe ser EXACTAMENTE {max_length} caracteres o menos

Genera una versión que mantenga el poder persuasivo y la coherencia del mensaje original:
"""
            
            print(f"[DEBUG] Enviando a IA para resumen: {len(original_response)} → {max_length} caracteres")
            
            response = self.openai.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[{"role": "user", "content": adaptation_prompt}],
                max_tokens=200,  # Aumentado para dar más espacio
                temperature=0.1  # Más determinístico
            )
            
            adapted = response.choices[0].message.content.strip()
            print(f"[DEBUG] IA devolvió: {len(adapted)} caracteres")
            
            # Verificar que realmente quepa
            if len(adapted) <= max_length:
                print(f"[INFO] ✅ Respuesta adaptada por IA: {len(adapted)}/{max_length} caracteres")
                return adapted
            else:
                # Si aún es muy larga, cortar de forma inteligente
                print(f"[WARNING] ⚠️ Respuesta de IA aún muy larga ({len(adapted)}), aplicando corte inteligente")
                return self._smart_truncate(adapted, max_length)
                
        except Exception as e:
            print(f"[ERROR] ❌ Error adaptando respuesta con IA: {e}")
            print(f"[DEBUG] Aplicando fallback: corte inteligente")
            # Fallback a corte inteligente
            return self._smart_truncate(original_response, max_length)
    
    def _smart_truncate(self, text, max_length):
        """
        Corta texto de forma inteligente, evitando cortar palabras
        
        Args:
            text (str): Texto a cortar
            max_length (int): Longitud máxima
            
        Returns:
            str: Texto cortado inteligentemente
        """
        if len(text) <= max_length:
            return text
        
        # Cortar en el último espacio antes del límite
        truncated = text[:max_length]
        last_space = truncated.rfind(' ')
        
        if last_space > max_length * 0.8:  # Si el último espacio está cerca del final
            return truncated[:last_space] + "..."
        else:
            # Si no hay espacios cerca, cortar y agregar puntos suspensivos
            return truncated[:max_length-3] + "..."

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
            f"Eres {self.name}, desarrollador fullstack especializado en Angular, Spring Boot y asistentes de IA. "
            f"Estás respondiendo en tu página web personal como asistente profesional. "
            f"Tu función es contestar preguntas sobre tu carrera, formación, habilidades, proyectos y experiencia. "
            f"Debes sonar profesional, auténtico y técnicamente competente, como si hablaras con un posible cliente o empleador. "
            f"IMPORTANTE: Cuando respondas preguntas sobre contratación o valor profesional, estructura tu respuesta de forma persuasiva: "
            f"1) Destaca beneficios concretos y diferenciadores, 2) Menciona experiencia relevante con ejemplos, "
            f"3) Conecta habilidades con valor para el empleador, 4) Termina con una propuesta de acción. "
            f"Si no sabes responder, usa la herramienta 'record_unknown_question'. "
            f"Si el usuario parece interesado, pide su email y usa 'record_user_details'. "
            f"Cuando el usuario quiera enviarte un email, usa 'send_email_to_me' con un asunto apropiado basado en el contexto. "
            f"Responde siempre con menos de {Config.MAX_RESPONSE_LENGTH} caracteres.\n\n"
            f"## CV Completo:\n{self.data_loader.get_cv_content()}\n\n"
            f"## Contexto Profesional:\n{self.data_loader.get_contexto_content()}\n\n"
            f"## Preguntas Frecuentes:\n{self.data_loader.get_faq_content()}\n\n"
            f"## Perfil de LinkedIn:\n{self.data_loader.get_linkedin_content()}\n\n"
            f"Con este contexto completo, chatea representando a {self.name} de forma fiel y profesional."
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
            self.waiting_for_message = None  # Reset estado
            self.last_email_suggestion = False  # Reset después de enviar
            if "Error" in result.get("status", ""):
                return f"❌ {result['status'][:140]}"
            else:
                return "✅ Correo enviado correctamente."
        
        # Detectar respuesta afirmativa a sugerencia de email
        if (self.last_email_suggestion and 
            message.strip().lower() in ["sí", "si", "ok", "vale", "perfecto", "claro"]):
            self.last_email_suggestion = True  # Mantener marcado
            return (
                "¡Perfecto! Solo necesito tu email y tu mensaje:\n\n"
                "📧 Formato:\n"
                "Email: tu@email.com\n"
                "Mensaje: Tu mensaje aquí"
            )
        
        # Si estamos esperando un mensaje después de recibir solo el email
        if self.waiting_for_message:
            # Verificar que el mensaje no contenga otro email (para evitar confusiones)
            if not re.search(r'\S+@\S+', message):
                sender_email = self.waiting_for_message
                body = message.strip()
                subject = self.infer_subject_from_context(body, history)
                
                self.pending_email = {
                    "sender_email": sender_email,
                    "subject": subject,
                    "body": body
                }
                self.waiting_for_message = None  # Reset
                
                return (
                    f"📧 Mensaje listo:\n"
                    f"De: {sender_email}\n"
                    f"Asunto: {subject}\n"
                    f"¿Enviar? (responde 'sí')"
                )[:Config.MAX_RESPONSE_LENGTH]
            else:
                # Si el usuario envía otro email, resetear y procesar normalmente
                self.waiting_for_message = None

        # Detectar patrones de email más flexibles
        
        # Patrón 1: "Email: ... Mensaje: ..."
        email_pattern1 = r"(?:email|correo):\s*(\S+@\S+).*?(?:mensaje|message):\s*(.+)"
        match1 = re.search(email_pattern1, message, re.IGNORECASE | re.DOTALL)
        
        # Patrón 2: Email seguido de texto en la misma línea
        email_pattern2 = r'(\S+@\S+)\s+(.+)'
        match2 = re.search(email_pattern2, message.strip())
        
        # Patrón 3: Email en una línea y mensaje en otra (líneas separadas) O email solo
        lines = message.strip().split('\n')
        email_match = None
        message_text = ""
        
        # Buscar email en cualquier línea
        for i, line in enumerate(lines):
            email_search = re.search(r'(\S+@\S+)', line.strip())
            if email_search:
                email_match = email_search.group(1)
                # Si hay más líneas, el resto son el mensaje
                if len(lines) > 1:
                    remaining_lines = lines[i+1:] if i+1 < len(lines) else []
                    if remaining_lines:
                        message_text = '\n'.join(remaining_lines).strip()
                    elif i > 0:
                        # Si el email está en la última línea, tomar las anteriores como mensaje
                        message_text = '\n'.join(lines[:i]).strip()
                break
        
        # Si no encontramos email en múltiples líneas, buscar email solo en línea única
        if not email_match and len(lines) == 1:
            email_search = re.search(r'^(\S+@\S+)$', message.strip())
            if email_search:
                email_match = email_search.group(1)
                message_text = ""  # No hay mensaje, solo email
        
        # Si encontramos patrón 1 (formato estructurado)
        if match1:
            sender_email = match1.group(1).strip()
            body = match1.group(2).strip()
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
        
        # Si encontramos patrón 2 (email + texto en la misma línea)
        elif match2:
            sender_email = match2.group(1).strip()
            body = match2.group(2).strip()
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
        
        # Si encontramos patrón 3 (email + mensaje en líneas separadas)
        elif email_match and message_text:
            subject = self.infer_subject_from_context(message_text, history)
            
            self.pending_email = {
                "sender_email": email_match,
                "subject": subject,
                "body": message_text
            }
            return (
                f"📧 Mensaje listo:\n"
                f"De: {email_match}\n"
                f"Asunto: {subject}\n"
                f"¿Enviar? (responde 'sí')"
            )[:Config.MAX_RESPONSE_LENGTH]
        
        # Si solo encontramos email sin mensaje, pedir el mensaje
        elif email_match and not message_text:
            self.waiting_for_message = email_match
            return (
                f"Perfecto, tengo tu email: {email_match}\n\n"
                f"Ahora solo necesito tu mensaje. ¿Qué quieres contarme?"
            )

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
        print(f"[DEBUG] Respuesta original: {len(full_response)} caracteres")
        
        # Verificar si necesitamos adaptar la respuesta por longitud
        email_suggestion = "\n\n💬 También puedes escribirme por email si prefieres."
        will_add_email_suggestion = not self.pending_email and not self.last_email_suggestion
        
        # Calcular espacio disponible
        if will_add_email_suggestion:
            available_space = Config.MAX_RESPONSE_LENGTH - len(email_suggestion)
            print(f"[DEBUG] Espacio disponible (con email): {available_space}")
        else:
            available_space = Config.MAX_RESPONSE_LENGTH
            print(f"[DEBUG] Espacio disponible (sin email): {available_space}")
        
        # Si la respuesta es muy larga, usar IA para resumirla inteligentemente
        if len(full_response) > available_space:
            print(f"[DEBUG] Respuesta muy larga, aplicando resumen IA")
            adapted_response = self._adapt_long_response(full_response, available_space)
        else:
            print(f"[DEBUG] Respuesta cabe, no necesita resumen")
            adapted_response = full_response
        
        # Agregar sugerencia de email si es necesario
        if will_add_email_suggestion:
            adapted_response += email_suggestion
            self.last_email_suggestion = True
        
        print(f"[DEBUG] Respuesta final: {len(adapted_response)} caracteres")
        return adapted_response 