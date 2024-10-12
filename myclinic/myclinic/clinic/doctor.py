from django.db import models
from django.contrib.auth.models import User
from .clinic import Clinic
from django.contrib import admin

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    speciality = models.CharField(max_length=50)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    profile_picture = models.ImageField(upload_to='doctor_pics/', null=True, blank=True)
    description = models.TextField(default="")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
admin.site.register(Doctor)