import cv2
import numpy as np
import pytesseract
from app.utils import parse_lab_tests, preprocess_text


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_lab_tests(image_bytes):
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    
    processed_img = cv2.GaussianBlur(thresh, (3, 3), 0)

    text = pytesseract.image_to_string(processed_img)

    cleaned_text = preprocess_text(text)
  
    tests = parse_lab_tests(cleaned_text)
    
    return tests