export interface Patient {
  id: number;
  patient_name: string;
  guardian_name: string;
  age: number;
  gender: string;
  blood_group: string;
  date_of_birth: string;
  phone_number: string;
  email_address: string;
  address: string;
}

export interface MedicalHistory {
  id: number;
  patient: number;
  patient_name: string;
  past_conditions: string;
  family_history: string;
  previous_surgeries: string;
  allergies: string;
}

export interface Checkup {
  id: number;
  patient: number;
  patient_name: string;
  symptoms: string;
  current_diagnosis: string;
  date_of_checkup: string;
  blood_pressure: string;
  heart_rate: string;
  temperature: string;
  weight: string;
  height: string;
  bmi: string;
  physical_exam_findings: string;
}

export interface LabTest {
  id: number;
  patient: number;
  patient_name: string;
  lab_results: string;
  imaging: string;
  other_tests: string;
}

export interface Treatment {
  id: number;
  patient: number;
  patient_name: string;
  checkup: number;
  checkup_date: string;
  related_disease: string;
  assigned_doctor: string;
  prescribed_medications: string;
  procedures: string;
  next_followup_date: string;
  lifestyle_recommendations: string;
  physiotherapy_advice: string;
}

export interface Note {
  id: number;
  patient: number;
  patient_name: string;
  doctor_remarks: string;
  special_warnings: string;
}

export interface PatientData {
  patient: Patient;
  medical_history: MedicalHistory;
  checkups: Checkup[];
  lab_tests: LabTest[];
  treatments: Treatment[];
  notes: Note[];
}
