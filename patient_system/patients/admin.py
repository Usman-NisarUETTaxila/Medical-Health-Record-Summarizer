from django.contrib import admin
from .models import Patient, PatientDetail, Treatment, Medicine, Appointment

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "age", "gender")

@admin.register(PatientDetail)
class PatientDetailAdmin(admin.ModelAdmin):
    list_display = ("id", "patient", "address", "phone_number", "emergency_contact", 'blood_group', 'medical_history')

@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    list_display = ("id", "patient", "treatment_name", "description", "start_date", "doctor_name")

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ("id", "treatment", "medicine_name", "dosage", "frequency", "duration_days")

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("id", "patient", "appointment_date", "doctor_name", "reason")
