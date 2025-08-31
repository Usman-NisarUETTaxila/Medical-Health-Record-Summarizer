import os
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
Your task is to read the patient's unstructured medical record and summarize it in a structured, detailed format.

Patient Record (unstructured):
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

# Example unstructured record (raw text, messy)
medical_record = """
Patient seen today, Johnathan Doe, 46 years old male. Complains of frequent urination, fatigue, and blurred vision. 
History of Type 2 Diabetes for 5 years, mother also diabetic. Past surgery: appendix removal in 2001. 
No drug allergies. 
Vitals: BP 140/90, HR 85, Temp 98.7F, Weight 85kg, Height 175cm. 
HbA1c 8.2%, Fasting sugar 170 mg/dL. 
Doctor suspects uncontrolled diabetes. 
Prescribed Metformin 1000mg twice daily and Insulin injection 10 units before breakfast. 
Advised low-carb diet, daily walking 30 min. 
Next visit in 1 month (30 Sept 2025). 
Contact: 123-456-7890, Address: 221B Baker Street, London.
"""

# Run chain
summary = chain.run(record=medical_record)
print("📋 Structured Medical Summary:\n", summary)
