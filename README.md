# Resume Parser Backend

A production-ready FastAPI backend that extracts structured data from resume files using OpenAI's LLM and maps it to your existing DTO format for seamless integration with your React job application portal.

## Key Features

- **Intelligent Resume Parsing**: Extracts data from PDF, DOC, and DOCX files using OpenAI GPT-3.5-turbo
- **Accurate DTO Mapping**: Converts extracted data to your exact DTO structure
- **Master Data Integration**: Maps extracted values to your existing master data IDs
- **Robust Error Handling**: Comprehensive validation and error recovery
- **Production Ready**: Optimized for performance and reliability

## Quick Start

1. **Setup Environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

2. **Configure API Key**
   ```bash
   cp env_template.txt .env
   # Edit .env and add your OpenAI API key
   ```

3. **Run Service**
   ```bash
   python main.py
   ```

4. **Test Integration**
   ```bash
   curl -X POST "http://localhost:8000/parse-resume" -F "file=@resume.pdf"
   ```

## API Documentation

### POST /parse-resume
Parse uploaded resume and return structured DTO data.

**Request:**
- Content-Type: multipart/form-data
- Body: Resume file (PDF, DOC, or DOCX)

**Response:**
```json
{
  "success": true,
  "data": {
    "empApplnPersonalDataDTO": { ... },
    "educationalDetailDTO": { ... },
    "professionalExperienceDTO": { ... },
    "researchDetailDTO": { ... },
    "additionalInformations": { ... }
  },
  "message": "Resume parsed successfully"
}
```

### GET /health
Health check endpoint for monitoring.

## Data Extraction Capabilities

### Personal Information
- Name, email, phone, address
- Date of birth, gender, marital status
- Nationality, religion, blood group
- Government IDs (Aadhar, passport)

### Education Details
- All qualification levels (Class 10, 12, UG, PG, PhD)
- Proper course names (Ph.D., M.Sc., B.Sc.)
- Accurate qualification level IDs (1-5)
- Institute, board/university information
- Completion years and current status

### Work Experience
- Current and previous employment
- Accurate duration calculations
- Designation, company, employment type
- Salary, notice period, achievements

### Research Experience
- PhD and research work detection
- Publications, conferences, collaborations
- Awards and recognitions
- Research areas and specializations

### Additional Information
- Skills, languages, certifications
- Awards, publications, conferences
- Volunteer work, achievements
- Profile summaries

## Advanced Features

### Intelligent Data Processing
- **Course Name Normalization**: Converts "Researcher" → "Ph.D.", "University of Mumbai" → "M.Sc."
- **Qualification Level Mapping**: PhD → "5", MSc → "4", BSc → "3"
- **Date Range Processing**: "2016-2018" → uses end year "2018"
- **Ongoing Education**: Handles "Thesis submitted" status correctly
- **Experience Calculation**: Accurate years/months from actual dates

### Master Data Integration
- Gender, marital status, religion mappings
- Country, state, city mappings
- Blood group, reservation category mappings
- Qualification level mappings
- Uses your existing master data JSON file

### Error Handling
- File type validation
- OpenAI API error recovery
- Data parsing error handling
- Type conversion and validation
- Graceful fallbacks for missing data

## File Structure

```
resumeparser/
├── main.py                          # FastAPI application
├── resume_parser.py                 # Resume parsing logic
├── dto_mapper.py                    # DTO mapping logic
├── requirements.txt                 # Python dependencies
├── dto.json                         # Your DTO structure reference
├── complete_master_data_mappings_csv_only.json  # Master data mappings
├── env_template.txt                 # Environment configuration
└── INTEGRATION_GUIDE.md            # Detailed integration guide
```

## React Integration

See `INTEGRATION_GUIDE.md` for complete React integration instructions including:
- Service setup and configuration
- Component implementation
- Error handling
- Data pre-filling
- Production deployment

## Production Deployment

### Requirements
- Python 3.8+
- 2GB RAM minimum
- OpenAI API key with sufficient credits
- HTTPS for production

### Environment Variables
```bash
OPENAI_API_KEY=your_production_api_key
HOST=0.0.0.0
PORT=8000
```

### Security
- Keep API keys secure
- Use HTTPS in production
- Implement rate limiting
- Validate file uploads

## Performance

- Fast processing with OpenAI GPT-3.5-turbo
- Optimized for quick response times
- Handles large resume files efficiently
- Robust error recovery and validation

## Support

For detailed integration instructions, troubleshooting, and React implementation examples, see `INTEGRATION_GUIDE.md`.
