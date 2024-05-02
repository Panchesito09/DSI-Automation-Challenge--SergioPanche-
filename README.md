# DSI Automation Challenge

## Descripción General del Proyecto

Este proyecto fue desarrollado como parte del Desafío de Automatización de DSI. Está diseñado para automatizar la extracción de texto de documentos a través de OCR (Reconocimiento Óptico de Caracteres) y ejecutar acciones basadas en el texto extraído. Utiliza tecnologías como Python, FastAPI, pytesseract, y pyautogui para implementar una API que controla aplicaciones en un entorno Windows y procesa imágenes para extraer información textual.

## Configuración y Ejecución

### Requisitos Previos

- Python 3.8 o superior instalado en tu sistema.
- Pip para la gestión de paquetes de Python.
- Tesseract-OCR instalado y configurado en tu sistema.

### Instalación de Dependencias

Para instalar todas las dependencias necesarias, ejecuta el siguiente comando en tu terminal:

pip install fastapi uvicorn pytesseract pyautogui python-multipart Pillow


Configuración del OCR
Instala Tesseract-OCR siguiendo las instrucciones disponibles en Tesseract GitHub. Asegúrate de añadir la ruta del ejecutable de Tesseract al PATH de tu sistema operativo.

Ejecución del Servidor
Inicia el servidor de desarrollo ejecutando el siguiente comando en tu terminal:

uvicorn main:app --reload

Este comando inicia un servidor local en http://127.0.0.1:8000. Puedes acceder a la documentación interactiva de la API y probar los endpoints directamente desde http://127.0.0.1:8000/docs.



Diseño y Arquitectura del Sistema
El sistema utiliza FastAPI como framework para crear una API REST, seleccionado por su alto rendimiento y facilidad de uso para crear APIs con Python.

Componentes Principales
Extracción de Texto: Utiliza pytesseract, una interfaz de Python para Tesseract-OCR, que permite la extracción de texto de imágenes.
Automatización de Interfaz de Usuario: Emplea pyautogui para interactuar con la interfaz gráfica de usuario de Windows, automatizando tareas como abrir aplicaciones y gestionar entradas de teclado.
Flujo de Trabajo
Apertura y Control de Aplicaciones: Automatiza la apertura de aplicaciones usando pyautogui.
Extracción de Texto: Captura pantallas de documentos abiertos y extrae texto usando pytesseract.
Lógica de Decisión y Acciones: Analiza el texto extraído y ejecuta acciones basadas en los resultados.

