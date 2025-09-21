from prompt_template import Patient_Summary_System

pss = Patient_Summary_System()
print(pss.generate_summary('http://localhost:8000/patient-app/api/patients/1/'))