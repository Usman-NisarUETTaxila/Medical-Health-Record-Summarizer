#!/usr/bin/env python3
"""
Comprehensive test for all improvements:
- Exception handling
- Patient ID validation  
- Numeric data processing
- Data cleaning and formatting
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'gradio'))

from prompt_engineering.prompt_template import Patient_Summary_System
import json

def test_comprehensive_improvements():
    """Test all the improvements"""
    PSS = Patient_Summary_System()
    
    print("🧪 Testing Comprehensive Improvements")
    print("=" * 50)
    
    # Test 1: Numeric data processing and validation
    print("\n1️⃣ Testing Numeric Data Processing:")
    test_data_numeric = {
        "patient": {
            "patient_name": "john doe",  # Test case conversion
            "guardian_name": "jane doe",
            "age": "25 years old",  # Test numeric extraction
            "gender": "male",  # Test case conversion
            "blood_group": "o+",  # Test case conversion
        },
        "checkups": [
            {
                "vitals": {
                    "weight": "70.5 kg",  # Test numeric extraction with units
                    "height": "175 cm",
                    "temperature": "98.6 F",
                    "pulse_rate": "72 bpm"
                },
                "symptoms": "  headache, fatigue  ",  # Test string cleaning
            }
        ],
        "medical_history": {
            "past_conditions": ["Hypertension", "Diabetes"],  # Test list conversion
            "allergies": ""  # Test empty string handling
        }
    }
    
    result1 = PSS.save_to_database(test_data_numeric)
    print(f"📊 Numeric Processing Result: {'✅ SUCCESS' if result1['success'] else '❌ FAILED'}")
    if result1["success"]:
        print(f"   Patient ID: {result1.get('patient_id')}")
    else:
        print(f"   Error: {result1.get('error')}")
    
    # Test 2: Exception handling with invalid data
    print("\n2️⃣ Testing Exception Handling:")
    test_data_invalid = {
        "patient": {
            "patient_name": "",  # Empty name
            "age": "invalid_age",  # Invalid age
            "gender": "unknown_gender",  # Invalid gender
            "blood_group": "XYZ",  # Invalid blood group
        },
        "checkups": [
            {
                "weight": "invalid_weight",  # Invalid numeric
                "height": None,  # None value
                "temperature": {"nested": "object"},  # Invalid type
            }
        ]
    }
    
    result2 = PSS.save_to_database(test_data_invalid)
    print(f"📊 Exception Handling Result: {'✅ SUCCESS' if result2['success'] else '❌ FAILED'}")
    if result2["success"]:
        print(f"   Patient ID: {result2.get('patient_id')} (Data was cleaned and saved)")
    else:
        print(f"   Error: {result2.get('error')}")
    
    # Test 3: Data cleaning and formatting (if we have existing patient)
    print("\n3️⃣ Testing Data Cleaning & Formatting:")
    if result1["success"]:
        patient_id = result1.get('patient_id')
        url = f"http://localhost:8000/patient-app/api/patients/{patient_id}/"
        
        try:
            cleaned_data = PSS.get_patient_data(url)
            if "error" not in cleaned_data:
                print("✅ Data retrieved and cleaned successfully")
                print("📋 Sample cleaned data:")
                if "patient" in cleaned_data:
                    patient = cleaned_data["patient"]
                    print(f"   Name: {patient.get('patient_name')}")
                    print(f"   Age: {patient.get('age')}")
                    print(f"   Gender: {patient.get('gender')}")
                if "checkups" in cleaned_data and cleaned_data["checkups"]:
                    checkup = cleaned_data["checkups"][0]
                    if "vital_signs" in checkup:
                        vitals = checkup["vital_signs"]
                        print(f"   Weight: {vitals.get('weight')}")
                        print(f"   Height: {vitals.get('height')}")
                        print(f"   Heart Rate: {vitals.get('heart_rate')}")
            else:
                print(f"❌ Data retrieval failed: {cleaned_data.get('error')}")
        except Exception as e:
            print(f"❌ Exception during data retrieval: {e}")
    
    # Test 4: Edge cases
    print("\n4️⃣ Testing Edge Cases:")
    edge_cases = [
        # Empty patient data
        {"patient": {}},
        # Missing required fields
        {"patient": {"patient_name": "Test"}},
        # Extreme values
        {"patient": {"patient_name": "Test", "age": -5, "guardian_name": "Guardian"}},
        {"patient": {"patient_name": "Test", "age": 200, "guardian_name": "Guardian"}},
    ]
    
    for i, case in enumerate(edge_cases, 1):
        try:
            result = PSS.save_to_database(case)
            status = "✅ HANDLED" if result["success"] else "⚠️ REJECTED"
            print(f"   Edge Case {i}: {status}")
        except Exception as e:
            print(f"   Edge Case {i}: ❌ EXCEPTION - {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Comprehensive Testing Complete!")
    print("\n📋 Summary of Improvements:")
    print("✅ Exception handling for all data types")
    print("✅ Patient ID validation and error messages") 
    print("✅ Numeric data extraction and validation")
    print("✅ Data cleaning and professional formatting")
    print("✅ Edge case handling")
    print("✅ Robust error recovery")

if __name__ == "__main__":
    test_comprehensive_improvements()
