import re
import os
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class CVInfo:
    """Data class to store extracted CV information"""
    title: str = ""
    skills: List[str] = None
    summary: List[str] = None
    highlights: List[str] = None
    accomplishments: List[str] = None
    experience: List[Dict[str, str]] = None
    education: List[Dict[str, str]] = None
    raw_text: str = ""
    
    def __post_init__(self):
        if self.skills is None:
            self.skills = []
        if self.summary is None:
            self.summary = []
        if self.highlights is None:
            self.highlights = []
        if self.accomplishments is None:
            self.accomplishments = []
        if self.experience is None:
            self.experience = []
        if self.education is None:
            self.education = []

class CVRegexExtractor:
    """Improved CV Information Extractor using Flexible Regular Expressions"""
    
    def __init__(self):
        self.setup_patterns()
    
    def setup_patterns(self):
        """Setup more flexible regex patterns for different sections"""
        
        # Title pattern 
        titles = r'[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*'

        self.title_pattern = re.compile(
            rf'^((?:{titles}))$',
            re.IGNORECASE
        )

        # More flexible section headers - simplified approach
        self.section_headers = {
            'skills': [r'\bskills?\b', r'\b\w+\s+skills?\b'],
            'summary': [r'\bsummary?\b', r'\b\w+\s+summary?\b', r'\bprofile?\b', r'\b\w+\s+profile?\b'],
            'highlights': [r'\bhighlights?\b', r'\b\w+\s+highlights?\b'],
            'accomplishments': [r'\baccomplishments?\b', r'\b\w+\s+accomplishments?\b'],
            'experience': [r'\bexperience?\b', r'\b\w+\s+experience?\b', r'\bwork\s+history?\b', r'\b\w+\s+work\s+history?\b'],
            'education': [r'\beducation?\b', r'\b\w+\s+education?\b']
        }
    
    def find_section_boundaries(self, text: str) -> Dict[str, tuple]:
        """Find all section headers and their positions"""
        sections_found = {}
        
        # Create a pattern that matches any section header
        all_patterns = []
        section_map = {}
        
        for section, patterns in self.section_headers.items():
            for pattern in patterns:
                full_pattern = rf'^\s*{pattern}\s*:?\s*$'
                all_patterns.append(full_pattern)
                section_map[full_pattern] = section
        
        combined_pattern = '|'.join([f'({pattern})' for pattern in all_patterns])
        
        lines = text.split('\n')
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            if not line_stripped:
                continue
                
            # Check each section pattern
            for section, patterns in self.section_headers.items():
                for pattern in patterns:
                    if re.match(rf'^\s*{pattern}\s*:?\s*$', line_stripped, re.IGNORECASE):
                        sections_found[section] = (i, line_stripped)
                        break
        
        return sections_found
    
    def extract_section_content_flexible(self, text: str, section_name: str) -> List[str]:
        """Extract ALL content from a section without any filtering"""
        lines = text.split('\n')
        section_boundaries = self.find_section_boundaries(text)
        
        if section_name not in section_boundaries:
            return []
        
        start_line = section_boundaries[section_name][0]
        
        # Find the next section boundary
        end_line = len(lines)
        for other_section, (line_num, _) in section_boundaries.items():
            if line_num > start_line and line_num < end_line:
                end_line = line_num
        
        # Extract ALL content between boundaries (no filtering)
        content_lines = []
        for i in range(start_line + 1, end_line):
            if i < len(lines):
                line = lines[i].strip()
                if line:  # Only skip completely empty lines
                    content_lines.append(line)
        
        return content_lines

    def read_extracted_text(self, file_path: str) -> str:
        """Read the extracted text from file"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    def extract_title(self, text: str) -> str:
        """Extract name or job title from the beginning of the CV"""
        lines = [l.strip() for l in text.splitlines() if l.strip()]

        for line in lines[:10]:
            # Skip known section headers
            is_section_header = False
            for section, patterns in self.section_headers.items():
                for pattern in patterns:
                    if re.match(rf'^\s*{pattern}\s*:?\s*$', line, re.IGNORECASE):
                        is_section_header = True
                        break
                if is_section_header:
                    break
            
            if is_section_header:
                break

            # Limit overly long lines (prevent summary sentences)
            if len(line.split()) > 4:
                continue

            # Only take if it matches title pattern
            if self.title_pattern.fullmatch(line):
                return line.title()

        return ""
    
    def extract_experience_flexible(self, text: str) -> List[Dict[str, str]]:
        """Extract ALL experience content and organize it simply"""
        experience_content = self.extract_section_content_flexible(text, 'experience')
        
        if not experience_content:
            return []
        
        # Simply return all content as one entry with all lines
        experiences = [{
            'content': experience_content,
            'raw_lines': experience_content
        }]
        
        return experiences
    

    def extract_education_flexible(self, text: str) -> List[Dict[str, str]]:
        """Extract ALL education content and organize it simply"""
        education_content = self.extract_section_content_flexible(text, 'education')
        
        if not education_content:
            return []
        
        # Simply return all content as one entry with all lines
        education_entries = [{
            'content': education_content,
            'raw_lines': education_content
        }]
        
        return education_entries

    # def extract_education(self, text: str) -> List[Dict[str, str]]:
    #     """Enhanced education extraction"""
    #     education_section = re.search(self.section_patterns['education'], text, re.DOTALL | re.IGNORECASE | re.MULTILINE)
        
    #     if not education_section:
    #         # Try alternative pattern
    #         alt_pattern = r'(?i)education\s*:?\s*\n(.*?)(?=\n\s*(?:experience|skills|summary|highlights|accomplishments)\s*:?\s*\n|\Z)'
    #         education_section = re.search(alt_pattern, text, re.DOTALL | re.IGNORECASE)
        
    #     if not education_section:
    #         # Fallback scan: detect education by degree keywords + institution
    #         fallback_matches = []
    #         for line in text.split('\n'):
    #             line = line.strip()
    #             if not line:
    #                 continue

    #             if 'university' in line.lower() or 'college' in line.lower():
    #                 if any(degree in line.lower() for degree in ['b.s', 'bachelor', 'm.s', 'master', 'phd', 'doctor']):
    #                     fallback_matches.append({
    #                         'year': '',  # No date, fallback only
    #                         'institution': line.split()[-3:],  # crude fallback
    #                         'degree': line.split(':')[0] if ':' in line else '',
    #                         'location': ''
    #                     })

    #         return fallback_matches
        
    #     content = education_section.group(1).strip()
    #     education_entries = []
        
    #     lines = content.split('\n')
    #     current_entry = {}
    #     additional_courses = []
        
    #     for line in lines:
    #         line = line.strip()
    #         if not line:
    #             continue
            
    #         # Check for year at the beginning of line
    #         year_match = re.match(r'^(\d{4})', line)
    #         if year_match:
    #             # Save previous entry if exists
    #             if current_entry:
    #                 if additional_courses:
    #                     current_entry['additional_courses'] = additional_courses
    #                 education_entries.append(current_entry.copy())
                
    #             # Start new entry
    #             current_entry = {
    #                 'year': year_match.group(1),
    #                 'institution': '',
    #                 'degree': '',
    #                 'location': ''
    #             }
    #             additional_courses = []
                
    #             # Extract institution and degree from the rest of the line
    #             remaining = line[year_match.end():].strip()
    #             if remaining:
    #                 # Look for institution patterns
    #                 institution_keywords = ['university', 'college', 'school', 'institute', 'academy', 'tech', 'career']
    #                 degree_keywords = ['diploma', 'bachelor', 'master', 'phd', 'certificate', 'associate', 'high school']
                    
    #                 # Split by common separators
    #                 parts = re.split(r'[-–,:]', remaining)
    #                 for part in parts:
    #                     part = part.strip()
    #                     if any(keyword in part.lower() for keyword in institution_keywords):
    #                         current_entry['institution'] = part
    #                     elif any(keyword in part.lower() for keyword in degree_keywords):
    #                         current_entry['degree'] = part
    #                     elif re.search(r'\b[A-Z][a-z]+\s*,\s*[A-Z][A-Z]\b', part):  # State pattern
    #                         current_entry['location'] = part
    #         else:
    #             # Check if it's additional course information
    #             if 'courses in' in line.lower() or 'classes in' in line.lower() or 'basic vocational' in line.lower():
    #                 additional_courses.append(line)
    #             elif current_entry and not current_entry.get('degree'):
    #                 # Might be degree information
    #                 if any(keyword in line.lower() for keyword in ['diploma', 'bachelor', 'master', 'phd', 'certificate']):
    #                     current_entry['degree'] = line
        
    #     # Don't forget the last entry
    #     if current_entry:
    #         if additional_courses:
    #             current_entry['additional_courses'] = additional_courses
    #         education_entries.append(current_entry)
        
    #     return education_entries

    def extract_education(self, text: str) -> List[Dict[str, str]]:
        """Enhanced education extraction"""

        education_section = re.search(
            r"Education\s*[\n\r]*(.*?)(?=\n\s*(Skills|Certifications|Experience|Projects|$))",
            text, re.DOTALL | re.IGNORECASE)
        
        if education_section:
            content = education_section.group(1)
        else:
            content = text

        
        content = education_section.group(1).strip()
        education_entries = []
        
        pattern = re.findall(
        r"(Bachelor|Master|Ph\.?D|Doctor)[\w\s\-]*?:\s*([A-Za-z&\s]+?),\s*(\d{4})\s+([A-Z][A-Za-z\s&]+University(?: College)?|University of [A-Za-z\s]+)\s*(.*)",
        content, re.IGNORECASE
        )
        results = []
        for degree, major, year, university, location in pattern:
            results.append({
                "degree": degree.strip(),
                "major": major.strip(),
                "year": year.strip(),
                "university": university.strip(),
                "location": location.strip()
            })

        return results
        

    
    def extract_cv_info(self, file_path: str) -> CVInfo:
        """Main method to extract all CV information with flexible parsing"""
        try:
            # Read the extracted text
            text = self.read_extracted_text(file_path)
            
            # Create CVInfo object
            cv_info = CVInfo()
            cv_info.raw_text = text
            
            # Extract title
            cv_info.title = self.extract_title(text)
            
            # Extract sections with flexible methods (ALL content under each section)
            cv_info.skills = self.extract_section_content_flexible(text, 'skills')
            cv_info.summary = self.extract_section_content_flexible(text, 'summary')
            cv_info.highlights = self.extract_section_content_flexible(text, 'highlights')
            cv_info.accomplishments = self.extract_section_content_flexible(text, 'accomplishments')
            
            # Extract experience and education (ALL content)
            cv_info.experience = self.extract_experience_flexible(text)
            cv_info.education = self.extract_education_flexible(text)
            
            return cv_info
            
        except Exception as e:
            raise Exception(f"Error extracting CV information: {e}")
    
    def format_output(self, cv_info: CVInfo) -> str:
        """Enhanced formatting of extracted information"""
        output = []
        
        if cv_info.title:
            output.append(cv_info.title)
            output.append("")

        if cv_info.summary:
            output.append("• Summary\n")            
            for summary_item in cv_info.summary:
                output.append(f"{summary_item}")
                output.append("")
        
        if cv_info.skills:
            output.append("• Skills\n")
            for skill in cv_info.skills:
                output.append(f"{skill}")
            output.append("")
        
        if cv_info.highlights:
            output.append("• Highlights\n")            
            for highlight in cv_info.highlights:
                output.append(f"{highlight}")
            output.append("")
        
        if cv_info.accomplishments:
            output.append("• Accomplishments\n")            
            for accomplishment in cv_info.accomplishments:
                output.append(f"{accomplishment}")
            output.append("")
        
        if cv_info.experience:
            output.append("• Experience\n")
            
            for exp in cv_info.experience:
                # Display all content under experience
                content = exp.get('content', [])
                for line in content:
                    output.append(f"{line}")
                output.append("")
        
        if cv_info.education:
            output.append("• Education\n")
            
            for edu in cv_info.education:
                # Display all content under education
                content = edu.get('content', [])
                for line in content:
                    output.append(f"{line}")
                output.append("")
        
        return '\n'.join(output)
    
    def save_formatted_output(self, cv_info: CVInfo, output_path: str):
        """Save formatted output to file"""
        formatted_text = self.format_output(cv_info)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(formatted_text)
        
        print(f"Formatted CV information saved to: {output_path}")

# Usage functions
def extract_cv_info_from_file(input_file: str) -> CVInfo:
    """Extract CV information from extracted text file"""
    extractor = CVRegexExtractor()
    return extractor.extract_cv_info(input_file)

def extract_and_save_cv_info(input_file: str, output_file: str) -> CVInfo:
    """Extract CV information and save formatted output"""
    extractor = CVRegexExtractor()
    cv_info = extractor.extract_cv_info(input_file)
    extractor.save_formatted_output(cv_info, output_file)
    return cv_info