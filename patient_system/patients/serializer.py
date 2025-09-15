from rest_framework import serializers
from .models import Patient, MedicalHistory, CheckUp, LabTests, TreatmentPlan, AdditionalNote


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            'id', 'patient_name', 'guardian_name', 'age', 'gender',
            'blood_group', 'date_of_birth', 'phone_number', 
            'email_address', 'address'
        ]
        extra_kwargs = {
            'email_address': {'required': False, 'allow_blank': True},
            'address': {'required': False, 'allow_blank': True},
        }

    def validate_age(self, value):
        if value < 0 or value > 150:
            raise serializers.ValidationError("Age must be between 0 and 150.")
        return value


class MedicalHistorySerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.patient_name', read_only=True)
    
    class Meta:
        model = MedicalHistory
        fields = [
            'id', 'patient', 'patient_name', 'past_conditions', 
            'family_history', 'previous_surgeries', 'allergies'
        ]
        extra_kwargs = {
            'previous_surgeries': {'required': False, 'allow_blank': True},
            'allergies': {'required': False, 'allow_blank': True},
        }


class CheckUpSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.patient_name', read_only=True)
    
    class Meta:
        model = CheckUp
        fields = [
            'id', 'patient', 'patient_name', 'symptoms', 'current_diagnosis',
            'date_of_checkup', 'blood_pressure', 'heart_rate', 'temperature',
            'weight', 'height', 'bmi', 'physical_exam_findings'
        ]
        extra_kwargs = {
            'physical_exam_findings': {'required': False, 'allow_blank': True},
        }

    def validate_date_of_checkup(self, value):
        from datetime import date
        if value > date.today():
            raise serializers.ValidationError("Checkup date cannot be in the future.")
        return value


class LabTestsSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.patient_name', read_only=True)
    
    class Meta:
        model = LabTests
        fields = [
            'id', 'patient', 'patient_name', 'lab_results', 
            'imaging', 'other_tests'
        ]
        extra_kwargs = {
            'imaging': {'required': False, 'allow_blank': True},
            'other_tests': {'required': False, 'allow_blank': True},
        }


class TreatmentPlanSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.patient_name', read_only=True)
    checkup_date = serializers.DateField(source='checkup.date_of_checkup', read_only=True)
    
    class Meta:
        model = TreatmentPlan
        fields = [
            'id', 'patient', 'patient_name', 'checkup', 'checkup_date',
            'related_disease', 'assigned_doctor', 'prescribed_medications',
            'procedures', 'next_followup_date', 'lifestyle_recommendations',
            'physiotherapy_advice'
        ]
        extra_kwargs = {
            'lifestyle_recommendations': {'required': False, 'allow_blank': True},
            'physiotherapy_advice': {'required': False, 'allow_blank': True},
        }

    def validate_next_followup_date(self, value):
        from datetime import date
        if value < date.today():
            raise serializers.ValidationError("Follow-up date cannot be in the past.")
        return value


class AdditionalNoteSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.patient_name', read_only=True)
    
    class Meta:
        model = AdditionalNote
        fields = [
            'id', 'patient', 'patient_name', 'doctor_remarks', 
            'special_warnings'
        ]
        extra_kwargs = {
            'special_warnings': {'required': False, 'allow_blank': True},
        }