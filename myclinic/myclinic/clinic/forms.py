from django import forms
from django.contrib.auth.models import User



class UserForm(forms.ModelForm):
    """
    A form for creating or updating a user (patient) in the system.

    This form includes fields for the user's first name, last name, email, 
    username, and password. It also validates the uniqueness of the username 
    and email, ensuring that no user with the same credentials exists in the system.

    Attributes:
        password (CharField): A password input field for the user.
        
    Methods:
        clean_username(): Validates the username to ensure it is unique and does not contain an "@" symbol.
        clean_email(): Validates the email to ensure it is unique in the system.

    Meta:
        model (User): The model associated with this form (the User model).
        fields (list): The list of fields included in the form, which are first name, last name, email, username, and password.
    """
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username", "password"]
    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username = username).exists():
            raise forms.ValidationError("Տվյալ մուտքանունով պացիենտ արդեն գրանցված է։")
        elif "@" in username:
            raise forms.ValidationError("Մուտքանունը չի կարող պարունակել @ սիմվոլը։")
        return username
    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email = email).exists():
            raise forms.ValidationError("Տվյալ էլ․ հասցեով պացիենտ արդեն գրանցված է։")
        return email
