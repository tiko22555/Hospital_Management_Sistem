import matplotlib.pyplot as plt
import io
import base64
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from ..clinic.models import Appointment, Doctor
import calendar
from datetime import datetime
from django.contrib.auth.decorators import login_required

def get_appointments_by_year(doctor):
    """
    Retrieves the total number of appointments for each year for the specified doctor.

    - Creates a list of years starting from 2024 until the current year + 5.
    - For each year, counts the number of appointments for the specified doctor.

    """
    current_year = datetime.now().year
    year_list = list(range(2024, current_year + 5))
    count_list = [Appointment.objects.filter(doctor=doctor, schedule__year=year).count() for year in year_list]
    return year_list, count_list

def get_appointments_by_day(doctor, year, month):
    """
    Retrieves the total number of appointments for each day of the specified month and year.

    - Determines the number of days in the given month and year.
    - Counts the number of appointments for each day for the specified doctor.

    """
    _, last_day = calendar.monthrange(year, month)
    day_list = list(range(1, last_day + 1))
    count_list = [Appointment.objects.filter(doctor=doctor, schedule__year=year, schedule__month=month, schedule__day=day).count() for day in day_list]
    return day_list, count_list

def get_appointments_by_month(doctor, year):
    """
    Retrieves the total number of appointments for each month of the specified year.

    - Creates a list of months from January to December.
    - Counts the number of appointments for each month for the specified doctor.

    """
    month_list = list(range(1, 13))
    count_list = [Appointment.objects.filter(doctor=doctor, schedule__year=year, schedule__month=month).count() for month in month_list]
    return month_list, count_list

def generate_bar_chart(labels, values, title):
    """
    Generates a bar chart for the given labels and values and encodes it in base64.

    - Creates a bar chart using Matplotlib, displaying the number of appointments.
    - Converts the chart into a base64 encoded PNG image.

    """
    fig, ax = plt.subplots(figsize=(12.96, 4.5))
    fig.patch.set_facecolor('#27f1bb')
    ax.set_facecolor('#8ffcdf')
    ax.bar(labels, values)
    ax.set_ylabel('Հանդիպումների քանակը')
    ax.set_title(title)
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close(fig)
    
    return f"data:image/png;base64,{image_base64}"

@login_required
def chart_view(request):
    """
    Displays a bar chart of appointments for a specific doctor based on user input.

    - Handles both GET and POST requests.
    - If a year and/or month is selected via POST, generates a chart based on those filters.
    - Returns the chart as a base64-encoded image or renders the page with the chart.
    
    """
    doctor = get_object_or_404(Doctor, user=request.user)

    if request.method == "POST":
        year_slot = request.POST.get('year')
        month_slot = request.POST.get('month')        

        if year_slot and not month_slot:
            labels, values = get_appointments_by_month(doctor, int(year_slot))
            labels = [calendar.month_name[m][:3] for m in labels]
            title = f"Բժիշկ {doctor}ի {year_slot}թ․֊ի զբաղվածության գրաֆիկ"
        elif year_slot and month_slot:
            labels, values = get_appointments_by_day(doctor, int(year_slot), int(month_slot))
            labels = [str(d) for d in labels]
            title = f"Բժիշկ {doctor}ի {year_slot}թ․֊ի {calendar.month_name[int(month_slot)]} ամսի զբաղվածության գրաֆիկ"
        else:
            labels, values = get_appointments_by_year(doctor)
            title = f"Բժիշկ {doctor}ի ընդհանուր զբաղվածության գրաֆիկ"

        image_base64 = generate_bar_chart(labels, values, title)
        return JsonResponse({"image_url": image_base64})

    labels, values = get_appointments_by_year(doctor)
    title = f"Բժիշկ {doctor}ի ընդհանուր զբաղվածության գրաֆիկ"
    image_base64 = generate_bar_chart(labels, values, title)
    return render(request, 'clinic/diagram.html', {
            'chart_image': image_base64,
            'year_list': labels,
            'month_list': [calendar.month_name[m][:3] for m in range(1, 13)],
            'current_year': datetime.now().year
        })

