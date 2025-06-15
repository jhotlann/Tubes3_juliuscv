import pdfplumber
import re
import os

class PDFTextExtractor:
   
    def extract_text(self, pdf_path: str, clean: bool = True) -> str:
        """
            Extract text as a single string
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        text = ""
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    print(f"Processing page {page_num}...")
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + " "
        except Exception as e:
            raise Exception(f"Failed to extract text from PDF: {e}")
        
        if clean:
            text = self.clean_text(text)
        
        return text
    
    def clean_text(self, text: str) -> str:
        """
        Clean the extracted text:
        - Converting to lowercase
        - Removing extra whitespaces
        - Removing special characters except spaces
        - Removing line breaks and tabs
        """
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove line breaks, tabs, and multiple spaces
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep letters, numbers, and spaces
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # Remove extra spaces again after special character removal
        text = re.sub(r'\s+', ' ', text)
        
        # Strip leading/trailing spaces
        text = text.strip()
        
        return text
    
    

def extract_pdf_to_string(pdf_path: str, clean: bool = True) -> str:
    """
        Extracted text as string
    """
    extractor = PDFTextExtractor()
    return extractor.extract_text(pdf_path, clean)
