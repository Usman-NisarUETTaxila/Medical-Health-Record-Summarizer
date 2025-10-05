# Text & File Upload AI Summary API

## Overview
This document describes the new API endpoints for generating AI summaries from text input and uploaded files.

## New API Endpoints

### 1. Generate Summary from Text
Generate AI summary from raw medical report text.

**Endpoint**: `POST /patient-app/api/summary/text/`

**Request Body**:
```json
{
  "text": "Patient medical report text here..."
}
```

**Response (Success)**:
```json
{
  "success": true,
  "summary": "AI generated summary...",
  "input_length": 1234,
  "source": "text_input"
}
```

**Response (Error)**:
```json
{
  "error": "No text provided",
  "details": "Please provide medical report text in the 'text' field"
}
```

**Example Usage**:
```bash
curl -X POST http://localhost:8000/patient-app/api/summary/text/ \
  -H "Content-Type: application/json" \
  -d '{"text": "Patient John Doe, 45 years old, presents with chest pain..."}'
```

---

### 2. Generate Summary from File Upload
Generate AI summary from uploaded medical report file.

**Endpoint**: `POST /patient-app/api/summary/file/`

**Request**: `multipart/form-data` with `file` field

**Supported File Types**:
- `.txt` - Text files (✅ Implemented)
- `.pdf` - PDF documents (⚠️ Requires manual implementation)
- `.doc`, `.docx` - Word documents (⚠️ Requires manual implementation)
- `.jpg`, `.jpeg`, `.png` - Images (⚠️ Requires OCR implementation)

**Response (Success - TXT files)**:
```json
{
  "success": true,
  "summary": "AI generated summary...",
  "filename": "report.txt",
  "file_size": 12345,
  "extracted_text": "First 500 characters...",
  "source": "file_upload"
}
```

**Response (Not Implemented - PDF/Images)**:
```json
{
  "error": "PDF extraction not implemented",
  "details": "PDF text extraction needs to be implemented manually",
  "note": "Please implement PDF extraction",
  "filename": "report.pdf",
  "file_size": 54321
}
```

**Example Usage**:
```bash
curl -X POST http://localhost:8000/patient-app/api/summary/file/ \
  -F "file=@medical_report.txt"
```

---

## Frontend Integration

### Text Input Mode

Users can paste medical report text directly into a textarea:

1. Select "Text" input mode
2. Paste medical report content
3. Click "Generate Summary"
4. AI summary appears immediately

**Frontend Code**:
```typescript
import { generateSummaryFromText } from "@/services/patientApi";

const summary = await generateSummaryFromText(textInput);
setAiSummary(summary);
```

### File Upload Mode

Users can upload medical report files:

1. Select "Upload" input mode
2. Click or drag-and-drop file
3. File info displayed (name, size)
4. Click "Generate Summary"
5. AI summary appears

**Frontend Code**:
```typescript
import { generateSummaryFromFile } from "@/services/patientApi";

const summary = await generateSummaryFromFile(uploadedFile);
setAiSummary(summary);
```

---

## Implementation Status

### ✅ Fully Implemented
- **Text Input**: Direct text analysis
- **TXT Files**: Plain text file upload and analysis
- **AI Summary Generation**: Using Google Gemini AI
- **Error Handling**: Comprehensive error messages
- **Frontend UI**: Complete upload and text input interface

### ⚠️ Requires Manual Implementation

#### PDF Extraction
You need to implement PDF text extraction. Suggested libraries:
- `PyPDF2`
- `pdfplumber`
- `pypdf`

**Example Implementation**:
```python
import PyPDF2

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text
```

#### Image OCR
You need to implement OCR for image files. Suggested libraries:
- `pytesseract`
- `easyocr`
- `Google Vision API`

**Example Implementation**:
```python
import pytesseract
from PIL import Image

def extract_text_from_image(image_file):
    image = Image.open(image_file)
    text = pytesseract.image_to_string(image)
    return text
```

#### Word Document Extraction
You need to implement Word document text extraction. Suggested libraries:
- `python-docx`
- `docx2txt`

**Example Implementation**:
```python
import docx

def extract_text_from_docx(docx_file):
    doc = docx.Document(docx_file)
    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    return text
```

---

## AI Prompt Template

The system uses a specialized prompt for text/file-based summaries:

```
You are a helpful medical assistant.

Your job is to analyze the following medical report and create a concise summary of 7-10 lines.

Rules:
- Extract patient name, age, and gender if mentioned
- Identify the main diagnosis or medical condition
- Mention key symptoms and vital signs
- List prescribed medications if any
- Include treatment recommendations
- Highlight any allergies or warnings
- Add a risk assessment at the end
- Use bold (**text**) for important medical terms
- Be clear, concise, and patient-friendly
```

---

## Workflow Comparison

### Database Mode (Existing)
1. Enter Patient ID
2. Fetch complete patient data
3. Display all patient information
4. Generate AI summary (optional)

### Text Mode (New)
1. Paste medical report text
2. Generate AI summary immediately
3. Display formatted summary
4. No patient data stored

### Upload Mode (New)
1. Upload medical report file
2. Extract text from file
3. Generate AI summary
4. Display formatted summary
5. No patient data stored

---

## Error Handling

### Common Errors

**No Text Provided**:
```json
{
  "error": "No text provided",
  "details": "Please provide medical report text in the 'text' field"
}
```

**No File Uploaded**:
```json
{
  "error": "No file uploaded",
  "details": "Please upload a medical report file"
}
```

**Unsupported File Type**:
```json
{
  "error": "Unsupported file type",
  "details": "Supported formats: .txt, .pdf, .doc, .docx, .jpg, .jpeg, .png",
  "uploaded_extension": ".xyz"
}
```

**AI API Key Missing**:
```json
{
  "error": "AI API key not found",
  "details": "No API key found. Please set GOOGLE_API_KEY environment variable",
  "note": "Please set GOOGLE_API_KEY environment variable in .env file"
}
```

---

## Security Considerations

1. **File Size Limits**: Consider implementing file size limits
2. **File Type Validation**: Only accept medical document formats
3. **Text Length Limits**: Prevent extremely long text inputs
4. **Rate Limiting**: Implement rate limiting for API calls
5. **Virus Scanning**: Scan uploaded files for malware
6. **Data Privacy**: Don't store uploaded files permanently

---

## Performance Optimization

### Recommendations
1. **Caching**: Cache summaries for identical inputs
2. **Async Processing**: Use Celery for large file processing
3. **File Cleanup**: Delete uploaded files after processing
4. **Compression**: Compress large text before sending to AI
5. **Batch Processing**: Process multiple files in batches

---

## Testing

### Test Text Input
```bash
curl -X POST http://localhost:8000/patient-app/api/summary/text/ \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Patient: John Doe, Age: 45, Gender: Male. Chief Complaint: Chest pain. Diagnosis: Acute myocardial infarction. Treatment: Aspirin, Nitroglycerin. Follow-up in 2 weeks."
  }'
```

### Test File Upload (TXT)
```bash
echo "Patient medical report content here..." > test_report.txt
curl -X POST http://localhost:8000/patient-app/api/summary/file/ \
  -F "file=@test_report.txt"
```

---

## Future Enhancements

- [ ] Support for DICOM medical images
- [ ] Multi-language support
- [ ] Voice-to-text input
- [ ] Real-time collaborative editing
- [ ] Summary comparison tool
- [ ] Export summaries to PDF
- [ ] Integration with EHR systems
- [ ] Batch file processing
- [ ] Summary templates customization

---

## Troubleshooting

### Issue: "OCR not implemented" error
**Solution**: Implement OCR extraction in `ai_views.py` for image files

### Issue: "PDF extraction not implemented" error
**Solution**: Implement PDF text extraction in `ai_views.py`

### Issue: Summary quality is poor
**Solution**: Adjust the AI prompt template in `ai_views.py` or use a different model

### Issue: File upload fails
**Solution**: Check file size limits in Django settings and CORS configuration

---

## API Response Times

- **Text Input**: 2-5 seconds
- **TXT File**: 3-6 seconds
- **PDF File**: 5-10 seconds (when implemented)
- **Image OCR**: 10-20 seconds (when implemented)

---

## Cost Considerations

- Google Gemini API has usage limits
- Monitor API calls to avoid exceeding quotas
- Consider implementing usage tracking
- Set up billing alerts

---

## Support

For implementation help with PDF/OCR:
1. Check the `prompt_template.py` for reference implementations
2. Review Django file upload documentation
3. Test with small files first
4. Monitor error logs for debugging
