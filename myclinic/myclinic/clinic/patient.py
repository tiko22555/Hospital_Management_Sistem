from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default= False)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
admin.site.register(Patient)