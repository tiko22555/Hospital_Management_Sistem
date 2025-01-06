from django.shortcuts import redirect, get_object_or_404
from ..clinic.models import Doctor, Appointment, Patient
from django.urls import reverse
from ..tools import send_email_to_user
from django.contrib.auth.decorators import login_required

@login_required
def cancel_appointment(request, app_id):
    """
    Cancels an appointment and sends a notification to the patient.

    If the doctor cancels the appointment, an email is sent to the patient.
    
    """
    doctor = Doctor.objects.filter(user = request.user).first()
    patient = Patient.objects.filter(user = request.user).first()
    app = get_object_or_404(Appointment, pk = app_id)
    schedule = app.schedule
    if doctor:
        patient = app.patient
        app.delete()
        send_email_to_user(patient.user.email,
                "Հանդիպման չեղարկում ֊ ՌԵԱԼ-ԼԱՅՖ",
                f"Ձեր {schedule.strftime('%Y-%m-%d %H:%M')} հանդիպումը չեղարկվել է բժիշկ {doctor}֊ի կողմից՝ զբաղվածության պատճառով։ Խնդրում ենք գրանցվել մեկ այլ ազատ ժամի։",
                'reallifecomplex2024@gmail.com'
                )
        return redirect(reverse("doctor_profile"))
    elif patient:
        app.delete()
        return redirect(reverse("patient_profile"))
    else:
        return redirect("log_out")
                