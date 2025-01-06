from django.shortcuts import render, redirect, get_object_or_404
from ..clinic.models import Doctor, Patient
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required

@login_required
def update_doctor_info(request):
    """
    Updates the doctor's profile information, such as speciality or profile picture.

    """
    doctor = get_object_or_404(Doctor, user=request.user)

    if request.method == 'POST':
        speciality = request.POST.get('speciality')         
        profile_picture = request.FILES.get('profile_picture') 

        if speciality:
            doctor.speciality = speciality
            doctor.save() 
        elif profile_picture:
            doctor.profile_picture = profile_picture 
            doctor.save()
        return redirect("doctor_profile")

@login_required
def edit_user_info(request):
    """
    Allows users (doctors or patients) to update their account details:
    - Email
    - Username
    - Password

    - Requires authentication.
    - Validates password changes and checks if the old password matches the current password.
    - Ensures new password and confirmation match before updating.

    """
    user = request.user
    patient = Patient.objects.filter(user = request.user).first()
    doctor = Doctor.objects.filter(user = request.user).first()

    if request.method == "POST":
        email = request.POST.get("email")
        username = request.POST.get("username")
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        new_password_again = request.POST.get("new_password_again")

        if email:
            user.email = email
            user.save()

        if username:
            user.username = username
            user.save()
        
        if not old_password or not check_password(old_password, user.password):
            return render(request, "clinic/edit_user_info.html",
                        {"error": "Նախկին գաղտնաբառը սխալ է!"})

        else:
            if not new_password:
                return render(request, "clinic/edit_user_info.html",
                    {"error": "Մուտքագրեք նոր գաղտնաբառ!"})
            else:
                if new_password != new_password_again:
                    return render(request, "clinic/edit_user_info.html",
                                {"error": "Գաղտնաբառերը չեն համընկնում!"})
                else:
                    user.set_password(new_password)
                    user.save()
                    return redirect("log_out")
    
    return render(request, "clinic/edit_user_info.html", {"doctor":doctor, "patient":patient})
        




            

            
