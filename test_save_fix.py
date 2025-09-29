#!/usr/bin/env python3
"""
Test script to verify the save functionality with proper data formatting
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'gradio'))

from prompt_engineering.prompt_template import Patient_Summary_System

def test_save_with_problematic_data():
    """Test saving data that previously caused validation errors"""
    PSS = Patient_Summary_System()
    
    # Test data that might cause "Not a valid string" errors
    test_data = {
        "patient": {
            "patient_name": "Test Patient",
            "guardian_name": "Test Guardian",
            "age": 30,
            "gender": "Male",
            "blood_group": "O+",
            "date_of_birth": "1990-01-01"
        },
        "medical_history": {
            "past_conditions": ["Hypertension", "Diabetes"],  # List instead of string
            "family_history": {"father": "Heart disease", "mother": "Diabetes"},  # Dict instead of string
            "allergies": ["Penicillin", "Peanuts"],  # List instead of string
            "previous_surgeries": None  # None value
        },
        "checkups": {  # Dict instead of list
            "symptoms": "Headache",
            "current_diagnosis": "Migraine",
            "date_of_checkup": "2024-01-01",
            "blood_pressure": "120/80",
            "heart_rate": "72",
            "temperature": "98.6",
            "weight": "70",
            "height": "175",
            "bmi": "22.9"
        },
        "lab_tests": [],
        "treatments": [],
        "notes": []
    }
    
    print("🧪 Testing save functionality with problematic data types...")
    print("📊 Original data structure:")
    import json
    print(json.dumps(test_data, indent=2, default=str))
    
    print("\n🔄 Attempting to save...")
    result = PSS.save_to_database(test_data)
    
    print(f"\n📋 Result: {result}")
    
    if result["success"]:
        print(f"✅ SUCCESS! Patient saved with ID: {result.get('patient_id')}")
    else:
        print(f"❌ FAILED: {result.get('error')}")
        if "details" in result:
            print(f"Details: {result['details']}")

if __name__ == "__main__":
    test_save_with_problematic_data()
