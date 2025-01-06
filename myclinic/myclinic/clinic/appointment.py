from django.db import models
from .doctor import Doctor
from .patient import Patient
from django.contrib import admin

class Appointment(models.Model):
    """
    Represents a medical appointment between a doctor and a patient.

    Attributes:
        doctor (ForeignKey): The doctor associated with the appointment.
        patient (ForeignKey): The patient associated with the appointment.
        schedule (DateTimeField): The scheduled date and time of the appointment.
        description (TextField): Additional information or notes about the appointment.

    Methods:
        __str__(): Returns a string representation of the appointment, including the patient, doctor, and schedule time.
    """
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    schedule = models.DateTimeField()
    description = models.TextField(default="")

    def __str__(self):
        return f"Appointment: {self.patient} with {self.doctor} on {self.schedule}"
    
admin.site.register(Appointment)