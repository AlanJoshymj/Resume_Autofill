import os
import json
from typing import Dict, Any
from openai import OpenAI
import PyPDF2
from docx import Document
import io

class ResumeParser:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "your_openai_api_key_here":
            raise ValueError(
                "OpenAI API key not found. Please set OPENAI_API_KEY in your .env file. "
                "Copy env_template.txt to .env and add your actual API key."
            )
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-3.5-turbo"
        
    async def parse_resume(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """
        Parse resume file and extract structured data using OpenAI
        """
        try:
            # Extract text from file
            text = self._extract_text(file_content, filename)
            
            if not text.strip():
                raise ValueError("No text could be extracted from the resume")
            
            # Use OpenAI to structure the data
            structured_data = await self._structure_with_openai(text)
            
            return structured_data
            
        except Exception as e:
            raise Exception(f"Error parsing resume: {str(e)}")
    
    def _extract_text(self, file_content: bytes, filename: str) -> str:
        """Extract text from PDF or DOCX file"""
        try:
            if filename.lower().endswith('.pdf'):
                return self._extract_from_pdf(file_content)
            elif filename.lower().endswith(('.doc', '.docx')):
                return self._extract_from_docx(file_content)
            else:
                raise ValueError(f"Unsupported file type: {filename}")
        except Exception as e:
            raise Exception(f"Error extracting text: {str(e)}")
    
    def _extract_from_pdf(self, file_content: bytes) -> str:
        """Extract text from PDF"""
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
    
    def _extract_from_docx(self, file_content: bytes) -> str:
        """Extract text from DOCX"""
        try:
            doc = Document(io.BytesIO(file_content))
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            raise Exception(f"Error reading DOCX: {str(e)}")
    
    async def _structure_with_openai(self, text: str) -> Dict[str, Any]:
        """Use OpenAI to structure the resume data"""
        try:
            prompt = f"""
            You are an expert resume parser with deep understanding of academic and professional resumes. 
            Extract and structure the following resume information into a JSON format with maximum accuracy.
            
            CRITICAL INSTRUCTIONS:
            1. EDUCATION YEARS: 
               - For date ranges like "2016-2018", use the END year (2018) for year_of_completion
               - For ongoing PhD/education: Set year_of_completion to "" (empty) and current_status to actual status like "Thesis Submitted"
               - Only use actual completion years, not start years
            
            2. WORK EXPERIENCE DATES:
               - For ongoing positions (PhD, current job): Set to_date as "Present" 
               - Be precise with from_date (use actual start year)
               - Calculate years/months accurately from the dates
            
            3. RESEARCH EXPERIENCE DETECTION:
               - If resume shows PhD, publications, research work, conferences → set has_research: true
               - Extract EXACT publication titles, conference names, collaborator names
               - Look for research areas, awards, presentations
            
            4. DATA ACCURACY:
               - Extract EXACT text from resume - no placeholders or generic text
               - If information is missing, use null (not empty arrays or empty strings)
               - Pay attention to context and relationships between sections
            
            5. ADDITIONAL INFORMATION:
               - Extract profile/summary sections
               - Get exact skills, languages, certifications
               - Include volunteer work, awards, achievements
               - Use null for missing information
            
            6. EDUCATION COURSE NAMES:
               - Use proper degree names: "Ph.D.", "M.Sc.", "B.Sc.", "Class 12", "Class 10"
               - Do NOT use university names as course names
               - If course field contains university name, use the degree name instead
               - ALWAYS provide course names, never leave them empty
               
            7. QUALIFICATION LEVELS:
               - Use exact terms: "PhD", "MSc", "BSc", "Class 12", "Class 10"
               - PhD should be "PhD" not "Ph.D" in qualification_level field
               - MSc should be "MSc" not "M.Sc" in qualification_level field
               - Be consistent with terminology
            
            Structure the data as follows:
            
            {{
                "personal_info": {{
                    "name": "Full Name",
                    "email": "email@example.com",
                    "phone": "phone number",
                    "address": "full address",
                    "date_of_birth": "YYYY-MM-DD",
                    "gender": "Male/Female/Other",
                    "marital_status": "Single/Married/Divorced/Widow/Other",
                    "nationality": "Nationality",
                    "religion": "Religion",
                    "blood_group": "Blood Group",
                    "aadhar_no": "Aadhar Number",
                    "passport_no": "Passport Number"
                }},
                "education": [
                    {{
                        "qualification_level": "Class 10/Class 12/UG/PG/PhD",
                        "course": "Course Name",
                        "specialization": "Specialization",
                        "institute": "Institute Name",
                        "board_or_university": "Board/University",
                        "year_of_completion": "YYYY (use END year for ranges, current year for ongoing)",
                        "current_status": "Current Status if ongoing (e.g., 'Thesis Submitted', 'Pursuing')",
                        "grade_or_percentage": "Grade/Percentage",
                        "country": "Country",
                        "state": "State"
                    }}
                ],
                "work_experience": [
                    {{
                        "designation": "Job Title",
                        "company": "Company Name",
                        "employment_type": "fulltime/parttime/contract",
                        "from_date": "YYYY-MM-DD",
                        "to_date": "YYYY-MM-DD or Present",
                        "current_salary": "Salary",
                        "notice_period": "Notice Period in days",
                        "years": "Years of experience",
                        "months": "Months of experience",
                        "description": "Job description"
                    }}
                ],
                "research_experience": {{
                    "has_research": true/false,
                    "research_areas": ["area1", "area2"],
                    "publications": ["EXACT publication title 1", "EXACT publication title 2"],
                    "conferences": ["EXACT conference name 1", "EXACT conference name 2"],
                    "awards": ["EXACT award name 1", "EXACT award name 2"],
                    "collaborations": ["EXACT collaborator name 1", "EXACT collaborator name 2"]
                }},
                "additional_informations": {{
                    "profile_summary": "Professional summary/profile section",
                    "skills": ["skill1", "skill2", "skill3"],
                    "awards": ["EXACT award name 1", "EXACT award name 2"],
                    "publications": ["EXACT publication title 1", "EXACT publication title 2"],
                    "conferences": ["EXACT conference name 1", "EXACT conference name 2"],
                    "collaborators": ["EXACT collaborator name 1", "EXACT collaborator name 2"],
                    "languages": ["language1", "language2"] or null,
                    "certifications": ["cert1", "cert2"] or null,
                    "volunteer_work": ["volunteer1", "volunteer2"] or null
                }}
            }}
            
            Resume Text:
            {text}
            
            Return only the JSON structure with EXACT information from the resume, no placeholders.
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert resume parser specializing in academic and professional resumes. You understand PhD programs, research work, publications, and career progression. Extract information with maximum accuracy and attention to detail. Return only valid JSON with exact information from the resume."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=4000
            )
            
            # Extract JSON from response
            content = response.choices[0].message.content.strip()
            
            # Clean up the response to extract JSON
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]
            
            # Parse JSON
            structured_data = json.loads(content)
            
            # Ensure all string values are properly converted
            structured_data = self._sanitize_data_types(structured_data)
            return structured_data
            
        except json.JSONDecodeError as e:
            raise Exception(f"Error parsing OpenAI response as JSON: {str(e)}")
        except Exception as e:
            raise Exception(f"Error calling OpenAI API: {str(e)}")
    
    def _sanitize_data_types(self, data):
        """Recursively sanitize data types to ensure strings are strings"""
        if isinstance(data, dict):
            return {key: self._sanitize_data_types(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self._sanitize_data_types(item) for item in data]
        elif isinstance(data, (int, float)):
            return str(data)
        elif data is None:
            return ""
        else:
            return str(data)
