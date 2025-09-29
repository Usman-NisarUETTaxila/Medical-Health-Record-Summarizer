import os
import json
import re
from dotenv import load_dotenv
from langchain_core.runnables import RunnableSequence
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages.utils import get_buffer_string
import requests 
load_dotenv()

class Patient_Summary_System:
    def __init__(self):
        self.api_key = None
        self.data = {}

    def get_patient_data(self,url):
        response = requests.get(url=url)
        if response.status_code == 200:
            self.data = response.json()
        else:
            self.data = {}

        return self.data

    def load_api_key(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("⚠️ No API key found. Please set GOOGLE_API_KEY environment variable and restart.")
        
    def generate_summary(self,url):
        self.get_patient_data(url=url)
        self.load_api_key()

        template_str = """
        You are a helpful medical assistant.

        Your job is to take the full patient record and create a summary of 7-10 lines in the form of a paragraph.

        Rules:
        - Always mention patient's name and age first.
        - If "current_diagnosis" exists → report it clearly.
        - If no disease/diagnosis → write exactly: "Patient has no reported medical conditions."
        - Mention prescribed medications (or "None").
        - Mention recovery plan (procedures, lifestyle, physiotherapy, follow-up).
        - Write Dates in a clear manner like 20th March 2021.
        - Bold the important words and terminologies.
        - Merge other important details (allergies, doctor remarks, warnings) in a simple way.
        - Be concise, clear, and easy to read.
        - At the very end, add a Risk line:
        - If labs/vitals/diagnosis indicate a risk → state it clearly (e.g., "High risk due to uncontrolled diabetes").
        - If nothing serious → write "No immediate risks reported."
        - After that, add a Doctor's Note written in simple words a patient can easily understand. Avoid medical jargon.

        You Must Consider All the Fields in the data.

        Now create a short summary in the form of a paragraph with 7-10 lines only, then finish with the risk line.

        Patient Record JSON:
        {record}
        """

        prompt = PromptTemplate(
            input_variables=["record"],
            template=template_str
        )

        # Initialize Gemini model
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            google_api_key=self.api_key,
            temperature=0.7
        )

        # Create RunnableSequence chain
        chain = RunnableSequence(prompt | llm)

        # Convert dict to JSON string
        json_input_str = json.dumps(self.data, indent=2)

        # Run chain
        if self.data != {}:
            raw_summary = chain.invoke({"record": json_input_str})
            summary_text = get_buffer_string([raw_summary])
        else:
            summary_text = "No Data Found!"
        
        return summary_text

    def generate_summary_from_data(self, record: dict):
        """Generate summary directly from an in-memory JSON-like dict."""
        self.data = record or {}
        self.load_api_key()

        template_str = """
        You are a helpful medical assistant.

        Your job is to take the full patient record and create a summary of 7-10 lines in the form of a paragraph.

        Rules:
        - Always mention patient's name and age first.
        - If "current_diagnosis" exists → report it clearly.
        - If no disease/diagnosis → write exactly: "Patient has no reported medical conditions."
        - Mention prescribed medications (or "None").
        - Mention recovery plan (procedures, lifestyle, physiotherapy, follow-up).
        - Write Dates in a clear manner like 20th March 2021.
        - Bold the important words and terminologies.
        - Merge other important details (allergies, doctor remarks, warnings) in a simple way.
        - Be concise, clear, and easy to read.
        - At the very end, add a Risk line:
        - If labs/vitals/diagnosis indicate a risk → state it clearly (e.g., "High risk due to uncontrolled diabetes").
        - If nothing serious → write "No immediate risks reported."
        - After that, add a Doctor's Note written in simple words a patient can easily understand. Avoid medical jargon.

        You Must Consider All the Fields in the data.

        Now create a short summary in the form of a paragraph with 7-10 lines only, then finish with the risk line.

        Patient Record JSON:
        {record}
        """

        prompt = PromptTemplate(
            input_variables=["record"],
            template=template_str
        )

        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            google_api_key=self.api_key,
            temperature=0.7
        )

        chain = RunnableSequence(prompt | llm)
        json_input_str = json.dumps(self.data, indent=2)
        if self.data != {}:
            raw_summary = chain.invoke({"record": json_input_str})
            summary_text = get_buffer_string([raw_summary])
        else:
            summary_text = "No Data Found!"
        return summary_text

    def save_to_database(self, patient_data: dict) -> dict:
        """
        Save structured patient data to the Django database
        """
        try:
            import requests
            
            # First check if Django server is running
            try:
                health_check = requests.get("http://localhost:8000/patient-app/api/patients/", timeout=5)
            except requests.exceptions.RequestException:
                return {
                    "success": False,
                    "error": "Django backend server is not running. Please start it with: python manage.py runserver"
                }
            
            # Helper function to convert any value to string safely
            def safe_string_convert(value):
                if value is None or value == "":
                    return ""
                elif isinstance(value, str):
                    return value
                elif isinstance(value, list):
                    return ", ".join(str(item) for item in value if item)
                elif isinstance(value, dict):
                    return ", ".join(f"{k}: {v}" for k, v in value.items() if v)
                else:
                    return str(value)
            
            # Transform the data to match Django API expectations
            # The Django API expects: patient, medical_history, checkups, lab_tests, treatments, notes
            formatted_data = {
                "patient": patient_data.get("patient", {}),
                "medical_history": {},
                "checkups": patient_data.get("checkups", []),
                "lab_tests": patient_data.get("lab_tests", []),
                "treatments": patient_data.get("treatments", []),
                "notes": patient_data.get("notes", [])
            }
            
            # Process medical_history with safe string conversion
            original_history = patient_data.get("medical_history", {})
            formatted_data["medical_history"] = {
                "past_conditions": safe_string_convert(original_history.get("past_conditions")) or "No significant past conditions",
                "family_history": safe_string_convert(original_history.get("family_history")) or "No significant family history",
                "allergies": safe_string_convert(original_history.get("allergies")) or "No known allergies",
                "previous_surgeries": safe_string_convert(original_history.get("previous_surgeries")) or "No previous surgeries"
            }
            
            # Ensure patient has required fields with defaults
            if "patient" in formatted_data and formatted_data["patient"]:
                patient_info = formatted_data["patient"]
                # Add default values for required fields if missing
                if "patient_name" not in patient_info:
                    patient_info["patient_name"] = "Unknown Patient"
                if "guardian_name" not in patient_info:
                    patient_info["guardian_name"] = "Unknown Guardian"
                if "age" not in patient_info:
                    patient_info["age"] = 0
                if "gender" not in patient_info:
                    patient_info["gender"] = "Other"
                if "blood_group" not in patient_info:
                    patient_info["blood_group"] = "O+"
                if "date_of_birth" not in patient_info:
                    patient_info["date_of_birth"] = "2000-01-01"
                if "phone_number" not in patient_info:
                    import random
                    patient_info["phone_number"] = f"+1234567{random.randint(1000, 9999)}"  # Unique phone number
                if "email_address" not in patient_info:
                    import random
                    patient_info["email_address"] = f"patient{random.randint(1000, 9999)}@example.com"
            
            
            # Process checkups with proper defaults
            checkups = formatted_data.get("checkups", [])
            if isinstance(checkups, dict):
                checkups = [checkups]
            elif not isinstance(checkups, list):
                checkups = []
            
            # Add defaults to each checkup
            processed_checkups = []
            for checkup in checkups:
                if isinstance(checkup, dict):
                    # Handle nested vitals structure
                    vitals = checkup.get("vitals", {})
                    
                    processed_checkup = {
                        "symptoms": safe_string_convert(checkup.get("symptoms")) or "General checkup",
                        "current_diagnosis": safe_string_convert(checkup.get("current_diagnosis")) or "Routine examination",
                        "date_of_checkup": checkup.get("date_of_checkup") or "2024-01-01",
                        "blood_pressure": safe_string_convert(vitals.get("blood_pressure") or checkup.get("blood_pressure")) or "120/80",
                        "heart_rate": safe_string_convert(vitals.get("pulse_rate") or vitals.get("heart_rate") or checkup.get("heart_rate")) or "72",
                        "temperature": safe_string_convert(vitals.get("temperature") or checkup.get("temperature")) or "98.6",
                        "weight": safe_string_convert(vitals.get("weight") or checkup.get("weight")) or "70",
                        "height": safe_string_convert(vitals.get("height") or checkup.get("height")) or "170",
                        "bmi": safe_string_convert(vitals.get("bmi") or checkup.get("bmi")) or "24.2",
                        "physical_exam_findings": safe_string_convert(checkup.get("physical_exam_findings")) or "Normal"
                    }
                    processed_checkups.append(processed_checkup)
            
            formatted_data["checkups"] = processed_checkups
            
            # Process treatments with proper defaults
            treatments = formatted_data.get("treatments", [])
            if isinstance(treatments, dict):
                treatments = [treatments]
            elif not isinstance(treatments, list):
                treatments = []
            
            processed_treatments = []
            for treatment in treatments:
                if isinstance(treatment, dict):
                    # Handle nested medications structure
                    medications = treatment.get("medications", [])
                    if isinstance(medications, list):
                        medications_str = ", ".join(str(med) for med in medications)
                    else:
                        medications_str = safe_string_convert(medications)
                    
                    # Handle follow-up date carefully
                    followup_date = treatment.get("next_followup_date")
                    if not followup_date:
                        followup_date = None
                    
                    processed_treatment = {
                        "related_disease": safe_string_convert(treatment.get("related_disease")) or "General treatment",
                        "assigned_doctor": safe_string_convert(treatment.get("assigned_doctor")) or "Dr. General", 
                        "prescribed_medications": medications_str or safe_string_convert(treatment.get("prescribed_medications")) or "As prescribed",
                        "procedures": safe_string_convert(treatment.get("procedures")) or "Standard care",
                        "lifestyle_recommendations": safe_string_convert(treatment.get("lifestyle_recommendations")) or "Maintain healthy lifestyle",
                        "physiotherapy_advice": safe_string_convert(treatment.get("physiotherapy_advice")) or "As needed"
                    }
                    
                    # Only add followup_date if it's not None
                    if followup_date:
                        processed_treatment["next_followup_date"] = followup_date
                    processed_treatments.append(processed_treatment)
            
            formatted_data["treatments"] = processed_treatments
            
            # Process lab_tests with defaults
            lab_tests = formatted_data.get("lab_tests", [])
            if isinstance(lab_tests, dict):
                lab_tests = [lab_tests]
            elif not isinstance(lab_tests, list):
                lab_tests = []
            
            processed_lab_tests = []
            for lab_test in lab_tests:
                if isinstance(lab_test, dict):
                    processed_lab_test = {
                        "lab_results": safe_string_convert(lab_test.get("lab_results")) or "No lab results available",
                        "imaging": safe_string_convert(lab_test.get("imaging")) or "No imaging performed",
                        "other_tests": safe_string_convert(lab_test.get("other_tests")) or "No additional tests"
                    }
                    processed_lab_tests.append(processed_lab_test)
            
            formatted_data["lab_tests"] = processed_lab_tests
            
            # Process notes with defaults
            notes = formatted_data.get("notes", [])
            if isinstance(notes, dict):
                notes = [notes]
            elif not isinstance(notes, list):
                notes = []
            
            processed_notes = []
            for note in notes:
                if isinstance(note, dict):
                    processed_note = {
                        "doctor_remarks": safe_string_convert(note.get("doctor_remarks")) or "No specific remarks",
                        "special_warnings": safe_string_convert(note.get("special_warnings")) or "No special warnings"
                    }
                    processed_notes.append(processed_note)
            
            formatted_data["notes"] = processed_notes
            
            # API endpoint for creating patient data
            url = "http://localhost:8000/patient-app/api/patients/"
            
            # Debug: Print summary of data being sent
            print(f"DEBUG: Saving patient '{formatted_data.get('patient', {}).get('patient_name', 'Unknown')}' with {len(formatted_data.get('treatments', []))} treatments")
            
            # Send POST request to create patient
            response = requests.post(url, json=formatted_data, headers={
                'Content-Type': 'application/json'
            }, timeout=10)
            
            if response.status_code == 201:
                created_data = response.json()
                patient_id = created_data.get('data', {}).get('patient', {}).get('id')
                return {
                    "success": True,
                    "message": f"Patient saved successfully with ID: {patient_id}",
                    "patient_id": patient_id,
                    "data": created_data
                }
            else:
                try:
                    error_data = response.json()
                    return {
                        "success": False,
                        "error": f"Failed to save patient. Status: {response.status_code}",
                        "details": str(error_data)
                    }
                except:
                    return {
                        "success": False,
                        "error": f"Failed to save patient. Status: {response.status_code}",
                        "details": response.text[:500]
                    }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Database save failed: {str(e)}"
            }

    def test_api_key(self) -> dict:
        """Test if the API key works with Google Generative AI"""
        try:
            self.load_api_key()
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            
            # List available models
            models = []
            try:
                for m in genai.list_models():
                    if 'generateContent' in m.supported_generation_methods:
                        models.append(m.name)
            except Exception:
                models = ["Could not list models"]
            
            # Try a simple text generation to test the key
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content("Say 'API key works'")
            return {
                "success": True, 
                "response": response.text,
                "available_models": models[:5]  # Show first 5 models
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def image_to_patient_json_fallback(self, image_bytes: bytes) -> dict:
        """
        Fallback method using Tesseract OCR + LLM for text extraction and structuring
        """
        try:
            from PIL import Image
            import pytesseract
            import io
            import platform
            
            # Set Tesseract path for Windows
            if platform.system() == "Windows":
                # Common Tesseract installation paths on Windows
                possible_paths = [
                    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
                    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
                    r"C:\Users\{}\AppData\Local\Programs\Tesseract-OCR\tesseract.exe".format(os.getenv('USERNAME', '')),
                    r"C:\Users\{}\AppData\Local\Microsoft\WinGet\Packages\UB-Mannheim.TesseractOCR_Microsoft.Winget.Source_8wekyb3d8bbwe\tesseract.exe".format(os.getenv('USERNAME', '')),
                    # Search in common winget installation locations
                    r"C:\Program Files\WindowsApps\UB-Mannheim.TesseractOCR*\tesseract.exe",
                ]
                
                tesseract_found = False
                for path in possible_paths:
                    if '*' in path:
                        # Handle wildcard paths
                        import glob
                        matches = glob.glob(path)
                        if matches:
                            pytesseract.pytesseract.tesseract_cmd = matches[0]
                            tesseract_found = True
                            break
                    elif os.path.exists(path):
                        pytesseract.pytesseract.tesseract_cmd = path
                        tesseract_found = True
                        break
                
                if not tesseract_found:
                    return {
                        "error": "Tesseract not found. Please install it manually or add to PATH.",
                        "install_instructions": "Download from: https://github.com/UB-Mannheim/tesseract/wiki"
                    }
            
            # Convert bytes to PIL Image
            image = Image.open(io.BytesIO(image_bytes))
            
            # Extract text using Tesseract
            extracted_text = pytesseract.image_to_string(image)
            
            if not extracted_text.strip():
                return {"error": "No text could be extracted from the image"}
            
            # Use LLM to structure the extracted text
            self.load_api_key()
            
            structure_prompt = f"""
            Convert this medical report text into structured JSON format:
            
            Text: {extracted_text}
            
            Return ONLY valid JSON with these keys:
            - patient: {{patient_name, age, gender, etc.}}
            - medical_history: {{past_conditions, allergies, etc.}}
            - checkups: [{{symptoms, diagnosis, vitals, etc.}}]
            - lab_tests: [{{results, imaging, etc.}}]
            - treatments: [{{medications, procedures, etc.}}]
            - notes: [{{doctor_remarks, warnings, etc.}}]
            
            If information is missing, omit the field or use null.
            """
            
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash-lite",
                google_api_key=self.api_key,
                temperature=0.3
            )
            
            response = llm.invoke(structure_prompt)
            response_text = response.content if hasattr(response, 'content') else str(response)
            
            # Try to parse JSON from response
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group(0))
                except:
                    pass
            
            return {
                "error": "Could not structure the extracted text",
                "extracted_text": extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text
            }
            
        except ImportError:
            return {"error": "pytesseract not installed. Run: pip install pytesseract"}
        except Exception as e:
            return {"error": f"OCR processing failed: {str(e)}"}

    def text_to_patient_json(self, text: str) -> dict:
        """
        Convert medical report text to structured JSON using LLM
        """
        try:
            self.load_api_key()
            
            structure_prompt = f"""
            Convert this medical report text into structured JSON format:
            
            Text: {text}
            
            Return ONLY valid JSON with these keys:
            - patient: {{patient_name, age, gender, blood_group, date_of_birth, phone_number, email_address, address}}
            - medical_history: {{past_conditions, family_history, previous_surgeries, allergies}}
            - checkups: [{{symptoms, current_diagnosis, date_of_checkup, blood_pressure, heart_rate, temperature, weight, height, bmi, physical_exam_findings}}]
            - lab_tests: [{{lab_results, imaging, other_tests}}]
            - treatments: [{{related_disease, assigned_doctor, prescribed_medications, procedures, next_followup_date, lifestyle_recommendations, physiotherapy_advice}}]
            - notes: [{{doctor_remarks, special_warnings}}]
            
            Use ISO date format YYYY-MM-DD when possible. If information is missing, omit the field or use null.
            """
            
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash-lite",
                google_api_key=self.api_key,
                temperature=0.3
            )
            
            response = llm.invoke(structure_prompt)
            response_text = response.content if hasattr(response, 'content') else str(response)
            
            # Try to parse JSON from response
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group(0))
                except:
                    pass
            
            return {
                "error": "Could not structure the text into JSON",
                "raw_response": response_text[:500] + "..." if len(response_text) > 500 else response_text
            }
            
        except Exception as e:
            return {"error": f"Text processing failed: {str(e)}"}

    def image_to_patient_json(self, image_bytes: bytes) -> dict:
        """
        Use Google Generative AI (Gemini) Vision to extract key patient info from an image
        and return a structured JSON aligned with our patient schema. Requires GOOGLE_API_KEY.
        """
        try:
            self.load_api_key()
        except Exception as e:
            return {"error": f"API key error: {str(e)}"}
            
        try:
            import google.generativeai as genai
        except ImportError:
            return {
                "error": "google-generativeai package not installed. Please run: pip install google-generativeai",
            }

        try:
            genai.configure(api_key=self.api_key)

            # Define the expected JSON schema as a guide for the model
            extraction_instructions = (
                "Extract structured data from the medical report image and return ONLY valid JSON. "
                "Keys: patient (patient_name, guardian_name, age, gender, blood_group, date_of_birth, "
                "phone_number, email_address, address), medical_history (past_conditions, family_history, "
                "previous_surgeries, allergies), checkups (list of {symptoms, current_diagnosis, date_of_checkup, "
                "blood_pressure, heart_rate, temperature, weight, height, bmi, physical_exam_findings}), "
                "lab_tests (list of {lab_results, imaging, other_tests}), treatments (list of {related_disease, "
                "assigned_doctor, prescribed_medications, procedures, next_followup_date, lifestyle_recommendations, "
                "physiotherapy_advice}), notes (list of {doctor_remarks, special_warnings}). "
                "Use ISO date format YYYY-MM-DD when possible. If a field is missing, omit it or set a reasonable null/empty value."
            )

            # Try different vision model names
            vision_models = [
                "gemini-1.5-flash",
                "gemini-1.5-pro", 
                "models/gemini-1.5-flash",
                "models/gemini-1.5-pro",
                "gemini-pro-vision",
                "models/gemini-pro-vision"
            ]
            
            model = None
            working_model = None
            
            for model_name in vision_models:
                try:
                    test_model = genai.GenerativeModel(model_name)
                    # Try a simple generation to test if it works
                    test_response = test_model.generate_content("test")
                    model = test_model
                    working_model = model_name
                    break
                except Exception as e:
                    continue
            
            if model is None:
                # Fallback to OCR + LLM approach
                return self.image_to_patient_json_fallback(image_bytes)

            # Convert bytes to proper format for the API
            import base64
            image_data = base64.b64encode(image_bytes).decode('utf-8')

            # Send the image and the instruction
            response = model.generate_content([
                extraction_instructions,
                {
                    "mime_type": "image/png",
                    "data": image_data
                }
            ])

            text = response.text or ""
            
            # Try multiple approaches to extract JSON
            parsed = {}
            
            # First try: look for JSON in code blocks
            code_block_match = re.search(r'```(?:json)?\s*(\{[\s\S]*?\})\s*```', text, re.MULTILINE)
            if code_block_match:
                try:
                    parsed = json.loads(code_block_match.group(1))
                    return parsed
                except Exception:
                    pass
            
            # Second try: look for JSON at the end
            json_str_match = re.search(r'\{[\s\S]*\}', text.strip())
            if json_str_match:
                try:
                    parsed = json.loads(json_str_match.group(0))
                    return parsed
                except Exception:
                    pass
            
            # Third try: clean and parse entire response
            cleaned = text.strip()
            cleaned = re.sub(r'^```json\s*|\s*```$', '', cleaned, flags=re.MULTILINE)
            try:
                parsed = json.loads(cleaned)
                return parsed
            except Exception:
                pass
                
            # If all parsing fails, return the raw text for debugging
            return {
                "error": "Could not parse JSON from response",
                "raw_response": text[:500] + "..." if len(text) > 500 else text
            }

        except Exception as e:
            return {
                "error": f"Image processing failed: {str(e)}",
                "type": type(e).__name__
            }
