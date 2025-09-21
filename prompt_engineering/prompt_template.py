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

# ✅ Improved template with all fields included + risk line
template_str = """
You are a helpful medical assistant.

Your job is to take the full patient record (with many fields) and create a **user-friendly summary of 5–6 short lines**.

Rules:
- Always mention patient's **name and age** first.
- If "current_diagnosis" exists → report it clearly.
- If no disease/diagnosis → write exactly: "Patient has no reported medical conditions."
- Mention prescribed medications (or "None").
- Mention recovery plan (procedures, lifestyle, physiotherapy, follow-up).
- Merge other important details (allergies, doctor remarks, warnings) in a simple way.
- Be concise, clear, and easy to read.
- At the very end, add a ** Risk line**:
  - If labs/vitals/diagnosis indicate a risk → state it clearly (e.g., "High risk due to uncontrolled diabetes").
  - If nothing serious → write "No immediate risks reported."
  - After that, add a **Doctor’s Note** written in simple words a patient can easily understand. Avoid medical jargon.

Here are all fields you must consider:
- patient_name, age, gender, date_of_birth, phone_number, email_address, address
- past_conditions, family_history, previous_surgeries, allergies
- symptoms, current_diagnosis
- vital signs (blood_pressure, heart_rate, temperature, weight, height, bmi)
- physical_exam_findings
- lab_results, imaging, other_tests
- prescribed_medications, procedures, lifestyle_recommendations, physiotherapy_advice
- next_followup_date, monitoring_instructions
- doctor_remarks, special_warnings

Now create a **short friendly summary** in 5–6 lines only, then finish with the risk line.

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

# Example patient JSON (all fields included)
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
    "current_diagnosis": "Uncontrolled Diabetes",  # 🔹 change to None to test "no conditions"
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

# Run chain
raw_summary = chain.invoke({"record": json_input_str})
summary_text = get_buffer_string([raw_summary])

# Ensure line breaks for readability
def format_paragraphs(text):
    return re.sub(r'\.\s+', '.\n', text)

summary = format_paragraphs(summary_text)

print("📋 User-Friendly Short Medical Summary:\n")
print(summary)
