from django.shortcuts import render, get_object_or_404
from ..clinic.models import Patient, Doctor
from datetime import datetime
from django.contrib.auth.decorators import login_required


@login_required
def appointment_success(request):
    """
    Displays a success message for a successfully registered appointment.

    Retrieves details about the doctor, patient, and appointment time from the request parameters.
    """
    patient_id = request.GET.get('patient_id')
    patient = get_object_or_404(Patient, pk = patient_id)
    doctor_id = request.GET.get('doctor_id')
    doctor = get_object_or_404(Doctor, pk = doctor_id)
    time_str = request.GET.get('time')
    appointment_time = datetime.strptime(time_str, '%Y-%m-%dT%H:%M')
    return render(request, 'clinic/appointment_success.html', {"doctor":doctor, "patient":patient, 'appointment_time': appointment_time})
