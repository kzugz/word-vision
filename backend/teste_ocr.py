import requests
import cv2
import numpy as np
from PIL import Image

# Carrega a imagem local
image_path = "../frontend/assets/word.png"
with open(image_path, "rb") as f:
    image_bytes = f.read()

# Envia para o backend
response = requests.post("http://127.0.0.1:5000/ocr", files={"image": ("word.png", image_bytes)})

# Imprime o resultado
print(response.json())

# Visualiza as caixas de texto detectadas
import easyocr

reader = easyocr.Reader(['pt'])

image_np = np.array(Image.open(image_path).convert("RGB"))
results = reader.readtext(image_np)

for (bbox, text, prob) in results:
    (tl, tr, br, bl) = bbox
    tl = tuple(map(int, tl))
    br = tuple(map(int, br))
    cv2.rectangle(image_np, tl, br, (0, 255, 0), 2)
    cv2.putText(image_np, text, tl, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

cv2.imshow("OCR Bounding Boxes", image_np)
cv2.waitKey(0)
cv2.destroyAllWindows()