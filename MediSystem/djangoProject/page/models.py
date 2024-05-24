from django.db import models

class Hospital(models.Model):
    hospital_id = models.AutoField(primary_key=True)
    hospital_name = models.CharField(max_length=100)
    hospital_address = models.CharField(max_length=255)

class Doctor(models.Model):
    doctor_id = models.AutoField(primary_key=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    tckn = models.CharField(max_length=12)
    date_of_birth = models.CharField(max_length=50)
    profession = models.CharField(max_length=50)

class Manager(models.Model):
    id = models.AutoField(primary_key=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    tckn = models.CharField(max_length=12)
    date_of_birth = models.CharField(max_length=50)

class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    tckn = models.CharField(max_length=12)
    date_of_birth = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    tel_no = models.CharField(max_length=50)
    address = models.CharField(max_length=100)

class Appointment(models.Model):
    appointment_id = models.AutoField(primary_key=True)
    appointment_date = models.CharField(max_length=50)
    appointment_time = models.CharField(max_length=50)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
