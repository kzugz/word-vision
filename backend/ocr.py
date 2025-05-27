import numpy as np
import easyocr
from PIL import Image
import io
import cv2
import Levenshtein

reader = easyocr.Reader(['pt'])

# Substituições comuns de OCR
def correct_ocr_text(text):
    corrections = {
        '7': 'T', '5': 'S', '0': 'O', '1': 'I', '2': 'Z', '8': 'B',
        '|': 'I', '!': 'I', '£': 'E', '$': 'S', '§': 'S', 'ß': 'B', '€': 'E',
    }
    return ''.join(corrections.get(char, char) for char in text)

# Pré-processamento da imagem
def preprocess_image(image_np):
    gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
    equalized = cv2.equalizeHist(gray)
    laplacian = cv2.Laplacian(equalized, cv2.CV_64F)
    sharp = cv2.convertScaleAbs(equalized - 0.5 * laplacian)
    return sharp

# Lista de palavras esperadas
palavras_validas = ['TESTE', 'PALAVRA', 'TEXTO', 'VISÃO', 'OCR']

# Correção por similaridade
def corrigir_por_similaridade(texto):
    if not texto:
        return texto
    return min(palavras_validas, key=lambda p: Levenshtein.distance(texto, p))

# Extração principal
def extract_text_from_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    image_np = np.array(image)
    
    improved_img = preprocess_image(image_np)
    result = reader.readtext(improved_img, detail=0)
    
    if result:
        texto = ''.join([r.strip().upper() for r in result])
        texto_corrigido = correct_ocr_text(texto)
        texto_final = corrigir_por_similaridade(texto_corrigido)
        return texto_final
    
    return ""