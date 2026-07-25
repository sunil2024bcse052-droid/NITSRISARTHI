import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Users\asus\OneDrive\Desktop\nitsrisarthi-rag\tesseract.exe"

image_path = r"C:\Users\asus\OneDrive\Desktop\nitsrisarthi-rag\WhatsApp Image 2025-11-03 at 11.35.21 PM.jpeg"

with Image.open(image_path) as img:
    text = pytesseract.image_to_string(img)

print("----- RAW OCR OUTPUT -----")
print(text)
print("----- END -----")
print(f"\nTotal characters extracted: {len(text)}")