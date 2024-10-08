from django.shortcuts import redirect, get_object_or_404
from ..clinic.models import Doctor, Appointment, Patient
from django.urls import reverse
from ..tools import send_email_to_user

    
def cancel_appointment(request, app_id):
    if request.user.is_authenticated:
        doctor = Doctor.objects.filter(user = request.user).first()
        patient = Patient.objects.filter(user = request.user).first()
        if doctor:
            app = get_object_or_404(Appointment, pk = app_id)
            doctor = app.doctor
            patient = app.patient
            schedule = app.schedule
            app.delete()
            send_email_to_user(patient.user.email,
                    "Հանդիպման չեղարկում ֊ ՌԵԱԼ-ԼԱՅՖ",
                    f"Ձեր {schedule.strftime('%Y-%m-%d %H:%M')} հանդիպումը չեղարկվել է բժիշկ {doctor}֊ի կողմից՝ զբաղվածության պատճառով։ Խնդրում ենք գրանցվել մեկ այլ ազատ ժամի։",
                    'reallifecomplex2024@gmail.com'
                    )
                    
            return redirect(reverse("doctor_profile"))
        elif patient:
            app = get_object_or_404(Appointment, pk = app_id)
            app.delete()
            return redirect(reverse("patient_profile"))
        else:
            return redirect("log_out")
    else:
        return redirect("login_")