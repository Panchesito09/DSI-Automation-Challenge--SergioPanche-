from fastapi import FastAPI, File, UploadFile, HTTPException, status, Depends, Body
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import JSONResponse
import pyautogui
from PIL import Image
import pytesseract
import io
import secrets

app = FastAPI()

security = HTTPBasic()

def Auth(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Autentica al usuario verificando las credenciales proporcionadas contra los valores almacenados seguramente.
    Lanza un error HTTP 401 si las credenciales son incorrectas.

    Args:
    - credentials (HTTPBasicCredentials): Credenciales que incluyen nombre de usuario y contraseña.

    Returns:
    - str: El nombre de usuario autenticado.

    Raises:
    - HTTPException: Si la autenticación falla.
    """
    try:
        correct_username = secrets.compare_digest(credentials.username, "admin")
        correct_password = secrets.compare_digest(credentials.password, "1234")
        if not (correct_username and correct_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Nombre de usuario o contraseña incorrectos",
                headers={"WWW-Authenticate": "Basic"},
            )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    return credentials.username

@app.get("/")
def read_root():
    """
    Endpoint raíz que proporciona un mensaje de saludo. Sirve como verificación rápida de que la API está operativa.

    Returns:
    - dict: Un mensaje de bienvenida.
    """
    return {"Hello": "World"}

@app.get("/automation")
def automation(username: str = Depends(Auth)):
    """
    Automatiza la apertura de un explorador de archivos y navega a un documento específico para realizar la captura de pantalla y el análisis de texto.

    Args:
    - username (str): Nombre de usuario autenticado obtenido a través del decorador `Depends`.

    Returns:
    - dict: Mensaje indicando si se encontró una factura en el documento.

    Raises:
    - HTTPException: Si ocurre un error durante la automatización.
    """
    try:
        pyautogui.press('win')
        pyautogui.write('Explorador de archivos')
        pyautogui.press('enter')
        pyautogui.sleep(3)
        pyautogui.hotkey('alt', 'd')
        pyautogui.sleep(2)
        pyautogui.write('C:\\Users\\sergi\\Downloads\\Factura')
        pyautogui.press('enter')
        pyautogui.sleep(3)
        screenshot = pyautogui.screenshot()
        screenshot.save('C:\\Users\\sergi\\Downloads\\screenshotreto.png')
        pyautogui.sleep(3)
        text = pytesseract.image_to_string(Image.open('C:\\Users\\sergi\\Downloads\\screenshotreto.png'))
        if 'factura' in text:
            parts = text.split('total')
            pyautogui.press('win')
            pyautogui.write('bloc de notas')
            pyautogui.press('enter')
            pyautogui.sleep(3)
            pyautogui.write(parts[1])
            pyautogui.press('enter')
            return {'message': 'El documento es una factura y la información sobre el total se mostrará en el bloc de notas'}
        else:
            return {'message': 'No se encontró una factura en el documento'}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.get("/commands")
def commands(command: str, username: str = Depends(Auth)):
    """
    Ejecuta comandos específicos mediante pyautogui según la entrada del usuario.

    Args:
    - command (str): El comando a ejecutar ('calculadora', 'bloc de notas', 'explorador de archivos').
    - username (str): Usuario autenticado que ejecuta el comando.

    Returns:
    - dict: Mensaje sobre la acción realizada.

    Raises:
    - HTTPException: Si ocurre un error al ejecutar el comando o si el comando no es reconocido.
    """
    try:
        if command == 'calculadora':
            pyautogui.press('win')
            pyautogui.write('calculadora')
            pyautogui.press('enter')
            return {'message': 'Calculadora abierta'}
        elif command == 'bloc de notas':
            pyautogui.press('win')
            pyautogui.write('bloc de notas')
            pyautogui.press('enter')
            return {'message': 'Bloc de notas abierto'}
        elif command == 'explorador de archivos':
            pyautogui.press('win')
            pyautogui.write('explorador de archivos')
            pyautogui.press('enter')
            return {'message': 'Explorador de archivos abierto'}
        else:
            return {'message': 'Comando no reconocido'}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.post("/extract-text/")
async def extract_text(file: UploadFile = File(...), username: str = Depends(Auth)):
    """
    Extrae texto de una imagen cargada, utilizando pytesseract para analizar el contenido de la imagen.

    Args:
    - file (UploadFile): La imagen de la cual se extraerá el texto.
    - username (str): Usuario que realiza la solicitud.

    Returns:
    - JSONResponse: El texto extraído de la imagen.

    Raises:
    - HTTPException: Si el archivo no es una imagen o si ocurre un error durante la extracción.
    """
    if file.content_type.startswith('image/'):
        try:
            contents = await file.read()
            image = Image.open(io.BytesIO(contents))
            text = pytesseract.image_to_string(image)
            text=JSONResponse(content={"extracted_text": text})
            return text
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tipo de archivo no soportado. Por favor subir una imagen.")

@app.post("/complete-sequence/")
async def complete_sequence(file: UploadFile = File(...), username: str = Depends(Auth)):
    """
    Procesa un documento o imagen cargado: extrae texto y realiza acciones específicas basadas en su contenido.

    Args:
    - file (UploadFile): La imagen o documento PDF a procesar.
    - username (str): Usuario que realiza la solicitud.

    Returns:
    - dict: Acciones realizadas basadas en el texto extraído.

    Raises:
    - HTTPException: Si el archivo no es soportado o si ocurre un error durante el procesamiento.
    """
    if file.content_type.startswith('image/') or file.content_type.startswith('application/pdf'):
        try:
            contents = await file.read()
            image = Image.open(io.BytesIO(contents))
            text = pytesseract.image_to_string(image)
            return execute_actions_based_on_text(text)
        except Exception as e:
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": str(e)})
    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tipo de archivo no soportado. Por favor, suba una imagen o documento PDF.")
    
def execute_actions_based_on_text(text: str):
    """
    Ejecuta acciones basadas en el texto extraído del documento cargado. Dependiendo del contenido del texto,
    realiza diversas acciones como abrir el bloc de notas y escribir información relevante.

    Args:
    - text (str): El texto extraído de un documento o imagen, que se analiza para determinar acciones relevantes.

    Returns:
    - dict: Un diccionario que contiene una lista de las acciones realizadas, detallando cada acción que se ha llevado a cabo
      basada en el análisis del texto.

    Raises:
    - Exception: Captura cualquier excepción general que pueda ocurrir durante la ejecución de las acciones y la reporta como parte de la respuesta.

    Ejemplos de acciones realizadas incluyen abrir el bloc de notas para escribir que se detectó una factura, abrir el bloc de notas
    para anotar sobre la presentación detectada, o simplemente escribir el texto completo en el bloc de notas si no se encuentran palabras clave específicas.
    """
    actions_performed = []
    try:
        if 'factura' in text.lower():
            pyautogui.press('win')
            pyautogui.write('notepad')
            pyautogui.press('enter')
            pyautogui.sleep(1)
            pyautogui.typewrite('Se detectó una factura en el texto.')
            pyautogui.press('enter')
            actions_performed.append("Bloc de notas abierto y mensaje escrito sobre factura.")
        elif 'presentacion' in text.lower():
            pyautogui.press('win')
            pyautogui.write('notepad')
            pyautogui.press('enter')
            pyautogui.sleep(1)
            pyautogui.typewrite('Se detectó una presentación en el texto.')
            pyautogui.press('enter')
            actions_performed.append("Bloc de notas abierto y mensaje escrito sobre presentación.")
        else:
            pyautogui.press('win')
            pyautogui.write('notepad')
            pyautogui.press('enter')
            pyautogui.sleep(1)
            pyautogui.typewrite(text)
            pyautogui.press('enter')
            actions_performed.append("Texto extraído mostrado en el bloc de notas.")

        if not actions_performed:
            actions_performed.append("No se encontraron acciones relevantes para realizar.")

    except Exception as e:
        actions_performed.append(f"Error al ejecutar acciones: {str(e)}")

    return {"actions_performed": actions_performed}

