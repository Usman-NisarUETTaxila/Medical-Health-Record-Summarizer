# AI Summary API Setup Guide

## Overview
This guide explains how to use the AI Summary API that generates intelligent medical summaries using Google's Gemini AI model.

## API Endpoint

### Generate AI Summary
- **URL**: `http://localhost:8000/patient-app/api/patients/{patient_id}/summary/`
- **Method**: POST
- **Description**: Generates an AI-powered medical summary for a specific patient

### Request Example
```bash
POST http://localhost:8000/patient-app/api/patients/1/summary/
Content-Type: application/json
```

### Response Example (Success)
```json
{
  "success": true,
  "patient_id": 1,
  "patient_name": "Ali Khan",
  "summary": "Ali Khan, a 28-year-old Male with blood type B+, presented with shortness of breath and coughing...",
  "data": {
    "patient": { ... },
    "medical_history": { ... },
    "checkups": [ ... ],
    "lab_tests": [ ... ],
    "treatments": [ ... ],
    "notes": [ ... ]
  }
}
```

### Response Example (Error)
```json
{
  "error": "AI service configuration error",
  "details": "No API key found. Please set GOOGLE_API_KEY environment variable",
  "note": "Please set GOOGLE_API_KEY environment variable in .env file"
}
```

## Setup Instructions

### 1. Environment Configuration
Create or update your `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

**How to get Google API Key:**
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and add it to your `.env` file

### 2. Install Required Dependencies
Make sure all dependencies are installed:

```bash
pip install -r requirements.txt
```

Required packages:
- `django`
- `djangorestframework`
- `django-cors-headers`
- `google-generativeai`
- `langchain`
- `langchain-google-genai`
- `python-dotenv`

### 3. Start the Django Server
```bash
cd patient_system
python manage.py runserver
```

### 4. Test the API

#### Using Python (requests)
```python
import requests

# Generate AI summary for patient ID 1
response = requests.post('http://localhost:8000/patient-app/api/patients/1/summary/')

if response.status_code == 200:
    data = response.json()
    print(f"Summary for {data['patient_name']}:")
    print(data['summary'])
else:
    print(f"Error: {response.json()}")
```

#### Using cURL
```bash
curl -X POST http://localhost:8000/patient-app/api/patients/1/summary/ \
  -H "Content-Type: application/json"
```

#### Using the Frontend UI
1. Start the frontend development server:
   ```bash
   cd gradio/ui/clinic-intellect-main
   npm run dev
   ```

2. Navigate to `http://localhost:8080`
3. Enter a patient ID and click "Fetch Data"
4. Click "Generate AI Summary" button
5. The AI-generated summary will appear in the results page

## How It Works

### Backend Flow
1. **API Request**: Frontend sends POST request to `/api/patients/{id}/summary/`
2. **Data Retrieval**: Django fetches complete patient data from database
3. **AI Processing**: 
   - Patient data is passed to `Patient_Summary_System` from `prompt_template.py`
   - System uses Google's Gemini AI model with specialized medical prompts
   - AI generates a comprehensive 7-10 line summary
4. **Response**: Summary is returned to the frontend

### AI Summary Features
The AI summary includes:
- Patient demographics (name, age, gender, blood type)
- Current diagnosis and symptoms
- Vital signs analysis
- Medical history (conditions, allergies, surgeries, family history)
- Current treatment plan and medications
- Recovery recommendations
- Risk assessment
- Doctor's notes in patient-friendly language

### Prompt Template
The AI uses a specialized medical prompt that:
- Focuses on clarity and conciseness (7-10 lines)
- Highlights important medical terms
- Includes risk assessment
- Provides patient-friendly explanations
- Considers all patient data fields

## File Structure

```
patient_system/
├── patients/
│   ├── ai_views.py          # AI summary endpoint
│   ├── views.py             # Main CRUD endpoints
│   ├── urls.py              # URL routing
│   ├── models.py            # Database models
│   └── serializer.py        # Data serializers
│
gradio/
├── prompt_engineering/
│   └── prompt_template.py   # AI summary generation logic
│
gradio/ui/clinic-intellect-main/
├── src/
│   ├── services/
│   │   └── patientApi.ts    # Frontend API calls
│   ├── pages/
│   │   └── Index.tsx        # Main UI component
│   └── types/
│       └── patient.ts       # TypeScript types
```

## Troubleshooting

### Error: "AI service configuration error"
**Solution**: Make sure `GOOGLE_API_KEY` is set in your `.env` file and the file is in the project root.

### Error: "Failed to import AI summary system"
**Solution**: Verify that `prompt_template.py` exists in `gradio/prompt_engineering/` directory.

### Error: "Patient not found"
**Solution**: Ensure the patient ID exists in the database. Use the Django admin or API to check.

### Error: CORS issues
**Solution**: Verify CORS settings in `patient_system/settings.py`:
```python
CORS_ALLOWED_ORIGINS = ["http://localhost:8080", "http://localhost:8000"]
```

### AI Summary is too generic
**Solution**: The prompt template can be customized in `prompt_template.py` to adjust the summary style and content.

## API Integration Examples

### React/TypeScript (Frontend)
```typescript
import { generateAISummary } from "@/services/patientApi";

const handleGenerateSummary = async (patientId: number) => {
  try {
    const summary = await generateAISummary(patientId);
    console.log("AI Summary:", summary);
  } catch (error) {
    console.error("Error:", error);
  }
};
```

### Python (Backend/Scripts)
```python
from patients.ai_views import generate_ai_summary
from rest_framework.test import APIRequestFactory

factory = APIRequestFactory()
request = factory.post(f'/api/patients/1/summary/')
response = generate_ai_summary(request, patient_id=1)
print(response.data)
```

## Performance Considerations

- **Response Time**: AI generation typically takes 2-5 seconds
- **Rate Limits**: Google AI API has rate limits (check your quota)
- **Caching**: Consider implementing caching for frequently accessed summaries
- **Async Processing**: For production, consider using Celery for async processing

## Security Notes

1. **API Key Protection**: Never commit `.env` file to version control
2. **Authentication**: Add authentication middleware for production
3. **Rate Limiting**: Implement rate limiting to prevent abuse
4. **Input Validation**: All patient data is validated before processing

## Future Enhancements

- [ ] Cache AI summaries to reduce API calls
- [ ] Add support for multiple AI models
- [ ] Implement summary history tracking
- [ ] Add customizable summary templates
- [ ] Support for multi-language summaries
- [ ] Real-time summary generation with WebSockets

## Support

For issues or questions:
1. Check the Django logs: `patient_system/logs/`
2. Review API response error messages
3. Verify environment configuration
4. Test with sample patient data

## License
This project uses Google's Gemini AI API which has its own terms of service.
