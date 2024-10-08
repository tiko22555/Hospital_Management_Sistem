from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from ..clinic.models import Doctor, Appointment
from datetime import datetime
import calendar
from ..tools import get_months

def get_days(request):
    year = int(request.GET.get('year'))
    month = datetime.strptime(request.GET.get('month'), '%B').month
    
    if month and 1 <= month <= 12:
        _, last_day = calendar.monthrange(year, month)
        if datetime.now().month == month:
            days = list(range(datetime.now().day, last_day + 1))
            if datetime.now().time().hour +4 >= 17:
                days.pop(0)
        else:
            days = list(range(1, last_day + 1))
        return JsonResponse({'days': days})
    
    return JsonResponse({'days': []})

def get_hours(request):
    selected_month = datetime.strptime(request.GET.get('month'), '%B').month
    selected_day = request.GET.get('day')
    doctor_id = request.GET.get('doctor_id')
    
    if selected_month and selected_day and doctor_id:
        doctor = get_object_or_404(Doctor, pk=doctor_id)
        selected_date = datetime(datetime.now().year, selected_month, int(selected_day)).date()
        start_time = "10:00"
        end_time = "18:00"
        time_slots = []
        
        while int(start_time[:2]) <= int(end_time[:2]):
            time_slots.append(start_time)
            start_time = str(int(start_time[:2]) + 1) + start_time[2:]
        
        existing_appointments = Appointment.objects.filter(doctor=doctor, schedule__date=selected_date)
        booked_slots = [appt.schedule.strftime('%H:%M') for appt in existing_appointments]
        available_slots = [slot for slot in time_slots if slot not in booked_slots]
        
        if selected_date == datetime.today().date():
            available_slots = [slot for slot in available_slots if int(slot[:2]) > datetime.now().hour + 5]
        
        return JsonResponse({'hours': available_slots})
    
    return JsonResponse({'hours': []})

def get_months_ajax(request):
    year = int(request.GET.get('year'))
    months = get_months(year)
    return JsonResponse({'months': months})
