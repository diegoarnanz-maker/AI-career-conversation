"""
Archivo principal del asistente personal
"""
import gradio as gr
from src.core import PersonalAssistant

def main():
    print("🚀 Iniciando Mi Asistente Personal...")
    
    # Crear instancia del asistente
    assistant = PersonalAssistant()
    
    # Mensaje de bienvenida que aparece al abrir el chat
    welcome_message = """¡Hola! 👋 Soy el asistente personal de **Diego Arnanz Lozano**.

Estoy aquí **24/7** para responder **cualquier pregunta** que tengas sobre Diego:

💼 **Experiencia profesional** - proyectos, tecnologías, roles
🎓 **Formación académica** - títulos, certificaciones, cursos  
🛠️ **Habilidades técnicas** - lenguajes, frameworks, herramientas
🚀 **Proyectos realizados** - detalles, tecnologías usadas
📧 **Contacto directo** - envío de emails inmediato

**Pregúntame lo que quieras** - desde lo más general hasta lo más específico. ¡Estoy aquí para ayudarte! 😊"""
    
    # Configurar y lanzar la interfaz de Gradio
    interface = gr.ChatInterface(
        assistant.chat, 
        type="messages",
        title="🤖 Asistente Profesional de Diego Arnanz Lozano",
        chatbot=gr.Chatbot(
            value=[{"role": "assistant", "content": welcome_message}],
            height=600,
            type="messages"
        )
    )
    
    print("✅ Asistente listo. Abriendo interfaz web...")
    interface.launch()

if __name__ == "__main__":
    main() 