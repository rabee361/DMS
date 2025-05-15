# in here we will find a way to clean the data before inserting it in the DB
from django import forms    
from .models import CustomForm

class AddRecordForm(forms.Form):
    record = forms.CharField(widget=forms.Textarea)


class CustomSurveyForm(forms.ModelForm):
    logo = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file', 'name': 'logo', 'id': 'id_logo'}))
    class Meta:
        model = CustomForm
        fields = ['name', 'title', 'welcome', 'language', 'template', 'logo']

