from django.db import models
from django.contrib.auth.models import User
from .clinic import Clinic
from django.contrib import admin

class Doctor(models.Model):
    """
    Represents a doctor working in a medical clinic.

    Attributes:
        user (OneToOneField): A one-to-one relationship with the User model, representing the doctor as a user in the system.
        speciality (CharField): The doctor's specialty or field of expertise.
        clinic (ForeignKey): A foreign key relationship with the Clinic model, indicating which clinic the doctor works at.
        is_active (BooleanField): A boolean indicating whether the doctor is currently active and available for appointments.
        profile_picture (ImageField, optional): An optional profile picture of the doctor.
        description (TextField): A text field that provides additional details or a description about the doctor.

    Methods:
        __str__(): Returns the full name of the doctor (first name and last name).
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    speciality = models.CharField(max_length=50)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    profile_picture = models.ImageField(upload_to='doctor_pics/', null=True, blank=True)
    description = models.TextField(default="")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
admin.site.register(Doctor)