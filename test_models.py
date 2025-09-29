import os
from dotenv import load_dotenv
load_dotenv()

try:
    import google.generativeai as genai
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ No GOOGLE_API_KEY found in .env file")
        exit()
    
    genai.configure(api_key=api_key)
    
    print("🔍 Available models:")
    print("-" * 50)
    
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"✅ {model.name}")
            print(f"   Methods: {model.supported_generation_methods}")
            print()
    
    print("\n🧪 Testing text generation:")
    test_models = ["gemini-pro", "models/gemini-pro", "gemini-1.5-flash", "models/gemini-1.5-flash"]
    
    for model_name in test_models:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Say hello")
            print(f"✅ {model_name}: {response.text}")
            break
        except Exception as e:
            print(f"❌ {model_name}: {str(e)[:100]}...")
    
    print("\n🖼️ Testing vision models:")
    vision_models = ["gemini-pro-vision", "gemini-1.5-pro", "models/gemini-pro-vision"]
    
    for model_name in vision_models:
        try:
            model = genai.GenerativeModel(model_name)
            print(f"✅ {model_name} - Available")
        except Exception as e:
            print(f"❌ {model_name} - {e}")

except ImportError:
    print("❌ google-generativeai not installed. Run: pip install google-generativeai")
except Exception as e:
    print(f"❌ Error: {e}")
