# in here we will find a way to clean the data before inserting it in the DB
from django import forms    
from .models import CustomForm

class AddRecordForm(forms.Form):
    record = forms.CharField(widget=forms.Textarea)


class CustomSurveyForm(forms.ModelForm):
    class Meta:
        model = CustomForm
        fields = ['name', 'title', 'welcome', 'language']

