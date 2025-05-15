from django import forms
from .models import Currency, ExchangePrice, Account, AccountMovement


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



class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = '__all__'


class AccountMovementForm(forms.ModelForm):
    class Meta:
        model = AccountMovement
        fields = '__all__'
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'date'}),
        }

