from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import os
from dotenv import load_dotenv
import json
from resume_parser import ResumeParser
from dto_mapper import DTOMapper

# Load environment variables
load_dotenv()

app = FastAPI(title="Resume Parser API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
try:
    resume_parser = ResumeParser()
    dto_mapper = DTOMapper()
except ValueError as e:
    print(f"Initialization Error: {e}")
    print("Please create a .env file with your OpenAI API key.")
    print("Copy env_template.txt to .env and add your actual API key.")
    exit(1)

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Resume Parser API",
        "version": "1.0.0",
        "endpoints": {
            "POST /parse-resume": "Parse uploaded resume file",
            "GET /health": "Health check endpoint"
        }
    }

@app.post("/parse-resume")
async def parse_resume(file: UploadFile = File(...)):
    """
    Parse uploaded resume and return structured DTO
    """
    try:
        # Validate file type
        if not file.filename.lower().endswith(('.pdf', '.doc', '.docx')):
            raise HTTPException(status_code=400, detail="Only PDF, DOC, and DOCX files are supported")
        
        # Read file content
        file_content = await file.read()
        
        # Parse resume
        extracted_data = await resume_parser.parse_resume(file_content, file.filename)
        
        # Map to DTO
        dto = dto_mapper.map_to_dto(extracted_data)
        
        return {
            "success": True,
            "data": dto,
            "message": "Resume parsed successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing resume: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Resume Parser API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
