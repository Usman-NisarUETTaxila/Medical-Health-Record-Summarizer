from rest_framework import serializers
from .models import (
    Patient, MedicalHistory, CheckUp,
    LabTests, TreatmentPlan,AdditionalNote
)


class MedicalHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalHistory
        fields = '__all__'


class CurrentVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrentVisit
        fields = '__all__'


class InvestigationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investigation
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
    checkups = CurrentVisitSerializer(many=True, read_only=True)
    labtests = InvestigationSerializer(many=True, read_only=True)
    treatments = TreatmentPlanSerializer(many=True, read_only=True)
    notes = AdditionalNoteSerializer(many=True, read_only=True)

    class Meta:
        model = Patient
        fields = '__all__'
