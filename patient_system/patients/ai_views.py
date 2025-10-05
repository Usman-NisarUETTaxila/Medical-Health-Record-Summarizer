"""
AI Summary Generation Views for Patient System
"""
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
import os
import sys
from dotenv import load_dotenv
import io
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract'  # manual path of tesseract if needed



load_dotenv()

from .models import Patient
from .serializer import (
    PatientSerializer, 
    MedicalHistorySerializer, 
    CheckUpSerializer, 
    LabTestsSerializer, 
    TreatmentPlanSerializer, 
    AdditionalNoteSerializer
)


@api_view(['POST'])
def generate_ai_summary(request, patient_id):
    """
    Generate AI summary for a patient using the prompt_template system
    POST: Generate AI summary for the specified patient
    
    Example:
    POST /patient-app/api/patients/1/summary/
    
    Response:
    {
        "success": true,
        "patient_id": 1,
        "patient_name": "Ali Khan",
        "summary": "AI generated summary text...",
        "data": { ... complete patient data ... }
    }
    """
    try:
        # Get complete patient data
        patient = get_object_or_404(Patient, id=patient_id)
        
        # Serialize patient data
        patient_data = PatientSerializer(patient).data
        
        # Get all related data
        complete_data = {
            'patient': patient_data,
            'medical_history': None,
            'checkups': [],
            'lab_tests': [],
            'treatments': [],
            'notes': []
        }
        
        # Medical History
        medical_history = patient.medical_history.first()
        if medical_history:
            complete_data['medical_history'] = MedicalHistorySerializer(medical_history).data
        
        # CheckUps (ordered by date)
        checkups = patient.checkups.all().order_by('-date_of_checkup')
        complete_data['checkups'] = CheckUpSerializer(checkups, many=True).data
        
        # Lab Tests
        lab_tests = patient.labtests.all()
        complete_data['lab_tests'] = LabTestsSerializer(lab_tests, many=True).data
        
        # Treatment Plans (ordered by follow-up date)
        treatments = patient.treatments.all().order_by('-next_followup_date')
        complete_data['treatments'] = TreatmentPlanSerializer(treatments, many=True).data
        
        # Additional Notes
        notes = patient.notes.all()
        complete_data['notes'] = AdditionalNoteSerializer(notes, many=True).data
        
        # Import the Patient_Summary_System
        try:
            # Add the gradio directory to the Python path
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            gradio_path = os.path.join(base_dir, 'gradio', 'prompt_engineering')
            
            if gradio_path not in sys.path:
                sys.path.insert(0, gradio_path)
            
            from prompt_template import Patient_Summary_System
            
            # Initialize the summary system
            summary_system = Patient_Summary_System()
            
            # Generate summary from the patient data
            summary = summary_system.generate_summary_from_data(complete_data)
            
            return Response({
                'success': True,
                'patient_id': patient_id,
                'patient_name': patient.patient_name,
                'summary': summary,
                'data': complete_data
            }, status=status.HTTP_200_OK)
            
        except ImportError as ie:
            return Response({
                'error': 'Failed to import AI summary system',
                'details': str(ie),
                'note': 'Make sure prompt_template.py is in the correct location',
                'path_tried': gradio_path
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        except ValueError as ve:
            # API key not found
            return Response({
                'error': 'AI API key not found',
                'details': str(ve),
                'note': 'Please set GOOGLE_API_KEY environment variable in .env file'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        except Exception as ai_error:
            return Response({
                'error': 'Failed to generate AI summary',
                'details': str(ai_error),
                'patient_data': complete_data
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    except Exception as e:
        return Response({
            'error': 'Failed to process request',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def generate_summary_from_text(request):
    """
    Generate AI summary from raw text input
    POST: Generate AI summary from medical report text
    
    Request Body:
    {
        "text": "Patient medical report text here..."
    }
    
    Response:
    {
        "success": true,
        "summary": "AI generated summary...",
        "input_length": 1234
    }
    """
    try:
        text_input = request.data.get('text', '').strip()
        
        if not text_input:
            return Response({
                'error': 'No text provided',
                'details': 'Please provide medical report text in the "text" field'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Import the Patient_Summary_System
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            gradio_path = os.path.join(base_dir, 'gradio', 'prompt_engineering')
            
            if gradio_path not in sys.path:
                sys.path.insert(0, gradio_path)
            
            from prompt_template import Patient_Summary_System
            
            # Initialize the summary system
            summary_system = Patient_Summary_System()
            summary_system.load_api_key()
            
            # Create a simple prompt for text-based summary
            import json
            from langchain.prompts import PromptTemplate
            from langchain_google_genai import ChatGoogleGenerativeAI
            from langchain_core.runnables import RunnableSequence
            from langchain_core.messages.utils import get_buffer_string
            
            template_str = """
            You are a helpful medical assistant.
            
            Your job is to analyze the following medical report text and create a concise summary of 7-10 lines.
            
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
            
            Medical Report Text:
            {text}
            """
            
            prompt = PromptTemplate(
                input_variables=["text"],
                template=template_str
            )
            
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash-exp",
                google_api_key=summary_system.api_key,
                temperature=0.7
            )
            
            chain = RunnableSequence(prompt | llm)
            raw_summary = chain.invoke({"text": text_input})
            summary = get_buffer_string([raw_summary])
            
            return Response({
                'success': True,
                'summary': summary,
                'input_length': len(text_input),
                'source': 'text_input'
            }, status=status.HTTP_200_OK)
            
        except ValueError as ve:
            return Response({
                'error': 'AI API key not found',
                'details': str(ve),
                'note': 'Please set GOOGLE_API_KEY environment variable in .env file'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        except Exception as ai_error:
            return Response({
                'error': 'Failed to generate AI summary',
                'details': str(ai_error)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    except Exception as e:
        return Response({
            'error': 'Failed to process request',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def generate_summary_from_file(request):
    """
    Generate AI summary from uploaded medical report file
    POST: Upload file and generate AI summary
    
    Request: multipart/form-data with 'file' field
    
    Response:
    {
        "success": true,
        "summary": "AI generated summary...",
        "filename": "report.pdf",
        "file_size": 12345,
        "extracted_text": "..." (optional)
    }
    """
    try:
        uploaded_file = request.FILES.get('file')
        
        if not uploaded_file:
            return Response({
                'error': 'No file uploaded',
                'details': 'Please upload a medical report file'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get file info
        filename = uploaded_file.name
        file_size = uploaded_file.size
        file_extension = os.path.splitext(filename)[1].lower()
        
        # Supported file types
        supported_extensions = ['.txt', '.pdf', '.doc', '.docx', '.jpg', '.jpeg', '.png']
        
        if file_extension not in supported_extensions:
            return Response({
                'error': 'Unsupported file type',
                'details': f'Supported formats: {", ".join(supported_extensions)}',
                'uploaded_extension': file_extension
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Read file content
        extracted_text = ""
        
        try:
            if file_extension == '.txt':
                # Read text file directly
                extracted_text = uploaded_file.read().decode('utf-8')
            
            elif file_extension in ['.jpg', '.jpeg', '.png']:
                # Image file - OCR using pytesseract
                try:
                    from PIL import Image
                    
                    # Read image from uploaded file
                    image = Image.open(uploaded_file)
                    
                    # Perform OCR
                    extracted_text = pytesseract.image_to_string(image)
                    
                    if not extracted_text.strip():
                        return Response({
                            'error': 'No text found in image',
                            'details': 'OCR could not extract any text from the image',
                            'note': 'Please ensure the image contains readable text',
                            'filename': filename
                        }, status=status.HTTP_400_BAD_REQUEST)
                    
                except ImportError:
                    return Response({
                        'error': 'OCR library not installed',
                        'details': 'pytesseract or Pillow is not installed',
                        'note': 'Install with: pip install pytesseract Pillow',
                        'filename': filename
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                except Exception as ocr_error:
                    return Response({
                        'error': 'OCR processing failed',
                        'details': str(ocr_error),
                        'note': 'Make sure Tesseract is installed on your system',
                        'filename': filename
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            elif file_extension == '.pdf':
                # PDF file - extract text using pdfplumber
                try:
                    import pdfplumber
                    
                    # Read PDF from uploaded file
                    pdf_bytes = uploaded_file.read()
                    pdf_file = io.BytesIO(pdf_bytes)
                    
                    # Extract text from all pages
                    with pdfplumber.open(pdf_file) as pdf:
                        extracted_text = ""
                        for page in pdf.pages:
                            page_text = page.extract_text()
                            if page_text:
                                extracted_text += page_text + "\n"
                    
                    if not extracted_text.strip():
                        return Response({
                            'error': 'No text found in PDF',
                            'details': 'PDF appears to be empty or contains only images',
                            'note': 'For image-based PDFs, consider converting to images first',
                            'filename': filename
                        }, status=status.HTTP_400_BAD_REQUEST)
                    
                except ImportError:
                    return Response({
                        'error': 'PDF library not installed',
                        'details': 'pdfplumber is not installed',
                        'note': 'Install with: pip install pdfplumber',
                        'filename': filename
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                except Exception as pdf_error:
                    return Response({
                        'error': 'PDF processing failed',
                        'details': str(pdf_error),
                        'filename': filename
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            elif file_extension in ['.doc', '.docx']:
                # Word document - placeholder
                return Response({
                    'error': 'Word document extraction not implemented',
                    'details': 'Word document extraction needs to be implemented manually',
                    'note': 'Please implement Word document extraction using python-docx',
                    'filename': filename,
                    'file_size': file_size
                }, status=status.HTTP_501_NOT_IMPLEMENTED)
        
        except Exception as read_error:
            return Response({
                'error': 'Failed to read file',
                'details': str(read_error),
                'filename': filename
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # If we have extracted text, generate summary
        if extracted_text.strip():
            # Import the Patient_Summary_System
            try:
                base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
                gradio_path = os.path.join(base_dir, 'gradio', 'prompt_engineering')
                
                if gradio_path not in sys.path:
                    sys.path.insert(0, gradio_path)
                
                from prompt_template import Patient_Summary_System
                
                # Initialize the summary system
                summary_system = Patient_Summary_System()
                summary_system.load_api_key()
                
                # Create a simple prompt for file-based summary
                import json
                from langchain.prompts import PromptTemplate
                from langchain_google_genai import ChatGoogleGenerativeAI
                from langchain_core.runnables import RunnableSequence
                from langchain_core.messages.utils import get_buffer_string
                
                template_str = """
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
                
                Medical Report:
                {text}
                """
                
                prompt = PromptTemplate(
                    input_variables=["text"],
                    template=template_str
                )
                
                llm = ChatGoogleGenerativeAI(
                    model="gemini-2.0-flash-exp",
                    google_api_key=summary_system.api_key,
                    temperature=0.7
                )
                
                chain = RunnableSequence(prompt | llm)
                raw_summary = chain.invoke({"text": extracted_text})
                summary = get_buffer_string([raw_summary])
                
                return Response({
                    'success': True,
                    'summary': summary,
                    'filename': filename,
                    'file_size': file_size,
                    'extracted_text': extracted_text[:500] + '...' if len(extracted_text) > 500 else extracted_text,
                    'source': 'file_upload'
                }, status=status.HTTP_200_OK)
                
            except ValueError as ve:
                return Response({
                    'error': 'AI API key not found',
                    'details': str(ve),
                    'note': 'Please set GOOGLE_API_KEY environment variable in .env file'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            except Exception as ai_error:
                return Response({
                    'error': 'Failed to generate AI summary',
                    'details': str(ai_error)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({
                'error': 'No text extracted from file',
                'details': 'The file appears to be empty or unreadable',
                'filename': filename
            }, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        return Response({
            'error': 'Failed to process file',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
