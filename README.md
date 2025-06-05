# Mi Asistente Personal con IA

Este proyecto es un asistente personal basado en IA que actúa como Diego Arnanz Lozano, respondiendo preguntas sobre su carrera, experiencia y habilidades profesionales.

## Características

- **Interfaz de chat interactiva** usando Gradio
- **Integración con OpenAI GPT-4o-mini** para conversaciones naturales
- **Notificaciones push** via Pushover para registrar interacciones
- **Lectura de CV en PDF** para obtener información detallada
- **Herramientas personalizadas** para registrar contactos y preguntas

## Requisitos Previos

1. **Python 3.8+** instalado en tu sistema
2. **Cuenta de OpenAI** con API key
3. **Cuenta de Pushover** (opcional, para notificaciones)

## Instalación

1. **Clona o descarga este proyecto**
   ```bash
   cd mi-asistente-personal
   ```

2. **Crea un entorno virtual**
   ```bash
   python -m venv venv
   
   # En Windows:
   venv\Scripts\activate
   
   # En macOS/Linux:
   source venv/bin/activate
   ```

3. **Instala las dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configura las variables de entorno**
   
   Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:
   ```
   OPENAI_API_KEY=tu_api_key_de_openai_aqui
   PUSHOVER_TOKEN=tu_token_de_pushover_aqui
   PUSHOVER_USER=tu_usuario_de_pushover_aqui
   ```

   **Importante:** 
   - Reemplaza `tu_api_key_de_openai_aqui` con tu API key real de OpenAI
   - Las variables de Pushover son opcionales (para notificaciones)

## Uso

1. **Ejecuta la aplicación**
   ```bash
   python app.py
   ```

2. **Abre tu navegador**
   - La aplicación se abrirá automáticamente en `http://localhost:7860`
   - Si no se abre automáticamente, ve a esa URL manualmente

3. **Interactúa con el asistente**
   - Haz preguntas sobre la experiencia profesional de Diego
   - El asistente puede registrar tu email si estás interesado en contactar
   - Todas las preguntas sin respuesta se registran automáticamente

## Personalización

Para adaptar este asistente a tu propio perfil:

1. **Modifica `me/summary.txt`**
   - Actualiza con tu información personal y profesional
   - Incluye educación, experiencia, habilidades, etc.

2. **Reemplaza `me/linkedin.pdf`**
   - Sube tu propio CV o perfil de LinkedIn en formato PDF

3. **Actualiza `app.py`**
   - Cambia `self.name = "Diego Arnanz Lozano"` por tu nombre
   - Modifica el system prompt si es necesario

4. **Configura notificaciones (opcional)**
   - Registra una cuenta en [Pushover](https://pushover.net/)
   - Actualiza las variables de entorno con tus credenciales

## Estructura del Proyecto

```
mi-asistente-personal/
├── app.py              # Aplicación principal
├── requirements.txt    # Dependencias de Python
├── README.md          # Este archivo
├── .env               # Variables de entorno (crear)
└── me/
    ├── summary.txt    # Resumen profesional
    └── linkedin.pdf   # CV o perfil en PDF
```

## Solución de Problemas

### Error: "No module named 'openai'"
```bash
pip install -r requirements.txt
```

### Error: "OpenAI API key not found"
- Verifica que el archivo `.env` existe y contiene `OPENAI_API_KEY=tu_clave_aqui`
- Asegúrate de que la clave de API es válida

### Error al leer el PDF
- Verifica que el archivo `me/linkedin.pdf` existe
- Asegúrate de que es un PDF válido y legible

### La aplicación no se abre en el navegador
- Ve manualmente a `http://localhost:7860`
- Verifica que no hay otros procesos usando el puerto 7860

## Tecnologías Utilizadas

- **Python 3.8+**
- **OpenAI GPT-4o-mini** - Modelo de lenguaje
- **Gradio** - Interfaz de usuario web
- **PyPDF** - Lectura de archivos PDF
- **python-dotenv** - Gestión de variables de entorno
- **requests** - Peticiones HTTP para notificaciones

## Licencia

Este proyecto es de uso libre para fines educativos y personales.

## Contacto

Si tienes preguntas sobre este proyecto, puedes contactar a Diego Arnanz Lozano:
- Email: diegodev96@gmail.com
- LinkedIn: [diegodev96](https://www.linkedin.com/in/diegodev96)
- Portfolio: [diegoarnanz-maker-portfolio.netlify.app](https://diegoarnanz-maker-portfolio.netlify.app) 