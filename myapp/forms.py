from django import forms

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User

from myapp.models import Task




class TaskForm(forms.ModelForm):

    
    class Meta:

        model = Task

        fields = ["title","due_date","status"]

        widgets = {
            "title":forms.TextInput(attrs={"class":"form-control mb-2"}),
            'due_date': forms.DateTimeInput(attrs={'class': 'form-control mb-2',
                                                    'type': 'datetime-local'}),
            "status":forms.CheckboxInput(attrs={'class': 'form-check-input mb-2'})
            
        }



class RegistrationForm(UserCreationForm):

    password1=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control mb-3"}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control mb-3"}))

    class Meta:

        model = User

        fields = ["username","password1","password2"]

        widgets = {
            "username":forms.TextInput(attrs={"class":"form-control"})
            }
        
        
class LoginForm(forms.Form):

    username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control mb-2"}))

    password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control mb-2"}))