# Resume Parser Backend - Production Ready

## Overview

This is a production-ready FastAPI backend that extracts structured data from resume files using OpenAI's LLM and maps it to your existing DTO structure. The backend is designed for seamless integration with your React job application portal.

## Core Files

### Essential Backend Files
- `main.py` - FastAPI application with resume parsing endpoint
- `resume_parser.py` - Resume parsing logic using OpenAI GPT-3.5-turbo
- `dto_mapper.py` - Maps extracted data to your exact DTO structure
- `requirements.txt` - Python dependencies
- `deploy.py` - Deployment and setup script

### Configuration Files
- `dto.json` - Your existing DTO structure reference
- `complete_master_data_mappings_csv_only.json` - Master data mappings
- `env_template.txt` - Environment configuration template

### Documentation
- `README.md` - Main documentation
- `INTEGRATION_GUIDE.md` - Detailed React integration guide
- `BACKEND_SUMMARY.md` - This summary document

## How It Works

### 1. Resume Upload
- User uploads PDF, DOC, or DOCX resume file
- File is validated for type and size
- Text is extracted using PyPDF2 (PDF) or python-docx (DOC/DOCX)

### 2. AI Processing
- Extracted text is sent to OpenAI GPT-3.5-turbo
- LLM analyzes resume and extracts structured data
- Enhanced prompts ensure accurate extraction
- Data is returned in JSON format

### 3. Data Mapping
- Raw extracted data is processed by DTO mapper
- Course names are normalized (Researcher → Ph.D.)
- Qualification levels are mapped to correct IDs
- Master data mappings are applied
- Dates are processed and calculated accurately

### 4. DTO Generation
- Data is structured into your exact DTO format
- All required fields are populated
- Missing data is handled gracefully with null values
- Response is returned to React frontend

## Key Features

### Intelligent Data Extraction
- **Personal Information**: Name, email, phone, address, DOB, gender, etc.
- **Education**: All qualification levels with proper course names
- **Work Experience**: Current and previous jobs with accurate duration
- **Research Experience**: PhD detection, publications, conferences
- **Additional Info**: Skills, awards, languages, certifications

### Advanced Processing
- **Course Name Normalization**: University names → degree names
- **Qualification Level Mapping**: PhD → "5", MSc → "4", BSc → "3"
- **Date Range Processing**: "2016-2018" → uses end year "2018"
- **Ongoing Education**: Handles "Thesis submitted" status
- **Experience Calculation**: Accurate years/months from dates

### Master Data Integration
- Uses your existing master data JSON file
- Maps extracted values to correct IDs
- Handles gender, marital status, religion, location mappings
- Maintains consistency with your database

## API Endpoints

### POST /parse-resume
- **Input**: Resume file (PDF, DOC, DOCX)
- **Output**: Complete DTO structure
- **Error Handling**: Comprehensive validation and error messages

### GET /health
- **Purpose**: Health check for monitoring
- **Output**: Service status

## React Integration

### Service Setup
```javascript
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const parseResume = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await axios.post(`${API_BASE_URL}/parse-resume`, formData);
  return response.data;
};
```

### Component Integration
```javascript
const handleResumeUpload = async (file) => {
  try {
    const result = await parseResume(file);
    // Pre-fill your form with result.data
    setFormData(result.data);
  } catch (error) {
    // Handle error
  }
};
```

## Production Deployment

### Prerequisites
- Python 3.8+
- OpenAI API key with sufficient credits
- 2GB RAM minimum
- HTTPS for production

### Setup Steps
1. **Environment Setup**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configuration**
   ```bash
   cp env_template.txt .env
   # Edit .env and add your OpenAI API key
   ```

3. **Deployment**
   ```bash
   python deploy.py  # Automated setup
   python main.py    # Start service
   ```

### Environment Variables
```bash
OPENAI_API_KEY=your_production_api_key
HOST=0.0.0.0
PORT=8000
```

## Data Accuracy

### Qualification Levels
- PhD → qualificationLevelId: "5"
- MSc → qualificationLevelId: "4"
- BSc → qualificationLevelId: "3"
- Class 12 → qualificationLevelId: "2"
- Class 10 → qualificationLevelId: "1"

### Course Names
- "Researcher" + PhD → "Ph.D."
- "University of Mumbai" + MSc → "M.Sc."
- Generic subjects → Proper degree names

### Experience Calculation
- Accurate years/months from actual dates
- Handles ongoing positions correctly
- Separates current vs previous experience

## Error Handling

### File Validation
- File type checking (PDF, DOC, DOCX only)
- File size validation
- Corrupted file detection

### API Errors
- OpenAI API error recovery
- Network timeout handling
- Rate limiting protection

### Data Processing
- Type conversion and validation
- Missing data handling
- Graceful fallbacks

## Performance

- Fast processing with OpenAI GPT-3.5-turbo
- Optimized for quick response times
- Handles large resume files efficiently
- Robust error recovery

## Security

- API key protection
- File upload validation
- Input sanitization
- Error message sanitization

## Monitoring

- Health check endpoint
- Error logging
- Performance metrics
- Usage tracking

## Support

For detailed integration instructions, see `INTEGRATION_GUIDE.md`.

For troubleshooting and advanced configuration, refer to the code comments and error messages.

## Next Steps

1. **Test with your resumes**: Upload sample resumes to verify accuracy
2. **Integrate with React**: Follow the integration guide
3. **Deploy to production**: Use the deployment script
4. **Monitor performance**: Set up logging and monitoring
5. **Scale as needed**: Add load balancing if required

The backend is now ready for production use with your React job application portal.
