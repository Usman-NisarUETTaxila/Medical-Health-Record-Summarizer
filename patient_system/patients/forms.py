# forms.py
from django import forms
from django.forms import formset_factory
from .models import Patient, MedicalHistory, CheckUp, LabTests, TreatmentPlan, AdditionalNote


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'patient_name', 'guardian_name', 'age', 'gender', 'blood_group',
            'date_of_birth', 'phone_number', 'email_address', 'address'
        ]
        widgets = {
            'patient_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter patient name'
            }),
            'guardian_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter guardian name'
            }),
            'age': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0', 'max': '150'
            }),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'blood_group': forms.Select(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+1234567890'
            }),
            'email_address': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@example.com'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter complete address'
            }),
        }


class MedicalHistoryForm(forms.ModelForm):
    class Meta:
        model = MedicalHistory
        fields = ['past_conditions', 'family_history', 'previous_surgeries', 'allergies']
        widgets = {
            'past_conditions': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'List past medical conditions'
            }),
            'family_history': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Family medical history'
            }),
            'previous_surgeries': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Previous surgeries (if any)'
            }),
            'allergies': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Known allergies'
            }),
        }


class CheckUpForm(forms.ModelForm):
    class Meta:
        model = CheckUp
        fields = [
            'symptoms', 'current_diagnosis', 'date_of_checkup',
            'blood_pressure', 'heart_rate', 'temperature', 'weight',
            'height', 'bmi', 'physical_exam_findings'
        ]
        widgets = {
            'symptoms': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe symptoms'
            }),
            'current_diagnosis': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Current diagnosis'
            }),
            'date_of_checkup': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'blood_pressure': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '120/80'
            }),
            'heart_rate': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '72 bpm'
            }),
            'temperature': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '98.6°F'
            }),
            'weight': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '70 kg'
            }),
            'height': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '170 cm'
            }),
            'bmi': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '24.2'
            }),
            'physical_exam_findings': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Physical examination findings'
            }),
        }


class LabTestsForm(forms.ModelForm):
    class Meta:
        model = LabTests
        fields = ['lab_results', 'imaging', 'other_tests']
        widgets = {
            'lab_results': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Laboratory test results'
            }),
            'imaging': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'X-ray, CT scan, MRI results'
            }),
            'other_tests': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Other diagnostic tests'
            }),
        }


class TreatmentPlanForm(forms.ModelForm):
    class Meta:
        model = TreatmentPlan
        fields = [
            'related_disease', 'assigned_doctor', 'prescribed_medications',
            'procedures', 'next_followup_date', 'lifestyle_recommendations',
            'physiotherapy_advice'
        ]
        widgets = {
            'related_disease': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Disease/Condition'
            }),
            'assigned_doctor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Dr. Name'
            }),
            'prescribed_medications': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'List prescribed medications'
            }),
            'procedures': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Medical procedures'
            }),
            'next_followup_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'lifestyle_recommendations': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Lifestyle recommendations'
            }),
            'physiotherapy_advice': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Physiotherapy advice'
            }),
        }


class AdditionalNoteForm(forms.ModelForm):
    class Meta:
        model = AdditionalNote
        fields = ['doctor_remarks', 'special_warnings']
        widgets = {
            'doctor_remarks': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Doctor remarks and observations'
            }),
            'special_warnings': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Special warnings or precautions'
            }),
        }


# Create formsets for multiple entries
CheckUpFormSet = formset_factory(CheckUpForm, extra=1, can_delete=True)
LabTestsFormSet = formset_factory(LabTestsForm, extra=1, can_delete=True)
TreatmentPlanFormSet = formset_factory(TreatmentPlanForm, extra=1, can_delete=True)
AdditionalNoteFormSet = formset_factory(AdditionalNoteForm, extra=1, can_delete=True)