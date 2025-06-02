import pdfplumber
import re
import argparse
import os
from typing import Optional

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
    
    def extract_to_file(self, pdf_path: str, output_path: str, clean: bool = True):
        """
            Extract text from PDF and save to a file.
        """
        print(f"Extracting text from: {pdf_path}")
        text = self.extract_text(pdf_path, clean)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        
        print(f"Text extracted and saved to: {output_path}")
        print(f"Total characters: {len(text)}")
        print(f"Total words: {len(text.split())}")
        return text

def main():
    parser = argparse.ArgumentParser(description='Extract text from PDF files using pdfplumber')
    parser.add_argument('pdf_path', help='Path to the PDF file')
    parser.add_argument('-o', '--output', help='Output text file path')
    parser.add_argument('--no-clean', action='store_true',
                       help='Skip text cleaning')
    parser.add_argument('--preview', action='store_true',
                       help='Show preview of extracted text')
    
    args = parser.parse_args()
    
    extractor = PDFTextExtractor()
    
    try:
        # Extract text
        text = extractor.extract_text(
            args.pdf_path, 
            clean=not args.no_clean
        )
        
        # Show preview if requested
        if args.preview:
            preview_length = min(500, len(text))
            print("\n" + "="*50)
            print("TEXT PREVIEW:")
            print("="*50)
            print(text[:preview_length] + "..." if len(text) > preview_length else text)
            print("="*50)
        
        # Save to file if output path specified
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"\nText saved to: {args.output}")
        else:
            # If no output file, just print the text
            print("\n" + "="*50)
            print("EXTRACTED TEXT:")
            print("="*50)
            print(text)
        
        print(f"\nExtraction completed!")
        print(f"Total characters: {len(text)}")
        print(f"Total words: {len(text.split())}")
        
    except Exception as e:
        print(f"Error: {e}")

# Example usage functions
def extract_pdf_to_string(pdf_path: str, clean: bool = True) -> str:
    """
        Extracted text as string
    """
    extractor = PDFTextExtractor()
    return extractor.extract_text(pdf_path, clean)

def extract_pdf_to_file(pdf_path: str, output_path: str, clean: bool = True) -> str:
    """ 
        Extracted text as string
    """
    extractor = PDFTextExtractor()
    return extractor.extract_to_file(pdf_path, output_path, clean)


if __name__ == "__main__":
    # Check if running as script with arguments
    import sys
    if len(sys.argv) > 1:
        main()
    else:
        # Required library:
        # pip install pdfplumber
         
        print("\nExample usage:")
        
        print(f"\n1. Basic extraction:")
        print(f"from pdf_extractor import extract_pdf_to_string")
        print(f"text = extract_pdf_to_string('your_file.pdf')")
        print(f"print(text)")
        
        print(f"\n2. Extract to file:")
        print(f"from pdf_extractor import extract_pdf_to_file")
        print(f"text = extract_pdf_to_file('your_file.pdf', 'output.txt')")
        
        print(f"\n3. Command line usage:")
        print(f"python pdf_extractor.py your_file.pdf -o output.txt --preview")
        print(f"python pdf_extractor.py your_file.pdf --preview")
        
        print(f"\n4. Without text cleaning:")
        print(f"text = extract_pdf_to_string('your_file.pdf', clean=False)")
        
        print("\nCommand line options:")
        print("  -o, --output    : Save to text file")
        print("  --no-clean     : Skip text cleaning")
        print("  --preview      : Show text preview")