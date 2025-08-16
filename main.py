import os
from langchain_google_genai import ChatGoogleGenerativeAI

def get_llm():
    """Basic setup for Gemini with LangChain"""
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash", 
        temperature=0.7,
        max_tokens=1024,
        timeout=60,
        max_retries=2,
    )
    return llm


llm = get_llm()
response = llm.invoke("Explain the topic of vector DBs")
print(response.content)
    
   