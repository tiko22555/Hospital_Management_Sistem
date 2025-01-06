from django.db import models
from django.contrib import admin

class Clinic(models.Model):
    """
    Represents a medical clinic.

    Attributes:
        name (CharField): The name of the clinic.
        image (ImageField, optional): An optional image associated with the clinic.

    Methods:
        __str__(): Returns the name of the clinic.
    """
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='clinic_images/', null=True, blank=True)
    def __str__(self):
        return self.name
    
admin.site.register(Clinic)