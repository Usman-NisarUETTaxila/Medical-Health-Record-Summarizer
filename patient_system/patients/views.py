from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import  render, redirect, get_object_or_404
from django.db import transaction
from datetime import datetime
from .models import Patient, MedicalHistory, CheckUp, LabTests, TreatmentPlan, AdditionalNote
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from .forms import (
    PatientForm, MedicalHistoryForm, CheckUpFormSet, 
    LabTestsFormSet, TreatmentPlanFormSet, AdditionalNoteFormSet
)
from .serializer import (
    PatientSerializer, 
    MedicalHistorySerializer, 
    CheckUpSerializer, 
    LabTestsSerializer, 
    TreatmentPlanSerializer, 
    AdditionalNoteSerializer
)

# Api Views
@api_view(['POST', 'GET', 'PUT', 'DELETE'])
def complete_patient_data(request, patient_id=None):
    """
    Single view to handle all CRUD operations for complete patient data
    POST: Create complete patient record with all related data
    GET: Retrieve patient with all related data  
    PUT: Update patient and related data
    DELETE: Delete patient and all related data
    """
    
    if request.method == 'POST':
        return create_complete_patient(request)
    
    elif request.method == 'GET':
        if patient_id:
            return get_complete_patient(request, patient_id)
        else:
            return get_all_patients(request)
    
    elif request.method == 'PUT':
        return update_complete_patient(request, patient_id)
    
    elif request.method == 'DELETE':
        return delete_patient(request, patient_id)


def create_complete_patient(request):
    """Create a complete patient record with all related data"""
    with transaction.atomic():
        try:
            # Extract patient data
            patient_data = request.data.get('patient', {})
            patient_serializer = PatientSerializer(data=patient_data)
            
            if not patient_serializer.is_valid():
                return Response({
                    'error': 'Patient data validation failed',
                    'details': patient_serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Create patient
            patient = patient_serializer.save()
            
            created_data = {
                'patient': patient_serializer.data,
                'medical_history': None,
                'checkups': [],
                'lab_tests': [],
                'treatments': [],
                'notes': []
            }
            
            # Create Medical History
            medical_history_data = request.data.get('medical_history')
            if medical_history_data:
                medical_history_data['patient'] = patient.id
                history_serializer = MedicalHistorySerializer(data=medical_history_data)
                if history_serializer.is_valid():
                    history = history_serializer.save()
                    created_data['medical_history'] = history_serializer.data
                else:
                    return Response({
                        'error': 'Medical history validation failed',
                        'details': history_serializer.errors
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            # Create CheckUps (can be multiple)
            checkups_data = request.data.get('checkups', [])
            if not isinstance(checkups_data, list):
                checkups_data = [checkups_data]
            
            created_checkups = []
            for checkup_data in checkups_data:
                if checkup_data:
                    checkup_data['patient'] = patient.id
                    checkup_serializer = CheckUpSerializer(data=checkup_data)
                    if checkup_serializer.is_valid():
                        checkup = checkup_serializer.save()
                        created_checkups.append(checkup)
                        created_data['checkups'].append(checkup_serializer.data)
                    else:
                        return Response({
                            'error': 'Checkup data validation failed',
                            'details': checkup_serializer.errors
                        }, status=status.HTTP_400_BAD_REQUEST)
            
            # Create Lab Tests (can be multiple)
            lab_tests_data = request.data.get('lab_tests', [])
            if not isinstance(lab_tests_data, list):
                lab_tests_data = [lab_tests_data]
            
            for lab_data in lab_tests_data:
                if lab_data:
                    lab_data['patient'] = patient.id
                    lab_serializer = LabTestsSerializer(data=lab_data)
                    if lab_serializer.is_valid():
                        lab = lab_serializer.save()
                        created_data['lab_tests'].append(lab_serializer.data)
                    else:
                        return Response({
                            'error': 'Lab tests validation failed',
                            'details': lab_serializer.errors
                        }, status=status.HTTP_400_BAD_REQUEST)
            
            # Create Treatment Plans (can be multiple)
            treatments_data = request.data.get('treatments', [])
            if not isinstance(treatments_data, list):
                treatments_data = [treatments_data]
            
            for treatment_data in treatments_data:
                if treatment_data:
                    treatment_data['patient'] = patient.id
                    
                    # Link to checkup if available
                    if created_checkups and 'checkup' not in treatment_data:
                        treatment_data['checkup'] = created_checkups[0].id
                    
                    treatment_serializer = TreatmentPlanSerializer(data=treatment_data)
                    if treatment_serializer.is_valid():
                        treatment = treatment_serializer.save()
                        created_data['treatments'].append(treatment_serializer.data)
                    else:
                        return Response({
                            'error': 'Treatment plan validation failed',
                            'details': treatment_serializer.errors
                        }, status=status.HTTP_400_BAD_REQUEST)
            
            # Create Additional Notes (can be multiple)
            notes_data = request.data.get('notes', [])
            if not isinstance(notes_data, list):
                notes_data = [notes_data]
            
            for note_data in notes_data:
                if note_data:
                    note_data['patient'] = patient.id
                    note_serializer = AdditionalNoteSerializer(data=note_data)
                    if note_serializer.is_valid():
                        note = note_serializer.save()
                        created_data['notes'].append(note_serializer.data)
                    else:
                        return Response({
                            'error': 'Notes validation failed',
                            'details': note_serializer.errors
                        }, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({
                'message': 'Complete patient record created successfully',
                'data': created_data
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'error': 'Failed to create patient record',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def get_complete_patient(request, patient_id):
    """Retrieve a complete patient record with all related data"""
    try:
        patient = get_object_or_404(Patient, id=patient_id)
        
        # Serialize patient data
        patient_data = PatientSerializer(patient).data
        
        # Get all related data
        complete_data = {
            'patient': patient_data,
            'medical_history': None,
            'checkups': [],
            'lab_tests': [],
            'treatments': [],
            'notes': []
        }
        
        # Medical History
        medical_history = patient.medical_history.first()
        if medical_history:
            complete_data['medical_history'] = MedicalHistorySerializer(medical_history).data
        
        # CheckUps (ordered by date)
        checkups = patient.checkups.all().order_by('-date_of_checkup')
        complete_data['checkups'] = CheckUpSerializer(checkups, many=True).data
        
        # Lab Tests
        lab_tests = patient.labtests.all()
        complete_data['lab_tests'] = LabTestsSerializer(lab_tests, many=True).data
        
        # Treatment Plans (ordered by follow-up date)
        treatments = patient.treatments.all().order_by('-next_followup_date')
        complete_data['treatments'] = TreatmentPlanSerializer(treatments, many=True).data
        
        # Additional Notes
        notes = patient.notes.all()
        complete_data['notes'] = AdditionalNoteSerializer(notes, many=True).data
        
        return Response(complete_data)
        
    except Exception as e:
        return Response({
            'error': 'Failed to retrieve patient data',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def get_all_patients(request):
    """Get all patients with basic info and counts of related records"""
    try:
        patients = Patient.objects.all()
        patients_data = []
        
        for patient in patients:
            patient_info = PatientSerializer(patient).data
            patient_info.update({
                'medical_history_count': patient.medical_history.count(),
                'checkups_count': patient.checkups.count(),
                'lab_tests_count': patient.labtests.count(),
                'treatments_count': patient.treatments.count(),
                'notes_count': patient.notes.count(),
                'last_checkup_date': patient.checkups.first().date_of_checkup if patient.checkups.exists() else None
            })
            patients_data.append(patient_info)
        
        return Response({
            'count': len(patients_data),
            'patients': patients_data
        })
        
    except Exception as e:
        return Response({
            'error': 'Failed to retrieve patients list',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def update_complete_patient(request, patient_id):
    """Update patient and related data"""
    with transaction.atomic():
        try:
            patient = get_object_or_404(Patient, id=patient_id)
            
            # Update patient data if provided
            patient_data = request.data.get('patient')
            if patient_data:
                patient_serializer = PatientSerializer(patient, data=patient_data, partial=True)
                if patient_serializer.is_valid():
                    patient_serializer.save()
                else:
                    return Response({
                        'error': 'Patient update validation failed',
                        'details': patient_serializer.errors
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            # Update or create medical history
            medical_history_data = request.data.get('medical_history')
            if medical_history_data:
                medical_history = patient.medical_history.first()
                if medical_history:
                    history_serializer = MedicalHistorySerializer(medical_history, data=medical_history_data, partial=True)
                else:
                    medical_history_data['patient'] = patient.id
                    history_serializer = MedicalHistorySerializer(data=medical_history_data)
                
                if history_serializer.is_valid():
                    history_serializer.save()
                else:
                    return Response({
                        'error': 'Medical history update failed',
                        'details': history_serializer.errors
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            # Handle other related data updates similar to medical history...
            # For brevity, showing the pattern with medical history
            
            # Get updated complete data
            return get_complete_patient(request, patient_id)
            
        except Exception as e:
            return Response({
                'error': 'Failed to update patient record',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def delete_patient(request, patient_id):
    """Delete patient and all related data"""
    try:
        patient = get_object_or_404(Patient, id=patient_id)
        patient_name = patient.patient_name
        
        # Django will handle cascade deletion of related records
        patient.delete()
        
        return Response({
            'message': f'Patient {patient_name} and all related data deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)
        
    except Exception as e:
        return Response({
            'error': 'Failed to delete patient',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Page Views

def create_complete_patient_form(request):
    """View to create complete patient record with form"""
    if request.method == 'POST':
        return handle_patient_form_submission(request)
    
    # GET request - show empty form
    context = {
        'patient_form': PatientForm(),
        'medical_history_form': MedicalHistoryForm(),
        'checkup_formset': CheckUpFormSet(),
        'lab_tests_formset': LabTestsFormSet(),
        'treatment_formset': TreatmentPlanFormSet(),
        'notes_formset': AdditionalNoteFormSet(),
        'form_action': 'create',
        'page_title': 'Create New Patient Record'
    }
    
    return render(request, 'patient_form.html', context)


def edit_complete_patient_form(request, patient_id):
    """View to edit complete patient record"""
    patient = get_object_or_404(Patient, id=patient_id)
    
    if request.method == 'POST':
        return handle_patient_form_submission(request, patient)
    
    # GET request - show form with existing data
    medical_history = patient.medical_history.first()
    checkups = patient.checkups.all().order_by('-date_of_checkup')
    lab_tests = patient.labtests.all()
    treatments = patient.treatments.all().order_by('-next_followup_date')
    notes = patient.notes.all()
    
    # Prepare initial data for formsets
    checkup_initial = [
        {
            'symptoms': checkup.symptoms,
            'current_diagnosis': checkup.current_diagnosis,
            'date_of_checkup': checkup.date_of_checkup,
            'blood_pressure': checkup.blood_pressure,
            'heart_rate': checkup.heart_rate,
            'temperature': checkup.temperature,
            'weight': checkup.weight,
            'height': checkup.height,
            'bmi': checkup.bmi,
            'physical_exam_findings': checkup.physical_exam_findings,
        } for checkup in checkups
    ]
    
    lab_initial = [
        {
            'lab_results': lab.lab_results,
            'imaging': lab.imaging,
            'other_tests': lab.other_tests,
        } for lab in lab_tests
    ]
    
    treatment_initial = [
        {
            'related_disease': treatment.related_disease,
            'assigned_doctor': treatment.assigned_doctor,
            'prescribed_medications': treatment.prescribed_medications,
            'procedures': treatment.procedures,
            'next_followup_date': treatment.next_followup_date,
            'lifestyle_recommendations': treatment.lifestyle_recommendations,
            'physiotherapy_advice': treatment.physiotherapy_advice,
        } for treatment in treatments
    ]
    
    notes_initial = [
        {
            'doctor_remarks': note.doctor_remarks,
            'special_warnings': note.special_warnings,
        } for note in notes
    ]
    
    context = {
        'patient_form': PatientForm(instance=patient),
        'medical_history_form': MedicalHistoryForm(instance=medical_history),
        'checkup_formset': CheckUpFormSet(initial=checkup_initial),
        'lab_tests_formset': LabTestsFormSet(initial=lab_initial),
        'treatment_formset': TreatmentPlanFormSet(initial=treatment_initial),
        'notes_formset': AdditionalNoteFormSet(initial=notes_initial),
        'patient': patient,
        'form_action': 'edit',
        'page_title': f'Edit Patient Record - {patient.patient_name}'
    }
    
    return render(request, 'patient_form.html', context)


def handle_patient_form_submission(request, patient=None):
    """Handle form submission for both create and update"""
    is_edit = patient is not None
    
    # Initialize forms
    patient_form = PatientForm(request.POST, instance=patient)
    medical_history = patient.medical_history.first() if is_edit else None
    medical_history_form = MedicalHistoryForm(request.POST, instance=medical_history)
    
    checkup_formset = CheckUpFormSet(request.POST)
    lab_tests_formset = LabTestsFormSet(request.POST)
    treatment_formset = TreatmentPlanFormSet(request.POST)
    notes_formset = AdditionalNoteFormSet(request.POST)
    
    # Validate all forms
    forms_valid = (
        patient_form.is_valid() and
        medical_history_form.is_valid() and
        checkup_formset.is_valid() and
        lab_tests_formset.is_valid() and
        treatment_formset.is_valid() and
        notes_formset.is_valid()
    )
    
    if forms_valid:
        try:
            with transaction.atomic():
                # Save patient
                patient_instance = patient_form.save()
                
                # Save medical history
                if medical_history_form.cleaned_data:
                    medical_history_instance = medical_history_form.save(commit=False)
                    medical_history_instance.patient = patient_instance
                    medical_history_instance.save()
                
                # Clear existing related data if editing
                if is_edit:
                    patient_instance.checkups.all().delete()
                    patient_instance.labtests.all().delete()
                    patient_instance.treatments.all().delete()
                    patient_instance.notes.all().delete()
                
                saved_checkups = []
                
                # Save checkups
                for checkup_form in checkup_formset:
                    if checkup_form.cleaned_data and not checkup_form.cleaned_data.get('DELETE', False):
                        checkup_instance = checkup_form.save(commit=False)
                        checkup_instance.patient = patient_instance
                        checkup_instance.save()
                        saved_checkups.append(checkup_instance)
                
                # Save lab tests
                for lab_form in lab_tests_formset:
                    if lab_form.cleaned_data and not lab_form.cleaned_data.get('DELETE', False):
                        lab_instance = lab_form.save(commit=False)
                        lab_instance.patient = patient_instance
                        lab_instance.save()
                
                # Save treatments
                for treatment_form in treatment_formset:
                    if treatment_form.cleaned_data and not treatment_form.cleaned_data.get('DELETE', False):
                        treatment_instance = treatment_form.save(commit=False)
                        treatment_instance.patient = patient_instance
                        
                        # Link to first checkup if available
                        if saved_checkups:
                            treatment_instance.checkup = saved_checkups[0]
                        
                        treatment_instance.save()
                
                # Save notes
                for note_form in notes_formset:
                    if note_form.cleaned_data and not note_form.cleaned_data.get('DELETE', False):
                        note_instance = note_form.save(commit=False)
                        note_instance.patient = patient_instance
                        note_instance.save()
                
                action = "updated" if is_edit else "created"
                messages.success(
                    request, 
                    f'Patient record for {patient_instance.patient_name} has been {action} successfully!'
                )
                
                return redirect('patient_detail', patient_id=patient_instance.id)
                
        except Exception as e:
            messages.error(request, f'Error saving patient record: {str(e)}')
    
    else:
        # Form validation failed
        messages.error(request, 'Please correct the errors in the form.')
    
    # Return form with errors
    context = {
        'patient_form': patient_form,
        'medical_history_form': medical_history_form,
        'checkup_formset': checkup_formset,
        'lab_tests_formset': lab_tests_formset,
        'treatment_formset': treatment_formset,
        'notes_formset': notes_formset,
        'patient': patient,
        'form_action': 'edit' if is_edit else 'create',
        'page_title': f'Edit Patient Record - {patient.patient_name}' if is_edit else 'Create New Patient Record'
    }
    
    return render(request, 'patient_form.html', context)


def patient_detail(request, patient_id):
    """View to display complete patient details"""
    patient = get_object_or_404(Patient, id=patient_id)
    medical_history = patient.medical_history.first()
    checkups = patient.checkups.all().order_by('-date_of_checkup')
    lab_tests = patient.labtests.all()
    treatments = patient.treatments.all().order_by('-next_followup_date')
    notes = patient.notes.all()
    
    context = {
        'patient': patient,
        'medical_history': medical_history,
        'checkups': checkups,
        'lab_tests': lab_tests,
        'treatments': treatments,
        'notes': notes,
    }
    
    return render(request, 'patient_detail.html', context)


def patient_list(request):
    """View to list all patients"""
    patients = Patient.objects.all().order_by('-id')
    
    # Add summary data for each patient
    patient_data = []
    for patient in patients:
        patient_info = {
            'patient': patient,
            'checkups_count': patient.checkups.count(),
            'lab_tests_count': patient.labtests.count(),
            'treatments_count': patient.treatments.count(),
            'last_checkup': patient.checkups.first(),
        }
        patient_data.append(patient_info)
    
    context = {
        'patient_data': patient_data,
    }
    
    return render(request, 'patient_list.html', context)


def delete_patient(request, patient_id):
    """View to delete a patient"""
    patient = get_object_or_404(Patient, id=patient_id)
    
    if request.method == 'POST':
        patient_name = patient.patient_name
        patient.delete()
        messages.success(request, f'Patient record for {patient_name} has been deleted.')
        return redirect('patient_list')
    
    return render(request, 'patient_confirm_delete.html', {'patient': patient})