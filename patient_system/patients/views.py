from rest_framework import viewsets
from .models import (
    Patient, MedicalHistory, CurrentVisit,
    Investigation, TreatmentPlan, FollowUp, AdditionalNote
)
from .serializer import (
    PatientSerializer, MedicalHistorySerializer, CurrentVisitSerializer,
    InvestigationSerializer, TreatmentPlanSerializer,
    FollowUpSerializer, AdditionalNoteSerializer
)


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class MedicalHistoryViewSet(viewsets.ModelViewSet):
    queryset = MedicalHistory.objects.all()
    serializer_class = MedicalHistorySerializer


class CurrentVisitViewSet(viewsets.ModelViewSet):
    queryset = CurrentVisit.objects.all()
    serializer_class = CurrentVisitSerializer


class InvestigationViewSet(viewsets.ModelViewSet):
    queryset = Investigation.objects.all()
    serializer_class = InvestigationSerializer


class TreatmentPlanViewSet(viewsets.ModelViewSet):
    queryset = TreatmentPlan.objects.all()
    serializer_class = TreatmentPlanSerializer


class FollowUpViewSet(viewsets.ModelViewSet):
    queryset = FollowUp.objects.all()
    serializer_class = FollowUpSerializer


class AdditionalNoteViewSet(viewsets.ModelViewSet):
    queryset = AdditionalNote.objects.all()
    serializer_class = AdditionalNoteSerializer
