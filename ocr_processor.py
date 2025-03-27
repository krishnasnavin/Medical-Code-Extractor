import cv2
import numpy as np
import logging
import pytesseract
from PIL import Image
import fitz  # PyMuPDF

logger = logging.getLogger(__name__)

def preprocess_image(file_path, file_extension):
    """
    Preprocess the image to improve OCR results
    
    Args:
        file_path: Path to the image file
        file_extension: File extension (pdf, jpg, png, etc.)
    
    Returns:
        Preprocessed image as a numpy array
    """
    try:
        # Handle PDFs differently
        if file_extension == 'pdf':
            logger.debug("Processing PDF document")
            # Open the PDF file
            pdf_document = fitz.open(file_path)
            
            # Get the first page
            page = pdf_document[0]
            
            # Render the page as an image
            pix = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))
            
            # Convert to numpy array
            img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)
            
            # Convert to grayscale if it's not already
            if pix.n > 1:
                img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        else:
            logger.debug(f"Processing image file: {file_extension}")
            # Read the image
            img = cv2.imread(file_path)
            
            # Convert to grayscale
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply image enhancement techniques
        # Noise removal
        img = cv2.GaussianBlur(img, (5, 5), 0)
        
        # Thresholding
        img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        
        # Dilation and erosion to remove noise
        kernel = np.ones((1, 1), np.uint8)
        img = cv2.dilate(img, kernel, iterations=1)
        img = cv2.erode(img, kernel, iterations=1)
        
        logger.debug("Image preprocessing completed successfully")
        return img
    
    except Exception as e:
        logger.error(f"Error during image preprocessing: {str(e)}")
        raise

def perform_ocr(image):
    """
    Perform OCR on the preprocessed image
    
    Args:
        image: Preprocessed image as a numpy array
    
    Returns:
        Extracted text as a string
    """
    try:
        logger.debug("Starting OCR process")
        
        # Convert the numpy array to a PIL Image
        pil_image = Image.fromarray(image)
        
        # Perform OCR
        custom_config = r'--oem 3 --psm 6 -l eng'
        text = pytesseract.image_to_string(pil_image, config=custom_config)
        
        logger.debug(f"OCR completed, extracted {len(text)} characters")
        return text
    
    except Exception as e:
        logger.error(f"Error during OCR: {str(e)}")
        raise
