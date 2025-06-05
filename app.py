from dotenv import load_dotenv
from openai import OpenAI
import json
import os
from pypdf import PdfReader
import gradio as gr

# Carga las variables de entorno desde un archivo .env
load_dotenv(override=True)

# Función para registrar un lead (email del usuario) en un archivo local
def record_user_details(email, name="Name not provided", notes="not provided"):
    with open("leads.txt", "a", encoding="utf-8") as f:
        f.write(f"{email} | {name} | {notes}\n")
    print(f"[INFO] Lead registrado: {email} | {name} | {notes}")
    return {"recorded": "ok"}

# Función para registrar una pregunta que el asistente no ha sabido responder
def record_unknown_question(question):
    with open("unknown_questions.txt", "a", encoding="utf-8") as f:
        f.write(f"{question}\n")
    print(f"[INFO] Pregunta sin respuesta registrada: {question}")
    return {"recorded": "ok"}

# Declaración de herramientas (tools) para que GPT pueda usarlas automáticamente
record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "The email address of this user"
            },
            "name": {
                "type": "string",
                "description": "The user's name, if they provided it"
            },
            "notes": {
                "type": "string",
                "description": "Any additional information about the conversation that's worth recording to give context"
            }
        },
        "required": ["email"],
        "additionalProperties": False
    }
}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question that couldn't be answered"
            },
        },
        "required": ["question"],
        "additionalProperties": False
    }
}

tools = [
    {"type": "function", "function": record_user_details_json},
    {"type": "function", "function": record_unknown_question_json}
]


# Clase que representa tu asistente inteligente personalizado
class Me:

    def __init__(self):
        self.openai = OpenAI()
        self.name = "Diego Arnanz Lozano"

        # Cargar el contenido de tu perfil PDF
        reader = PdfReader("me/linkedin.pdf")
        self.linkedin = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.linkedin += text

        # Cargar el resumen desde un archivo de texto
        with open("me/summary.txt", "r", encoding="utf-8") as f:
            self.summary = f.read()

    # Método para ejecutar herramientas cuando GPT las solicita
    def handle_tool_call(self, tool_calls):
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            print(f"[TOOL] Ejecutando herramienta: {tool_name}")
            tool = globals().get(tool_name)
            result = tool(**arguments) if tool else {}
            results.append({
                "role": "tool",
                "content": json.dumps(result),
                "tool_call_id": tool_call.id
            })
        return results

    # Prompt del sistema para que GPT sepa que debe responder como si fuera tú
    def system_prompt(self):
        prompt = (
            f"Eres {self.name}, y estás respondiendo en su página web. "
            f"Tu función es contestar preguntas sobre su carrera, formación, habilidades y experiencia. "
            f"Debes sonar profesional y auténtico, como si hablaras con un posible cliente o empleador. "
            f"Si no sabes responder, usa la herramienta 'record_unknown_question'. "
            f"Si el usuario parece interesado, pide su email y usa 'record_user_details'.\n\n"
            f"## Resumen:\n{self.summary}\n\n"
            f"## Perfil de LinkedIn:\n{self.linkedin}\n\n"
            f"Con este contexto, chatea representando a {self.name} de forma fiel."
        )
        return prompt

    # Función principal de conversación
    def chat(self, message, history):
        messages = [{"role": "system", "content": self.system_prompt()}] + history + [{"role": "user", "content": message}]
        done = False
        while not done:
            response = self.openai.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                tools=tools
            )
            if response.choices[0].finish_reason == "tool_calls":
                message = response.choices[0].message
                tool_calls = message.tool_calls
                results = self.handle_tool_call(tool_calls)
                messages.append(message)
                messages.extend(results)
            else:
                done = True
        return response.choices[0].message.content


# Lanza la interfaz web con Gradio
if __name__ == "__main__":
    me = Me()
    gr.ChatInterface(me.chat, type="messages").launch()
