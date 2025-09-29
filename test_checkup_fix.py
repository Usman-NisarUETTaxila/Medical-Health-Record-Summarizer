#!/usr/bin/env python3
"""
Test script to verify checkup data handling
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'gradio'))

from prompt_engineering.prompt_template import Patient_Summary_System

def test_save_with_checkup_data():
    """Test saving data with checkup information"""
    PSS = Patient_Summary_System()
    
    # Test data with checkup that might cause validation errors
    test_data = {
        "patient": {
            "patient_name": "Checkup Test Patient",
            "guardian_name": "Test Guardian",
            "age": 35,
            "gender": "Female"
        },
        "medical_history": {
            "past_conditions": "Hypertension",
            "allergies": "None"
        },
        "checkups": [
            {
                "symptoms": "Headache, fatigue",
                "current_diagnosis": "Migraine",
                "date_of_checkup": "2024-01-15",
                "blood_pressure": "130/85",
                "heart_rate": "78",
                "temperature": "99.1",
                "weight": "65",
                "height": "165",
                "bmi": "23.9"
            }
        ]
    }
    
    print("🧪 Testing checkup data save functionality...")
    print("📊 Data with checkup:")
    import json
    print(json.dumps(test_data, indent=2))
    
    print("\n🔄 Attempting to save...")
    result = PSS.save_to_database(test_data)
    
    print(f"\n📋 Result: {result}")
    
    if result["success"]:
        print(f"✅ SUCCESS! Patient with checkup saved with ID: {result.get('patient_id')}")
    else:
        print(f"❌ FAILED: {result.get('error')}")
        if "details" in result:
            print(f"Details: {result['details']}")

if __name__ == "__main__":
    test_save_with_checkup_data()
