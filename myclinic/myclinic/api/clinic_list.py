from django.shortcuts import render
from ..clinic.models import Clinic

def clinic_list(request):
    clinics = Clinic.objects.all()
    return render(request, "clinic/clinic_list.html", {"clinics":clinics})