from django.shortcuts import render, get_object_or_404
from ..clinic.models import  Doctor, Appointment
from datetime import datetime
import calendar
from django.contrib.auth.decorators import login_required

@login_required
def search_date_of_appointment(request):
    """
    Allows a doctor to select a specific date and view appointments for that date.
    
    """
    doctor = get_object_or_404(Doctor, user=request.user)
    current_year = datetime.now().year
    current_month = datetime.now().month

    year_list = list(range(2024, current_year + 2))

    if request.method == "POST":
        year = int(request.POST.get("year"))
        month = int(request.POST.get("month"))
    else:
        year = current_year
        month = current_month
        
    month_list = list(range(1, 13))
    
    days_in_month = calendar.monthrange(year, month)[1]
    day_list = list(range(1, days_in_month + 1))

    if request.method == "POST" and "day" in request.POST:
        day = int(request.POST.get("day"))
        date = datetime(year, month, day)
        if date.date() <= datetime.now().date():
            app_list_past = list(Appointment.objects.filter(doctor=doctor, schedule__date=date))
            return render(request, "clinic/appointments.html", {"app_list_past": app_list_past, "doctor": doctor})
        else:
            app_list = list(Appointment.objects.filter(doctor=doctor, schedule__date=date))
            return render(request, "clinic/appointments.html", {"app_list": app_list, "doctor": doctor})

    return render(request, "clinic/search_date_of_appointment.html", {
        "year_list": year_list,
        "month_list": month_list,
        "day_list": day_list,
        "selected_year": year,
        "selected_month": month,
        "doctor": doctor
    })

       