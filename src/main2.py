import pyautogui
import pytesseract
from PIL import Image


def open_specific_document(filepath):
    # Abre el explorador de archivos
    pyautogui.press('win')
    pyautogui.write('explorer')
    pyautogui.press('enter')
    pyautogui.sleep(2)

    # Navega al archivo específico
    pyautogui.hotkey('ctrl', 'l')  # Selecciona la barra de dirección
    pyautogui.write(filepath)
    pyautogui.press('enter')
    pyautogui.sleep(2)

    # Maximizar la ventana si es necesario
    pyautogui.hotkey('win', 'up')