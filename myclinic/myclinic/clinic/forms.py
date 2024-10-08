from django import forms
from django.contrib.auth.models import User



class UserForm(forms.ModelForm):
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