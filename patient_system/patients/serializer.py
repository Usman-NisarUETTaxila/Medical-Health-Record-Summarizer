from rest_framework import serializers
from .models import (
    Patient, MedicalHistory, CheckUp,
    LabTests, TreatmentPlan,AdditionalNote
)


class MedicalHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalHistory
        fields = '__all__'


class CheckUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckUp
        fields = '__all__'


class LabTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabTests
        fields = '__all__'


class TreatmentPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreatmentPlan
        fields = '__all__'


class AdditionalNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalNote
        fields = '__all__'


class PatientSerializer(serializers.ModelSerializer):
    medical_history = MedicalHistorySerializer(many=True, read_only=True)
    checkups = CheckUpSerializer(many=True, read_only=True)
    labtests = LabTestSerializer(many=True, read_only=True)
    treatments = TreatmentPlanSerializer(many=True, read_only=True)
    notes = AdditionalNoteSerializer(many=True, read_only=True)

    class Meta:
        model = Patient
        fields = '__all__'
