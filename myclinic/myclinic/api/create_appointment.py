from django.shortcuts import render, redirect, get_object_or_404
from ..clinic.models import Patient, Doctor, Appointment
from django.urls import reverse
from datetime import datetime
from ..tools import get_months

def create_appointment(request, doctor_id, patient_id=None):
    """
    Handles appointment scheduling for a specific doctor, allowing patients to select a date and time.

    """
    doctor = get_object_or_404(Doctor, pk=doctor_id, is_active=True)
    current_year = datetime.now().year

    if request.method == "POST":
        if request.user.is_authenticated:
            patient = Patient.objects.filter(pk=patient_id).first() or Patient.objects.filter(user=request.user).first()

            if patient:
                patient_id = patient.id
                selected_year = int(request.POST.get("year"))
                selected_month = datetime.strptime(request.POST.get('month'), '%B').month
                selected_day = request.POST.get("day_slot")
                selected_time = request.POST.get("time_slot")
                schedule = datetime.combine(
                    datetime(selected_year, selected_month, int(selected_day)), 
                    datetime.strptime(selected_time, '%H:%M').time()
                )
                context = {
                        "doctor": doctor,
                        "years": [current_year, current_year + 1],
                        "months": get_months(selected_year),
                        'error': 'Դուք արդեն գրանցված եք նշված օրը։'
                    }
                if Appointment.objects.filter(patient=patient, doctor=doctor, schedule__date=schedule.date()).exists():
                    return render(request, 'clinic/create_appointment.html', context)
                
                elif Appointment.objects.filter(patient=patient, schedule=schedule).exists():
                    context["error"] = 'Դուք արդեն գրանցված եք նշված օրը տվյալ ժամին ուրիշ բժշկի մոտ:'
                    return render(request, 'clinic/create_appointment.html', context)

                Appointment.objects.create(patient=patient, doctor=doctor, schedule=schedule)
                schedule_url = schedule.strftime('%Y-%m-%dT%H:%M')
                url = reverse("appointment_success") + f'?time={schedule_url}&doctor_id={doctor_id}&patient_id={patient_id}'
                return redirect(url)
            
            return redirect("log_out") 
        
        return redirect("login_")
    
    years = [current_year, current_year + 1]
    
    return render(request, 'clinic/create_appointment.html', {
        'doctor': doctor,
        'years': years,
        'months': get_months(current_year),
    })

