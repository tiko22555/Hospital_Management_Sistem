from django.shortcuts import render, redirect, get_object_or_404
from ..clinic.models import  Doctor, Appointment, Patient
from datetime import datetime
    
def select_email(request):
    if request.user.is_authenticated:
        doctor = get_object_or_404(Doctor, user = request.user)
        if request.method == "GET":
            return render(request, "clinic/select_email.html", {"doctor":doctor})
        else:
            patient_email = request.POST["email"]
            patient = Patient.objects.filter(user__email = patient_email).first()
            if not patient:
                return render(request, "clinic/select_email.html", {
                    "doctor":doctor,
                    'error': 'Տվյալ էլ․ հասցեով պացիենտ գոյություն չունի:'
                    })
            app_list_past = list(Appointment.objects.filter(doctor = doctor, patient__user__email = patient_email, schedule__date__lte = datetime.now().date()))
            app_list = list(Appointment.objects.filter(doctor = doctor, patient__user__email = patient_email, schedule__date__gt = datetime.now().date()))
            return render(request, "clinic/appointments.html", {"app_list":app_list, "app_list_past":app_list_past, "doctor":doctor})       
    else:
        return redirect("login_")