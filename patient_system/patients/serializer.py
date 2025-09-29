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
            'past_conditions': {'required': False, 'allow_blank': True},
            'family_history': {'required': False, 'allow_blank': True},
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
            'symptoms': {'required': False, 'allow_blank': True},
            'current_diagnosis': {'required': False, 'allow_blank': True},
            'date_of_checkup': {'required': False},
            'blood_pressure': {'required': False, 'allow_blank': True},
            'heart_rate': {'required': False, 'allow_blank': True},
            'temperature': {'required': False, 'allow_blank': True},
            'weight': {'required': False, 'allow_blank': True},
            'height': {'required': False, 'allow_blank': True},
            'bmi': {'required': False, 'allow_blank': True},
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
            'lab_results': {'required': False, 'allow_blank': True},
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
            'checkup': {'required': False},
            'related_disease': {'required': False, 'allow_blank': True},
            'assigned_doctor': {'required': False, 'allow_blank': True},
            'prescribed_medications': {'required': False, 'allow_blank': True},
            'procedures': {'required': False, 'allow_blank': True},
            'next_followup_date': {'required': False},
            'lifestyle_recommendations': {'required': False, 'allow_blank': True},
            'physiotherapy_advice': {'required': False, 'allow_blank': True},
        }

    def validate_next_followup_date(self, value):
        # Allow None values and skip validation for empty dates
        if value is None or value == "":
            return None
        from datetime import date
        if isinstance(value, str):
            try:
                from datetime import datetime
                value = datetime.strptime(value, "%Y-%m-%d").date()
            except:
                return None
        if value and value < date.today():
            # Don't raise error, just set to None for past dates
            return None
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
            'doctor_remarks': {'required': False, 'allow_blank': True},
            'special_warnings': {'required': False, 'allow_blank': True},
        }