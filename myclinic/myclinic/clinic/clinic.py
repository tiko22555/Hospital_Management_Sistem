from django.db import models
from django.contrib import admin

class Clinic(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='clinic_images/', null=True, blank=True)
    def __str__(self):
        return self.name
    
admin.site.register(Clinic)