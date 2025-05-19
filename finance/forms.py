from django import forms
from .models import *


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


class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = '__all__'
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'date'}),
        }

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = '__all__'
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'date'}),
        }

class ExpenseForm(forms.ModelForm):
    date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'date'}))
    class Meta:
        model = Expense
        fields = '__all__'


class AccountMovementForm(forms.ModelForm):
    class Meta:
        model = AccountMovement
        fields = '__all__'
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'date'}),
        }

