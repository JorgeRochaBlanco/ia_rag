# Ejemplo funcional de uso de la API RAG con Gemini

Un chatbot sencillo de asistencia al equipo de apoyo a los investigadores, construido con la API de búsqueda de archivos de Gemini.

Este proyecto demuestra cómo construir un agente RAG (Generación Aumentada por Recuperación) que puede responder preguntas basándose en tu base de conocimiento documental, así como en un conjunto de instrucciones y configuración ajustables, según las necesidades. A nivel de interfaz de usuarios, tiene dos grandes partes, una para gestionar (borrar y cargar *corpus documental*, que actúa como base de conocimientos), y otra interfaz que usa dicho *corpus* y, en base a las instrucciones suministradas, permite interactuar con la base de conocimientos como un chatbot, similar por ejemplo a las interfaces típicas de ChatGPT o Google Gemini, permitiendo encadenar una conversación con múltiples preguntas y respuestas.

El aspecto de la interfaz con la que podemos gestionar el *corpus documental* (base de conocimientos para la IA) sería este:

 ![Preview](carga_corpus.png)

 Y el aspecto de la interfaz del *chat bot* sería este:

 ![Preview](chatbot.png)

 El motor de IA utilizado en este ejemplo el Gemini (probado con la versión 2.5 flash, pero puede cambiarse) y el motor de API de repositorio vectorial de Google, asociado.


## Inicio rápido

### 1. Prerrequisitos
- Instalar entorno [Python](https://www.python.org/downloads/windows/) (3.13 o superior)
- Clave de API de Gemini AI ([obtener aquí](https://aistudio.google.com/app/apikey))

### 2. Instalación
Creamos entorno virtual de Python en la carpeta del proyecto e instalamos los paquetes indicados en el fichero de requerimientos:

```
python -m venv .venv
```
Activar el entorno virtual en Windows (salvo que se use entorno de codificación como Visual Studio, por ejemplo, y se configure ahí):
```
.venv\Scripts\activate
```
A partir de ahí, ya podemos lanzar tanto el gestor del *corpus* como el *chat bot*:
```
streamlit run storage_handling.py

streamlit run chat.py
```

### 3. Configuración del entorno

Crea un archivo `.env` con tu clave de API, aquí incluimos los valores dados como ejemplo inicial, pero que pueden alterarse según las necesidades:

```bash
GEMINI_API_KEY="your-api-key-here"    #este valor debe obtenerse en google
IA_MODEL="gemini-2.5-flash"
STORE_NAME="convoc_investig"
DISPLAY_NAME="BD Investigacion"
FICH_INSTRUCCIONES_IA="ia-instructions-convoc-inv.txt"
```

La aplicación se abrirá en ambos casos en tu navegador en `http://localhost:8501`
