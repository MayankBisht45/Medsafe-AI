import os
import pytesseract
from PIL import Image

# For Windows users: Point pytesseract directly to executable path
# Uncomment and update the line below if Tesseract is not in your System PATH:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(image_file):
    """
    Processes an uploaded image file and returns extracted OCR text.
    """
    try:
        # Load image using PIL
        img = Image.open(image_file)
        
        # Perform OCR
        raw_text = pytesseract.image_to_string(img)
        
        # Clean up empty lines
        cleaned_text = "\n".join([line.strip() for line in raw_text.splitlines() if line.strip()])
        
        return cleaned_text if cleaned_text else "No readable text found in image."
    except Exception as e:
        return f"Error processing image with Tesseract: {str(e)}"