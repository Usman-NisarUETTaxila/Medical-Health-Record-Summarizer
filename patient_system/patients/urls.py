from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Single endpoint for all patient CRUD operations
    path('api/patients/', views.complete_patient_data, name='patient-list-create'),
    path('api/patients/<int:patient_id>/', views.complete_patient_data, name='patient-detail'),

    # HTML form pages
    path('patients/new/', views.create_complete_patient_form, name='create_complete_patient_form'),
    path('patients/<int:patient_id>/edit/', views.edit_complete_patient_form, name='edit_complete_patient_form'),
    path('patients/<int:patient_id>/', views.patient_detail, name='patient_detail'),
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/<int:patient_id>/delete/', views.delete_patient, name='delete_patient'),
]
