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

class Patient_Summary_System():
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
