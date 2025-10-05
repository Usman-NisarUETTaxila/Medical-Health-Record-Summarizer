# Complete Installation Guide

## Quick Start

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Install Tesseract OCR

#### Windows
Download and install from: https://github.com/UB-Mannheim/tesseract/wiki

Or use package manager:
```powershell
# Using Chocolatey
choco install tesseract

# Using Scoop
scoop install tesseract
```

#### macOS
```bash
brew install tesseract
```

#### Linux
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install tesseract-ocr

# Fedora/RHEL
sudo dnf install tesseract
```

### 3. Set Up Environment Variables

Create a `.env` file in the project root:
```env
GOOGLE_API_KEY=your_google_api_key_here
```

Get your Google API key from: https://makersuite.google.com/app/apikey

### 4. Run Database Migrations
```bash
cd patient_system
python manage.py makemigrations
python manage.py migrate
```

### 5. Start Django Server
```bash
python manage.py runserver
```

### 6. Start Frontend (Optional)
```bash
cd gradio/ui/clinic-intellect-main
npm install
npm run dev
```

## Verify Installation

### Test Tesseract
```bash
tesseract --version
```

### Test Python Dependencies
```python
import pdfplumber
import pytesseract
from PIL import Image
print("All dependencies installed successfully!")
```

### Test API
```bash
# Test text summary
curl -X POST http://localhost:8000/patient-app/api/summary/text/ \
  -H "Content-Type: application/json" \
  -d '{"text": "Patient: John Doe, Age: 45, Diagnosis: Hypertension"}'

# Test file upload (create a test.txt first)
echo "Patient medical report" > test.txt
curl -X POST http://localhost:8000/patient-app/api/summary/file/ \
  -F "file=@test.txt"
```

## Features Available

✅ **Database Mode**: Fetch patient data by ID
✅ **Text Input Mode**: Paste medical report text
✅ **File Upload Mode**: 
  - TXT files
  - PDF files (text extraction)
  - Images (JPG, PNG) with OCR
✅ **AI Summary Generation**: Google Gemini AI
✅ **Beautiful UI**: Modern React interface

## Troubleshooting

### Tesseract not found
Add Tesseract to your system PATH or configure in code.

### PDF extraction fails
Make sure `pdfplumber` is installed: `pip install pdfplumber`

### OCR fails
1. Check Tesseract installation
2. Verify image quality
3. Ensure image contains readable text

### API key error
Make sure `.env` file exists with `GOOGLE_API_KEY` set.

## Next Steps

1. Create sample patient data
2. Test all three input modes
3. Customize AI prompts if needed
4. Set up production deployment
5. Configure CORS for production domains

## Documentation

- `AI_SUMMARY_API_SETUP.md` - API setup guide
- `TEXT_FILE_UPLOAD_API.md` - Text/file upload API docs
- `OCR_PDF_SETUP.md` - OCR and PDF extraction guide
- `UI_IMPROVEMENTS.md` - UI enhancement details

## Support

For issues:
1. Check error messages in console
2. Review Django logs
3. Verify all dependencies installed
4. Test with sample files first
