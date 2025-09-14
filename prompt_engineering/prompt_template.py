import os
import json
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI

# Load API key from environment
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("⚠️ No API key found. Restart PyCharm after setting the variable.")

# Configure Gemini with LangChain
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=api_key,
    temperature=0.3  # lower temp = structured, factual output
)

# Enhanced structured prompt
template = """
You are an intelligent medical assistant. 
Your task is to read the patient's medical record (provided in JSON format) and summarize it in a structured, detailed format.

Patient Record (JSON):
{record}

Provide a structured medical summary with the following fields:

**Patient Information**
- Full Name
- Age
- Gender
- Date of Birth
- Contact Information
- Address

**Medical History**
- Past medical conditions
- Family medical history
- Previous surgeries
- Allergies

**Current Visit**
- Symptoms/Chief complaint
- Current diagnosis
- Vital signs (Blood pressure, Heart rate, Temperature, Weight, Height, BMI)
- Physical examination findings

**Investigations**
- Lab results (Blood tests, Urine tests, etc.)
- Imaging (X-ray, MRI, CT, Ultrasound)
- Other diagnostic tests

**Treatment Plan**
- Prescribed medications (name, dosage, frequency, duration)
- Procedures recommended
- Lifestyle & diet recommendations
- Physiotherapy/rehabilitation advice (if applicable)

**Follow-up**
- Next follow-up date
- Monitoring instructions
- Long-term care notes

**Additional Notes**
- Doctor’s remarks
- Special warnings (if any)
"""

prompt = PromptTemplate(
    input_variables=["record"],
    template=template
)

# Create chain
chain = LLMChain(llm=llm, prompt=prompt)

# -------------------------------
# Dummy JSON input (example file)
# -------------------------------
dummy_patient_json = {
    "Patient Information": {
        "Full Name": "Johnathan Doe",
        "Age": 46,
        "Gender": "Male",
        "Date of Birth": "1979-05-14",
        "Contact Information": "123-456-7890",
        "Address": "221B Baker Street, London"
    },
    "Medical History": {
        "Past medical conditions": ["Type 2 Diabetes (5 years)"],
        "Family medical history": ["Mother - Diabetes"],
        "Previous surgeries": ["Appendix removal (2001)"],
        "Allergies": []
    },
    "Current Visit": {
        "Symptoms": ["Frequent urination", "Fatigue", "Blurred vision"],
        "Diagnosis": "Uncontrolled Diabetes",
        "Vitals": {
            "Blood pressure": "140/90",
            "Heart rate": "85",
            "Temperature": "98.7F",
            "Weight": "85kg",
            "Height": "175cm",
            "BMI": "27.8"
        }
    },
    "Investigations": {
        "Lab results": {"HbA1c": "8.2%", "Fasting sugar": "170 mg/dL"},
        "Imaging": None,
        "Other tests": None
    },
    "Treatment Plan": {
        "Medications": [
            {"name": "Metformin", "dosage": "1000mg", "frequency": "Twice daily"},
            {"name": "Insulin", "dosage": "10 units", "frequency": "Before breakfast"}
        ],
        "Lifestyle": "Low-carb diet, daily walking 30 minutes"
    },
    "Follow-up": {
        "Next visit": "2025-09-30",
        "Monitoring": "Blood sugar monitoring daily"
    },
    "Additional Notes": {
        "Doctor’s remarks": "Patient needs strict diet control",
        "Special warnings": None
    }
}

# Convert JSON dict to string so LLM can read it
json_input_str = json.dumps(dummy_patient_json, indent=2)

# Run chain
summary = chain.run(record=json_input_str)

print("📋 Structured Medical Summary:\n")
print(summary)
