from django.shortcuts import render, redirect, get_object_or_404
from ..clinic.models import Patient, Doctor, Appointment
from django.urls import reverse

    
def create_appointment(request):
    if request.user.is_authenticated:
        doctor = get_object_or_404(Doctor, user = request.user)
        doctor_id = doctor.id
        if request.method == "GET":
            return render(request, "clinic/select_email.html", {"doctor":doctor})
        else:
            patient_email = request.POST["email"]
            patient = Patient.objects.filter(user__email = patient_email).first()
            if patient:
                patient_id = patient.id
            else:
                return render(request, "clinic/select_email.html", {
                    "doctor":doctor,
                    'error': 'Տվյալ էլ․ հասցեով պացիենտ գոյություն չունի:'
                    })
            app_list = list(Appointment.objects.filter(patient = patient))
            if app_list:
                return redirect(reverse("doctor_schedule", args=(doctor_id, patient_id)))
            else:
                return render(request, "clinic/select_email.html", {
                    "doctor":doctor,
                    'error': 'Տվյալ պացիենտը դեռ չի այցելել ՌԵԱԼ ԼԱՅՖ բժշկական կենտրոն:'
                    })
    else:
        return redirect("login_")