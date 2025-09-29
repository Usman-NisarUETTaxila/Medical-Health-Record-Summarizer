#!/usr/bin/env python3
"""
Minimal test to verify basic save functionality
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'gradio'))

from prompt_engineering.prompt_template import Patient_Summary_System

def test_minimal_save():
    """Test with absolute minimal data"""
    PSS = Patient_Summary_System()
    
    # Minimal test data - only patient info
    test_data = {
        "patient": {
            "patient_name": "Minimal Test",
            "guardian_name": "Test Guardian",
            "age": 25,
            "gender": "Male"
        }
    }
    
    print("🧪 Testing minimal save (patient only)...")
    result = PSS.save_to_database(test_data)
    
    print(f"📋 Result: {result}")
    
    if result["success"]:
        print(f"✅ SUCCESS! Minimal patient saved with ID: {result.get('patient_id')}")
    else:
        print(f"❌ FAILED: {result.get('error')}")
        if "details" in result:
            print(f"Details: {result['details']}")

if __name__ == "__main__":
    test_minimal_save()
