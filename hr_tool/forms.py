from .models import *
from django import forms

from django.contrib.auth import get_user_model
User = get_user_model()


    
class EmployeeRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
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


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'


class CourseEmployeeForm(forms.ModelForm):
    class Meta:
        model = CourseEmployee
        fields = '__all__'


class HRLoanForm(forms.ModelForm):
    class Meta:
        model = HRLoan
        fields = '__all__'


class HolidayForm(forms.ModelForm):
    start = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    class Meta:
        model = Holiday
        fields = ['employee', 'days', 'start', 'accepted', 'paid']


class ExtraWorkForm(forms.ModelForm):
    start = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    class Meta:
        model = ExtraWork
        fields = ['employee', 'days', 'start', 'notes', 'value_per_hour', 'currency']


class AdditionDiscountForm(forms.ModelForm):
    start = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    end = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    class Meta:
        model = AdditionDiscount
        fields = ['employee', 'value', 'currency', 'type', 'start', 'end']

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

