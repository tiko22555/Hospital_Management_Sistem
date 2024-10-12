from django.core.mail import send_mail
from datetime import datetime

def clinic_name_eng(clinic_name):
    dict_clinic_name = {
        "ՆՅԱՐԴԱԲԱՆԱԿԱՆ":"neuropatologist",
        "ՈՒՐՈԼՈԳԻԱԿԱՆ":"urologist",
        "ՍՐՏԱԲԱՆԱԿԱՆ":"cardiologist",
        "ՆԱՐԿՈԼՈԳԻԱԿԱՆ":"narcologist",
        "ՌևՄԱՏՈԼՈԳԻԱԿԱՆ":"rheumatologist",
        "ԳԻՆԵԿՈԼՈԳԻԱԿԱՆ":"gynecologist",
        "ՈՒՌՈՒՑՔԱԲԱՆԱԿԱՆ":"oncologist",
        "ԱՆՈԹԱՅԻՆ":"therapeutist"
    }
    return(dict_clinic_name[clinic_name])

def get_months(year):
    months_full = ['January', 'February', 'March', 'April', 'May', 'June', 
                   'July', 'August', 'September', 'October', 'November', 'December']
    
    current_year = datetime.now().year
    current_month = datetime.now().month
    
    if year == current_year:
        return months_full[current_month - 1:] 
    else:
        return months_full 
        

def send_email_to_user(patient_email, status, desc, admin_email):
    send_mail(status, desc, admin_email, [patient_email], fail_silently=False)