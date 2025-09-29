import os
from dotenv import load_dotenv
load_dotenv()

try:
    import google.generativeai as genai
    
    api_key = os.getenv("GOOGLE_API_KEY")
    print(f"API Key found: {'Yes' if api_key else 'No'}")
    
    if api_key:
        genai.configure(api_key=api_key)
        
        # Test basic text generation
        try:
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content("Hello")
            print("✅ Text generation works!")
            print(f"Response: {response.text}")
        except Exception as e:
            print(f"❌ Text generation failed: {e}")
        
        # Test vision model
        try:
            model = genai.GenerativeModel("gemini-pro-vision")
            print("✅ Vision model accessible!")
        except Exception as e:
            print(f"❌ Vision model failed: {e}")

except Exception as e:
    print(f"Error: {e}")
