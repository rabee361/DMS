# users/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from django.contrib.auth import get_user_model
from django.db.models import Count
from .models import UserRole, Criteria
from itertools import groupby
from django.utils.safestring import mark_safe
User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role','upload_limit','phonenumber']



class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'role']


class UserRoleForm(forms.ModelForm):
    class Meta:
        model = UserRole
        fields = ['name','criteria']
        widgets = {
            'criteria': forms.CheckboxSelectMultiple(),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Group criteria by name
        if 'criteria' in self.fields:
            # Get all criteria and sort them by name
            criteria_qs = Criteria.objects.all().order_by('name', 'criteria_type')
            
            # Group by name (category)
            grouped_criteria = {}
            for criteria in criteria_qs:
                if criteria.name not in grouped_criteria:
                    grouped_criteria[criteria.name] = []
                
                # Create label with Arabic translation of criteria type
                type_arabic = {
                    'add': 'إضافة',
                    'edit': 'تعديل',
                    'delete': 'حذف'
                }.get(criteria.criteria_type, criteria.criteria_type)
                
                label = f"{criteria.name} - {type_arabic}"
                grouped_criteria[criteria.name].append((criteria.id, label))
            
            # Create the new choices list with category headers
            criteria_choices = []
            for category, choices in grouped_criteria.items():
                for choice in choices:
                    criteria_choices.append(choice)
            
            # Update the choices for the criteria field
            self.fields['criteria'].choices = criteria_choices


class AdminChangePasswordForm(forms.Form):
    new_password = forms.CharField(
        label="كلمة المرور الجديدة",
        widget=forms.PasswordInput
    )
    confirm_password = forms.CharField(
        label="تأكيد كلمة المرور الجديدة",
        widget=forms.PasswordInput
    )



class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(label="Password", strip=False, widget=forms.PasswordInput)
