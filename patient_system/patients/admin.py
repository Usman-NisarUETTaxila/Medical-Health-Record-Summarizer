from django.contrib import admin
from .models import (
    Patient,
    MedicalHistory,
    CurrentVisit,
    Investigation,
    TreatmentPlan,
    FollowUp,
    AdditionalNote,
)


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "age", "gender", "date_of_birth", "contact_information", "address")
    search_fields = ("full_name", "contact_information")
    list_filter = ("gender", "date_of_birth")


@admin.register(MedicalHistory)
class MedicalHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "patient", "past_conditions", "family_history", "previous_surgeries", "allergies")
    search_fields = ("patient__full_name", "past_conditions", "family_history", "previous_surgeries", "allergies")


@admin.register(CurrentVisit)
class CurrentVisitAdmin(admin.ModelAdmin):
    list_display = ("id", "patient", "symptoms", "current_diagnosis", "blood_pressure", "heart_rate", "temperature")
    search_fields = ("patient__full_name", "symptoms", "current_diagnosis")


@admin.register(Investigation)
class InvestigationAdmin(admin.ModelAdmin):
    list_display = ("id", "patient", "lab_results", "imaging", "other_tests")
    search_fields = ("patient__full_name", "lab_results", "imaging", "other_tests")


@admin.register(TreatmentPlan)
class TreatmentPlanAdmin(admin.ModelAdmin):
    list_display = ("id", "patient", "prescribed_medications", "procedures", "lifestyle_recommendations", "physiotherapy_advice")
    search_fields = ("patient__full_name", "prescribed_medications", "procedures")


@admin.register(FollowUp)
class FollowUpAdmin(admin.ModelAdmin):
    list_display = ("id", "patient", "next_followup_date", "monitoring_instructions", "long_term_care_notes")
    search_fields = ("patient__full_name", "monitoring_instructions", "long_term_care_notes")


@admin.register(AdditionalNote)
class AdditionalNoteAdmin(admin.ModelAdmin):
    list_display = ("id", "patient", "doctor_remarks", "special_warnings")
    search_fields = ("patient__full_name", "doctor_remarks", "special_warnings")
