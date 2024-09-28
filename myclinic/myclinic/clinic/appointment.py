from django.db import models
from django.contrib.auth.models import User
from .doctor import Doctor
from .patient import Patient
from django.contrib import admin

class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    schedule = models.DateTimeField()
    description = models.TextField(default="")

    def __str__(self):
        return f"Appointment: {self.patient} with {self.doctor} on {self.schedule}"
    
admin.site.register(Appointment)