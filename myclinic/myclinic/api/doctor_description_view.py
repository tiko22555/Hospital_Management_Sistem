from django.shortcuts import render, get_object_or_404
from ..clinic.models import Doctor

def doctor_description_view(request, doctor_id):
    doctor = get_object_or_404(Doctor, pk = doctor_id)
    return render(request, "clinic/doctor_description_view.html", {"doctor":doctor})