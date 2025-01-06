from django.shortcuts import render, get_object_or_404
from ..clinic.models import  Doctor, Appointment, Patient
from datetime import datetime
from django.contrib.auth.decorators import login_required

@login_required
def search_patient_email(request):
    """
    Allows a doctor to search for a patient by email and view their past and upcoming appointments.

    - If the provided email corresponds to a registered patient, displays the patient's appointments with the doctor.
    - If no patient is found with the given email, returns an error message.
    
    """
    doctor = get_object_or_404(Doctor, user = request.user)
    if request.method == "GET":
        return render(request, "clinic/search_patient_email.html", {"doctor":doctor})
    else:
        patient_email = request.POST["email"]
        patient = Patient.objects.filter(user__email = patient_email).first()
        if not patient:
            return render(request, "clinic/search_patient_email.html", {
                "doctor":doctor,
                'error': 'Տվյալ էլ․ հասցեով պացիենտ գոյություն չունի:'
                })
        app_list_past = list(Appointment.objects.filter(doctor = doctor, patient__user__email = patient_email, schedule__date__lte = datetime.now().date()))
        app_list = list(Appointment.objects.filter(doctor = doctor, patient__user__email = patient_email, schedule__date__gt = datetime.now().date()))
        return render(request, "clinic/appointments.html", {"app_list":app_list, "app_list_past":app_list_past, "doctor":doctor})       