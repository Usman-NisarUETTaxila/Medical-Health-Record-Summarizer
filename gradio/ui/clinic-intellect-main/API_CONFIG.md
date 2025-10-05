# API Configuration

## Base URL
```
http://localhost:8000/patient-app
```

## Endpoints

### Get Patient by ID
- **Endpoint**: `/api/patients/{id}/`
- **Method**: GET
- **Example**: `http://localhost:8000/patient-app/api/patients/1/`

### Response Structure
```json
{
  "patient": {
    "id": 1,
    "patient_name": "Ali Khan",
    "guardian_name": "Muhammad Khan",
    "age": 28,
    "gender": "Male",
    "blood_group": "B+",
    "date_of_birth": "1997-03-15",
    "phone_number": "+923001234567",
    "email_address": "ali.khan@example.com",
    "address": "Lahore, Pakistan"
  },
  "medical_history": {
    "id": 1,
    "patient": 1,
    "patient_name": "Ali Khan",
    "past_conditions": "Asthma since childhood",
    "family_history": "Father has hypertension",
    "previous_surgeries": "Appendectomy (2015)",
    "allergies": "Dust allergy"
  },
  "checkups": [
    {
      "id": 1,
      "patient": 1,
      "patient_name": "Ali Khan",
      "symptoms": "Shortness of breath, coughing",
      "current_diagnosis": "Asthma exacerbation",
      "date_of_checkup": "2025-09-01",
      "blood_pressure": "120/80",
      "heart_rate": "88 bpm",
      "temperature": "98.6 F",
      "weight": "70kg",
      "height": "175cm",
      "bmi": "22.9",
      "physical_exam_findings": "Wheezing in lungs"
    }
  ],
  "lab_tests": [
    {
      "id": 1,
      "patient": 1,
      "patient_name": "Ali Khan",
      "lab_results": "Normal CBC",
      "imaging": "Chest X-ray clear",
      "other_tests": "Pulmonary function test reduced"
    }
  ],
  "treatments": [
    {
      "id": 1,
      "patient": 1,
      "patient_name": "Ali Khan",
      "checkup": 1,
      "checkup_date": "2025-09-01",
      "related_disease": "Asthma",
      "assigned_doctor": "Dr. Sara Ahmed",
      "prescribed_medications": "Inhaled corticosteroids, bronchodilator",
      "procedures": "Nebulization therapy",
      "next_followup_date": "2025-10-01",
      "lifestyle_recommendations": "Avoid dust, use mask outdoors",
      "physiotherapy_advice": "Breathing exercises"
    }
  ],
  "notes": [
    {
      "id": 1,
      "patient": 1,
      "patient_name": "Ali Khan",
      "doctor_remarks": "Stable condition after treatment",
      "special_warnings": "Stable condition after treatment"
    }
  ]
}
```

## CORS Configuration
The Django backend has been configured with CORS headers to allow requests from:
- `http://localhost:8080` (Frontend dev server)
- `http://localhost:8000` (Django server)

## Notes
- All API endpoints are prefixed with `/patient-app/api/`
- Patient ID is required to fetch patient data
- The response includes complete patient information including medical history, checkups, lab tests, treatments, and doctor's notes
