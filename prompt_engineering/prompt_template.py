import os
import json
import re
from langchain_core.runnables import RunnableSequence
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages.utils import get_buffer_string

# Load API key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("⚠️ No API key found. Please set GOOGLE_API_KEY environment variable and restart.")

# Prompt template with explicit mention of all fields + conclusion
template_str = """
You are a knowledgeable and compassionate medical assistant.

Your task is to analyze the patient's medical record provided in JSON format, and generate a **concise but complete structured summary**.

🔹 Rules:
- Cover **all fields** provided in the JSON.
- If a field is missing, null, or empty, explicitly write "None" or "Not reported."
- Use **bold section headings**.
- Write short, clear sentences.
- Use bullet points for lists like symptoms, medications, past conditions.
- At the very end, add a **bold one-line conclusion** that summarizes:
  - Main diagnosis
  - Critical health risk
  - Key recommendation

📋 Sections to include:

**Patient Information**
- patient_name
- age
- gender
- date_of_birth
- phone_number
- email_address
- address

**Medical History**
- past_conditions
- family_history
- previous_surgeries
- allergies

**Current Visit**
- symptoms
- current_diagnosis
- vital signs (blood_pressure, heart_rate, temperature, weight, height, bmi)
- physical_exam_findings

**Investigations**
- lab_results
- imaging
- other_tests

**Treatment Plan**
- prescribed_medications
- procedures
- lifestyle_recommendations
- physiotherapy_advice

**Follow-up**
- next_followup_date
- monitoring_instructions

**Additional Notes**
- doctor_remarks
- special_warnings

**Conclusion**
→ One line summary of diagnosis, risk, and recommendation.

Patient Record JSON:
{record}
"""

prompt = PromptTemplate(
    input_variables=["record"],
    template=template_str
)

# Initialize Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=api_key,
    temperature=0.3
)

# Create RunnableSequence chain
chain = RunnableSequence(prompt | llm)

# Example patient JSON
dummy_patient_json = {
    "patient_name": "Johnathan Doe",
    "age": 46,
    "gender": "Male",
    "date_of_birth": "1979-05-14",
    "phone_number": "+1234567890",
    "email_address": "john.doe@example.com",
    "address": "221B Baker Street, London",
    "past_conditions": ["Type 2 Diabetes (5 years)"],
    "family_history": ["Mother - Diabetes"],
    "previous_surgeries": ["Appendix removal (2001)"],
    "allergies": [],
    "symptoms": ["Frequent urination", "Fatigue", "Blurred vision"],
    "current_diagnosis": "Uncontrolled Diabetes",
    "blood_pressure": "140/90",
    "heart_rate": "85",
    "temperature": "98.7F",
    "weight": "85kg",
    "height": "175cm",
    "bmi": "27.8",
    "physical_exam_findings": "Normal heart sounds",
    "lab_results": {"HbA1c": "8.2%", "Fasting sugar": "170 mg/dL"},
    "imaging": None,
    "other_tests": None,
    "prescribed_medications": [
        "Metformin 1000mg twice daily",
        "Insulin 10 units before breakfast"
    ],
    "procedures": "None",
    "lifestyle_recommendations": "Low-carb diet, daily walking 30 minutes",
    "physiotherapy_advice": None,
    "next_followup_date": "2025-09-30",
    "monitoring_instructions": "Blood sugar monitoring daily",
    "doctor_remarks": "Patient needs strict diet control",
    "special_warnings": None
}

# Convert dict to JSON string
json_input_str = json.dumps(dummy_patient_json, indent=2)

# Invoke chain and get AIMessage output
raw_summary = chain.invoke({"record": json_input_str})

# Convert AIMessage to plain string
summary_text = get_buffer_string([raw_summary])

# Post-process string: ensure each sentence starts on a new line
def format_paragraphs(text):
    return re.sub(r'\.\s+', '.\n', text)

# Final formatted summary
summary = format_paragraphs(summary_text)

print("📋 Structured Medical Summary:\n")
print(summary)
