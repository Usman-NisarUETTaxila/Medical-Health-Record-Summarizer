from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Patient(models.Model):
    patient_name = models.CharField(max_length=200)
    guardian_name = models.CharField(max_length=200)
    age = models.PositiveIntegerField()
    gender = models.CharField(
        max_length=10,
        choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")],
    )
    blood_group = models.CharField(
        max_length=10,
        choices=[("AB+", "AB+"), ("A-", "A-"), ("A+", "A+"), ("AB-", "AB-"), ("B-", "B-"), ("B+", "B+"), ("O+","O+"), ("O-","O-")],
    )
    date_of_birth = models.DateField()
    phone_number = PhoneNumberField(unique=True)
    email_address = models.EmailField(max_length=254, unique=True, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.patient_name} {self.age} {self.gender}"


class MedicalHistory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="medical_history")
    past_conditions = models.TextField()
    family_history = models.TextField()
    previous_surgeries = models.TextField(blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"History for {self.patient.patient_name}"


class CheckUp(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="checkups")
    symptoms = models.TextField()
    current_diagnosis = models.TextField()
    date_of_checkup = models.DateField()

    # Vital signs
    blood_pressure = models.CharField(max_length=50)
    heart_rate = models.CharField(max_length=50)
    temperature = models.CharField(max_length=50)
    weight = models.CharField(max_length=50)
    height = models.CharField(max_length=50)
    bmi = models.CharField(max_length=50)

    physical_exam_findings = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Checkup for {self.patient.patient_name} on {self.date_of_checkup}"


class LabTests(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="labtests")
    lab_results = models.TextField()
    imaging = models.TextField(blank=True, null=True)
    other_tests = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Lab Tests for {self.patient.patient_name}"

class TreatmentPlan(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="treatments")
    checkup = models.ForeignKey(CheckUp, on_delete=models.CASCADE, related_name="checkup")
    related_disease = models.CharField(max_length=100)
    prescribed_medications = models.TextField()
    procedures = models.TextField()
    next_followup_date = models.DateField()
    lifestyle_recommendations = models.TextField(blank=True, null=True)
    physiotherapy_advice = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Treatment plan for {self.patient.patient_name}"

class AdditionalNote(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="notes")
    doctor_remarks = models.TextField()
    special_warnings = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Notes for {self.patient.patient_name}"
