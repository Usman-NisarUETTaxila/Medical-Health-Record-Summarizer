#!/usr/bin/env python3
"""
Test script with simplified data (no treatments)
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'gradio'))

from prompt_engineering.prompt_template import Patient_Summary_System

def test_simple_save():
    """Test saving without treatments to isolate the issue"""
    PSS = Patient_Summary_System()
    
    # Simplified test data without treatments
    test_data = {
        "patient": {
            "patient_name": "Simple Test",
            "guardian_name": "Test Guardian",
            "age": 30,
            "gender": "Male"
        },
        "medical_history": {
            "past_conditions": "Hypertension",
            "allergies": "None"
        },
        "checkups": [],
        "treatments": [],  # Empty treatments
        "lab_tests": [],
        "notes": []
    }
    
    print("🧪 Testing simple save (no treatments)...")
    result = PSS.save_to_database(test_data)
    
    print(f"📋 Result: {result}")
    
    if result["success"]:
        print(f"✅ SUCCESS! Simple patient saved with ID: {result.get('patient_id')}")
        
        # Now test with treatments
        print("\n🧪 Testing with treatments...")
        test_data_with_treatments = test_data.copy()
        test_data_with_treatments["patient"]["patient_name"] = "Treatment Test"
        test_data_with_treatments["treatments"] = [
            {
                "medications": ["Aspirin", "Ibuprofen"]
            }
        ]
        
        result2 = PSS.save_to_database(test_data_with_treatments)
        print(f"📋 Treatment Result: {result2}")
        
        if result2["success"]:
            print(f"✅ SUCCESS! Patient with treatments saved with ID: {result2.get('patient_id')}")
        else:
            print(f"❌ FAILED with treatments: {result2.get('error')}")
    else:
        print(f"❌ FAILED simple save: {result.get('error')}")

if __name__ == "__main__":
    test_simple_save()
