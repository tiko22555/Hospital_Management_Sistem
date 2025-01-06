from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

class Patient(models.Model):
    """
    A model representing a patient in the system.

    This model is linked to the `User` model through a one-to-one relationship.
    It also includes a field to indicate whether the patient is marked as deleted.

    Attributes:
        user (OneToOneField): The `User` model associated with the patient.
        is_deleted (BooleanField): A boolean field indicating whether the patient has been deleted. Defaults to False.

    Methods:
        __str__(): Returns a string representation of the patient, showing their full name.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default= False)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
admin.site.register(Patient)