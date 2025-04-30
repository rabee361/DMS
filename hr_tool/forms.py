from .models import *
from django import forms

from django.contrib.auth import get_user_model
User = get_user_model()


    
class EmployeeRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Employee
        exclude = ['last_login','date_joined','groups','user_permissions']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        
        return cleaned_data
    
    
class EmployeeUpdateForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = ['last_login','date_joined','password','is_superuser','is_staff','groups','user_permissions']


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = '__all__'


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'


class HolidayForm(forms.ModelForm):
    start = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    end = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    class Meta:
        model = Holiday
        fields = ['employee', 'hours', 'start', 'end', 'accepted']



class AbsenceForm(forms.ModelForm):
    start = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    end = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    
    class Meta:
        model = Absence
        fields = ['start', 'end', 'reason', 'employee']


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name']


class WorkGoalForm(forms.ModelForm):
    class Meta:
        model = WorkGoal
        exclude = ['created']


class HRSettingsForm(forms.ModelForm):
    class Meta:
        model = HRSettings
        fields = '__all__'

