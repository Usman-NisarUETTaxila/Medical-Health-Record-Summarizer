#!/usr/bin/env python3
"""
Debug test to see exact error details
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'gradio'))

from prompt_engineering.prompt_template import Patient_Summary_System
import json

def test_debug_save():
    """Test with debug output"""
    PSS = Patient_Summary_System()
    
    # Simple test with treatments
    test_data = {
        "patient": {
            "patient_name": "Debug Test",
            "guardian_name": "Test Guardian",
            "age": 30,
            "gender": "Male"
        },
        "medical_history": {
            "past_conditions": "None",
            "allergies": "None"
        },
        "treatments": [
            {
                "medications": ["Aspirin"]
            }
        ]
    }
    
    print("🧪 Testing with debug output...")
    print("📊 Input data:")
    print(json.dumps(test_data, indent=2))
    
    result = PSS.save_to_database(test_data)
    
    print(f"\n📋 Full Result: {json.dumps(result, indent=2)}")
    
    if result["success"]:
        print(f"✅ SUCCESS! Patient saved with ID: {result.get('patient_id')}")
    else:
        print(f"❌ FAILED: {result.get('error')}")
        if "details" in result:
            print(f"Details: {result['details']}")

if __name__ == "__main__":
    test_debug_save()
