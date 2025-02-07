from django.shortcuts import render, get_object_or_404
from ..clinic.models import Clinic
import requests
from bs4 import BeautifulSoup
from ..tools import clinic_name_eng
from django.contrib.auth.decorators import login_required

def doctor_list(request, clinic_id):
    """
    Retrieves and displays a list of active doctors associated with a specific clinic.

    """
    clinic = get_object_or_404(Clinic, pk = clinic_id)
    doctors = clinic.doctor_set.all().filter(is_active=True)
    return render(request, "clinic/doctor_list.html", {"doctors":doctors, "clinic":clinic})

@login_required
def another_doctors(request, clinic_id):
    """
    Scrapes and displays additional doctors not registered in the system but associated with 
    the given clinic from an external website.

    """
    clinic = get_object_or_404(Clinic, pk = clinic_id)
    
    URL = f"https://www.doctors.am/en/doctors/{clinic_name_eng(clinic.name)}"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    item_boxes = soup.find_all('div', class_='item-box')
    list_item = []
    for item in item_boxes:
        name_ = item.find("h3", class_ = "name")
        link = name_.find("a")["href"]
        spec = item.find("div", class_= "type")
        speciality = spec.find("a").text.strip()
        name = name_.text.strip()
        list_item.append({
            "name": name,
            "link": link,
            "speciality": speciality
        })

    return render(request, "clinic/another_doctors.html", {"list_item":list_item})
