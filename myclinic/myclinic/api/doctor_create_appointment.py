from django.shortcuts import render, redirect, get_object_or_404
from ..clinic.models import Patient, Doctor, Appointment
from django.urls import reverse
from django.contrib.auth.decorators import login_required

@login_required
def doctor_create_appointment(request):
    """
    Doctor registers a patient for an appointment if the patient is already registered 
    in the system and has visited the clinic at least once.

    If the patient does not exist or has never visited, the function returns appropriate error messages.

    """
    doctor = get_object_or_404(Doctor, user = request.user)
    doctor_id = doctor.id
    if request.method == "GET":
        return render(request, "clinic/search_patient_email.html", {"doctor":doctor})
    else:
        patient_email = request.POST["email"]
        patient = Patient.objects.filter(user__email = patient_email).first()
        if patient:
            patient_id = patient.id
        else:
            return render(request, "clinic/search_patient_email.html", {
                "doctor":doctor,
                'error': 'Տվյալ էլ․ հասցեով պացիենտ գոյություն չունի:'
                })
        app_list = list(Appointment.objects.filter(patient = patient))
        if app_list:
            return redirect(reverse("create_appointment", args=(doctor_id, patient_id)))
        else:
            return render(request, "clinic/search_patient_email.html", {
                "doctor":doctor,
                'error': 'Տվյալ պացիենտը դեռ չի այցելել ՌԵԱԼ ԼԱՅՖ բժշկական կենտրոն:'
                })
