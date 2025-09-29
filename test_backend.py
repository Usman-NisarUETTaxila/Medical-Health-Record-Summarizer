#!/usr/bin/env python3
"""
Test script to verify Django backend connectivity and patient creation
"""
import requests
import json
import random

def test_backend():
    base_url = "http://localhost:8000/patient-app/api/patients/"
    
    print("🔍 Testing Django Backend Connection...")
    
    # Test 1: Check if server is running
    try:
        response = requests.get(base_url, timeout=5)
        print(f"✅ Server is running! Status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Server not running: {e}")
        print("💡 Start Django server with: cd patient_system && python manage.py runserver")
        return
    
    # Test 2: Try to create a simple patient
    test_patient_data = {
        "patient": {
            "patient_name": "Test Patient",
            "guardian_name": "Test Guardian", 
            "age": 30,
            "gender": "Male",
            "blood_group": "O+",
            "date_of_birth": "1993-01-01",
            "phone_number": f"+1234567{random.randint(1000, 9999)}",
            "email_address": "test@example.com",
            "address": "123 Test Street"
        },
        "medical_history": {
            "past_conditions": "None",
            "family_history": "No significant family history",
            "previous_surgeries": "None",
            "allergies": "None"
        },
        "checkups": [
            {
                "symptoms": "Regular checkup",
                "current_diagnosis": "Healthy",
                "date_of_checkup": "2024-01-01",
                "blood_pressure": "120/80",
                "heart_rate": "72",
                "temperature": "98.6",
                "weight": "70",
                "height": "175",
                "bmi": "22.9",
                "physical_exam_findings": "Normal"
            }
        ],
        "lab_tests": [],
        "treatments": [],
        "notes": []
    }
    
    print("\n📤 Testing patient creation...")
    try:
        response = requests.post(
            base_url, 
            json=test_patient_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            patient_id = data.get('data', {}).get('patient', {}).get('id')
            print(f"✅ Patient created successfully!")
            print(f"🆔 Patient ID: {patient_id}")
            print(f"📋 Response: {json.dumps(data, indent=2)[:300]}...")
        else:
            print(f"❌ Failed to create patient")
            print(f"📄 Response: {response.text[:500]}")
            
    except Exception as e:
        print(f"❌ Error creating patient: {e}")

if __name__ == "__main__":
    test_backend()
