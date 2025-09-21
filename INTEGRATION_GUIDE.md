# Resume Parser Backend - Integration Guide

## Overview

This backend service extracts structured data from resume files (PDF, DOC, DOCX) using OpenAI's LLM and maps it to your existing DTO structure. It's designed to integrate seamlessly with your React job application portal.

## Essential Files

- `main.py` - FastAPI application with resume parsing endpoint
- `resume_parser.py` - Resume parsing logic using OpenAI
- `dto_mapper.py` - Maps extracted data to your DTO structure
- `requirements.txt` - Python dependencies
- `dto.json` - Your existing DTO structure reference
- `complete_master_data_mappings_csv_only.json` - Master data mappings
- `env_template.txt` - Environment configuration template

## Setup Instructions

### 1. Environment Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file from the template:

```bash
cp env_template.txt .env
```

Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=your_actual_openai_api_key_here
HOST=0.0.0.0
PORT=8000
```

### 3. Run the Service

```bash
python main.py
```

The service will start on `http://localhost:8000`

## API Endpoints

### POST /parse-resume

**Description:** Parse uploaded resume and return structured DTO

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: File upload (PDF, DOC, or DOCX)

**Response:**
```json
{
  "success": true,
  "data": {
    // Your complete DTO structure
  },
  "message": "Resume parsed successfully"
}
```

**Error Response:**
```json
{
  "success": false,
  "detail": "Error message"
}
```

### GET /health

**Description:** Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "message": "Resume Parser API is running"
}
```

## React Integration

### 1. Install Dependencies

```bash
npm install axios
```

### 2. Create Resume Parser Service

Create `src/services/resumeParser.js`:

```javascript
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_RESUME_PARSER_URL || 'http://localhost:8000';

class ResumeParserService {
  async parseResume(file) {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${API_BASE_URL}/parse-resume`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to parse resume');
    }
  }

  async checkHealth() {
    try {
      const response = await axios.get(`${API_BASE_URL}/health`);
      return response.data;
    } catch (error) {
      throw new Error('Resume parser service is not available');
    }
  }
}

export default new ResumeParserService();
```

### 3. Create Resume Upload Component

Create `src/components/ResumeUpload.js`:

```javascript
import React, { useState } from 'react';
import resumeParserService from '../services/resumeParser';

const ResumeUpload = ({ onResumeParsed }) => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
      if (!['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'].includes(selectedFile.type)) {
        setError('Please upload a PDF, DOC, or DOCX file');
        return;
      }
      setFile(selectedFile);
      setError(null);
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!file) return;

    setLoading(true);
    setError(null);

    try {
      const result = await resumeParserService.parseResume(file);
      onResumeParsed(result.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="resume-upload">
      <form onSubmit={handleSubmit}>
        <div className="file-input">
          <input
            type="file"
            accept=".pdf,.doc,.docx"
            onChange={handleFileChange}
            disabled={loading}
          />
        </div>
        
        {error && <div className="error">{error}</div>}
        
        <button 
          type="submit" 
          disabled={!file || loading}
          className="upload-button"
        >
          {loading ? 'Parsing Resume...' : 'Parse Resume'}
        </button>
      </form>
    </div>
  );
};

export default ResumeUpload;
```

### 4. Integration in Your Application

```javascript
import React, { useState } from 'react';
import ResumeUpload from './components/ResumeUpload';

const JobApplication = () => {
  const [parsedData, setParsedData] = useState(null);

  const handleResumeParsed = (data) => {
    setParsedData(data);
    // Pre-fill your form with the parsed data
    // data contains the complete DTO structure
  };

  return (
    <div>
      <h2>Job Application</h2>
      
      <ResumeUpload onResumeParsed={handleResumeParsed} />
      
      {parsedData && (
        <div>
          <h3>Parsed Data:</h3>
          <pre>{JSON.stringify(parsedData, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default JobApplication;
```

## Data Structure

The API returns data in your exact DTO structure with the following key sections:

### Personal Information
- `empApplnPersonalDataDTO` - Name, email, phone, address, etc.
- `addressDetailDTO` - Address details

### Education
- `educationalDetailDTO` - All education records with proper qualification levels
- `qualificationLevelsList` - Array of education entries
- `highestQualificationLevelId` - Correctly identifies highest qualification

### Work Experience
- `professionalExperienceDTO` - Current and previous work experience
- `isCurrentlyWorking` - Boolean for current employment status
- `currentExperience` - Current job details with accurate years/months
- `totalPreviousExperienceYears/Months` - Previous experience totals

### Research Experience
- `researchDetailDTO` - Research experience details
- `isResearchExperience` - Boolean for research background

### Additional Information
- `additionalInformations` - Skills, awards, publications, conferences, etc.

## Data Mapping Features

### Qualification Level Mapping
- PhD → qualificationLevelId: "5"
- MSc → qualificationLevelId: "4" 
- BSc → qualificationLevelId: "3"
- Class 12 → qualificationLevelId: "2"
- Class 10 → qualificationLevelId: "1"

### Course Name Normalization
- "Researcher" + PhD → "Ph.D."
- "University of Mumbai" + MSc → "M.Sc."
- Generic subjects → Proper degree names

### Master Data Integration
- Gender, marital status, religion, country, state mappings
- Uses your existing master data JSON file
- Maps extracted values to correct IDs

## Error Handling

The service includes comprehensive error handling:

- File type validation (PDF, DOC, DOCX only)
- OpenAI API error handling
- Data parsing error recovery
- Type conversion and validation
- Graceful fallbacks for missing data

## Performance

- Fast processing using OpenAI GPT-3.5-turbo
- Optimized for quick response times
- Handles large resume files efficiently
- Robust error recovery

## Production Deployment

### Environment Variables
```bash
OPENAI_API_KEY=your_production_api_key
HOST=0.0.0.0
PORT=8000
```

### Server Requirements
- Python 3.8+
- 2GB RAM minimum
- 1GB disk space
- Internet access for OpenAI API

### Security Considerations
- Keep OpenAI API key secure
- Use HTTPS in production
- Implement rate limiting if needed
- Validate file uploads on server side

### Monitoring
- Health check endpoint: `/health`
- Log parsing errors for monitoring
- Track API usage and performance

## Troubleshooting

### Common Issues

1. **OpenAI API Key Error**
   - Ensure API key is correctly set in .env file
   - Check API key has sufficient credits

2. **File Upload Errors**
   - Verify file is PDF, DOC, or DOCX
   - Check file size limits
   - Ensure file is not corrupted

3. **Parsing Errors**
   - Check resume text is extractable
   - Verify file format compatibility
   - Review error logs for details

4. **Data Mapping Issues**
   - Verify master data JSON file is present
   - Check DTO structure matches expectations
   - Review mapping logic for edge cases

### Support

For technical support or questions about integration, refer to the code comments and error messages for detailed troubleshooting information.
