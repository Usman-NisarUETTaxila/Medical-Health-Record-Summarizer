from django.contrib import admin
from .models import (
    Patient,
    MedicalHistory,
    CheckUp,
    LabTests,
    TreatmentPlan,
    AdditionalNote,
)


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("id", "patient_name", "guardian_name",  "age", "gender", "date_of_birth","phone_number", "email_address", "address")
    search_fields = ("patient_name", "phone_number", "email_address")
    list_filter = ("gender", "date_of_birth")


@admin.register(MedicalHistory)
class MedicalHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "patient", "past_conditions", "family_history", "previous_surgeries", "allergies")
    search_fields = ("patient__patient_name", "past_conditions", "family_history", "previous_surgeries", "allergies")


@admin.register(CheckUp)
class CheckUpAdmin(admin.ModelAdmin):
    list_display = ("id", "patient", "symptoms", "current_diagnosis","date_of_checkup", "blood_pressure", "heart_rate", "temperature")
    search_fields = ("patient__patient_name", "symptoms", "current_diagnosis", "date_of_checkup")


@admin.register(LabTests)
class LabTestAdmin(admin.ModelAdmin):
    list_display = ("id", "patient", "lab_results", "imaging", "other_tests")
    search_fields = ("patient__patient_name", "lab_results", "imaging", "other_tests")


@admin.register(TreatmentPlan)
class TreatmentPlanAdmin(admin.ModelAdmin):
    list_display = ("id", "patient", "checkup" ,"related_disease","assigned_doctor",  "prescribed_medications", "procedures","next_followup_date" ,"lifestyle_recommendations", "physiotherapy_advice")
    search_fields = ("patient__patient_name", "checkup__date_of_checkup" "prescribed_medications", "procedures", "next_followup_date", "assigned_doctor")

@admin.register(AdditionalNote)
class AdditionalNoteAdmin(admin.ModelAdmin):
    list_display = ("id", "patient", "doctor_remarks", "special_warnings")
    search_fields = ("patient__patient_name", "doctor_remarks", "special_warnings")
