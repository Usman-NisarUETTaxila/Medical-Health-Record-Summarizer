from django.contrib import admin
from django.urls import path, include
from . import views
from . import ai_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Single endpoint for all patient CRUD operations
    path('api/patients/', views.complete_patient_data, name='patient-list-create'),
    path('api/patients/<int:patient_id>/', views.complete_patient_data, name='patient-detail'),
    
    # AI Summary endpoints
    path('api/patients/<int:patient_id>/summary/', ai_views.generate_ai_summary, name='patient-ai-summary'),
    path('api/summary/text/', ai_views.generate_summary_from_text, name='summary-from-text'),
    path('api/summary/file/', ai_views.generate_summary_from_file, name='summary-from-file'),

    # HTML form pages
    path('patients/new/', views.create_complete_patient_form, name='create_complete_patient_form'),
    path('patients/<int:patient_id>/edit/', views.edit_complete_patient_form, name='edit_complete_patient_form'),
    path('patients/<int:patient_id>/', views.patient_detail, name='patient_detail'),
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/<int:patient_id>/delete/', views.delete_patient, name='delete_patient'),
]
