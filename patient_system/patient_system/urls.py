"""
URL configuration for patient_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from patients.views import (
    PatientViewSet, MedicalHistoryViewSet, CurrentVisitViewSet,
    InvestigationViewSet, TreatmentPlanViewSet,
    FollowUpViewSet, AdditionalNoteViewSet
)

router = DefaultRouter()
router.register(r'patients', PatientViewSet)
router.register(r'medical-history', MedicalHistoryViewSet)
router.register(r'visits', CurrentVisitViewSet)
router.register(r'investigations', InvestigationViewSet)
router.register(r'treatments', TreatmentPlanViewSet)
router.register(r'followups', FollowUpViewSet)
router.register(r'notes', AdditionalNoteViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
