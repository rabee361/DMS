# in here we will find a way to clean the data before inserting it in the DB
from django import forms    
from .models import CustomForm
from .cursor_db import table_exists

class AddRecordForm(forms.Form):
    record = forms.CharField(widget=forms.Textarea)


class CustomSurveyForm(forms.ModelForm):
    logo = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file', 'name': 'logo', 'id': 'id_logo'}))
    
    class Meta:
        model = CustomForm
        fields = ['name', 'title', 'welcome', 'language', 'template', 'logo']
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        
        # Check if a CustomForm with this name already exists
        if CustomForm.objects.filter(name=name).exists():
            raise forms.ValidationError("A form with this name already exists.")
        
        # Check if a table with this name already exists
        if table_exists(name):
            raise forms.ValidationError("A table with this name already exists in the database.")
        
        return name

