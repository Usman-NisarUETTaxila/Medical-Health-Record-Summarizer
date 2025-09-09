from django.db import models

class Patient(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class PatientDetail(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    emergency_contact = models.CharField(max_length=15)
    blood_group = models.CharField(max_length=5)
    medical_history = models.TextField()

    def __str__(self):
        return f"Details of {self.patient}"


class Treatment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    treatment_name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    doctor_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.treatment_name} for {self.patient}"


class Medicine(models.Model):
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE)
    medicine_name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=50)
    duration_days = models.IntegerField()

    def __str__(self):
        return f"{self.medicine_name} for {self.treatment}"


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    doctor_name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    reason = models.TextField()

    def __str__(self):
        return f"Appointment with {self.doctor_name} for {self.patient}"
