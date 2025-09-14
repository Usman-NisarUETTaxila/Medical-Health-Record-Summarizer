from django.db import models


class Patient(models.Model):

    full_name = models.CharField(max_length=200)
    age = models.PositiveIntegerField()
    gender = models.CharField(
        max_length=10,
        choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")],
    )
    date_of_birth = models.DateField()
    contact_information = models.CharField(max_length=200, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.full_name


class MedicalHistory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="medical_history")
    past_conditions = models.TextField(blank=True, null=True)
    family_history = models.TextField(blank=True, null=True)
    previous_surgeries = models.TextField(blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"History for {self.patient.full_name}"


class CurrentVisit(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="visits")
    symptoms = models.TextField(blank=True, null=True)
    current_diagnosis = models.TextField(blank=True, null=True)

    # Vital signs
    blood_pressure = models.CharField(max_length=50, blank=True, null=True)
    heart_rate = models.CharField(max_length=50, blank=True, null=True)
    temperature = models.CharField(max_length=50, blank=True, null=True)
    weight = models.CharField(max_length=50, blank=True, null=True)
    height = models.CharField(max_length=50, blank=True, null=True)
    bmi = models.CharField(max_length=50, blank=True, null=True)

    physical_exam_findings = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Visit for {self.patient.full_name}"


class Investigation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="investigations")
    lab_results = models.TextField(blank=True, null=True)
    imaging = models.TextField(blank=True, null=True)
    other_tests = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Investigation for {self.patient.full_name}"


class TreatmentPlan(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="treatments")
    prescribed_medications = models.TextField(blank=True, null=True)
    procedures = models.TextField(blank=True, null=True)
    lifestyle_recommendations = models.TextField(blank=True, null=True)
    physiotherapy_advice = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Treatment plan for {self.patient.full_name}"

class FollowUp(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="followups")
    next_followup_date = models.DateField(blank=True, null=True)
    monitoring_instructions = models.TextField(blank=True, null=True)
    long_term_care_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Follow-up for {self.patient.full_name}"


class AdditionalNote(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="notes")
    doctor_remarks = models.TextField(blank=True, null=True)
    special_warnings = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Notes for {self.patient.full_name}"
