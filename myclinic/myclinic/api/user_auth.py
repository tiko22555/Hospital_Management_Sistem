from django.shortcuts import render, redirect
from ..clinic.models import Patient, Doctor
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from ..tools import send_email_to_user
from ..clinic.forms import UserForm
import random

def register(request):
    """
    Handles user registration for the clinic system.

    - Accepts POST requests with user registration data.
    - Creates a new User and a linked Patient object.
    - Sends a confirmation email to the user upon successful registration.

    """
    if not request.user.is_authenticated:
        if request.method == "POST":
            user_form = UserForm(request.POST)
            if user_form.is_valid():
                user = user_form.save(commit=False)
                user.set_password(user_form.cleaned_data['password'])
                user.save()
            
                patient = Patient(user = user)
                patient.save()
                
                send_email_to_user(patient.user.email,
                "Գրանցում՝ ՌԵԱԼ-ԼԱՅՖ",
                "Դուք հաջողությամբ գրանցվել եք ՌԵԱԼ-ԼԱՅՖ բժշկական կենտրոնի կայքում",
                'reallifecomplex2024@gmail.com'
                )
                return redirect("login_")
            return render(request, "clinic/register.html",{"user_form":user_form})
        else:
            user_form = UserForm()
            return render(request, "clinic/register.html",{"user_form":user_form})
    else:
        return redirect("log_out")
        
def login_(request):
    """
    Handles user authentication and login.

    - Supports login via username or email.
    - Redirects to the appropriate profile page (doctor or patient) upon successful login.
    - Displays error messages for invalid credentials or deleted accounts.

    """
    if not request.user.is_authenticated:
        if request.method == "GET":
            return render(request, "clinic/login.html",{})
        identifier = request.POST["identifier"]
        password = request.POST["password"]
        if "@" in identifier:
            try:
                user = User.objects.get(email = identifier)
                username = user.username
            except User.DoesNotExist:
                username = None

        else:
            username = identifier
        user = authenticate(username = username, password = password)
        if user:
            login(request, user)
            doctor = Doctor.objects.filter(user = user).first()
            patient = Patient.objects.filter(user = user, is_deleted = False).first()
            if doctor:
                return redirect("doctor_profile")
            elif patient:
                return redirect("patient_profile")
            else:
                return render(request, "clinic/login.html", {"error": "Տվյալ պրոֆիլը հեռացված է։"})
        return render(request, "clinic/login.html", {"error": "Մուտքանունը կամ գաղտնաբառը սխալ է։"})
    else:
        return redirect("log_out")
def log_out(request):
    """
    Logs out the authenticated user and redirects to the login page.

    """
    logout(request)
    return redirect("login_")
def send_email_for_reset_password(request):
    """
    Initiates the password reset process by sending a verification code to the user's email.

    - Verifies if the email belongs to a valid doctor or patient.
    - Stores the verification code and email in the session.

    """
    if request.method == "POST":
        email = request.POST["email"]
        doctor = Doctor.objects.filter(user__email = email).first()
        patient = Patient.objects.filter(user__email = email, is_deleted = False).first()
        if doctor or patient:
            code = random.randint(100000, 999999)
            request.session['reset_code'] = code 
            request.session['reset_email'] = email

            send_email_to_user(
                email,
                "Գաղտնաբառի փոփոխում՝ ՌԵԱԼ-ԼԱՅՖ",
                f"Մուտքագրեք այս կոդը գաղտնաբառի փոփոխման համար: {code}",
                'reallifecomplex2024@gmail.com'
            )
            return redirect("input_code")  
        else:
            return render(request, "clinic/send_email_for_reset_password.html", {"error": "Սխալ էլ․ հասցե"})
    return render(request, "clinic/send_email_for_reset_password.html", {})


def input_code(request):
    """
    Handles verification of the reset code sent to the user's email.

    - Compares the entered code with the session-stored code.
    - Redirects to the password reset page upon successful verification.

    """
    if 'reset_code' not in request.session:
        return redirect('send_email_for_reset_password') 

    if request.method == "POST":
        code = request.POST.get("code", "").strip() 
        right_code = request.session["reset_code"]

        if code == str(right_code):
            del request.session['reset_code'] 
            return redirect("reset_password") 

        return render(request, "clinic/input_code.html", {"error":"Սխալ կոդ!"})

    return render(request, "clinic/input_code.html", {})
def reset_password(request):
    """
    Allows the user to reset their password after successful verification.

    - Checks if the new password and confirmation match.
    - Updates the user's password and clears the reset session data.

    """
    if request.method == "POST":
        password = request.POST["password"]
        password_again = request.POST["password_again"]
        email = request.session["reset_email"]
        if password == password_again:
            user = User.objects.get(email = email)
            user.set_password(password)
            user.save()
            del request.session['reset_email']
            return redirect("login_")
        return render(request, "clinic/reset_password.html",
                    {"error": "Գաղտնաբառերը չեն համընկնում!"})
    return render(request, "clinic/reset_password.html",{})
