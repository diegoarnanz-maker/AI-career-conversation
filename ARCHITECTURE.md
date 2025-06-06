# 🏗️ Arquitectura del Asistente Personal

## 📁 Estructura de Carpetas

```
mi-asistente-personal/
├── src/                          # Código fuente principal
│   ├── __init__.py
│   ├── config/                   # Configuración centralizada
│   │   ├── __init__.py
│   │   └── settings.py          # Variables de entorno y configuración
│   ├── core/                    # Lógica principal del asistente
│   │   ├── __init__.py
│   │   ├── assistant.py         # Clase principal PersonalAssistant
│   │   └── data_loader.py       # Cargador de datos del perfil
│   └── tools/                   # Herramientas del asistente
│       ├── __init__.py
│       ├── email_tools.py       # Funciones de email
│       ├── data_tools.py        # Funciones de datos (leads, preguntas)
│       └── tool_definitions.py  # Definiciones JSON para OpenAI
├── data/                        # Archivos de datos
│   ├── me/                      # Datos del perfil personal
│   │   ├── linkedin.pdf         # PDF de LinkedIn
│   │   └── summary.txt          # Resumen personal
│   ├── leads.txt               # Registro de leads
│   └── unknown_questions.txt   # Preguntas sin respuesta
├── main.py                     # Archivo principal de ejecución
├── app.py                      # Archivo original (legacy)
├── requirements.txt            # Dependencias
├── .env                        # Variables de entorno
└── README.md                   # Documentación principal
```

## 🧩 Componentes Principales

### 1. **Config (`src/config/`)**
- **`settings.py`**: Configuración centralizada
  - Variables de entorno SMTP
  - Rutas de archivos
  - Configuración del asistente
  - Validación de configuración

### 2. **Core (`src/core/`)**
- **`assistant.py`**: Clase principal `PersonalAssistant`
  - Lógica de conversación
  - Manejo de herramientas
  - Inferencia de asuntos de email
  - Control de sugerencias
- **`data_loader.py`**: Clase `DataLoader`
  - Carga de PDF de LinkedIn
  - Carga de resumen personal
  - Manejo de errores de archivos

### 3. **Tools (`src/tools/`)**
- **`email_tools.py`**: Funciones de email
  - `send_email_to_me()`: Envío de emails reales
- **`data_tools.py`**: Funciones de datos
  - `record_user_details()`: Registro de leads
  - `record_unknown_question()`: Registro de preguntas
- **`tool_definitions.py`**: Definiciones JSON
  - Esquemas para OpenAI Function Calling

## 🚀 Cómo Usar

### Ejecutar con Nueva Arquitectura
```bash
python main.py
```

### Ejecutar Versión Original (Legacy)
```bash
python app.py
```

## ✅ Ventajas de la Nueva Arquitectura

1. **🔧 Modularidad**: Cada componente tiene una responsabilidad específica
2. **📝 Mantenibilidad**: Código más fácil de leer y modificar
3. **🧪 Testeable**: Cada módulo se puede probar independientemente
4. **📈 Escalabilidad**: Fácil agregar nuevas herramientas o funcionalidades
5. **⚙️ Configuración**: Configuración centralizada y fácil de gestionar
6. **📚 Documentación**: Código autodocumentado con docstrings

## 🔄 Migración

La nueva arquitectura mantiene **100% compatibilidad** con la funcionalidad original:
- ✅ Mismo comportamiento de conversación
- ✅ Mismas herramientas (email, leads, preguntas)
- ✅ Misma configuración SMTP
- ✅ Mismos archivos de datos

## 🛠️ Desarrollo

### Agregar Nueva Herramienta
1. Crear función en `src/tools/`
2. Agregar definición JSON en `tool_definitions.py`
3. Importar en `__init__.py`
4. Usar en `assistant.py`

### Modificar Configuración
1. Editar `src/config/settings.py`
2. Usar `Config.VARIABLE` en el código

### Agregar Nuevo Módulo Core
1. Crear archivo en `src/core/`
2. Importar en `__init__.py`
3. Usar en `assistant.py` o `main.py` 