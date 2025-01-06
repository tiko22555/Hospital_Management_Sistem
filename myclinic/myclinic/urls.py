"""
URL configuration for myclinic project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .api.appointment_success import appointment_success
from .api.create_appointment import create_appointment
from .api.cancel_appointment import cancel_appointment
from .api.doctor_create_appointment import doctor_create_appointment
from .api.search_date_of_appointment import search_date_of_appointment
from .api.upcoming_appointments import upcoming_appointments
from .api.search_patient_email import search_patient_email
from .api.clinic_list import clinic_list
from .api.datetime import get_days, get_hours, get_months_ajax
from .api.descriptions import appointment_description, appointment_description_edit, doctor_description
from .api.doctor_list import doctor_list, another_doctors
from .api.profiles import doctor_profile, patient_profile, profile, is_active, delete_profile
from .api.user_auth import register, login_, log_out, send_email_for_reset_password, input_code, reset_password
from .api.work_diagram import chart_view
from .api.update_info import update_doctor_info, edit_user_info
from .api.doctor_description_view import doctor_description_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", clinic_list, name = "clinic_list"),
    path("<int:clinic_id>/doctors/", doctor_list, name = "doctor_list"),
    path("<int:doctor_id>/create_appointment/", create_appointment, name = "create_appointment"),
    path("<int:doctor_id>/<int:patient_id>/create_appointment/", create_appointment, name = "create_appointment"),
    path("appointment_success/", appointment_success, name = "appointment_success"),
    path("doctor_profile/", doctor_profile, name = "doctor_profile"),
    path("register/", register, name = "register"),
    path("login_/", login_, name = "login_"),
    path("log_out/", log_out, name = "log_out"),
    path("patient_profile/", patient_profile, name = "patient_profile"),
    path("appointment_description/<app_id>/", appointment_description, name = "appointment_description"),
    path("search_date_of_appointment/", search_date_of_appointment, name = "search_date_of_appointment"),
    path("search_patient_email/", search_patient_email, name = "search_patient_email"),
    path("upcoming_appointments/", upcoming_appointments, name = "upcoming_appointments"),
    path("appointment_description_edit/<app_id>/", appointment_description_edit, name = "appointment_description_edit"),
    path("profile/", profile, name = "profile"),
    path("<int:clinic_id>/another_doctors/", another_doctors, name = "another_doctors"),
    path("cancel_appointment/<app_id>/", cancel_appointment, name = "cancel_appointment"),
    path("is_active/", is_active, name = "is_active"),
    path('get_days/', get_days, name='get_days'),
    path('get_hours/', get_hours, name='get_hours'),
    path('get_months/', get_months_ajax, name='get_months_ajax'),
    path("doctor_create_appointment/", doctor_create_appointment, name = "doctor_create_appointment"),
    path("chart_view/", chart_view, name = "chart_view"),
    path("doctor_description/", doctor_description, name = "doctor_description"),
    path('update_doctor_info/', update_doctor_info, name='update_doctor_info'),
    path("<int:doctor_id>/doctor_description_view/", doctor_description_view, name = "doctor_description_view"),
    path("delete_profile/", delete_profile, name = "delete_profile"),
    path("edit_user_info/", edit_user_info, name = "edit_user_info"),
    path("send_email_for_reset_password/", send_email_for_reset_password, name = "send_email_for_reset_password"),
    path("reset_password_code/", input_code, name = "input_code"),
    path("reset_password/", reset_password, name = "reset_password")
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
