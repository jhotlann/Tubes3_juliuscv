import os
import sys
import argparse
from pdf_extractor import PDFTextExtractor
from regex import CVRegexExtractor, CVInfo

class IntegratedCVProcessor:
    """Integrated processor that handles PDF extraction and CV information extraction"""
    
    def __init__(self):
        self.pdf_extractor = PDFTextExtractor()
        self.regex_extractor = CVRegexExtractor()
    
    def process_pdf(self, pdf_path: str, output_dir: str = None) -> CVInfo:
        """
        Process a PDF file: extract text, then extract CV information
        
        Args:
            pdf_path: Path to the PDF file
            output_dir: Directory to save intermediate and final files
        
        Returns:
            CVInfo object with extracted information
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        # Set default output directory
        if output_dir is None:
            output_dir = os.path.dirname(pdf_path)
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate file names
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        raw_text_file = os.path.join(output_dir, f"{base_name}_raw_text.txt")
        clean_text_file = os.path.join(output_dir, f"{base_name}_clean_text.txt")
        regex_output_file = os.path.join(output_dir, f"{base_name}_regex_extracted.txt")
        
        print(f"Processing PDF: {pdf_path}")
        print(f"Output directory: {output_dir}")
        
        try:
            # Step 1: Extract raw text (no cleaning for regex processing)
            print("\n[1/3] Extracting raw text from PDF...")
            raw_text = self.pdf_extractor.extract_text(pdf_path, clean=False)
            
            # Save raw text
            with open(raw_text_file, 'w', encoding='utf-8') as f:
                f.write(raw_text)
            print(f"Raw text saved to: {raw_text_file}")
            
            # Step 2: Extract clean text (for pattern matching)
            print("\n[2/3] Extracting clean text from PDF...")
            clean_text = self.pdf_extractor.extract_text(pdf_path, clean=True)
            
            # Save clean text
            with open(clean_text_file, 'w', encoding='utf-8') as f:
                f.write(clean_text)
            print(f"Clean text saved to: {clean_text_file}")
            
            # Step 3: Extract CV information using regex
            print("\n[3/3] Extracting CV information using regex...")
            cv_info = self.regex_extractor.extract_cv_info(raw_text_file)
            
            # Save formatted CV information
            self.regex_extractor.save_formatted_output(cv_info, regex_output_file)
            
            # Print summary
            self.print_extraction_summary(cv_info)
            
            return cv_info
            
        except Exception as e:
            raise Exception(f"Error processing PDF: {e}")
    
    def process_multiple_pdfs(self, pdf_directory: str, output_dir: str = None) -> dict:
        """
        Process multiple PDF files in a directory
        
        Args:
            pdf_directory: Directory containing PDF files
            output_dir: Directory to save all outputs
        
        Returns:
            Dictionary mapping PDF filenames to CVInfo objects
        """
        if not os.path.exists(pdf_directory):
            raise FileNotFoundError(f"Directory not found: {pdf_directory}")
        
        # Set default output directory
        if output_dir is None:
            output_dir = os.path.join(pdf_directory, "extracted_cv_info")
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Find all PDF files
        pdf_files = [f for f in os.listdir(pdf_directory) if f.lower().endswith('.pdf')]
        
        if not pdf_files:
            print(f"No PDF files found in {pdf_directory}")
            return {}
        
        print(f"Found {len(pdf_files)} PDF files to process")
        
        results = {}
        for i, pdf_file in enumerate(pdf_files, 1):
            pdf_path = os.path.join(pdf_directory, pdf_file)
            print(f"\n{'='*60}")
            print(f"Processing {i}/{len(pdf_files)}: {pdf_file}")
            print(f"{'='*60}")
            
            try:
                cv_info = self.process_pdf(pdf_path, output_dir)
                results[pdf_file] = cv_info
                print(f"Successfully processed {pdf_file}")
            except Exception as e:
                print(f"✗ Error processing {pdf_file}: {e}")
                results[pdf_file] = None
        
        # Print overall summary
        successful = sum(1 for result in results.values() if result is not None)
        print(f"\n{'='*60}")
        print(f"PROCESSING SUMMARY")
        print(f"{'='*60}")
        print(f"Total files: {len(pdf_files)}")
        print(f"Successfully processed: {successful}")
        print(f"Failed: {len(pdf_files) - successful}")
        
        return results
    
    def print_extraction_summary(self, cv_info: CVInfo):
        """Print a summary of extracted information"""
        print(f"EXTRACTION SUMMARY:")
        print(f"Title: {cv_info.title or 'Not found'}")
        print(f"Skills: {len(cv_info.skills)} items")
        print(f"Summary: {len(cv_info.summary)} items")
        print(f"Highlights: {len(cv_info.highlights)} items")
        print(f"Accomplishments: {len(cv_info.accomplishments)} items")
        print(f"Experience: {len(cv_info.experience)} entries")
        print(f"Education: {len(cv_info.education)} entries")

def main():
    """Main function with command line interface"""
    parser = argparse.ArgumentParser(description='Integrated CV Processor - Extract and analyze CV information from PDF files')
    parser.add_argument('input', help='PDF file or directory containing PDF files')
    parser.add_argument('-o', '--output', help='Output directory for extracted files')
    parser.add_argument('--single', action='store_true', help='Process single PDF file (default: auto-detect)')
    parser.add_argument('--multiple', action='store_true', help='Process multiple PDF files in directory')
    parser.add_argument('--preview', action='store_true', help='Show preview of extracted information')
    
    args = parser.parse_args()
    
    processor = IntegratedCVProcessor()
    
    try:
        # Determine if input is file or directory
        if os.path.isfile(args.input) and args.input.lower().endswith('.pdf'):
            # Single file mode
            print("Processing single PDF file...")
            cv_info = processor.process_pdf(args.input, args.output)
            
            if args.preview:
                print(f"\n{'='*50}")
                print("EXTRACTED INFORMATION PREVIEW:")
                print(f"{'='*50}")
                formatted_output = processor.regex_extractor.format_output(cv_info)
                preview_length = min(1500, len(formatted_output))
                print(formatted_output[:preview_length] + "..." if len(formatted_output) > preview_length else formatted_output)
        
        elif os.path.isdir(args.input):
            # Multiple files mode
            print("Processing multiple PDF files...")
            results = processor.process_multiple_pdfs(args.input, args.output)
            
            if args.preview and results:
                # Show preview of first successful result
                for pdf_file, cv_info in results.items():
                    if cv_info is not None:
                        print(f"\n{'='*50}")
                        print(f"SAMPLE PREVIEW ({pdf_file}):")
                        print(f"{'='*50}")
                        formatted_output = processor.regex_extractor.format_output(cv_info)
                        preview_length = min(1000, len(formatted_output))
                        print(formatted_output[:preview_length] + "..." if len(formatted_output) > preview_length else formatted_output)
                        break
        
        else:
            print(f"Error: '{args.input}' is not a valid PDF file or directory")
            return 1
        
        print(f"\nProcessing completed successfully!")
        return 0
        
    except Exception as e:
        print(f"Error: {e}")
        return 1

# Example usage functions
def process_single_pdf(pdf_path: str, output_dir: str = None) -> CVInfo:
    """Process a single PDF file"""
    processor = IntegratedCVProcessor()
    return processor.process_pdf(pdf_path, output_dir)

def process_pdf_directory(pdf_directory: str, output_dir: str = None) -> dict:
    """Process all PDF files in a directory"""
    processor = IntegratedCVProcessor()
    return processor.process_multiple_pdfs(pdf_directory, output_dir)

if __name__ == "__main__":
    # Check if running as script with arguments
    if len(sys.argv) > 1:
        exit_code = main()
        sys.exit(exit_code)
    else:
        # Show usage examples
        print("Integrated CV Processor")
        print("="*50)
        print("\nUsage examples:")
        print("1. Process single PDF:")
        print("   python integrated_cv_processor.py data/10276858.pdf -o output/")
        print("   python integrated_cv_processor.py data/10276858.pdf --preview")
        
        print("\n2. Process multiple PDFs:")
        print("   python integrated_cv_processor.py data/ -o output/")
        print("   python integrated_cv_processor.py data/ --preview")
        
        print("\n3. Python usage:")
        print("   from integrated_cv_processor import process_single_pdf")
        print("   cv_info = process_single_pdf('data/10276858.pdf')")
        print("   print(cv_info.title)")
        print("   print(cv_info.skills)")
        
        print("\nCommand line options:")
        print("  -o, --output    : Output directory")
        print("  --single        : Force single file mode")
        print("  --multiple      : Force multiple files mode")  
        print("  --preview       : Show preview of extracted information")
        
        # Show example with existing file if available
        if os.path.exists("data/10276858.pdf"):
            print(f"\n" + "="*50)
            print("RUNNING EXAMPLE WITH EXISTING FILE:")
            print("="*50)
            try:
                processor = IntegratedCVProcessor()
                cv_info = processor.process_pdf("data/10276858.pdf")
                print("\nExample completed successfully!")
            except Exception as e:
                print(f"Error in example: {e}")