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
    """Improved CV Information Extractor using Regular Expressions"""
    
    def __init__(self):
        self.setup_patterns()
    
    def setup_patterns(self):
        """Setup improved regex patterns for different sections"""
        
        # Title pattern 
        name_pat = r'[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*'
        titles   = r'Chef|Engineer|Developer|Manager|Analyst|Designer|Coordinator|' \
                   r'Specialist|Assistant|Director|Executive|Officer|Representative|' \
                   r'Consultant|Supervisor|Administrator|Cook'

        self.title_pattern = re.compile(
            rf'^(?:{name_pat}|(?:{titles}))$',
            re.IGNORECASE
        )

        # Improved section headers patterns - more flexible matching
        self.section_patterns = {
            'skills': r'(?i)^\s*(?:skills?|keterampilan|keahlian)\s*:?' +
                      r'\s*$\n(.*?)(?=^\s*(?:summary|ringkasan|tentang saya|about me|highlights|pencapaian|accomplishments|pengalaman|experience|pendidikan|education)\s*:?' +
                      r'\s*$|\Z)',

            'summary': r'(?i)^\s*(?:summary|ringkasan|tentang saya|about me)\s*:?' +
                       r'\s*$\n(.*?)(?=^\s*(?:skills|keterampilan|keahlian|highlights|pencapaian|accomplishments|experience|pengalaman|pendidikan|education)\s*:?' +
                       r'\s*$|\Z)',

            'highlights': r'(?i)^\s*(?:highlights?)\s*:?' +
                          r'\s*$\n(.*?)(?=^\s*(?:skills|keterampilan|keahlian|summary|ringkasan|tentang saya|about me|accomplishments|pencapaian|experience|pengalaman|pendidikan|education)\s*:?' +
                          r'\s*$|\Z)',

            'accomplishments': r'(?i)^\s*(?:accomplishments?|pencapaian)\s*:?' +
                               r'\s*$\n(.*?)(?=^\s*(?:skills|keterampilan|keahlian|summary|ringkasan|tentang saya|about me|highlights|experience|pengalaman|pendidikan|education)\s*:?' +
                               r'\s*$|\Z)',

            'experience': r'(?i)^\s*(?:experience|pengalaman)\s*:?' +
                          r'\s*$\n(.*?)(?=^\s*(?:skills|keterampilan|keahlian|summary|ringkasan|tentang saya|about me|highlights|accomplishments|pencapaian|pendidikan|education)\s*:?' +
                          r'\s*$|\Z)',

            'education': r'(?i)^\s*(?:education|pendidikan)\s*:?' +
                          r'\s*$\n(.*?)(?=^\s*(?:skills|keterampilan|keahlian|summary|ringkasan|tentang saya|about me|highlights|accomplishments|pencapaian|experience|pengalaman)\s*:?' +
                          r'\s*$|\Z)'
        }
        
        # Improved date patterns
        self.date_pattern = re.compile(
            r'('
                # Numeric ISO & variants: YYYY-MM-DD, YYYY/MM/DD, YYYY.MM.DD
                r'\d{4}[-\/\.]\d{1,2}[-\/\.]\d{1,2}'
            r'|'
                # DMY numeric: DD-MM-YYYY, DD/MM/YYYY, DD.MM.YYYY
                r'\d{1,2}[-\/\.]\d{1,2}[-\/\.]\d{4}'
            r'|'
                # Short numeric no year: DD/MM, MM/DD
                r'\d{1,2}[-\/\.]\d{1,2}'
            r'|'
                # Abbrev month-day (En & Id): 09-Nov, 9-Des, 9-Agt, etc.
                r'\d{1,2}-(?:Jan|Feb|Mar|Apr|Mei|Jun|Jul|Aug|Agt|Sep|Okt|Oct|Nov|Des|Dec)'
            r'|'
                # Full named day-month-year (En & Id)
                r'\d{1,2}\s+'
                r'(?:January|February|March|April|May|June|July|August|September|October|November|December'
                r'|Januari|Februari|Maret|April|Mei|Juni|Juli|Agustus|September|Oktober|November|Desember)'
                r'\s+\d{4}'
            r'|'
                # US style named month-day-year (En & Id)
                r'(?:January|February|March|April|May|June|July|August|September|October|November|December'
                r'|Januari|Februari|Maret|April|Mei|Juni|Juli|Agustus|September|Oktober|November|Desember)'
                r'\s+\d{1,2},\s*\d{4}'
            r'|'
                # Month Year full (En & Id)
                r'(?:January|February|March|April|May|June|July|August|September|October|November|December'
                r'|Januari|Februari|Maret|April|Mei|Juni|Juli|Agustus|September|Oktober|November|Desember)'
                r'\s+\d{4}'
            r'|'
                # Month Year abbreviated (En & Id), e.g. Jan 2025, Agt 2026
                r'(?:Jan|Feb|Mar|Apr|Mei|Jun|Jul|Aug|Agt|Sep|Okt|Nov|Des|Dec)'
                r'\s+\d{4}'
            r')'
            r'\s*[-—]\s*'
            r'('
                # ulangi semua format tanggal kedua + Present/Current
                r'\d{4}[-\/\.]\d{1,2}[-\/\.]\d{1,2}'
            r'|'
                r'\d{1,2}[-\/\.]\d{1,2}[-\/\.]\d{4}'
            r'|'
                r'\d{1,2}[-\/\.]\d{1,2}'
            r'|'
                r'\d{1,2}-(?:Jan|Feb|Mar|Apr|Mei|Jun|Jul|Aug|Agt|Sep|Okt|Oct|Nov|Des|Dec)'
            r'|'
                r'\d{1,2}\s+'
                r'(?:January|February|March|April|May|June|July|August|September|October|November|December'
                r'|Januari|Februari|Maret|April|Mei|Juni|Juli|Agustus|September|Oktober|November|Desember)'
                r'\s+\d{4}'
            r'|'
                r'(?:January|February|March|April|May|June|July|August|September|October|November|December'
                r'|Januari|Februari|Maret|April|Mei|Juni|Juli|Agustus|September|Oktober|November|Desember)'
                r'\s+\d{1,2},\s*\d{4}'
            r'|'
                r'(?:January|February|March|April|May|June|July|August|September|October|November|December'
                r'|Januari|Februari|Maret|April|Mei|Juni|Juli|Agustus|September|Oktober|November|Desember)'
                r'\s+\d{4}'
            r'|'
                # Month Year abbreviated (En & Id)
                r'(?:Jan|Feb|Mar|Apr|Mei|Jun|Jul|Aug|Agt|Sep|Okt|Nov|Des|Dec)'
                r'\s+\d{1,2},\s*\d{4}'
            r'|'
                r'(?:Jan|Feb|Mar|Apr|Mei|Jun|Jul|Aug|Agt|Sep|Okt|Nov|Des|Dec)'
                r'\s+\d{4}'
            r'|'
                r'Present|Current'
            r')',
            re.IGNORECASE
        )
        self.year_pattern = r'\b(19|20)\d{2}\b'
        
        # Company and position patterns
        self.company_position_pattern = r'([A-Za-z\s&,.-]+)\s+([\w\s/]+)$'
        
        # Education patterns
        self.degree_pattern = re.compile(
            r'(?i)\b(?:'
            r'Bachelor|B\.Sc|BSc|Sarjana|S\.1|S1'
            r'|Master|M\.Sc|MSc|Magister|S\.2|S2'
            r'|PhD|Doctorate|Doktor|S\.3|S3'
            r'|Diploma\s?[I|II|III|IV]?|Dipl\.\s?[I|II|III|IV]?'
            r'|Certificate|Cert\.?|Associate|High\s?School|Vocational|Professional'
            r')\b'                    
            r'.*?'                  
            r'(?:in|of|on|:)\s*'         
            r'([A-Za-z0-9\s&,\.\-]+)',    
            re.IGNORECASE
        )

        self.institution_pattern = re.compile(
            r'([A-Za-z0-9\s&,\.\-]+?'      
            r'(?:'
            r'University|Universitas'
            r'|College|Sekolah'
            r'|School|Institut|Institute'
            r'|Academy|Akademi'
            r'|Tech(?:nology)?|Teknologi'
            r'|Polytechnic|Politeknik'
            r'|Vocational' 
            r')\b)',                      
            re.IGNORECASE
        )
    
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
            # skip section headers
            if line.upper() in ('SKILLS', 'SUMMARY', 'HIGHLIGHTS', 'ACCOMPLISHMENTS',
                                'EXPERIENCE', 'EDUCATION'):
                break

            # batasi baris yang terlalu panjang (mencegah kalimat summary)
            if len(line.split()) > 4:
                continue

            # hanya ambil jika full‑match pattern
            if self.title_pattern.fullmatch(line):
                # kembalikan Title Case untuk readability
                return line.title()

        return ""
    
    def extract_section_content(self, text: str, section_name: str) -> List[str]:
        """Extract content from a specific section with improved parsing"""
        pattern = self.section_patterns.get(section_name, '')
        if not pattern:
            return []
        
        # Use multiline flag for better section matching
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE | re.MULTILINE)
        if not match:
            return []
        
        content = match.group(1).strip()
        if not content:
            return []
        
        # Split content into lines and clean
        lines = []
        for line in content.split('\n'):
            line = line.strip()
            # Skip empty lines and date-only lines
            if line and not re.match(r'^\d{1,2}\/\d{4}\s*[-—]\s*\d{1,2}\/\d{4}', line):
                lines.append(line)
        
        return lines
    
    def extract_accomplishments(self, text: str) -> List[str]:
        """Enhanced accomplishments extraction"""
        # Try the section pattern first
        accomplishments = self.extract_section_content(text, 'accomplishments')
        
        if not accomplishments:
            # Alternative patterns for accomplishments
            alt_patterns = [
                r'(?i)accomplishments?\s*:?\s*\n((?:.*\n?)*?)(?=\n\s*(?:experience|education|skills|summary|highlights)\s*:?\s*\n|\Z)',
                r'(?i)achievements?\s*:?\s*\n((?:.*\n?)*?)(?=\n\s*(?:experience|education|skills|summary|highlights)\s*:?\s*\n|\Z)'
            ]
            
            for pattern in alt_patterns:
                match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
                if match:
                    content = match.group(1).strip()
                    if content:
                        accomplishments = [line.strip() for line in content.split('\n') if line.strip()]
                        break
        
        return accomplishments
    
    def extract_experience(self, text: str) -> List[Dict[str, str]]:
        """Enhanced experience extraction with better date and company parsing"""
        # First try to find the experience section
        experience_section = re.search(self.section_patterns['experience'], text, re.DOTALL | re.IGNORECASE | re.MULTILINE)
        
        if not experience_section:
            # Try alternative patterns
            alt_pattern = r'(?i)experience\s*:?\s*\n(.*?)(?=\n\s*(?:education|skills|summary|highlights|accomplishments)\s*:?\s*\n|\Z)'
            experience_section = re.search(alt_pattern, text, re.DOTALL | re.IGNORECASE)
        
        if not experience_section:
            return []
        
        content = experience_section.group(1).strip()
        experiences = []
        
        # Look for date patterns to identify job entries
        date_pattern = r'(\d{1,2}\/\d{4})\s*[-–]\s*(\d{1,2}\/\d{4}|Present|Current)'
        
        # Split content by lines and group by date patterns
        lines = content.split('\n')
        current_job = {}
        current_responsibilities = []
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            if not line:
                i += 1
                continue
            
            # Check if line contains a date range
            date_match = re.search(date_pattern, line)
            if date_match:
                # Save previous job if exists
                if current_job:
                    current_job['responsibilities'] = current_responsibilities[:5]  # Limit to 5 responsibilities
                    experiences.append(current_job.copy())
                
                # Start new job entry
                current_job = {
                    'date_range': f"{date_match.group(1)} - {date_match.group(2)}",
                    'company': '',
                    'position': '',
                    'responsibilities': []
                }
                current_responsibilities = []
                
                # Look for company and position in next line
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    if next_line and not re.search(date_pattern, next_line):
                        # Parse company and position
                        parts = next_line.split()
                        if len(parts) >= 2:
                            # Look for position keywords at the end
                            position_keywords = ['chef', 'cook', 'manager', 'assistant', 'supervisor', 'coordinator', 'specialist', 'server', 'prep']
                            position_found = False
                            
                            # Find position by looking for keywords
                            for j, part in enumerate(reversed(parts)):
                                if any(keyword in part.lower() for keyword in position_keywords):
                                    # Position is from this word to the end
                                    pos_start = len(parts) - j - 1
                                    current_job['position'] = ' '.join(parts[pos_start:])
                                    current_job['company'] = ' '.join(parts[:pos_start]) if pos_start > 0 else next_line
                                    position_found = True
                                    break
                            
                            if not position_found:
                                # Fallback: assume last word is position
                                current_job['position'] = parts[-1]
                                current_job['company'] = ' '.join(parts[:-1])
                        else:
                            current_job['company'] = next_line
                        
                        i += 1  # Skip the company/position line
            else:
                # This is likely a responsibility or description
                if current_job and line:
                    current_responsibilities.append(line)
            
            i += 1
        
        # Don't forget the last job
        if current_job:
            current_job['responsibilities'] = current_responsibilities[:5]
            experiences.append(current_job)
        
        return experiences
    
    def extract_education(self, text: str) -> List[Dict[str, str]]:
        """Enhanced education extraction"""
        education_section = re.search(self.section_patterns['education'], text, re.DOTALL | re.IGNORECASE | re.MULTILINE)
        
        if not education_section:
            # Try alternative pattern
            alt_pattern = r'(?i)education\s*:?\s*\n(.*?)(?=\n\s*(?:experience|skills|summary|highlights|accomplishments)\s*:?\s*\n|\Z)'
            education_section = re.search(alt_pattern, text, re.DOTALL | re.IGNORECASE)
        
        if not education_section:
            return []
        
        content = education_section.group(1).strip()
        education_entries = []
        
        lines = content.split('\n')
        current_entry = {}
        additional_courses = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check for year at the beginning of line
            year_match = re.match(r'^(\d{4})', line)
            if year_match:
                # Save previous entry if exists
                if current_entry:
                    if additional_courses:
                        current_entry['additional_courses'] = additional_courses
                    education_entries.append(current_entry.copy())
                
                # Start new entry
                current_entry = {
                    'year': year_match.group(1),
                    'institution': '',
                    'degree': '',
                    'location': ''
                }
                additional_courses = []
                
                # Extract institution and degree from the rest of the line
                remaining = line[year_match.end():].strip()
                if remaining:
                    # Look for institution patterns
                    institution_keywords = ['university', 'college', 'school', 'institute', 'academy', 'tech', 'career']
                    degree_keywords = ['diploma', 'bachelor', 'master', 'phd', 'certificate', 'associate', 'high school']
                    
                    # Split by common separators
                    parts = re.split(r'[-–,:]', remaining)
                    for part in parts:
                        part = part.strip()
                        if any(keyword in part.lower() for keyword in institution_keywords):
                            current_entry['institution'] = part
                        elif any(keyword in part.lower() for keyword in degree_keywords):
                            current_entry['degree'] = part
                        elif re.search(r'\b[A-Z][a-z]+\s*,\s*[A-Z][A-Z]\b', part):  # State pattern
                            current_entry['location'] = part
            else:
                # Check if it's additional course information
                if 'courses in' in line.lower() or 'classes in' in line.lower() or 'basic vocational' in line.lower():
                    additional_courses.append(line)
                elif current_entry and not current_entry.get('degree'):
                    # Might be degree information
                    if any(keyword in line.lower() for keyword in ['diploma', 'bachelor', 'master', 'phd', 'certificate']):
                        current_entry['degree'] = line
        
        # Don't forget the last entry
        if current_entry:
            if additional_courses:
                current_entry['additional_courses'] = additional_courses
            education_entries.append(current_entry)
        
        return education_entries
    
    def extract_cv_info(self, file_path: str) -> CVInfo:
        """Main method to extract all CV information with improved parsing"""
        try:
            # Read the extracted text
            text = self.read_extracted_text(file_path)
            
            # Create CVInfo object
            cv_info = CVInfo()
            cv_info.raw_text = text
            
            # Extract title
            cv_info.title = self.extract_title(text)
            
            # Extract sections with improved methods
            cv_info.skills = self.extract_section_content(text, 'skills')
            cv_info.summary = self.extract_section_content(text, 'summary')
            cv_info.highlights = self.extract_section_content(text, 'highlights')
            cv_info.accomplishments = self.extract_accomplishments(text)
            
            # Extract experience and education with enhanced parsing
            cv_info.experience = self.extract_experience(text)
            cv_info.education = self.extract_education(text)
            
            return cv_info
            
        except Exception as e:
            raise Exception(f"Error extracting CV information: {e}")
    
    def format_output(self, cv_info: CVInfo) -> str:
        """Enhanced formatting of extracted information"""
        output = []
        
        if cv_info.title:
            output.append(cv_info.title)
            output.append("")
        
        if cv_info.skills:
            output.append("Skills\n")
            
            for skill in cv_info.skills:
                output.append(f"{skill}")
            output.append("")
        
        if cv_info.summary:
            output.append("Summary\n")            
            for summary_item in cv_info.summary:
                output.append(f"{summary_item}")
            output.append("")
        
        if cv_info.highlights:
            output.append("Highlights\n")            
            for highlight in cv_info.highlights:
                output.append(f"{highlight}")
            output.append("")
        
        if cv_info.accomplishments:
            output.append("Accomplishments\n")            
            for accomplishment in cv_info.accomplishments:
                output.append(f"{accomplishment}")
            output.append("")
        
        if cv_info.experience:
            output.append("Experience\n")
            
            for i, exp in enumerate(cv_info.experience, 1):
                output.append(f"{exp.get('date_range', 'Date not specified')}")
                output.append(f"Position: {exp.get('position', 'Position not specified')}")
                output.append(f"Company: {exp.get('company', 'Company not specified')}")
                
                responsibilities = exp.get('responsibilities', [])
                if responsibilities:
                    output.append("Responsibilities:")
                    for resp in responsibilities:
                        output.append(f"{resp}")
                output.append("")
        
        if cv_info.education:
            output.append("Education\n")
            
            for i, edu in enumerate(cv_info.education, 1):
                output.append(f"{edu.get('year', 'Year not specified')}")
                if edu.get('institution'):
                    output.append(f"Institution: {edu.get('institution')}")
                if edu.get('degree'):
                    output.append(f"Degree: {edu.get('degree')}")
                if edu.get('location'):
                    output.append(f"Location: {edu.get('location')}")
                
                additional_courses = edu.get('additional_courses', [])
                if additional_courses:
                    output.append("Additional Courses:")
                    for course in additional_courses:
                        output.append(f"{course}")
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