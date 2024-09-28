from django.shortcuts import render, redirect, get_object_or_404
from ..clinic.models import Doctor

def update_doctor_info(request):
    if request.user.is_authenticated:
        doctor = get_object_or_404(Doctor, user=request.user)

        if request.method == 'POST':
            speciality = request.POST.get('speciality')
            email = request.POST.get('email')
            profile_picture = request.FILES.get('profile_picture') 

            if speciality:
                doctor.speciality = speciality

            if email:
                doctor.user.email = email
                doctor.user.save()

            if profile_picture:
                doctor.profile_picture = profile_picture 
                doctor.save()

            doctor.save() 

            return redirect('doctor_profile')

        return render(request, 'clinic/doctor_profile.html', {'doctor': doctor})
    return redirect("login_")

