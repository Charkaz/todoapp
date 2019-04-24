from django import forms
from .models import newtasks,serhs

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=50,label="istifadeci adi " )
    email = forms.EmailField(max_length=50,label="Email")
    password = forms.CharField(max_length=50,label="Sifre",widget=forms.PasswordInput)
    confirm = forms.CharField(max_length=50,label="Tekrar sifre",widget=forms.PasswordInput)
    

    def clean(self):
        username = self.cleaned_data.get("username")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")

        if password and confirm and password != confirm:
            raise forms.ValidationError("Sifreler uygun deyil !")

        values ={
            'username':username,
            'email':email,
            'password':password
        }

        return values

class LoginUser(forms.Form):
    username = forms.CharField(max_length=50, label="istifadeci")
    password = forms.CharField(max_length=50 , label="sifre",widget=forms.PasswordInput)


class Paylas(forms.Form):
    
    username = forms.CharField(max_length=50 , label="username")




class addTask(forms.ModelForm):
    class Meta:
        model = newtasks
        fields = ['title','text','deadline']


class addComent(forms.ModelForm):
    class Meta:
        model = serhs
        fields = ['serh']