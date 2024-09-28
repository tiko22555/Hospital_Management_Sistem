from django.shortcuts import render, redirect
from ..clinic.models import Patient, Doctor
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from ..tools import send_email_to_patient

def register(request):
    if not request.user.is_authenticated:
        if request.method == "GET":
            return render(request, "clinic/register.html",{})
        else:
            firstname = request.POST['fname']
            lastname = request.POST['lname']
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            existing_user = User.objects.filter(username=username).first()
            existing_email = User.objects.filter(email=email).first()
            if existing_user:
                return render(request, "clinic/register.html", {'error': f'Տվյալ մուտքանունով պացիենտ արդեն գրանցված է։'})
            elif existing_email:
                return render(request, "clinic/register.html", {'error': 'Տվյալ էլ․ հասցեով պացիենտ արդեն գրանցված է։'})
            else:
                user = User.objects.create_user(
                        first_name=firstname, 
                        last_name=lastname, 
                        username = username,
                        password = password,
                        email=email)
                user.save()
                patient = Patient(user = user)
                patient.save()
                send_email_to_patient(patient.user.email,
                "Գրանցում՝ ՌԵԱԼ-ԼԱՅՖ",
                "Դուք հաջողությամբ գրանցվել եք ՌԵԱԼ-ԼԱՅՖ բժշկական կենտրոնի կայքում",
                'reallifecomplex2024@gmail.com'
                )
                return redirect("login_")
    else:
        return redirect("log_out")
        
def login_(request):
    if not request.user.is_authenticated:
        if request.method == "GET":
            return render(request, "clinic/login.html",{})
        username = request.POST["username"]
        password = request.POST["password"]
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
    logout(request)
    return redirect("login_")