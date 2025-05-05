from django import forms
from .models import Currency, ExchangePrice


class CurrencyForm(forms.ModelForm):
    class Meta:
        model = Currency
        fields = '__all__'

class ExchangePriceForm(forms.ModelForm):
    class Meta:
        model = ExchangePrice
        fields = '__all__'
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'date'}),
        }