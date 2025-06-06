"""
Archivo principal del asistente personal
Usa la nueva arquitectura modular
"""
import gradio as gr
from src.core import PersonalAssistant

def main():
    """Función principal para lanzar la aplicación"""
    print("🚀 Iniciando Mi Asistente Personal...")
    
    # Crear instancia del asistente
    assistant = PersonalAssistant()
    
    # Configurar y lanzar la interfaz de Gradio
    interface = gr.ChatInterface(
        assistant.chat, 
        type="messages",
        title="Mi Asistente Personal - Diego Arnanz Lozano",
        description="Asistente conversacional profesional con capacidades de email y registro de leads"
    )
    
    print("✅ Asistente listo. Abriendo interfaz web...")
    interface.launch()

if __name__ == "__main__":
    main() 