#!/usr/bin/env python3
"""
Test script to verify treatment data handling with nested structure
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'gradio'))

from prompt_engineering.prompt_template import Patient_Summary_System

def test_save_with_nested_data():
    """Test saving data with the nested structure seen in debug output"""
    PSS = Patient_Summary_System()
    
    # Test data matching the structure from debug output
    test_data = {
        "patient": {
            "patient_name": "John",
            "guardian_name": "Ali",
            "dob": "01/01/2000",
            "blood_group": "B+",
            "age": 24,
            "gender": "Male"
        },
        "medical_history": {
            "past_conditions": ["Hypertension", "Asthma"],
            "allergies": ["Allergic Rhinitis"]
        },
        "checkups": [
            {
                "vitals": {
                    "weight": "70 kg",
                    "height": "175 cm",
                    "blood_pressure": "120/80 mmHg",
                    "temperature": "37.2 °C",
                    "pulse_rate": "72 bpm",
                    "respiratory_rate": "16 breaths/min"
                }
            }
        ],
        "treatments": [
            {
                "medications": [
                    "Alstmoril",
                    "Albuterol", 
                    "Cetirizine"
                ]
            }
        ],
        "lab_tests": [],
        "notes": []
    }
    
    print("🧪 Testing nested data structure save...")
    print("📊 Data structure (matches debug output):")
    import json
    print(json.dumps(test_data, indent=2))
    
    print("\n🔄 Attempting to save...")
    result = PSS.save_to_database(test_data)
    
    print(f"\n📋 Result: {result}")
    
    if result["success"]:
        print(f"✅ SUCCESS! Patient with nested data saved with ID: {result.get('patient_id')}")
    else:
        print(f"❌ FAILED: {result.get('error')}")
        if "details" in result:
            print(f"Details: {result['details']}")

if __name__ == "__main__":
    test_save_with_nested_data()
