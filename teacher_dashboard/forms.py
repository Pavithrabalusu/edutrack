from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Student
from .models import Profile

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))

class UploadFileForm(forms.Form):
    file = forms.FileField()

# ✅ NEW: Add Student Form
class AddStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'age', 'studytime', 'failures', 'absences', 'g1', 'g2', 'g3']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Student Full Name'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'studytime': forms.NumberInput(attrs={'class': 'form-control'}),
            'failures': forms.NumberInput(attrs={'class': 'form-control'}),
            'absences': forms.NumberInput(attrs={'class': 'form-control'}),
            'g1': forms.NumberInput(attrs={'class': 'form-control'}),
            'g2': forms.NumberInput(attrs={'class': 'form-control'}),
            'g3': forms.NumberInput(attrs={'class': 'form-control'}),
        }

from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']