import matplotlib.pyplot as plt
import io
import base64
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from ..clinic.models import Appointment, Doctor
import calendar
from datetime import datetime

def get_appointments_by_year(doctor):
    current_year = datetime.now().year
    year_list = list(range(2024, current_year + 2))
    count_list = [Appointment.objects.filter(doctor=doctor, schedule__year=year).count() for year in year_list]
    return year_list, count_list

def get_appointments_by_day(doctor, year, month):
    _, last_day = calendar.monthrange(year, month)
    day_list = list(range(1, last_day + 1))
    count_list = [Appointment.objects.filter(doctor=doctor, schedule__year=year, schedule__month=month, schedule__day=day).count() for day in day_list]
    return day_list, count_list

def get_appointments_by_month(doctor, year):
    month_list = list(range(1, 13))
    count_list = [Appointment.objects.filter(doctor=doctor, schedule__year=year, schedule__month=month).count() for month in month_list]
    return month_list, count_list

def generate_bar_chart(labels, values, title):
    fig, ax = plt.subplots(figsize=(12.96, 5))
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

def chart_view(request):
    if request.user.is_authenticated:
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
                if len(labels) <= 4:
                    labels = [str(label)for label in labels]  
                    title = f"Բժիշկ {doctor}ի ընդհանուր զբաղվածության գրաֆիկ"
                else:
                    title = f"Բժիշկ {doctor}ի ընդհանուր զբաղվածության գրաֆիկ"

            image_base64 = generate_bar_chart(labels, values, title)
            return JsonResponse({"image_url": image_base64})

        labels, values = get_appointments_by_year(doctor)
        if len(labels) <= 4:
            labels = [str(label)for label in labels]
            
            title = f"Բժիշկ {doctor}ի ընդհանուր զբաղվածության գրաֆիկ"
        else:
            title = f"Բժիշկ {doctor}ի ընդհանուր զբաղվածության գրաֆիկ"
        image_base64 = generate_bar_chart(labels, values, title)
        return render(request, 'clinic/diagram.html', {
            'chart_image': image_base64,
            'year_list': labels,
            'month_list': [calendar.month_name[m][:3] for m in range(1, 13)],
            'current_year': datetime.now().year
        })
    return redirect("login_")
